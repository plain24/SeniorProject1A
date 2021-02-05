# imports
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

# constants
FONT_FAMILY = "Roboto Bold"
BACKGROUND_COLOR = "#242424"

# create main window
app = tk.Tk()
app.title("Project Group 1A")
app.geometry('1320x800')
app.resizable(False, False)
app.configure(bg=BACKGROUND_COLOR)

# set min sizes for all columns
for column in range(11):
    app.columnconfigure(column, minsize=120)

# create header labels
header = tk.Label(
    app,
    text="Java cross-compiler/translator to Python",
    bg=BACKGROUND_COLOR,
    fg="white",
    height=2,
    font=(FONT_FAMILY, 28)
)
header.grid(column=0, row=0, columnspan=11, sticky='nsew', pady=(20, 0))

info_header = tk.Label(
    app,
    text="Copy/Paste or import Java code in the left box. "
         "Click the \"Translate\" button and the Python code will appear in the right box.\n"
         "Either copy paste from the output box or click the \"Download\" button for a .py file of your translated code.",
    bg=BACKGROUND_COLOR,
    fg="#20bebe",
    height=2,
    font=(FONT_FAMILY, 12)
)
info_header.grid(column=0, row=1, columnspan=11, sticky='nsew', pady=(0, 20))

# create small labels
input_label = tk.Label(
    app,
    text="Input text here or open file:",
    bg=BACKGROUND_COLOR,
    fg="white",
    font=(FONT_FAMILY, 9)
)
input_label.grid(column=1, row=2, columnspan=4, sticky="nsew", pady=(0, 1))

output_label = tk.Label(
    app,
    text="Output will show here:",
    bg=BACKGROUND_COLOR,
    fg="white",
    font=(FONT_FAMILY, 9)
)
output_label.grid(column=6, row=2, columnspan=4, sticky='nsew', pady=(0, 1))

# create text boxes
input_text_box = scrolledtext.ScrolledText(
    app,
    wrap=tk.WORD,
    height=30,
    width=30,
    borderwidth=0
)
input_text_box.grid(column=1, row=3, columnspan=4, sticky='nsew')

output_text_box = scrolledtext.ScrolledText(
    app,
    wrap=tk.WORD,
    height=30,
    width=30,
    borderwidth=0
)
output_text_box.grid(column=6, row=3, columnspan=4, sticky='nsew')


# button functions
def clear_input(self):
    self.delete("1.0", tk.END)


def open_file(self):
    file_1 = filedialog.askopenfilename(
        initialdir="G:/",
        title="Select a File",
        filetypes=[("java files", "*.java")]
    )
    if file_1:
        file_2 = open(file_1, "r")
        self.delete("1.0", tk.END)
        self.insert("1.0", file_2.read())
        file_2.close()


def translate_file(self):
    self.delete("1.0", tk.END)
    self.insert("1.0", "Translation not yet implemented...")


def download_file(self):
    output_text = self.get("1.0", tk.END)
    print(len(output_text))
    if len(output_text) > 1:
        output_filename = filedialog.asksaveasfilename(
            initialdir="G:/",
            defaultextension='.txt',
            title="Save File As",
            filetypes=[("python file", ".py")])
        file = open(output_filename, "w")
        file.write(output_text)
        file.close()
        messagebox.showinfo(title="File Saved", message=f"Your file has been saved to:\n{output_filename}")
    else:
        return


# create buttons
translate_btn = tk.Button(
    app,
    text="Translate >>>",
    width=10,
    height=3,
    font=(FONT_FAMILY, 8),
    command=lambda: translate_file(output_text_box)
)
translate_btn.grid(column=5, row=3, sticky='ew', padx=5)

clear_btn = tk.Button(
    app,
    text="Clear Input",
    width=10,
    height=2,
    font=(FONT_FAMILY, 8),
    command=lambda: clear_input(input_text_box)
)
clear_btn.grid(column=2, row=4, pady=(1, 0), sticky='ew')

open_file_btn = tk.Button(
    app,
    text="Open File",
    width=10,
    height=2,
    font=(FONT_FAMILY, 8),
    command=lambda: open_file(input_text_box)
)
open_file_btn.grid(column=3, row=4, pady=(1, 0), sticky='ew')

download_btn = tk.Button(
    app,
    text="Download as .py",
    width=10,
    height=2,
    font=(FONT_FAMILY, 8),
    command=lambda: download_file(output_text_box)
)
download_btn.grid(column=7, row=4, pady=(1, 0), sticky='ew', columnspan=2)

app.mainloop()