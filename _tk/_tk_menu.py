import copy
import tkinter as tk
from collections import OrderedDict
from typing import Literal, Optional, Callable

from utils import MenuWindowMixin, GameParamsType, WindowMixin, GameModeEnum, ACTIVE_BACKGROUND_COLOR


class WorkMenu(tk.Menu, WindowMixin):

    def __init__(self, root: tk.Tk, main_window: 'View'):  # noqa
        self.__root = root
        self.__main_window = main_window
        self.__menubar = tk.Menu(self.__root)  # инициализация сайдбара
        self.__root.config(menu=self.__menubar)  # запуск сайдбара
        super().__init__(self.__menubar)

    def start(self):
        self.__init_menu()

    def __menu_options(self):
        print('настройки')

    def __init_menu(self):
        """ Инициализируем меню сайбара """
        self.__create_game_fields()  # запускаем выпадающее меню Файл
        self.__create_help_fields()  # запускаем выпадающее меню Справка

    def __create_game_fields(self):
        """ Меню сайдбара, вкладка "Файл" """
        fail_fields = tk.Menu(self.__menubar, tearoff=0)

        fail_fields.add_command(label='     Новая игра', command=self.__reboot_main_window)
        fail_fields.add_command(label='     Статистика', command=self.__menu_options)
        fail_fields.add_command(label='     Параметры', command=self.__program_settings)
        fail_fields.add_command(label='     Изменить оформление', command=self.__menu_options)
        fail_fields.add_command(label='     Выход', command=self.__main_window.destroy)
        self.__menubar.add_cascade(label='Игра', menu=fail_fields)

    def __create_help_fields(self):
        """ Меню сайдбара, вкладка "Справка" """
        help_fields = tk.Menu(self.__menubar, tearoff=0)

        help_fields.add_command(label='     Посмотреть справку', command=self.__menu_options)
        help_fields.add_command(label='     О программе', command=self.__about_program)
        help_fields.add_command(label='     Другие игры в Интернете', command=self.__other_games)
        self.__menubar.add_cascade(label='Справка', menu=help_fields)

    def __reboot_main_window(self):
        self.__main_window.reboot(params=self.game_settings)

    def __set_settings_handler(self, params: GameParamsType) -> None:
        self.__main_window.reboot(params=params)

    def __program_settings(self):
        settings = ProgramSettingsWindow(self)
        settings.program_version = self.program_version
        settings.game_settings = self.game_settings
        settings.settings_handler = self.__set_settings_handler
        settings.window_title = 'Параметры'
        settings.window_width = 500
        settings.window_height = 700
        settings.start()
        settings.grab_set()

    def __about_program(self):
        about = AboutProgramWindow(parent=self)
        about.window_title = 'О программе "Сапер"'
        about.program_version = self.program_version
        about.window_width = 400
        about.window_height = 300
        about.start()
        about.grab_set()

    def __other_games(self):
        other = OtherGamesWindow(parent=self)
        other.window_title = 'Другие игры в Интернете'
        other.program_version = self.program_version
        other.window_width = 350
        other.window_height = 250
        other.start()
        other.grab_set()


class ProgramSettingsWindow(MenuWindowMixin):

    __settings_handler = None

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)
        self.__init_window_body()
        self.__init_buttons()

    @property
    def settings_handler(self) -> Optional[Callable]:
        return self.__settings_handler

    @settings_handler.setter
    def settings_handler(self, settings_handler: Callable):
        self.__settings_handler = settings_handler

    def start(self):
        super().start()
        self.__set_defaults_fields_values()
        self.__init_level_radiobuttons()
        self.__init_check_buttons()
        self.__set_configure()
        self.__init_window()

    def __set_defaults_fields_values(self):
        self.__radiobuttons_value = tk.IntVar(value=GameModeEnum.get_this_type(params=self.game_settings))

        self.__height_field_value = tk.IntVar(value=self.game_settings.height)
        self.__width_field_value = tk.IntVar(value=self.game_settings.width)
        self.__mines_count_field_value = tk.IntVar(value=self.game_settings.mines_count)
        self.__animation_value = tk.BooleanVar(value=self.game_settings.need_animation)
        self.__sound_value = tk.BooleanVar(value=self.game_settings.need_sound)
        self.__help_value = tk.BooleanVar(value=self.game_settings.need_help)
        self.__continue_game_value = tk.BooleanVar(value=self.game_settings.need_continue_saved_game)
        self.__saved_game_value = tk.BooleanVar(value=self.game_settings.need_saved_game)
        self.__question_marks_value = tk.BooleanVar(value=self.game_settings.need_question_marks)
        self.__woodpecker_value = tk.BooleanVar(value=self.game_settings.i_am_woodpecker)

    def __init_window(self):
        self.__frame_for_border.pack(pady=25)
        self.__frame_level.pack(pady=1, padx=1, fill=tk.BOTH)

        self.__newbie_radiobutton.place(relx=0.03, rely=0.16, anchor=tk.W)
        self.__amateur_radiobutton.place(relx=0.03, rely=0.48, anchor=tk.W)
        self.__professional_radiobutton.place(relx=0.03, rely=0.8, anchor=tk.W)
        self.__special_radiobutton.place(relx=0.43, rely=0.16, anchor=tk.W)

        self.__special_radiobutton_height_field_label.place(relx=0.49, rely=0.33, anchor=tk.W)
        self.__special_radiobutton_height_field.place(relx=0.83, rely=0.33, anchor=tk.W)
        self.__special_radiobutton_width_field_label.place(relx=0.49, rely=0.5, anchor=tk.W)
        self.__special_radiobutton_width_field.place(relx=0.83, rely=0.5, anchor=tk.W)
        self.__special_radiobutton_mine_count_field_label.place(relx=0.49, rely=0.67, anchor=tk.W)
        self.__special_radiobutton_mine_count_field.place(relx=0.83, rely=0.67, anchor=tk.W)

        self.__check_button_animation.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_sound.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_help.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_continue_game.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_saved_game.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_question_marks.pack(anchor=tk.W, padx=15, pady=5)
        self.__check_button_woodpecker.pack(anchor=tk.W, padx=15, pady=5)

        self.__button_ok.place(relx=0.49, rely=0.95, anchor=tk.E)
        self.__button_cancel.place(relx=0.51, rely=0.95, anchor=tk.W)

    def __init_window_body(self):
        self.__frame_for_border = tk.Frame(self, bg='gray')  # width=471, height=351
        self.__frame_level = tk.Frame(self.__frame_for_border,  width=470, height=250)  # width=470, height=350

    def __init_level_radiobuttons(self):
        # создаем переменную для хранения результата выбора
        level_value = GameModeEnum.get_this_type(params=self.game_settings)

        common_set = OrderedDict((
            ('master', self.__frame_level),
        ))
        radiobutton_common_set = copy.copy(common_set)
        radiobutton_common_set.update((
            ('master', self.__frame_level),
            ('variable', self.__radiobuttons_value),
            ('activebackground', ACTIVE_BACKGROUND_COLOR),
            ('width', 18),
            ('height', 3),
            ('anchor', tk.W),
        ))

        self.__newbie_radiobutton = tk.Radiobutton(  # чекбокс "Новичок"
            text='Новичок\n10 мин\nполе 9х9 ячеек',
            value=GameModeEnum.NEWBIE.value,
            **radiobutton_common_set,
        )
        self.__amateur_radiobutton = tk.Radiobutton(  # чекбокс "Любитель"
            text='Любитель\n40 мин\nполе 16х16 ячеек',
            value=GameModeEnum.AMATEUR.value,
            **radiobutton_common_set,
        )
        self.__professional_radiobutton = tk.Radiobutton(  # чекбокс "Профессионал"
            text='Профессионал\n99 мин\nполе 16х30 ячеек',
            value=GameModeEnum.PROFESSIONAL.value,
            **radiobutton_common_set,
        )
        self.__special_radiobutton = tk.Radiobutton(  # чекбокс "Особый" - назначение параметров вручную
            text='Особый',
            value=GameModeEnum.SPECIAL.value,
            **radiobutton_common_set,
        )
        state_value: Literal['normal', 'disabled'] = 'disabled'
        if level_value == GameModeEnum.SPECIAL.value:
            state_value = 'normal'

        label_common_set = copy.copy(common_set)
        label_common_set.update((
            ('master', self.__frame_level),
            ('state', state_value),
            ('activebackground', ACTIVE_BACKGROUND_COLOR),
        ))
        field_common_set = copy.copy(label_common_set)
        field_common_set.update((
            ('width', 5),
            ('increment', 1),
            ('activebackground', ACTIVE_BACKGROUND_COLOR),
        ))

        self.__special_radiobutton_height_field_label = tk.Label(  # Высота
            text='Высота (9-30):', **label_common_set,
        )
        self.__special_radiobutton_height_field = tk.Spinbox(
            from_=9, to=30, textvariable=self.__height_field_value, **field_common_set,
        )
        self.__special_radiobutton_width_field_label = tk.Label(  # Ширина
            text='Ширина (9-40):', **label_common_set,
        )
        self.__special_radiobutton_width_field = tk.Spinbox(
            from_=9, to=40, textvariable=self.__width_field_value, **field_common_set,
        )
        self.__special_radiobutton_mine_count_field_label = tk.Label(  # Количество мин
            text='Число мин (10-700):', **label_common_set,
        )
        self.__special_radiobutton_mine_count_field = tk.Spinbox(
            from_=10, to=700, textvariable=self.__mines_count_field_value, **field_common_set,
        )

    def __set_configure(self):
        """ Установка конфигураций после инициализации всех компонентов """
        self.__newbie_radiobutton.configure(command=self.__set_level_mode)
        self.__amateur_radiobutton.configure(command=self.__set_level_mode)
        self.__professional_radiobutton.configure(command=self.__set_level_mode)
        self.__special_radiobutton.configure(command=self.__set_level_mode)

    def __set_level_mode(self):
        """ Смена режима назначения уровня """
        radiobuttons_value = self.__radiobuttons_value.get()
        if radiobuttons_value == GameModeEnum.SPECIAL.value:
            state_value: Literal['normal', 'disabled'] = 'normal'
        else:
            state_value: Literal['normal', 'disabled'] = 'disabled'
            self.__height_field_value.set(
                value=GameModeEnum.get_default_height(
                    mode_value=radiobuttons_value, default_value=self.game_settings.height
                )
            )
            self.__width_field_value.set(
                value=GameModeEnum.get_default_width(
                    mode_value=radiobuttons_value, default_value=self.game_settings.width
                )
            )
            self.__mines_count_field_value.set(
                value=GameModeEnum.get_default_mines_count(
                    mode_value=radiobuttons_value, default_value=self.game_settings.mines_count
                )
            )

        self.__special_radiobutton_height_field_label.configure(state=state_value)
        self.__special_radiobutton_height_field.configure(state=state_value)
        self.__special_radiobutton_width_field_label.configure(state=state_value)
        self.__special_radiobutton_width_field.configure(state=state_value)
        self.__special_radiobutton_mine_count_field_label.configure(state=state_value)
        self.__special_radiobutton_mine_count_field.configure(state=state_value)

    def __init_check_buttons(self):
        common_set = OrderedDict((
            ('master', self),
            ('width', 56),
            ('height', 2),
            ('anchor', tk.W),
            ('activebackground', ACTIVE_BACKGROUND_COLOR),
        ))
        self.__check_button_animation = tk.Checkbutton(
            text="Воспроизводить анимацию", variable=self.__animation_value, **common_set)
        self.__check_button_sound = tk.Checkbutton(
            text="Звуковое сопровождение", variable=self.__sound_value, **common_set)
        self.__check_button_help = tk.Checkbutton(
            text="Показывать подсказки", variable=self.__help_value, **common_set)
        self.__check_button_continue_game = tk.Checkbutton(
            text="Всегда продолжать сохраненную игру", variable=self.__continue_game_value, **common_set)
        self.__check_button_saved_game = tk.Checkbutton(
            text="Всегда сохранять игру при выходе", variable=self.__saved_game_value, **common_set)
        self.__check_button_question_marks = tk.Checkbutton(
            text="Знаки вопроса при двойном щелчке правой кнопкой мыши",
            variable=self.__question_marks_value, **common_set)
        self.__check_button_woodpecker = tk.Checkbutton(
            text="Я дятел!", variable=self.__woodpecker_value, **common_set)

    def __init_buttons(self):
        self.__button_ok = tk.Button(self, text="Ок", command=self.__set_new_menu_options, width=10)
        self.__button_cancel = tk.Button(self, text="Отмена", command=self.destroy, width=10)

    def __set_new_menu_options(self):
        result_settings: GameParamsType = GameParamsType(
            height=self.__height_field_value.get(),
            width=self.__width_field_value.get(),
            mines_count=self.__mines_count_field_value.get(),
            need_animation=self.__animation_value.get(),
            need_sound=self.__sound_value.get(),
            need_help=self.__help_value.get(),
            need_continue_saved_game=self.__continue_game_value.get(),
            need_saved_game=self.__saved_game_value.get(),
            need_question_marks=self.__question_marks_value.get(),
            i_am_woodpecker=self.__woodpecker_value.get(),
        )

        self.destroy()

        if self.settings_handler is not None and self.game_settings != result_settings:
            self.settings_handler(params=result_settings)


class AboutProgramWindow(MenuWindowMixin):

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)
        self.__init_button()

    def start(self):
        super().start()
        self.__init_window_body()
        self.__init_window()

    def __init_window(self):
        self.label_title.pack(padx=20, pady=10)
        self.body_1_row.pack()
        self.button.pack(side="bottom", pady=10)

    def __init_window_body(self):
        self.label_title = tk.Label(self, text="О программе")
        self.body_1_row = tk.Label(
            self, text=f"Сюда обычно никто не заглядывает,\n"
                       f"поэтому можно нести всякую хрень!\n\n"
                       f"Эту игру я написал самолично со скуки\n"
                       f"хотелось, знаете-ли нормальный\n"
                       f"Сапер под Линух!\n\n"
                       f"С уважением, Ensin.\n\n"
                       f"Щучу! Без уважения!!\n\n"
                       f"Версия игры {self.program_version}, 2024г."
        )

    def __init_button(self):
        self.button = tk.Button(self, text="Закрыть", command=self.destroy)


class OtherGamesWindow(MenuWindowMixin):

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)
        self.__init_window_body()
        self.__init_button()

    def start(self):
        super().start()
        self.__init_window()

    def __init_window(self):
        self.body_1_row.pack(pady=10)
        self.button.pack(side="bottom", pady=5)

    def __init_window_body(self):
        self.body_1_row = tk.Label(
            self, text="Вот скажи, дятел, что ты\n"
                       "ожидал тут увидеть?\n\n"
                       "Хочешь других игр,\n"
                       "собака неблагодарная?!\n"
                       "А вот хрен тебе!\n\n"
                       "С уважением, Ensin.\n"
                       "Щучу, щучу! Без уважения!!\n\n"
        )

    def __init_button(self):
        self.button = tk.Button(self, text="Закрыть", command=self.destroy)
