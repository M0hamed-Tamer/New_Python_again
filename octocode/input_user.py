from turtle import Turtle,Screen
sam = Turtle()
window = Screen()
window.title('Mohamed Tamer : Python ')
list_of_shapes =('square','triangle','circle',"مربع","مثلث","دائره")

def draw_spuare():
    for _ in range(4):
        sam.pensize(5)
        sam.color('blue')
        sam.shape('turtle')
        sam.forward(150)
        sam.left(90)

def draw_triangle():
    for _ in range(3):
        sam.pensize(10)
        sam.color('purple')
        sam.shape('circle')
        sam.forward(200)
        sam.left(120)


def draw_circle():
    sam.pensize(4)
    sam.color('black')
    sam.shape('square')
    sam.circle(150)

game = True
while game:
    user = window.textinput('لحظه من فضلك ','ماذا تريد ان ترسم--> مربع ,مثلث , دائره (En & ar)')
    if user in list_of_shapes:
        if user == 'square' or 'مربع':
            draw_spuare()

        elif user == 'triangle' or 'مثلث':
            draw_triangle()

        elif user == 'circle' or 'مربع':
            draw_circle()
    elif user == 'خروج' or 'exit':
        game=False
        window.clear()
        sam.color('black')
        sam.hideturtle()
        window.bgcolor('LightCyan1')
        sam.write('Press any key to exit',align='center',font=('arial',35,'normal'))
        sam.color('darkgray')
        sam.penup()
        sam.goto(0,-50)
        sam.pendown()
        sam.write('اضغط في اي مكان للخروج ',align='center',font=('arial',25,'normal'))


window.exitonclick()