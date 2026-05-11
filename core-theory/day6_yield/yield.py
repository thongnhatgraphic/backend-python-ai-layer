def count_up(n):
    for i in range(1, n + 1):
        print(i)
        yield i

for i in count_up(5):
    print("i is:", i)
    
# count = count_up(5)
# print(count)
# next(count)
# next(count)
# next(count)
# next(count)
# next(count)



# print("------------------")
def even_numbers(n):
    list_even_number = [ j for j in range (1, n+1) if j % 2 == 0]
    
    for i in list_even_number:
        yield i

for i in even_numbers(10):
    print(i)

def odd_numbers(n):
    for i in range(1, n + 1):
        if i % 2 != 0:
            yield i

for i in odd_numbers(10):
    print(i)

#     # ------fibonaci series-------

def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        yield a
        (a, b) = b, a + b

for i in fibonacci(10):
    print(i)