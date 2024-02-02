import pytest
from polyforms.geom_utilities import *

def test_get_distance():
    # Example usage:
    str1 = "abcdef"
    str2 = "acbcf"
    lcs = longest_common_subsequence(str1, str2)
    print(lcs)  # Output: 'abcf'
    # assert 12 == 12