import random

#TO-DO
#handleBlackJacks

cardNames = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
chipCount = 0
bet = 0
playing = True
blackJack = False
#creates a card with a name, suit and value
class Card:
    def __init__(self, suit, cardName):
        self.suit = suit
        self.cardName = cardName
    def __str__(self):
        return self.cardName + ' of ' + self.suit + ' (' + str(values[self.cardName]) + ')'

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for cardName in cardNames:
                self.deck.append(Card(suit, cardName))

    def __str__(self):
        display = ''
        for card in self.deck:
            display += '\n' + card.__str__()
        return display

    def shuffle(self):
        random.shuffle(self.deck)

    #returns a single card
    def deal(self):
        dealCard = self.deck.pop()
        return dealCard


class Hand:
    def __init__(self):
        self.cards = []
        self.handCount = 0
        self.aces = 0

    def addCard(self, card):
        self.cards.append(card)
        self.handCount += values[card.cardName]
        if card.cardName == 'Ace':
            self.aces += 1
        

    def handleAces(self):
        while self.aces and self.handCount > 21:
            self.handCount -= 10
            self.aces -= 1

class Chips:
    def __init__(self):
        self.chipCount = chipCount
        self.bet = bet

    def setChipCount(self):
        self.chipCount = int(input("Enter Buy In: "))
    
    def winHand(self):
        self.chipCount += self.bet
    
    def loseHand(self):
        self.chipCount -= self.bet

def placeBet(chips):
    while True:
        try:
            chips.bet = int(input("Place your bet: "))
        except ValueError:
            print("Your bet must be an integer value less than or equal to your total chips")
        else:
            if chips.bet > chips.chipCount:
                print("Uh Oh! Your bet must be less than or equal to ", chips.chipCount)
            else:
                break

def checkBlackJack(hand, chips):
    if hand.handCount == 21:
        print("BLACKJACK!!!")
        chips.chipCount += (1.5 * chips.bet)
        blackJack = True

def hit(deck, hand):
    hand.addCard(deck.deal())
    hand.handleAces()

def hitOrStay(deck, hand):
    action = int(input("Enter 1 to hit or 0 to stay: "))
    global playing
    try:
        if action == 1:
            hit(deck, playerHand)
        elif action == 0:
            print("Player Stands\n")
            playing = False
    except ValueError:
        print("Invalid input")


#helper functions to handle the outcome of cards
def playerLoss(chips):
    chips.chipCount -= chips.bet
    print("Loser!")

def playerBust(chips):
    chips.chipCount -= chips.bet
    print("You Busted!")

def playerWin(chips):
    chips.chipCount += chips.bet
    print("You Win!")

#functions to display the current hand of cards
def showPlayer(dealerHand, playerHand):
    print("Dealer is showing a(n): ")
    print(dealerHand.cards[1])
    print("Your cards: ")
    for card in playerHand.cards:
        print(card)

def showDealer(dealerHand, playerHand):
    print("Dealer has: ", dealerHand.handCount)
    for card in dealerHand.cards:
        print(card)
    print("You have: ", playerHand.handCount)
    for card in playerHand.cards:
        print(card)

print("***** Welcome to Garrett's Casino *****")
playerChips = Chips()
playerChips.setChipCount()
while True:
    #reset game and shuffle deck
    deck = Deck()
    deck.shuffle()
    playerHand = Hand()
    dealerHand = Hand()
    
    #take player bet
    placeBet(playerChips)

    #deal inital 4 cards
    playerHand.addCard(deck.deal())
    dealerHand.addCard(deck.deal())
    playerHand.addCard(deck.deal())
    dealerHand.addCard(deck.deal())

    checkBlackJack(playerHand, playerChips)
    if not blackJack:
        while playing:
            showPlayer(dealerHand, playerHand)
            hitOrStay(deck, playerHand)
            if playerHand.handCount > 21:
                showPlayer(dealerHand, playerHand)
                playerBust(playerChips)
                break

        if playerHand.handCount <= 21:
            while dealerHand.handCount < 17:
                hit(deck, dealerHand)
            showDealer(dealerHand, playerHand)

        if dealerHand.handCount > 21:
            print("Dealer Busted")
            playerWin(playerChips)
        elif dealerHand.handCount > playerHand.handCount:
            playerLoss(playerChips)
        elif dealerHand.handCount < playerHand.handCount and playerHand.handCount <= 21:
            playerWin(playerChips)
        else:
            print("Push")

    #show current chip count after hand
    count = playerChips.chipCount
    print("Your chip count: ", count)

    playAgain = int(input("Enter 1 to play again, enter 0 to quit: "))

    if playAgain == 1:
        playing = True
    else:
        print("Goodbye :(")
        break