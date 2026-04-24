<<<<<<< HEAD
import numpy as np

class RideRequest:
    """
    Represents a passenger ride request in the ride-hailing system.

    Attributes:
        request_id  : unique identifier (e.g. R1, R2 ...)
        pickup      : (row, col) passenger pickup point on the grid
        destination : (row, col) passenger destination on the grid
        status      : 'pending', 'assigned', or 'completed'
        assigned_driver : the Driver object assigned to this request (or None)
    """

    def __init__(self, request_id: int, pickup: tuple, destination: tuple):
        """
        Args:
            request_id  : integer ID, displayed as R1, R2 ...
            pickup      : (row, col) of the passenger pickup point (P)
            destination : (row, col) of the destination (R)
        """
        self.request_id      = f"R{request_id}"
        self.pickup          = pickup
        self.destination     = destination
        self.status          = "pending"
        self.assigned_driver = None

    def assign(self, driver) -> None:
        """Assign a driver to this request."""
        self.assigned_driver = driver
        self.status          = "assigned"
        driver.set_busy()

    def complete(self) -> None:
        """Mark the request as completed and free the driver."""
        self.status = "completed"
        if self.assigned_driver:
            self.assigned_driver.set_available()

    def is_pending(self) -> bool:
        return self.status == "pending"

    def is_assigned(self) -> bool:
        return self.status == "assigned"

    def is_completed(self) -> bool:
        return self.status == "completed"

    def __repr__(self) -> str:
        driver_info = (
            self.assigned_driver.driver_id
            if self.assigned_driver else "None"
        )
        return (
            f"RideRequest({self.request_id} | "
            f"pickup={self.pickup} | "
            f"destination={self.destination} | "
            f"status={self.status} | "
            f"driver={driver_info})"
        )


# ── Demo ──────────────────────────────────────────────
if __name__ == "__main__":

    from driver import Driver

    rng = np.random.default_rng()

    # Create some requests
    requests = [
        RideRequest(1, pickup=(1, 2), destination=(4, 4)),
        RideRequest(2, pickup=(0, 3), destination=(3, 1)),
        RideRequest(3, pickup=(2, 0), destination=(4, 2)),
    ]

    print("── Ride Requests ──")
    for r in requests:
        print(r)

    # Create a driver and assign to first request
    driver = Driver(driver_id=1, position=(0, 0), rng=rng)
    print(f"\n-- Assigning {driver.driver_id} to {requests[0].request_id} --")
    requests[0].assign(driver)
    print(requests[0])
    print(driver)

    # Complete the ride
    print(f"\n-- Completing {requests[0].request_id} --")
    requests[0].complete()
    print(requests[0])
    print(driver)
=======
import numpy as np

class RideRequest:
    """
    Represents a passenger ride request in the ride-hailing system.

    Attributes:
        request_id  : unique identifier (e.g. R1, R2 ...)
        pickup      : (row, col) passenger pickup point on the grid
        destination : (row, col) passenger destination on the grid
        status      : 'pending', 'assigned', or 'completed'
        assigned_driver : the Driver object assigned to this request (or None)
    """

    def __init__(self, request_id: int, pickup: tuple, destination: tuple):
        """
        Args:
            request_id  : integer ID, displayed as R1, R2 ...
            pickup      : (row, col) of the passenger pickup point (P)
            destination : (row, col) of the destination (R)
        """
        self.request_id      = f"R{request_id}"
        self.pickup          = pickup
        self.destination     = destination
        self.status          = "pending"
        self.assigned_driver = None

    def assign(self, driver) -> None:
        """Assign a driver to this request."""
        self.assigned_driver = driver
        self.status          = "assigned"
        driver.set_busy()

    def complete(self) -> None:
        """Mark the request as completed and free the driver."""
        self.status = "completed"
        if self.assigned_driver:
            self.assigned_driver.set_available()

    def is_pending(self) -> bool:
        return self.status == "pending"

    def is_assigned(self) -> bool:
        return self.status == "assigned"

    def is_completed(self) -> bool:
        return self.status == "completed"

    def __repr__(self) -> str:
        driver_info = (
            self.assigned_driver.driver_id
            if self.assigned_driver else "None"
        )
        return (
            f"RideRequest({self.request_id} | "
            f"pickup={self.pickup} | "
            f"destination={self.destination} | "
            f"status={self.status} | "
            f"driver={driver_info})"
        )


# ── Demo ──────────────────────────────────────────────
if __name__ == "__main__":

    from driver import Driver

    rng = np.random.default_rng()

    # Create some requests
    requests = [
        RideRequest(1, pickup=(1, 2), destination=(4, 4)),
        RideRequest(2, pickup=(0, 3), destination=(3, 1)),
        RideRequest(3, pickup=(2, 0), destination=(4, 2)),
    ]

    print("── Ride Requests ──")
    for r in requests:
        print(r)

    # Create a driver and assign to first request
    driver = Driver(driver_id=1, position=(0, 0), rng=rng)
    print(f"\n-- Assigning {driver.driver_id} to {requests[0].request_id} --")
    requests[0].assign(driver)
    print(requests[0])
    print(driver)

    # Complete the ride
    print(f"\n-- Completing {requests[0].request_id} --")
    requests[0].complete()
    print(requests[0])
    print(driver)
>>>>>>> ee54ac11b6f7b578caf02c80209c3ed8d4ce5561
