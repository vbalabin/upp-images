import tkinter as tk

class BinaryScale(tk.Scale):
    """
    Adds a lever-like behavior to a Scale
    """
    def __init__(self, strvalue, truestr, falsestr, *args, **kwargs):
        self._variable = tk.IntVar(value=1)
        super().__init__(variable=self._variable, state= tk.DISABLED, *args, **kwargs)
        self.bind('<ButtonRelease-1>', self._on_click)
        self.strv = strvalue
        self.truestr = truestr
        self.falsestr = falsestr

    @property
    def variable(self):
        return bool(self._variable.get())

    @variable.setter
    def variable(self, value):
        self._variable.set(int(value))
    
    def _on_click(self, event):
        self.variable = not self.variable
        if self.variable:
            self.strv.variable = self.truestr
        else:
            self.strv.variable = self.falsestr

