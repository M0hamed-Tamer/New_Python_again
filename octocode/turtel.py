from turtle import Turtle, Screen
import random
import time
win = Screen()

sam = Turtle()

sam.speed('fastest')
win.bgcolor('black')
sam.color('white')
for _ in range(20):
    sam.left(50)
    sam.circle(100)

win.exitonclick()
