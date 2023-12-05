"""
PART ONE
On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form
a single two-digit number. For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document (input.txt). What is the sum of all of the calibration values?
"""

with open("input.txt", "r") as f:
    calibration_doc = f.read().splitlines()

total = 0

for line in calibration_doc:

    digits = [char for char in line if char.isdigit()]

    if not digits:
        total += 0

    else:
        first = digits[0]
        last = digits[::-1][0]
        total += int(first + last)



"""
PART TWO
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two,
three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""

digit_map = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

cleanups = {
    "oneight": "18",
    "twone": "21",
    "threeight": "38",
    "fiveight": "58",
    "sevenine": "79",
    "eightwo": "82",
    "eighthree": "83",
    "nineight": "98",
}

total = 0

for line in calibration_doc:

    for pattern, replacement in cleanups.items():
        line = line.replace(pattern, replacement)

    for digit_str, digit in digit_map.items():
        line = line.replace(digit_str, digit)

    if should_print:
        print(line)

    digits = [char for char in line if char.isdigit()]

    if not digits:
        total += 0

    else:
        first = digits[0]
        last = digits[::-1][0]
        total += int(first + last)
