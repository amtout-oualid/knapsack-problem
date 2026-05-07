import time
import random

# ==========================================
# Data for Instance 1 (n=100)
# ==========================================
n = 100
W = 1400

u = [4, 7, 8, 2, 1, 1, 9, 5, 5, 3, 9, 9, 5, 4, 4, 9, 3, 7, 9, 7, 10, 9, 1, 9, 5, 3, 2, 6, 2, 2, 3, 10, 4, 2, 4, 5, 9, 2, 5, 8, 5, 2, 9, 6, 1, 8, 10, 6, 1, 8, 6, 4, 8, 8, 8, 1, 8, 9, 9, 3, 5, 6, 3, 7, 6, 8, 8, 3, 4, 3, 10, 4, 6, 4, 2, 2, 6, 10, 10, 8, 3, 7, 7, 10, 8, 7, 1, 1, 4, 8, 5, 6, 3, 9, 8, 7, 6, 5, 5, 1]
w = [18, 16, 18, 11, 13, 17, 10, 19, 14, 17, 19, 12, 17, 10, 20, 16, 15, 16, 10, 20, 11, 20, 14, 16, 19, 13, 16, 19, 16, 12, 17, 11, 16, 17, 12, 12, 19, 13, 18, 14, 14, 16, 11, 10, 10, 19, 12, 13, 20, 20, 19, 12, 12, 18, 17, 20, 15, 16, 18, 10, 15, 19, 12, 16, 12, 15, 11, 12, 20, 20, 15, 18, 15, 13, 19, 15, 15, 11, 18, 11, 15, 18, 10, 18, 19, 12, 16, 17, 16, 17, 12, 12, 14, 15, 15, 15, 12, 16, 16, 12]

# Helper function
def evaluate(sol):
    return sum(u[i] for i in sol), sum(w[i] for i in sol)

# 1. Max Utility
def greedy_max_utility():
    start = time.time()
    items = sorted(range(n), key=lambda i: u[i], reverse=True)
    sol, cur_w = [], 0
    for i in items:
        if cur_w + w[i] <= W: sol.append(i); cur_w += w[i]
    val, weight = evaluate(sol)
    print(f"--- 1. Max Utility Greedy ---")
    print(f"Utility (Z): {val} | Weight: {weight}/{W} | CPU Time: {time.time()-start:.6f}s\n")

# 2. Min Weight
def greedy_min_weight():
    start = time.time()
    items = sorted(range(n), key=lambda i: w[i])
    sol, cur_w = [], 0
    for i in items:
        if cur_w + w[i] <= W: sol.append(i); cur_w += w[i]
    val, weight = evaluate(sol)
    print(f"--- 2. Min Weight Greedy ---")
    print(f"Utility (Z): {val} | Weight: {weight}/{W} | CPU Time: {time.time()-start:.6f}s\n")

# 3. Max Ratio
def greedy_max_ratio():
    start = time.time()
    items = sorted(range(n), key=lambda i: u[i]/w[i], reverse=True)
    sol, cur_w = [], 0
    for i in items:
        if cur_w + w[i] <= W: sol.append(i); cur_w += w[i]
    val, weight = evaluate(sol)
    print(f"--- 3. Max Ratio (Density) Greedy ---")
    print(f"Utility (Z): {val} | Weight: {weight}/{W} | CPU Time: {time.time()-start:.6f}s\n")

# 4. Tie-Breaking
def greedy_tie_break():
    start = time.time()
    items = sorted(range(n), key=lambda i: (u[i]/w[i], w[i]), reverse=True)
    sol, cur_w = [], 0
    for i in items:
        if cur_w + w[i] <= W: sol.append(i); cur_w += w[i]
    val, weight = evaluate(sol)
    print(f"--- 4. Tie-Breaking Greedy ---")
    print(f"Utility (Z): {val} | Weight: {weight}/{W} | CPU Time: {time.time()-start:.6f}s\n")

# 5. Randomized
def greedy_random():
    start = time.time()
    items = sorted(range(n), key=lambda i: u[i]/w[i], reverse=True)
    sol, cur_w = [], 0
    avail = [i for i in items if cur_w+w[i]<=W]
    while avail:
        ch = random.choice(avail[:3]) # k=3
        sol.append(ch)
        cur_w += w[ch]
        items.remove(ch)
        avail = [i for i in items if cur_w+w[i]<=W]
    val, weight = evaluate(sol)
    print(f"--- 5. Randomized Greedy ---")
    print(f"Utility (Z): {val} | Weight: {weight}/{W} | CPU Time: {time.time()-start:.6f}s\n")

if __name__ == "__main__":
    #greedy_max_utility()
    #greedy_min_weight()
    #greedy_max_ratio()
    #greedy_tie_break()
    greedy_random()