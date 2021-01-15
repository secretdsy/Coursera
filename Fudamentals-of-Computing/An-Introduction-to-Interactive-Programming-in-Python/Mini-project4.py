# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(2, 4) * (-1)**random.randrange(1,3),
            random.randrange(1, 3) * (-1)**random.randrange(1,3)]
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
paddle2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
paddle_inc = 5
score1 = 0
score2 = 0
direction = "right"

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == "right":
        ball_vel = [random.randrange(2, 4),
                    random.randrange(1, 3) * (-1)**random.randrange(1,3)]
    elif direction == "left":
        ball_vel = [-random.randrange(2, 4), 
                    random.randrange(1, 3) * (-1)**random.randrange(1,3)]
    

    # define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel
    paddle1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    paddle2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global PAD_WIDTH
    global direction
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        ball_vel[0] = -(ball_vel[0] * 1.1)
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        ball_vel[0] = -(ball_vel[0] * 1.1)
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # draw paddles
    if paddle1_pos >= HEIGHT / 2:
        paddle1_pos = min(paddle1_pos + paddle1_vel, HEIGHT - PAD_HEIGHT)
    else:
        paddle1_pos = max(paddle1_pos + paddle1_vel, 0)
    if paddle2_pos >= HEIGHT / 2:
        paddle2_pos = min(paddle2_pos + paddle2_vel, HEIGHT - PAD_HEIGHT)
    else:
        paddle2_pos = max(paddle2_pos + paddle2_vel, 0)
    
    canvas.draw_line([0, paddle1_pos], [0, paddle1_pos + PAD_HEIGHT], 14, "White")
    canvas.draw_line([WIDTH, paddle2_pos], [WIDTH, paddle2_pos + PAD_HEIGHT], 14, "White")
    
    # determine whether paddle and ball collide
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and (ball_pos[1] - paddle1_pos < 0 or ball_pos[1] - paddle1_pos > PAD_HEIGHT):
        score2 += 1
        direction = "right"
        new_game()
    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS) and (ball_pos[1] - paddle2_pos < 0 or ball_pos[1] - paddle2_pos > PAD_HEIGHT):
        score1 += 1
        direction = "left"
        new_game()
    
    # draw scores
    canvas.draw_text(str(score1) + ":" + str(score2), [270, 50], 40, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = - paddle_inc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle_inc
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = - paddle_inc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle_inc
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
def reset():
    global score1, score2
    score1 = 0
    score2 = 0
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 50)

# start frame
new_game()
frame.start()
