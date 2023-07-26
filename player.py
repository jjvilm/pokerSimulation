class Player():
    def __init__(self, name, chips):
        self.name = name
        self.hole_cards =  dict() # dict with values as a set
        self.hand = dict() # composed of community_cards + hole_cards
        self.hand_rank = [] # hand rank: 1-10 highrank - royalflush
        self.sequenced_ranks = [] # if have straight ranks in here
        self.rank_pairs_in_hand = {} # key=name of function values are usually a list
        self.chips = chips
    

    def reset(self):
        self.hole_cards = dict()
        self.hand = dict()
        self.hand_rank = []
        self.sequenced_ranks = []
        self.rank_pairs_in_hand = {} # init players dict


    def __str__(self):
        return self.name

    def bet(self,amount):
        return amount

    def fold(self):
        pass 

    def all_in(self):
        self.bet(self.chips)

    def fold(self):
        pass
    def call(self):
        pass
    def raise_(self):
        pass