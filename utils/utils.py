from random import randint


def dice_toss(ability:int):
    tot = 0
    for _ in range(ability):
        tot += randint(1, 7)
    return(tot)

