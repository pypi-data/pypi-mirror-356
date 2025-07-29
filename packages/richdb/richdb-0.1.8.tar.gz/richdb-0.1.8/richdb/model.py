#-*- encoding=utf-8 -*-

PRIORITY_MATH_TABLE = ['Time', '1D', '']  #try to maintain a world use copy to make code simple.

class MathModel:
    def __add__(self):
        pass
    def __radd__(self):
        pass
    def __sub__(self):
        pass
    def __rsub__(self):
        pass

    def __div__(self):
        pass
    def __rdiv__(self):
        pass
    def __mul__(self):
        pass
    def __rmul__(self):
        pass

    def defaultstep(self):
        pass


class DataModel:
    def __add__(self):
        pass

    def __radd__(self):
        pass

    def __sub__(self):
        pass

    def __rsub__(self):
        pass

    def __oplus__(self):
        pass

    def __ominus__(self):
        pass

    def __odiv__(self):
        pass

    def __omult__(self):
        pass
    