class ManualControl:
    def __init__(self, rover):
        self.rover = rover
        self.moving_forward = False
        self.moving_backward = False
        self.turning_left = False
        self.turning_right = False

    def move_forward(self):
        self.moving_forward = True

    def move_backward(self):
        self.moving_backward = True

    def turn_left(self):
        self.turning_left = True

    def turn_right(self):
        self.turning_right = True

    def stop(self):
        self.moving_forward = False
        self.moving_backward = False
        self.turning_left = False
        self.turning_right = False

    def update(self):
        if self.moving_forward:
            self.rover.move_forward()
        if self.moving_backward:
            self.rover.move_backward()
        if self.turning_left:
            self.rover.turn_left()
        if self.turning_right:
            self.rover.turn_right()
