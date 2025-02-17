import turtle
import sys
import os
playerspeed = 20


# Set up Window Screen ------------------------
window = turtle.Screen()
window.title("Ping Pong Game By Fo2sh ")
window.setup(width = 800, height = 600)
window.tracer(0) # Don't Delay Photos cuz i want it to be fast as a video
window.bgcolor(.3,.3,.3)


#ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.shapesize(stretch_len= 1 ,stretch_wid=1)
ball.goto(x=0,y=0)
ball.penup()
ball_dx , ball_dy = 1 , -1
ball_speed = 0.4


#center line
CenterLine = turtle.Turtle()
CenterLine.speed(0)
CenterLine.shape("square")
CenterLine.color("White")
CenterLine.shapesize(stretch_len=.1, stretch_wid=25)
CenterLine.penup()
CenterLine.goto(x=0 , y=0)


# Right Player
player1 = turtle.Turtle()
player1.color("Blue")
player1.shape("square")
player1.shapesize(stretch_len=1 , stretch_wid= 5)
player1.penup()
player1.goto(x= 350 , y = 0)
player1_score = 0


# Left Player
player2 = turtle.Turtle()
player2.color("Red")
player2.shape("square")
player2.shapesize(stretch_len=1 , stretch_wid= 5)
player2.penup()
player2.goto(x= -350 , y = 0)
player2_score = 0


#Score Text
score = turtle.Turtle()
score.speed(0)
score.penup()
score.color("White")
score.goto(0,260)
score.write(f"Player1: 0   Player2: 0",align = "center" ,font = ("Courier", 14 , "normal"))
score.hideturtle()


#player1 Movement
def p1_move_up():
    player1.sety(player1.ycor() + playerspeed)

def p1_move_down():
    player1.sety(player1.ycor() - playerspeed)


#player2 Movement
def p2_move_up():
    player2.sety(player2.ycor() + playerspeed)

def p2_move_down():
    player2.sety(player2.ycor() - playerspeed)



#React With keyboard and move

window.listen()
window.onkeypress(p1_move_up, "Up")
window.onkeypress(p1_move_down, "Down")
window.onkeypress(p2_move_up, "w")
window.onkeypress(p2_move_down, "s")





while True:
    window.update()

    #ball Movement
    ball.setx(ball.xcor() + (ball_speed * ball_dx))
    ball.sety(ball.ycor() + (ball_speed * ball_dy))



    # Wall Touch
    if (ball.ycor() > 290):
        ball.sety(290)
        ball_dy *= -1

    if (ball.ycor() < -290):
        ball.sety(-290)
        ball_dy *= -1


    #score Board
    if (ball.xcor() > 390):
        ball.goto(0,0)
        score.clear()
        player2_score += 1
        ball_dx *= -1
        score.write(f"Player2: {player2_score}   Player1: {player1_score}",align = "center" ,font = ("Courier", 14 , "normal"))


    if (ball.xcor() < -390):
        ball.goto(0,0)
        score.clear()
        player1_score += 1
        ball_dx *= -1
        score.write(f"Player2: {player2_score}   Player1: {player1_score}",align = "center" ,font = ("Courier", 14 , "normal"))




    # Collision With player1
    if ball.xcor() < -340 and ball.xcor() > -350 and ball.ycor() > (player2.ycor() - 60) and ball.ycor() < (player2.ycor() + 60):
        ball.setx(-340)
        ball_dx *= -1



    # Collision With Player2
    if ball.xcor() > 340 and ball.xcor() < 350 and ball.ycor() > (player1.ycor() - 60) and ball.ycor() < (player1.ycor() + 60):
        ball.setx(340)
        ball_dx *= -1



    #Borders Of The Game
    if (player2.ycor() <= -250):
        player2.sety(-250)

    if (player2.ycor() >= 250):
        player2.sety(250)


    if (player1.ycor() <= -250):
        player1.sety(-250)

    if (player1.ycor() >= 250):
        player1.sety(250)





    





