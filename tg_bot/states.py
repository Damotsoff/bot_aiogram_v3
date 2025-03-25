from aiogram.fsm.state import State, StatesGroup




ChooseBudgetOption = State("ChooseBudgetOption")
EnterBudget = State("EnterBudget")
ViewSummary = State("ViewSummary")


class SetIncomeExpenses(StatesGroup):
    AddIncome = State()
    AddExpenses = State()
