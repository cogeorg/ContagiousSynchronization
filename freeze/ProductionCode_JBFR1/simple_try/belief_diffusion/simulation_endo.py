__author__ = 'christophaymanns'

import numpy as np
import scipy.stats as stats
import matplotlib.pylab as pl
import networkx as nx
import pickle
import os
import sys
import pdb

def gen_private_belief(mu0,s0,mu1,s1,signal):
    f0 = stats.norm.pdf(signal,mu0,s0)
    f1 = stats.norm.pdf(signal,mu1,s1)

    p = 1./(1 + f0/f1)

    return p

def gen_signal_structure_het(sig_params,p_inf,N):


    if len(sig_params) == 1:
        sig_inf = sig_params['inf']
        mu0 = np.ones(N)*sig_inf['mu0']
        mu1 = np.ones(N)*sig_inf['mu1']
        s0 = np.ones(N)*sig_inf['s0']
        s1 = np.ones(N)*sig_inf['s1']

    elif len(sig_params) == 2:
        sig_inf = sig_params['inf']
        sig_un_inf = sig_params['uninf']
        inf_id = np.random.binomial(1,p_inf,N)

        signal_inf = np.random.normal(sig_inf['mu0'],sig_inf['s0'],len(inf_id[inf_id == 1]))
        signal_un_inf = np.random.normal(sig_un_inf['mu0'],sig_un_inf['s0'],len(inf_id[inf_id == 0]))

        mu0 = np.zeros(len(inf_id))
        mu1 = np.zeros(len(inf_id))
        s0 = np.zeros(len(inf_id))
        s1 = np.zeros(len(inf_id))

        mu0[inf_id == 1] = sig_inf['mu0']
        mu1[inf_id == 1] = sig_inf['mu1']

        mu0[inf_id == 0] = sig_un_inf['mu0']
        mu1[inf_id == 0] = sig_un_inf['mu1']

        s0[inf_id == 1] = sig_inf['s0']
        s1[inf_id == 1] = sig_inf['s1']

        s0[inf_id == 0] = sig_un_inf['s0']
        s1[inf_id == 0] = sig_un_inf['s1']

    else:
        print('ERROR: no signal structure provided. Exiting...')
        sys.exit(0)


    return [mu0,mu1,s0,s1]

def network_update(sig_params,p_inf=1,N = 50,rho = 0.1,weight_type = 'equal'):

    wealth = np.zeros(N)
    degree = np.zeros(N)
    x = 0
    g = 0
    G = nx.erdos_renyi_graph(N, rho)
    for t in range(0,100000):
        if t%10000 == 0:
            print(t)
        [x,x_init,g] = main(sig_params,G=G,p_inf=p_inf,N = N,rho = rho,weight_type = weight_type,its=5)
        wealth[x[:,0] == 0] += 1
    degree = np.array(nx.degree(g).values())

    d = {}
    for i in range(N):
        if degree[i] in d:
            d[degree[i]].append(wealth[i])
        else:
            d[degree[i]] = []
            d[degree[i]].append(wealth[i])

    for key in d:
        d[key] = np.mean(d[key])

    pl.figure()
    pl.plot(degree,wealth,'o')

    pl.figure()
    pl.plot(d.keys(),d.values(),'o')

    pl.show()



def main(sig_params,G=None,p_inf=1,N = 50,rho = 0.1,weight_type = 'equal',its = 100):
    N = N#50#20
    rho = rho

    [mu0,mu1,s0,s1] = gen_signal_structure_het(sig_params,p_inf,N)
    #[mu0,mu1,s0,s1] = [sig_params['inf']['mu0'],sig_params['inf']['mu1'],sig_params['inf']['s0'],sig_params['inf']['s1']]

    x = np.zeros((N,1))
    k = np.zeros((N,1))
    pb = np.zeros((N,1))
    x_init = np.zeros((N,1))


    #x[:,0] = np.random.binomial(1,0.5,N)

    #signal = np.random.normal(mu0,s0,N)
    signal = np.random.normal(0,1,N)*s0 + mu0

    pb[:,0] = gen_private_belief(mu0,s0,mu1,s1,signal)
    x = np.around(pb)
    x_init = np.copy(x)

    if G == None:
        G = nx.erdos_renyi_graph(N, rho)
    A = np.asarray(nx.adjacency_matrix(G))

    k[:,0] = np.sum(A,axis=1)
    k_alt = np.copy(k[:,0])
    k[k_alt == 0] = 1

    #its = 100
    for i in range(its):
        sb = A.dot(x)/k
        #signal = np.random.normal(mu0,s0,N)
        signal = np.random.normal(0,1,N)*s0 + mu0
        pb[:,0] = gen_private_belief(mu0,s0,mu1,s1,signal)
        if weight_type == 'equal':
            x = np.around(0.5*(pb + sb))
        elif weight_type == 'neighbor':
            x = np.around(pb/(k+1.) + k/(k+1.)*sb)
        elif weight_type == 'rel_neighbor':
            x = np.around((1-k/(N-1.))*pb + k/(N-1.)*sb)
        x[k_alt == 0] = np.around(pb[k_alt == 0])

    return [x,x_init,G]


#try:
#    mu0 = float(sys.argv[3])
#except IndexError:
#    mu0 = 0.4

mu0= 0.49

print(mu0)
s0 = np.sqrt(0.1)#np.sqrt(0.1)
mu1 = 1-mu0
s1 = s0

sig_params = {}
sig_params['inf'] = {}
sig_params['inf']['mu0'] = mu0
sig_params['inf']['mu1'] = mu1
sig_params['inf']['s0'] = s0
sig_params['inf']['s1'] = s1

rho = 0.3#5
N = 100

network_update(sig_params,p_inf=1,N = N,rho = rho,weight_type = 'equal')


#rhos = np.linspace(0,0.95,num=20)
#N = 100
#pinf_fix = 0.5
#rho_sweep = False
#p_sweep = True
#rho_fix = 0.5
#ps = np.linspace(0.1,0.9,num=20)
#
#
#try:
#    runs = int(sys.argv[1])
#except IndexError:
#    runs = 500
#
#try:
#    sub_folder = sys.argv[2]+'/'
#except IndexError:
#    sub_folder = 'testing/'
#
#try:
#    mu0 = float(sys.argv[3])
#except IndexError:
#    mu0 = 0.4
#
#try:
#    weighting = sys.argv[4]
#except IndexError:
#    weighting = 'equal'
#
#try:
#    mu0_un = float(sys.argv[5])
#except IndexError:
#    mu0_un = 0
#
#sub_folder += weighting +'/'
#
#s0 = np.sqrt(0.1)
#mu1 = 1-mu0
#s1 = s0
#
#sig_params = {}
#sig_params['inf'] = {}
#sig_params['inf']['mu0'] = mu0
#sig_params['inf']['mu1'] = mu1
#sig_params['inf']['s0'] = s0
#sig_params['inf']['s1'] = s1
#
#if mu0_un != 0:
#    sig_params['uninf'] = {}
#    sig_params['uninf']['mu0'] = mu0_un
#    sig_params['uninf']['mu1'] = 1-mu0_un
#    sig_params['uninf']['s0'] = s0
#    sig_params['uninf']['s1'] = s1
#
#seeds = np.arange(1,runs+1)
#
#if rho_sweep:
#
#    x_m = np.zeros((len(rhos),runs))
#    x_i = np.zeros((len(rhos),runs))
#
#    for i in range(len(rhos)):
#        print('rho = '+str(rhos[i]))
#        for j in range(runs):
#            np.random.seed(seeds[j])
#            #[x,xi] = main(mu0,mu1,s1,s0,N = N, rho = rhos[i],weight_type=weighting)
#            [x,xi] = main(sig_params,p_inf=pinf_fix,N = N, rho = rhos[i],weight_type=weighting)
#            x_m[i,j] = np.mean(x)
#            x_i[i,j] = np.mean(xi)
#
#elif p_sweep:
#
#    x_m = np.zeros((len(ps),runs))
#    x_i = np.zeros((len(ps),runs))
#
#    for i in range(len(rhos)):
#        print('p_inf = '+str(ps[i]))
#        for j in range(runs):
#            np.random.seed(seeds[j])
#            #[x,xi] = main(mu0,mu1,s1,s0,N = N, rho = rhos[i],weight_type=weighting)
#            [x,xi] = main(sig_params,p_inf=ps[i],N = N, rho = rho_fix,weight_type=weighting)
#            x_m[i,j] = np.mean(x)
#            x_i[i,j] = np.mean(xi)
#
#
#path = os.getcwd()+'/'+sub_folder
#
#if not os.path.exists(path):
#    os.makedirs(path)
#
#params = [N,rhos,mu0,mu1,s0,s1,seeds,weighting,runs,sig_params,rho_fix,pinf_fix]
#
#pickle.dump(x_m,open(path+'mean_action_'+str(mu0),'wb'))
#pickle.dump(x_i,open(path+'initial_action_'+str(mu0),'wb'))
#pickle.dump(params,open(path+'params_'+str(mu0),'wb'))
#
##pl.figure()
##pl.hist(np.reshape(x_m,(runs*len(rhos),1)))
##pl.show()