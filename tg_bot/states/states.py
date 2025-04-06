from aiogram.fsm.state import State, StatesGroup


class Pay(StatesGroup):
    AddPayment = State()


class SupportStates(StatesGroup):
    waiting_for_support_text = State()


class StateBalance(StatesGroup):
    balance = State()


class SetCounters(StatesGroup):
    AddPosition = State()
    AddItem = State()
    AddPrice = State()


class ProductsStates(StatesGroup):
    AddProducts = State()


class DeleteProductState(StatesGroup):
    Position = State()
