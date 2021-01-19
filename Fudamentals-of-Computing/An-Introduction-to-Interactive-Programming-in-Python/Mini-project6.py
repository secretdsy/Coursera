# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
score = 0
deal_flag = False
hit_flag = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
    
    def draw_back(self, canvas, pos):
        card_loc = (CARD_CENTER[0], CARD_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []
    
    """
    def __str__(self):
        result = ""
        for i in range(len(self.hand)):
            result += (str(self.hand[i]) + " ")
        return "Hand contains " + result
    """
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        sum_value = 0
        ten_cnt = 0
        for i in range(len(self.hand)):
            if str(self.hand[i])[-1:] == "A" and sum_value < 10:
                sum_value += 11
                ten_cnt += 1
            else:
                sum_value += VALUES[str(self.hand[i])[-1:]]
                if sum_value > 21 and ten_cnt > 0:
                    sum_value -= 10
                    ten_cnt -= 1
        return sum_value

# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck.append(SUITS[i]+RANKS[j])
        return self.deck

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        self.pop_card = self.deck.pop()
        self.deal = Card(self.pop_card[:1], self.pop_card[-1:])
        return self.deal
    """
    def __str__(self):
        result = ""
        for i in range(len(self.deck)):
            result += (str(self.deck[i]) + " ")
        return "Deck contains " + result
    """

#define event handlers for buttons
def deal():
    global outcome, in_play
    global player, dealer, deck, player_list, dealer_list
    global score, hit_flag
    if in_play == True and hit_flag == True:
        score -= 1
    
    player_list = []
    dealer_list = []
    player = Hand()
    dealer = Hand()    
    deck = Deck()
    deck.shuffle()

    for i in range(2):
        tmp = deck.deal_card()
        player.add_card(tmp)
        player_list.append(str(tmp))
    for i in range(2):
        tmp = deck.deal_card()
        dealer.add_card(tmp)
        dealer_list.append(str(tmp))
        
    in_play = True
    hit_plag = False

def hit():
    global player, player_list
    global score, in_play, hit_flag
    hit_flag = True
    tmp = deck.deal_card()
    player.add_card(tmp)
    player_list.append(str(tmp))
    
    if player.get_value() > 21:
        score -= 1
        in_play = False

def stand():
    global player, dealer, in_play
    global score
    while(dealer.get_value() < 17 and dealer.get_value() < player.get_value()):
        tmp = deck.deal_card()
        dealer.add_card(tmp)
        dealer_list.append(str(tmp))
        
    if dealer.get_value() > 21:
        score += 1
    elif dealer.get_value() >= player.get_value():
        in_play = False
        score -= 1
    else:
        in_play = False
        score += 1
        
    in_play = False

# draw handler    
def draw(canvas):
    global player_list, dealer_list
    global score, in_play, hit_flag, deal_flag
    canvas.draw_text("Blackjack", (0, 50), 50, "Blue")
    canvas.draw_text("score : " + str(score), (400, 50), 30, "Black")
    canvas.draw_text("Dealer", (0, 170), 30, "Black")
    canvas.draw_text("Player", (0, 470), 30, "Black")
    
    if dealer.get_value() > 21:
        canvas.draw_text("Dealer bust, You win.", (200, 170), 30, "Black")
    elif in_play == False and (dealer.get_value() >= player.get_value() or player.get_value() > 21):
        canvas.draw_text("You lose.", (200, 170), 30, "Black")
        canvas.draw_text("New deal?", (200, 470), 30, "Black")
    elif hit_flag == True and deal_flag == True:
        canvas.draw_text("You lose.", (200, 170), 30, "Black")
        canvas.draw_text("New deal?", (200, 470), 30, "Black")
        hit_flag = False
        deal_flag = False
    elif in_play == False and dealer.get_value() < player.get_value():
        canvas.draw_text("You win.", (200, 170), 30, "Black")
    elif in_play == True:
        canvas.draw_text("Hit or stand?", (200, 470), 30, "Black")
    
    for i in range(len(player_list)):
        card = Card(player_list[i][:1], player_list[i][-1:])
        card.draw(canvas, [0 + i*100, 500])
    for i in range(len(dealer_list)):
        card = Card(dealer_list[i][:1], dealer_list[i][-1:])
        if in_play == True:
            if i == 0:
                card.draw_back(canvas, [0, 200])
            else:
                card.draw(canvas, [0 + i*100, 200])
        else:
            card.draw(canvas, [0 + i*100, 200])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric