from DeckOfCards import *

USER_SCORE = 0
DEALER_SCORE = 0
USER_HAND = []
DEALER_HAND = []
GAME_RUNNING = True
DECK = DeckOfCards()

def show_and_shuffle():
    print("Deck before shuffling:")
    print(DECK)
    DECK.shuffle_deck()
    print("Deck after shuffling:")
    print(DECK)

def user_initial_hand():
    global USER_HAND
    USER_HAND.append(DECK.get_card())
    USER_HAND.append(DECK.get_card())
    for card in USER_HAND:
        print(card)
        add_score(card) 

def add_score(card, dealer=False):
    global USER_SCORE, DEALER_SCORE

    if dealer:
        if card.face == "Ace":
            if DEALER_SCORE + 11 <= 21:
                DEALER_SCORE += 11
            else:
                DEALER_SCORE += 1
        else:
            DEALER_SCORE += card.val
    else:
        if card.face == "Ace":
            if USER_SCORE + 11 <= 21:
                USER_SCORE += 11
            else:
                USER_SCORE += 1
        else:
            USER_SCORE += card.val

def user_hit():
    global USER_HAND, GAME_RUNNING
    card = DECK.get_card()
    USER_HAND.append(card)
    print(f"Card drawn: {card}") #TODO
    add_score(card)
    print_score()

    if USER_SCORE > 21:
        print('You busted!')
        GAME_RUNNING = False

def print_score(dealer=False):
    if dealer:
        print(f"Dealer's total score is: {DEALER_SCORE}")
    else:
        print(f"Your total score is: {USER_SCORE}")

def dealer_initial_hand():
    global DEALER_HAND
    for i in range(2):
        card = DECK.get_card()
        DEALER_HAND.append(card)
        add_score(card, dealer=True)
        print(f'Dealer card number {i+1} is: {card}')

def dealer_hit():
    global GAME_RUNNING
    while DEALER_SCORE < 17:  # Dealer hits until reaching 17 or more
        card = DECK.get_card()
        DEALER_HAND.append(card)
        add_score(card, dealer=True)
        print(f'Dealer card number {len(DEALER_HAND)} is: {card}')

    print_score(dealer=True)

    # Determine game outcome after dealer finishes
    if DEALER_SCORE > 21:
        print("Dealer busted, you win!")
    elif DEALER_SCORE > USER_SCORE:
        print("Dealer score is higher, you lose!")
    elif DEALER_SCORE < USER_SCORE:
        print("Your score is higher, you win!")
    else:
        print("It's a tie!")
    
    GAME_RUNNING = False  # End the game after the dealer finishes

def ask_user():
    global GAME_RUNNING
    valid = False
    while not valid and GAME_RUNNING:
        hit = input("Would you like to hit? (y/n): ").lower()

        if hit == 'y':
            user_hit()
            valid = True
        elif hit == 'n':
            dealer_initial_hand()
            dealer_hit()
            valid = True
        else:
            print("Please provide a valid input (y/n)")

def reset_game():
    global USER_SCORE, DEALER_SCORE, USER_HAND, DEALER_HAND, GAME_RUNNING
    USER_SCORE = 0
    DEALER_SCORE = 0
    USER_HAND = []
    DEALER_HAND = []
    GAME_RUNNING = True

def game_loop():
    show_and_shuffle()
    user_initial_hand()
    print_score()

    while GAME_RUNNING:
        ask_user()

def main():
    game_loop()
    while True:
        play_again = input("Would you like to play again? (y/n): ").lower()
        if play_again == 'y':
            reset_game()
            game_loop()
        elif play_again == 'n':
            print("Thanks, goodbye!")
            break
        else:
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
