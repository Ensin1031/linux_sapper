import tkinter as tk

from _tk import View


def _program_version() -> str:
    with open('Version.txt', 'r') as file:
        return file.read()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("Hello, world!")


if __name__ == '__main__':
    game_window = View()
    game_window.program_version = _program_version()
    game_window.start()
    # root = tk.Tk()
    # app = Application(master=root)
    # app.mainloop()
