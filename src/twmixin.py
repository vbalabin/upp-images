import tkinter as tk

class TextVarMixin():
    """
    ads StringVar and creates property out of it
    """
    def __init__(self, initialstr, *args, **kwargs):
        self._variable = tk.StringVar(value=initialstr)
        super().__init__(textvariable=self._variable, *args, **kwargs)

    @property
    def variable(self):
        return self._variable.get()

    @variable.setter
    def variable(self, value):
        self._variable.set(value)