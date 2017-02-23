__author__ = 'christophaymanns'

import network_formation as nf
import numpy as np
import sys
import os
import pickle
import networkx as nx
import matplotlib.pylab as pl
import pdb

# Compare learning dynamics between ER networks and endogenous networks:
#
# For endogenous networks use core configuration (i.e. some agents with high signal strength and low cost of maintaining a link)
# Hold cost and signal parameters constant.
#
# Analyze two scenarios:
# (1) x_init based on private belief
# (2) x_init with some bias
#
# Study:
# - Probability of contagion
# - Time to convergence
#
# Data to store:
# - Adjacency matrix of endogenous networks
# - mean x_init
# - mean x_final
# - Estimate of convergence time
# - network density
# - clustering
# - shortest path length
#
# Sample:
# Create ensemble of 1000 networks with N = 30 agents. Note that we reuse the the networks for different values for x_init.

def calc_convergence_time(xt,tol = 0.05,dt = 15):
    t_tot = len(xt)
    t_converge = t_tot
    for t in range(0,t_tot-dt):
        if np.abs(xt[t]-xt[t+dt]) < tol:
            t_converge = t
            break

    return t_converge


try:
    seed_start = int(sys.argv[1])
except IndexError:
    seed_start = -1

try:
    seed_end = int(sys.argv[2])
    if seed_end < seed_start:
        print('ERROR: seed end must be larger than seed start')
        sys.exit(0)

except IndexError:
    seed_end = - 1

try:
    if sys.argv[3] == 'load':
        load_networks = True
    else:
        load_networks = False
except IndexError:
    load_networks = False

runs = 100
n_xinits = 11
N = 30
boltzmann_matching = True
s = np.sqrt(0.1)

x_init_exo = np.linspace(0.4,0.8,num=n_xinits-1)

if seed_start > 0 and seed_end > 0:
    seeds = np.arange(seed_start,seed_end)
    runs  = len(seeds)
else:
    seeds = np.arange(0,runs)

endo_networks = []


#path = os.getcwd() + '/' + 'seed_' + str(seed_start) +'_' + str(seed_end) + '/'
path = os.getcwd() + '/Results/results_endo_networks/' + 'seed_' + str(seed_start) +'_' + str(seed_end) + '/'
filename = 'network_ensemble'

if load_networks == False:

    print('========== GENERATING NETWORKS =============')

    # First generate ensemble of networks
    for i in range(runs):
        print(i)
        [G,mu0s,cs,M,bmm] = nf.generate_network_core(N=N,seed=seeds[i],doPlot=False,doSave=False,t_converge=400,boltzmann_matching=boltzmann_matching)
        network = [mu0s,cs,seeds[i],M,bmm]
        endo_networks.append(network)


    if not os.path.exists(path):
        os.makedirs(path)

    print('========== SAVING NETWORKS =============')

    pickle.dump(endo_networks,open(path+filename,'wb'))

else:

    # First load networks

    networks = []
    mu0s = []

    nets = pickle.load(open(path+filename))

    for net in nets:
        networks.append(net[3])
        mu0s.append(net[0])

    runs = 2#00
    seeds = np.arange(0,runs)
    n_nets = len(networks)

    x_init_m = np.zeros((n_xinits,n_nets,runs))
    x_final_m = np.zeros((n_xinits,n_nets,runs))
    t_converge = np.zeros((n_xinits,n_nets,runs))

    x_init_m_ER = np.zeros((n_xinits,n_nets,runs))
    x_final_m_ER = np.zeros((n_xinits,n_nets,runs))
    t_converge_ER = np.zeros((n_xinits,n_nets,runs))

    rhos = np.zeros(n_nets)

    for i in range(n_xinits):

        for j in range(n_nets):

            G = nx.Graph(networks[j])
            mu0 = mu0s[j]

            n = networks[j].shape[0]
            rho = np.sum(networks[j])/(n*(n-1))
            rhos[j] = rho

            if j%100 == 0:
                print('Bias: '+str(i)+' network: '+str(j))

            for k in range(runs):

                np.random.seed(seeds[k])

                # First run with endogenously formed network

                if i == 0:
                    [x,x_init,g,xm_t] = nf.main(mu0,s,G=G,x_initial=-1)
                else:
                    [x,x_init,g,xm_t] = nf.main(mu0,s,G=G,x_initial=x_init_exo[i-1])

                x_final_m[i,j,k] = np.mean(x)
                x_init_m[i,j,k] = np.mean(x_init)
                t_converge[i,j,k] = calc_convergence_time(xm_t)

                # Then run with ER network
                # Note that while above the network is constant, here we are regenerating a network for every run

                if i == 0:
                    [x,x_init,g,xm_t] = nf.main(mu0,s,N=N,rho=rho,x_initial=-1)
                else:
                    [x,x_init,g,xm_t] = nf.main(mu0,s,N=N,rho=rho,x_initial=x_init_exo[i-1])

                x_final_m_ER[i,j,k] = np.mean(x)
                x_init_m_ER[i,j,k] = np.mean(x_init)
                t_converge_ER[i,j,k] = calc_convergence_time(xm_t)


    results_endo = [x_final_m,x_init_m,t_converge]
    results_ER = [x_final_m_ER,x_init_m_ER,t_converge_ER]
    params = [N,rhos,seeds]

    #pl.figure()
    #pl.hist(x_final_m[1,:,1])
    #
    #pl.figure()
    #pl.hist(x_final_m_ER[1,:,1])
    #
    #
    #pl.figure()
    #nx.draw(plot_graph)
    #
    #pl.show()

    pickle.dump(results_endo,open(path+'results_endo_new','wb'))
    pickle.dump(results_ER,open(path+'results_ER_new','wb'))
    pickle.dump(params,open(path+'params_new','wb'))