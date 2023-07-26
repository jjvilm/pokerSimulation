from deck import Deck
from player import Player
from dealer import Dealer
from mechanics import declare_winner
from os import system


# create deck
deck = Deck()

# dealer deal cards to player
p1 = Player("Abe", 1000)
p2 = Player("Bob", 1000)
p3 = Player("Che", 1000)
p4 = Player("Dee", 1000)
p5 = Player("Ell", 1000)
p6 = Player("Fed", 1000)
players = [p1,p2,p3,p4,p5,p6]

# dealer
Game = Dealer(deck, players)
phases = ["pre-flop", "flop", "turn", "river"]

rank_condition = [1] # Rank that must be won by
n_ranks = 2 # No. of players with the same rank
n_winners = 1 # No. of winners
game_count = 0

def run():
    #pre-flop
    system('cls')
    Game.pre_flop()
    Game.flop()
    Game.turn()
    Game.river()

while 1:
    ####### DEBUG ############
    '♠' '♣' '♦' '♥'
    #(14,'♠')  (5,'♠') (9,'♠')
    # system('cls')
    # comm_card = ((10,'♥'),(8,'♦'),(5,'♠'), (6,'♥'),(2,'♠'))
    # p1_hole_cards = ((2,'♥'),(5,'♣'))
    # p2_hole_cards = ((2,'♣'),(5,'♦'))
    # # testing
    # player_list = [p1,p2]
    # cards = (p1_hole_cards, p2_hole_cards)
    # Game.test_mechanics(player_list,cards, comm_card)
    # Game.display_cc()
    ####### ^^^ DEBUG ^^^ ############
    run()
    Game.showdown()

    winners = declare_winner(players)
    print("winner:", winners)

    # break
    # input()

    # # new game
    Game.deck.reset_deck()

    player_ranks = []
    for player in players:
            player_ranks.append(player.hand_rank)
            player.reset()
    highest_rank = max(player_ranks)
    # more than 1 player has the rank condition
    if (player_ranks.count(highest_rank) >= n_ranks 
    and highest_rank in rank_condition
    and len(winners) >= n_winners):
        print(f"len of winners:{len(winners)} {winners}")
        print(f"No. Games:{game_count + 1}")
        input()
        game_count = 0

    game_count += 1
    Game.init_card_dicts()
    Game.community_cards_string = ""






