import sys
from polyforms.n_gon import NGonProblem
from polyforms.n_gon import FileWriter
from polyforms.n_gon import Format
from polyforms.backtrackk import Backtrackk
from polyforms.polyiamond import Polyiamond



files = [
    'perfect_5.txt',
    'perfect_7.txt',
    'perfect_9.txt',
    'perfect_11.txt',
    'perfect_13.txt',
    'perfect_15.txt',
    'perfect_17.txt',
    'perfect_19.txt',
    'perfect_21.txt',
    'perfect_23.txt'
]


def f(line, metric):
    p = Polyiamond(line)
    if metric == 'area':
        return p.get_area()
    elif metric == 'diameter':
        return p.diameter()[0]
    elif metric == 'width':
        return p.width()




def main(lower, upper):
    metric = 'area'
    max_array = dict()
    max_value = dict()
    min_array = dict()
    min_value = dict()
    for i in range(lower, upper):
        if not (i % 6 in [3,5]):
            continue
        print(f"Processing {i}")
        max_value[i] = 0
        max_array[i] = []
        min_value[i] = 10000000000
        min_array[i] = []
        fileName = f'../../docs/polimondi/acute_{i}.txt'
        line_count = 0
        with open(fileName, 'r') as file:
            for line in file:
                line = line.rstrip('\n')
                val = f(line, metric)
                if val > max_value[i]:
                    max_array[i] = []
                    max_value[i] = val
                if val == max_value[i]:
                    max_array[i].append(line)
                if val < min_value[i]:
                    min_array[i] = []
                    min_value[i] = val
                if val == min_value[i]:
                    min_array[i].append(line)

        file = open(f'maxacute_{metric}.txt', 'a')
        file.write(f'{i}-polyiamond(s) with max {metric} {max_value[i]}:\n')
        for pp in max_array[i]:
            file.write(f'{pp}\n')
        file.close()

        file = open(f'minacute_{metric}.txt', 'a')
        file.write(f'{i}-polyiamond(s) with min {metric} {min_value[i]}:\n')
        for pp in min_array[i]:
            file.write(f'{pp}\n')
        file.close()

    # for i in range(lower, upper):
    #     print(f'{i}-polyiamond(s) with max {metric} {max_value[i]}:')
    #     for pp in max_array[i]:
    #         print(pp)
    # print()
    # for i in range(lower, upper):
    #     print(f'{i}-polyiamond(s) with min {metric} {min_value[i]}:')
    #     for pp in min_array[i]:
    #         print(pp)



# This file is meant to write all perfect polyiamonds to a file 'perfect_nn.txt'
if __name__ == '__main__':
    lower = int(sys.argv[1])
    upper = int(sys.argv[2])
    main(lower,upper)
