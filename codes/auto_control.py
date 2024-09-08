import math


class AutoControl:
    def __init__(self, rover):
        self.rover = rover
        self.target_lat = None
        self.target_lon = None
        self.step_size = 10  # Movement step size

    def set_target(self, lat, lon):
        self.target_lat = lat
        self.target_lon = lon

    def navigate_to_target(self):
        if self.target_lat is None or self.target_lon is None:
            return  # No target set

        rover_lat, rover_lon = self.rover.get_lat_lon()
        delta_lat = self.target_lat - rover_lat
        delta_lon = self.target_lon - rover_lon
        distance = math.sqrt(delta_lat ** 2 + delta_lon ** 2)

        if distance < self.step_size:
            # Close enough to target, stop moving
            self.rover.stop()
        else:
            # Move towards target
            angle = math.atan2(delta_lon, delta_lat)  # Assuming lat/lon as coordinates
            self.rover.move_forward()
            self.rover.adjust_heading(angle)

    def update(self):
        self.navigate_to_target()

    def stop_auto_navigation(self):
        # Stop any ongoing auto navigation and reset state
        self.is_navigating = False
        self.target_x = None
        self.target_y = None
        print("Auto navigation stopped.")
