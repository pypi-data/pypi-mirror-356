# odd_sorter/core.py

def sort_odds(lst):
    odds = sorted([x for x in lst if x % 2 == 1])
    result = []
    odd_index = 0

    for x in lst:
        if x % 2 == 1:
            result.append(odds[odd_index])
            odd_index += 1

    return result
