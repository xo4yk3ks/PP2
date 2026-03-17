from functools import reduce

nums = [1, 2, 3, 4, 5]

# map
squared = list(map(lambda x: x**2, nums))

# filter
evens = list(filter(lambda x: x % 2 == 0, nums))

# reduce
sum_all = reduce(lambda x, y: x + y, nums)

print(squared, evens, sum_all)
