from City import City

city = City(rows=5, cols=5)

# Display grid
city.display()

# Display all drivers
city.display_drivers()

# Display all ride requests
city.display_requests()

# Display edge weights
city.display_weights()

# Test manhattan distance
print("\n── Manhattan Distances ──")
for driver in city.drivers:
    for req in city.requests:
        dist = city.manhattan_distance(driver.position, req.pickup)
        print(f"  {driver.driver_id} -> {req.request_id} : {dist}")