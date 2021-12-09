# general idea:
#   search for most likely "path" of nodes (coins) using viterbi algorithm

import numpy as np
from brute_force import brute_force, stringify

# CHANGE THIS TO FALSE IF YOU DONT WANT BRUTE FORCED SOLUTION
bf = True


## DATA SETUP

test = 2 # index for tests
chain = open(f'tests/chain-{test}.txt')
emit = open(f'tests/emit-{test}.txt')
obs = open(f'tests/obs-{test}.txt')

floats = [[float(x) for x in line.split()] for line in chain.readlines() if len(line) > 0]
P = np.array(floats).T
# P[a][b] = probability of going from coin a to coin b

Q = np.array([float(x) for x in emit.readlines()])
Q = np.vstack((1 - Q, Q)).T
# Q[c][x] = probability of getting result x given coin c

X = np.array([int(x) for x in obs.read().split()])
# X[i] = result (H/T) at round i

# number of coins
n = Q.shape[0]
# number of samples
m = X.shape[0]

print(P)
print(Q)
print(X)
print()


## ALGORITHM

v = np.zeros((m, n))
# v[i][c] = viterbi value of coin c in ith round

# set base case
# assumed starting with coin 0
v[0][0] = Q[0][X[0]] # probability of getting X[0] given coin 0

# rounds i = 1..m
for i in range(1, m):
    # current coin
    for curr in range(n):
        max_k = 0
        # previous coin in previous round
        for prev in range(n):
            # if max of the kth
            if max_k < v[i-1][prev] * P[prev][curr]:
                max_k = v[i-1][prev] * P[prev][curr]
        # v[] P(X[i] | coin) * max_k (P(coin | k) * v_i-1(k))
        v[i][curr] = Q[curr][X[i]] * max_k


## SOLUTION

# this is our pure viterbi maximum
#   this will tell us the probability for the most likely state string
print(f'{v}\n')
# by taking the argmax at each step we should get the optimal path right? 
optimal_path = np.array([np.argmax(r) for r in v])
print('naive solution:\n', optimal_path, '\n')


# no, this argmax is actually wrong.
# look at example 2: the "optimal" path is not even possible because it tries 
#   to go from state 1 -> 0, which has a 0 probability
# moreover, with example 3, the solution is just wrong from being optimal

# to fix this, lets iterate back through the viterbi matrix and correct by 
#   enforcing our state transition distribution at each step 
original = optimal_path.copy()


# basically backwards viterbi simplified
# going backwards from: i=m-1..1
for i in range(m-1, 0, -1):
    # elem-wise multiply the probabilities of going to the optimal node at 
    #   round i (this we know is optimal) from each node at round i-1
    v[i-1] *= P.T[optimal_path[i]]
    # now recompute the i-1'th optimal node based on our adjusted understanding 
    #   of what is possible
    optimal_path[i-1] = np.argmax(v[i-1])


# now we have an optimal solution that behaves our transition laws and accurately
#   reflects the costs of moving 
print(f'\n{v}\n')
print('our solution:\n', optimal_path)
with open(f'solution-{test}.txt', 'w') as sol:
    sol.write(stringify(optimal_path))
print()


if bf:
    # but is our correction actually optimal? there is only one way to find out:
    #   brute force the solution (who needs proofs?)
    solution_dict, max_prob, max_string = brute_force(P, Q, X, n, m)

    print('brute force solution:')
    print('', np.array(max_string), '\n\n')
    # compare difference b/w brute force optimal and ours
    print('Difference b/w our solution and brute force:')
    print(' Brute force is', (max_prob - v[-1][optimal_path[-1]])/v[-1][optimal_path[-1]], 'times better')
    print()

    # this is code comparing our solution before correction to our brute force optimum 
    original_key = stringify(original)
    print('Difference b/w naive soltuion and brute force:')
    if original_key in solution_dict.keys():
        print(' Brute force is', (max_prob - solution_dict[original_key])/solution_dict[original_key], 'times better\n')
    else:
        print('', original, 'is an invalid solution\n')