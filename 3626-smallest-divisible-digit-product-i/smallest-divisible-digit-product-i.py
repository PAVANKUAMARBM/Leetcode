class Solution:
    def product(self, n):
        prod = 1
        while n:
            prod *= n % 10
            n //= 10
        return prod

    def smallestNumber(self, n, t):
        while self.product(n) % t != 0:
            n += 1
        return n