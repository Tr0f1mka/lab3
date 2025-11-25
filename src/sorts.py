from src.utilities.check_list import check_list


def bubble_sort(a: list[str]) -> list[int | float | str]:
    """
    Сортировка пузырьком
    """

    ans = check_list(a)
    for i in range(len(ans)):
        for j in range(len(ans) - i - 1):
            if ans[j] > ans[j + 1]:                         #type: ignore
                ans[j], ans[j + 1] = ans[j + 1], ans[j]     #type: ignore
    return ans


def quick_sort(a: list[int | float | str]) -> list[int | float | str]:
    """
    Быстрая сортировка
    """

    if len(a) <= 1:
        return a
    mid = a[len(a) // 2]
    left = [x for x in a if x < mid]      #type: ignore
    middle = [x for x in a if x == mid]   #type: ignore
    right = [x for x in a if x > mid]     #type: ignore

    return quick_sort(left) + middle + quick_sort(right)


def counting_sort(a: list[int]) -> list[int]:
    """
    Сортировка подсчётом
    """

    if not a:
        return []
    min_len = min(a)
    cnt = [0 for i in range(max(a)-min_len + 1)]
    for i in a:
        cnt[i-min_len] += 1
    res = []
    for i in range(len(cnt)):
        while cnt[i] > 0:
            res.append(i+min_len)
            cnt[i] -= 1

    return res


def radix_sort(a: list[str], base: int = 10) -> list[str]:
    """
    Поразрядная сортировка
    """

    if not a:
        return []

    if "." in "".join(a):
        raise ValueError("Error: radix sort does not work with real numbers.")

    max_elem = len(max(a, key=len))

    res = [i.zfill(max_elem) for i in a]
    for i in range(max_elem - 1, -1, -1):
        args: list[list[str]] = [[] for j in range(base)]
        for elem in res:
            args[int(elem[i], base)].append(elem)
        res = [elem for arg in args for elem in arg]
    res = [elem.lstrip("0") for elem in res]
    while "" in res:
        res[res.index("")] = "0"
    return res


def bucket_sort(a: list[int|float], buckets: int | None = None) -> list[int|float] | str:
    """
    Корзинная сортировка
    """

    if len(a) < 2:                               # Возврат пустого/малого списка
        return a

    min_elem = min(a)                            # Объявление нужных констант
    diff = max(a) - min_elem

    if not diff:                                 # Возврат списка одинаковых элементов
        return a

    if buckets is None:                          # Если неизвестно количество корзин - использование длины списка
        buckets = len(a)
    elif buckets <= 1:
        return "Error: basket sorting requires at least 2 buckets"

    arrs: list[list[int|float]] = [[] for i in range(buckets)]          # Создание списка корзин

    for elem in a:                               # Раскидывание элементов по корзинам
        ind = int(
            (elem - min_elem) * buckets / diff
        )                                        # Вычисление индекса нужной корзины
        if ind == buckets:                       # Если индекс равен размеру - уменьшение на 1
            ind -= 1
        arrs[ind].append(elem)

    for i in range(buckets):                     # Сортировка корзин
        arrs[i] = bucket_sort(arrs[i], buckets)  #type: ignore

    result: list[int|float] = []                 # Сбор результата
    for bucket in arrs:
        result += bucket

    return result


def build_tree(a: list[int | float | str], n: int, i: int):
    """
    Постройка бинарного дерева
    :param a: Преобразуемый список
    :param n: Размер списка
    :param i: Индекс перемещаемого элемента
    """

    parent = i
    lt = 2 * i + 1
    rt = 2 * i + 2

    if lt < n and a[parent] < a[lt]:          #type: ignore
        parent = lt
    if rt < n and a[parent] < a[rt]:          #type: ignore
        parent = rt

    if parent != i:
        a[i], a[parent] = a[parent], a[i]     #type: ignore
        build_tree(a, n, parent)


def heap_sort(a: list[str]) -> list[int | float | str]:
    """
    Сортировка кучей
    """

    ans = check_list(a)
    n = len(ans)
    for i in range(n - 1, -1, -1):
        build_tree(ans, n, i)

    for i in range(n-1, 0, -1):
        ans[i], ans[0] = ans[0], ans[i]   #type: ignore
        build_tree(ans, i, 0)
    return ans


# print()
# from random import randint, seed  # noqa: E402
# seed(10)
# b = ['a3', '52c', 'e6', '2a', 'A000', '23','320']
# b = [3, 4, 1, 10, -7, 0]
# b = [4.3, 76.5, -3, -3.1, 0, 4]
# b = ['a', 'cat', 'werty', 'pk', 7]
# b = [True, True, False, True]
# b = [[1, 2], [3, 4], [1,], [5,]]
# b = "34 56 -7 4 -1.0".split()
# print(b)
# print(sorted(b))
# b = list(map(str, b))

# print()
# print(bubble_sort(b))
# print(b)
# print(quick_sort(b))
# print()
# print(counting_sort(b))
# print()
# print(radix_sort([str(x) for x in b], 16))
# print(b)
# print(bucket_sort(b))
# print()
# print(b)
# print()
# print(heap_sort(b))
