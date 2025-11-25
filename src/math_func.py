from functools import lru_cache


def factorial(n: int) -> int | str:
    if n < 0:
        return f"Error: undefined element with index {n}"
    a = 1
    for i in range(1, n + 1):
        a *= i
    return a


@lru_cache(None)
def factorial_recursive(n: int) -> int | str:
    if n < 0:
        return f"Error: undefined element with index {n}"
    if n == 0:
        return 1
    if n < 3:
        return n
    return n * factorial_recursive(n - 1)


def fibo(n: int) -> int | str:
    if n < 0:
        return f"Error: undefined element with index {n}"
    if n == 0:
        return 0
    d = [0, 1]
    for i in range(2, n+1):
        d.append(d[i-1]+d[i-2])
    return d[-1]


@lru_cache(None)
def fibo_recursive(n: int) -> int | str:
    if n < 0:
        return f"Error: undefined element with index {n}"
    if n < 2:
        return n
    return fibo_recursive(n - 1) + fibo_recursive(n - 2)      #type: ignore



# x = 3
# print(fibo_iter(x))
# print(fibo_recursive(x))
# print(fibonacci_numpy(x))
# print(fibo_recursive(x) == fibonacci_numpy(x))


# for i in range(-2, 11):
#     print(factorial(i))
# print()

# for i in range(-2, 11):
#     print(factorial_recursive(i))
# print()

# for i in range(-2, 11):
#     print(fibo(i))
# print()

# for i in range(-2, 11):
#     print(fibo_recursive(i))
# print()
