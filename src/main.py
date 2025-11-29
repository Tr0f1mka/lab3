import typer   #type: ignore
from typing import Optional
from src.kasino.slot.slot import Slot
from src.kasino.videopoker import VideoPoker
from src.kasino.blackjack import BlackJack
from src.stack.stack import Stack
from src.queue.queue import Queue
import src.math_func as math_f
import src.sorts as sorts
from src.utilities.check_list import check_list


"""-Объявление объектов-"""


app = typer.Typer()
app_slot = Slot()
app_videopoker = VideoPoker()
app_blackjack = BlackJack()
app_stack = Stack()
app_queue = Queue()


def check_bet(x: int, min_x: int, max_x: int) -> int | None:
    """
    Проверяет корректность ставки
    :param x: Число - проверяемая ставка
    :param min_x: Число - минимальный порог
    :param max_x: Число - максимальный порог
    :return: Число - ставка
    """

    if x < min_x or x > max_x:
        raise typer.BadParameter(f"Значение должно быть между {min_x} и {max_x}")
    return x


def check_buckets(x: int | None) -> int | None:
    """
    Проверяет корректность количества вёдер

    """

    if x:
        if x < 2:
            raise typer.BadParameter("Минимальное количество корзин - 2")
    return x


"""--------Слот---------"""


@app.command(help="Сделать крутку")
def spin() -> None:
    app_slot.spin()


@app.command(help="Изменить текущую ставку в слоте")
def slot_bet(
    a: int = typer.Argument(
        help="Варианты ставок: 1 - 10 GC, 2 - 25 GC, 3 - 50 GC(ввести номер ставки)",
        callback=lambda x: check_bet(x, 1, 3)
    ),
) -> None:
    app_slot.change_bet(a)


"""-----Видеопокер------"""


@app.command(help="Сыграть в видеопокер")
def poker() -> None:
    app_videopoker.game()


@app.command(help="Изменить текущую ставку в видеопокере")
def poker_bet(
    a: int = typer.Argument(
        help="Варианты ставок: 1 - 25 GC, 2 - 50 GC, 3 - 75 GC, 4 - 100 GC, 5 - 125 GC(ввести номер ставки)",
        callback=lambda x: check_bet(x, 1, 5)
    )
) -> None:
    app_videopoker.poker_bet(a)


@app.command(hidden=True, name="^^vv<><>BA")
def cheat():
    """
    Чит-код, меняющий значение баланса на 10000 GC(не добавляет, а заменяет)
    """

    app_videopoker.cheat()


"""------Блекджек-------"""


@app.command(help="Сыграть в блекджек")
def black(
    a: int = typer.Argument(
        help="Сделать ставку от 25 до 500 GC",
        callback=lambda x: check_bet(x, 25, 500)
    )
) -> None:
    app_blackjack.game(a)


"""--------Стек---------"""


@app.command(
    help="Добавить элемент в стек", context_settings={"ignore_unknown_options": True}
)
def s_push(
    x: float = typer.Argument(help="Целое число, которое нужно положить в стек"),
) -> None:
    e = app_stack.push(x)            #type: ignore
    print(e) if e else ...

@app.command(help="Выводит верхний элемент стека, удаляя его.")
def s_pop() -> None:
    print(app_stack.pop())           #type: ignore


@app.command(help="Выводит верхний элемент стека")
def s_peek() -> None:
    print(app_stack.peek())          #type: ignore


@app.command(help="Проверяет, пуст ли стек")
def s_is_empty() -> None:
    print(app_stack.is_empty())      #type: ignore


@app.command(help="Выводит размер стека")
def s_len() -> None:
    print(len(app_stack))            #type: ignore


@app.command(help="Выводит минимум стека")
def s_min() -> None:
    print(app_stack.min())           #type: ignore


"""-------Очередь-------"""


@app.command(
    help="Добавить элемент в очередь", context_settings={"ignore_unknown_options": True}
)
def q_enqueue(
    x: float = typer.Argument(help="Целое число, которое нужно положить в очередь"),
) -> None:
    app_queue.enqueue(x)             #type: ignore


@app.command(help="Выводит верхний элемент очереди, удаляя его.")
def q_dequeue() -> None:
    print(app_queue.dequeue())             #type: ignore


@app.command(help="Выводит верхний элемент очереди")
def q_front() -> None:
    print(app_queue.front())               #type: ignore


@app.command(help="Проверяет, пуста ли очередь")
def q_is_empty() -> None:
    print(app_queue.is_empty())            #type: ignore


@app.command(help="Выводит размер очереди")
def q_len() -> None:
    print(len(app_queue))          #type: ignore


"""---Матем. функции----"""


@app.command(context_settings={"ignore_unknown_options": True})
def fact(x: int = typer.Argument(help="Целое число"),
         r: bool = typer.Option(False, "-r", "--recursive", help="Расчёт методом рекурсии(точен)")) -> None:
    """Выводит факториал x"""

    if r:
        for i in range(x):
            math_f.factorial_recursive(i)
        typer.echo(math_f.factorial_recursive(x))
    else:
        typer.echo(math_f.factorial(x))


@app.command(context_settings={"ignore_unknown_options": True})
def fibo(x: int = typer.Argument(help="Целое число"),
         r: bool = typer.Option(False, "-r", "--recursive", help="Расчёт методом рекурсии")) -> None:
    """Выводит элемент из последовательности Фибоначчи"""

    if r:
        for i in range(x):
            math_f.fibo_recursive(i)
        typer.echo(math_f.fibo_recursive(x))
    else:
        typer.echo(math_f.fibo(x))


"""-----Сортировки------"""


@app.command(help="Сортировка пузырьком",
             context_settings={"ignore_unknown_options": True})
def bubble(x : list[str] = typer.Argument(help="Сортируемый массив")):
    a = sorts.bubble_sort(x)
    typer.echo(a)


@app.command(help="Быстрая сортировка",
             context_settings={"ignore_unknown_options": True})
def quick(x : list[str] = typer.Argument(help="Сортируемый массив")):
    a = sorts.quick_sort(check_list(x))
    typer.echo(a)


@app.command(help="Сортировка подсчётом",
             context_settings={"ignore_unknown_options": True})
def counting(x : list[int] = typer.Argument(help="Сортируемый массив")):
    a = sorts.counting_sort(x)
    typer.echo(a)


@app.command(help="Сортировка по разрядам",
             context_settings={"ignore_unknown_options": True})
def radix(x : list[str] = typer.Argument(help="Сортируемый массив"),
          b: Optional[int] = typer.Option(None, "-b", "--base", help="Система счисления")):
    try:
        if b:
            a = sorts.radix_sort(x, b)    #type: ignore
        else:
            a = sorts.radix_sort(x)       #type: ignore
        typer.echo(a)
    except ValueError as e:
        print(e)


@app.command(help="Сортировка корзинами",
             context_settings={"ignore_unknown_options": True})
def bucket(x : list[float] = typer.Argument(help="Сортируемый массив"),
           b: Optional[int] = typer.Option(None, "-b", "--buckets", help="Количество корзин")):

    a = sorts.bucket_sort(x, b)
    typer.echo(a)


@app.command(help="Сортировка по куче",
             context_settings={"ignore_unknown_options": True})
def heap(x : list[str] = typer.Argument(help="Сортируемый массив")):
    a = sorts.heap_sort(x)
    typer.echo(a)


if __name__ == "__main__":
    app()
