__author__ = 'christophaymanns'

import matplotlib.pylab as pl
import pickle
import numpy as np
import os
import pdb
import sys

def compute_frequencies(x,y):

    freq = {}

    for i in range(len(x)):
        point  = (x[i,0],y[i,0])
        if point in freq:
            freq[point] += 1
        else:
            freq[point] = 1

    frequencies = freq.values()
    points = freq.keys()

    xu = np.zeros(len(points))
    yu = np.zeros(len(points))

    cnt = 0
    for p in points:
        xu[cnt] = p[0]
        yu[cnt] = p[1]
        cnt += 1

    return [xu,yu,frequencies]

def main(path,mu0,mode):

    name_xm = 'mean_action_'+str(mu0)
    name_xi = 'initial_action_'+str(mu0)

    x_m = pickle.load(open(path+name_xm,'rb'))
    x_i = pickle.load(open(path+name_xi,'rb'))

    s1 = x_m.shape[0]
    s2 = x_m.shape[1]

    if mode == 'inf':
        rhos = np.linspace(0,0.95,num=20)
    elif mode == 'het':
        rhos = np.linspace(0.1,0.9,num=20)


    figs = []

    f = pl.figure()
    pl.hist(np.reshape(x_m,(s1*s2,1)))
    pl.title('Distribution of average action at t = 100')
    pl.ylabel('frequency')
    pl.xlabel('average action')
    figs.append(f)

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

    if mode == 'inf':
        xlabel = 'density'
    elif mode == 'het':
        xlabel = 'p(informed)'

    f = pl.figure()
    pl.subplot(2,1,1)
    pl.plot(rhos,contagion_frq,label='unconditional')
    pl.plot(rhos,cond_contagion_frq_low,label='xi <= 0.5')
    pl.title('Probability of contagion')
    leg = pl.legend(loc=1, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.subplot(2,1,2)
    pl.plot(rhos,contagion_frq,label='unconditional')
    pl.plot(rhos,cond_contagion_frq_high,'r',label='xi > 0.5')
    leg = pl.legend(loc=1, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.xlabel(xlabel)
    figs.append(f)

    f = pl.figure()
    pl.plot(rhos,cond_contagion_frq_low)
    pl.legend()
    pl.title('Conditional probability of contagion')
    pl.xlabel(xlabel)
    figs.append(f)

    f = pl.figure()
    pl.plot(rhos,x_mean)
    pl.title('Average action at t = 100')
    pl.xlabel(xlabel)
    figs.append(f)

    #f = pl.figure()
    #pl.plot(np.reshape(x_i,(s1*s2,1)),np.reshape(x_m,(s1*s2,1)),'o')
    #pl.hlines(0.5,0,1)
    #pl.vlines(0.5,0,1)
    #pl.title('Dependence on initial condition')
    #pl.xlabel('average initial action')
    #pl.ylabel('average final action')
    #figs.append(f)

    [xu,yu,freq] = compute_frequencies(np.reshape(x_i,(s1*s2,1)),np.reshape(x_m,(s1*s2,1)))

    f = pl.figure()
    pl.scatter(xu,yu,c=np.log10(freq),edgecolor = 'none')
    cbar = pl.colorbar()
    cbar.set_label('log10 of frequency', rotation=270)
    pl.hlines(0.5,-.1,1.1)
    pl.vlines(0.5,-.1,1.1)
    pl.xlim([-0.1,1.1])
    pl.ylim([-0.1,1.1])
    pl.title('Dependence on initial condition')
    pl.xlabel('average initial action')
    pl.ylabel('average final action')
    figs.append(f)

    fig_save_path = path + 'figures/'

    if not os.path.exists(fig_save_path):
        os.makedirs(fig_save_path)

    for i, figure in enumerate(figs):
        figure.savefig(fig_save_path+'figure%d.pdf' % i,format ='pdf')


try:
    sub_folder = sys.argv[1]+'/'
except IndexError:
    sub_folder = 'testing/'

try:
    mu0 = float(sys.argv[2])
except IndexError:
    mu0 = 0.4

try:
    weighting = sys.argv[3]
except IndexError:
    weighting = 'equal'

try:
    mode = sys.argv[4]
except IndexError:
    mode = 'inf'


#path = os.getcwd()+'/'+sub_folder + weighting +'/'
path = os.getcwd()+'/Results/results_ER_networks/'+sub_folder + weighting +'/'
main(path,mu0,mode)