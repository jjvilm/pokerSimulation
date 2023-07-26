def get_best_5_card_hand(hole_cards, community_cards):
    # Combine hole cards with community cards
    all_cards = set(hole_cards)
    all_cards |= community_cards

    # Generate all possible 5-card combinations
    from itertools import combinations
    all_combinations = combinations(all_cards, 5)

    # Find the best 5-card hand
    best_hand = max(all_combinations, key=lambda cards: max(cards))

    return best_hand


def get_highest_card_rank(hole_cards, community_cards):
    best_hand = get_best_5_card_hand(hole_cards, community_cards)
    highest_card = max(best_hand)
    return highest_card


# Example usage
player1_hole_cards = {14, 9}  # Player 1's hole cards
player2_hole_cards = {14, 5}  # Player 2's hole cards
community_cards = {2,3,8,11,12}

highest_rank_player1 = get_highest_card_rank(player1_hole_cards, community_cards)
highest_rank_player2 = get_highest_card_rank(player2_hole_cards, community_cards)

if highest_rank_player1 > highest_rank_player2:
    print("Player 1 has the highest-ranking card:", highest_rank_player1)
elif highest_rank_player2 > highest_rank_player1:
    print("Player 2 has the highest-ranking card:", highest_rank_player2)
else:
    print("It's a tie. Both players have the same highest-ranking card:", highest_rank_player1)
