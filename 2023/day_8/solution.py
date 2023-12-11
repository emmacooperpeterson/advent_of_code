from functools import reduce

with open("input.txt", "r") as f:
    instructions = f.read().splitlines()

directions = [direction for direction in instructions[0]]
instructions = {i[:3]: {"L": i[7:10], "R": i[12:15]} for i in instructions[2:]}

next_location = "AAA"
end_location = "ZZZ"
p1_num_iterations = 0

def get_next_location(directions, instructions, num_iterations, next_location):
    direction = directions[num_iterations % len(directions)]
    next_location = instructions[next_location][direction]
    num_iterations += 1
    return next_location, num_iterations

while next_location != end_location:
    next_location, p1_num_iterations = get_next_location(
        directions, instructions, p1_num_iterations, next_location
    )

# part 2
next_locations = [k for k in instructions.keys() if k.endswith("A")]

num_iterations_list = []

# for each location ending with A, find num_iterations to a path ending in Z
# then find the least common multiple of the list of num_iterations
for next_location in next_locations:
    num_iterations = 0

    while not next_location.endswith("Z"):
        next_location, num_iterations = get_next_location(
            directions, instructions, num_iterations, next_location
        )

    num_iterations_list.append(num_iterations)


def greatest_common_denominator(a, b):
    while b:
        a, b = b, a%b
    return a

def least_common_multiple(a, b):
    return a*b // greatest_common_denominator(a, b)


p2_num_iterations = reduce(
    lambda a, b: least_common_multiple(a, b), num_iterations_list
)
