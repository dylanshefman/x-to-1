def ask_for_int(message):
    is_int = False
    while not is_int:
        try:
            value = int(input(message))
            is_int = True
        except:
            print("        Please enter an integer value.")
    
    return value

def setup():
    print("Welcome to the x-to-1 scorekeeper!\n")

    # get number of rounds
    num_rounds = ask_for_int("Enter number of rounds: ")

    # get number of players
    num_players = ask_for_int("Enter number of players: ")
    
    # ensure deck has enough cards
    while num_players * num_rounds > 52:
        print(f"{num_players} players playing {num_rounds} rounds would require {num_players * num_rounds} cards. Try again.")
        # get number of rounds
        num_rounds = ask_for_int("Enter number of rounds")
        # get number of players
        num_players = ask_for_int("Enter number of players: ")

    # get player names
    players = []
    for i in range(num_players):
        player = input(f"Enter player {i+1} name: ")
        player = player[0].upper() + player[1:].lower()
        while player in players:
            print("        Player names must be distinct.")
            player = input(f"Enter player {i+1} name: ")
            player = player[0].upper() + player[1:].lower()
        players.append(player)

    # initialize each player's bet to 0
    bets = {}
    for player in players:
        bets[player] = 0

    # initialize each player's score to 0
    scores = {}
    for player in players:
        scores[player] = 0

    print("\nStarting game!\n")

    return players, num_rounds, bets, scores

def round(round_num, num_cards, players, bets, scores):
    # get index of dealer
    dealer_index = round_num % len(players)
    print(f"{players[dealer_index]} is the dealer.\n")

    sum_bets_so_far = 0
    # iterate through players
    for i in range(1, len(players) + 1):
        # get player's index
        index = (dealer_index + i) % len(players)
        # if player is last to bet, print bet restriction
        if i == len(players) and sum_bets_so_far <= num_cards:
            print(f"        ({players[index]} may not bet {num_cards - sum_bets_so_far}.)")
        # get bet
        bet = ask_for_int(f"Enter {players[index]}'s bet: ")
        # if last player bets forbidden amount, ask them to try again
        if i == len(players):
            while bet == num_cards - sum_bets_so_far:
                print(f"        ({players[index]} can't bet that. Try again.)")
                bet = ask_for_int(f"Enter {players[index]}'s bet: ")
        # add bet to bet dictionary
        bets[players[index]] = bet
        sum_bets_so_far += bet

    print("\n")

    winners = []
    losers = []
    sum_tricks_so_far = 0
    num_players_counted = 0
    # iterate through players
    for i in range(1, len(players) + 1):
        # get player's index
        index = (dealer_index + i) % len(players)
        
        # if sum of tricks so far is equal to number of cards in the hand, then player must have won 0
        if sum_tricks_so_far == num_cards:
            actual = 0
            print(f"X-to-1 has determined that {players[index]} won {actual} tricks.")
        # if player is not last to enter number of tricks won, ask for number won
        elif num_players_counted < len(players) - 1:
            actual = ask_for_int(f"Enter the number of tricks {players[index]} won: ")
            # reject number of tricks won if it's impossible
            while actual > num_cards - sum_tricks_so_far:
                print(f"        Previous players have won a total of {sum_tricks_so_far} tricks. It is not possible for {players[index]} to have won {actual} tricks.")
                actual = ask_for_int(f"Enter the number of tricks {players[index]} won: ")
        # otherwise calculate number of tricks won
        else:
            actual = num_cards - sum_tricks_so_far
            message = f"X-to-1 has determined that {players[index]} won {actual} tricks."
            if actual == 1: message = message[:-2] + "."
            print(message)

        sum_tricks_so_far += actual
        num_players_counted += 1

        # if player wins amount bet, calculate winnings
        if bets[players[index]] == actual:
            if actual == 0:
                winnings = 5
            else:
                winnings = actual + 10
            scores[players[index]] = scores[players[index]] + winnings
            winners.append((players[index], winnings))
        # otherwise calculate losses
        else:
            offset = abs(bets[players[index]] - actual)
            scores[players[index]] = scores[players[index]] - offset
            losers.append((players[index], offset))
    
    # display winners and losers
    print(f"\nWinners:")
    for item in winners:
        print(f"{item[0]} ({item[1]})")
    print(f"Losers:")
    for item in losers:
        print(f"{item[0]} ({item[1] * -1})")
    
    return scores

def results(scores):
    print("\nFinal scores:")
    for player in scores:
        print(f"{player}: {scores[player]}")
    max = 0
    winner = ""
    for player in scores:
        if scores[player] > max:
            max = scores[player]
            winner = player
    
    winners = []
    for player in scores:
        if scores[player] == max:
            winners.append(player)
    if len(winners) > 1:
        winners = ", ".join(winners)
    else:
        winners = winner
    print(f"Winner: {winner}")

def scores_to_date(scores):
    print("\nScores so far:")
    for player in scores:
        print(f"{player}: {scores[player]}")
    max = 0
    leader = ""
    for player in scores:
        if scores[player] > max:
            max = scores[player]
            leader = player
    
    leaders = []
    for player in scores:
        if scores[player] == max:
            leaders.append(player)
    if len(leaders) > 1:
        leaders = ", ".join(leaders)
    else:
        leaders = leader
    print(f"In the lead: {leaders}\n\n")


def edit(scores, players):
    choice = input("\nWould you like to edit scores? Enter 'Y' to edit or anything else to continue. ")
    
    if choice == "Y" or choice == "y":
        num_amends = ask_for_int("How many scores would you like to change? ")
        while num_amends > len(players):
            print(f"        You may only edit {len(players)} players.")
            num_amends = ask_for_int("How many scores would you like to change? ")
        for i in range(num_amends):
            if num_amends > 1: print(f"Completing edit {i+1}.")
            name = input("Enter the name of the player whose score you would like to change: ")
            exists = False

            for player in players:
                if name.lower() == player.lower():
                    exists = True
                    scores[player] = ask_for_int(f"Enter the amended score for {player}: ")
                    break
            while not exists:
                print(f"        Player '{name}' was not found. Please try again.")
                name = input("Enter the name of the player whose score you would like to change: ")
                for player in players:
                    if name.lower() == player.lower():
                        exists = True
                        scores[player] = ask_for_int(f"Enter the amended score for {player}: ")
                        break

    return scores

def main():
    players, num_rounds, bets, scores = setup()

    num_cards = num_rounds
    round_num = 0

    while num_cards > 0:
        print(f"Starting round of {num_cards}.")
        scores = round(round_num, num_cards, players, bets, scores)
        scores = edit(scores, players)
        if num_cards > 1: 
            scores_to_date(scores)
        num_cards -= 1
        round_num += 1
    
    results(scores)
    
main()
