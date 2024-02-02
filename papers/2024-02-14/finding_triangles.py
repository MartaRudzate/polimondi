def main():
    for n in range(27, 500):
        if n % 6 not in [3, 5]:
            continue
        the_third = n * (n + 1) // 6
        for i in range(3, n):
            if i % 2 != 0:
                continue
            for j in range(2, i):
                if j % 2 != 1:
                    continue
                for k in range(1, j):
                    if k % 2 != 0:
                        continue
                    countA = ((n - j) // 2) * ((n + j + 2) // 2) + ((2 + k) // 2) * (k // 2)
                    # if n == 35 and i == 30 and j == 23 and k == 10:
                    #    print(f'the_third = {the_third}, countA = {countA}')
                    if countA != the_third:
                        continue
                    countE = ((i - k) // 2) * ((i + k + 2) // 2)
                    if countE != the_third:
                        continue
                    print(f'n={n}, ({i},{j},{k})')

if __name__ == '__main__':
    main()