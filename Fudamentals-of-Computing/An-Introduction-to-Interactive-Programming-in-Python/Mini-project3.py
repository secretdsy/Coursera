# template for "Stopwatch: The Game"
import simplegui
# define global variables
m = ''
s = ''
ms = ''
counter = 0
ans = 0
atmp = 0
flag = True
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global m
    global s
    global ms
    m = str(int(t) / 600)
    s = "00" + str((int(t) - int(m) * 600) / 10)
    ms = str(int(t) % 10)
    time = m + ":" + s[-2:] + "." + ms
    return time
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global flag
    flag = True
    timer.start()

def stop():
    global s
    global ms
    global ans
    global atmp
    global flag
    timer.stop()
    if int(s) != 0 and int(s) % 5 == 0 and ms == '0' and flag == True:
        ans += 1
        atmp += 1
        flag = False
    elif int(s) != 0 and flag == True:
        atmp += 1
        flag = False
        
    
def reset():
    global counter
    global ans
    global atmp
    global flag
    timer.stop()
    flag = True
    counter = 0
    ans = 0
    atmp = 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    counter += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(counter),[120, 180], 48, "White")
    canvas.draw_text(str(ans) + "/" + str(atmp),[300, 50], 48, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 400, 300)

# register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()

# Please remember to review the grading rubric
