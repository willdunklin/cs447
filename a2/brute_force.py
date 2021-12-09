# the general idea is to build strings of states and record the probabilities of each 
#   state occurring in a dictionary
# when generating a new string, rely on the dictionary for lookup of string[:-1]
#   and compute in the same way as viterbi/forward algorithm
# we can also terminate calculations if a prefix of string s has probability of occurring = 0
#   i.e. that string could not occur
# finally we skim off the strings of full length whose probabilities are non-zero

# this is terrible, inefficient code but does get us the desired brute force answer
import numpy as np

def brute_force(P: np.array, Q: np.array, X: np.array, n: int, m: int) -> tuple((dict, float, list)):
    solution_dict = {}
    # keys to this dict are string representations of lists of states
    prob = {}

    # initial distribution
    prob[str([0])] = Q[0][X[0]]
    for i in range(1, n):
        prob[str([i])] = 0

    # loop over all strings
    for s in range(n**m):
        string = []
        # go through each "digit" of a string
        for i in reversed(range(m)):
            # extract the ith digit of s in base n
            state = (s // (n**i)) % n
            string.append(state)

            # if this string has been calculated before, skip
            if str(string) in prob.keys():
                continue

            # if the prefix of the string is in the dictionary
            #   do viterbi-esque calculation to store in probability dictionary
            if str(string[:-1]) in prob.keys():

                # if the probability of the prefix is 0
                if prob[str(string[:-1])] == 0:
                    # set the probability of this string to 0
                    prob[str(string)] = 0
                    continue

                # otherwise: calculate the probability using viterbi
                # probability(string) =  P(prefix) * Q[c][X[len(out)-1]] * P(prev -> c)
                #                        previous  *       output        *  transition
                prob[str(string)] = prob[str(string[:-1])] * Q[state][X[len(string)-1]] * P[string[-2]][state]

            # if this is a valid final string, add it to the solutions dictionary
            if len(string) == m and prob[str(string)] != 0:
                solution_dict[stringify(string)] = prob[str(string)]

    # num solutions, num strings logged, num possible strings
    # print(len(solution_dict), len(prob), n**(m+1)-1)

    # return solution 
    key = max(solution_dict, key=solution_dict.get)
    max_string = [int(x) for x in key.split()]
    return solution_dict, solution_dict[key], max_string

# convert to parsible key string for solution dictionary
def stringify(xs: list) -> str:
    out = ''
    for x in xs:
        out += f'{x} '
    return out