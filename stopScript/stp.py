def input_listener(stop_event):
    """
    Поток, который слушает ввод пользователя.
    Если введено "Y" или "y", устанавливает флаг stop_event.
    """
    while not stop_event.is_set():
        user_input = input("Введите 'Y', чтобы остановить скрипт: ").strip().lower()
        if user_input == "y":
            print("\n🛑 Остановка скрипта...")
            stop_event.set()  # Устанавливаем флаг
            break