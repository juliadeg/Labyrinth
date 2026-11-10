
from labyrinth import createLabCSP

n = 4
csp = createLabCSP(n, minimum_walls=1)
solution = csp.backtracking_search()

if solution is False:
    print("No solution")
else:
    print("\n🚩 Start    🏁 Goal\n")
    for row in range(n):
        tiles = []
        for col in range(n):
            cell = solution[row * n + col]
            if cell == 1:
                tiles.append("██")
            elif col == 0:
                tiles.append("🚩")
            elif col == n - 1:
                tiles.append("🏁")
            else:
                tiles.append("  ")
        print("".join(tiles))

