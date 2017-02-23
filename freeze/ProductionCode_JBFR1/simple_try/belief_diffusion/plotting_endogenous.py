__author__ = 'christophaymanns'

import matplotlib.pylab as pl
import pickle
import numpy as np
import os
import pdb
import sys
import networkx as nx
import network_formation as nf

def calc_prob_contagion(x_m,x_i):

    x_m = np.transpose(x_m)
    x_i = np.transpose(x_i)

    s1 = x_m.shape[0]
    s2 = x_m.shape[1]

    contagion_frq = np.zeros(s1)
    x_mean = np.zeros(s1)
    cond_contagion_frq_low = np.zeros(s1)
    cond_contagion_frq_high = np.zeros(s1)

    for i in range(0,s1):
        cnt_cond_low = 0
        cnt_cond_high = 0
        obs_cond_low = 0
        obs_cond_high = 0
        for j in range(0,s2):

            if x_i[i,j] <= 0.5:
                obs_cond_low += 1.
                if x_m[i,j] > 0.8:
                    cnt_cond_low += 1.
            else:
                obs_cond_high += 1.
                if x_m[i,j] > 0.8:
                    cnt_cond_high += 1.

        x_mean[i] = np.mean(x_m[i,:])
        contagion_frq[i] = (cnt_cond_high+cnt_cond_low)/s2
        if obs_cond_low != 0:
            cond_contagion_frq_low[i] = cnt_cond_low/obs_cond_low
        if obs_cond_high != 0:
            cond_contagion_frq_high[i] = cnt_cond_high/obs_cond_high

    return [contagion_frq,cond_contagion_frq_low,cond_contagion_frq_high]

def compute_contagion(x):

    shape = x.shape
    if len(shape) > 1:

        [s1,s2] = x.shape

        p_contagion = np.zeros(s2)

        for j in range(s2):
            cont_cnt = 0
            for i in range(s1):

                if x[i,j] > 0.8:
                    cont_cnt += 1.

            p_contagion[j] = cont_cnt/s1

    else:

        p_contagion = 0
        s1 = shape[0]
        cont_cnt = 0
        for i in range(s1):
            if x[i] > 0.8:
                cont_cnt += 1.

        p_contagion = cont_cnt/s1


    return p_contagion

def load_data_new(paths):
    networks = []
    mu0s = []

    for path in paths:
        nets = pickle.load(open(path+'network_ensemble'))

        for net in nets:
            networks.append(net[3])
            mu0s.append(net[0])

    n_nets = len(networks)
    n_xinits = 11
    runs = 100

    x_init_m = np.zeros((n_xinits,n_nets,runs))
    x_final_m = np.zeros((n_xinits,n_nets,runs))
    t_converge = np.zeros((n_xinits,n_nets,runs))

    x_init_m_ER = np.zeros((n_xinits,n_nets,runs))
    x_final_m_ER = np.zeros((n_xinits,n_nets,runs))
    t_converge_ER = np.zeros((n_xinits,n_nets,runs))

    rhos = np.zeros(n_nets)

    index = 0
    for path in paths:

        [xf,xi,tc] = pickle.load(open(path+'results_endo_new'))
        length = xf.shape[1]
        x_init_m[:,index:index+length,:] = xi
        x_final_m[:,index:index+length,:] = xf
        t_converge[:,index:index+length,:] = tc

        [xf,xi,tc] = pickle.load(open(path+'results_ER_new'))
        length = xf.shape[1]
        x_init_m_ER[:,index:index+length,:] = xi
        x_final_m_ER[:,index:index+length,:] = xf
        t_converge_ER[:,index:index+length,:] = tc

        [N,rho,seeds] = pickle.load(open(path+'params_new'))

        rhos[index:index+length] = rho

        index = index+length

    # Now reshape and transpose arrays to make compatible with existing functions

    x_init_m = np.transpose(np.reshape(x_init_m,(n_xinits,n_nets*runs)))
    x_final_m = np.transpose(np.reshape(x_final_m,(n_xinits,n_nets*runs)))
    t_converge = np.transpose(np.reshape(t_converge,(n_xinits,n_nets*runs)))

    x_init_m_ER = np.transpose(np.reshape(x_init_m_ER,(n_xinits,n_nets*runs)))
    x_final_m_ER = np.transpose(np.reshape(x_final_m_ER,(n_xinits,n_nets*runs)))
    t_converge_ER = np.transpose(np.reshape(t_converge_ER,(n_xinits,n_nets*runs)))

    return [x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s]


def load_data(paths):

    networks = []
    mu0s = []

    for path in paths:
        nets = pickle.load(open(path+'network_ensemble'))

        for net in nets:
            networks.append(net[3])
            mu0s.append(net[0])

    runs = len(networks)
    n_xinits = 11

    x_init_m = np.zeros((runs,n_xinits))
    x_final_m = np.zeros((runs,n_xinits))
    t_converge = np.zeros((runs,n_xinits))

    x_init_m_ER = np.zeros((runs,n_xinits))
    x_final_m_ER = np.zeros((runs,n_xinits))
    t_converge_ER = np.zeros((runs,n_xinits))

    rhos = np.zeros(runs)

    index = 0
    for path in paths:

        [xf,xi,tc] = pickle.load(open(path+'results_endo'))
        length = xf.shape[0]
        x_init_m[index:index+length,:] = xi
        x_final_m[index:index+length,:] = xf
        t_converge[index:index+length,:] = tc

        [xf,xi,tc] = pickle.load(open(path+'results_ER'))
        length = xf.shape[0]
        x_init_m_ER[index:index+length,:] = xi
        x_final_m_ER[index:index+length,:] = xf
        t_converge_ER[index:index+length,:] = tc

        [N,rho] = pickle.load(open(path+'params'))

        rhos[index:index+length] = rho

        index = index+length

    return [x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s]


def network_statistics(paths):

    figs = []

    [x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s] = load_data(paths)

    degrees = []
    density = []

    N = networks[0].shape[0]

    for net in networks:
        G = nx.Graph(net)
        degrees += nx.degree(G).values()
        n = net.shape[0]
        d = np.sum(net)/(n*(n-1))
        density.append(d)

    mean_density = np.mean(density)
    std_density = np.std(density)

    degrees_ER = []

    for i in range(len(networks)):
        G = nx.erdos_renyi_graph(N,mean_density)
        degrees_ER += nx.degree(G).values()

    [hist,bins] = np.histogram(degrees,bins = 30,density=True)
    bins = bins[:-1] + (bins[1] - bins[0])/2

    [hist_ER,bins_ER] = np.histogram(degrees_ER,bins = 30,density=True)
    bins_ER = bins_ER[:-1] + (bins_ER[1] - bins_ER[0])/2

    font_size = 15
    font = {'size': font_size}

    pl.rc('font', **font)

    f = pl.figure()
    pl.semilogy(bins,hist,'bo',label='endogenous')
    pl.semilogy(bins_ER,hist_ER,'rD',label='ER')
    leg = pl.legend(loc=1, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.annotate('Average network density: '+str(np.around(mean_density,decimals=2)) +' $\pm$ '+ str(np.around(std_density,decimals=3)), xy=(0.1, 0.1), xycoords='axes fraction')
    pl.xlabel('degree')
    pl.ylabel('Probability')

    figs.append(f)

    G = nx.Graph(networks[22])

    values = np.ones(N)
    values[2] = 5
    values[3] = 5
    values[4] = 5
    values[5] = 5

    f = pl.figure()
    nx.draw(G,cmap = pl.get_cmap('binary'), node_color = values,with_labels=False)
    figs.append(f)

    #pl.show()

    return figs

def make_hist(x,x_ER,xlabel,ER_label):

    [hist,bins] = np.histogram(x,bins = 10,density=True)
    bins = bins[:-1] + (bins[1] - bins[0])/2

    [hist_ER,bins_ER] = np.histogram(x_ER,bins = 10,density=True)
    bins_ER = bins_ER[:-1] + (bins_ER[1] - bins_ER[0])/2

    font_size = 15
    font = {'size': font_size}

    pl.rc('font', **font)

    f = pl.figure()
    pl.semilogy(bins,hist,'bo',label='endogenous')
    pl.semilogy(bins_ER,hist_ER,'rD',label=ER_label)
    leg = pl.legend(loc=1, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.xlabel(xlabel)
    pl.ylabel('Probability density')

    return f


def contagion_analysis(path):

    figs = []

    #[x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s] = load_data(paths)
    [x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s] = load_data_new(paths)

    rho_m = np.around(np.mean(rhos),decimals=2)
    rho_std = np.around(np.std(rhos),decimals=3)

    #pl.rc('text', usetex=True)

    ER_label = 'ER:'# '+ r"$\rho = $" + str(rho_m)+r"$ \pm$ " + str(rho_std)


    f = make_hist(x_final_m[:,0],x_final_m_ER[:,0],'Average final action',ER_label)
    figs.append(f)
    f = make_hist(t_converge[:,0],t_converge_ER[:,0],'Convergence time',ER_label)
    figs.append(f)

    [contagion_frq,cond_contagion_frq_low,cond_contagion_frq_high] = calc_prob_contagion(x_final_m[:,1:],x_init_m[:,1:])
    [contagion_frq_ER,cond_contagion_frq_low_ER,cond_contagion_frq_high_ER] = calc_prob_contagion(x_final_m_ER[:,1:],x_init_m_ER[:,1:])

    #contagion_prob = compute_contagion(x_final_m[:,0])
    #contagion_prob_ER = compute_contagion(x_final_m_ER[:,0])

    xinits = x_init_m[1,1:]

    f = pl.figure()
    pl.plot(xinits,contagion_frq,'-bo',label='endogenous')
    pl.plot(xinits,contagion_frq_ER,'--rD',label=ER_label)
    leg = pl.legend(loc=2, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.xlabel('average initial action')
    pl.ylabel('Probability of contagion')
    figs.append(f)

    f = pl.figure()
    pl.semilogy(xinits,contagion_frq,'-bo',label='endogenous')
    pl.semilogy(xinits,contagion_frq_ER,'--rD',label=ER_label)
    leg = pl.legend(loc=2, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.xlabel('average initial action')
    pl.ylabel('Probability of contagion')
    figs.append(f)

    return figs
    #pl.show()


def main(paths):
    [x_init_m,x_final_m,t_converge,x_init_m_ER,x_final_m_ER,t_converge_ER,rhos,networks,mu0s] = load_data(paths)
    id = 103
    net = networks[id]
    mu0 = mu0s[id]

    runs = 1000
    np.random.seed(1)

    #xm_ts = np.zeros((runs,101))
    xs = np.zeros(runs)

    for i in range(runs):
        if i%100==0:
            print(i)
        #[x,x_init,G,xm_t] = nf.main(mu0,s=np.sqrt(0.1),G=nx.Graph(net),x_initial=0.8)
        #[x,x_init,G,xm_t] = nf.main(mu0s[i],s=np.sqrt(0.1),G=nx.Graph(networks[i]),x_initial=0.8)
        [x,x_init,G,xm_t] = nf.main(mu0,s=np.sqrt(0.1),G=None,rho=0.08,N=30,x_initial=0.8)
        #xm_ts[i,:] = xm_t
        xs[i] = np.mean(x)

    #pl.figure()
    #pl.plot(np.transpose(xm_ts))

    pl.figure()
    nx.draw(nx.Graph(net))

    pl.figure()
    pl.hist(xs)


    pl.show()

paths = []
paths.append(os.getcwd() + '/Results/results_endo_networks/seed_1_301/')
paths.append(os.getcwd() + '/Results/results_endo_networks/seed_301_601/')
paths.append(os.getcwd() + '/Results/results_endo_networks/seed_601_1001/')

figs = []

figs += network_statistics(paths)
figs += contagion_analysis(paths)

fig_save_path = os.getcwd() + '/Results/results_endo_networks/figures/'

if not os.path.exists(fig_save_path):
    os.makedirs(fig_save_path)

for i, figure in enumerate(figs):
    figure.savefig(fig_save_path+'figure%d.pdf' % i,format ='pdf')