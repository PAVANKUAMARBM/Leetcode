# class Solution:
#     def product(self, n):
#         prod = 1
#         while n:
#             prod *= n % 10
#             n //= 10
#         return prod

#     def smallestNumber(self, n, t):
#         while self.product(n) % t != 0:
#             n += 1
#         return n


class Solution:
    def smallestNumber(self, n, t):
        while True:
            product=1
            for num in str(n):
                product*=int(num)

            if product%t==0:
                return n
            n+=1
        