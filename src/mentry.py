import tkinter as tk
from src.twmixin import TextVarMixin

class MergerEntry(TextVarMixin, tk.Entry):
    """
    tkinter Entry with a variable attached
    """
    def __init__(self, initialstr, *args, **kwargs):
        super().__init__(initialstr, *args, **kwargs)