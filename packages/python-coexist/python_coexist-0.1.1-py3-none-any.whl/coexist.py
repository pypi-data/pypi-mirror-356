from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager


@contextmanager
def coexist(max_workers: int = None):
    """
    Run multiple code statements concurrently using a simple and Pythonic context manager

    Example:

    with coexist() as ce:
        ce(lambda: print("Hello"))  # Thread 1
        ce(lambda: print("World"))  # Thread 2
    """
    tasks = []

    def submit(func: callable):
        if not callable(func):
            raise TypeError(
                '\nTypeError detected: This usually means "coexist" was used incorrectly ..\n\n'
                'Valid usage example:\n'
                'with coexist() as ce:\n'
                '    ce(lambda: print("Hello"))\n'
                '    ce(lambda: print("World"))'
            )
        tasks.append(func)

    yield submit

    with ThreadPoolExecutor(max_workers=max_workers or len(tasks)) as executor:
        futures = [executor.submit(task) for task in tasks]
        for future in futures:
            future.result()
