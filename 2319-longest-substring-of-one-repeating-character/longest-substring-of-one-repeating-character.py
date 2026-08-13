class Solution(object):
    def longestRepeating(self, s, queryCharacters, queryIndices):
        """
        :type s: str
        :type queryCharacters: str
        :type queryIndices: List[int]
        :rtype: List[int]
        """
        n = len(s)
        chars = list(s)

        prefix = [0] * (4 * n)
        suffix = [0] * (4 * n)
        longest = [0] * (4 * n)

        def merge(node, left, right, mid):
            left_len = mid - left + 1
            right_len = right - mid

            prefix[node] = prefix[node * 2]
            suffix[node] = suffix[node * 2 + 1]
            longest[node] = max(
                longest[node * 2],
                longest[node * 2 + 1]
            )

            if chars[mid] == chars[mid + 1]:
                longest[node] = max(
                    longest[node],
                    suffix[node * 2] + prefix[node * 2 + 1]
                )

                if prefix[node * 2] == left_len:
                    prefix[node] += prefix[node * 2 + 1]

                if suffix[node * 2 + 1] == right_len:
                    suffix[node] += suffix[node * 2]

        def build(node, left, right):
            if left == right:
                prefix[node] = suffix[node] = longest[node] = 1
                return

            mid = (left + right) // 2
            build(node * 2, left, mid)
            build(node * 2 + 1, mid + 1, right)
            merge(node, left, right, mid)

        def update(node, left, right, index):
            if left == right:
                return

            mid = (left + right) // 2

            if index <= mid:
                update(node * 2, left, mid, index)
            else:
                update(node * 2 + 1, mid + 1, right, index)

            merge(node, left, right, mid)

        build(1, 0, n - 1)

        answer = []

        for index, char in zip(queryIndices, queryCharacters):
            if chars[index] != char:
                chars[index] = char
                update(1, 0, n - 1, index)

            answer.append(longest[1])

        return answer