#Show basic instructions
def show_help():
    print("\nTry to find the way out before the monsters finds you!")
    print("\nYou can move up(U), down(D), left(L), or right(R).")
    print("\nYou cannot move into any space you have already been in.")
    print("\nIf you box yourself in or get attached by the monster, you lose...")
    print("\nTo show these instructions again type 'HELP'. To end the game type 'QUIT'.")


def welcomeMessage():
    print("\nDungeon Run är ett textbaserat äventyrsspel för en spelare. Det spelas genom att göra val i menyer som") 
    print("\ninnehåller olika alternativ. Man väljer vilken typ av hjälte man vill spela, för att sedan utforska en karta") 
    print("\nmed slumpmässigt innehåll i jakt på skatter. Men se upp för monster! Det gäller att samla på sig så mycket") 
    print("\nskatter som möjligt och att hitta ut med livet i behåll.")
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