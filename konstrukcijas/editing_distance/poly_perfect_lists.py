import sys
from polyforms.n_gon import NGonProblem
from polyforms.n_gon import FileWriter
from polyforms.n_gon import Format
from polyforms.backtrackk import Backtrackk

def main(n):
    q = NGonProblem(n, list(range(n, 0, -1)), "", Format.COMPACT, FileWriter(f'perfect_{n}.txt'))
    b = Backtrackk(q)
    while b.attempt(0):
        q.display()
    print(f'Found {q.solution_count} polyiamonds')


# This file is meant to write all perfect polyiamonds to a file 'perfect_nn.txt'
if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)
