"""SCVx* algorithm"""

import copy
import numpy as np
import time


class SCPSolution:
    """Solution structure for SCvx* algorithm

    The solution structure is to the non-convex OCP of the form:

    min_{x,u,v,y} J(x,u,v,y)
    s.t. 
        x_{k+1} = x_k + f(x_k,u_k,v_k,y_k)
        ||u_k|| <= v_k
        g(x,u,v,y) = 0
        h(x,u,v,y) <= 0
    
    Attributes:
        x (np.array): optimal state trajectory
        u (np.array): optimal control trajectory
        v (np.array): optimal control magnitude terms
        y (np.array): optimal general variables
        sols (list): list of solutions
        summary_dict (dict): summary dictionary
    """
    def __init__(self, xopt, uopt, vopt, yopt, sols, summary_dict, variables_each_iterations=None):
        self.x = xopt
        self.u = uopt
        self.v = vopt
        self.y = yopt
        self.sols = sols
        self.summary_dict = summary_dict
        self.variables_each_iterations = variables_each_iterations
        return


class SCvxStar:
    """SCvx* algorithm for optimal control problems

    Hyperparameters are defined according to `Oguri, 2023` (doi: 10.1109/CDC49753.2023.10383462).

    Args:
        problem (ContinuousControlSCOCP or ImpulsiveControlSCOCP): `SCOCP` instance
        tol_opt (float): optimality tolerance
        tol_feas (float): feasibility tolerance
        rho0 (float): step acceptance criterion parameter
        rho1 (float): trust-region radius contraction threshold
        rho2 (float): trust-region radius expansion threshold
        alpha1 (float): trust-region radius contraction factor s.t. r_k+1 = max(r_k/alpha1, r_bounds[0])
        alpha2 (float): trust-region radius expansion factor s.t. r_k+1 = min(r_k*alpha2, r_bounds[1])
        beta (float): weight update factor
        gamma (float): update factor forLagrange multiplier update criterion delta
        r_bounds (list): trust region bounds
        weight_max (float): maximum weight
    """
    def __init__(
        self,
        problem,
        tol_opt = 1e-6,
        tol_feas = 1e-6,
        rho0 = 0.0,
        rho1 = 0.25,
        rho2 = 0.7,
        alpha1 = 2.0,
        alpha2 = 3.0,
        beta = 2.0,
        gamma = 0.9,
        r_bounds = [1e-8, 10.0],
        steps_minimum_trust_region = 10,
        weight_max = 1e16,
    ):
        # assertions on hyperparameters
        assert 0.0 <= rho0 < 1.0, "rho0 must be in [0.0, 1.0)"
        assert alpha1 > 1.0, "alpha1 must be greater than 1.0"
        assert alpha2 > 1.0, "alpha2 must be greater than 1.0"
        assert rho1 < rho2, "rho1 must be less than rho2"
        assert beta > 1.0, "beta must be greater than 1.0"
        assert 0.0 < gamma < 1.0, "gamma must be in (0.0, 1.0)"
        assert r_bounds[0] > 0.0, "r_bounds[0] must be greater than 0.0"
        assert r_bounds[1] > r_bounds[0], "r_bounds[1] must be greater than r_bounds[0]"
        
        self.problem = problem
        self.tol_opt = tol_opt
        self.tol_feas = tol_feas
        self.rho0 = rho0
        self.rho1 = rho1
        self.rho2 = rho2
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.beta = beta
        self.gamma = gamma
        self.r_bounds = r_bounds
        self.steps_minimum_trust_region = steps_minimum_trust_region
        self.weight_max = weight_max
        return
    

    def evaluate_penalty(self, gdyn, g, h):
        """Evaluate penalty function according to Augmented Lagrangian formulation
        
        Args:
            gdyn (np.array): (N-1)-by-nx array of nonlinear dynamics constraints violations
            g (np.array): ng-by-1 array of nonlinear equality constraints violations
            h (np.array): nh-by-1 array of nonlinear inequality constraints violations
        """
        assert gdyn.shape == (self.problem.N-1, self.problem.integrator.nx),\
            f"gdyn.shape = {gdyn.shape} != (self.problem.N-1, self.problem.integrator.nx) = {(self.problem.N-1, self.problem.integrator.nx)}"
        Nseg,_ = self.problem.lmb_dynamics.shape
        penalty = 0.0
        for i in range(Nseg):
            penalty += self.problem.lmb_dynamics[i,:] @ gdyn[i,:] + self.problem.weight/2 * gdyn[i,:] @ gdyn[i,:]
        if self.problem.ng > 0:
            assert g.shape == (self.problem.ng,)
            penalty += self.problem.lmb_eq @ g + self.problem.weight/2 * (g @ g)
        if self.problem.nh > 0:
            assert h.shape == (self.problem.nh,)
            h_pos = np.clip(h, 0, None)      # penalize only when inequality constraint is violated
            penalty += self.problem.lmb_ineq @ h_pos + self.problem.weight/2 * (h_pos @ h_pos)
        return penalty
    
    
    def solve(
        self,
        xbar,
        ubar,
        vbar = None,
        ybar = None,
        maxiter: int = 10,
        verbose: bool = True,
        feasability_norm = np.inf,
        debug = False,
        exit_condition_rho = False,
        save_all_iterations = False,
    ):
        """Solve optimal control problem via SCvx* algorithm
        
        Args:
            xbar (np.array): N-by-nx array of reference states
            ubar (np.array): N-by-nu array of reference controls
            vbar (np.array): N-by-1 array of reference constraints
            maxiter (int): maximum number of iterations
            verbose (bool): whether to print verbose output
            feasability_norm (str): norm to use for feasibility evaluation
            debug (bool): whether to print debug output
            exit_condition_rho (bool): whether to exit if rho < rho0
            save_all_iterations (bool): whether to save all iterations

        Returns:
            SCPSolution: solution object
        """
        tstart = time.time()
        header = f"|  Iter  |     J0      |   Delta J   |   Delta L   |    chi     |     rho     |     r      |   weight   | step acpt. |"
        print_frequency = 10
        delta = 1e16
        status_AL = "NotConverged"
        chi = 1e15
        rho = self.rho0  # initialize rho to rho0
        n_min_trust_region = 0
        sols = []

        # initialize vbar if not provided
        if vbar is None:
            assert self.problem.augment_Gamma == False, f"If augment_Gamma is True, vbar must be provided"
            # vbar = np.sum(ubar, axis=1).reshape(-1,1)
        if ybar is None and self.problem.ny > 0:
            ybar = np.zeros((self.problem.ny,))

        # initial constraint violation evaluation
        gdyn_nl_bar, _ = self.problem.evaluate_nonlinear_dynamics(xbar, ubar, vbar)
        g_nl_bar, h_nl_bar = self.problem.evaluate_nonlinear_constraints(xbar, ubar, vbar, ybar)
        assert g_nl_bar.shape == (self.problem.ng,),\
            f"Shape of equality constraint violations by self.problem.evaluate_nonlinear_constraints does not match (self.problem.ng,)"
        assert h_nl_bar.shape == (self.problem.nh,),\
            f"Shape of inequality constraint violations by self.problem.evaluate_nonlinear_constraints does not match (self.problem.nh,)"

        # initialize summary dictionary
        scp_summary_dict = {
            "num_iter": 0,
            "status": "NotConverged",
            "J0": [],
            "chi": [],
            "DeltaJ": [],
            "DeltaL": [],
            "accept": [],
            "weight": self.problem.weight,
            "trust_region_radius": self.problem.trust_region_radius,
            "rho": self.rho0,
            "t_cvx": [],
            "t_scp": [],
        }
        variables_each_iterations = []

        for k in range(maxiter):
            tstart_scp = time.time()

            # build linear model
            self.problem.build_linear_model(xbar, ubar, vbar)
            tstart_cvx = time.time()
            xopt, uopt, vopt, yopt, xi_dyn_opt, xi_opt, zeta_opt = self.problem.solve_convex_problem(xbar, ubar, vbar, ybar)
            scp_summary_dict["t_cvx"].append(time.time() - tstart_cvx)
            if self.problem.cp_status not in ["optimal", "optimal_inaccurate"]:
                status_AL = "CPFailed"
                if verbose:
                    print(f"    Convex problem did not converge to optimality (status = {self.problem.cp_status})!")
                break
            
            # evaluate nonlinear dynamics
            gdyn_nl_opt, sols = self.problem.evaluate_nonlinear_dynamics(xopt, uopt, vopt)

            # evaluate nonlinear constraints
            g_nl_opt, h_nl_opt = self.problem.evaluate_nonlinear_constraints(xopt, uopt, vopt, yopt)
            chi = np.linalg.norm(np.concatenate((gdyn_nl_opt.flatten(order='C'), g_nl_opt, h_nl_opt)), feasability_norm)

            # evaluate penalized objective
            J0     = self.problem.evaluate_objective(xopt, uopt, vopt, yopt)
            J0_bar = self.problem.evaluate_objective(xbar, ubar, vbar, ybar)
            J_bar  = J0_bar + self.evaluate_penalty(gdyn_nl_bar, g_nl_bar, h_nl_bar)
            J_opt  = J0     + self.evaluate_penalty(gdyn_nl_opt, g_nl_opt, h_nl_opt)
            L_opt  = J0     + self.evaluate_penalty(xi_dyn_opt, xi_opt, zeta_opt)

            # evaluate step acceptance criterion parameter
            DeltaJ = J_bar - J_opt
            DeltaL = J_bar - L_opt
            rho = DeltaJ / DeltaL

            if debug:
                print(f"\n  SCvxStar debug mode output at iteration {k+1}:")
                print(f"    J0            = {J0:1.4e}")
                print(f"    P(g(z), h(z)) = {self.evaluate_penalty(gdyn_nl_opt, g_nl_opt, h_nl_opt):1.4e}")
                print(f"    P(xi, zeta)   = {self.evaluate_penalty(xi_dyn_opt, xi_opt, zeta_opt):1.4e}")
                print(f"        ||gdyn_nl_opt|| = {np.linalg.norm(gdyn_nl_opt, np.inf):1.4e}, ||xi_dyn_opt||  = {np.linalg.norm(xi_dyn_opt, np.inf):1.4e}")
                if self.problem.ng > 0:
                    print(f"        ||g_nl_opt||    = {np.linalg.norm(g_nl_opt, np.inf):1.4e}, ||xi_opt||      = {np.linalg.norm(xi_opt, np.inf):1.4e}")
                if self.problem.nh > 0:
                    print(f"        ||h_nl_opt||    = {np.linalg.norm(h_nl_opt, np.inf):1.4e}, ||zeta_opt||      = {np.linalg.norm(zeta_opt, np.inf):1.4e}")
                print(f"    J0 = {J0:1.4e}, J0_bar = {J0_bar:1.4e}")
                print(f"    J_opt = J0 + P(g(z), h(z)) = {J0:1.4e} + {self.evaluate_penalty(gdyn_nl_opt, g_nl_opt, h_nl_opt):1.4e} = {J_opt:1.4e}")
                print(f"    L_opt = J0 + P(xi, zeta)   = {J0:1.4e} + {self.evaluate_penalty(xi_dyn_opt, xi_opt, zeta_opt):1.4e} = {L_opt:1.4e}")
                print(f"    Delta J = {DeltaJ:1.4e}, Delta L = {DeltaL:1.4e}, rho = {rho:1.4e}")
                # print(f"        xi_opt              = {xi_opt}")
                # print(f"        self.problem.lmb_eq = {self.problem.lmb_eq}")
                print(f"    chi = {chi:1.4e}")
                print("\n")

            if rho >= self.rho0:
                step_acpt_msg = "yes"
            else:
                step_acpt_msg = "no "
            if verbose:
                if np.mod(k, print_frequency) == 0:
                    print(f"\n{header}")
                print(f"   {k+1:3d}   | {J0: 1.4e} | {DeltaJ: 1.4e} | {DeltaL: 1.4e} | {chi:1.4e} | {rho: 1.4e} | {self.problem.trust_region_radius:1.4e} | {self.problem.weight:1.4e} |    {step_acpt_msg}     |")

            # update storage
            scp_summary_dict["J0"].append(J0)
            scp_summary_dict["chi"].append(chi)
            scp_summary_dict["DeltaJ"].append(DeltaJ)
            scp_summary_dict["DeltaL"].append(DeltaL)
            scp_summary_dict["accept"].append(int(rho >= self.rho0))
            if save_all_iterations:
                variables_each_iterations.append({
                    "x": copy.deepcopy(xopt),
                    "u": copy.deepcopy(uopt),
                    "v": copy.deepcopy(vopt),
                    "y": copy.deepcopy(yopt),
                })

            if (chi <= self.tol_feas) and (abs(DeltaJ) <= self.tol_opt) and (exit_condition_rho is False or rho >= self.rho0):
                status_AL = "Optimal"
                break
                
            if rho >= self.rho0:
                xbar[:,:] = xopt[:,:]
                ubar[:,:] = uopt[:,:]
                if vbar is not None:
                    vbar[:,:] = vopt[:,:]
                if self.problem.ny > 0:
                    ybar[:] = yopt[:]
                gdyn_nl_bar[:,:] = gdyn_nl_opt[:,:]
                if self.problem.ng > 0:
                    g_nl_bar[:] = g_nl_opt[:]
                if self.problem.nh > 0:
                    h_nl_bar[:] = h_nl_opt[:]

                if abs(DeltaJ) < np.abs(delta):
                    # update multipliers
                    self.problem.lmb_dynamics = self.problem.lmb_dynamics + self.problem.weight * gdyn_nl_opt
                    if self.problem.ng > 0:
                        self.problem.lmb_eq   = self.problem.lmb_eq + self.problem.weight * g_nl_opt
                    if self.problem.nh > 0:
                        self.problem.lmb_ineq = np.clip(self.problem.lmb_ineq + self.problem.weight * h_nl_opt, 0, None)

                    # update weight
                    self.problem.weight = min(self.beta * self.problem.weight, self.weight_max)
                    
                    # multiplier & weight update
                    if delta > 1e15:
                        delta = abs(DeltaJ)
                    else:
                        delta *= self.gamma

            # update trust-region
            if rho < self.rho1:
                self.problem.trust_region_radius = max(self.problem.trust_region_radius/self.alpha1, self.r_bounds[0])
            elif rho >= self.rho2:
                self.problem.trust_region_radius = min(self.problem.trust_region_radius*self.alpha2, self.r_bounds[1])

            # update steps at minimum trust region
            if self.problem.trust_region_radius == self.r_bounds[0]:
                n_min_trust_region += 1
            else:
                n_min_trust_region = 0
            if n_min_trust_region >= self.steps_minimum_trust_region:
                status_AL = "SlowProgress"
                if verbose:
                    print(f"    Exceeded {n_min_trust_region} steps at minimum trust region! Stopping SCvx*due to slow progress...\n")
                break
            scp_summary_dict["t_scp"].append(time.time() - tstart_scp)

        if (k == maxiter - 1) and (status_AL not in ["Optimal", "CPFailed", "SlowProgress"]):
            if chi <= self.tol_feas:
                status_AL = "Feasible"
            else:
                status_AL = "MaxIter"

        # print summary
        t_algorithm = time.time() - tstart
        if verbose:
            print("\n")
            print(f"    SCvx* algorithm summary:")
            print(f"        Status                          : {status_AL}")
            print(f"        Objective value                 : {scp_summary_dict['J0'][-1]:1.8e}")
            print(f"        Penalized objective improvement : {scp_summary_dict['DeltaJ'][-1]:1.8e} (tol: {self.tol_opt:1.4e})")
            print(f"        Constraint violation            : {scp_summary_dict['chi'][-1]:1.8e} (tol: {self.tol_feas:1.4e})")
            print(f"        Total iterations                : {k+1}")
            print(f"        SCvx* algorithm time            : {t_algorithm:1.4f} seconds")
            print("\n")

        # update summary dictionary
        scp_summary_dict["num_iter"] = k + 1
        scp_summary_dict["status"] = status_AL
        scp_summary_dict["status_CP"] = self.problem.cp_status
        scp_summary_dict["weight"] = self.problem.weight
        scp_summary_dict["trust_region_radius"] = self.problem.trust_region_radius
        scp_summary_dict["rho"] = rho
        scp_summary_dict["t_algorithm"] = t_algorithm
        return SCPSolution(xopt, uopt, vopt, yopt, sols, scp_summary_dict, variables_each_iterations)
    
    def plot_DeltaJ(self, axis, summary_dict: dict, s = 5):
        """Plot iterations of DeltaJ"""
        iters = np.arange(len(summary_dict["DeltaJ"]))
        axis.plot(iters, np.abs(summary_dict["DeltaJ"]), c='k', lw=0.5)
        axis.scatter(iters, np.abs(summary_dict["DeltaJ"]), marker="o", s=s, color=['g' if a == 1 else 'r' for a in summary_dict["accept"]], zorder=2)
        axis.set(yscale='log', xlabel='Iter.', ylabel='|DeltaJ|')
        return
    
    def plot_chi(self, axis, summary_dict: dict, s = 5):
        """Plot iterations of chi"""
        iters = np.arange(len(summary_dict["chi"]))
        axis.plot(iters, summary_dict["chi"], c='k', lw=0.5)
        axis.scatter(iters, summary_dict["chi"], marker="o", s=s, color=['g' if a == 1 else 'r' for a in summary_dict["accept"]], zorder=2)
        axis.set(yscale='log', xlabel='Iter.', ylabel='chi')
        return
    
    def plot_J0(self, axis, summary_dict: dict, s = 5):
        """Plot iterations of J0"""
        iters = np.arange(len(summary_dict["J0"]))
        axis.plot(iters, summary_dict["J0"], c='k', lw=0.5)
        axis.scatter(iters, summary_dict["J0"], marker="o", s=s, color=['g' if a == 1 else 'r' for a in summary_dict["accept"]], zorder=2)
        axis.set(xlabel='Iter.', ylabel='J0')
        return
