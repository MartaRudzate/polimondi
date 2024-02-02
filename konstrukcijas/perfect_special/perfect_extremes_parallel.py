import sys

from polyforms.polyiamond import Polyiamond
from multiprocessing import Pool, cpu_count


def f(line, metric):
    p = Polyiamond(line)
    if metric == 'area':
        return p.get_area()
    elif metric == 'diameter':
        return p.diameter()[0]
    elif metric == 'width':
        return p.width()
    elif metric == 'dimension':
        return min(p.get_bounding_sizes())


def process_prefix(ptype, n, metric, prefix):
    # print('XX ptype = {}'.format(ptype))
    # print('XX n = {}'.format(n))
    # print('XX prefix = {}'.format(prefix))
    # print('XX metric = {}'.format(metric))
    print(f"Finding extreme {ptype} {n}-polyiamonds, prefix '{prefix}', order by '{metric}'")
    max_value = 0
    max_array = []
    min_value = 10000000000
    min_array = []
    fileName = f'../editing_distance/{ptype}_{n}_{prefix}.txt'
    with open(fileName, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            val = f(line, metric)
            if val > max_value:
                max_array = []
                max_value = val
            if val == max_value:
                max_array.append(line)
            if val < min_value:
                min_array = []
                min_value = val
            if val == min_value:
                min_array.append(line)

    file1 = open(f'maxall_{ptype}_{n}_{metric}.txt', 'a')
    file2 = open(f'minall_{ptype}_{n}_{metric}.txt', 'a')
    file3 = open(f'maxone_{ptype}_{n}_{metric}.txt', 'a')
    file4 = open(f'minone_{ptype}_{n}_{metric}.txt', 'a')

    for pp in max_array:
        file1.write(f'{pp},{max_value}\n')
    for pp in min_array:
        file2.write(f'{pp},{min_value}\n')
    if len(max_array) > 0:
        pp = max_array[0]
        file3.write(f'{pp},{max_value}\n')
    if len(min_array) > 0:
        pp = min_array[0]
        file4.write(f'{pp},{min_value}\n')

    file1.close()
    file2.close()
    file3.close()
    file4.close()
    return (prefix,len(min_array), min_value, len(max_array), max_value)


def main(ptype, n, metric):

    # prefixes4 = ['ABAB', 'ABAC', 'ABAE', 'ABAF',
    #              'ABCA', 'ABCB', 'ABCD', 'ABCE',
    #              'ABDB', 'ABDC', 'ABDE', 'ABDF',
    #              'ABFA', 'ABFB', 'ABFD', 'ABFE',
    #              'ACAB', 'ACAC', 'ACAE', 'ACAF',
    #              'ACBA', 'ACBC', 'ACBD', 'ACBF',
    #              'ACDB', 'ACDC', 'ACDE', 'ACDF',
    #              'ACEA', 'ACEC', 'ACED', 'ACEF']

#    prefixes = ['ABABA', 'ABABC', 'ABABD', 'ABABF', 'ABACA', 'ABACB', 'ABACD', 'ABACE', 'ABAEA', 'ABAEC', 'ABAED', 'ABAEF', 'ABAFA', 'ABAFB', 'ABAFD', 'ABAFE',
#                'ABCAB', 'ABCAC', 'ABCAE', 'ABCAF', 'ABCBA', 'ABCBC', 'ABCBD', 'ABCBF', 'ABCDB', 'ABCDC', 'ABCDE', 'ABCDF', 'ABCEA', 'ABCEC', 'ABCED', 'ABCEF',
#                'ABDBA', 'ABDBC', 'ABDBD', 'ABDBF', 'ABDCA', 'ABDCB', 'ABDCD', 'ABDCE', 'ABDEA', 'ABDEC', 'ABDED', 'ABDEF', 'ABDFA', 'ABDFB', 'ABDFD', 'ABDFE',
#                'ABFAB', 'ABFAC', 'ABFAE', 'ABFAF', 'ABFBA', 'ABFBC', 'ABFBD', 'ABFBF', 'ABFDB', 'ABFDC', 'ABFDE', 'ABFDF', 'ABFEA', 'ABFEC', 'ABFED', 'ABFEF']
    prefixes = ['ACABA', 'ACABC', 'ACABD', 'ACABF', 'ACACA', 'ACACB', 'ACACD', 'ACACE', 'ACAEA', 'ACAEC', 'ACAED', 'ACAEF', 'ACAFA', 'ACAFB', 'ACAFD', 'ACAFE',
                'ACBAB', 'ACBAC', 'ACBAE', 'ACBAF', 'ACBCA', 'ACBCB', 'ACBCD', 'ACBCE', 'ACBDB', 'ACBDC', 'ACBDE', 'ACBDF', 'ACBFA', 'ACBFB', 'ACBFD', 'ACBFE',
                'ACDBA', 'ACDBC', 'ACDBD', 'ACDBF', 'ACDCA', 'ACDCB', 'ACDCD', 'ACDCE', 'ACDEA', 'ACDEC', 'ACDED', 'ACDEF', 'ACDFA', 'ACDFB', 'ACDFD', 'ACDFE',
                'ACEAB', 'ACEAC', 'ACEAE', 'ACEAF', 'ACECA', 'ACECB', 'ACECD', 'ACECE', 'ACEDB', 'ACEDC', 'ACEDE', 'ACEDF', 'ACEFA', 'ACEFB', 'ACEFD', 'ACEFE']

    num_processes = min(cpu_count(), len(prefixes))
    with Pool(num_processes) as pool:
        results = pool.starmap(process_prefix, [(ptype, n, metric, prefix) for prefix in prefixes])

    file0 = open(f'mmsummary_{ptype}_{n}_{metric}_F.txt', 'a')
    for result in results:
        csv_string = ','.join(str(item) for item in result)
        file0.write(f'{csv_string}\n')
    file0.close()



# python perfect_extremes_parallel.py perfect 25 area
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python perfect_extremes_parallel.py <poly-type> <n> <metric>")
        sys.exit(1)
    ptype = sys.argv[1]
    n = int(sys.argv[2])
    metric = sys.argv[3]
    if not ptype in ['perfect', 'acute', 'obtuse']:
        print("Poly-type must be 'perfect', 'acute', or 'obtuse'")
        sys.exit(1)
    if not metric in ['area', 'diameter', 'width', 'dimension']:
        print("Metric must be 'area', 'diameter', 'width', or 'dimension'")
        sys.exit(1)

    main(ptype, n, metric)
