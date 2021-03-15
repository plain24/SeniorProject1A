# imports
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import scrolledtext, filedialog, messagebox
from Parser import main as ParseMain
from Scanner import *

# constants
FONT_FAMILY = "Cordana"
BACKGROUND_COLOR = "#1a1a1a"
BTN_WIDTH = 192
BTN_HEIGHT = 50


# main window class
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # customize main window
        self.title("Java cross-compiler/translator to Python")
        self.geometry('1675x1010+0+0')
        self.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)

        self.file_input = None

        # set min sizes for all columns
        for column in range(11):
            if column == 0 or column == 10:
                self.columnconfigure(column, minsize=35)
            elif column == 5:
                self.columnconfigure(column, minsize=5)
            else:
                self.columnconfigure(column, minsize=200)

        # create small labels
        self.input_label = tk.Label(
            self,
            text="Input text here or open file:",
            bg="#555555",
            fg="white",
            font=(FONT_FAMILY, 11, 'bold'),
            bd=2
        )
        self.input_label.grid(column=1, row=0, columnspan=4, sticky="nsew", pady=(10, 1))

        self.output_label = tk.Label(
            self,
            text="Output will show here:",
            bg="#555555",
            fg="white",
            font=(FONT_FAMILY, 11, 'bold')
        )
        self.output_label.grid(column=6, row=0, columnspan=4, sticky='nsew', pady=(10, 1))

        self.input_text_box = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            height=64,
            width=30,
            borderwidth=0,
            font=(FONT_FAMILY, 8)
        )
        self.input_text_box.grid(column=1, row=3, columnspan=4, sticky='nsew')

        self.output_text_box = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            height=64,
            width=30,
            borderwidth=0,
            font=(FONT_FAMILY, 8)
        )
        self.output_text_box.grid(column=6, row=3, columnspan=4, sticky='nsew')

        # create button images
        self.clear_btn_img = ImageTk.PhotoImage(Image.open("clear_input_img2.png"))
        self.instructions_img = ImageTk.PhotoImage(Image.open("instructions_img2.png"))
        self.download_img = ImageTk.PhotoImage(Image.open("download_img2.png"))
        self.translate_img = ImageTk.PhotoImage(Image.open("translate_img2.png"))
        self.open_file_img = ImageTk.PhotoImage(Image.open("open_file_img2.png"))

        # create buttons
        self.clear_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            borderwidth=0,
            font=(FONT_FAMILY, 9),
            image=self.clear_btn_img,
            command=self.clear_input
        )
        self.clear_btn.grid(column=2, row=4, pady=(5, 0))

        self.open_file_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            borderwidth=0,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            font=(FONT_FAMILY, 9),
            image=self.open_file_img,
            command=self.open_file
        )
        self.open_file_btn.grid(column=3, row=4, pady=(5, 0))

        self.translate_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            borderwidth=0,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            font=(FONT_FAMILY, 9),
            image=self.translate_img,
            command=self.translate_file
        )
        self.translate_btn.grid(column=7, row=4, pady=(5, 0), columnspan=1)

        self.download_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            borderwidth=0,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            font=(FONT_FAMILY, 9),
            image=self.download_img,
            command=self.download_file
        )
        self.download_btn.grid(column=8, row=4, pady=(5, 0), columnspan=1)

        self.instructions_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            borderwidth=0,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            font=(FONT_FAMILY, 9),
            image=self.instructions_img,
            command=self.instruction_open
        )
        self.instructions_btn.grid(column=4, row=4, columnspan=3, pady=(5, 0))

    # button functions
    def clear_input(self):
        self.input_text_box.delete("1.0", tk.END)

    def open_file(self):
        file_1 = filedialog.askopenfilename(
            initialdir="G:/",
            title="Select a File",
            filetypes=[("java files", "*.java")]
        )
        if file_1:
            file_2 = open(file_1, "r")
            self.input_text_box.delete("1.0", tk.END)
            self.input_text_box.insert("1.0", file_2.read())
            file_2.close()
####################################################################
            self.file_input = file_1

    def translate_file(self):
        if self.input_text_box.compare("end-1c", "==", "1.0"):
            messagebox.showerror('Error', 'Input box is empty')
            return
        self.output_text_box.delete("1.0", tk.END)
####################################################################
        test = Scanner()
        test.prepFile(self.file_input)
        output = ParseMain(test.progNodes)
        # print(output.toString())
####################################################################
        self.output_text_box.insert("1.0", output.toString())

    def download_file(self):
        if self.output_text_box.compare("end-1c", "==", "1.0"):
            messagebox.showerror('Error', 'Output box is empty')
            return
        else:
            output_text = self.output_text_box.get("1.0", tk.END)
            output_filename = filedialog.asksaveasfilename(
                initialdir="G:/",
                defaultextension='.txt',
                title="Save File As",
                filetypes=[("python file", ".py")])
            if output_filename:
                file = open(output_filename, "w")
                file.write(output_text)
                file.close()
                messagebox.showinfo(title="File Saved", message=f"Your file has been saved to:\n{output_filename}")
            else:
                return

    def instruction_open(self):
        popup = Popup(self)
        popup.mainloop()


class Popup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.overrideredirect(True)
        self.geometry('800x470+437+150')
        self.resizable(False, False)
        self.configure(bg=BACKGROUND_COLOR)
        self.title("Instructions")
        self.attributes('-topmost', True)

        with open("instructions.txt") as f:
            self.instruction_text = f.read()

        self.instructions_window_header = tk.Label(
            self,
            text="Instructions",
            bg="#555555",
            fg="#cccccc",
            height=1,
            padx=5,
            pady=5,
            anchor='center',
            font=(FONT_FAMILY, 18)
        )
        self.instructions_window_header.pack(side=tk.TOP, pady=(15, 0), padx=10, expand=True, fill=tk.BOTH)

        self.instructions_window_label = tk.Label(
            self,
            text=self.instruction_text,
            fg="#cccccc",
            bg="#333333",
            height=13,
            anchor='nw',
            justify=tk.LEFT,
            wraplength=760,
            padx=10,
            pady=10,
            font=(FONT_FAMILY, 14)
        )
        self.instructions_window_label.pack(fill=tk.BOTH, pady=(2, 10), padx=10)

        # create button image
        self.instructions_window_close_img = ImageTk.PhotoImage(Image.open("close_window_img.png"))

        self.instructions_window_close_btn = tk.Button(
            self,
            text="",
            width=BTN_WIDTH,
            height=BTN_HEIGHT,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR,
            borderwidth=0,
            font=(FONT_FAMILY, 9),
            image=self.instructions_window_close_img,
            command=self.close_instruction
        )
        self.instructions_window_close_btn.pack(side=tk.BOTTOM, pady=(5, 20), expand=False)

        # disable buttons on main gui window
        self.grab_set()

    def close_instruction(self):
        self.destroy()
        # enable buttons on main gui window
        self.grab_release()


if __name__ == "__main__":
    app = App()
    app.mainloop()
