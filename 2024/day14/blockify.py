# pylint: disable=line-too-long, missing-function-docstring, missing-module-docstring

from collections import defaultdict
from collections.abc import Callable
from typing import Any

def blockify(grid:list[list], fx:Callable[[Any],bool]=bool) -> list[list[int]]:
    """return a bitmap using unicode block characters 

    Args:
        grid (list[list]): input values as a list of lists
        fx (Callable, optional): boolean function applied to each cell in grid. Defaults to bool.

    Returns:
        list[list[int]]: grid with 2x2 bitmap unicode characters
    """

    blocks = {
        0: ('\u0020', 'SPACE'),
        1: ('\u2598', 'QUADRANT UPPER LEFT'),
        2: ('\u259D', 'QUADRANT UPPER RIGHT'),
        3: ('\u2580', 'UPPER HALF BLOCK'),

        4: ('\u2596', 'QUADRANT LOWER LEFT'),
        5: ('\u258C', 'LEFT HALF BLOCK'),
        6: ('\u259E', 'QUADRANT UPPER RIGHT AND LOWER LEFT'),
        7: ('\u259B', 'QUADRANT UPPER LEFT AND UPPER RIGHT AND LOWER LEFT'),

        8: ('\u2597', 'QUADRANT LOWER RIGHT'),
        9: ('\u259A', 'QUADRANT UPPER LEFT AND LOWER RIGHT'),
        10: ('\u2590', 'RIGHT HALF BLOCK'),
        11: ('\u259C', 'QUADRANT UPPER LEFT AND UPPER RIGHT AND LOWER RIGHT'),

        12: ('\u2584', 'LOWER HALF BLOCK'),
        13: ('\u2599', 'QUADRANT UPPER LEFT AND LOWER LEFT AND LOWER RIGHT'),
        14: ('\u259F', 'QUADRANT UPPER RIGHT AND LOWER LEFT AND LOWER RIGHT'),
        15: ('\u2588', 'FULL BLOCK'),
        }

    quad_ops = [(0, 0, 0), (1, 0, 1), (0, 1, 2), (1, 1, 3)]

    d = defaultdict(bool, {(x,y): fx(ch) for y,row in enumerate(grid) for x,ch in enumerate(row)})
    return [[blocks[sum(d[x+qo[0], y+qo[1]] << qo[2] \
                        for qo in quad_ops)][0] \
                            for x in range(0,len(grid[0]),2)] \
                                for y in range(0,len(grid),2)]
