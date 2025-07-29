import numpy as np


class dummy_class:
    def __init__(self):
        print("Example class created")

    @staticmethod
    def log10(a=1):
        return np.log10(a)


if __name__ == "__main__":
    ExampleObject = dummy_class(10)
    x = ExampleObject.log10()
    print(x)