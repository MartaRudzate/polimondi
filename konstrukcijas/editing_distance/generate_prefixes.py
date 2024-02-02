def generate_strings(n):
    if n <= 0:
        return []

    # letters = ['A', 'C', 'E']
    letters = ['A', 'B', 'C', 'D', 'E', 'F']
    opp_letters = {'A': 'D', 'B': 'E', 'C': 'F', 'D': 'A', 'E': 'B', 'F': 'C'}

    results = []

    def dfs(current_string):
        if len(current_string) == n:
            results.append(current_string)
            return
        for letter in letters:
            if not current_string or (current_string[-1] != letter and opp_letters[current_string[-1]] != letter):
                dfs(current_string + letter)

    dfs('')
    results = list(filter(lambda x: x[0:2] in ['AB', 'AC'], results))
    return sorted(results)




def main():
    LL = [231066, 1149921, 1322751, 431525, 561253, 1038368, 1742350, 1133745, 792906, 262534, 935755, 1292195, 399366, 503442, 999463, 1331226, 719466, 1351249, 468769, 688898, 345863, 1419059, 1930196, 281643, 1230568, 1873405, 1368990, 864119, 182422, 1693176, 1320225, 293132, 700911, 1682889, 1732279, 440139, 658194, 1139313, 1802006, 1308603, 0, 1194545, 600358, 0, 0, 0, 778634, 0, 565124, 748974, 1394342, 903922, 615710, 1236718, 1019789, 872725, 0, 0, 1347854, 1607984, 1000243, 532220, 1427837, 1482052, 579290, 1343745, 1403015, 815835, 845800, 1171081, 1619215, 1076982, 1254196, 0, 0, 1516904, 902088, 910160, 486532, 1362967, 577150, 1157715, 570263, 719828, 482524, 733862, 1944500, 1703932, 1173485, 1776782, 1319877, 766000, 798047, 832915, 158099, 842718, 619982, 1205461, 1472335, 356900, 380995, 645330, 1573482, 1522188, 41411, 934483, 1109052, 477647, 0, 0, 592702, 0, 0, 0, 0, 0, 457783, 739348, 1059446, 740458, 213720, 309471, 383461, 214877, 0, 0, 0, 0]
    shortened = []
    for i in range(0, len(LL)//4):
        elt = LL[4*i] + LL[4*i+1] + LL[4*i+2] + LL[4*i+3]
        shortened.append(elt)
    print(len(LL))
    print(len(shortened))
    print(shortened)



if __name__ == '__main__':
    main()

    # # Example usage:
    # n = 5
    # print(generate_strings(n))