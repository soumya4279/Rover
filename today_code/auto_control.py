import math


class AutoControl:
    def __init__(self, board):
        self.board = board
        self.target_lat = None
        self.target_lon = None

    def set_target(self, target_lat, target_lon):
        self.target_lat = target_lat
        self.target_lon = target_lon
        self.navigate_to_target()

    def navigate_to_target(self):
        # Ensure the rover is continuously navigating to the target
        if self.target_lat is not None and self.target_lon is not None:
            self.update()

    def update(self):
        if self.target_lat is None or self.target_lon is None:
            return False

        # Calculate the distance to the target
        lat_diff = self.target_lat - self.board.position_x
        lon_diff = self.target_lon - self.board.position_y
        distance = math.sqrt(lat_diff ** 2 + lon_diff ** 2)

        # Define a small threshold to consider as "reached"
        threshold = 0.1

        if distance < threshold:
            # Target reached
            self.board.position_x = self.target_lat
            self.board.position_y = self.target_lon
            self.board.update_rover_position()  # Update position
            return True  # Target reached

        # Calculate the angle to the target
        angle_to_target = math.atan2(lon_diff, lat_diff)

        # Adjust heading to face the target
        self.board.adjust_heading(angle_to_target)

        # Move forward by a small step
        move_distance = min(distance, 1)  # Move by 1 unit or the remaining distance
        self.board.position_x += move_distance * math.cos(angle_to_target)
        self.board.position_y += move_distance * math.sin(angle_to_target)
        self.board.update_rover_position()

        return False  # Continue moving

    def stop_auto_navigation(self):
        self.target_lat = None
        self.target_lon = None
