from aiogram import F, Bot, types, Router
from aiogram.fsm.state import State, StatesGroup

budget_router = Router()


ChooseBudgetOption = State("ChooseBudgetOption")
EnterBudget = State("EnterBudget")
ViewSummary = State("ViewSummary")


class SetIncomeExpenses(StatesGroup):
    AddIncome = State()
    AddExpenses = State()
