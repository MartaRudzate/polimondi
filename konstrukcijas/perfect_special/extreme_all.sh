#!/bin/bash

echo "Processing ${1}-polyiamonds:"

python perfect_extremes_parallel.py perfect "$1" area
python best_prefixes.py perfect "$1" area
python perfect_extremes_parallel.py perfect "$1" diameter
python best_prefixes.py perfect "$1" diameter
python perfect_extremes_parallel.py perfect "$1" dimension
python best_prefixes.py perfect "$1" dimension
python perfect_extremes_parallel.py perfect "$1" width
python best_prefixes.py perfect "$1" width
