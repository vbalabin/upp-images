import tkinter as tk
from src.twmixin import TextVarMixin

class BinaryLabel(TextVarMixin, tk.Label):
    """
    tkinter Label with a variable attached
    """
    def __init__(self, initialstr, *args, **kwargs):
        super().__init__(initialstr, *args, **kwargs)
