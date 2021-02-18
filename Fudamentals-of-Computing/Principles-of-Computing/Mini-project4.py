"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(1000)


def comb(outcomes, leng):
    """
    Combinations of outcomes
    """
    for num in range(len(outcomes)):
        if leng == 1:
            yield [outcomes[num]]
        else:
            for next in comb(outcomes[num + 1:], leng - 1):
                yield [outcomes[num]] + next

                
def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    hand_set = set(hand)
    max_score = 0
    for num in hand_set:
        tmp = hand.count(num) * num
        max_score = max(max_score, tmp)
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    tmp = gen_all_sequences(tuple([i for i in range(1, num_die_sides + 1)]), num_free_dice)
    exv_cand_list = []
    for num in list(tmp):
        exv_cand_list.append(score(held_dice + num))
    len_cand = len(exv_cand_list)
    return sum(exv_cand_list) / float(len_cand)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    hand = sorted(hand)
    hand_set = set([()])
    for dummy_i in range(0, len(hand) + 1):
        for dummy_j in comb(hand, dummy_i):
            hand_set.add(tuple(dummy_j))
    return hand_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    max_hand = tuple()
    max_exp = 0
    holds_set = gen_all_holds(hand)
    
    for dummy_i in holds_set:
        tmp_exp = expected_value(dummy_i, num_die_sides, len(hand)-len(dummy_i))
        if max_exp < tmp_exp:
            print("max")
            max_exp = tmp_exp
            max_hand = dummy_i
            print(max_exp, max_hand)
        else:
            print("tmp")
            print(tmp_exp, dummy_i)
    return (max_exp, max_hand)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print("Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score)

    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

#strategy((1,2,3,3,4),4)
