from _tk import View


def _program_version() -> str:
    with open('Version.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    game_window = View()
    game_window.program_version = _program_version()
    game_window.start()
