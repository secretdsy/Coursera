# implementation of card game - Memory
import simplegui
import random

num_list = []
clicked_list = []
ans_list = []
num_flag = []
clicked_idx = []
turns = 0
cnt = 1

# helper function to initialize globals
def new_game():
    global num_list, num_flag, clicked_idx, clicked_list
    global turns, cnt
    num_list = [n for n in range(8) for x in range(2)]
    random.shuffle(num_list)
    num_flag = [False for n in range(16)]
    clicked_idx = []
    clicked_list = []
    cnt = 1
    turns = 0
    label.set_text("Turns = " + str(turns))
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global clicked_list, num_flag, clicked_idx
    global turns, cnt
    clicked = pos[0] // 50
    if num_flag[clicked] == False:
        if cnt == 1:
            turns += 1
            label.set_text("Turns = " + str(turns))
            if len(clicked_idx) > 1:
                num_flag[clicked_idx[0]] = False
                num_flag[clicked_idx[1]] = False
                clicked_idx = []
                clicked_list = []
            cnt = 2
            clicked_list.append(num_list[clicked])
            clicked_idx.append(clicked)
            num_flag[clicked] = True
        else:
            cnt = 1
            clicked_list.append(num_list[clicked])
            clicked_idx.append(clicked)
            num_flag[clicked] = True
            if clicked_list[0] == clicked_list[1]:
                clicked_idx = []
                clicked_list = []

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global num_list, num_flag
    for i in range(len(num_list)):
        if num_flag[i] == True:
            canvas.draw_text(str(num_list[i]), [50 * i + 10, 75], 60, 'White')
    for i in range(len(num_list)):
        if num_flag[i] == False:
            canvas.draw_polygon([[50 * i, 0], [50 * (i+1), 0], [50 * (i+1), 100], [50 * i, 100]], 4, 'Blue', 'White')            

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric