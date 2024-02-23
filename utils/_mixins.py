import tkinter as tk
from typing import Optional, Tuple

from ._types import GameParamsType


class WindowMixin:
    _program_version: str = ''
    _width = 400
    _height = 300
    _game_settings: GameParamsType = GameParamsType(
        height=16,
        width=30,
        mines_count=99,
        need_animation=False,
        need_sound=False,
        need_help=False,
        need_continue_saved_game=False,
        need_saved_game=False,
        need_question_marks=False,
        i_am_woodpecker=False,
    )
    _title: str = 'Сапер'

    def start(self) -> None:
        raise NotImplementedError

    @property
    def window_width(self) -> int:
        return self._width

    @window_width.setter
    def window_width(self, width: int):
        self._width = width

    @property
    def window_height(self) -> int:
        return self._height

    @window_height.setter
    def window_height(self, height: int):
        self._height = height

    @property
    def window_title(self) -> str:
        return self._title

    @window_title.setter
    def window_title(self, title: str):
        self._title = title

    @property
    def program_version(self) -> str:
        return self._program_version

    @program_version.setter
    def program_version(self, version: str):
        self._program_version = version

    @property
    def game_settings(self) -> GameParamsType:
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        self._game_settings = settings


class MenuWindowMixin(tk.Toplevel, WindowMixin):

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)

    def _window_config(self):
        self.title(self.window_title)
        self.resizable(False, False)
        x = int(self.winfo_screenwidth() / 2 - self.window_width / 2)
        y = int(self.winfo_screenheight() / 2 - self.window_height / 2)
        self.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')

    def start(self):
        self._window_config()


class ButtonWithNeighbors(tk.Button):
    """ Кастомная кнопка с меткой """

    def __init__(
            self,
            bt_id: str,
            bt_number: int,
            bt_column_index: int,
            bt_row_index: int,
            bt_top: Optional['ButtonWithNeighbors'] = None,
            bt_top_right: Optional['ButtonWithNeighbors'] = None,
            bt_right: Optional['ButtonWithNeighbors'] = None,
            bt_bottom_right: Optional['ButtonWithNeighbors'] = None,
            bt_bottom: Optional['ButtonWithNeighbors'] = None,
            bt_bottom_left: Optional['ButtonWithNeighbors'] = None,
            bt_left: Optional['ButtonWithNeighbors'] = None,
            bt_top_left: Optional['ButtonWithNeighbors'] = None,
            has_bomb: bool = False,  # есть ли бомба на кнопке
            has_flag: bool = False,  # установлен ли флаг на кнопке (блокировка)
            is_empty_pressed: bool = False,  # кнопка без бомбы нажата
            count_bombs_around: int = 0,
            **kwargs,
    ):
        self.bt_id: str = bt_id
        self.bt_number: int = bt_number
        self.bt_column_index: int = bt_column_index
        self.bt_row_index: int = bt_row_index
        self.bt_top: Optional['ButtonWithNeighbors'] = bt_top
        self.bt_top_right: Optional['ButtonWithNeighbors'] = bt_top_right
        self.bt_right: Optional['ButtonWithNeighbors'] = bt_right
        self.bt_bottom_right: Optional['ButtonWithNeighbors'] = bt_bottom_right
        self.bt_bottom: Optional['ButtonWithNeighbors'] = bt_bottom
        self.bt_bottom_left: Optional['ButtonWithNeighbors'] = bt_bottom_left
        self.bt_left: Optional['ButtonWithNeighbors'] = bt_left
        self.bt_top_left: Optional['ButtonWithNeighbors'] = bt_top_left
        self.has_bomb: bool = has_bomb
        self.has_flag: bool = has_flag
        self.is_empty_pressed: bool = is_empty_pressed
        self.count_bombs_around: int = count_bombs_around
        super().__init__(**kwargs)

    @property
    def get_neighbors_collection(self) -> Tuple[
        Optional['ButtonWithNeighbors'], Optional['ButtonWithNeighbors'],
        Optional['ButtonWithNeighbors'], Optional['ButtonWithNeighbors'],
        Optional['ButtonWithNeighbors'], Optional['ButtonWithNeighbors'],
        Optional['ButtonWithNeighbors'], Optional['ButtonWithNeighbors']
    ]:
        return (
            self.bt_top,
            self.bt_top_right,
            self.bt_right,
            self.bt_bottom_right,
            self.bt_bottom,
            self.bt_bottom_left,
            self.bt_left,
            self.bt_top_left,
        )


class LabelWithTimer(tk.Label):
    """ Кастомная метка Tkinter с функционалом таймера """

    __timer_is_run: bool = False

    def __init__(self, timer_start_value: int, **kwargs):
        self.__timer_value: int = timer_start_value
        kwargs['text'] = self.__label_text
        super().__init__(**kwargs)

    @property
    def __label_text(self) -> str:
        """ Создание текста для метки """
        if self.timer_value > 9999:
            self.timer_value = 9999
        result: str = str(self.timer_value)
        while len(result) < 4:
            result = '0' + result
        return result

    def __update_clock(self):
        if not self.timer_is_run:
            return
        self.timer_value += 1
        self.configure(text=self.__label_text)
        self.master.after(1000, self.__update_clock)

    @property
    def timer_value(self) -> int:
        return self.__timer_value

    @timer_value.setter
    def timer_value(self, value: int):
        self.__timer_value = value

    @property
    def timer_is_run(self) -> bool:
        return self.__timer_is_run

    @timer_is_run.setter
    def timer_is_run(self, timer_is_run: bool):
        self.__timer_is_run = timer_is_run

    def start_timer(self):
        if self.timer_is_run:
            return
        self.timer_is_run = True
        self.__update_clock()

    def stop_timer(self):
        self.timer_is_run = False

    def clear_timer(self):
        self.stop_timer()
        self.timer_value = 0
        self.configure(text=self.__label_text)


class LabelWithBombCount(tk.Label):
    """ Кастомная метка Tkinter с функционалом количества бомб """

    __timer_is_run: bool = False

    def __init__(self, start_bomb_count: int, bomb_positions_idx: Tuple[int], **kwargs):
        self.__bomb_count: int = start_bomb_count
        self.__bomb_positions_idx: Tuple[int] = bomb_positions_idx
        kwargs['text'] = self.__label_text
        super().__init__(**kwargs)

    @property
    def __label_text(self) -> str:
        """ Создание текста для метки """
        result: str = str(self.__bomb_count)
        while len(result) < 3:
            result = '0' + result
        return result
