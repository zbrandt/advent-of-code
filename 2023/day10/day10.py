import sys
import re
from rich import print
from rich.console import Console

pipes = {
    '|' : [[-1, 0], [ 1,  0], 'vertical pipe'],
    '-' : [[ 0,-1], [ 0,  1], 'horizontal pipe'],
    'L' : [[-1, 0], [ 0,  1], '90-degree bend NE'],
    'J' : [[-1, 0], [ 0, -1], '90-degree bend NW'],
    '7' : [[ 1, 0], [ 0, -1], '90-degree bend SW'],
    'F' : [[ 1, 0], [ 0,  1], '90-degree bend SE'],
    '.' : [[ 0, 0], [ 0,  0], 'ground'],
    'S' : [[ 0, 0], [ 0,  0], 'starting position'],
}
directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
loop_pieces = {}

def key(pos) -> str:
    return f'R{pos[0]}C{pos[1]}'

def loop_length(starting, prev, pos, length) -> int:
    global loop_pieces
    loop_pieces = {}
    loop_chain = []
    loop_pieces[key(pos)] = 1
    loop_chain.append(pos)
    while pos != starting:
        ch = grid[pos[0]][pos[1]]
        pipe = pipes[ch]
        a = [x+y for x,y in zip(pos, pipe[0])]
        b = [x+y for x,y in zip(pos, pipe[1])]
        #print (f'loop_length({starting}, {prev}, {pos}, {length}) {ch=} {pipe[2]} {a=} {b=}')
        if a == prev:
            prev,pos = pos,b
        elif b == prev:
            prev,pos = pos,a
        else:
            #print (f'pipe \"{ch}\" at {pos=} does not connect to {prev=}')
            assert prev == starting
            return 0
        loop_pieces[key(pos)] = 1
        loop_chain.append(pos)
        length += 1
    print (f'loop_length: back to start {length=} {len(loop_pieces)=} {len(loop_chain)=}')
    assert len(loop_chain) == length
    first = loop_chain[0]
    last = loop_chain[-2]
    start_old = grid[starting[0]][starting[1]]
    start_new = start_old
    if first[0] == last[0]:
        start_new = '-'
    elif first[1] == last[1]:
        start_new = '|'
    elif first[0] == starting[0]:
        if first[1] > starting[1]:
            if last[0] > starting[0]:
                start_new = 'F' 
            else:
                start_new = 'L'
        else:
            if last[0] > starting[0]:
                start_new = '7' 
            else:
                start_new = 'J'
    elif last[0] == starting[0]:
        if last[1] > starting [1]:
            if first[0] > starting[0]:
                start_new = 'F'
            else:
                start_new = 'L'
        else:
            if first[0] > starting[0]:
                start_new = '7'
            else:
                start_new = 'J'
    else:
        assert False
    #print (f'{start_old=} {start_new=}')
    grid[starting[0]][starting[1]] = start_new

    return length

console = Console()
console.rule("[bold red]Original ")

grid = []
starting = []
for line in sys.stdin:
    row = ['.'] + list(line.strip()) + ['.']
    if not grid:
        grid.append(list('.' * len(row)))
    if 'S' in row:
        starting = [len(grid), row.index('S')]
    grid.append(row)
grid.append(list('.' * len(grid[0])))

print (f'{'\n'.join([''.join(row) for row in grid])}')
print (f'{starting=}')

console.rule("[bold red]Start Replaced ")

max_loop = 0
for dir in directions:
    pos = [x+y for x,y in zip(starting, dir)]
    ll = loop_length (starting, starting, pos, 1)
    if ll > max_loop:
        max_loop = ll
        max_loop_pieces = loop_pieces

# pylint: disable=C0200

for row in range(len(grid)):
    for col in range(len(grid[0])):
        if key([row,col]) not in max_loop_pieces:
            grid[row][col] = '.'

print (f'{'\n'.join([''.join(row) for row in grid])}')

console.rule("[bold red]Smooth Version")

inside = False
from_top = False
from_bottom = False
inside_total = 0
for row in range(len(grid)):
    for col in range(len(grid[0])):
        ch = grid[row][col]
        if ch == '.':
            grid[row][col] = ('O', 'I')[inside]
            inside_total += inside
        if ch == '|':
            inside = not inside
        if ch == 'F':
            from_bottom = True
        elif ch == 'L':
            from_top = True
        elif ch == '7':
            if from_top:
                inside = not inside
            from_top = False
            from_bottom = False
        elif ch == 'J':
            if from_bottom:
                inside = not inside
            from_top = False
            from_bottom = False
        if ch in '-|F7LJ':
            grid[row][col] = '\u2501\u2503\u250f\u2513\u2517\u251B'['-|F7LJ'.index(ch)]

grid_str = f'{'\n'.join([''.join(row) for row in grid])}'
grid_str = re.sub(r'I', '[bold black on bright_green]I[/]', grid_str)
grid_str = re.sub(r'O', '[bold black on bright_cyan]O[/]', grid_str)
print (grid_str)

print (f'{max_loop=} farthest={max_loop//2}')
print (f'{inside_total=}')

