import turtle
import logging
import math

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class VirtualMotor:
    """Simulates a motor using the Turtle graphics module."""

    def __init__(self, forward_pin, backward_pin, turtle_obj, name="Motor"):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self.turtle_obj = turtle_obj
        self.name = name
        self.moving = False  # Flag to track the movement state

    def forward(self):
        """Simulate moving forward."""
        self.moving = True
        print(f"{self.name} moving forward")
        self._move_turtle_forward()

    def backward(self):
        """Simulate moving backward."""
        self.moving = True
        print(f"{self.name} moving backward")
        self._move_turtle_backward()

    def stop(self):
        """Simulate stopping."""
        self.moving = False
        print(f"{self.name} stopped")

    def _move_turtle_forward(self):
        """Move Turtle forward continuously until stopped."""
        if self.moving:
            try:
                self.turtle_obj.forward(10)
                self.center_view()  # Keep Turtle in the center of the view
                self.turtle_obj.screen.ontimer(self._move_turtle_forward, 50)
            except turtle.TurtleGraphicsError as e:
                logging.error(f"Error moving turtle forward: {e}")

    def _move_turtle_backward(self):
        """Move Turtle backward continuously until stopped."""
        if self.moving:
            try:
                self.turtle_obj.backward(10)
                self.center_view()  # Keep Turtle in the center of the view
                self.turtle_obj.screen.ontimer(self._move_turtle_backward, 50)
            except turtle.TurtleGraphicsError as e:
                logging.error(f"Error moving turtle backward: {e}")

    def center_view(self):
        """Center the screen view on the Turtle."""
        x, y = self.turtle_obj.position()
        self.turtle_obj.screen.setworldcoordinates(x - 200, y - 200, x + 200, y + 200)
        self.turtle_obj.screen.update()


class VirtualPiBoard:
    """Simulates a Raspberry Pi board using Turtle."""

    def __init__(self):
        # Initialize the Turtle screen
        self.screen = turtle.Screen()
        self.screen.title("Virtual Raspberry Pi Board Simulation")
        self.screen.bgcolor("white")

        # Initialize the Turtle object representing the rover
        self.rover = turtle.Turtle()
        self.rover.color("blue")
        self.rover.penup()  # Lift the pen to avoid drawing lines
        self.rover.speed(0)  # Highest speed for immediate response

        # Initialize simulated GPS coordinates
        self.latitude = 0.0
        self.longitude = 0.0
        self.update_coordinates()  # Initial coordinate display

        # Initialize motors with their respective Turtle control
        self.motor_right = VirtualMotor(forward_pin=17, backward_pin=18, turtle_obj=self.rover, name="Right Motor")
        self.motor_left = VirtualMotor(forward_pin=22, backward_pin=23, turtle_obj=self.rover, name="Left Motor")

        # Set initial mode to manual
        self.mode = "manual"  # Possible values: "manual", "auto"
        self.target_latitude = None
        self.target_longitude = None
        self.setup_ui()

    def setup_ui(self):
        """Set up UI and key bindings."""
        self.bind_keys()
        self.ask_for_mode()  # Ask user to choose mode

    def move_forward(self):
        """Move the rover forward."""
        if self.mode == "manual":
            self.motor_right.forward()
            self.motor_left.forward()
            self.update_coordinates()

    def move_backward(self):
        """Move the rover backward."""
        if self.mode == "manual":
            self.motor_right.backward()
            self.motor_left.backward()
            self.update_coordinates()

    def turn_left(self):
        """Simulate turning left."""
        if self.mode == "manual":
            print("Rover turning left")
            self.rover.left(15)
            self.update_coordinates()

    def turn_right(self):
        """Simulate turning right."""
        if self.mode == "manual":
            print("Rover turning right")
            self.rover.right(15)
            self.update_coordinates()

    def stop(self):
        """Stop the rover."""
        self.motor_right.stop()
        self.motor_left.stop()

    def update_coordinates(self):
        """Update and display the rover's simulated GPS coordinates."""
        self.latitude = self.rover.ycor() / 10.0  # Scale factor for simulation
        self.longitude = self.rover.xcor() / 10.0
        self.screen.title(
            f"Virtual Raspberry Pi Board Simulation - Lat: {self.latitude:.2f}, Lon: {self.longitude:.2f}")

    def bind_keys(self):
        """Bind arrow keys to rover movement functions and mode switch."""
        self.screen.listen()
        self.screen.onkeypress(self.move_forward, "Up")
        self.screen.onkeyrelease(self.stop, "Up")
        self.screen.onkeypress(self.move_backward, "Down")
        self.screen.onkeyrelease(self.stop, "Down")
        self.screen.onkeypress(self.turn_left, "Left")
        self.screen.onkeypress(self.turn_right, "Right")
        self.screen.onkeyrelease(self.stop, "space")
        self.screen.onkeypress(self.toggle_mode, "m")  # Bind 'm' key to toggle modes

    def toggle_mode(self):
        """Toggle between manual and automatic modes."""
        if self.mode == "manual":
            self.mode = "auto"
            print("Switched to automatic mode")
            self.ask_for_target_location()
        else:
            self.mode = "manual"
            print("Switched to manual mode")
            self.stop()  # Stop the rover when switching to manual mode

    def ask_for_mode(self):
        """Prompt the user to select the mode."""
        mode_input = self.screen.textinput("Mode Selection", "Enter mode (manual/auto): ")
        if mode_input:
            mode_input = mode_input.strip().lower()
            if mode_input == "auto":
                self.mode = "auto"
                self.ask_for_target_location()
            else:
                self.mode = "manual"

    def ask_for_target_location(self):
        """Prompt the user for target location in automatic mode."""
        if self.mode == "auto":
            try:
                lat_input = self.screen.textinput("Target Location", "Enter target latitude:")
                lon_input = self.screen.textinput("Target Location", "Enter target longitude:")
                if lat_input and lon_input:
                    self.target_latitude = float(lat_input)
                    self.target_longitude = float(lon_input)
                    print(f"Target set to Lat: {self.target_latitude}, Lon: {self.target_longitude}")
                    self.start_auto_mode()
                else:
                    print("Target location inputs cannot be empty.")
            except ValueError:
                print("Invalid input. Please enter numeric values for latitude and longitude.")

    def start_auto_mode(self):
        """Start automatic mode behavior."""
        if self.mode == "auto":
            print("Starting automatic mode")
            self.auto_move()  # Start automatic movement

    def auto_move(self):
        """Move the rover automatically towards the target."""
        try:
            if self.mode == "auto":
                distance = self.calculate_distance_to_target()
                print(f"Current Distance to Target: {distance:.2f}")  # Debug print
                if distance > 1.0:  # Adjust the threshold as needed
                    self.move_towards_target()
                    self.update_coordinates()
                    self.screen.update()  # Ensure the screen updates with the new position
                    self.screen.ontimer(self.auto_move, 500)  # Continue moving every 0.5 second
                else:
                    self.stop()  # Stop if the rover is close to the target
                    print("Reached the target location.")
                    self.ask_for_mode()  # Ask user to select mode after reaching the target
        except Exception as e:
            logging.error(f"Error in automatic mode: {e}")
            self.mode = "manual"  # Switch back to manual mode on error

    def move_towards_target(self):
        """Move the rover towards the target location."""
        try:
            target_x = self.target_longitude * 10
            target_y = self.target_latitude * 10
            angle_to_target = self.rover.towards(target_x, target_y)
            distance = self.calculate_distance_to_target()

            self.rover.setheading(angle_to_target)
            print(f"Moving towards angle: {angle_to_target}, Distance: {distance:.2f}")

            if distance > 1.0:  # Ensure movement while away from the target
                self.motor_right.forward()
                self.motor_left.forward()
            else:
                self.stop()  # Stop if very close to the target
        except Exception as e:
            logging.error(f"Error moving towards target: {e}")
            self.stop()  # Stop the rover on error
            self.ask_for_mode()

    def calculate_distance_to_target(self):
        """Calculate the distance to the target location."""
        dx = self.target_longitude * 10 - self.rover.xcor()
        dy = self.target_latitude * 10 - self.rover.ycor()
        return math.sqrt(dx ** 2 + dy ** 2)

    def cleanup(self):
        """Clean up the Turtle graphics."""
        self.screen.bye()