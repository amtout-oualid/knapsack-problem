import time
import random

# ==========================================
# Data for Instance 1 (n=100, W=1400)
# ==========================================
n = 100
W = 1400
u = [4, 7, 8, 2, 1, 1, 9, 5, 5, 3, 9, 9, 5, 4, 4, 9, 3, 7, 9, 7, 10, 9, 1, 9, 5, 3, 2, 6, 2, 2, 3, 10, 4, 2, 4, 5, 9, 2, 5, 8, 5, 2, 9, 6, 1, 8, 10, 6, 1, 8, 6, 4, 8, 8, 8, 1, 8, 9, 9, 3, 5, 6, 3, 7, 6, 8, 8, 3, 4, 3, 10, 4, 6, 4, 2, 2, 6, 10, 10, 8, 3, 7, 7, 10, 8, 7, 1, 1, 4, 8, 5, 6, 3, 9, 8, 7, 6, 5, 5, 1]
w = [18, 16, 18, 11, 13, 17, 10, 19, 14, 17, 19, 12, 17, 10, 20, 16, 15, 16, 10, 20, 11, 20, 14, 16, 19, 13, 16, 19, 16, 12, 17, 11, 16, 17, 12, 12, 19, 13, 18, 14, 14, 16, 11, 10, 10, 19, 12, 13, 20, 20, 19, 12, 12, 18, 17, 20, 15, 16, 18, 10, 15, 19, 12, 16, 12, 15, 11, 12, 20, 20, 15, 18, 15, 13, 19, 15, 15, 11, 18, 11, 15, 18, 10, 18, 19, 12, 16, 17, 16, 17, 12, 12, 14, 15, 15, 15, 12, 16, 16, 12]

# --- Helpers ---
def evaluate(sol): return sum(u[i] for i in range(n) if sol[i])
def get_weight(sol): return sum(w[i] for i in range(n) if sol[i])

# --- Local Search Components (for VND) ---
def ls_1_flip(sol):
    curr = list(sol)
    v_c, w_c = evaluate(curr), get_weight(curr)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            new_w = w_c - w[i] if curr[i] == 1 else w_c + w[i]
            new_v = v_c - u[i] if curr[i] == 1 else v_c + u[i]
            if new_w <= W and new_v > v_c:
                curr[i] = 1 - curr[i]; v_c, w_c = new_v, new_w
                improved = True; break
    return curr

def ls_swap(sol):
    curr = list(sol)
    v_c, w_c = evaluate(curr), get_weight(curr)
    improved = True
    while improved:
        improved = False
        in_k = [i for i in range(n) if curr[i] == 1]
        out_k = [i for i in range(n) if curr[i] == 0]
        for i in in_k:
            for j in out_k:
                new_w = w_c - w[i] + w[j]
                new_v = v_c - u[i] + u[j]
                if new_w <= W and new_v > v_c:
                    curr[i], curr[j] = 0, 1; v_c, w_c = new_v, new_w
                    improved = True; break
            if improved: break
    return curr

def run_vnd(x_init):
    x = list(x_init)
    k, k_max = 1, 2
    while k <= k_max:
        x_p = ls_1_flip(x) if k == 1 else ls_swap(x)
        if evaluate(x_p) > evaluate(x):
            x = list(x_p); k = 1
        else: k += 1
    return x

# --- VNS Components ---
def shaking_1_flip(sol, k):
    x_p = list(sol)
    for _ in range(k):
        idx = random.randint(0, n-1)
        x_p[idx] = 1 - x_p[idx]
        while get_weight(x_p) > W:
            x_p[idx] = 1 - x_p[idx]; idx = random.randint(0, n-1); x_p[idx] = 1 - x_p[idx]
    return x_p

def run_vns(x_init, duration=2.0):
    start_time = time.time()
    best_x = list(x_init)
    while time.time() - start_time < duration:
        k, k_max = 1, 5
        while k <= k_max:
            x_p = shaking_1_flip(best_x, k)
            x_pp = run_vnd(x_p)
            if evaluate(x_pp) > evaluate(best_x):
                best_x = list(x_pp); k = 1
            else: k += 1
    return best_x

# --- Main Execution ---
if __name__ == "__main__":
    # Initial Solution: Min Weight Greedy (Z=532)
    items = sorted(range(n), key=lambda i: w[i])
    init_sol, cur_w = [0]*n, 0
    for i in items:
        if cur_w + w[i] <= W: init_sol[i] = 1; cur_w += w[i]
    
    print("-" * 50)
    print("Variable Neighborhood Search (VNS) Execution")
    print("-" * 50)
    
    start_cpu = time.time()
    final_sol = run_vns(init_sol, duration=2.0)
    cpu_time = time.time() - start_cpu
    
    print(f"[*] Final Utility (Z): {evaluate(final_sol)}")
    print(f"[*] CPU Time: {cpu_time:.6f} seconds")
    print("-" * 50)