import re
import csv
import sys

def smallest_prefixes(filename, colNum):
    try:
        # Using dictionary to store prefixes with the same 3rd column value
        good_values = []
        smallest_value = 10000000000

        # Open and parse the CSV file
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                prefix = row[0]
                current_value = float(row[colNum])

                # Store the prefix in the dictionary
                if current_value < smallest_value - 1E-7:
                    good_values = [prefix]
                    smallest_value = current_value
                elif current_value > smallest_value + 1E-7:
                    continue
                else:
                    good_values.append(prefix)

        # Create a regex pattern to match all prefixes with the smallest third column value
        # regex_pattern = "(" + "|".join(good_values) + ")"
        return good_values
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def largest_prefixes(filename, colNum):
    try:
        # Using dictionary to store prefixes with the same 3rd column value
        good_values = []
        largest_value = 0

        # Open and parse the CSV file
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                prefix = row[0]
                current_value = float(row[colNum])

                # Store the prefix in the dictionary
                if current_value > largest_value + 1E-7:
                    good_values = [prefix]
                    largest_value = current_value
                elif current_value < largest_value - 1E-7:
                    continue
                else:
                    good_values.append(prefix)

        # Create a regex pattern to match all prefixes with the smallest third column value
        # regex_pattern = "(" + "|".join(good_values) + ")"
        return good_values
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def filter_good_prefixes(infile, good_prefixes, outfile):
    pref_len = len(good_prefixes[0])
    try:
        file2 = open(outfile, 'w')
        with open(infile, 'r') as file:
            # Go through each line in the file
            for line in file:
                current_prefix = line[0:pref_len]
                if current_prefix in good_prefixes:
                    file2.write(line)
        file2.close()
    except FileNotFoundError:
        print(f"File '{infile}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# You call the function with the filename
def main(ptype, n, metric):
    min_prefixes = smallest_prefixes(f'mmsummary_{ptype}_{n}_{metric}_F.txt', 2)
    max_prefixes = largest_prefixes(f'mmsummary_{ptype}_{n}_{metric}_F.txt', 4)
    print(f'min_prefixes = {min_prefixes}, max_prefixes = {max_prefixes}')
    filter_good_prefixes(f'minall_{ptype}_{n}_{metric}.txt', min_prefixes, f'minall_{ptype}_{n}_{metric}_F.txt')
    filter_good_prefixes(f'maxall_{ptype}_{n}_{metric}.txt', max_prefixes, f'maxall_{ptype}_{n}_{metric}_F.txt')



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

    #
    # if len(sys.argv) < 2:
    #     print("Usage: python perfect_extremes_parallel.py <poly-type> <n> <metric>")
    #     sys.exit(1)
    # fname = sys.argv[1]
    # main(fname)

