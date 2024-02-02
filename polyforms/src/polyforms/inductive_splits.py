from .point_tg import *
import requests

# This class is responsible for finding splits of existing polyiamonds
# into fragments, where sides in the fragments satisfy some properties
# that make polyiamond inductive constructions possible.

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

files2 = [
    'acute_9.txt',
    'acute_27.txt',
    'acute_29.txt',
    'acute_33.txt',
    'acute_35.txt',
    'acute_39.txt',
    'acute_41.txt',
    'acute_45.txt',
    'acute_47.txt',
    'acute_51.txt',
    'acute_53.txt',

]

class InductiveSplits:

    def __init__(self, source):
        base_url = 'http://www.dudajevagatve.lv/static/polimondi/'
        self.url = base_url + source


    @staticmethod
    def p(arg):
        all_chars = list(arg)
        result = PointTg(0,0,0)
        for ch in all_chars:
            result += DIRECTIONS[ch]
        return result

    @staticmethod
    def g(arg):
        all_chars = list(arg)
        n = len(arg)
        result = PointTg(0,0,0)
        for idx, ch in enumerate(all_chars):
            result += (n-idx) * DIRECTIONS[ch]
        return result


    def read_list(self):
        response = requests.get(self.url)
        response.raise_for_status()  # Ensure we got a valid response
        return response.text.splitlines()







