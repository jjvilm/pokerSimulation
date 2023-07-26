def break_high_card_tie(players: list) -> list:
    # get players hand cards as a set
    # {name:set(2,4,5)}
    def prepare_hand():
        for player in players:
            player.sequenced_ranks = set()
            for rank_set in player.hand.values():
                player.sequenced_ranks = player.sequenced_ranks.union(rank_set)
            # remove the 2 smallest cards from their set
            player.sequenced_ranks.remove(min(player.sequenced_ranks))
            player.sequenced_ranks.remove(min(player.sequenced_ranks))
            print("ln12:",player.name,  sorted(player.sequenced_ranks, reverse=True))
        
        # find highest score
        highest_ranking_card_among_players = max([max(player.sequenced_ranks) for player in players])
        candidates = [player for player in players if highest_ranking_card_among_players in player.sequenced_ranks]
        return candidates

    def next_high_card(candidates):
        # check everyones highest ranking card
        players_highest_ranking_card = dict()
        # get each player's highest ranking card
        for player in candidates:
            players_highest_ranking_card[player] = max(player.sequenced_ranks)
        # best card among players
        highest_card_among_players = max(players_highest_ranking_card.values())
        # print("ln231:highest ranking card:", highest_card_among_players)
        # only players with the best card
        candidates = [player for player,high_rank in players_highest_ranking_card.items() if high_rank == highest_card_among_players]
        # print([candidate.name for candidate in candidates])
        # remove that card from these candidates and go again
        for player in candidates:
            player.sequenced_ranks.remove(highest_card_among_players)
        
        
        return candidates


    candidates = prepare_hand()
    for _ in range(5):
        if len(candidates) == 1:
            return [candidate.name for candidate in candidates]
        
        candidates = next_high_card(candidates)
        
    return [candidate.name for candidate in candidates]

def break_tie_3_or_4_of_a_kind(players: list, rank_break):
    def prepare_hand():
        print("Doing a calc on rank:", rank_break)
        # players with 3-of-a-kind
        pair_of_cards = [player for player in players if player.hand_rank == rank_break]

        players_highest_pair = {}
        # find highest ranking hand of pairs (3s or 4s of-a-kind)
        for player in pair_of_cards:
            pairs_in_hand = player.rank_pairs_in_hand['three_or_four_kind']
            higher_ranking_pair = max(pairs_in_hand)
            # remove higher_ranking_pair for next iteration to work properly
            pairs_in_hand.remove(higher_ranking_pair)
            # gets player higher-ranking pairs
            players_highest_pair[player] = higher_ranking_pair

            # remove highest pair from hand, so later the highest card or 2nd highest pair can be analyzed
            player.sequenced_ranks = list()
            for rank_set in player.hand.values():
                # print("ln81:", rank_set)
                if higher_ranking_pair in rank_set:
                    # leave only the kicker cards 
                    rank_set.remove(higher_ranking_pair)
                player.sequenced_ranks += rank_set

            # remove the 2 smallest cards from their set
            player.sequenced_ranks.remove(min(player.sequenced_ranks))
            player.sequenced_ranks.remove(min(player.sequenced_ranks))

            print("ln76:",player.name,  sorted(player.sequenced_ranks, reverse=True))

        # print("ln37:",players_highest_pair)

        highest_ranking_pair = max(players_highest_pair.values())
        print("ln81 higher_ranking_pair", higher_ranking_pair)
        # player(s) with high-ranking pair
        candidates = [player for player,rank in players_highest_pair.items() if rank == highest_ranking_pair]
        print("ln84 candidates:", [candidate.name for candidate in candidates])
        return candidates

    def next_high_card(candidates):
        # check everyones highest ranking card
        players_highest_ranking_card = dict()
        # get each player's highest ranking card
        for player in candidates:
            players_highest_ranking_card[player] = max(player.sequenced_ranks)
        # best card among players
        highest_card_among_players = max(players_highest_ranking_card.values())
        # print("ln231:highest ranking card:", highest_card_among_players)
        # only players with the best card
        candidates = [player for player,high_rank in players_highest_ranking_card.items() if high_rank == highest_card_among_players]
        # print([candidate.name for candidate in candidates])
        # remove that card from these candidates and go again
        for player in candidates:
            player.sequenced_ranks.remove(highest_card_among_players)
        
        
        return candidates
    
    candidates = prepare_hand()
    
    # iterate once for 4okind, and twice for 3okind
    iterations = 1 if rank_break == 8 else 2
    for _ in range(iterations):
        print("iterations:", _)
        if len(candidates) == 1:
            return [candidate.name for candidate in candidates]
        
        candidates = next_high_card(candidates)
        
    return [candidate.name for candidate in candidates]
    
    # # players with same rankingpairs.  go with higher ranking kicker
    # if len(candidates) >= 2:
    #         players_with_same_highranking_pair = [player for player_name in candidates for player in pair_of_cards if player.name == player_name] 
    #         # print("ln48:", players_with_same_highranking_pair)
    #         # more than 2 with same high-ranking pair
    #         # if it's one-pair, go with highest-ranking kicker
    #         # if it's two-pair, go with 2nd highest-ranking pair
    #         players_side_cards = {}
    #         for player in players_with_same_highranking_pair:
    #             players_side_cards[player.name] = []
    #             # print("ln79:", player.name)
    #             for rank_set in player.hand.values():
    #                 for rank in rank_set:
    #                     players_side_cards[player.name].append(rank)
    #             # sum up ranks to use as score
    #             # players_side_cards_score[player.name] = sum(players_side_cards_score[player.name])
    #         # print("ln61:", players_side_cards)
    #         highest_kicker = max([rank for rank_set in players_side_cards.values() for rank in rank_set])
    #         # print("ln63:", highest_kicker)
    #         players_with_highest_kicker = [ name for name,rank_set in players_side_cards.items() if max(rank_set) == highest_kicker]
    #         # print("ln65:", players_with_highest_kicker)
    #         candidates = players_with_highest_kicker
    
    # return candidates

def break_full_house_tie(players: list):
    """  best three of a kind is the winner, if both players have the same three of a kind,
      the best pair wins. If both players have the same three of a kind and pair,
        the hand will always be split."""
    def break_tie(candidates, option=0):
        # players with 3-of-a-kind
        players_highest_trips_or_pair = {}
        # find highest ranking hand of pairs (3s or 4s of-a-kind)
        for player in candidates:
            # 0th index have the 3-of-a-kind ranks
            players_highest_trips_or_pair[player.name] = player.rank_pairs_in_hand['full_house'][option]

            # following line can be commented out, used for VISUALS only
            if option == 0:
                player.sequenced_ranks += ([player.rank_pairs_in_hand['full_house'][option] for _ in range(3)])
            if option == 1:
                player.sequenced_ranks += ([player.rank_pairs_in_hand['full_house'][option] for _ in range(2)])
            print(player.name, player.sequenced_ranks)

        higher_ranking_3ofkind = max(players_highest_trips_or_pair.values())
        print("ln157 higher_ranking_pair", higher_ranking_3ofkind)
        # player(s) with high-ranking pair
        candidates = [name for name,rank in players_highest_trips_or_pair.items() if rank == higher_ranking_3ofkind]
        candidates = [player for player in players if player.name in candidates]
        print("ln60 candidates:", [candidate.name for candidate in candidates])
        return candidates
    
    candidates = [player for player in players if player.hand_rank == 7]
    # option=0 for threes, option=1 for pairs
    candidates = break_tie(candidates, option=0)
    if len(candidates) >= 2:
        candidates = break_tie(candidates, option=1)
        return [candidate.name for candidate in candidates]
    else:
        return [candidate.name for candidate in candidates]

def break_tie_in_onepair(players: list):
    def get_onepair_players():
        onepair_players = [player for player in players if player.hand_rank == 2]
        players_highest_pair = {}
        for player in onepair_players:
            pairs_in_hand = player.rank_pairs_in_hand['pair']
            higher_ranking_pair = max(pairs_in_hand)
            # remove higher_ranking_pair for next iteration to work properly
            pairs_in_hand.remove(higher_ranking_pair)
            players_highest_pair[player.name] = higher_ranking_pair
            # remove highest pair from hand, so later the highest card or 2nd highest pair can be analyzed
            for rank_set in player.hand.values():
                # print("ln81:", rank_set)
                if higher_ranking_pair in rank_set:
                    # leave only the kicker cards 
                    rank_set.remove(higher_ranking_pair)

        highest_ranking_pair = max(players_highest_pair.values())
        candidates = [player for name,rank in players_highest_pair.items() for player in onepair_players if rank == highest_ranking_pair and name == player.name]
        print("ln124:", [candidate.name for candidate in candidates])
        if len(candidates) >= 2:
            # get the cards that will be used for ranking
            for player in candidates:
                player.sequenced_ranks = []
                # print("ln79:", player.name)
                for rank_set in player.hand.values():
                    for rank in rank_set:
                        player.sequenced_ranks.append(rank)

        return candidates
    
    def iterate_until_highest_ranking_card(candidates):
        # check everyones highest ranking card
        players_highest_ranking_card = dict()
        # get each player's highest ranking card
        for player in candidates:
            players_highest_ranking_card[player] = max(player.sequenced_ranks)
        # best card among players
        highest_card_among_players = max(players_highest_ranking_card.values())
        print("ln231:highest ranking card:", highest_card_among_players)
        # only players with the best card
        candidates = [player for player,high_rank in players_highest_ranking_card.items() if high_rank == highest_card_among_players]
        print([candidate.name for candidate in candidates])
        # remove that card from these candidates and go again
        for player in candidates:
            player.sequenced_ranks.remove(highest_card_among_players)
        
        
        return candidates
    
    candidates = get_onepair_players()
    # iterate 3 times, b/ (5 cards in hand - 2 cards(pair) = 3)
    for _ in range(3):
        # print(_)
        if len(candidates) == 1:
            # input()
            return [candidate.name for candidate in candidates]
        candidates = iterate_until_highest_ranking_card(candidates)
        
    return [candidate.name for candidate in candidates]

def break_tie_in_twopairs(players: list):

    def break_ties(iterations):
            # print("ln26:iterating:", iterations)
            print("Iteration:", _)
            # finding highest pair of cards from players
            players_highest_pair = {}
            for player in two_pair_players:
                pairs_in_hand = player.rank_pairs_in_hand['pair']
                higher_ranking_pair = max(pairs_in_hand)
                # remove higher_ranking_pair for next iteration to work properly
                pairs_in_hand.remove(higher_ranking_pair)
                players_highest_pair[player.name] = higher_ranking_pair
                # remove highest pair from hand, so later the highest card or 2nd highest pair can be analyzed
                for rank_set in player.hand.values():
                    # print("ln81:", rank_set)
                    if higher_ranking_pair in rank_set:
                        # leave only the kicker cards 
                        rank_set.remove(higher_ranking_pair)

            print("ln42:",players_highest_pair)

            highest_ranking_pair = max(players_highest_pair.values())
            # player(s) with high-ranking pair
            candidates = [name for name,rank in players_highest_pair.items() if rank == highest_ranking_pair]
            # print("ln43:", candidates, "with highest pair:",highest_ranking_pair )
            
            if len(candidates) == 1:
                iterations = 0
                return candidates, iterations
            if len(candidates) >= 2:
                players_with_same_highranking_pair = [player for player_name in candidates for player in two_pair_players if player.name == player_name] 
                # print("ln48:", players_with_same_highranking_pair)
                # more than 2 with same high-ranking pair
                # if it's one-pair, go with highest-ranking kicker
                # if it's two-pair, go with 2nd highest-ranking pair
                players_side_cards = {}
                for player in players_with_same_highranking_pair:
                    players_side_cards[player.name] = []
                    # print("ln79:", player.name)
                    for rank_set in player.hand.values():
                        for rank in rank_set:
                            players_side_cards[player.name].append(rank)
                    # sum up ranks to use as score
                    # players_side_cards_score[player.name] = sum(players_side_cards_score[player.name])
                # print("ln61:", players_side_cards)
                highest_kicker = max([rank for rank_set in players_side_cards.values() for rank in rank_set])
                # print("ln63:", highest_kicker)
                players_with_highest_kicker = [ name for name,rank_set in players_side_cards.items() if max(rank_set) == highest_kicker]
                # print("ln65:", players_with_highest_kicker)
                candidates = players_with_highest_kicker
                # print("ln:67:", candidates)
                            
            
                # Decrease iterations to break out of the loop if we have a winner
                iterations -= 1
                return candidates, iterations # Return the updated 'candidates' and 'iterations' values
    # players with two pairs
    two_pair_players: list(object) = [player for player in players if player.hand_rank == 3]
    # 1 winner
    if len(two_pair_players) == 1:
        return two_pair_players[0].name
    # multiple candidates
    # print("two pair players:", len(two_pair_players))
    # return select_from_multiple_players_with_pairs(two_pair_players, pair_rank=3)
    
    # iterate 1 if players have one-pair, else 2 for two pairs
    iterations = 2 
    for _ in range(iterations):
        candidates, iterations = break_ties(iterations)  
        if iterations == 0:
            break
    # print("ln83:",candidates)  
    return candidates

def break_tie_in_straight_flush(players: list):
    # {'abe':14, 'cee':13}
    # find out who has the highest ranking in their ranks sequence within the suit
    candidates = [player for player in players if player.hand_rank in [9,10]]
    players_highest_ranking = dict()
    for player in candidates:
        # if len(player.sequenced_ranks) == 0:
        #     continue
        players_highest_ranking[player.name] = max(player.sequenced_ranks)
        print(player.name, sorted(player.sequenced_ranks, reverse=True))
    highest_rank_among_players = max(players_highest_ranking.values())
    winners = [name for name, rank in players_highest_ranking.items() if rank == highest_rank_among_players]
    print("Straight Flush:", players_highest_ranking)
    return winners

def break_tie_in_flush(players: list):

    def get_flush_cards():
        candidates = []
        for player in players:
            flush_cards = [rank for rank_set in player.hand.values() for rank in rank_set if len(rank_set) >= 5]
            if len(flush_cards) == 0:
                continue
            # trim the list to 5 cards, the hand to declare winner of best hand (consists of 5 cards)
            if len(flush_cards) == 7:
                flush_cards.remove(min(flush_cards))
                flush_cards.remove(min(flush_cards))
            if len(flush_cards) == 6:
                flush_cards.remove(min(flush_cards))
            player.sequenced_ranks = flush_cards
            # adds the players that have a flush to the list
            candidates.append(player)
        return candidates
    def iterations(candidates):
        # check everyones highest ranking card
        players_highest_ranking_card = dict()
        # get each player's highest ranking card
        for player in candidates:
            players_highest_ranking_card[player] = max(player.sequenced_ranks)
        # best card among players
        highest_card_among_players = max(players_highest_ranking_card.values())
        # print("ln231:highest ranking card:", highest_card_among_players)
        # only players with the best card
        candidates = [player for player,high_rank in players_highest_ranking_card.items() if high_rank == highest_card_among_players]
        # print([candidate.name for candidate in candidates])
        # remove that card from these candidates and go again
        for player in candidates:
            print(player.name, sorted(player.sequenced_ranks, reverse=True))
            player.sequenced_ranks.remove(highest_card_among_players)
        
        return candidates
    
    candidates = get_flush_cards()
    for _ in range(5):
        print("Iteration", _)
        if len(candidates) == 1:
            # input()
            return [candidate.name for candidate in candidates]
        # print(_)
        candidates = iterations(candidates)
        
    return [candidate.name for candidate in candidates]

def break_tie_in_straight(players: list):
    # find out who has the highest ranking in their ranks sequence
    # {'abe':14, 'cee':13}
    players_highest_ranking = dict()
    for player in players:
        if len(player.sequenced_ranks) == 0 and player.hand_rank != 5:
            continue
        print("ln239:", player.name, player.sequenced_ranks)
        players_highest_ranking[player.name] = max(player.sequenced_ranks)
    highest_rank_among_players = max(players_highest_ranking.values())
    winners = [name for name, rank in players_highest_ranking.items() if rank == highest_rank_among_players]
    print("Straight:", winners)
    return winners