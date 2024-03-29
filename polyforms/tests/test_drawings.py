import matplotlib.pyplot as plt
import matplotlib.patches as patches
from polyforms.polyiamond import Polyiamond
from polyforms.point_tg import *

STEP = 20
def mul_step(arg):
    return STEP*(arg // STEP)

def test_poly51():
    dir = "ACACACACAEAEAEAEAECECECECEAECECECECECECECACAEACAEAC"
    llen = range(len(dir),0,-1)
    p1 = Polyiamond(list(zip(llen, list(dir))))
    descartes = p1.get_descartes()
    expected = [(0.0, 0.0), (51.0, 0.0), (26.0, 43.30127018922193), (75.0, 43.30127018922193),
                (51.0, 84.87048957087498), (98.0, 84.87048957087498), (75.0, 124.70765814495915),
                (120.0, 124.70765814495915), (98.0, 162.81277591147446), (141.0, 162.81277591147446),
                (120.0, 126.43970895252804), (161.0, 126.43970895252804), (141.0, 91.7986928011505),
                (180.0, 91.7986928011505), (161.0, 58.88972745734183), (198.0, 58.88972745734183),
                (180.0, 27.712812921102035), (215.0, 27.712812921102035), (198.0, -1.7320508075688772),
                (181.5, 26.846787517317598), (165.5, -0.8660254037844386), (150.0, 25.980762113533157), (135.0, 0.0),
                (120.5, 25.11473670974872), (106.5, 0.8660254037844386), (93.0, 24.24871130596428),
                (80.0, 1.7320508075688772), (105.0, 1.7320508075688772), (93.0, -19.05255888325765),
                (81.5, 0.8660254037844386), (70.5, -18.186533479473212), (60.0, 0.0), (50.0, -17.32050807568877),
                (40.5, -0.8660254037844386), (31.5, -16.454482671904334), (23.0, -1.7320508075688772),
                (15.0, -15.588457268119894), (7.5, -2.598076211353316), (0.5, -14.722431864335457),
                (-6.0, -3.4641016151377544), (-12.0, -13.856406460551018), (-17.5, -4.330127018922193),
                (-7.5, -4.330127018922193), (-12.0, 3.4641016151377544), (-4.0, 3.4641016151377544),
                (-7.5, -2.598076211353316), (-1.5, -2.598076211353316), (-4.0, 1.7320508075688772),
                (0.0, 1.7320508075688772), (-1.5, -0.8660254037844386), (0.5, -0.8660254037844386)]

    assert len(descartes) == 51
    for idx,item in enumerate(descartes):
        assert abs(item[0] - expected[idx][0]) < 1e-07
        assert abs(item[1] - expected[idx][1]) < 1e-07