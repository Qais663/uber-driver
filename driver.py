import numpy as np

class Driver:
    """
    Represents a driver in the ride-hailing system.

    Attributes:
        driver_id : unique identifier (e.g. D1, D2 ...)
        position  : (row, col) on the city grid
        speed     : travel speed in km/h (random 30–120)
        status    : 'available' or 'busy'
    """

    def __init__(self, driver_id: int, position: tuple, rng: np.random.Generator):
        """
        Args:
            driver_id : integer ID, will be displayed as D1, D2 ...
            position  : (row, col) assigned by City when placing on grid
            rng       : numpy random generator passed from City (shared seed)
        """
        self.driver_id = f"D{driver_id}"
        self.position  = position
        self.speed     = int(rng.integers(30, 121))   # random 30–120 km/h
        self.status    = "available"

    def set_busy(self) -> None:
        """Mark driver as busy (assigned to a ride)."""
        self.status = "busy"

    def set_available(self) -> None:
        """Mark driver as available again (ride completed)."""
        self.status = "available"

    def is_available(self) -> bool:
        """Return True if driver can accept a ride."""
        return self.status == "available"

    def __repr__(self) -> str:
        return (
            f"Driver({self.driver_id} | "
            f"pos={self.position} | "
            f"speed={self.speed}km/h | "
            f"status={self.status})"
        )


# ── Demo ──────────────────────────────────────────────
if __name__ == "__main__":
    rng = np.random.default_rng()

    drivers = [
        Driver(driver_id=i, position=(i, i*2), rng=rng)
        for i in range(1, 6)
    ]

    for d in drivers:
        print(d)

    # Simulate assigning a ride
    print("\n-- Assigning ride to D1 --")
    drivers[0].set_busy()
    print(drivers[0])

    print("\n-- Available drivers --")
    for d in drivers:
        if d.is_available():
            print(f"  {d.driver_id} at {d.position} ({d.speed} km/h)")