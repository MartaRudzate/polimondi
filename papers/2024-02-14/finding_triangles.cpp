#include <iostream>

int main() {
    for (int n = 27; n < 2000; ++n) {
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