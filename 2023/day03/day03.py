import sys

class Grid:
    def __init__(self, lines:[str]):
        width = len(lines[0])
        header_footer = list('.' * (width + 2))
        self.grid: list[list[str]] = []
        self.grid.append(header_footer)
        for line in lines:
            self.grid.append(list('.' + line + '.'))
        self.grid.append(header_footer)
        self.stars = {}
        self.near_gear = []
    
    def is_sym(self, row, col) -> bool:
        ch = g.grid[row][col]
        addr = f'R{row}C{col}'
        if ch == '*':
            self.near_gear.append(addr)
        val = ch != '.' and not ch.isdigit()
        #if val:
        #    print (f'found sym at grid[{row}][{col}] "{g.grid[row][col]}"')
        return val
    
    def is_part(self, row, col) -> bool:
        val = self.is_sym(row-1, col) or self.is_sym(row, col) or self.is_sym(row+1, col)
        if val:
            print (f'is_part: found sym near grid[{row}][{col}] "{g.grid[row][col]}"')
        return val
    
    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)


input_lines:list[str] = sys.stdin.read().split()
g:Grid = Grid(input_lines)
in_number:bool = False
is_part:bool = False
part_number:int = 0
part_sum:int = 0
for row in range(1,len(g.grid)-1):
    for col in range(1,len(g.grid[0])-1):
        #print (f'loop grid[{row}][{col}] g="{g.grid[row][col]}" {in_number=} {is_part=} {part_number=}')
        ch = g.grid[row][col]
        was_part = is_part
        if in_number:
            is_part |= g.is_part(row, col)
            if ch.isdigit():
                in_number = True
                part_number = part_number * 10 + int(ch)
            else:
                if is_part:
                    print (f'found part {part_number} gear={g.near_gear}')
                    part_sum += part_number
                    if len(g.near_gear) == 1:
                        g.stars[g.near_gear[0]] = g.stars.get(g.near_gear[0], []) + [part_number]
                part_number = 0
                g.near_gear = []
                in_number = False
                is_part = False
        elif ch.isdigit():
            in_number = True
            g.near_gear = []
            is_part = g.is_part(row, col-1) or g.is_part(row, col)
            part_number = int(ch)
        else:
            in_number = False
            is_part = False
            pass
        if not was_part and is_part:
            #print (f'found part at grid[{row}][{col}] "{g.grid[row][col]}"')
            pass

gears = [x for x in g.stars.values() if len(x) == 2]
sum_gear_ratios = sum([x[0]*x[1] for x in gears])
print (g.stars)
print (gears)

print (f'{str(g)}')
print (f'{part_sum = }')
print (f'{sum_gear_ratios = }')
