with open("input.txt", "r") as f:
    instructions = f.read().splitlines()

directions = [direction for direction in instructions[0]]
instructions = {i[:3]: {"L": i[7:10], "R": i[12:15]} for i in instructions[2:]}

next_location = "AAA"
end_location = "ZZZ"
num_iterations = 0
reached_end = False

while next_location != end_location:
    options = instructions[next_location]
    direction = directions[num_iterations % len(directions)]
    next_location = options[direction]
    num_iterations += 1
