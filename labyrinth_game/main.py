#!/usr/bin/env python3

from labyrinth_game import constants, player_actions, utils

game_state = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def process_command(game_state, command):
    parts = command.strip().lower().split()
    if not parts:
        return

    cmd = parts[0]
    arg = " ".join(parts[1:]) if len(parts) > 1 else None

    # Словарь простых команд (match-case не поддерживается в Python 3.9)
    simple_commands = {
        "help": lambda: player_actions.show_help(constants.COMMANDS),
        "h": lambda: player_actions.show_help(constants.COMMANDS),
        "look": lambda: utils.describe_current_room(game_state),
        "l": lambda: utils.describe_current_room(game_state),
        "inventory": lambda: player_actions.show_inventory(game_state),
        "i": lambda: player_actions.show_inventory(game_state),
    }

    if cmd in simple_commands:
        simple_commands[cmd]()
    elif cmd in ("go", "g"):
        if arg:
            player_actions.move_player(game_state, arg)
        else:
            print("Куда идти? Укажите направление.")
    elif cmd in ("take", "t"):
        if arg:
            player_actions.take_item(game_state, arg)
        else:
            print("Что взять? Укажите предмет.")
    elif cmd in ("use", "u"):
        if not arg:
            print("Что использовать? Укажите предмет.")
        elif arg in ("treasure_chest", "treasure chest"):
            if game_state["current_room"] == "treasure_room":
                utils.attempt_open_treasure(game_state)
            else:
                print("Здесь нет сундука с сокровищами.")
        else:
            player_actions.use_item(game_state, arg)
    elif cmd in ("solve", "s"):
        if game_state["current_room"] == "treasure_room":
            utils.attempt_open_treasure(game_state)
        else:
            utils.solve_puzzle(game_state)
    elif cmd in ("quit", "exit", "q"):
        print("Спасибо за игру!")
        game_state["game_over"] = True
    elif cmd in ("north", "south", "east", "west"):
        player_actions.move_player(game_state, cmd)
    else:
        print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    """
    Главная функция игры - точка входа.

    Запускает игровой цикл и обрабатывает команды игрока
    до окончания игры (победы или поражения).
    """
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game_over"]:
        command = player_actions.get_input()
        process_command(game_state, command)


if __name__ == "__main__":
    main()
