import os
from typing import Literal
import inspect
import shutil
import json
from dataclasses import dataclass, asdict
import numpy as np
import sktopt
from sktopt import tools
from sktopt.core.optimizers import common
from sktopt.core import derivatives, projection
from sktopt.core import visualization
from sktopt.mesh import visualization as visualization_mesh
from sktopt.fea import solver
from sktopt import filter
from sktopt.fea import composer
from sktopt.core import misc
from sktopt.tools.logconf import mylogger
logger = mylogger(__name__)



@dataclass
class Evolutionary_Config(common.DensityMethodConfig):
    interpolation: Literal["SIMP"] = "SIMP"
    population_size: int = 30
    offspring_size: int = 60
    n_generations: int = 100
    mutation_strength: float = 0.1
    elite_size: int = 5


def generate_initial_population(
    cfg: Evolutionary_Config, n_variables: int,
    vol_frac: float
):
    pop = np.random.rand(cfg.population_size, n_variables)
    pop = enforce_volume_constraint(pop, cfg, n_variables, vol_frac)
    return pop


def enforce_volume_constraint(
    pop,
    cfg: Evolutionary_Config, n_variables: int,
    vol_frac: float
):
    # 各個体がvol_fracを満たすようにスケーリング
    return np.minimum(pop, 1.0) * (
        vol_frac * n_variables
    ) / np.maximum(pop.sum(axis=1, keepdims=True), 1e-8)


def mutate(x, cfg: Evolutionary_Config):
    child = x + cfg.mutation_strength * np.random.randn(*x.shape)
    return np.clip(child, 0.0, 1.0)


class Evolutionary_Optimizer(common.DensityMethod):
    """
    """
    def __init__(
        self,
        cfg: Evolutionary_Config,
        tsk: sktopt.mesh.TaskConfig,
    ):
        assert cfg.lambda_lower < cfg.lambda_upper
        super().__init__(cfg, tsk)


    def init_schedulers(self, export: bool = True):

        cfg = self.cfg
        p_init = cfg.p_init
        vol_frac_init = cfg.vol_frac_init
        move_limit_init = cfg.move_limit_init
        beta_init = cfg.beta_init
        self.schedulers.add(
            "p",
            p_init,
            cfg.p,
            cfg.p_step,
            cfg.max_iters
        )
        self.schedulers.add(
            "vol_frac",
            vol_frac_init,
            cfg.vol_frac,
            cfg.vol_frac_step,
            cfg.max_iters
        )
        self.schedulers.add(
            "filter_radius",
            cfg.filter_radius_init,
            cfg.filter_radius,
            cfg.filter_radius_step,
            cfg.max_iters
        )
        if export:
            self.schedulers.export()

    def parameterize(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_defaults(
            self.tsk.mesh,
            self.cfg.filter_radius,
            solver_option="cg_pyamg",
            # solver_option=self.cfg.solver_option,
            dst_path=f"{self.cfg.dst_path}/data",
        )

    def load_parameters(self):
        self.helmholz_solver = filter.HelmholtzFilter.from_file(
            f"{self.cfg.dst_path}/data"
        )

    # def initialize_density(self):
    #     tsk = self.tsk
    #     cfg = self.cfg
    #     val_init = cfg.vol_frac_init
    #     rho = np.zeros_like(tsk.all_elements, dtype=np.float64)
    #     iter_begin = 1
    #     if cfg.restart is True:
    #         if cfg.restart_from > 0:
    #             data_dir = f"{cfg.dst_path}/data"
    #             data_fname = f"{cfg.restart_from:06d}-rho.npz"
    #             data_path = f"{data_dir}/{data_fname}"
    #             data = np.load(data_path)
    #             iter_begin = cfg.restart_from + 1
    #         else:
    #             iter, data_path = misc.find_latest_iter_file(
    #                 f"{cfg.dst_path}/data"
    #             )
    #             data = np.load(data_path)
    #             iter_begin = iter + 1
    #         iter_end = cfg.max_iters + 1
    #         self.recorder.import_histories()
    #         rho[tsk.design_elements] = data["rho_design_elements"]
    #         del data
    #     else:
    #         rho += val_init
    #         np.clip(rho, cfg.rho_min, cfg.rho_max, out=rho)
    #         iter_end = cfg.max_iters + 1

    #     if cfg.design_dirichlet is True:
    #         rho[tsk.force_elements] = 1.0
    #     else:
    #         rho[tsk.dirichlet_force_elements] = 1.0
    #     rho[tsk.fixed_elements] = 1.0
    #     return rho, iter_begin, iter_end

    def initialize_params(self):
        tsk = self.tsk
        cfg = self.cfg
        rho, iter_begin, iter_end = self.initialize_density()
        n_variables = rho.shape[0]
        population = generate_initial_population(cfg, n_variables, cfg.vol_frac_init)
        force_list = tsk.force if isinstance(tsk.force, list) else [tsk.force]
        u_dofs = np.zeros((tsk.basis.N, len(force_list)))
        
        return (
            iter_begin,
            iter_end,
            population,
            n_variables,
            force_list,
            u_dofs
        )
        
    def get_compliance(
        self,
        rho,
        p,
        force_list,
        u_dofs,
        density_interpolation,
    ) -> float:
        rho_projected = rho
        compliance_avg = solver.compute_compliance_basis_multi_load(
            self.tsk.basis, self.tsk.free_dofs, self.tsk.dirichlet_dofs,
            force_list,
            cfg.E0, cfg.E_min, p, tsk.nu,
            rho_projected,
            u_dofs,
            elem_func=density_interpolation,
            solver=cfg.solver_option
        )
        
        return compliance_avg / len(force_list)


    def get_strain_energy(
        self,
        rho,
        p,
        force_list,
        u_dofs,
        density_interpolation,
    ) -> float:
        rho_projected = rho
        strain_energy = composer.strain_energy_skfem_multi(
            tsk.basis, rho_projected, u_dofs,
            cfg.E0, cfg.E_min, p, tsk.nu,
            elem_func=density_interpolation
        )
        return strain_energy / len(force_list)
    
    
    def get_metrics(
        self,
        rho,
        p,
        force_list,
        u_dofs,
        density_interpolation
    ) -> float:
        compliance = self.get_compliance(
            rho,
            p,
            force_list,
            u_dofs,
            density_interpolation
        )
        return compliance

    def optimize(self):
        tsk = self.tsk
        cfg = self.cfg
        tsk.export_analysis_condition_on_mesh(cfg.dst_path)
        logger.info(f"dst_path : {cfg.dst_path}")
        self.init_schedulers()
        density_interpolation = composer.simp_interpolation
        # dC_drho_func = derivatives.dC_drho_simp
        (
            iter_begin,
            iter_end,
            population,
            n_variables,
            force_list,
            u_dofs
        ) = self.initialize_params()
        elements_volume_design = tsk.elements_volume[tsk.design_elements]
        elements_volume_design_sum = np.sum(elements_volume_design)
        # self.helmholz_solver.update_radius(
        #     tsk.mesh, filter_radius_prev, solver_option="cg_pyamg"
        # )
        
        tsk = self.tsk
        cfg = self.cfg
        
        fitness = np.array(
            [
                self.get_metrics(
                    rho,
                    p,
                    force_list,
                    u_dofs,
                    density_interpolation
                ) for rho in population
            ]
        )

        # for generation in range(n_generations):
        for iter_loop, iter in enumerate(range(iter_begin, iter_end)):
            logger.info(f"iterations: {iter} / {iter_end - 1}")
            (
                p,
                vol_frac,
                filter_radius
            ) = self.schedulers.values_as_list(
                iter,
                [
                    'p', 'vol_frac', 'filter_radius'
                ],
                export_log=True,
                precision=6
            )
            
            # Select Elite
            elite_indices = np.argsort(fitness)[:cfg.elite_size]
            elite = population[elite_indices]

            # Generating offspring by mutating selected elite individuals
            offspring = []
            while len(offspring) < cfg.offspring_size:
                parent_idx = np.random.choice(cfg.elite_size)
                child = mutate(elite[parent_idx], cfg)
                offspring.append(child)

            offspring = np.array(offspring)
            offspring = enforce_volume_constraint(
                offspring, cfg, n_variables, vol_frac
            )

            offspring_fitness = np.array(
                [
                    self.get_metrics(
                        rho,
                        p,
                        force_list,
                        u_dofs,
                        density_interpolation
                    ) for rho in offspring
                ]
            )

            # Select Next Generation (μ+λ)
            total_fitness = np.concatenate([fitness, offspring_fitness])
            best_indices = np.argsort(total_fitness)[:cfg.population_size]
            total_population = np.vstack([population, offspring])
            population = total_population[best_indices]
            fitness = total_fitness[best_indices]
            
            # population[:cfg.offspring_size] = offspring
            # fitness[:cfg.offspring_size] = offspring_fitness
            # best_indices = np.argsort(fitness)[:cfg.population_size]
            # population = population[best_indices]
            # fitness = fitness[best_indices]

            if any(
                (iter % (cfg.max_iters // cfg.record_times) == 0,
                 iter == 1)
            ):
                # print(f"Generation {generation}: Best compliance = {fitness[0]:.4e}")
                pass

        best_solution = population[0]
        return best_solution, fitness[0]



if __name__ == '__main__':
    import argparse
    from sktopt.mesh import toy_problem

    parser = argparse.ArgumentParser(
        description=''
    )
    parser = misc.add_common_arguments(parser)
    parser.add_argument(
        '--mu_p', '-MUP', type=float, default=100.0, help=''
    )
    parser.add_argument(
        '--lambda_v', '-LV', type=float, default=1.0, help=''
    )
    parser.add_argument(
        '--lambda_decay', '-LD', type=float, default=0.95, help=''
    )
    args = parser.parse_args()

    if args.task_name == "toy1":
        tsk = toy_problem.toy1()
    elif args.task_name == "toy1_fine":
        tsk = toy_problem.toy1_fine()
    elif args.task_name == "toy2":
        tsk = toy_problem.toy2()
    else:
        tsk = toy_problem.toy_msh(args.task_name, args.mesh_path)

    print("load toy problem")
    print("generate LogMOC_Config")
    cfg = Evolutionary_Config.from_defaults(
        **vars(args)
    )

    print("optimizer")
    optimizer = Evolutionary_Optimizer(cfg, tsk)
    print("parameterize")
    optimizer.parameterize()
    # optimizer.parameterize(preprocess=False)
    # optimizer.load_parameters()
    print("optimize")
    optimizer.optimize()
    # optimizer.optimize_org()
