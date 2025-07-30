'''
This file contains pre-processing, post-processing, and analytical tools for simulations.

Public Funcions:
- check_convergence:    Check whether a simulation result converges. i.e. whether U, V's fluctuation are very small.
- combine_sim:          Combine two simulation objects and return a new one (the first two unchanged).
                        Intended usage: say you have sim1, sim2 with same parameters except for sim_time, say 10 and 20.
                                        Then combine_sim takes a weighted average (with ratio 1:2) of results and return a new sim3.
                                        So that you now have sim3 with 30 sim_time.

Private Functions:
- rounds_expected:      Roughly calculates how many rounds are expected in a single simulation (which reflects runtime).
                        NOTE: Not well-developed. Not recommending to use.
- scale_maxtime:        Given two simulation objects, scale first one's maxtime towards the second, so that the two have the same expected rounds.
                        Intended to possibly decrease maxtime and save runtime.
                        NOTE: Not well-developed. Not recommending to use.

'''

from . import model as model
from . import figures as figures
from .tools import figure_tools as figure_t

import numpy as np
import math




def rounds_expected(sim):
    '''
    NOTE: Not well-developed. Not recommending to use.

    Predict how many rounds will run in single_test. i.e., how many for loops from time = 0 to sim.maxtime.
    Calculated based on expected_UV. 
    '''

    N = sim.N
    M = sim.M
    U_expected, V_expected = figures.UV_expected_val(sim)

    rates = []
    patch0 = None  # simulate patch i, j
    patch0_nb = []  # simulate neighbors of patch i, j
    
    # loop through N, M, create a sample patch to calculate rates, store them
    for i in range(N):
        for j in range(M):
            patch0 = model.patch(U_expected[i][j], V_expected[i][j], sim.X[i][j], sim.P[i][j])

            nb_indices = None
            if sim.boundary:
                nb_indices = model.find_nb_zero_flux(N, M, i, j)
            else:
                nb_indices = model.find_nb_periodical(N, M, i, j)
            
            for k in range(4):
                if nb_indices[k] != None:
                    i_nb = nb_indices[k][0]
                    j_nb = nb_indices[k][1]
                    patch0_nb_k = model.patch(U_expected[i_nb][j_nb], V_expected[i_nb][j_nb], sim.X[i_nb][j_nb], sim.P[i_nb][j_nb])
                    patch0_nb_k.update_pi_k()
                    patch0_nb.append(patch0_nb_k)

                else:
                    patch0_nb.append(None)

            patch0.nb = patch0_nb
            patch0.update_pi_k()
            patch0.update_mig()

            rates += patch0.pi_death_rates
            rates += patch0.mig_rates
    
    delta_t_expected = (1 / sum(rates)) * math.log(1 / 0.5)
    r_expected = round(sim.maxtime / delta_t_expected)

    return r_expected




def scale_maxtime(sim1, sim2, scale_interval = True):
    '''
    NOTE: Not well-developed. Not recommending to use.

    Scale sim1's maxtime towards sim2's, so they will run similar number of rounds in single_test, and hence similar runtime.
    Intended to reduce the effect of changing params on runtime. 
    
    Input:
    - scale_interval decides whether to scale sim1's interval as well, so that the same number of data will be stored.
    '''

    r_expected1 = rounds_expected(sim1)
    r_expected2 = rounds_expected(sim2)
    ratio = r_expected2 / r_expected1

    new_maxtime = sim1.maxtime * ratio
    old_max_record = sim1.maxtime / sim1.interval

    if scale_interval:
        sim1.interval = new_maxtime / old_max_record

    sim1.change_maxtime(new_maxtime)




def check_convergence(sim, interval = 20, start = 0.8, fluc = 0.07):
    '''
    Check whether a simulation converges or not.
    Based on whether the fluctuation of U, V, pi all < 'fluc' in the later 'tail' portion of time.
    
    Essentially find the max and min values (of population) in every small interval, and then check whether their difference > min * fluc.

    Inputs:
    - sim: a simulation object
    - interval: int, how many records to take average over,
                and then compare this "local mean" with "whole-tail mean" and expect the difference to be less than fluc.
    - start: (0, 1) float, decides where you expect to check convergence from. Smaller start needs earlier convergence.
    - fluc: (0, 1) float. How much fluctuation is allowed between the average value of a small interval and the mean.
    '''

    if (start < 0) or (start > 1):
        raise ValueError("start should be a float in (0, 1)")
    if (fluc < 0) or (fluc > 1):
        raise ValueError("fluc should be a float in (0, 1)")
    if (type(interval) != int) or (interval < 1):
        raise ValueError("interval should be an int >= 1")
    
    interval = figure_t.scale_interval(interval, sim.compress_itv)

    start_index = int(sim.max_record * start)  # where the tail starts
    num_interval = int((sim.max_record - start_index) / interval)  # how many intervals in total

    # find the max and min value of the small intervals 
    # initiate as average of the first interval
    min_U = np.mean(sim.U[:, :, start_index : start_index + interval])
    max_U = np.mean(sim.U[:, :, start_index : start_index + interval])
    min_V = np.mean(sim.V[:, :, start_index : start_index + interval])
    max_V = np.mean(sim.V[:, :, start_index : start_index + interval])

    for i in range(1, num_interval):
        # lower and upper bound of current interval
        lower = start_index + i * interval
        upper = lower + interval

        ave_U = np.mean(sim.U[:, :, lower : upper])
        ave_V = np.mean(sim.V[:, :, lower : upper])

        # Compare with min, max
        if ave_U > max_U:
            max_U = ave_U
        if ave_U < min_U:
            min_U = ave_U

        if ave_V > max_V:
            max_V = ave_V
        if ave_V < min_V:
            min_V = ave_V

        # check whether (max - min) > min * fluc
        if (max_U - min_U) > min_U * fluc:
            return False
        if (max_V - min_V) > min_V * fluc:
            return False
            
    return True




def combine_sim(sim1, sim2):
    '''
    Combine data of sim1 and sim2. 
    Intended usage: assume sim1 and sim2 has the same N, M, maxtime, interval, boundary, max_record, and I, X, P
    combine_sim then combines the two results and calculate a new weighted average of the two data, return a new sim object. 
    Essentially allows breaking up many rounds of simulations into several smaller pieces, and then put together.

    Inputs:
    - sim1, sim2: both stochastic_model.simulation object. All input parameters the same except for sim_time, print_pct and seed.
            Raises error if not.

    Returns:

    - sim3:       a new simulation object whose U, V, U_pi, V_pi are weighted averages of sim1 and sim2
                (weighted by sim_time). 
                sim3.print_pct is set to sim1's, seed set to None, sim_time set to sum of sim1's and sim2's. All other params same as sim1
    '''
    if not (sim1.N == sim2.N and
            sim1.M == sim2.M and
            sim1.maxtime == sim2.maxtime and
            sim1.record_itv == sim2.record_itv and
            sim1.boundary == sim2.boundary and
            sim1.max_record == sim2.max_record and
            np.array_equal(sim1.I, sim2.I) and
            np.array_equal(sim1.X, sim2.X) and
            np.array_equal(sim1.P, sim2.P)):
        
        raise ValueError('sim1 and sim2 have different input parameters (N, M, maxtime, interval, boundary, max_record, or I, X, P).')

    if sim1.seed == sim2.seed:
        raise ValueError('Cannot combine two simulations with the same seed.')
    
    # copy sim1, except for no data and a different sim_time
    combined_sim_time = sim1.sim_time + sim2.sim_time
    sim3 = sim1.copy(copy_data = False)
    sim3.sim_time = combined_sim_time
    sim3.seed = None

    for i in range(sim3.N):
        for j in range(sim3.M):
            for k in range(sim3.max_record):
                sim3.U[i][j][k] = (sim1.U[i][j][k] * sim1.sim_time + sim2.U[i][j][k] * sim2.sim_time) / combined_sim_time
                sim3.V[i][j][k] = (sim1.V[i][j][k] * sim1.sim_time + sim2.V[i][j][k] * sim2.sim_time) / combined_sim_time
                sim3.U_pi[i][j][k] = (sim1.U_pi[i][j][k] * sim1.sim_time + sim2.U_pi[i][j][k] * sim2.sim_time) / combined_sim_time
                sim3.V_pi[i][j][k] = (sim1.V_pi[i][j][k] * sim1.sim_time + sim2.V_pi[i][j][k] * sim2.sim_time) / combined_sim_time

    return sim3



