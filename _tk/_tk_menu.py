import tkinter as tk

from utils import MenuWindowMixin, GameParamsType, WindowMixin


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
        self.__main_window.reboot(params=GameParamsType(
            height=18,
            width=40,
            mines_count=100,
            need_animation=False,
            need_sound=False,
            need_help=False,
            need_continue_saved_game=False,
            need_saved_game=False,
            need_question_marks=False,
            i_am_woodpecker=False,
        ))

    def __program_settings(self):
        settings = ProgramSettingsWindow(self)
        settings.program_version = self.program_version
        settings.game_settings = self.game_settings
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

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)
        self.__init_window_body()
        self.__init_level_radiobuttons()
        self.__init_button()
        self.__result_settings: GameParamsType = GameParamsType(
            height=16,
            width=30,
            mines_count=90,
            need_animation=False,
            need_sound=False,
            need_help=False,
            need_continue_saved_game=False,
            need_saved_game=False,
            need_question_marks=False,
            i_am_woodpecker=False,
        )

    def start(self):
        super().start()
        self.__init_window()

    def __init_window(self):
        self.__frame_for_border.pack(pady=15)
        self.__frame_level.pack(pady=1, padx=1, fill=tk.BOTH)
        self.__newbie_radiobutton.pack(anchor='w')
        self.__amateur_radiobutton.pack(anchor='w')
        self.__professional_radiobutton.pack(anchor='w')
        self.__special_radiobutton.pack(anchor='w')
        self.button_ok.pack(side="bottom", pady=10)

    def __init_window_body(self):
        self.__frame_for_border = tk.Frame(self, bg='gray')  # width=471, height=351
        self.__frame_level = tk.Frame(self.__frame_for_border)  # width=470, height=350

    def __init_level_radiobuttons(self):
        # создаем переменную для хранения результата выбора
        self.__result_level = tk.IntVar()
        self.__result_level.set(2)
        # чекбокс "Новичок"
        self.__newbie_radiobutton = tk.Radiobutton(self.__frame_level, text='Новичок\n10мин\nполе 9х9 ячеек', variable=self.__result_level, value=0)
        # self.__newbie_radiobutton_label = tk.Frame(self, bg='gray', width=471, height=351)
        # чекбокс "Любитель"
        self.__amateur_radiobutton = tk.Radiobutton(self.__frame_level, text='Любитель\n40мин\nполе 16х16 ячеек', variable=self.__result_level, value=1)
        # self.__amateur_radiobutton_label = tk.Frame(self, bg='gray', width=471, height=351)
        # чекбокс "Профессионал"
        self.__professional_radiobutton = tk.Radiobutton(self.__frame_level, text='Профессионал\n99мин\nполе 16х30 ячеек', variable=self.__result_level, value=2)
        # self.__professional_radiobutton_label = tk.Frame(self, bg='gray', width=471, height=351)
        # чекбокс "Особый" - назначение параметров вручную
        self.__special_radiobutton = tk.Radiobutton(self.__frame_level, text='Особый', variable=self.__result_level, value=3)
        # self.__special_radiobutton_label = tk.Frame(self, bg='gray', width=471, height=351)

        # # чекбокс "Особый" - назначение параметра высота
        # self.__special_radiobutton_height_field = tk.Frame(self, bg='gray', width=471, height=351)
        # self.__special_radiobutton_height_field_label = tk.Frame(self, bg='gray', width=471, height=351)
        # # чекбокс "Особый" - назначение параметра ширина
        # self.__special_radiobutton_width_field = tk.Frame(self, bg='gray', width=471, height=351)
        # self.__special_radiobutton_width_field_label = tk.Frame(self, bg='gray', width=471, height=351)
        # # чекбокс "Особый" - назначение параметра количество мин
        # self.__special_radiobutton_mine_count_field = tk.Frame(self, bg='gray', width=471, height=351)
        # self.__special_radiobutton_mine_count_field_label = tk.Frame(self, bg='gray', width=471, height=351)

    def __init_button(self):
        self.button_ok = tk.Button(self, text="Ок", command=self.__menu_options)
        self.button_cancel = tk.Button(self, text="Отмена", command=self.destroy)

    def __menu_options(self):
        print(f'настройки === {self.__result_level.get()}')


class AboutProgramWindow(MenuWindowMixin):

    def __init__(self, parent: tk.Menu):
        super().__init__(parent)
        self._program_version: str = ''
        self.__init_window_body()
        self.__init_button()

    def start(self):
        super().start()
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
