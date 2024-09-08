import turtle
import math
from auto_control import AutoControl
from manual_control import ManualControl


class VirtualPiBoard:
    def __init__(self):
        self.motor = turtle.Turtle()
        self.motor.hideturtle()
        self.motor.penup()
        self.position_x = 0
        self.position_y = 0
        self.heading = 0  # Angle in radians
        self.rover = turtle.Turtle()
        self.rover.shape("turtle")  # Change shape here
        self.rover.color("blue")
        self.rover.penup()
        self.rover.speed(5)  # Increase speed (1 is fastest, 10 is slowest)
        self.auto_control = AutoControl(self)
        self.manual_control = ManualControl(self)
        self.control_mode = 'manual'  # Default to manual mode

    def move_forward(self):
        self.position_x += math.cos(self.heading) * 10
        self.position_y += math.sin(self.heading) * 10
        self.update_rover_position()

    def move_backward(self):
        self.position_x -= math.cos(self.heading) * 10
        self.position_y -= math.sin(self.heading) * 10
        self.update_rover_position()

    def turn_left(self):
        self.heading -= math.pi / 8  # Turn 22.5 degrees left
        self.update_rover_position()

    def turn_right(self):
        self.heading += math.pi / 8  # Turn 22.5 degrees right
        self.update_rover_position()

    def stop(self):
        # Not strictly needed since we're updating continuously
        pass

    def get_lat_lon(self):
        # For simplicity, assume x and y directly represent lat and lon
        return self.position_x, self.position_y

    def adjust_heading(self, angle):
        self.heading = angle
        self.update_rover_position()

    def update_rover_position(self):
        self.rover.setheading(math.degrees(self.heading))
        self.rover.goto(self.position_x, self.position_y)
        self.update_screen_title()

    def update_screen_title(self):
        lat, lon = self.get_lat_lon()
        turtle.title(f"Rover Simulation - Lat: {lat:.2f}, Lon: {lon:.2f}")

    def set_auto_mode(self):
        self.control_mode = 'auto'
        print("Switched to auto mode")
        self.prompt_target_location()

    def set_manual_mode(self):
        self.control_mode = 'manual'
        print("Switched to manual mode")

    def prompt_target_location(self):
        # Prompt the user to enter target latitude and longitude
        target_lat = turtle.numinput("Target Location", "Enter target latitude:", default=0)
        target_lon = turtle.numinput("Target Location", "Enter target longitude:", default=0)
        if target_lat is not None and target_lon is not None:
            self.auto_control.set_target(target_lat, target_lon)
        else:
            self.set_manual_mode()  # Return to manual mode if the user cancels input


def setup_key_bindings(board):
    turtle.listen()
    turtle.onkeypress(board.manual_control.move_forward, 'Up')
    turtle.onkeypress(board.manual_control.move_backward, 'Down')
    turtle.onkeypress(board.manual_control.turn_left, 'Left')
    turtle.onkeypress(board.manual_control.turn_right, 'Right')
    turtle.onkeyrelease(board.manual_control.stop, 'Up')
    turtle.onkeyrelease(board.manual_control.stop, 'Down')
    turtle.onkeyrelease(board.manual_control.stop, 'Left')
    turtle.onkeyrelease(board.manual_control.stop, 'Right')
    turtle.onkey(board.set_auto_mode, 'a')  # Switch to auto mode
    turtle.onkey(board.set_manual_mode, 'm')  # Switch to manual mode


def main():
    screen = turtle.Screen()
    screen.title("Rover Simulation - Lat: 0.00, Lon: 0.00")
    screen.bgcolor("white")

    board = VirtualPiBoard()  # Instantiate the virtual board

    setup_key_bindings(board)  # Set up keyboard controls for manual and auto mode switching

    def update():
        # Update based on the current control mode
        if board.control_mode == 'auto':
            board.auto_control.update()  # Update auto mode movement
        else:
            board.manual_control.update()  # Update manual mode controls
        screen.ontimer(update, 100)  # Schedule the next update

    update()  # Initial update call to start the loop
    turtle.mainloop()  # Start the turtle main loop


if __name__ == '__main__':
    main()
