import tkinter as tk
from typing import Optional

from _db import Connection
from _tk._tk_menu import WorkMenu
from _tk._tk_game_frame import MainGameFrame
from utils import WindowMixin, GameParamsType


class View(WindowMixin):

    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.__db_connector = Connection()
        self.__db_connector.connect()

        self.game_settings = self.set_game_settings(params=self.__db_connector.params)

        self.__menu_frame = WorkMenu(root=self.root, main_window=self)
        self.__game_frame = MainGameFrame(root=self.root, main_window=self)

    def destroy(self):
        self.root.destroy()

    def start(self):
        """ Запуск основного окна программы """
        self.__main_window_config()

        self.__game_frame.program_version = self.program_version
        self.__game_frame.game_settings = self.game_settings
        self.__game_frame.start()
        self.__menu_frame.program_version = self.program_version
        self.__menu_frame.game_settings = self.game_settings
        self.__menu_frame.start()

        self.root.mainloop()

    def reboot(self, params: Optional[GameParamsType] = None):
        """ Ребут основного окна игры. Если передают новые настройки - то с ними """

        if params is not None:
            self.__db_connector.update_params(params=params)
            self.game_settings = self.set_game_settings(params=params)
            self.__game_frame.reboot_game(params=params)

        self.__main_window_config()

        self.__menu_frame = WorkMenu(root=self.root, main_window=self)
        self.__menu_frame.game_settings = self.game_settings
        self.__menu_frame.program_version = self.program_version
        self.__menu_frame.start()

        # self.__game_frame = MainGameFrame(root=self.root, main_window=self)
        # self.__game_frame.game_settings = self.game_settings
        # self.__game_frame.program_version = self.program_version
        # self.__game_frame.start()

        self.root.mainloop()

    def __main_window_config(self):
        self.root.title(f'Сапер - v.{self.program_version}, автор - Ensin')
        self.root.resizable(False, False)
        x = int(self.root.winfo_screenwidth() / 2 - self.window_width / 2)
        y = int(self.root.winfo_screenheight() / 2 - self.window_height / 2)
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')

    def set_game_settings(self, params: GameParamsType) -> GameParamsType:
        self.window_width = 40 + params.width * 25 + 40
        self.window_height = params.height * 25 + 85
        return params
