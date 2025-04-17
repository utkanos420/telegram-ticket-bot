from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter


class UserStates(StatesGroup):
    global_state = State()
    get_password = State()


class Anketa(StatesGroup):
    get_floor = State()
    get_auditory = State()
    get_trouble = State()
    description = State()
    result = State()
