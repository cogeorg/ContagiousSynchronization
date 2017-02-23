__author__ = 'christophaymanns'

import numpy as np
import scipy.stats as stats
import scipy.integrate as integrate
import matplotlib.pylab as pl
import networkx as nx
import pickle
import os
import sys
import pdb
import itertools

def gen_private_belief(mu0,s0,mu1,s1,signal):
    f0 = stats.norm.pdf(signal,mu0,s0)
    f1 = stats.norm.pdf(signal,mu1,s1)

    p = 1./(1 + f0/f1)

    return p


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = np.random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"



def p_belief_dist(p,mu0,mu1,s):
    dsdp = ((-(1-p)/p**2 - 1/p)*p*s**2)/((mu0-mu1)*(1-p))
    Ps = np.exp(-((mu0-mu1)**2 - 2*s**2 * np.log(1/p-1))**2/(8*(mu0-mu1)**2*s**2))/(np.sqrt(2*np.pi)*s)
    return dsdp*Ps

def pick_agent(mu0s,selection_set):

    beta = 30.#15.
    E = np.abs(0.5-mu0s[np.array(list(selection_set),dtype=int)])
    Emax = np.max(E)
    prob = np.exp(beta*(E-Emax))
    prob = prob/np.sum(prob)

    #pdb.set_trace()
    choices = []
    selection_list = list(selection_set)
    for i in range(len(prob)):
        choices.append([selection_list[i],prob[i]])

    #id_B = np.random.choice(np.array(list(selection_set),dtype=int),p=prob)
    id_B = weighted_choice(choices)
    #id_B = list(selection_set)[index]

    return id_B

def prob_correct_action(mu0,mu0ks,s,q = 0.5):
    # Note that this is equal to the expected utility

    k = len(mu0ks)

    # let's compute the probability of choosing the correct action (assume state = 0)

    # first find the probability that neighbor chooses the correct action (assume state = 0) and neighbor only receives private signal
    pks = np.zeros(k)
    for i in range(k):
        #pks[i] = integrate.quad(p_belief_dist,0.01,0.5,args=(mu0ks[i],1-mu0ks[i],s))[0]
        pks[i] = integrate.quad(p_belief_dist,0.01,1-q,args=(mu0ks[i],1-mu0ks[i],s))[0]

    # now consider all possible configurations of the neighbors' actions

    # sum of actions lies in (0,k)

    prob_social_belief = np.zeros(k+1)
    prob_correct_ac = np.zeros(k+1)

    for i in range(0,k+1):
        # now find all combinations of actions that sum to k
        if i == 0:
            probs = np.copy(pks)
            prob = np.prod(probs)
            prob_social_belief[i] = prob
            prob_correct_ac[i] = prob
        elif i < k:
            ids = itertools.combinations(np.arange(0,k),i)
            prob = 0

            for id in ids:
                action_vector = np.zeros(k)
                action_vector[np.array(id)] = 1

                #pdb.set_trace()

                probs = np.copy(pks)
                probs[np.array(id)] = 1-probs[np.array(id)]

                prob += np.prod(probs)

            prob_social_belief[i] = prob

            prob_correct_ac[i] = prob*integrate.quad(p_belief_dist,0.01,1-i/float(k),args=(mu0,1-mu0,s))[0]
        else:
            # if all neighbors choose action 1 the probability of choosing 0 for our agent is zero since it is already at the threshold.
            # only doing this step for clarity, could also run loop only till k.
            prob_correct_ac[i] = 0

    # now the total probability of choosing the correct action is:

    P = np.sum(prob_correct_ac)

    return P

def update_neighbor(mu0s,s,M,Us,cs,q=0.5,override_utility = True,debug = False,boltzmann_matching=True):
    # M is the adjacency matrix of the network
    N = M.shape[0]
    all_agents = np.arange(0,N)

    # randomly select an agent
    id_A = np.random.randint(0,N)

    #pdb.set_trace()

    # construct set of agents from which to randomly select possible new neighbor
    id_neighbors_A = all_agents[M[id_A,:]==1]

    agent_set = set(np.arange(0,N))
    non_set = set(id_neighbors_A)
    non_set.add(id_A)

    selection_set = agent_set.difference(non_set)

    if len(selection_set) > 0:

        #pdb.set_trace()

        rand_int = np.random.randint(0,len(selection_set))

        #id_B = list(selection_set)[np.argmax(np.abs(0.5-mu0s[np.array(list(selection_set),dtype=int)]))]
        if boltzmann_matching:
            id_B = pick_agent(mu0s,selection_set)
        else:
            id_B = list(selection_set)[rand_int]

        id_neighbors_B = all_agents[M[id_B,:]==1]

        # Now we need to decide whether to add a link to this agent or not. Let's call the first agent A and the second agent B.
        # Let dUdk_A be the marginal utility of adding a link for agent A, a similar term exists for agent B.
        # The marginal cost of adding a link for agent A is c_A, similarly for B. Define the least informative link in the set of
        # neighbors of A or B: l_min (i.e. the link to the agent with the least informative signal). Denote "\ x" = without link x.


        # We distinguish 5 cases:
        # (1) dUdk_A > c_A AND dUdk_B > c_B => form link
        # (2) dUdk_A < c_A BUT dUdk_A( \ l_min) > c_A AND mu0_B > mu0_l_min AND dUdk_B > c_B => form link
        # (3) The same as (2) but for B->A and A->B.
        # (4) The same as (2) but for both A and B.
        # (5) None of the above => no new link is formed.

        # This procedure should ensure pairwise stability.

        # CASE (1):

        id_neighbors_A_new = np.zeros(len(id_neighbors_A)+1,dtype=int)
        id_neighbors_A_new[0:-1] = id_neighbors_A
        id_neighbors_A_new[-1] = id_B

        id_neighbors_B_new = np.zeros(len(id_neighbors_B)+1,dtype=int)
        id_neighbors_B_new[0:-1] = id_neighbors_B
        id_neighbors_B_new[-1] = id_B

        #pdb.set_trace()

        U_A_new = prob_correct_action(mu0s[id_A],mu0s[id_neighbors_A_new],s,q)
        U_B_new = prob_correct_action(mu0s[id_B],mu0s[id_neighbors_B_new],s,q)

        dUdk_A =  U_A_new - Us[id_A]
        dUdk_B =  U_B_new - Us[id_B]

        if dUdk_A > cs[id_A] and dUdk_B > cs[id_B]:

            #pdb.set_trace()

            M[id_A,id_B] = 1
            M[id_B,id_A] = 1
            Us[id_A] = U_A_new
            Us[id_B] = U_B_new

        # CASE (2):

        elif dUdk_A < cs[id_A] and dUdk_B > cs[id_B]:

            if len(id_neighbors_A) == 0:

                if override_utility:
                    # if agent has no neighbors yet, just add the link (this is a special case, when adding the first link the marginal utility may actually be zero or less)
                    # add link anyways

                    M[id_A,id_B] = 1
                    M[id_B,id_A] = 1
                    Us[id_A] = U_A_new
                    Us[id_B] = U_B_new

                    if debug:
                        print('OVERRIDE - 1')

            else:

                #pdb.set_trace()

                l_min_A = np.argmin(mu0s[id_neighbors_A])

                if np.abs(0.5-mu0s[id_neighbors_A[l_min_A]]) < np.abs(0.5-mu0s[id_B]):

                    id_neighbors_A_new = np.copy(id_neighbors_A)
                    id_neighbors_A_new[l_min_A] = id_B

                    U_A_new = prob_correct_action(mu0s[id_A],mu0s[id_neighbors_A_new],s,q)

                    dUdk_A =  U_A_new - Us[id_A]

                    # the following should always be satisfied once we are here:

                    if dUdk_A > cs[id_A]:
                        M[id_A,id_B] = 1
                        M[id_B,id_A] = 1
                        M[id_A,id_neighbors_A[l_min_A]] = 0
                        M[id_neighbors_A[l_min_A],id_A] = 0
                        Us[id_A] = U_A_new
                        Us[id_B] = U_B_new

        # CASE (3):

        elif dUdk_A > cs[id_A] and dUdk_B < cs[id_B]:

            if len(id_neighbors_B) == 0:

                if override_utility:
                    # if agent has no neighbors yet, just add the link (this is a special case, when adding the first link the marginal utility may actually be zero or less)
                    # add link anyways

                    M[id_A,id_B] = 1
                    M[id_B,id_A] = 1
                    Us[id_A] = U_A_new
                    Us[id_B] = U_B_new

                    if debug:
                        print('OVERRIDE - 2')

            else:

                l_min_B = np.argmin(mu0s[id_neighbors_B])

                if np.abs(0.5-mu0s[id_neighbors_B[l_min_B]]) < np.abs(0.5-mu0s[id_A]):

                    id_neighbors_B_new = np.copy(id_neighbors_B)
                    id_neighbors_B_new[l_min_B] = id_A

                    U_B_new = prob_correct_action(mu0s[id_B],mu0s[id_neighbors_B_new],s,q)

                    dUdk_B =  U_B_new - Us[id_B]

                    # the following should always be satisfied once we are here:

                    if dUdk_B > cs[id_B]:
                        M[id_A,id_B] = 1
                        M[id_B,id_A] = 1
                        M[id_A,id_neighbors_B[l_min_B]] = 0
                        M[id_neighbors_B[l_min_B],id_A] = 0
                        Us[id_A] = U_A_new
                        Us[id_B] = U_B_new

        # CASE (4):

        elif dUdk_A < cs[id_A] and dUdk_B < cs[id_B]:

            #pdb.set_trace()

            if len(id_neighbors_A) == 0 or len(id_neighbors_B) == 0:

                if override_utility:
                    # if agent has no neighbors yet, just add the link (this is a special case, when adding the first link the marginal utility may actually be zero or less)
                    # add link anyways

                    M[id_A,id_B] = 1
                    M[id_B,id_A] = 1
                    Us[id_A] = U_A_new
                    Us[id_B] = U_B_new

                    if debug:
                        print('OVERRIDE - 3')

            else:

                #pdb.set_trace()

                l_min_A = np.argmin(mu0s[id_neighbors_A])
                l_min_B = np.argmin(mu0s[id_neighbors_B])

                if np.abs(0.5-mu0s[id_neighbors_B[l_min_B]]) < np.abs(0.5-mu0s[id_A]) and np.abs(0.5-mu0s[id_neighbors_A[l_min_A]]) < np.abs(0.5-mu0s[id_B]):

                    id_neighbors_B_new = np.copy(id_neighbors_B)
                    id_neighbors_B_new[l_min_B] = id_A

                    id_neighbors_A_new = np.copy(id_neighbors_A)
                    id_neighbors_A_new[l_min_A] = id_B

                    U_A_new = prob_correct_action(mu0s[id_A],mu0s[id_neighbors_A_new],s,q)
                    U_B_new = prob_correct_action(mu0s[id_B],mu0s[id_neighbors_B_new],s,q)

                    dUdk_A =  U_A_new - Us[id_A]
                    dUdk_B =  U_B_new - Us[id_B]

                    # the following should always be satisfied once we are here:

                    if dUdk_A > cs[id_A] and dUdk_B > cs[id_B]:
                        M[id_A,id_B] = 1
                        M[id_B,id_A] = 1
                        M[id_A,id_neighbors_A[l_min_A]] = 0
                        M[id_neighbors_A[l_min_A],id_A] = 0
                        M[id_A,id_neighbors_B[l_min_B]] = 0
                        M[id_neighbors_B[l_min_B],id_A] = 0
                        Us[id_A] = U_A_new
                        Us[id_B] = U_B_new

        # CASE (5):

        else:

            pass

    return [M,Us]

def main(mu0s,s,G=None,p_inf=1,N = 50,rho = 0.1,weight_type = 'equal',its = 100,x_initial = -1):

    if G == None:
        #pdb.set_trace()
        G = nx.erdos_renyi_graph(N, rho)
    A = np.asarray(nx.adjacency_matrix(G))
    N = A.shape[0]

    rho = rho


    mu0 = mu0s
    mu1 = 1 - mu0s
    s0 = s1 = s

    x = np.zeros((N,1))
    k = np.zeros((N,1))
    pb = np.zeros((N,1))
    x_init = np.zeros((N,1))

    xm_t = np.zeros(its+1)


    #x[:,0] = np.random.binomial(1,0.5,N)

    #signal = np.random.normal(mu0,s0,N)
    signal = np.random.normal(0,1,N)*s0 + mu0

    pb[:,0] = gen_private_belief(mu0,s0,mu1,s1,signal)

    if x_initial < 0:
        x = np.around(pb)
    else:
        x = np.ones((N,1))*x_initial

    x_init = np.copy(x)

    xm_t[0] = np.mean(x_init)

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

        xm_t[i+1] = np.mean(x)

    return [x,x_init,G,xm_t]

def simulate_with_fixed_network(load_graph = False):

    runs = 10000
    N = 30
    xs = np.zeros(runs)
    xinits = np.zeros(runs)

    #np.random.seed(3)

    if load_graph:
        path = os.getcwd()+'/'
        name = 'graph_mu0s'
        [G,mu0s] = pickle.load(open(path+name,'rb'))
    else:
        [G,mu0s] = generate_network_core(doPlot=False,seed=-1,doSave=True)
    s = np.sqrt(0.1)

    [x,xinit,g,xm_t_G] = main(mu0s,s,G=G)
    rho = np.sum(np.asarray(nx.adjacency_matrix(G)))/(N*(N-1))
    [x,xinit,g,xm_t_ER] = main(mu0s,s,G=None,N=N,rho=rho)

    pl.figure()
    pl.plot(xm_t_G,'b')
    pl.plot(xm_t_ER,'r')

    #for i in range(runs):
    #    if i%1000 == 0:
    #        print(i)
    #    [x,xinit,g] = main(mu0s,s,G=G)
    #    #[x,xinit,g] = main(mu0s,s,G=None,N=30)
    #    xs[i] = np.mean(x)
    #    xinits[i] = np.mean(xinit)
    #
    #pl.figure()
    #pl.hist(xs)
    #
    #pl.figure()
    #pl.hist(xinits)
    #
    pl.figure()
    nx.draw(G)

    pl.show()


def generate_network_core(N=30,seed = 3,doPlot = True,doSave = False,t_converge = 400,boltzmann_matching = True):
    N = N#30#20#10
    if seed > 0:
        np.random.seed(seed)
    all_agents = np.arange(0,N)

    M = np.zeros((N,N))
    M[0,1] = M[1,0] = 1

    mu0s = np.ones(N)*0.4
    s = np.sqrt(0.1)
    Us = np.zeros(N)
    cs = np.ones(N)*0.1#*0.1#*0.11041347180414752#0.15

    mu0s[2] = 0.3
    cs[2] = 0.

    mu0s[3] = 0.3
    cs[3] = 0.

    mu0s[4] = 0.3
    cs[4] = 0.

    mu0s[5] = 0.3
    cs[5] = 0.


    for i in range(N):
        ids = all_agents[M[i,:]==1]
        Us[i] = prob_correct_action(mu0s[i],mu0s[ids],s,q = 0.5)#0.6

    Us[2] = 0.6
    Us[3] = 0.6
    Us[4] = 0.6

    runs = t_converge
    density = np.zeros(runs)
    clustering = np.zeros(runs)
    diff = np.zeros(runs)

    for i in range(runs):
        #if i%100 == 0:
        #    print(i)
        Mo = np.copy(M)
        [M,Us] = update_neighbor(mu0s,s,M,Us,cs,boltzmann_matching=boltzmann_matching)
        density[i] = np.sum(M)/(N*(N-1))
        G =nx.Graph(M)
        clustering[i] = nx.average_clustering(G)
        diff[i] = np.sum(np.abs(M-Mo))


    G =nx.Graph(M)

    if doPlot:
        print(M)
        #print('Shortest path: '+str( nx.average_shortest_path_length(G)))

        pl.figure()
        pl.plot(density)
        pl.plot(clustering)

        pl.figure()
        pl.plot(diff)

        pl.figure()
        pl.imshow(M,interpolation=None)

        pl.figure()
        nx.draw(nx.Graph(M))

        pl.figure()
        pl.hist(nx.degree(G).values())


        pl.show()

    if doSave:
        path = os.getcwd()+'/'
        name = 'graph_mu0s'
        pickle.dump([G,mu0s],open(path+name,'wb'))

    return [G,mu0s,cs,M,boltzmann_matching]

def test3():

    #np.random.seed(4)
    #np.random.seed(10)
    # Let's consider the case with four nodes and no cost of establishing a link.
    N = 20#5
    all_agents = np.arange(0,N)

    # We start of with the empty network or two disconnected components

    initial_net = 'empty'

    if initial_net == 'empty':
        M = np.zeros((N,N))
    elif initial_net == 'two':
        M = np.zeros((N,N))
        M[0,1] = M[1,0] = 1
        M[2,3] = M[3,2] = 1

    mu0s = np.ones(N)*0.4
    s = np.sqrt(0.1)
    Us = np.zeros(N)
    cs = np.ones(N)*0.05

    mu0s[2] = 0.3

    for i in range(N):
        ids = all_agents[M[i,:]==1]
        Us[i] = prob_correct_action(mu0s[i],mu0s[ids],s,q = 0.5)

    #print(M)
    runs = 500
    density = np.zeros(runs)
    clustering = np.zeros(runs)

    for i in range(runs):
        if i%100 == 0:
            print(i)
        [M,Us] = update_neighbor(mu0s,s,M,Us,cs)
        density[i] = np.sum(M)/(N*(N-1))
        G =nx.Graph(M)
        clustering[i] = nx.average_clustering(G)
        #print(M)

    clustering_ER = np.zeros(runs)
    for i in range(100):
        G = nx.erdos_renyi_graph(N, 0.22)
        clustering_ER[i] = nx.average_clustering(G)

    av_clustering_ER = np.mean(clustering_ER)

    pl.figure()
    pl.plot(density)
    pl.plot(clustering)
    pl.hlines(av_clustering_ER,0,200)

    pl.figure()
    nx.draw(nx.Graph(M))

    pl.show()


def test2():

    mu0 = 0.4
    mu1 = 0.6
    s = np.sqrt(0.1)

    runs = 14

    Ps = np.zeros(runs)

    for run in range(1,runs):

        k = run
        mu0ks = np.ones(k)*0.3

        Ps[run] = prob_correct_action(mu0,mu0ks,s,q=0.5)
        print('P with social belief: '+str(Ps[run]))

    Pp = integrate.quad(p_belief_dist,0.01,0.5,args=(mu0,1-mu0,s))[0]
    print('P with private belief only: '+str(Pp))

    Ps[0] = Pp

    pl.figure()
    pl.plot(np.arange(0,runs),Ps)
    pl.plot(np.arange(1,runs),np.diff(Ps))
    pl.hlines(Pp,0,runs)

    pl.show()

def test1():

    mu0 = 0.4
    mu1 = 0.6
    s = np.sqrt(0.1)

    p = np.linspace(0.01,0.99,num=200)
    dist = p_belief_dist(p,mu0,mu1,s)

    u_lim = 0.5

    area = integrate.quad(p_belief_dist,0.01,u_lim,args=(mu0,mu1,s))
    print(area)

    mu0 = 0.3
    dist_1 = p_belief_dist(p,mu0,1-mu0,s)

    area = integrate.quad(p_belief_dist,0.01,u_lim,args=(mu0,mu1,s))
    print(area)

    mu0 = 0.48
    dist_2 = p_belief_dist(p,mu0,1-mu0,s)

    area = integrate.quad(p_belief_dist,0.01,u_lim,args=(mu0,mu1,s))
    print(area)

    font_size = 15
    font = {'size': font_size}

    pl.rc('font', **font)

    f = pl.figure()
    pl.plot(p,dist,'--b',label ='$\mu_ 0 = 0.4$',linewidth =1)
    pl.plot(p,dist_1,'-r',label ='$\mu_ 0 = 0.3$',linewidth =1)
    pl.plot(p,dist_2,'-.k',label ='$\mu_ 0 = 0.48$',linewidth =1)
    pl.vlines(0.5,0,14)
    leg = pl.legend(loc=1, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.ylabel('Probability density')
    pl.xlabel('private belief')

    f.savefig(os.getcwd()+'/'+'PRIVATE_BELIEF_DIST.pdf',format ='pdf')

    mu0 = 0.4
    mu1 = 0.6
    s = np.sqrt(0.1)
    q = np.linspace(0.01,0.99,num=200)
    q_comp = np.zeros(200)

    for i in range(200):
        q_comp[i] = integrate.quad(p_belief_dist,1-q[i],0.99,args=(mu0,mu1,s))[0]

    f = pl.figure()
    pl.plot(q,q_comp,'--b',label = '$\Pr(x = 1 | q = q)$')
    pl.plot(q,q,'-r',label = '$q$')
    leg = pl.legend(loc=2, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    pl.xlabel('Social belief')
    pl.ylabel('Average belief')
    pl.ylim([-0.01,1.01])
    pl.xlim([-0.01,1.01])

    f.savefig(os.getcwd()+'/'+'EQ_SOCIAL_BELIEF.pdf',format ='pdf')

    pl.show()

test1()
#test2()
#test3()
#generate_network()
#simulate_with_fixed_network(load_graph=True)
#simulate_with_fixed_network(load_graph=False)