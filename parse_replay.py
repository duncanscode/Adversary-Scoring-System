from zephyrus_sc2_parser import parse_replay
from database import save_to_db, fetch_data

def replay_parser(filepath):
    print(f"Parsing replay: {filepath}")
    replay_data = parse_replay(filepath)
    
    # Assume 'PablosCruise' is your username
    my_username = 'PablosCruise'
    
    # Initialize variables
    win = 0
    loss = 0
    opponent_name = None
    
    # Get players
    player1 = replay_data.players[1]
    player2 = replay_data.players[2]
    print(f"Player 1 {player1.name}")
    print(f"Player 2 {player2.name}")
    print(f"Winner: {replay_data.metadata['winner']}")
    
    # Determine winner and opponent
    if player1.name == my_username:
        opponent_name = player2.name
        if replay_data.metadata['winner'] == 1:
            win = 1
        else:
            loss = 1
    elif player2.name == my_username:
        opponent_name = player1.name
        if replay_data.metadata['winner'] == 2:
            win = 1
        else:
            loss = 1
    else:
        print("Error: Your username not found in the replay")
        return
    
    # Get the map name (assuming it's stored in metadata)
    map_name = replay_data.metadata['map']
    print(f"Opponent: {opponent_name}")
    print(f"Map: {map_name}")
    print(f"Result: {'Win' if win else 'Loss'}")
    
    # Save to database
    save_to_db(opponent_name, map_name, win, loss)

def calculate_win_loss(oppname):
    query = "SELECT SUM(wins) AS total_wins, SUM(losses) AS total_losses FROM matches where opponent_name = ?;"
    opponent_name = oppname 
    results = fetch_data(query,(opponent_name,))
    print(results)
