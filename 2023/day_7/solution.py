from itertools import groupby
import numpy as np
import pandas as pd
import re

PART = 2  # 1 or 2


def adjust_j(card_groups):
    """
    This is for part 2. If there are any Js in the card_groups, append them to
    the largest non-J group.

    e.g. [["A", "A"], [2], [3], ["J"]] --> [["A", "A", "J"], [2], [3]]
    """

    num_j = sum([item=="J" for sublist in card_groups for item in sublist])
    if num_j == 0 or num_j == 5:
        return card_groups

    else:
        j_group = ["J"] * num_j
        non_j_groups = [g for g in card_groups if "J" not in g]
        non_j_groups.sort(key=len)
        non_j_groups[-1] += j_group
        return non_j_groups


# setup
with open("input.txt", "r") as f:
    hands = f.read().splitlines()

hands = pd.DataFrame([h.split() for h in hands], columns=["cards", "bid"])
hands["bid"] = hands["bid"].astype("int")

# create one column for each of the 5 cards per hand
cards = hands["cards"].apply(lambda x: pd.Series(list(x)))
cards.columns = [f"card_{i}" for i in range(1, 6)]
hands = pd.concat([cards, hands], axis=1)

# create card groups, e.g. "233KT" --> [[2], [3, 3], [K], [T]]
hands["cards"] = hands.apply(lambda row: ''.join(sorted(row["cards"])), axis=1)

hands["card_groups"] = hands.apply(
    lambda row: [list(g) for k, g in groupby(row["cards"])], axis=1
)

if PART == 2:  # append Js to largest non-J group
    hands["card_groups"] = hands.apply(
        lambda row: adjust_j(row["card_groups"]), axis=1
    )

# for each hand, count number of unique cards and size of largest group
hands["n_groups"] = hands.apply(lambda row: len(row["card_groups"]), axis=1)
hands["max_group_size"] = hands.apply(
    lambda row: max([len(g) for g in row["card_groups"]]), axis=1
)

# rank the hands, not yet taking individual cards into account
hand_ranks = [7, 6, 5, 4, 3, 2, 1]

conditions = [
    (hands["n_groups"] == 1),                                    # five of a kind
    (hands["max_group_size"] == 4),                              # four of a kind
    ((hands["n_groups"] == 2) & (hands["max_group_size"] == 3)), # full house
    ((hands["n_groups"] == 3) & (hands["max_group_size"] == 3)), # three of a kind
    ((hands["n_groups"] == 3) & (hands["max_group_size"] == 2)), # two pair
    (hands["n_groups"] == 4),                                    # one pair
    (hands["n_groups"] == 5)                                     # high card
]

hands["hand_rank"] = np.select(conditions, hand_ranks)

# convert all cards to numbers
replacements = {
    1: {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14},
    2: {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}
}

hands = hands.replace(replacements[PART])
hands = hands.astype({f"card_{i}": "int" for i in range(1, 6)})

# sort and rank
hands = hands.sort_values(["hand_rank", "card_1", "card_2", "card_3", "card_4", "card_5"])
hands["rank"] = range(1, len(hands)+1)

# calculate winnings
hands["winnings"] = hands["bid"] * hands["rank"]
total_winnings = hands["winnings"].sum()
