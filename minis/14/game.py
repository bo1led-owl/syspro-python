from typing import List


def readField(filename: str) -> List[List[int]]:
    with open(filename, "r", encoding="utf-8") as f:
        result = list(
            map(lambda line: list(map(lambda c: c == '*', line.strip())), f)
        )
    assert all(map(lambda line: len(line) == len(result), result))
    return result


def countNeighbours(field: List[List[bool]], i: int, j: int) -> int:
    n = len(field)
    row_above = (i - 1) % n
    row_below = (i + 1) % n
    left_col = (j - 1) % n
    right_col = (j + 1) % n

    neighbours = (
        (row_above, left_col),
        (row_above, j),
        (row_above, right_col),
        (i, left_col),
        (i, right_col),
        (row_below, left_col),
        (row_below, j),
        (row_below, right_col),
    )

    result = 0
    for row, col in neighbours:
        result += int(field[row][col])
    return result


def step(field: List[List[bool]]) -> List[List[bool]]:
    result = [[False for i in range(len(field))] for j in range(len(field))]
    for i in range(len(field)):
        for j in range(len(field)):
            neighbours = countNeighbours(field, i, j)

            if field[i][j]:
                should_live = 1 < neighbours < 4
                result[i][j] = should_live
            else:
                should_become_populated = neighbours == 3
                result[i][j] = should_become_populated
    return result
