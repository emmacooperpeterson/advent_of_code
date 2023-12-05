"""
PART ONE
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58
(middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine
schematic?
"""

import numpy as np
import pandas as pd
import re

with open("input.txt", "r") as f:
    engine_schematic = f.read()

symbols = {char for char in engine_schematic if not re.match("[\d\.\n]", char)}
symbols = {f"\{s}" for s in symbols}
symbol_pattern = f"[{''.join(symbols)}]"

engine_schematic = engine_schematic.splitlines()

all_numbers = []
all_symbol_indexes = []
all_star_indexes = []
part_numbers = []

for i, row in enumerate(engine_schematic):
    numbers = [match.group() for match in re.finditer("\d+", row)]

    number_spans = [match.span() for match in re.finditer("\d+", row)]

    symbol_indexes = [match.span()[0] for match in re.finditer(symbol_pattern, row)]

    all_numbers.append(list(map(lambda n, s: (n, s), numbers, number_spans)))
    all_symbol_indexes.append(symbol_indexes)

    # for part two
    star_indexes = [match.span()[0] for match in re.finditer("\*", row)]
    all_star_indexes.append([(i, si) for si in star_indexes])


potential_gears = []
for i, numbers in enumerate(all_numbers):

    symbol_indexes = all_symbol_indexes[i].copy()

    # for part two
    star_indexes = all_star_indexes[i].copy()

    if i > 0:
        symbol_indexes += all_symbol_indexes[i-1]
        star_indexes += all_star_indexes[i-1]

    if i < len(all_numbers) - 1:
        symbol_indexes += all_symbol_indexes[i+1]
        star_indexes += all_star_indexes[i+1]

    for number, span in numbers:
        if [s for s in symbol_indexes if s in range(span[0]-1, span[1]+1)]:
            part_numbers.append(int(number))

        # for part two. star_indexes is [(row_num, star_index), ...]
        nearby_stars = [s for s in star_indexes if s[1] in range(span[0]-1, span[1]+1)]
        if nearby_stars:
            potential_gears += [(ns[0], ns[1], int(number)) for ns in nearby_stars]

part_number_sum = sum(part_numbers)

potential_gears = pd.DataFrame(potential_gears, columns=["row_num", "star_index", "number"])
potential_gears["count"] = potential_gears.groupby(["row_num", "star_index"])["number"].transform("count")
gears = potential_gears[potential_gears["count"]==2].drop(columns=["count"])
gears = gears.groupby(["row_num", "star_index"])["number"].apply(np.array).reset_index()
gears["gear_ratio"] = gears["number"].apply(lambda cell: cell[0]*cell[1])

gear_ratio_sum = gears["gear_ratio"].sum()


"""
PART TWO

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is
adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which
gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio
is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because
it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

# incorporated above
