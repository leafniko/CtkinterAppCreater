from tkinter import filedialog





def open_file_dialog(filetypes,initialdir):
    # Open a file dialog and get the selected file path
    # [('data files','*.csv;*.txt')]
    file_path = filedialog.askopenfilename(filetypes=filetypes,initialdir=initialdir)
    if file_path:
        return file_path
