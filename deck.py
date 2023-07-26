import itertools

class Deck():
    def __init__(self):
        self.cards = self.create_deck()

    def reset_deck(self):
        self.cards = self.create_deck()
         

    def create_deck(self) -> dict:
        # ranks = [2, 3, 4, 5, 6, 7, 8 , 9 , 10, 'J', 'Q', 'K', 'A']
        ranks = [2, 3, 4, 5, 6, 7, 8 , 9 , 10, 11, 12, 13, 14]
        suits = ['♠', '♣', '♦', '♥']
        # suits = ['spades', 'clubs', 'diamonds', 'hearts']
        # better way to build deck is by having a dictionary of sets
        # key will be the suit types, and the sequence, will be the set
        deck = {}
        for suit in suits:
            deck[suit] = set(ranks)

        # 
        #deck = list(itertools.product(ranks, suits))
        """ {
            '♠': {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
            '♣': {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}, 
            '♦': {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}, 
            '♥': {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}} """
        return deck

    def remove_card(self,card: tuple):
        rank = card[0]
        suit = card[1]
        try:
            self.cards[suit].remove(rank)
        except:
            print(f"Duplicate Card {card} added")

    def format_card(self, card: tuple):
        """" Returns a beautified display of the card"""
        # print(f"ln39:{card}")
        rank = card[0]
        suit = card[1]
        letter_ranks = {11:'J',12:'Q',13:'K',14:'A'}
        # Adds the letters to the ranks after 10
        if rank in letter_ranks.keys():
            rank = letter_ranks[rank]


        formatted_card = f"{rank}{suit}"
        return formatted_card

    

if __name__ == "__main__":
    deck1 = Deck()
    deck = deck1.create_deck()

    # Print the deck
    for card in deck:
        print(card)
