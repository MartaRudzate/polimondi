from polyforms.grammar import *

# 'ACB.DFE.DFE.AC.',[['C.','F.','F.','B.'],['B.','E.','E.','C.']]

def test_derive_SEQ_4_3_A():
    # Example usage:
    axiom = 'acb[S1]dfe[S2]dfe[S3]ac[S4]'
    rule0 = {'S1':'c[T1]', 'S2':'f[T2]', 'S3':'f[T3]', 'S4':'b[T4]',
            'T1':'b[S1]', 'T2':'e[S2]', 'T3':'e[S3]', 'T4':'c[S4]'}
    g = Grammar(axiom, [rule0])
    assert g.derive([]) == 'ACBDFEDFEAC'
    assert g.derive([0]) == 'ACBCDFEFDFEFACB'

