import random
import copy
import math
import time
import sys
import numpy as np

import heapq

def heapify(x):   
    heapq.heapify(x)

def push(heap, item):
    heapq.heappush(heap, -item)

def pop(heap):
    return -heapq.heappop(heap)

def build_heap(num_arr):
    heapify(num_arr)
    return num_arr

def karmarkar_karp(A):  # O(nlog(n))
    S = (A * (-1)).tolist()    
    heap = build_heap(S)    # O(nlog(n))
    elem1 = pop(heap)
    elem2 = pop(heap)
    while (elem2 != 0):
        push(heap, abs(elem1 - elem2))  # put/pop data it requires log(n)
        push(heap, 0)

        #print heap
        elem1 = pop(heap)
        elem2 = pop(heap)
    
    return elem1

def generate_randomize_instance(size):
    r_max = 10**12
    return np.random.randint(r_max, size=size, dtype=np.int64)    

#RepRandom -- Stan
def rand_solution_standard(size):
    return np.random.randint(2, size=size, dtype=np.int64) * 2 - 1
    
def calc_residual_using_standard(size, A, S):
    residual = np.dot(A, S)        
    return abs(residual)

def repeated_random_using_standard(size, A, max_iter, start):
    S = start
    for i in range(max_iter):
        S_1 = rand_solution_standard(size)
        if calc_residual_using_standard(size, A, S_1) < calc_residual_using_standard(size, A, S):
            S = S_1
    return calc_residual_using_standard(size, A, S)

#RepRandom -- PP
def rand_solution_prepartition(size):
    return np.random.randint(size, size=size, dtype=np.int64).tolist()    

def new_sequence_from_prepartition(size, P, A):
    # A_prime = copy.copy(A)
    A_prime = A.tolist()
    for j in range(size):
        if P[j] != j:
            temp = A[j]
            A_prime[P[j]] += temp
            A_prime[j] -= temp
    return np.array(A_prime)
    

def repeated_random_using_prepartition(size, A, max_iter, start):
    S = new_sequence_from_prepartition(size, start, A)
    for i in range(max_iter):
        S_1 = new_sequence_from_prepartition(size, rand_solution_prepartition(size), A)
        if karmarkar_karp(S_1) < karmarkar_karp(S):
            S = S_1
    return karmarkar_karp(S)

#HillClimb -- Stan
def rand_neighbor_standard(size, S):
    X = copy.copy(S)
    i = int(random.random() * size)
    j = int(random.random() * size)
    while i == j:
        j = int(random.random() * size)
    X[i] *= -1 
    if (random.random() < 0.5):
        X[j] *= -1
    return X
            
def hill_climb_standard(size, A, max_iter, start):
    S = start
    res_0 = calc_residual_using_standard(size, A, S)
    for x in range(max_iter):
        S_1 = rand_neighbor_standard(size, S)
        res_1 = calc_residual_using_standard(size, A, S_1)
        if res_1 < res_0:
            S = S_1
            res_0 = calc_residual_using_standard(size, A, S)
    return calc_residual_using_standard(size, A, S)

# HillClimb -- PP
def rand_neighbor_prepartition(size, P):
    X = copy.copy(P)
    i = int(random.random() * size)
    j = int(random.random() * size)
    while P[i] == j:
        j = int(random.random() * size)
    X[i] = j
    return X

def hill_climb_prepartition(size, A, max_iter, start):
    P = start
    S = new_sequence_from_prepartition(size, P, A)
    for x in range(max_iter):
        P_1 = rand_neighbor_prepartition(size, P)
        S_1 = new_sequence_from_prepartition(size, P_1, A)
        if karmarkar_karp(S_1) < karmarkar_karp(S):
            S = S_1
    return karmarkar_karp(S)

#SimAn -- Stan
def T(x):
    return (10**10)*(0.8 ** (x/300))

def simulated_annealing_standard(size, A, max_iter, start):
    S = start
    S_2 = copy.copy(S)
    for i in range(max_iter):
        S_1 = rand_neighbor_standard(size, S) 
        res_0 = calc_residual_using_standard(size, A, S)
        res_1 = calc_residual_using_standard(size, A, S_1)
        if res_1 < res_0:
            S = S_1
        elif random.random() < math.exp(-(res_1 - res_0)/T(i)):
            S = S_1
        if calc_residual_using_standard(size, A, S) < calc_residual_using_standard(size, A, S_2):
            S_2 = copy.copy(S)
    return calc_residual_using_standard(size, A, S_2)

#Simulated Annealing -- PP
def simulated_annealing_prepartition(size, A, max_iter, start):
    P = start
    P_2 = copy.copy(P)
    res_0 = karmarkar_karp(new_sequence_from_prepartition(size, P, A))
    res_2 = karmarkar_karp(new_sequence_from_prepartition(size, P_2, A))
    for i in range(max_iter):
        P_1 = rand_neighbor_prepartition(size, P)
        res_1 = karmarkar_karp(new_sequence_from_prepartition(size, P_1, A))
        if res_1 < res_0:
            P = P_1
            res_0 = karmarkar_karp(new_sequence_from_prepartition(size, P, A))
        elif random.random() < math.exp(-(res_1 - res_0)/T(i)):
            P = P_1
            res_0 = karmarkar_karp(new_sequence_from_prepartition(size, P, A))
        if res_0 < res_2:
            P_2 = copy.copy(P)
            res_2 = karmarkar_karp(new_sequence_from_prepartition(size, P_2, A))
    return karmarkar_karp(new_sequence_from_prepartition(size, P_2, A))


def main():
    start_all = time.time()
    
    random.seed()
    size = 100
    max_iter = 25000
    # max_iter = 2500
    trials = 100
    
    RR_stan = 0
    RR_pp = 0
    KK_sum = 0
    HC_stan = 0
    HC_pp = 0
    SA_stan = 0
    SA_pp = 0

    KK_time = 0
    RR_stan_time = 0
    RR_pp_time = 0
    HC_stan_time = 0
    HC_pp_time = 0
    SA_stan_time = 0
    SA_pp_time = 0

    if len(sys.argv) > 1:
        algorithm = int(sys.argv[2])
        inputfile = sys.argv[3]
        fp = open(inputfile, "r")
        lines = fp.readlines()
        fp.close()

        instance = []
        for row in lines:
            instance.append(int(row))

        instance = np.array(instance)

        result = 0
        stan_start = rand_solution_standard(size)
        pp_start = rand_solution_prepartition(size)

        if algorithm == 0: 
            result = karmarkar_karp(instance)               
        elif algorithm == 1: 
            result = repeated_random_using_standard(size, instance, max_iter, stan_start)
        elif algorithm == 2: 
            result = hill_climb_standard(size, instance, max_iter, stan_start)
        elif algorithm == 3: 
            result = hill_climb_standard(size, instance, max_iter, stan_start)
        elif algorithm == 11: 
            result = repeated_random_using_prepartition(size, instance, max_iter, pp_start)
        elif algorithm == 12: 
            result = hill_climb_prepartition(size, instance, max_iter, pp_start)            
        elif algorithm == 13: 
            result = simulated_annealing_prepartition(size, instance, max_iter, pp_start)
        print(result)

    else:
        for i in range(trials):
            stan_start = rand_solution_standard(size)
            pp_start = rand_solution_prepartition(size)
            
            instance = generate_randomize_instance(size)

            #karmarkar_karp 
            start = time.time()
            KK_sum += karmarkar_karp(instance)
            end = time.time()
            KK_time += (end - start)
            
            #RR_stan
            start = time.time()
            RR_stan += repeated_random_using_standard(size, instance, max_iter, stan_start)
            end = time.time()
            RR_stan_time += (end - start)
            
            #RR_pp
            start = time.time()
            RR_pp += repeated_random_using_prepartition(size, instance, max_iter, pp_start)
            end = time.time()
            RR_pp_time += (end - start)

            #HC_stan
            start = time.time()
            HC_stan += hill_climb_standard(size, instance, max_iter, stan_start)
            end = time.time()
            HC_stan_time += (end - start)

            #HC_pp
            start = time.time()
            HC_pp += hill_climb_prepartition(size, instance, max_iter, pp_start)
            end = time.time()
            HC_pp_time += (end - start)

            #SA_stan
            start = time.time()
            SA_stan += simulated_annealing_standard(size, instance, max_iter, stan_start)
            end = time.time()
            SA_stan_time += (end - start)

            #SA_pp
            start = time.time()
            SA_pp += simulated_annealing_prepartition(size, instance, max_iter, pp_start)
            end = time.time()
            SA_pp_time += (end - start)

        end_all = time.time()
        time_all = end_all - start_all
        
        print("KK avg: ", int(KK_sum/trials))
        print("avg time: ", KK_time/trials)
        print("\n")
        print("RR_stan avg: ", int(RR_stan/trials))
        print("avg time: ", RR_stan_time/trials)
        print("\n")
        print("RR_pp avg: ", int(RR_pp/trials))
        print("avg time: ", RR_pp_time/trials)
        print("\n")
        print("HC_stan avg: ", int(HC_stan/trials))
        print("avg time: ", HC_stan_time/trials)
        print("\n")
        print("HC_pp avg: ", int(HC_pp/trials))
        print("avg time: ", HC_pp_time/trials)
        print("\n")
        print("SA_stan avg: ", int(SA_stan/trials))
        print("avg time: ", SA_stan_time/trials)
        print("\n")
        print("SA_pp avg: ", int(SA_pp/trials))
        print("avg time: ", SA_pp_time/trials)
        print("\n")
        
        print("time_all: ", time_all)
        
main()
