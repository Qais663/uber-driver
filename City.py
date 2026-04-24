import numpy as np
from collections import deque
from driver import Driver
from request import RideRequest

class City:
    """
    Represents a city as a 2D grid for a simplified ride-hailing system.

    Cell values:
        0  → empty road
        X  → blocked cell
        D  → driver
        P  → passenger pickup point
        R  → destination (ride end)
    """

    EMPTY       = '0'
    BLOCKED     = 'X'
    DRIVER      = 'D'
    PASSENGER   = 'P'
    DESTINATION = 'R'

    def __init__(self, rows: int = 5, cols: int = 5, seed: int = None):
        self.rows = rows
        self.cols = cols
        self.rng  = np.random.default_rng(seed)

        total_cells = rows * cols

        # Scale entity counts
        num_blocked      = max(1, int(total_cells * 0.15))
        num_drivers      = max(1, int(total_cells * 0.04))
        num_passengers   = max(1, int(total_cells * 0.04))
        num_destinations = max(1, int(total_cells * 0.04))

        total_entities = num_blocked + num_drivers + num_passengers + num_destinations

        if total_entities > total_cells:
            raise ValueError(
                f"Too many entities ({total_entities}) for a {rows}x{cols} grid "
                f"({total_cells} cells)."
            )

        # Build grid
        flat = np.array(
            [self.BLOCKED]      * num_blocked      +
            [self.DRIVER]       * num_drivers      +
            [self.PASSENGER]    * num_passengers   +
            [self.DESTINATION]  * num_destinations +
            [self.EMPTY]        * (total_cells - total_entities),
            dtype='<U1'
        )
        self.rng.shuffle(flat)
        self.grid = flat.reshape(rows, cols)

        # Drivers
        driver_positions = self._find(self.DRIVER)
        self.drivers = [
            Driver(driver_id=i + 1, position=pos, rng=self.rng)
            for i, pos in enumerate(driver_positions)
        ]

        # Requests
        passenger_positions   = self._find(self.PASSENGER)
        destination_positions = self._find(self.DESTINATION)

        self.requests = [
            RideRequest(request_id=i + 1, pickup=p, destination=d)
            for i, (p, d) in enumerate(zip(passenger_positions, destination_positions))
        ]

        self.blocked_positions = self._find(self.BLOCKED)

        self.edge_weights = self._build_edge_weights()

    # ─────────────────────────────────────────────
    def _find(self, symbol: str) -> list:
        positions = np.argwhere(self.grid == symbol)
        return [tuple(p) for p in positions]

    def is_passable(self, row: int, col: int) -> bool:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
        return self.grid[row, col] != self.BLOCKED

    def get_cell(self, row: int, col: int) -> str:
        return self.grid[row, col]

    def set_cell(self, row: int, col: int, symbol: str) -> None:
        self.grid[row, col] = symbol

    # ─────────────────────────────────────────────
    def _build_edge_weights(self) -> dict:
        weights    = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for r in range(self.rows):
            for c in range(self.cols):
                if not self.is_passable(r, c):
                    continue
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not self.is_passable(nr, nc):
                        continue
                    edge = ((r, c), (nr, nc))
                    if edge not in weights:
                        w = int(self.rng.integers(10, 101))
                        weights[edge]               = w
                        weights[((nr, nc), (r, c))] = w
        return weights

    def get_weight(self, a: tuple, b: tuple) -> int:
        return self.edge_weights.get((a, b), -1)

    # ─────────────────────────────────────────────

    def manhattan_distance(self, a: tuple, b: tuple) -> int:
        """
        Calculate Manhattan distance between two points.
        |x1-x2| + |y1-y2|
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def distance(self, start: tuple, end: tuple) -> int:
        if start == end:
            return 0

        visited = set()
        queue   = deque([(start, 0)])
        visited.add(start)

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        while queue:
            (row, col), dist = queue.popleft()
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                neighbor = (nr, nc)

                if neighbor == end:
                    return dist + 1

                if neighbor not in visited and self.is_passable(nr, nc):
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return -1

    def travel_time(self, start: tuple, end: tuple, speed: int) -> float:
        if start == end:
            return 0.0

        visited = set()
        queue   = deque([(start, 0)])
        visited.add(start)

        directions = [(-1,0),(1,0),(0,-1),(0,1)]

        while queue:
            (row, col), total_w = queue.popleft()
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                neighbor = (nr, nc)

                w = self.edge_weights.get(((row, col), neighbor))
                if w is None:
                    continue

                new_total = total_w + w

                if neighbor == end:
                    return round(new_total / (speed * 1000) * 60, 2)

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, new_total))

        return -1.0

    # ─────────────────────────────────────────────
    def display(self) -> None:
        print(f"\n{'─' * (self.cols * 2 + 1)}")
        for row in self.grid:
            print(' '.join(row))
        print(f"{'─' * (self.cols * 2 + 1)}\n")

    def display_drivers(self) -> None:
        print("\n── Drivers ──")
        for d in self.drivers:
            print(f"  {d}")

    def display_requests(self) -> None:
        print("\n── Ride Requests ──")
        for r in self.requests:
            print(f"  {r}")

    def display_weights(self) -> None:
        print("\n── Edge Weights ──")
        seen = set()
        for (a, b), w in self.edge_weights.items():
            if (b, a) not in seen:
                print(f"  {a} <-> {b} : {w}m")
                seen.add((a, b))

    def __repr__(self) -> str:
        return f"City({self.rows}x{self.cols} | drivers={len(self.drivers)} | requests={len(self.requests)})"


# ── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    city = City(rows=5, cols=5)
    city.display()
    print(city)

    city.display_drivers()
    city.display_requests()

    print("\n── Travel Times ──")
    for driver in city.drivers:
        for req in city.requests:
            t = city.travel_time(driver.position, req.pickup, driver.speed)
            print(
                f"{driver.driver_id} ({driver.speed}km/h) -> {req.request_id} {req.pickup} : "
                f"{'unreachable' if t == -1.0 else f'{t} min'}"
            )

