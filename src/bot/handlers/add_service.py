from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database.models import User, Service
from src.database.session import async_session_maker
from src.bot.keyboards.services import get_services_keyboard, get_cancel_keyboard
from src.bot.states.add_service import AddServiceStates
from src.core.security import security_service
from src.core.logger import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.message(F.text == "/add")
async def cmd_add(message: types.Message, state: FSMContext):
    """Команда /add - начало добавления сервиса"""
    await state.set_state(AddServiceStates.selecting_service)
    await message.answer(
        "🔌 <b>Добавление сервиса</b>\n\n"
        "Выберите сервис, который хотите добавить:",
        reply_markup=get_services_keyboard()
    )


@router.callback_query(F.data.startswith("add_service_"))
async def process_service_selection(
    callback: types.CallbackQuery,
    state: FSMContext
):
    """Обработка выбора сервиса"""
    service_name = callback.data.replace("add_service_", "")
    
    if service_name == "cancel":
        await state.clear()
        await callback.message.edit_text("❌ Добавление сервиса отменено")
        await callback.answer()
        return
    
    # Сохраняем выбранный сервис
    await state.update_data(selected_service=service_name)
    await state.set_state(AddServiceStates.entering_api_key)
    
    await callback.message.edit_text(
        f"🔑 <b>Введите API-ключ для {service_name.title()}</b>\n\n"
        "Отправьте ключ в следующем сообщении.\n"
        "Для отмены нажмите /cancel",
        reply_markup=get_cancel_keyboard()
    )
    await callback.answer()


@router.message(AddServiceStates.entering_api_key, F.text)
async def process_api_key_input(
    message: types.Message,
    state: FSMContext
):
    """Обработка ввода API-ключа"""
    api_key = message.text.strip()
    
    # Шифруем ключ
    encrypted_key = security_service.encrypt(api_key)
    
    # Сохраняем в состояние
    await state.update_data(api_key=encrypted_key)
    await state.set_state(AddServiceStates.confirming)
    
    await message.answer(
        "✅ <b>Данные получены!</b>\n\n"
        "Нажмите /confirm для завершения или /cancel для отмены",
        reply_markup=get_cancel_keyboard()
    )


@router.message(F.text == "/confirm")
async def cmd_confirm(message: types.Message, state: FSMContext):
    """Подтверждение добавления сервиса"""
    current_state = await state.get_state()
    
    if current_state != AddServiceStates.confirming.state:
        await message.answer("❌ Нет активных процессов для подтверждения")
        return
    
    # Получаем данные из состояния
    data = await state.get_data()
    service_name = data.get("selected_service")
    encrypted_key = data.get("api_key")
    tg_id = message.from_user.id
    
    if not all([service_name, encrypted_key]):
        await message.answer("❌ Ошибка: недостаточно данных")
        await state.clear()
        return
    
    # Сохраняем в БД
    async with async_session_maker() as session:
        # Находим пользователя
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        
        if not user:
            # Создаем нового пользователя
            user = User(tg_id=tg_id, username=message.from_user.username)
            session.add(user)
            await session.flush()
        
        # Создаем сервис
        service = Service(
            user_id=user.id,
            service_name=service_name,
            connection_type="api",
            credentials={"api_key": encrypted_key},
            is_active=True
        )
        session.add(service)
        await session.commit()
        
        service_id = service.id
    
    await state.clear()
    
    await message.answer(
        f"✅ <b>Сервис добавлен!</b>\n\n"
        f"Сервис: {service_name.title()}\n"
        f"ID: {service_id}\n\n"
        "Используйте /status для проверки баланса"
    )


@router.message(F.text == "/cancel")
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Отмена текущего процесса"""
    await state.clear()
    await message.answer("❌ Операция отменена")