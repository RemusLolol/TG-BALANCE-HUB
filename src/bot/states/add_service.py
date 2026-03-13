from aiogram.fsm.state import State, StatesGroup


class AddServiceStates(StatesGroup):
    """Состояния для процесса добавления сервиса"""
    selecting_service = State()      # Выбор сервиса
    entering_api_key = State()       # Ввод API-ключа
    entering_api_secret = State()    # Ввод API-секрета (опционально)
    confirming = State()             # Подтверждение