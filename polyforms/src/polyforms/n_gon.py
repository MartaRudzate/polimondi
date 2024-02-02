import math
import itertools
import copy
from enum import Enum

from .backtrackk import *
from .point_tg import *

class Format(Enum):
    DESCARTES = 'descartes'
    LETTERS = 'letters'
    COMPACT = 'compact'

class FileWriter:
    def __init__(self, filename):
        self.filename = filename
        if self.filename != '__list__':
            self.file = open(filename, 'w')

    def write(self, text):
        if self.filename != '__list__':
            print(text, file=self.file)

    def close(self):
        if self.filename != '__list__':
            self.file.close()

class NGonProblem:

    def __init__(self, n, perm, prefix, format, file_writer):
        print("creating NGonProblem({},{})".format(n,perm))
        self.N = n
        self.directions = []
        self.perm = perm
        self.format = format
        self.file_writer = file_writer
        self.prefix = prefix

        # Record the min/max area; and the min/max count of acute angles 
        self.minArea = n**4
        self.maxArea = 0
        self.minAcute = n
        self.maxAcute = 0
        # self.updateExtremes = False
        self.all_results = []

        #self.outfile = open("poly_{}_{}.txt".format(n, self.perm), "w")

        # Uzkrāj polimonda virsotnes
        self.vertices = [PointTg(0, 0, 0)]
        # Punkti, kurus šķērso polimonda perimetrs.
        self.points = set()
        # aritmētisko progresiju summas. Ja n == 5, tad  series_sums = [0, 1, 3, 6, 10, 15]
        perm_rev = copy.deepcopy(self.perm)
        perm_rev.reverse()
        perm_rev.insert(0,0)
        self.series_sums  = list(itertools.accumulate(perm_rev))
        # līdz šim atrasto atrisinājumu skaits
        self.solution_count = 0


    # def reset(self):
    #     self.directions = []
    #     self.vertices = [PointTg(0, 0, 0)]
    #     self.points = set()




    # Funkcijas, lai ielūkotos backtracking objekta iekšējā stāvoklī
    def debug_state(self, prefix):
        print('{}, directions = {}'.format(prefix, self.directions))

    def debug_full(self, prefix):
        print('{}: directions={}, vertices={}, points={}'.format(prefix, self.directions, self.vertices, self.points))


    # Pielabo datu struktūras, pievienojot (status=1) vai atceļot (status=0) gājienu.
    def setPosition(self, move, status):
        # self.debug_full(prefix='({},{})'.format(move,status))
        # sideLength = self.N - len(self.directions) + 1
        sideLength = self.perm[len(self.directions) - 1]

        if status == 1:
            nextSide = sideLength*DIRECTIONS[move]
            nextVertex = self.vertices[-1] + nextSide
            for i in range(1, sideLength+1):
                currPoint = self.vertices[-1] + i*DIRECTIONS[move]
                self.points.add(currPoint)
            self.vertices.append(nextVertex)

        if status == 0:
            prevVertext = self.vertices.pop()
            for i in range(0, sideLength - 1):
                currPoint = prevVertext - i*DIRECTIONS[move]
                if move == 'A' and status == 0 and self.directions == []:
                    print('Feeling sad; points = {}, removing {}'.format(self.points, currPoint))
                self.points.remove(currPoint)
                if move == 'A' and status == 0 and self.directions == []:
                    print('Feeling sadder; points = {}'.format(self.points))

    # Vai nekrustojas ar agrāk novilktām malām
    def check1(self, level, move):
        for i in range(1, self.N - level + 1):
            currPoint = self.vertices[-1] + i * DIRECTIONS[move]
            if currPoint in self.points:
                return False
        return True

    # Vai pietiek atlikušo malu garumu, lai atgrieztos
    def check2(self, level, move):
        nextSide = (self.N - level) * DIRECTIONS[move]
        nextVertex = self.vertices[-1] + nextSide
        # print('check2(level={}, move={}, nextSide={}, nextVertex={}, abs={}, sums={})'.format(level, move, nextSide, nextVertex, nextVertex.abs(), self.series_sums[self.N - level - 1]))
        return nextVertex.abs() <= self.series_sums[self.N - level - 1]

    # Pēdējā/īsākā polimonda mala nedrīkst būt horizontāla, jo pirmā ir horizontāls.
    def check3(self, level, move):
        if level == self.N - 1 and (move == 'A' or move == 'D'):
            return False
        return True

    # Vai drīkst vilkt malu norādītajā virzienā?
    def valid(self, level, move):
        c1 = self.check1(level, move)
        c2 = self.check2(level, move)
        c3 = self.check3(level, move)
        # print('valid({},{}) = {} = {} and {} and {}'.format(level, move, c1 and c2 and c3, c1, c2, c3))
        return c1 and c2 and c3

    # Vai polimonds ir pabeigts?
    def done(self, level):
        if level == self.N - 1:
            self.solution_count += 1
            return True
        else:
            return False

    # Pievienojam esošo gājienu
    def record(self, level, move):
        self.directions.append(move)
        self.setPosition(move, 1)


    # Parāpjamies atpakaļ, ja apakškokā zem šī gājiena visur bija strupceļš.
    def undo(self, level, move):
        move = self.directions.pop()
        self.setPosition(move, 0)
        # pārejot uz citu apakškoku, "initValues" vērtības nepielieto, bet sāk no 0.
        # self.initValues = []

    # Kompakti izvada vienu atrisinājumu kā daudzstūri, ja polimonada zīmēšana pabeigta: done(self,level)==True
    def display(self):
        if self.file_writer == '__list__':
            if self.format == Format.LETTERS:
                self.all_results.append(self.directions)
            elif self.format == Format.DESCARTES:
                self.all_results.append(PointTg.convert_divainas_dekarta(self.directions))
            elif self.format == Format.COMPACT:
                self.all_results.append("".join(self.directions))

        else:
            if self.file_writer is None:
                out_func = print
            else:
                out_func = self.file_writer.write
            # if self.updateExtremes:
            #     polyiamond_area = PointTg.get_signed_area(self.directions)
            #     (a60, a120, a240, a300) = PointTg.count_angles(self.directions)
            #     if self.maxArea < abs(polyiamond_area):
            #         self.maxArea = abs(polyiamond_area)
            #     if self.minArea > abs(polyiamond_area):
            #         self.minArea = abs(polyiamond_area)
            #     if self.minAcute > a60 + a300:
            #         self.minAcute = a60 + a300
            #     if self.maxAcute < a60 + a300:
            #         self.maxAcute = a60 + a300
            #
            #     if self.format == Format.LETTERS:
            #         out_func(self.directions, end='')
            #         # out_func(', #S = {}, acute={}, obtuse={}'.format(polyiamond_area, a60+a300, a120+a240))
            #     elif self.format == Format.DESCARTES:
            #         out_func(PointTg.convert_divainas_dekarta(self.directions), end='')
            #         # out_func(', #S = {}, acute={}, obtuse={}'.format(polyiamond_area, a60+a300, a120+a240))
            #     else:
            #         # silent mode
            #         return

            if self.format == Format.LETTERS:
                out_func(self.directions)
            elif self.format == Format.DESCARTES:
                out_func(PointTg.convert_divainas_dekarta(self.directions))
            elif self.format == Format.COMPACT:
                out_func("".join(self.directions))



    # Atgriež iteratoru ar iespējamiem gājieniem, ja iepriekšējās malas virziens bija "direction"
    # Ja direction=='0', tad drīkst braukt tikai pa labi.
    # Ja direction=='1', tad drīkst pagriezties pa kreisi šaurā 60 grādu leņķī ('C') vai 120 grādu leņķī ('B')
    # Visos citos gadījumos nākamie gājieni ir četri (nevar sakrist ar "direction" vai tam pretējo).
    def moves(self, level):
        if (level < len(self.prefix)):
            return self.prefix[level]
        else:
            if level == 0:
                direction = '0'
            elif level == 1:
                direction = '1'
            else:
                direction = self.directions[level-1]
            return PointTg.NEXT_MOVES[direction]


 

# def findFirstSolution(n):
#     q = NGonProblem(n, list(range(1,n+1)))
#     b = Backtrackk(q)
#     if b.attempt(0):
#         q.display(Format.COMPACT)

def print_all_solutions(perm, format, file_name):
    if file_name == '__list__':
        file_writer = FileWriter(file_name)
        out_func = file_writer.write
    elif file_name != '':
        file_writer = FileWriter(file_name)
        out_func = file_writer.write
    else:
        file_writer = None
        out_func = print
    q = NGonProblem(len(perm), perm, "", format, file_writer)
    b = Backtrackk(q)
    # total = 0
    try:
        while b.attempt(0):
            q.display()
            # q.reset()
            # total += 1
        #out_func('Solutions found: {} '.format(q.solution_count))
        #out_func('Area belongs to: [{},{}]'.format(q.minArea, q.maxArea))
        #out_func('Acute angles belong to: [{}, {}]'.format(q.minAcute, q.maxAcute))
    finally:
        if file_name != '':
            file_writer.close()


def get_all_solutions(perm, format):
    q = NGonProblem(len(perm), perm, "", format, '__list__')
    b = Backtrackk(q)
    while b.attempt(0):
        q.display()
        # q.reset()
    return q.all_results
