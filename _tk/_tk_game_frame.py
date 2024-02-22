import tkinter as tk

from utils import WindowMixin, GameParamsType


class MainGameFrame(tk.Frame, WindowMixin):

    def __init__(self, root: tk.Tk, main_window: 'View'):
        super().__init__()
        self.__root = root
        self.__main_window = main_window
        self.__frame_width = 0
        self.__frame_height = 0

    def start(self):
        self.__window_body()
        self.__init_window()

    def reboot_game(self, params: GameParamsType) -> None:
        self.result_frame.destroy()
        self.game_settings = params

        self.__window_body()
        self.__init_window()

    @property
    def game_settings(self):
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        self._game_settings = settings
        self.frame_width = 1 + settings.width * 25 + 1
        self.frame_height = 1 + settings.height * 25 + 1

    def __window_body(self):
        """ Создаем основной фрейм с игрой """
        # create frames
        # self.user_frame = tk.Frame(self.__root, bg='green', width=588, height=33)  # фрейм со строкой поиска
        self.result_frame = tk.Frame(
            self.__root,
            bg="White",
            borderwidth=3,
            width=self.frame_width,
            height=self.frame_height,
            relief=tk.SUNKEN,
        )

    def __init_window(self):
        """ Инициализируем основной фрейм с игрой """
        self.result_frame.pack(pady=35)

    @property
    def frame_width(self) -> int:
        return self.__frame_width

    @frame_width.setter
    def frame_width(self, width: int):
        self.__frame_width = width

    @property
    def frame_height(self) -> int:
        return self.__frame_height

    @frame_height.setter
    def frame_height(self, height: int):
        self.__frame_height = height
