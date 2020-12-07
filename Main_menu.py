#Show basic instructions
def show_help():
    print("\nTry to find the way out before the monsters finds you!")
    print("\nYou can move up(U), down(D), left(L), or right(R).")
    print("\nYou cannot move into any space you have already been in.")
    print("\If you box yourself in or get attached by the monster, you lose...")
    print("\nTo show these instructions again type 'HELP'. To end the game type 'QUIT'.")

#Initialization of parameters?

#Temporary move command
players_moves = []
players_directions = ["U", "D", "L", "R"]

player_choice = input(">>>").upper()

#game loop
while True:
    if player_choice == "HELP":
        show_help()
        player_choice = input(">>>").upper()
    elif player_choice == "QUIT":
        break
    elif player_choice not in players_directions:
        print("\n>>>Command key not recognized<<<")
        show_help()
        player_choice = input("Please Try Again. >>>").upper()