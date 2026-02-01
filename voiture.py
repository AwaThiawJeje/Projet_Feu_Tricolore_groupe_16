import turtle
import random

class Voiture:
    def __init__(self, screen, direction, color):
        self.screen = screen
        self.direction = direction
        self.color = color

        self.base_speed = random.uniform(3, 4.5)
        self.speed = self.base_speed
        self.stopped = False

        self.t = turtle.RawTurtle(screen)
        self.t.hideturtle()
        self.t.penup()
        self.t.speed(0)

        # forme et positionement
        if direction in ["E", "W"]:
            self.t.shape("car_h")  # Utilise la forme horizontale
            y_pos = -40 if direction == "E" else 40
            x_pos = -650 if direction == "E" else 650
            self.t.goto(x_pos, y_pos)
            self.t.setheading(0 if direction == "E" else 180)
        else:
            self.t.shape("car_v")  # Utilise la forme verticale
            x_pos = 40 if direction == "N" else -40
            y_pos = -550 if direction == "N" else 550
            self.t.goto(x_pos, y_pos)
            self.t.setheading(90 if direction == "N" else 270)

        self.t.color(color)
        self.t.showturtle()

    def move(self):
        if not self.stopped:
            self.t.forward(self.speed)

    def is_off_screen(self):
        x, y = self.t.position()
        return abs(x) > 700 or abs(y) > 600