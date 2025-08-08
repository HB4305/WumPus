self.grid[y][x].wumpus = False
                # remove stench from neighbors
                for nx, ny in get_neighbors((x, y), self.size):
                    print(f"[ENV] Removing stench from ({nx}, {ny})")
                    if self.in_bounds(nx, ny):
                        # Check if there are other wumpus nearby
                        has_other_wumpus = False
                        for wnx, wny in get_neighbors((nx, ny), self.size):
                            if (wnx, wny) in self.wumpus_positions:
                                print (f"[ENV] Found another wum