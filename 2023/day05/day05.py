import sys

class Map:
    def __init__(self):
        self.name:str = None
        self.mappings:[int] = []

        while True:
            line = input()
            category,_,_ = line.partition(':')
            if category:
                x = category.split()
                if x[1] != 'map':
                    assert f'expected map in {category=}'
                self.name = x[0]
                print (f'found map {self.name=}')
                break

        while True:
            try:
                line = input()
            except EOFError:
                return
            nums = list(map(int,line.split()))
            if len(nums) < 3:
                self.mappings = sorted(self.mappings, key = lambda x: x[1])
                print (self.mappings)
                return
            self.mappings.append(nums)

    def domap(self, x) -> int:
        for mapping in self.mappings:
            if x >= mapping[1] and x < mapping[1] + mapping[2]:
                return x + mapping[0] - mapping[1]
        return x

    def map_ranges(self, range_list) -> list[list[int, int]]:
        mapped_ranges = []
        for r in range_list:
            mapped_range = [self.domap(x) for x in r]
            mapped_ranges.append(mapped_range)
        return mapped_ranges

    def first_subrange(self, subrange) -> [int]:
        #print (f'first_subrange({subrange=})')
        if subrange[0] < self.mappings[0][1]:
            #print (f'first_subrange leading')
            if subrange[1] < self.mappings[0][1]:
                #print (f'no overlap')
                return subrange
            else:
                for m in self.mappings:
                    if subrange[1] >= m[1]:
                        return [subrange[0], m[1]-1]
                return subrange
        else:
            for m in self.mappings:
                #print (f'check mapping {m}')
                if subrange[0] >= m[1] and subrange[0] < m[1] + m[2]:
                    if subrange[1] < m[1] + m[2]:
                        #print (f'fits in mapping {m}')
                        return subrange
                    else:
                        #print (f'partial fits in mapping {m}')
                        return [subrange[0], m[1] + m[2] - 1]
        
        #print (f'first_subrange no overlap trailing')
        return subrange
            
    def get_subranges(self, span):
        #print (f'get_subranges({span=})')
        subranges = []
        pos = span[0]
        while True:
            subrange = self.first_subrange([pos, span[1]])
            pos = subrange[1] + 1
            subranges.append(subrange)
            if pos > span[1]:
                break
        return subranges
        
    def __str__(self):
        return f'Map {self.name}:\n' + '\n'.join([f'  [{x[0]:13,}, {x[1]:13,}, {x[2]:13,}]' for x in self.mappings])

class Almanac:
    def __init__(self):
        self.seeds:list[int] = []
        self.ranges:list[int] = []
        self.locations:list[int] = []
        self.min_location2:int = 0
        self.maps:list[Map] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            category,_,value = line.partition(':')
            if category == 'seeds':
                self.seeds = list(map(int, value.split()))
                self.ranges = [[self.seeds[i], self.seeds[i]+self.seeds[i+1]-1] for i in range(0,len(self.seeds),2)]
                break

        print (f'{self.seeds=}')
        print (f'{self.ranges=}')

        print (f'')
        for _ in range(7):
            self.maps.append(Map())

        for m in self.maps:
            print (m)

        for x in self.seeds:
            print (f'seed {x}', end='')
            for m in self.maps:
                x = m.domap(x)
                print (f' --> {x}', end='')
            print ('')
            self.locations.append(x)

        print ('2' * 40)

        for m in self.maps:
            subranges = []
            print (f'  map {m.name}: ranges: {self.ranges}')
            for r in self.ranges:
                print (f'  map {m.name}: {r} --> ', end='', flush=True)
                sr = m.get_subranges(r)
                print (f'{sr}', flush=True)
                subranges.extend(sr)
            new_ranges = m.map_ranges(subranges)
            print (f'map_ranges {m.name}: {subranges} --> {new_ranges}')
            self.ranges = new_ranges

        self.min_location2 = min([min(x) for x in self.ranges])
 
a:Almanac = Almanac()
print (f'min location  = {min(a.locations)}')
print (f'min location2 = {a.min_location2}')