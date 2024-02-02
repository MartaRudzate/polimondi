from polyforms.polyiamond import Polyiamond
from polyforms.polyiamond import get_minimal_bounding_sizes
from polyforms.point_tg import *
from polyforms.perfect_seq import PerfectSeq

def test_bounding_hexagon():
    p1 = Polyiamond([(5, 'A'), (4, 'C'), (3, 'E'), (2, 'D'), (1, 'F')])
    p1.setup()
    result = p1.get_bounding_hexagon()
    assert result == (-4, 0, -5, 1, 0, 5)

def test_bounding_box():
    p1 = Polyiamond([(5,'A'), (4,'C'), (3,'E'), (2,'D'), (1,'F')])
    p1.setup()
    bounds = p1.get_bounding_sizes()
    # print('bounds = {}'.format(bounds))
    assert bounds == (4, 6, 5)

def test_direction_counts():
    p1 = Polyiamond([(5, 'A'), (4, 'C'), (3, 'E'), (2, 'D'), (1, 'F')])
    p1.setup()
    counts = p1.get_direction_counts()
    # print('bounds = {}'.format(bounds))
    assert counts == (7, 3, 5)

def test_is_inside3():
    p1 = Polyiamond([(5, 'A'), (4, 'C'), (3, 'E'), (2, 'D'), (1, 'F')])
    # p1.setup()
    assert not p1.is_inside(PointTg(0, 0, 0))
    assert not p1.is_inside(AA)
    assert not p1.is_inside(BB)
    assert not p1.is_inside(CC)
    assert not p1.is_inside(AA + BB)
    assert p1.is_inside(2*AA + BB)
    assert p1.is_inside(2*AA + 2*BB)
    assert p1.is_inside(3*AA + BB)
    assert not p1.is_inside(5*AA)
    assert not p1.is_inside(4*AA + BB)


def test_winding_number():
    p1 = Polyiamond([(5, 'A'), (4, 'C'), (3, 'E'), (2, 'D'), (1, 'F')])
    p1.setup()
    assert p1.winding_number(AA + BB) == 0
    assert p1.winding_number(2*AA + BB) == -1
    assert p1.winding_number(AA + 2*BB) == 0

def test_perimeter_points():
    p1 = Polyiamond([(5, 'A'), (4, 'C'), (3, 'E'), (2, 'D'), (1, 'F')])
    all_points = p1.list_perimeter()
    for pt in all_points:
        assert not p1.is_inside(pt)

def test_long_perimeter_points():
    polyiamonds = ['ACACACACAEAEAEAEAECECECECEAECECECECECECECACAEACAEAC',
                   'ACECECEAEAEAEAEACACACACECEAECECECACACECACACACECACAE',
                   'ABABABCEDEDEDEDEDEFEFAC',
                   'ACEDFEFEFBCBCBFBCBCBDCB']
    for pp in polyiamonds:
        sides = list(zip(range(len(pp), 0, -1), list(pp)))
        pmond = Polyiamond(sides)
        all_points = pmond.list_perimeter()
        for pt in all_points:
            #if pmond.is_inside(pt):
            #    print('pp = {}, pt = {}'.format(pp, pt))
            assert not pmond.is_inside(pt)

def test_large_polygon():
    pp = 'ACACACACAEAEAEAEAECECECECEAECECECECECECECACAEACAEAC'
    pt = PointTg(51, -3, -48)
    pmond = Polyiamond(list(zip(range(len(pp), 0, -1), list(pp))))
    assert not pmond.is_inside(pt)


def test_get_min_bounding_box():
    perfect_nine_dir = ['ABFDEDCDC', 'ACECEAEAC', 'ACEDEABAC']
    perfect_nine_poly = [Polyiamond(list(zip(range(len(pp), 0, -1), list(pp)))) for pp in perfect_nine_dir]
    sublist = get_minimal_bounding_sizes(perfect_nine_poly)
    sublist_codes = [''.join([t[1] for t in poly.sides]) for poly in sublist]
    assert sublist_codes == ['ACECEAEAC']

def test_polyiamond_isvalid():
    seq0 = 'ACBACBDFEDFEDFEDFEACBAC'
    p0 = Polyiamond(list(zip(range(len(seq0), 0, -1), list(seq0))))
    assert p0.is_valid()

    seq1 = 'ACBABCBDFEDFDFEDFEDEFEACBFCFC'
    p1 = Polyiamond(list(zip(range(len(seq1), 0, -1), list(seq1))))
    assert not p1.is_valid()

    seq2 = 'ACBACBACBDFEDFDEFEDFEDFEDFEACBACFBC'
    p2= Polyiamond(list(zip(range(len(seq2), 0, -1), list(seq2))))
    assert not p2.is_valid()


def test_polyseq6_isvalid():
    perfectSeq = PerfectSeq()
    pSequence = perfectSeq.pseq['SEQ_6_5_B']
    for n in range(0, 6):
        p = Polyiamond(pSequence.get(n))
        assert p.is_valid()

def test_list_inside():
    pp = Polyiamond('ACEDF')
    result = pp.list_inside()
    assert len(result) == 18

def test_list_triangles():
    # pp = Polyiamond('ACDCEAEACAEAECEAEAC')
    pp = Polyiamond('ACEDF')
    area = pp.get_area()
    triangles = pp.list_triangles()
    assert len(triangles) == area