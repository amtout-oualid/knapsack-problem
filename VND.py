import time
import random

# ==========================================
# Data for Instance 1 (n=100)
# ==========================================
n = 100
W = 1400
u = [4, 7, 8, 2, 1, 1, 9, 5, 5, 3, 9, 9, 5, 4, 4, 9, 3, 7, 9, 7, 10, 9, 1, 9, 5, 3, 2, 6, 2, 2, 3, 10, 4, 2, 4, 5, 9, 2, 5, 8, 5, 2, 9, 6, 1, 8, 10, 6, 1, 8, 6, 4, 8, 8, 8, 1, 8, 9, 9, 3, 5, 6, 3, 7, 6, 8, 8, 3, 4, 3, 10, 4, 6, 4, 2, 2, 6, 10, 10, 8, 3, 7, 7, 10, 8, 7, 1, 1, 4, 8, 5, 6, 3, 9, 8, 7, 6, 5, 5, 1]
w = [18, 16, 18, 11, 13, 17, 10, 19, 14, 17, 19, 12, 17, 10, 20, 16, 15, 16, 10, 20, 11, 20, 14, 16, 19, 13, 16, 19, 16, 12, 17, 11, 16, 17, 12, 12, 19, 13, 18, 14, 14, 16, 11, 10, 10, 19, 12, 13, 20, 20, 19, 12, 12, 18, 17, 20, 15, 16, 18, 10, 15, 19, 12, 16, 12, 15, 11, 12, 20, 20, 15, 18, 15, 13, 19, 15, 15, 11, 18, 11, 15, 18, 10, 18, 19, 12, 16, 17, 16, 17, 12, 12, 14, 15, 15, 15, 12, 16, 16, 12]

def evaluate(sol): return sum(u[i] for i in range(n) if sol[i])
def get_weight(sol): return sum(w[i] for i in range(n) if sol[i])

# 0. Initial Solution (Min Weight: Z=532)
def get_initial_solution():
    items = sorted(range(n), key=lambda i: w[i])
    sol, cur_w = [0]*n, 0
    for i in items:
        if cur_w + w[i] <= W: sol[i] = 1; cur_w += w[i]
    return sol

# 1. 1-Flip Local Search
def ls_1_flip(sol):
    curr = list(sol)
    v_curr, w_curr = evaluate(curr), get_weight(curr)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            new_w = w_curr - w[i] if curr[i] == 1 else w_curr + w[i]
            new_v = v_curr - u[i] if curr[i] == 1 else v_curr + u[i]
            if new_w <= W and new_v > v_curr:
                curr[i] = 1 - curr[i]; v_curr, w_curr = new_v, new_w
                improved = True; break
    return curr

# 2. Swap Local Search
def ls_swap(sol):
    curr = list(sol)
    v_curr, w_curr = evaluate(curr), get_weight(curr)
    improved = True
    while improved:
        improved = False
        in_knap = [i for i in range(n) if curr[i] == 1]
        out_knap = [i for i in range(n) if curr[i] == 0]
        for i in in_knap:
            for j in out_knap:
                new_w = w_curr - w[i] + w[j]
                new_v = v_curr - u[i] + u[j]
                if new_w <= W and new_v > v_curr:
                    curr[i], curr[j] = 0, 1
                    v_curr, w_curr = new_v, new_w
                    improved = True; break
            if improved: break
    return curr

# 3. VND Algorithm
def run_vnd(x_init):
    x = list(x_init)
    k, k_max = 1, 2
    while k <= k_max:
        if k == 1: x_p = ls_1_flip(x)
        else: x_p = ls_swap(x)
        if evaluate(x_p) > evaluate(x):
            x = list(x_p); k = 1
        else: k += 1
    return x

# 4. VNS Shaking
def shaking(sol, k):
    x_p = list(sol)
    for _ in range(k):
        idx = random.randint(0, n-1)
        x_p[idx] = 1 - x_p[idx]
        while get_weight(x_p) > W:
            x_p[idx] = 1 - x_p[idx] # Revert
            idx = random.randint(0, n-1)
            x_p[idx] = 1 - x_p[idx]
    return x_p

# 5. VNS Algorithm
def run_vns(x_init, duration=2.0):
    start = time.time()
    x = list(x_init)
    while time.time() - start < duration:
        k = 1
        while k <= 3:
            x_p = shaking(x, k)
            x_pp = ls_1_flip(x_p) # Intensification
            if evaluate(x_pp) > evaluate(x):
                x = list(x_pp); k = 1
            else: k += 1
    return x

# ==========================================
# Execution and Comparison
# ==========================================
if __name__ == "__main__":
    init_sol = get_initial_solution()
    
    print("="*55)
    print(f"{'METAHEURISTIC':<15} | {'UTILITY (Z)':<12} | {'CPU TIME'}")
    print("="*55)
    
    # Run VND
    start_vnd = time.time()
    vnd_sol = run_vnd(init_sol)
    time_vnd = time.time() - start_vnd
    print(f"{'VND':<15} | {evaluate(vnd_sol):<12} | {time_vnd:.6f} s")
    
    # Run VNS
    start_vns = time.time()
    vns_sol = run_vns(init_sol, duration=2.0)
    time_vns = time.time() - start_vns
    print(f"{'VNS':<15} | {evaluate(vns_sol):<12} | {time_vns:.6f} s")
    print("="*55)