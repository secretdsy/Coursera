import random

def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    else:
        return 4


def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    else:
        return 'scissors'
    

def rpsls(player_choice):
    
    # print a blank line to separate consecutive games
    print('')
    # print out the message for the player's choice
    print('Player chooses ' + player_choice)
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print('Computer chooses ' + comp_choice)
    # compute difference of comp_number and player_number modulo five
    diff = comp_number - player_number
    # use if/elif/else to determine winner, print winner message
    if diff % 5 == 1 or diff % 5 == 2:
        print('Computer wins!')
    elif diff % 5 == 3 or diff % 5 == 4:
        print('Player wins!')
    else:
        print('Player and computer tie!')
        
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


