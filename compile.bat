call activate pyqt_env
pyinstaller -i img\puzzle.ico --clean --noconsole -F merger.py
call conda deactivate
pause
