import simplegui
import random
import math

secret_num = 0
count = 0
num_range = 0
def new_game():
    global secret_num
    range100()
    
def range100():
    global count
    global secret_num
    global num_range
    num_range = 100
    count = int(math.ceil(math.log(100, 2)))
    secret_num = random.randrange(0, 100)
    print('New game. Range is from 0 to 100')
    print('Number of remaning guesses is ' + str(count))
    print('')

def range1000():
    global count
    global secret_num
    global num_range
    num_range = 1000
    count = int(math.ceil(math.log(1000, 2)))
    secret_num = random.randrange(0, 1000)
    print('New game. Range is from 0 to 1000')
    print('Number of remaning guesses is ' + str(count))
    print('')
    
def input_guess(guess):
    global count
    count -= 1
    if int(guess) > num_range or int(guess) < 0:
        print('Guess was ' + guess)
        print('Number of remaning guesses is ' + str(count))
        print('Out of guesses!')
        print('')
    elif secret_num == int(guess):
        print('Guess was ' + guess)
        print('Number of remaning guesses is ' + str(count))
        print('Correct!')
        print('')
    elif count == 0 and secret_num != int(guess):
        print('Guess was ' + guess)
        print('Number of remaning guesses is ' + str(count))
        print('You ran out of guesses.  The number was ' + str(secret_num))
        print('')
    elif secret_num > int(guess):
        print('Guess was ' + guess)
        print('Number of remaning guesses is ' + str(count))
        print('Higher')
        print('')
    else:
        print('Guess was ' + guess)
        print('Number of remaning guesses is ' + str(count))
        print('Lower')
        print('')
    
    if count == 0:
        if num_range == 100:
            range100()
        elif num_range == 1000:
            range1000()
        
f = simplegui.create_frame('Guess the number', 200, 200)

f.add_button('Range is [0, 100)', range100, 200)
f.add_button('Range is [0, 1000)', range1000, 200)
f.add_input('Enter a guess', input_guess, 200)

new_game()

