class StrUtil:

    @staticmethod
    def lcs(x, y):
        # Create a matrix to store lengths of longest common suffixes
        dp = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]

        # Fill the matrix in bottom-up fashion
        for i in range(len(x) + 1):
            for j in range(len(y) + 1):
                if i == 0 or j == 0:
                    dp[i][j] = 0
                elif x[i - 1] == y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Length of LCS is in the bottom right cell
        return dp[-1][-1]

    @staticmethod
    def indel(x, y):
        lcs_length = StrUtil.lcs(x, y)
        return len(x) + len(y) - 2 * lcs_length


    @staticmethod
    def augmented_LCS(x, y):
        # Create a matrix to store lengths of longest common suffixes
        dp = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]

        # Build the dp matrix in bottom-up fashion
        for i in range(1, len(x) + 1):
            for j in range(1, len(y) + 1):
                if x[i - 1] == y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Reconstruct the LCS from the dp matrix
        lcs_length = dp[len(x)][len(y)]
        augmented_x = ""
        augmented_y = ""
        i, j = len(x), len(y)

        while i > 0 and j > 0:
            if x[i - 1] == y[j - 1]:
                # Current character is part of LCS
                augmented_x = x[i - 1] + augmented_x
                augmented_y = y[j - 1] + augmented_y
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                # Delete from 'x' (not part of LCS)
                augmented_x = f"({x[i - 1]})" + augmented_x
                i -= 1
            else:
                # Delete from 'y' (not part of LCS)
                augmented_y = f"({y[j - 1]})" + augmented_y
                j -= 1

        # Add remaining characters of x and y
        while i > 0:
            augmented_x = f"({x[i - 1]})" + augmented_x
            i -= 1
        while j > 0:
            augmented_y = f"({y[j - 1]})" + augmented_y
            j -= 1

        return (lcs_length, augmented_x.replace(')(', ''), augmented_y.replace(')(', ''))