from turtle import Turtle, Screen

win = Screen()
sam = Turtle()
win.bgcolor('black')
win.setup(width=1000 , height= 1000)
sam.shape('turtle')
sam.speed('fastest')
sam.color('red')
sam.fillcolor('yellow')

def draw_circles():
    sam.penup()
    sam.goto(-300,-300)
    sam.pendown()
    for _ in range(10):
        sam.circle(50)
        sam.left(360 / 10)

def draw_squares():
    sam.penup()
    sam.goto(0,0)
    sam.pendown()
    for _ in range(10):
        for _ in range(4):
            sam.forward(90)
            sam.left(90)
        sam.left(360 / 10)

def draw_triangles():
    sam.penup()
    sam.goto(300,300)
    sam.pendown()
    for _ in range(10):
        for _ in range(3):
            sam.forward(100)
            sam.left(120)
        sam.left(360 / 10)

draw_circles()
draw_squares()
draw_triangles()

win.exitonclick()
