from random import randint


def dice_toss(skill:int):
    tot = 0
    for _ in range(skill):
        tot += randint(1, 7)
    return(tot)

def sort_keys(obj:dict) -> list:
    return list(dict(sorted(obj.items(), key=lambda item: item[1], reverse=True)).keys())