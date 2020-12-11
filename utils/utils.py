from random import randint


def dice_toss(ability:int):
    tot = 0
    for _ in range(ability):
        tot += randint(1, 7)
    return(tot)

def sort_keys(obj:dict) -> list:
    return list(dict(sorted(obj.items(), key=lambda item: item[1], reverse=True)).keys())