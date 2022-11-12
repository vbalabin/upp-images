import sys
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter.filedialog import askopenfilenames, askdirectory
from PIL import Image

# every project's class has its own module
from src.bscale import BinaryScale
from src.blabel import BinaryLabel
from src.mentry import MergerEntry

# resizing and concatenating scripts are stored as static methods
from src.mscripts import MergerScripts


class ImageMerger():
    bg_color = '#ffffff'
    folder = MergerScripts.find_folderpath(sys.argv[0])

    # in this list string value for "output path variable" is stored
    # if you click another tab, path changes
    output_entry_values = list()
    output_entry_values.append(MergerScripts.make_default_file_path(folder, 'png')) 
    output_entry_values.append(folder)
    output_entry_values.append(MergerScripts.make_default_file_path(folder, 'pdf')) 
    output_entry_values.append(folder)
    current_active_tab = 0

    DARK_BG = 'LightSteelBlue'
    LIGHT_BG = 'AliceBlue'
    
    def __init__(self, master):
        self.master = master
        self.configure_main_window()

        self.tabs_panel = self.add_notebook_panel(master)
        self.tabs_panel.bind("<ButtonRelease-1>", self._switch_tab_onclick)

        # region "define Concatenation tab"
        self.tabs_panel.concatenation_tab = self.append_tab(self.tabs_panel, 'Concatenate')
        self.tabs_panel.concatenation_tab.grid_ = self.add_grid(self.tabs_panel.concatenation_tab, 4, 6)
        self.lb_concat = self.add_label(0, 1, self.tabs_panel.concatenation_tab, 'Concatenate Vertically')
        self.bs_concat = self.add_biscale(0, 0, self.tabs_panel.concatenation_tab, self.lb_concat, 
                                            'Concatenate Vertically', 'Concatenate Horizontally')
        self.lb_resize = self.add_label(1, 1, self.tabs_panel.concatenation_tab, 'Resize to Max')
        self.bs_resize = self.add_biscale(1, 0, self.tabs_panel.concatenation_tab, self.lb_resize, 
                                            'Resize to Max', 'Do not Resize')
        self.colorbtn = self.add_color_btn(self.tabs_panel.concatenation_tab.grid_[2][0])
        self.lb_colorb = self.add_label(2, 1, self.tabs_panel.concatenation_tab, 'Background Color')
        # endregion

        # region "define Resizing tab"
        self.tabs_panel.resizing_tab = self.append_tab(self.tabs_panel, 'Resize')
        self.tabs_panel.resizing_tab.grid_ = self.add_grid(self.tabs_panel.resizing_tab, 4, 6)
        self.lb_sizes = self.add_label(0, 1, self.tabs_panel.resizing_tab, 'Percent')
        self.bs_sizes = self.add_biscale(0, 0, self.tabs_panel.resizing_tab, self.lb_sizes, 
                                            'Percent', 'Pixels')        
        self.lb_width = tk.Label(self.tabs_panel.resizing_tab.grid_[1][0], text='W:', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))
        self.lb_width.pack(side=tk.RIGHT, padx=3)
        self.width_entry = self.add_size_entry(self.tabs_panel.resizing_tab.grid_[1][1])
        self.lb_height = tk.Label(self.tabs_panel.resizing_tab.grid_[1][2], text='H:', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))        
        self.lb_height.pack(side=tk.RIGHT, padx=3)
        self.height_entry = self.add_size_entry(self.tabs_panel.resizing_tab.grid_[1][3])

        self.lb_maxmin = self.add_label(2, 1, self.tabs_panel.resizing_tab, 'maximum sizes')
        self.bs_maxmin = self.add_biscale(2, 0, self.tabs_panel.resizing_tab, self.lb_maxmin, 
                                            'maximum sizes', 'minimum sizes')
        self.find_widthheight_btn = self.add_wdthgt_btn(2, 4, self.tabs_panel.resizing_tab)

        self.lb_file_type = self.add_label(3, 1, self.tabs_panel.resizing_tab, 'save as PNG')
        self.bs_file_type = self.add_biscale(3, 0, self.tabs_panel.resizing_tab, self.lb_file_type, 
                                            'save as PNG', 'save as JPG')
        self.lb_rgba_convert = self.add_label(3, 5, self.tabs_panel.resizing_tab, 'RGB')
        self.bs_rgba_convert = self.add_biscale(3, 4, self.tabs_panel.resizing_tab, self.lb_rgba_convert, 
                                            'RGBA', 'RGB')
        self.bs_rgba_convert.variable = False
        # endregion

        # region "define create pdf"
        self.tabs_panel.pdf_tab = self.append_tab(self.tabs_panel, 'pdf')
        self.tabs_panel.pdf_tab.grid_ = self.add_grid(self.tabs_panel.pdf_tab, 4, 6)
        self.lb_dpi = tk.Label(self.tabs_panel.pdf_tab.grid_[0][0], text='DPI', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))
        self.lb_dpi.pack(side=tk.LEFT)
        self.dpi_entry = self.add_dpi_entry(self.tabs_panel.pdf_tab.grid_[0][1])

        self.lb_quality = tk.Label(self.tabs_panel.pdf_tab.grid_[1][0], text='Quality', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))
        self.lb_quality.pack(side=tk.LEFT)
        self.quality_entry = self.add_dpi_entry(self.tabs_panel.pdf_tab.grid_[1][1])
        self.quality_entry.variable = '60'
        # endregion    
         
        # region "define cropping"
        self.tabs_panel.cropping_tab = self.append_tab(self.tabs_panel, 'cropping')
        self.tabs_panel.cropping_tab.grid_ = self.add_grid(self.tabs_panel.cropping_tab, 4, 6)

        self.lb_leftwidth = tk.Label(self.tabs_panel.cropping_tab.grid_[0][0], text='LW:', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))
        self.lb_leftwidth.pack(side=tk.RIGHT, padx=3)
        self.leftwidth_entry = self.add_size_entry(self.tabs_panel.cropping_tab.grid_[0][1], initial='0')
        self.lb_leftheight = tk.Label(self.tabs_panel.cropping_tab.grid_[0][2], text='LH:', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))        
        self.lb_leftheight.pack(side=tk.RIGHT, padx=3)
        self.leftheight_entry = self.add_size_entry(self.tabs_panel.cropping_tab.grid_[0][3], initial='0')

        self.lb_rightwidth = tk.Label(self.tabs_panel.cropping_tab.grid_[1][0], text='RW:', 
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))
        self.lb_rightwidth.pack(side=tk.RIGHT, padx=3)
        self.rightwidth_entry = self.add_size_entry(self.tabs_panel.cropping_tab.grid_[1][1], initial='~')
        self.lb_rightheight = tk.Label(self.tabs_panel.cropping_tab.grid_[1][2], text='RH:',
                                bg=self.DARK_BG, font=('Consolas', '14', 'bold'))        
        self.lb_rightheight.pack(side=tk.RIGHT, padx=3)
        self.rightheight_entry = self.add_size_entry(self.tabs_panel.cropping_tab.grid_[1][3], initial='~')        

        self.find_leftright_btn = self.add_lftrht_btn(0, 4, self.tabs_panel.cropping_tab)

        self.colorbtn_crop = self.add_color_btn(self.tabs_panel.cropping_tab.grid_[2][0])
        self.lb_colorb_crop = self.add_label(2, 1, self.tabs_panel.cropping_tab, 'Background Color')
        # endregion                

        # region "define Files frame"
        self.files_frame = self.add_file_frame(master)
        self.files_frame.grid_ = self.add_grid(self.files_frame, 10, 6)
        self.lb_files = self.add_label(0, 0, self.files_frame, 'Files:')
        self.lb_files.configure(font=('Consolas', '12', 'bold'), padx=3)
        self.lstbox = self.add_listbox(1, 0, self.files_frame)
        self.clear_listboxbtn = self.add_clear_listbox_btn(self.files_frame.grid_[0][3])
        self.inputbtn = self.add_inputbtn(self.files_frame.grid_[0][4])
        self.excludebtn = self.add_excludebtn(self.files_frame.grid_[0][5])
        self.lb_outputdir = self.add_label(6, 0, self.files_frame, 'Output Path:')
        self.lb_outputdir.configure(font=('Consolas', '12', 'bold'), padx=3)
        self.direntry = self.add_outputdir_entry(7, 0, self.files_frame, self.output_entry_values[0])
        self.outputdir_btn = self.add_outputdir_btn(self.files_frame.grid_[7][5])
        self.outputdir_btn = self.add_process_btn(9, 2, self.files_frame)
        # endregion
        

    def _switch_tab_onclick(self, event=None):
        """
        clicking tabs event calls this function
        """
        tab_index = self.tabs_panel.index('current')
        if tab_index != self.current_active_tab:
            self.output_entry_values[self.current_active_tab] = self.direntry.variable
            self.current_active_tab = tab_index
            self.direntry.variable = self.output_entry_values[tab_index]
            self.lstbox.focus_force()
        else:
            return
            
       
    def configure_main_window(self):
        """
        main window properties
        """
        self.master.title('ImageFiles Merger')
        _icon_path = r"img/puzzle.ico"
        self.master.iconbitmap(_icon_path)
        self.master.geometry('320x480')
        self.master.configure(bg=self.DARK_BG)
        self.master.resizable(False, False)

    def add_notebook_panel(self, master):
        """
        placed in top side of the app
        """
        nb = ttk.Notebook(master, width=304, height=124)
        nb.style = ttk.Style()
        nb.style.theme_create( "tabs", parent="alt", settings={
            ".": {
                "configure": {"background": self.DARK_BG}
            },           
            "TNotebook": {
                "configure": {
                    "tabmargins": [2, 5, 2, 0], 
                    "borderwidth": 0
                }
            },
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": self.DARK_BG},
                "map": {
                    "background": [("selected", 'AliceBlue')],
                    "expand": [("selected", [1, 1, 1, 0])] 
                } 
            } 
        } )

        nb.style.theme_use("tabs")
        nb.pack(expand=1)
        return nb

    def append_tab(self, notebook, text):
        """
        creates frame, appends it as a tab
        """
        frame = tk.LabelFrame(notebook, width=300, height=120, bg=self.DARK_BG)
        notebook.add(frame, text=text)
        return frame

    def add_file_frame(self, master):
        """
        file related widget placed here
        """
        _frame = tk.LabelFrame(master, width=300, height=420, relief=tk.FLAT, border=1)
        _frame.propagate(False)
        _frame.pack(side=tk.BOTTOM, pady=8)
        return _frame

    def add_grid(self, master, sizex=8, sizey=8):
        """
        creates a table structure on a given frame
        """
        result = list()
        for i in range(sizex):
            result.append(list())
            tk.Grid.rowconfigure(master, i, weight=0)
            for j in range(sizey):
                frame = tk.Frame(master, width=50, height=30, bg=self.DARK_BG)
                frame.grid(row=i, column=j, sticky=tk.NSEW)
                tk.Grid.columnconfigure(master, j, weight=0)
                result[i].append(frame)
        return result

    def _call_clrchooser(self):
        """
        uses tkinter.dialogs colorchooser \\
        sets self.bg_color
        """
        _clr = colorchooser.askcolor()
        self.colorbtn.configure(background=_clr[1])
        self.colorbtn_crop.configure(background=_clr[1])
        self.bg_color = _clr[1]

    def add_color_btn(self, master):
        """
        if "do not resize" flag is set \\
        selecting concatenated image bg color is often needed
        """
        _btn = tk.Button(master, text='', background=self.bg_color, width=3, height=1, 
                command=self._call_clrchooser)
        master.propagate(False)
        _btn.pack(pady=8)
        return _btn

    def add_biscale(self, row_index, column_index, master, lbl, truestr, falsestr):
        """
        biscale(BinaryScale) is a customized Scale \\
        it acts like simple "on/off" lever for an inner variable \\
        and changes related Label text by onclick event
        """
        _scale = BinaryScale(master=master, strvalue=lbl, truestr=truestr, falsestr=falsestr, 
                orient='horizontal', from_=0, to=1)
        _scale.configure(background='Teal', length=25, width=8, highlightbackground='DarkSlateBlue', 
                borderwidth=0, sliderrelief=tk.FLAT, troughcolor=self.LIGHT_BG, sliderlength=15, 
                highlightthickness=2, showvalue=0)
        _scale.grid(row=row_index, column=column_index)
        return _scale

    def add_label(self, row_index, column_index, master, txt):
        """
        just hides some simple code
        """
        _label = BinaryLabel(master=master, initialstr=txt, background=self.DARK_BG, 
                font=('Consolas', '14', 'bold'))
        _label.grid(row=row_index, column=column_index, columnspan=5, sticky=tk.W)
        return _label

    def add_size_entry(self, master, txt='', initial='100'):
        """
        for width and height entries
        """
        master.propagate(False)
        _entry = MergerEntry(master=master, initialstr=txt, justify='right', bg=self.LIGHT_BG)
        _entry.pack(pady=3)
        _entry.variable = initial
        return _entry

    def add_dpi_entry(self, master, txt=''):
        """
        for dpi entriy
        """
        master.propagate(False)
        _entry = MergerEntry(master=master, initialstr=txt, justify='right', bg=self.LIGHT_BG)
        _entry.pack(pady=6, padx=9)
        _entry.variable = '96'
        return _entry          

    def _find_widthheight(self):
        """
        runs through selected image list, \\
        returns width and height in pixels
        """
        self.bs_sizes.variable = False
        self.bs_sizes.strv.variable = self.bs_sizes.falsestr
        file_names = self.lstbox.get(0, tk.END)
        if not file_names: 
            self.width_entry.variable = 'none'
            self.height_entry.variable = 'none'
            return
        image_list = [Image.open(e) for e in file_names]

        if self.bs_maxmin.variable:
            self.width_entry.variable = MergerScripts.find_max_width(image_list)
            self.height_entry.variable = MergerScripts.find_max_height(image_list)
        else:
            self.width_entry.variable = MergerScripts.find_min_width(image_list)
            self.height_entry.variable = MergerScripts.find_min_height(image_list)

    def _find_leftright(self):
        """
        runs through selected image list, \\
        returns right width and right height in pixels
        for find btn in concatenation tab
        """
        file_names = self.lstbox.get(0, tk.END)
        if not file_names: 
            self.leftwidth_entry.variable = 'none'
            self.leftheight_entry.variable = 'none'
            self.rightwidth_entry.variable = 'none'
            self.rightheight_entry.variable = 'none'
            return
        image_list = [Image.open(e) for e in file_names]

        self.leftwidth_entry.variable = '0'
        self.leftheight_entry.variable = '0'
        self.rightwidth_entry.variable = MergerScripts.find_max_width(image_list)
        self.rightheight_entry.variable = MergerScripts.find_max_height(image_list)


    def add_wdthgt_btn(self, rowindex, columnindex, master):
        """
        "find" button
        """
        _frame = tk.Frame(master, width=75, height=30, background=self.DARK_BG)
        _frame.propagate(False)
        _frame.grid(row=rowindex, column=columnindex, columnspan=2)
        _btn = tk.Button(_frame, text='find', activebackground=self.LIGHT_BG, 
                font=('Consolas', '14', 'bold'), command=self._find_widthheight)
        _btn.pack(padx=5, pady=3)
        return _btn     

    def add_lftrht_btn(self, rowindex, columnindex, master):
        """
        "find" button
        """
        _frame = tk.Frame(master, width=75, height=30, background=self.DARK_BG)
        _frame.propagate(False)
        _frame.grid(row=rowindex, column=columnindex, columnspan=2)
        _btn = tk.Button(_frame, text='find', activebackground=self.LIGHT_BG, 
                font=('Consolas', '14', 'bold'), command=self._find_leftright)
        _btn.pack(padx=5, pady=3)
        return _btn     


    def add_listbox(self, rowindex, columnindex, master):
        """
        main listbox
        """
        lbox = tk.Listbox(master, bg=self.LIGHT_BG, height=4)
        lbox.grid(row=rowindex, column=columnindex, columnspan=6, rowspan=4, sticky=tk.NSEW)
        return lbox

    def _clear_listbox_files(self):
        self.lstbox.delete(0, tk.END)

    def add_clear_listbox_btn(self, master):
        """
        "cl" clear button
        """
        master.propagate(False)
        _btn = tk.Button(master, activebackground=self.LIGHT_BG, command=self._clear_listbox_files)
        _btn.img = tk.PhotoImage(file=r"img/clear.png")
        _btn.configure(image=_btn.img)        
        _btn.pack(padx=5, pady=3)
        return _btn     

    def _call_selectfiles(self):
        """
        called by "+" button \\
        calls tkinter.dialogs askopenfilenames \\
        if listbox cursor is active file names should be placed after it \\
        """
        _curpos = self.lstbox.curselection()
        filelist = askopenfilenames(filetypes=(("image files", "*.png *.jpg *.jpeg *.gif"),))
        if len(_curpos):
            _curpos = 1 + int(_curpos[0])
            for i, name in enumerate(filelist):
                self.lstbox.insert(i + _curpos, name)
        else:
            for name in filelist:
                self.lstbox.insert(tk.END, name)             

    def add_inputbtn(self, master):
        """
        '+' sign button
        """
        master.propagate(False)
        _btn = tk.Button(master, activebackground=self.LIGHT_BG, command=self._call_selectfiles)
        _btn.img = tk.PhotoImage(file=r"img/include.png")
        _btn.configure(image=_btn.img)
        _btn.pack(padx=5, pady=3)
        return _btn

    def _call_excludefile(self):
        """
        called by "-" button
        """
        _curpos = self.lstbox.curselection()
        if len(_curpos):
            self.lstbox.delete(_curpos)

    def add_excludebtn(self, master):
        """
        '-' sign button
        """
        master.propagate(False)
        _btn = tk.Button(master, activebackground=self.LIGHT_BG, command=self._call_excludefile)
        _btn.img = tk.PhotoImage(file=r"img/exclude.png")
        _btn.configure(image=_btn.img)        
        _btn.pack(padx=5, pady=3)
        return _btn

    def add_outputdir_entry(self, rowindex, columnindex, master, txt):
        """
        creates tk.Entry that shows output path
        """
        _entry = MergerEntry(master=master, initialstr=txt, bg=self.LIGHT_BG)
        _entry.grid(row=rowindex, column=columnindex, columnspan=5, sticky=tk.NSEW, padx=3, pady=4)
        return _entry

    def _call_askdir(self):
        """
        outputdir_btn calls this
        """
        _path = askdirectory()
        
        _path = ['\\' if e == '/' else e for e in _path]
        _path.append('\\')
        
        self.output_entry_values[0] = MergerScripts.make_default_file_path(''.join(_path), 'png')
        self.output_entry_values[1] = ''.join(_path)
        self.output_entry_values[2] = MergerScripts.make_default_file_path(''.join(_path), 'pdf')
        self.output_entry_values[3] = ''.join(_path)

        self.direntry.variable = self.output_entry_values[self.current_active_tab]


    def add_outputdir_btn(self, master):
        """
        """
        master.propagate(False)
        _btn = tk.Button(master, text='<<', activebackground=self.LIGHT_BG, 
                font=('Consolas', '14', 'bold'), command=self._call_askdir)
        _btn.pack(padx=5, pady=3)
        return _btn

    def _call_process_files(self):
        """
        called by "process" button \\
        checks 'current_active_tab' property \\
        calls subservient functions
        """
        if self.current_active_tab == 0:
            self._make_concatenation()
        elif self.current_active_tab == 1:
            self._make_resizing()
        elif self.current_active_tab == 2:
            self._make_pdf()
        elif self.current_active_tab == 3:
            self._make_cropping()                          

    def _make_concatenation(self):
        """
        depending on activated flags different combination of scripts is called
        """
        file_names = self.lstbox.get(0, tk.END)
        if len(file_names) < 2: return

        image_list = [Image.open(e) for e in file_names]

        if self.bs_resize.variable: 
            if self.bs_concat.variable:
                max_width = MergerScripts.find_max_width(image_list)
                image_list = MergerScripts.resize_all_tomax(image_list, max_width, 
                                                    Image, is_vertical=True)
            else:
                max_height = MergerScripts.find_max_height(image_list)
                image_list = MergerScripts.resize_all_tomax(image_list, max_height, 
                                                    Image, is_vertical=False)
            
        if self.bs_concat.variable: 
            result_image = MergerScripts.concatenate_v(image_list, self.bg_color, Image)
        else:
            result_image = MergerScripts.concatenate_h(image_list, self.bg_color, Image)
        
        _path = self.direntry.variable
        _path = MergerScripts.make_default_file_path(_path, 'png') # try
        self.direntry.variable = _path

        try:
            dpi = int(self.dpi_entry.variable)
        except ValueError:
            dpi = 96        

        result_image.save(f'{self.direntry.variable}', 'PNG', dpi=(dpi, dpi))

    def _make_resizing(self):
        """
        converts width, height values \\
        calls subservient resizing functions
        """
        file_names = self.lstbox.get(0, tk.END)
        if not file_names: return

        try:
            width = int(self.width_entry.variable)
        except ValueError:
            width = None

        try:
            height = int(self.height_entry.variable)
        except ValueError:
            height = None
        
        filetype = 'PNG' if self.bs_file_type.variable else 'JPEG'

        try:
            dpi = int(self.dpi_entry.variable)
        except ValueError:
            dpi = 96

        is_converted_to_rgb = not self.bs_rgba_convert.variable

        if self.bs_sizes.variable == True:
            MergerScripts.resize_percents(
                file_names, self.direntry.variable, width, height, filetype, dpi, is_converted_to_rgb)
        else:
            MergerScripts.resize_pixels(
                file_names, self.direntry.variable, width, height, filetype, dpi, is_converted_to_rgb)
            
    def _make_pdf(self):
        """
        according to dpi value \\
        calls subservient pdf functions
        """
        import os

        file_names = self.lstbox.get(0, tk.END)
        if not file_names: return

        try:
            dpi = int(self.dpi_entry.variable)
        except ValueError:
            dpi = 96
        
        # temp_folder = f'{os.getcwd()}\\temp\\'.replace('\\', '/', -1)
        # MergerScripts.clear_temp(temp_folder)
        # MergerScripts.resize_percents(file_names, temp_folder, 100, 100, 'JPEG', dpi, False)
        # temp_file_names = MergerScripts.change_to_temp_filenames(temp_folder, file_names)

        MergerScripts.create_pdf(file_names, self.direntry.variable, dpi, self.quality_entry.variable)

    def _make_cropping(self):
        """
        redefines canvas of the images
        """
        file_names = self.lstbox.get(0, tk.END)
        if not file_names: return        

        left_w = int(self.leftwidth_entry.variable)
        left_h = int(self.leftheight_entry.variable)
        right_w = int(self.rightwidth_entry.variable)
        right_h = int(self.rightheight_entry.variable)
        frame_coordinates = (left_w, left_h), (right_w, right_h)

        try:
            dpi = int(self.dpi_entry.variable)
        except ValueError:
            dpi = 96

        MergerScripts.crop_images(file_names, self.bg_color, self.direntry.variable, frame_coordinates, dpi)

    def add_process_btn(self, rowindex, columnindex, master):
        """
        place "process" btn on bottom line
        """
        _frame = tk.Frame(master, width=100, height=30, background=self.DARK_BG)
        _frame.grid(row=rowindex, column=columnindex, columnspan=2)
        _frame.propagate(False)
        _btn = tk.Button(_frame, text='Process', activebackground=self.LIGHT_BG, 
                font=('Consolas', '14', 'bold'), command=self._call_process_files)
        _btn.pack(padx=5, pady=3)
        return _btn              

if __name__ == "__main__":
    root = tk.Tk()
    im = ImageMerger(root)
    root.mainloop()
