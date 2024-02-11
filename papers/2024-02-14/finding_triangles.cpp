#include <iostream>

// find triangles that have a vertex at the bottom
int main() {
    for (int n = 2000; n < 2500; ++n) {
        if (!(n % 6 == 3 || n % 6 == 5)) {
            continue;
        }
        int the_third = n * (n + 1) / 6;
        for (int i = 3; i < n; ++i) {
            if (i % 2 != 0) {
                continue;
            }
            for (int j = 2; j < i; ++j) {
                if (j % 2 != 1) {
                    continue;
                }
                for (int k = 1; k < j; ++k) {
                    if (k % 2 != 0) {
                        continue;
                    }
                    int countA = ((n - j) / 2) * ((n + j + 2) / 2) + ((2 + k) / 2) * (k / 2);
                    if (countA != the_third) {
                        continue;
                    }
                    int countE = ((i - k) / 2) * ((i + k + 2) / 2);
                    if (countE != the_third) {
                        continue;
                    }
                    std::cout << "n=" << n << ", (" << i << "," << j << "," << k << ")\n";
                }
            }
        }
    }
    return 0;
}

// find triangles that have a vertex at the bottom
int main2() {
    for (int n = 2000; n < 2500; ++n) {
        if (!(n % 6 == 3 || n % 6 == 5)) {
            continue;
        }
        int the_third = n * (n + 1) / 6;
        for (int i = 3; i < n; ++i) {
            if (i % 2 != 0) {
                continue;
            }
            for (int j = 2; j < i; ++j) {
                if (j % 2 != 0) {
                    continue;
                }
                for (int k = 1; k < j; ++k) {
                    if (k % 2 != 0) {
                        continue;
                    }
                    int countA = ((n + (i+1))/2) * ((n - (i+1))/2 + 1)  + ((j+2)/2 * (j /2));

//                    int countE = ((i + k) / 2) * ((i - k) / 2);
//                    if (n == 39 && i == 36 && j == 26 && k == 16) {
//                        std::cout << "countA = " << countA << "countE = " << countE << std::endl;
//                    }

                    if (countA != the_third) {
                        continue;
                    }
                    int countE = ((i + k) / 2) * ((i - k) / 2);
                    if (countE != the_third) {
                        continue;
                    }
                    std::cout << "n=" << n << ", (" << i << "," << j << "," << k << ")\n";
                }
            }
        }
    }
    return 0;
}