import turtle

class FeuTricolore:
    def __init__(self, screen, x, y):
        self.state = "RED"
        self.t = turtle.RawTurtle(screen)
        self.t.hideturtle()
        self.t.speed(0)
        self.x = x
        self.y = y

    def dessiner(self):
        self.t.clear()
        self.t.penup()
        self.t.goto(self.x - 12, self.y - 35)
        self.t.setheading(0)

        self.t.pendown()
        self.t.color("black", "#111827")
        self.t.begin_fill()
        for _ in range(2):
            self.t.forward(24)
            self.t.left(90)
            self.t.forward(70)
            self.t.left(90)
        self.t.end_fill()
        self.dessiner_lumieres(self.y + 25, "#ff0000" if self.state == "RED" else "#200")
        self.dessiner_lumieres(self.y + 0, "#ffaa00" if self.state == "ORANGE" else "#210")
        self.dessiner_lumieres(self.y - 25, "#00ff00" if self.state == "GREEN" else "#020")

    def dessiner_lumieres(self, y_pos, color):
        self.t.penup()

        self.t.goto(self.x, y_pos)

        self.t.dot(18, color)