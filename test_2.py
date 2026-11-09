from labyrinth import createLabCSP

n = 4
csp = createLabCSP(n, minimum_walls=1)
solution = csp.backtracking_search()

if solution is False:
    print("No solution")
else:
    for row in range(n):
        print([solution[row * n + col] for col in range(n)])

