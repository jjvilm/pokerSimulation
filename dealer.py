from random import choice, shuffle
from mechanics import analyze_gameplay, declare_winner

class Dealer():
    def __init__(self, deck, players):
        self.deck = deck
        self.community_cards = dict() # dict with values as sets
        self.community_cards_string = "" # Used for displaying the cards in order obtained
        self.pot = 0
        self.players = players

        self.init_card_dicts()


    def get_card(self) -> tuple:
        """ Returns a card from deck, and removes it from it"""
        # card = choice(self.deck.cards)
        try: 
            # suit = choice(list(self.deck.cards.keys()))
            # make sure the cards have not been exhausted
            suit = choice([ suit for suit,rank_set in self.deck.cards.items() if len(rank_set) != 0])
            rank = choice(list(self.deck.cards[suit]))
        except Exception as e:
            print(e, "\n","suit",  suit)
            print(e, "\n", "self.deck.cards",self.deck.cards)
            input()
        # remove card from deck
        card = (rank, suit)
        self.deck.remove_card(card)
        return card

    def deal_cards(self,):
        # give a random card to the players
        for player in self.players:
            # adds a card chosen at random from deck    
            rank,suit = self.get_card()

            # print(f"ln35:{player.hole_cards}")
            player.hole_cards[suit].add(rank)
            # print(f"ln37:{player.hole_cards}")

    def test_mechanics(self,players: object, player_cards: tuple, community_cards: tuple):
        copy_player_list = self.players.copy()
        # remove the players we're given the selected cards giving more random cards
        for i,player in enumerate(players):
            copy_player_list.remove(player)

            # instead of giving random cards the the passed player
            # give selected cards, and init community_cards as well
            # the rest of the players will get random cards.
            # remove card from deck
            for card in player_cards[i]:
                rank,suit = card
                player.hole_cards[suit].add(rank)
                self.deck.remove_card(card)

        # add community cards
        for card in community_cards:
            rank,suit = card
            self.community_cards[suit].add(rank)
            # remove from deck
            self.deck.remove_card(card)
            card = self.deck.format_card((rank,suit))
            self.community_cards_string += f"[{card}] "

        for player in copy_player_list:
            for _ in range(2):
                # adds a card chosen at random from deck    
                rank,suit = self.get_card()

                player.hole_cards[suit].add(rank)

    def get_community_card(self):
        rank,suit = self.get_card()
        self.community_cards[suit].add(rank)
        card = self.deck.format_card((rank,suit))
        self.community_cards_string += f"[{card}] "
        
    def init_card_dicts(self):
        suits = self.deck.cards.keys()
        # print(f"ln45:{suits}")
        # set up community cards as a dict with values as sets
        # self.community_cards = dict()
        for suit in suits:
                self.community_cards[suit] = set()

        # initialize players hole_cards dicitonary, sets each key(suit) as a set
        for player in self.players:
            for suit in suits:
                player.hole_cards[suit] = set()

            
    # deals all hole cards to players
    def pre_flop(self):
        print("pre-flop")
        for _ in range(2):
            self.deal_cards()

    def flop(self):
        print("flop")
        for _ in range(3):
            self.get_community_card()
        # print(f"Community cards: {self.community_cards}")
        self.display_cc()
    
    def turn(self):
        print("turn")
        self.get_community_card()
        # print(f"Community cards: {self.community_cards}")
        self.display_cc()

    def river(self):
        print("river")
        self.get_community_card()
        # print(f"Community cards: {self.community_cards}")
        self.display_cc()

    def showdown(self):
        def combine_dictionaries(dict1, dict2):
            # combines hole cards and community cards into a hand 
            combined_dict = {key: set(dict1.get(key, [])) | set(dict2.get(key, []))
                            for key in set(dict1) | set(dict2)}
            return combined_dict
        
        for player in self.players:
            player.hand = combine_dictionaries(self.community_cards, player.hole_cards)
            # gets hole cards as a list of tuples: [(8, '♦'), (8, '♥')]
            hole_cards = [(rank, suit) for suit, rank_set in player.hole_cards.items() for rank in rank_set]

            # print(f"ln76:{hole_cards}")
            # print(f"ln77:{player.hole_cards}")
            # card1 = hole_cards[0][0]
            # card2 = hole_cards[0][1]
            card1, card2 = hole_cards
            # make it display nicely
            card1 = self.deck.format_card(card1)
            card2 = self.deck.format_card(card2)
            # print(f"Community cards: {self.community_cards}")
            analyze_gameplay(player)
            print(f"{player} has: [{card1}] [{card2}]: {player.hand_rank}")
            # print(f"player.hand_rank: {player.hand_rank}")
        
        # declare_winner(self.players)
        # new game
        # for player in self.players:
        #     player.reset()
       


    def display_cc(self):
        # cards = ""
        # for suit,rank_set in self.community_cards.items():
        #     if len(rank_set) >= 1:
        #         for rank in rank_set:
        #             card = self.deck.format_card((rank,suit))
        #             cards += f"{card} "

        print(f"Community cards: {self.community_cards_string}")
        
        

