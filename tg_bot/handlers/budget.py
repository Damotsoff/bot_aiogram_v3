from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from tg_bot.states import ChooseBudgetOption, SetIncomeExpenses, EnterBudget


budget_router = Router()


@budget_router.message(Command("budget"))
async def cmd_budget(message: types.Message, state: FSMContext):
    await message.answer(
        """
Welcome to the Personal Finance Tracker Bot.

Choose an option:
1. Add Income and Expenses
2. Set Budget
3. View Summary
"""
    )
    await state.set_state(ChooseBudgetOption)


@budget_router.message(
    ChooseBudgetOption,
    F.text.startswith("1"),
)
async def choose_add_income_expenses(message: types.Message, state: FSMContext):
    await message.answer("Enter the amount of income")
    await state.set_state(SetIncomeExpenses.AddIncome)


@budget_router.message(
    SetIncomeExpenses.AddIncome,
    # F.text.isdigit(),
    F.text.as_("income"),
)
async def enter_income(message: types.Message, state: FSMContext, income: int):
    await state.update_data(income=int(income))
    await message.answer("Enter the amount of expenses")
    await state.set_state(SetIncomeExpenses.AddExpenses)


@budget_router.message(
    SetIncomeExpenses.AddExpenses,
    F.text.isdigit(),
    F.text.cast(int).as_("expenses"),
)
async def enter_expenses(message: types.Message, state: FSMContext, expenses: int):
    await state.update_data(expenses=expenses)
    await message.answer("Thank you for entering the data.")
    await cmd_budget(message, state)


@budget_router.message(ChooseBudgetOption, F.text.startswith("2"))
async def choose_set_budget(message: types.Message, state: FSMContext):
    await message.answer("Enter the amount of budget")
    await state.set_state(EnterBudget)


@budget_router.message(
    EnterBudget,
    F.text.isdigit(),
    F.text.cast(int).as_("budget"),
)
async def enter_budget(message: types.Message, state: FSMContext, budget: int):
    await state.update_data(budget=budget)
    await message.answer("Thank you for entering the budget.")
    await cmd_budget(message, state)


@budget_router.message(StateFilter(SetIncomeExpenses, EnterBudget))
async def enter_income_expenses_invalid(message: types.Message):
    await message.reply("Invalid input. Please enter a number.")


@budget_router.message(ChooseBudgetOption, F.text.startswith("3"))
async def choose_view_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()
    income = data.get("income")
    expenses = data.get("expenses")
    budget = data.get("budget")
    if not data:
        await message.answer("You have not entered any data yet.")
        await cmd_budget(message, state)
        return

    if not income:
        await message.answer("You have not entered any income yet.")
        await choose_add_income_expenses(message, state)
        return

    if not expenses:
        await message.answer("You have not entered any expenses yet.")
        await message.answer("Enter the amount of expenses")
        await state.set_state(SetIncomeExpenses.AddExpenses)
        return

    if not budget:
        await message.answer("You have not entered any budget yet.")
        await choose_set_budget(message, state)
        return

    balance = income - expenses
    summary = f"""
💰 Income: {income}
💸 Expenses: {expenses}
📊 Budget: {budget}
💼 Balance: {balance}
"""
    if balance < 0:
        summary += f"🚨 You are in debt by {abs(balance)}\n"
    if expenses > budget:
        summary += f"🚨 You are over budget by {expenses - budget}\n"

    summary += "If you want to clear the data, enter /clear\n"
    summary += "If you want to exit, enter /exit\n"
    await message.answer(summary)


@budget_router.message(Command("clear"))
async def clear(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Data cleaned!")


@budget_router.message(Command("exit"))
async def exit_state(message: types.Message, state: FSMContext):
    await state.storage.close()
    await message.answer("storage exit")
