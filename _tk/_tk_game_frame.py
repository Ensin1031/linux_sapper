import random
import tkinter as tk
from collections import OrderedDict
from tkinter import font

import tksvg

from itertools import product
from typing import Tuple, List, Optional

from utils import (
    WindowMixin, GameParamsType, ButtonWithNeighbors, LABEL_BUTTON_PREFIX, BTN_SIZE,
    LabelWithTimer, LabelWithBombCount,
)
from utils import SVGImages


class MainGameFrame(tk.Frame, WindowMixin):

    def __init__(self, root: tk.Tk, main_window: 'View'):  # noqa
        super().__init__()
        self.__root = root
        self.__main_window = main_window
        self.__frame_width = 0
        self.__frame_height = 0

        self.__bomb_idx: Tuple = ()
        self.__clock_icon = tksvg.SvgImage(data=SVGImages.TIMER, scaletoheight=30)
        self.__play_icon = tksvg.SvgImage(data=SVGImages.PLAY, scaletoheight=30)
        self.__pause_icon = tksvg.SvgImage(data=SVGImages.PAUSE, scaletoheight=30)
        self.__mine_icon = tksvg.SvgImage(data=SVGImages.MINE, scaletoheight=30)
        self.__flag_red_icon = tksvg.SvgImage(data=SVGImages.FLAG_RED, scaletoheight=20)

        self.__game_run: bool = False
        self.__game_pause: bool = False
        self.__game_end: bool = False

        self.__pause_button: Optional[tk.Button] = None

    def start(self):
        self.__window_body()
        self.__init_window()

    def reboot_game(self, params: GameParamsType) -> None:
        if self.__work_game_frame is not None:
            self.__work_game_frame.destroy()
        if self.__info_game_frame is not None:
            self.__info_game_frame.destroy()
        self.game_settings = params

        self.__window_body()
        self.__init_window()

    @property
    def game_settings(self):
        return self._game_settings

    @game_settings.setter
    def game_settings(self, settings: GameParamsType):
        self._game_settings = settings

        bomb_idx_list: List = []
        range_list: List = list(range(settings.mines_count))

        for _ in range_list:
            bomb_id = random.randint(1, settings.width * settings.height)
            if bomb_id not in bomb_idx_list:
                bomb_idx_list.append(bomb_id)
            else:
                range_list.append(0)

        self.__bomb_idx: Tuple = tuple(bomb_idx_list)

        print(len(bomb_idx_list), bomb_idx_list)  # TODO убрать
        self.frame_width = 1 + settings.width * BTN_SIZE + 1
        self.frame_height = 1 + settings.height * BTN_SIZE + 1

    def __pause_or_play_game(self):
        if self.__pause_button is None or not self.__game_run:
            return
        if self.__game_pause:
            self.__pause_button.configure(
                image=self.__pause_icon
            )
            self.__game_pause = False
            self.__timer_data_label.start_timer()
        else:
            self.__pause_button.configure(
                image=self.__play_icon
            )
            self.__game_pause = True
            self.__timer_data_label.stop_timer()

    def __window_body(self):
        """ Создаем основной фрейм с игрой """
        self.__work_game_frame = tk.Frame(
            master=self.__root,
            borderwidth=3,
            width=self.frame_width,
            height=self.frame_height,
            relief=tk.SUNKEN,
        )
        self.__info_game_frame = tk.Frame(
            master=self.__root,
            width=self.frame_width,
            height=40,
        )
        self.__timer_game_frame = tk.Frame(
            master=self.__info_game_frame,
            width=100,
            height=30,
        )
        self.__count_bomb_game_frame = tk.Frame(
            master=self.__info_game_frame,
            width=100,
            height=30,
        )

        bt_index = 1
        for value in tuple(product(
            range(1, self.game_settings.width + 1),
            range(1, self.game_settings.height + 1)
        )):
            i_col = value[0]
            i_row = value[1]
            self.__create_button_with_label(bt_index=bt_index, i_row=i_row, i_col=i_col)
            bt_index += 1

        for bt in self.__work_game_frame.children.values():

            if isinstance(bt, ButtonWithNeighbors):
                self.__set_mine_button_configurations(mine_btn=bt)

        common_data_label_set = OrderedDict((
            ('width', 5),
            ('height', 30),
            ('borderwidth', 2),
            ('relief', tk.SUNKEN),
            ('bg', 'blue'),
            ('fg', 'white'),
            ('font', font.Font(family='Helvetica', size=16)),
        ))

        self.__timer_label = tk.Label(
            master=self.__timer_game_frame, image=self.__clock_icon
        )
        self.__timer_data_label = LabelWithTimer(
            timer_start_value=0,
            master=self.__timer_game_frame,
            **common_data_label_set,
        )
        self.__pause_button = tk.Button(
            master=self.__info_game_frame, image=self.__pause_icon, command=self.__pause_or_play_game, state=tk.DISABLED
        )
        self.__bomb_count_label = tk.Label(
            master=self.__count_bomb_game_frame, image=self.__mine_icon
        )
        self.__bomb_count_data_label = LabelWithBombCount(
            start_bomb_count=self.game_settings.mines_count,
            bomb_positions_idx=self.__bomb_idx,
            master=self.__count_bomb_game_frame,
            **common_data_label_set,
        )

    def __set_mine_button_configurations(self, mine_btn: ButtonWithNeighbors) -> None:
        """ Установка данных у кнопки игрового поля """
        bt_column_index: int = mine_btn.bt_column_index
        bt_row_index: int = mine_btn.bt_row_index

        bt_top_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index and x.bt_row_index == bt_row_index - 1,
            self.__work_game_frame.children.values()
        )) if bt_row_index > 1 else ()
        mine_btn.bt_top = bt_top_arr[0] if len(bt_top_arr) > 0 else None

        bt_top_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index - 1,
            self.__work_game_frame.children.values()
        )) if bt_row_index > 1 and bt_column_index < self.game_settings.width else ()
        mine_btn.bt_top_right = bt_top_right_arr[0] if len(bt_top_right_arr) > 0 else None

        bt_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index,
            self.__work_game_frame.children.values()
        )) if bt_column_index < self.game_settings.width else ()
        mine_btn.bt_right = bt_right_arr[0] if len(bt_right_arr) > 0 else None

        bt_bottom_right_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index + 1 and x.bt_row_index == bt_row_index + 1,
            self.__work_game_frame.children.values()
        )) if bt_column_index < self.game_settings.width and bt_row_index < self.game_settings.height else ()
        mine_btn.bt_bottom_right = bt_bottom_right_arr[0] if len(bt_bottom_right_arr) > 0 else None

        bt_bottom_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index and x.bt_row_index == bt_row_index + 1,
            self.__work_game_frame.children.values()
        )) if bt_row_index < self.game_settings.height else ()
        mine_btn.bt_bottom = bt_bottom_arr[0] if len(bt_bottom_arr) > 0 else None

        bt_bottom_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index + 1,
            self.__work_game_frame.children.values()
        )) if bt_row_index < self.game_settings.height and bt_column_index > 1 else ()
        mine_btn.bt_bottom_left = bt_bottom_left_arr[0] if len(bt_bottom_left_arr) > 0 else None

        bt_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index,
            self.__work_game_frame.children.values()
        )) if bt_column_index > 1 else ()
        mine_btn.bt_left = bt_left_arr[0] if len(bt_left_arr) > 0 else None

        bt_top_left_arr = tuple(filter(
            lambda x: x.bt_column_index == bt_column_index - 1 and x.bt_row_index == bt_row_index - 1,
            self.__work_game_frame.children.values()
        )) if bt_column_index > 1 and bt_row_index > 1 else ()
        mine_btn.bt_top_left = bt_top_left_arr[0] if len(bt_top_left_arr) > 0 else None

        mine_btn.count_bombs_around = len(tuple(
            filter(lambda x: x is not None and x.has_bomb, mine_btn.get_neighbors_collection)
        )) if not mine_btn.has_bomb else 0

    def __create_button_with_label(self, bt_index: int, i_row: int, i_col: int) -> None:
        """ Создание 1 кнопки - контейнера """
        mine_button = ButtonWithNeighbors(
            master=self.__work_game_frame,
            bt_id=LABEL_BUTTON_PREFIX if bt_index == 1 else f'{LABEL_BUTTON_PREFIX}{bt_index}',
            bt_column_index=i_col,
            bt_row_index=i_row,
            bt_number=bt_index,
            has_bomb=bt_index in self.__bomb_idx,
        )
        mine_button.bind('<Button-1>', lambda event: self.__mine_left_click_event(event=event, bt=mine_button))
        mine_button.bind('<Button-2>', lambda event: self.__mine_middle_click_event(event=event, bt=mine_button))
        mine_button.bind('<Button-3>', lambda event: self.__mine_rigth_click_event(event=event, bt=mine_button))

        mine_button.grid(column=i_col, row=i_row)

    def __start_game(self):
        if self.__game_run:
            return
        self.__game_run = True
        self.__game_pause = False
        self.__pause_button.configure(state=tk.ACTIVE)
        self.__timer_data_label.start_timer()

    def __mine_left_click_event(self, event: tk.Event, bt: ButtonWithNeighbors):
        """ Эвент клика ЛКМ по кнопке - контейнеру """
        print('__mine_left_click_event event ===', type(event), event)  # TODO убрать
        print('__mine_left_click_event ===', bt.has_bomb, bt.count_bombs_around, bt)  # TODO убрать
        self.__start_game()
        # if bt.has_flag:
        #     bt.has_flag = False
        #     bt.configure(
        #         image='',
        #         state=tk.ACTIVE,
        #         relief=tk.GROOVE,
        #     )
        # else:
        #     bt.has_flag = True
        #     bt.configure(
        #         image=self.__flag_red_icon,
        #         state=tk.DISABLED,
        #         relief=tk.SUNKEN,
        #     )

    def __mine_rigth_click_event(self, event: tk.Event, bt: ButtonWithNeighbors):
        """ Эвент клика ПКМ по кнопке - контейнеру """
        print('__mine_rigth_click_event event ===', type(event), event)  # TODO убрать
        print('__mine_rigth_click_event ===', bt.has_bomb, bt.count_bombs_around, bt)  # TODO убрать
        self.__start_game()
        if bt.has_flag:
            bt.has_flag = False
            bt.configure(
                image='',
            )
        else:
            bt.has_flag = True
            bt.configure(
                image=self.__flag_red_icon,
            )

    def __mine_middle_click_event(self, event: tk.Event, bt: ButtonWithNeighbors):
        """ Эвент клика средней кнопки мыши либо ПКМ + ЛКМ одновременно по кнопке - контейнеру """
        print('__mine_middle_click_event event ===', type(event), event)  # TODO убрать
        print('__mine_middle_click_event ===', bt.has_bomb, bt.count_bombs_around, bt)  # TODO убрать
        self.__start_game()

    def __init_window(self):
        """ Инициализируем основной фрейм с игрой """
        self.__work_game_frame.place(relx=0.5, y=30, anchor=tk.N)
        self.__info_game_frame.pack(pady=20, side=tk.BOTTOM)

        self.__timer_game_frame.place(relx=0.02, rely=0.5, anchor=tk.W)
        self.__count_bomb_game_frame.place(relx=0.98, rely=0.5, anchor=tk.E)

        self.__timer_label.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
        self.__timer_data_label.place(relx=0.67, rely=0.6, anchor=tk.CENTER)
        self.__pause_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.__bomb_count_data_label.place(relx=0.3, rely=0.6, anchor=tk.CENTER)
        self.__bomb_count_label.place(relx=1, rely=0.5, anchor=tk.E)

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
