import json
import string
import random
import tqdm

WIDTH = 25
HEIGHT = 100000
NUM_WORDS = HEIGHT * 1.5
MAX_RUNS = 1000


def initGrid():
    grid = [["" for x in range(WIDTH)] for y in range(HEIGHT)]

    return grid


def fillGridWithRandomLetters(grid):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == "":
                grid[y][x] = random.choice(string.ascii_uppercase)

    return grid


def placeHorizontal(grid, gridUsed, word):
    beginAndEnd = []

    placed = False
    runs = 0
    while not placed and runs < MAX_RUNS:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        if x + len(word) < WIDTH:
            if all(
                [
                    grid[y][x + i] == "" or grid[y][x + i] == word[i]
                    for i in range(len(word))
                ]
            ):
                for i in range(len(word)):
                    grid[y][x + i] = word[i]
                    gridUsed[y][x + i] = True

                placed = True

                beginAndEnd = [(y, x), (y, x + len(word) - 1)]

        runs += 1

    return grid, gridUsed, placed, beginAndEnd


def placeVertical(grid, gridUsed, word):
    beginAndEnd = []

    placed = False
    runs = 0
    while not placed and runs < MAX_RUNS:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        if y + len(word) < HEIGHT:
            if all(
                [
                    grid[y + i][x] == "" or grid[y + i][x] == word[i]
                    for i in range(len(word))
                ]
            ):
                for i in range(len(word)):
                    grid[y + i][x] = word[i]
                    gridUsed[y + i][x] = True

                placed = True

                beginAndEnd = [(y, x), (y + len(word) - 1, x)]

        runs += 1

    return grid, gridUsed, placed, beginAndEnd


def placeDiagonalSouthEast(grid, gridUsed, word):
    beginAndEnd = []

    placed = False
    runs = 0
    while not placed and runs < MAX_RUNS:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        if x + len(word) < WIDTH and y + len(word) < HEIGHT:
            if all(
                [
                    grid[y + i][x + i] == "" or grid[y + i][x + i] == word[i]
                    for i in range(len(word))
                ]
            ):
                for i in range(len(word)):
                    grid[y + i][x + i] = word[i]
                    gridUsed[y + i][x + i] = True

                placed = True

                beginAndEnd = [(y, x), (y + len(word) - 1, x + len(word) - 1)]

        runs += 1

    return grid, gridUsed, placed, beginAndEnd


def placeDiagonalSouthWest(grid, gridUsed, word):
    beginAndEnd = []

    placed = False
    runs = 0
    while not placed and runs < MAX_RUNS:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)

        if x - len(word) >= 0 and y + len(word) < HEIGHT:
            if all(
                [
                    grid[y + i][x - i] == "" or grid[y + i][x - i] == word[i]
                    for i in range(len(word))
                ]
            ):
                for i in range(len(word)):
                    grid[y + i][x - i] = word[i]
                    gridUsed[y + i][x - i] = True

                placed = True

                beginAndEnd = [
                    (y, x),
                    (
                        y + len(word) - 1,
                        x - len(word) + 1,
                    ),
                ]

        runs += 1

    return grid, gridUsed, placed, beginAndEnd


def generateWordGrid(wordList):
    grid = initGrid()
    gridUsed = [[False for x in range(WIDTH)] for y in range(HEIGHT)]

    beginAndEndList = {}
    words = []

    # randomize wordList
    random.shuffle(wordList)

    for i in tqdm.tqdm(range(0, len(wordList))):
        word = wordList[i]
        direction = random.choice(["horizontal", "vertical", "diagonal1", "diagonal2"])
        reverse = random.choice([True, False])

        if len(word) > 12 or len(word) < 4:
            continue
        word = word[::-1] if reverse else word

        placed = False
        beginAndEnd = []

        if direction == "horizontal":
            grid, gridUsed, placed, beginAndEnd = placeHorizontal(grid, gridUsed, word)

        if direction == "vertical":
            grid, gridUsed, placed, beginAndEnd = placeVertical(grid, gridUsed, word)

        if direction == "diagonal1":
            grid, gridUsed, placed, beginAndEnd = placeDiagonalSouthEast(
                grid, gridUsed, word
            )

        if direction == "diagonal2":
            grid, gridUsed, placed, beginAndEnd = placeDiagonalSouthWest(
                grid, gridUsed, word
            )

        if placed:
            word = word[::-1] if reverse else word
            stringified = json.dumps(beginAndEnd, separators=(",", ":"))
            beginAndEndList[stringified] = [word, len(words)]
            words.append(stringified)

        if len(words) >= NUM_WORDS:
            break

    grid = fillGridWithRandomLetters(grid)

    return grid, beginAndEndList, words


with open("english_450k.json", "r") as wordList:
    wordlist = json.load(wordList)["words"]

wordlist = [word.upper() for word in wordlist]


grid, beginAndEndList, words = generateWordGrid(wordlist)
print(len(words))

with open("wordgrid.json", "w") as wordGrid:
    json.dump({"grid": grid, "wordsEnds": beginAndEndList, "words": words}, wordGrid)
