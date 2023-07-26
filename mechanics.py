# from typing import Tuple
from collections import Counter
from ties import break_tie_in_straight_flush, break_tie_in_straight, break_full_house_tie
from ties import break_high_card_tie,break_tie_in_twopairs, break_tie_3_or_4_of_a_kind
from ties import break_tie_in_flush, break_tie_in_onepair



hand_rankings = {
    1: 'High Card', 
    2: 'One Pair', 
    3: 'Two Pair', 
    4: 'Three-of-a-Kind', 
    5: 'Straight', 
    6: 'Flush', 
    7: 'FullHouse', 
    8: 'Four-of-a-Kind', 
    9: 'Straight Flush', 
    10: 'Royal Flush'
}

def analyze_gameplay(player: object) -> int:
    rank_count, suit_count = count_occurences(player.hand)
    player.hand_rank = []

    player.hand_rank.append(pair(player,rank_count)) # stable
    player.hand_rank.append(three_or_four_kind(player, rank_count)) # stable
    player.hand_rank.append(straight(player, rank_count,suit_count)) # stable
    player.hand_rank.append(full_house(player, rank_count)) # stable

    # print(f"{player.name} hand_rank: {player.hand_rank}")
    player.hand_rank = max(player.hand_rank)

def count_occurences(hand: dict) -> dict:
    # Count the occurrences of each rank and suit
    rank_count = Counter(rank for rank_set in hand.values() for rank in rank_set)
    suit_count = {suit:len(hand[suit]) for suit in hand.keys()}
    # print(f"ln33:{rank_count}")
    # print(f"ln34:{suit_count}")

    return rank_count, suit_count

def has_sequence(rank_count: list, player=None) -> tuple(): 
    # print(f"ln50 :{rank_count}")
    """ pass in a list of ranks, e.g. [2,4,4,3,10,8]"""  
    ranks = list(set(rank for rank in rank_count))
    # print(f"ln47:{ranks}")

    # converts to set, so it sorts in order, and removes duplicates
    # then back to list to be able to reference by index
    # print(f"ln54: {ranks}")
    # print(f"rank_dict {rank_dict}")
    # print(f"sequence {rank_sequence}")
    sequence_count = 0
    last_sequenced = 0
    # sequence in reverse, from highest to lowest
    for i in range(len(ranks) - 1, 0, -1):
        # i = i + 1
        if ranks[i] - 1 == ranks[i - 1]:
            sequence_count += 1

            # ONLY the top 5 highest cards needed
            if sequence_count == 4:
                # check if next rank is next in sequence
                # print("ln88",ranks[i],ranks[i -1]  )
                # if ranks[i] - 1 == ranks[i-1]:  # NOT NEEDED B/ SEQUENCE WILL BE BIGGER THAN 5
                last_sequenced = ranks[i - 1] + 4
                if player != None:
                    player.sequenced_ranks = [rank for rank in range(ranks[i-1], ranks[i-1] + 5)]
                    print(f"ln70:{player.name, sorted(player.sequenced_ranks)}")
                break
            # print(f"ln84:seqCount:{sequence_count}-{ranks[i]}")
        else:
            # print(f"ln94:{ranks[i] - 1, ranks[i - 1]}")
            sequence_count = 0  # Reset the sequence count
    
    # print(f"ln88:sequence count:{sequence_count}")

    # [10, 11, 12, 13, 14] = 4 hops, which would be 5 consecutive cards
    if sequence_count >= 4:  # Found a sequence of 5 consecutive numbers
        # print(f"ln69:{ranks}")
        # print(f"{ranks} Last in sequence: {last_sequenced}")
        return True, last_sequenced
    return False, last_sequenced

def is_same_suit(suit_count: dict) -> tuple:
    """ Any hand of 5 cards all the same suit"""
    for suit,suit_count in suit_count.items():
        # print("ln111:suit",suit,"count:",suit_count)
        if suit_count >= 5:
            return (True,suit)
    return (False,suit)

def full_house(player, rank_count: dict):
    """ Three-of-a-kind and a pair
        Hand with highest theree-of-a-kind win """
    threes = []
    pairs = []

    values = rank_count.values()
    if 3 in values and 2 in values:
        for rank,count in rank_count.items():
            # get the threes and pairs, then add the higher ranking to rank_pairs_in_hand, first item will be the 3s
            if count == 2:
                pairs.append(rank)
            elif count == 3:
                threes.append(rank)
        # higher-ranking 3-of-a-kind rank
        threes = max(threes)
        # higher-ranking pair rank
        pairs = max(pairs)

        player.rank_pairs_in_hand['full_house'] = [threes,pairs]
        return 7
    
    return 1  
def straight(player, rank_count: dict, suit_count: dict) -> int:
    """ Any five cards in sequence, but not the same suit"""
    is_sequence, last_sequenced_rank = has_sequence(rank_count)
    # A flush
    is_flush, suit_type_in_flush = is_same_suit(suit_count)

    # handles Straight flush and royal flush
    if is_flush:
        # check all cards in sequence have the same suit type in flush
        flush_ranks = list(player.hand[suit_type_in_flush])
        player.sequenced_ranks = flush_ranks
        # print("ln128 flush_ranks:",flush_ranks)
        # is_part_of_winning_hand = validate_winning_hand(player,flush_ranks, suit_type_in_flush)
        
        if is_sequence:
            # check if the sequence is in the flush cards
            sequence_in_flush_ranks, flush_last_sequenced = has_sequence(flush_ranks, player)
            # possible royal flush
            if sequence_in_flush_ranks:
                if 14 == flush_last_sequenced:
                    # royal flush
                    return 10
                # no High card in flush sequence
                # straight flush
                return 9
            
        # no sequence in flush, so probably just a flush
        return 6
    
    # print(f"ln149:{is_sequence}")
    if is_sequence:
        ranks_in_sequence = [rank  for rank in range(last_sequenced_rank, last_sequenced_rank-5,-1)]
        # print("ln178:",sorted(ranks_in_sequence))
        player.sequenced_ranks = ranks_in_sequence
        return 5
        
    return 1
def three_or_four_kind(player: object, rank_count: dict) -> int:
    """ Three cards of the same rank"""
    # print("ln185:", "clearing rank_pairs_in_hand")
    pairs_in_hand = player.rank_pairs_in_hand['three_or_four_kind'] = [] # clear incase some items exist in it already
    for rank,count in rank_count.items():
        # checks to make sure  card is part of the player's hole cards
        if count >= 3:
            pairs_in_hand.append(rank)
            if count >= 4:
                return 8
            return 4
    # print(f"!= 3kind ->3")
    return 1
def pair(player: object, rank_count: dict):
    """ Any two cards of the same rank"""
    # if len(pairs_in_hand) >= 1:
    # print("ln200:", "clearing rank_pairs_in_hand")
    pairs_in_hand = player.rank_pairs_in_hand['pair']  = []

    # if more than one pair
    for rank,count in rank_count.items():
        if count >= 2:
            pairs_in_hand.append(rank)
    # print("ln206:",pairs_in_hand)

    # no pairs
    if len(pairs_in_hand) == 0:
        return 1
    
    # two pair
    if len(pairs_in_hand) >= 2:
        return 3
    # one pair
    if len(pairs_in_hand) == 1:
        return 2
    

def decode_ranked(rank: int) -> int:
    if rank == 11:
        return 'J'
    elif rank == 12:
        return 'Q'
    elif rank == 13:
        return 'K'
    elif rank == 14:
        return 'A'
    else:
        return rank


def declare_winner(players: dict) -> str:
    player_ranks = {}
    # dict = name: card value
    for player in players:
        player_ranks[player.name] = player.hand_rank
    # print(player_ranks)
    # candidate winners
    top_player_rank = max(player_ranks.values())
    # candidates will be the ones with top_player_rank
    # list of names
    candidates: list = [player for player in player_ranks.keys() if player_ranks[player] == top_player_rank]

    print(f"top_player_rank_max: >>>{hand_rankings[top_player_rank]}<<< [rank:{top_player_rank}]")
    # declare winner here if only 1 player with higest rank
    if len(candidates) == 1:
            return candidates

    #  straight flush, or royal flush
    if top_player_rank in [9,10]:
        return break_tie_in_straight_flush(players)
    # four-of-a-kind
    if top_player_rank == 8:
        return break_tie_3_or_4_of_a_kind(players,8)
    # full House
    if top_player_rank == 7:
        return break_full_house_tie(players)
    # Flush
    if top_player_rank == 6:
        return break_tie_in_flush(players)
    # Straight
    if top_player_rank == 5:
        return break_tie_in_straight(players)
    # three-of-a-kind
    if top_player_rank == 4:
        return break_tie_3_or_4_of_a_kind(players,4)
    # break ties in one pair, or two pair
    if top_player_rank == 3:
        return break_tie_in_twopairs(players)
    if top_player_rank == 2:
        return break_tie_in_onepair(players)
    # break ties high-rank card
    if top_player_rank == 1:
        return break_high_card_tie(players)
   