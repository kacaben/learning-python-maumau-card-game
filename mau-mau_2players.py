# Mau-mau - Czech version (8 is not a special card here)
# 2 players share the screen - they have to press enter before their "hand" is revealed
# the --help and --resume clears the screen, shows Rules, clears the screen again, and reprints the game screen
# author: Katerina Benova

from random import shuffle
import os
from colorama import init
from termcolor import cprint

init()


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


# create a deck, get faceUp card and deal two hands
def createDeck():
    deck = []
    faceUpCard = ""
    faceValues = ['A', 'J', 'Q', 'K']
    suites = ["C", "D", "H", "S"]
    specials = ["J", "A", "7"]

    for i in range(4):
        for card in range(7, 11):
            deck.append(suites[i] + str(card))

        for card in faceValues:
            deck.append(suites[i] + card)

    shuffle(deck)
    for card in deck:
        cardEnd = card[-1]
        if cardEnd not in specials:
            deck.remove(card)
            faceUpCard = card
            break

    player1Hand = deck[0:5]
    player2Hand = deck[5:10]
    deck = deck[10:]

    return faceUpCard, deck, player1Hand, player2Hand


class Player:
    def __init__(self, name, hand, card=""):
        self.name = name
        self.hand = hand
        self.card = card

    def discard(self, card):
        self.card = card
        discarded.append(self.hand.pop(self.hand.index(self.card)))

    def draw(self):
        for i in range(drawCount):
            self.hand.append(cardDeck.pop(0))


# check if played card can be accepted:
# - if freshSeven true, only 7 can be played
# - fits the face-up card (suite or value)
# - Jack can be always played (unless freshSeven)

def checkCard(faceUpCard, playCard):
    suite = faceUpCard[0]
    value = faceUpCard[-1]
    playCard = playCard
    if freshSeven and playCard[-1] == "7":
        return True
    if freshSeven and playCard[-1] != "7":
        return False
    elif playCard[-1] == "J":
        return True
    elif playCard.startswith(suite) or playCard.endswith(value):
        return True
    else:
        return False


def invalidChoice(card):
    screen_clear()
    cprint(card + " is not a valid choice. Try again.", "red")

# if Jack is played, the player is prompted to input new suite
def jack():
    suites = ["C", "D", "H", "S"]
    while True:
        newsuite = input("Your card is Jack and you can change the suite. "
                         "Please select [C]lubs, [D]iamonds, [H]earts or [S]pades: ").upper()
        if newsuite in suites:
            return newsuite + "J"
        elif newsuite == "--HELP":
            rules(2)
            continue
        else:
            continue

# if player types --help in any part of the game, the screen is cleared and the rules are printed.
# After '--resume', the rules are cleared and the game progress is resumed / reprinted on the screen
def rules(stage=0):
    screen_clear()
    cprint("The rules of Mau-Mau (the Czech version)\n", "green")
    print(
        "The game is played with a 32-card German pack.\n"
        "The aim is to be first to get rid of all of one's cards.\n\n"
        "The players are each dealt a hand of 5 cards. The rest are placed face down as the stock.\n"
        "At the beginning of the game the topmost card is revealed and placed face up on the table. Then the\n"
        "players take turns to play their cards.\n"
        "A card can only be played if it corresponds to the suit or value of the face-up card - e.g. if it is\n"
        "the 10 of spades, only another spade or another 10 can be played (but see below for Jacks).\n"
        "If a player is not able to do this, they draw one card from the stack and passes on their next turn.\n"
        "When the drawing stack is empty, the playing stack (except for the topmost card) is shuffled and\n"
        "turned over to serve as new drawing stack.\n\n"
        "The 7, Jack and Ace of all suits are significant cards:\n"
        "- If a 7 is played, the next player has to draw two cards or play another 7, in which case the other\n"
        "  player must take 4 cards from the pack, unless they too have a 7,then 6, then 8.\n"
        "- A Jack of any suit is the equivalent of a Joker and can be played on any card.The player who plays\n"
        "  it then chooses a card suit. The next player then plays as if the Jack was of the chosen suit.\n"
        "- If an Ace is played, one other card must be played with it. If the player does not have another \n"
        "  card, or cannot follow in suit or number, then the player must take a card from the pack.\n"
        "  If your final card is an Ace, you cannot win on that turn.\n\n"
        "When a player has only one card left, they must say 'Mau'.\n")

    cprint("Type '--resume' to resume the game", "green")
    while True:
        txt =input()

        if txt == "--resume":
            screen_clear()
            if stage == 1:
                print("It's your turn,", player.name, ". Press Enter when ready.")
            if stage == 2:
                print("It's your turn,", player.name, ". Press Enter when ready.\n")
                print("Face-up card:", faceUpCard)
                print("Your hand:", *player.hand)
            break
        else:
            cprint("Please type '--resume' to resume the game","red")
            continue


# set game
faceUpCard, cardDeck, player1Hand, player2Hand = createDeck()

# set the 1st screen, get players names
player1Name = ""  # in case the --help is called by the second player

while True:
    cprint("Welcome to Mau Mau card game for two players","red")
    cprint("Type '--help' to see the rules and '--resume' to resume the game", "green")
    # create players
    if player1Name:
        print("Player 1, enter your name:", player1Name)
    else:
        player1Name = input("Player 1, enter your name: ").upper()
        player1 = Player(player1Name, player1Hand)
        if player1Name == "--HELP":
            rules()
            player1Name = ""
            continue
    player2Name = input("Player 2, enter your name: ").upper()
    player2 = Player(player2Name, player2Hand)
    if player2Name == "--HELP":
        rules()
        continue
    else:
        break


# pre-set game variables
game = True
discarded = []
freshAce = False
freshSeven = False
drawCount = 1
sevenCount = 0
player = player1
playerChange = True
lastCard = False


while game:
    try:
        # this loop can be executed several times in one player's turn before switching to the other player
        if playerChange:
            print("It's your turn,", player.name, ". Press Enter when ready.")
            txt = input()
            if txt == "--help":
                rules()
                continue

        playerChange = False

        if lastCard:
            cprint("Mau! Your opponent has the last card!\n", "red")

        print("Face-up card:", faceUpCard)
        print("Your hand:", *player.hand)

        if freshAce:
            card = input("After Ace you have to play another card or [D]raw a new card: ").upper()
        elif not cardDeck and not discarded:
            card = input("Play a card: ").upper()
        else:
            card = input("Play a card or choose to [D]raw a new card: ").upper()

        if card == "--HELP":
            rules(1)
            continue
        elif card == "D":
            player.draw()
            drawCount = 1
            sevenCount, freshSeven = 0, False
            # restock the cardDeck from 'discarded' pile
            if not cardDeck and discarded:
                cardDeck = discarded[:-1]
                shuffle(cardDeck)
                discarded.clear()
                discarded.append(faceUpCard)

        elif card in player.hand:
            if not checkCard(faceUpCard, card):
                invalidChoice(card)
                continue

            player.discard(card)
            faceUpCard = discarded[-1]

            if card[-1] == "J":
                faceUpCard = jack()
            elif card[-1] == "A":
                freshAce = True
                player.discard(card)
                faceUpCard = discarded[-1]
                continue
            elif card[-1] == "7":
                freshSeven = True
                sevenCount += 1
                drawCount = sevenCount * 2

            freshAce = False

        else:
            invalidChoice(card)
            continue

        if not player.hand:
            cprint("\n" + player.name + " is the Winner! Congratulations!", "green")
            input()
            game = False
        if len(player.hand) == 1:
            lastCard = True
        else:
            lastCard = False

        screen_clear()
        playerChange = True
        if player == player1:
            player = player2
        else:
            player = player1

    except Exception:
        pass
