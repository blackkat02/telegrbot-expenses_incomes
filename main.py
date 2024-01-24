TOCEN_BOT = "6196116707:AAF9gW5hSTbcm_NIR_Xpvn_9osJ2QKQpzXM"
user_data_expensess = {category: dict() for category in ["food", "service", "transportation"]}
#from typing import Tuple, Any, List
import json
from collections import defaultdict
import calendar
import logging
from datetime import datetime, timedelta
from functools import wraps
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler,  Updater, MessageHandler#, Filters
from decimal import Decimal

user_data_operation = defaultdict(dict)
user_data = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start" was triggered!')
    # markup = types.InlineKeyboardMarkup
    # markup.add(types.InlineKeyboardButton('категорія витрат 1'))
    await update.message.reply_text(
        "Welcome to my Expenses List Bot!\n"
        "Commands:\n"
        "list and add expense categories: /start_add\n"
        "Start list: /start_list\n"
        "Add list of expense categories: /add_list_of_expense_categories\n"
        "Remove expenses: /remove_expenses <expenses number>\n"
        "Clear expenses: /clear_expenses\n"
        "Start list income: /start_list_income\n"
        "Adding cat_1 income: /add_income <cat_1 income> <sum income> [data income]\n"
        "Adding cat_2 income: /add_income <cat_2 income> <sum income> [data income]\n"
        "list income: /list_income\n"
        "Remove income: /remove_income <income number>\n"
        "Clear income: /clear_income\n"
    )


async def add_list_of_expense_categories(update: Update, context: CallbackContext) -> None:
    logging.info('Command "list_of_expense_categories" was triggered!')
    await update.message.reply_text(
        'list of expense categories: \n'
        'Food: /add_food_expenses <sum expenses>\n'
        'Service: /add_service_expenses <sum expenses>\n'
        'Transportation: /add_transportation_expenses <sum expenses>\n'
    )


async def start_add(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start_add" was triggered!')
    await update.message.reply_text(
        "Commands: \n"
        "Adding food expenses: /add_food_expenses <sum expenses> \n"
        "Adding service expenses: /add_service_expenses <sum expenses>\n"
        "Adding expenses transportation: /add_transportation_expenses <sum expenses>\n"
    )


async def start_list(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start_list" was triggered!')
    await update.message.reply_text(
        "Commands: \n"
        "List expenses: /list_expenses\n"
        "list expenses weeks: /list_expenses_weeks\n"
        "list expenses weeks: /list_expenses_months\n"
        "List food expenses full: /list_food_expenses_full\n"
        "List food expenses day: /list_food_expenses_day\n"
        "List food expenses week: /list_food_expenses_week\n"
        "List food expenses month:/list_food_expenses_month\n"
        "List food expenses year: /list_food_expenses_year\n"
        "List service expenses full: /list_service_expenses_full\n"
        "List service expenses day: /list_service_expenses_day\n"
        "List service expenses week: /list_service_expenses_week\n"
        "List service expenses month: /list_service_expenses_month\n"
        "List service expenses year: /list_service_expenses_year\n"
        "List transportation expenses day: /list_transport_expenses_full\n"
        "List transportation expenses day: /list_transport_expenses_day\n"
        "List transportation expenses week: /list_transport_expenses_week\n"
        "List transportation expenses week: /list_transport_expenses_month\n"
        "List transportation expenses week: /list_transport_expenses_year\n"
    )


async def start_list_income(update: Update, context: CallbackContext) -> None:
    logging.info('Command "start_list" was triggered!')
    await update.message.reply_text(
        "Commands: \n"
        "list sales income_day: /list_sales_income_day\n"
        "list_sales_income_week: /list_sales_income_week\n"
        "list_sales_income_month: /list_sales_income_month\n"
        "list_sales_income_year: /list_sales_income_year\n"
        "list_sales_income_day: /list_sales_income_full\n"

        "list sales income_day: /list_rental_income_day\n"
        "list_sales_income_week: /list_rental_income_week\n"
        "list_sales_income_month: /list_rental_income_month\n"
        "list_sales_income_year: /list_rental_income_year\n"
        "list_sales_income_day: /list_rental_income_full\n"
    )


def process_add_operation(type_transaction, type_operation):
    def decorator(func):
        @wraps(func)
        async def add_operation(update: Update, context: CallbackContext, *args, **kwargs) -> None:
            user_id = update.message.from_user.id
            transaction_amount = ' '.join(context.args)
            date_operation = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            operation = type_operation, transaction_amount, date_operation

            if type_transaction not in user_data:
                user_data[type_transaction] = {}

            if user_id not in user_data[type_transaction]:
                user_data[type_transaction][user_id] = []

            user_data[type_transaction][user_id].append(operation)
            await update.message.reply_text(f"Added {type_operation} operation: {operation}")
            return

        return add_operation

    return decorator



@process_add_operation("expenses", "food")
async def add_food_expenses(update: Update, context: CallbackContext) -> None:
    return


@process_add_operation("expenses", "service")
async def add_service_expenses(update: Update, context: CallbackContext) -> None:
    return


@process_add_operation("expenses", "transportation")
async def add_transportation_expenses(update: Update, context: CallbackContext) -> None:
    return


@process_add_operation("income", "sales")
async def add_sales_income(update: Update, context: CallbackContext) -> None:
    return


@process_add_operation("income", "rental")
async def add_rental_income(update: Update, context: CallbackContext) -> None:
    return


def process_list_expenses(type_transaction, type_operation):
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            user_id = update.message.from_user.id

            try:
                if user_id not in user_data[type_transaction] or not user_data[type_transaction][user_id]:
                    await update.message.reply_text(f"You don't have any {type_transaction} transaction")
                    return
            except KeyError as e:
                # Handle the KeyError, you can log it or send an error message
                await update.message.reply_text(f"You don't have any {type_transaction} transaction")
                return

            return await func(update, context, *args, **kwargs)

        return wrapper

    return decorator



@process_list_expenses("expenses", "full")
async def list_expenses(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    result = '\n'.join([f"{i + 1}. {t}" for i, t in enumerate(user_data['expenses'][user_id])])
    await update.message.reply_text(result)


@process_list_expenses("expenses", "weeks")
async def list_expenses_weeks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    list_expenses_delta = []
    now = datetime.now()
    start_data = now - timedelta(weeks=1)

    for operation in user_data['expenses'][user_id]:
        expenses_date = datetime.strptime(operation[2], '%Y-%m-%d %H:%M:%S')
        if now >= expenses_date >= start_data:
            list_expenses_delta.append(operation)

    if not list_expenses_delta:
        await update.message.reply_text("You don't have any weekly expenses")
    else:
        result = '\n'.join(map(str, list_expenses_delta))
        await update.message.reply_text(f"List expenses weeks:\n{result}")


@process_list_expenses("expenses", "months")
async def list_expenses_months(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if not user_data.get('expenses'):
        await update.message.reply_text("You don't have any monthly expenses")
        return

    end_data = datetime.now()
    days_in_month = calendar.monthrange(end_data.year, end_data.month)[1]
    start_data = end_data - timedelta(days=days_in_month) - timedelta(days=1)

    list_delta = []
    for expenses in user_data['expenses'][user_id]:
        expenses_date = datetime.strptime(expenses[2], '%Y-%m-%d %H:%M:%S')
        if end_data >= expenses_date >= start_data:
            list_delta.append(expenses)

    if list_delta:
        result = '\n'.join(map(str, list_delta))
        await update.message.reply_text(f"List expenses month:\n{result}")
    else:
        await update.message.reply_text("You don't have any monthly expenses")


def list_type_expenses(type_transaction, type_operation):
    """

    :param type_transaction:
    :param type_operation:
    :return: user_data_operation[user_id][type_operation]
    """

    class Decorator:
        def __init__(self, func):
            self.func = func
            wraps(func)(self)

        async def __call__(self, update, context, *args, **kwargs):
            user_id = update.message.from_user.id

            # Use defaultdict to automatically create entries if they don't exist
            user_data_operation[user_id] = defaultdict(list)

            try:
                if user_id not in user_data[type_transaction] or not user_data[type_transaction][user_id]:
                    await update.message.reply_text(f"You don't have any {type_transaction} transaction")
                    return
            except KeyError as e:
                # Handle the KeyError, you can log it or send an error message
                await update.message.reply_text(f"You don't have any {type_transaction} transaction")
                return

#            if not user_data[type_transaction][user_id]:
 #               await update.message.reply_text(f"You don't have any {type_transaction} transaction")
  #              return

            for operation in user_data[type_transaction][user_id]:
                if operation[0] == type_operation:
                    user_data_operation[user_id][type_operation].append(operation)
                    print(user_data_operation[user_id][type_operation])

            if not user_data_operation[user_id][type_operation]:
                await update.message.reply_text(f"You don't have any {type_operation} operation")
                return

            return await self.func(update, context, *args, **kwargs)

    return Decorator


async def list_day(update, context, type_transaction=None, type_operation=None):
    user_id = update.message.from_user.id
    list_operation_delta = []
    end_data = datetime.now()
    start_data = end_data - timedelta(days=1)

    for operation in user_data[type_transaction][user_id]:
        operation_date = datetime.strptime(operation[2], '%Y-%m-%d %H:%M:%S')
        if operation[0] == type_operation and end_data >= operation_date >= start_data:
            list_operation_delta.append(operation)

    if list_operation_delta:
        result = '\n'.join(map(str, list_operation_delta))
        await update.message.reply_text(f"Daily {type_operation} {type_transaction}:\n{result}")
    else:
        await update.message.reply_text(f"You don't have any Daily {type_transaction} {type_operation}")


async def list_week(update: Update, context: CallbackContext, type_transaction=None, type_operation=None):
    user_id = update.message.from_user.id
    list_operation_delta = []
    end_data = datetime.now()
    start_data = end_data - timedelta(weeks=1)
    for operation in user_data[type_transaction][user_id]:
        operation_date = datetime.strptime(operation[2], '%Y-%m-%d %H:%M:%S')
        if operation[0] == type_operation and end_data >= operation_date >= start_data:
            list_operation_delta.append(operation)
    if list_operation_delta:
        result = '\n'.join(map(str, list_operation_delta))
        await update.message.reply_text(f"Weekly {type_operation} {type_transaction}:\n{result}")
    else:
        await update.message.reply_text(f"You don't have any Weekly {type_operation} {type_transaction}")


async def list_month(update: Update, context: CallbackContext, type_transaction=None, type_operation=None) -> None:
    user_id = update.message.from_user.id
    list_operation_delta = []
    end_data = datetime.now()
    days_in_month = calendar.monthrange(end_data.year, end_data.month)[1]
    start_data = end_data - timedelta(days=days_in_month) - timedelta(days=1)

    for operation in user_data[type_transaction][user_id]:
        operation_date = datetime.strptime(operation[2], '%Y-%m-%d %H:%M:%S')
        if operation[0] == type_operation and end_data >= operation_date >= start_data:
            list_operation_delta.append(operation)
    if list_operation_delta:
        result = '\n'.join(map(str, list_operation_delta))
        await update.message.reply_text(f"Monthly {type_operation} {type_transaction}:\n{result}")
    else:
        await update.message.reply_text(f"You don't have any Monthly {type_operation} {type_transaction}")


async def list_year(update, context, type_transaction=None, type_operation=None) -> None:
    user_id = update.message.from_user.id
    list_operation_delta = []
    end_data = datetime.now()
    start_data = end_data - timedelta(days=365)

    for operation in user_data[type_transaction][user_id]:
        operation_date = datetime.strptime(operation[2], '%Y-%m-%d %H:%M:%S')
        if operation[0] == type_operation and end_data >= operation_date >= start_data:
            list_operation_delta.append(operation)

    if list_operation_delta:
        result = '\n'.join(map(str, list_operation_delta))
        await update.message.reply_text(f"Yearly {type_operation} {type_transaction}:\n{result}")
    else:
        await update.message.reply_text(f"You don't have any Yearly {type_operation} {type_transaction}")


async def list_full(update, context, type_transaction=None, type_operation=None) -> None:
    user_id = update.message.from_user.id
    list_operation_delta = []

    for operation in user_data[type_transaction][user_id]:
        if operation[0] == type_operation:
            list_operation_delta.append(operation)

    if list_operation_delta:
        result = '\n'.join(map(str, list_operation_delta))
        await update.message.reply_text(f"Daily {type_operation} {type_transaction}:\n{result}")
    else:
        await update.message.reply_text(f"You don't have any Daily {type_transaction} {type_operation}")


@list_type_expenses("expenses", "food")
async def list_food_expenses_day(update: Update, context: CallbackContext) -> None:
    await list_day(update, context, type_transaction="expenses", type_operation="food")


@list_type_expenses("expenses", "food")
async def list_food_expenses_week(update: Update, context: CallbackContext) -> None:
    await list_week(update, context, type_transaction="expenses", type_operation="food")


@list_type_expenses("expenses", "food")
async def list_food_expenses_month(update: Update, context: CallbackContext) -> None:
    await list_month(update, context, type_transaction="expenses", type_operation="food")


@list_type_expenses("expenses", "food")
async def list_food_expenses_year(update, context) -> None:
    await list_year(update, context, type_transaction="expenses", type_operation="food")


@list_type_expenses("expenses", "food")
async def list_food_expenses_full(update, context) -> None:
    await list_full(update, context, type_transaction="expenses", type_operation="food")


@list_type_expenses("expenses", "service")
async def list_service_expenses_day(update: Update, context: CallbackContext) -> None:
    await list_day(update, context, type_transaction="expenses", type_operation="service")


@list_type_expenses("expenses", "service")
async def list_service_expenses_week(update: Update, context: CallbackContext) -> None:
    await list_week(update, context, type_transaction="expenses", type_operation="service")


@list_type_expenses("expenses", "service")
async def list_service_expenses_month(update: Update, context: CallbackContext) -> None:
    await list_month(update, context, type_transaction="expenses", type_operation="service")


@list_type_expenses("expenses", "service")
async def list_service_expenses_year(update, context) -> None:
    await list_year(update, context, type_transaction="expenses", type_operation="service")


@list_type_expenses("expenses", "service")
async def list_service_expenses_full(update, context) -> None:
    await list_full(update, context, type_transaction="expenses", type_operation="service")


@list_type_expenses("expenses", "transportation")
async def list_transport_expenses_day(update, context) -> None:
    await list_day(update, context, type_transaction="expenses", type_operation="transportation")


@list_type_expenses("expenses", "transportation")
async def list_transport_expenses_week(update: Update, context: CallbackContext) -> None:
    await list_week(update, context, type_transaction="expenses", type_operation="transportation")


@list_type_expenses("expenses", "transportation")
async def list_transport_expenses_month(update: Update, context: CallbackContext) -> None:
    await list_month(update, context, type_transaction="expenses", type_operation="transportation")
    return


@list_type_expenses("expenses", "transportation")
async def list_transport_expenses_year(update: Update, context: CallbackContext) -> None:
    await list_year(update, context, type_transaction="expenses", type_operation="transportation")


@list_type_expenses("expenses", "transportation")
async def list_transport_expenses_full(update: Update, context: CallbackContext) -> None:
    await list_full(update, context, type_transaction="expenses", type_operation="transportation")



@list_type_expenses("income", "sales")
async def list_sales_income_day(update: Update, context: CallbackContext) -> None:
    await list_day(update, context, type_transaction="income", type_operation="sales")


@list_type_expenses("income", "sales")
async def list_sales_income_week(update: Update, context: CallbackContext) -> None:
    await list_week(update, context, type_transaction="income", type_operation="sales")


@list_type_expenses("income", "sales")
async def list_sales_income_month(update: Update, context: CallbackContext) -> None:
    await list_month(update, context, type_transaction="income", type_operation="sales")


@list_type_expenses("income", "sales")
async def list_sales_income_year(update: Update, context: CallbackContext) -> None:
    await list_year(update, context, type_transaction="income", type_operation="sales")


@list_type_expenses("income", "sales")
async def list_sales_income_full(update: Update, context: CallbackContext) -> None:
    await list_full(update, context, type_transaction="income", type_operation="sales")


@list_type_expenses("income", "rental")
async def list_rental_income_day(update: Update, context: CallbackContext) -> None:
    await list_day(update, context, type_transaction="income", type_operation="rental")


@list_type_expenses("income", "rental")
async def list_rental_income_week(update: Update, context: CallbackContext) -> None:
    await list_week(update, context, type_transaction="income", type_operation="rental")


@list_type_expenses("income", "rental")
async def list_rental_income_month(update: Update, context: CallbackContext) -> None:
    await list_month(update, context, type_transaction="income", type_operation="rental")


@list_type_expenses("income", "rental")
async def list_rental_income_year(update: Update, context: CallbackContext) -> None:
    await list_year(update, context, type_transaction="income", type_operation="rental")


@list_type_expenses("income", "rental")
async def list_rental_income_full(update: Update, context: CallbackContext) -> None:
    await list_full(update, context, type_transaction="income", type_operation="rental")


def remove_oper(type_transaction):
    def decor_remove(func):
        async def remove_operations(update: Update, context: CallbackContext) -> None:
            user_id = update.message.from_user.id
            if not user_data[type_transaction][user_id]:
                await update.message.reply_text(f"You don't have any {type_transaction} to remove")
                return
            try:
                removed_idx = int(context.args[0]) - 1
                user_data[type_transaction][user_id].pop(removed_idx)
                await update.message.reply_text(f'{type_transaction} successfully removed')
            except (ValueError, IndexError):
                await update.message.reply_text(f'{user_id} You entered an invalid index')
                return
        return remove_operations
    return decor_remove

@remove_oper("expenses")
async def remove_expenses(update: Update, context: CallbackContext) -> None:
    pass  # Your implementation here


@remove_oper("income")
async def remove_income(update: Update, context: CallbackContext, type_transaction="income") -> None:
    pass


async def clear_expenses(update: Update, context: CallbackContext, type_transaction="expenses") -> None:
    user_id = update.message.from_user.id
    user_data[type_transaction][user_id] = []
    await update.message.reply_text("Cleared successfully")


async def clear_income(update: Update, context: CallbackContext, type_transaction="income") -> None:
    user_id = update.message.from_user.id
    user_data[type_transaction][user_id] = []
    await update.message.reply_text("Cleared successfully")


# def run():
def run():
    app = ApplicationBuilder().token(TOCEN_BOT).build()
    logging.info("Application built successfully!")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("add_food_expenses", add_food_expenses))
    app.add_handler(CommandHandler("add_service_expenses", add_service_expenses))
    app.add_handler(CommandHandler("add_transportation_expenses", add_transportation_expenses))
    app.add_handler(CommandHandler("add_sales_income", add_sales_income))
    app.add_handler(CommandHandler("add_rental_income", add_rental_income))
    app.add_handler(CommandHandler("start_add", start_add))
    app.add_handler(CommandHandler("add_list_of_expense_categories", add_list_of_expense_categories))
    app.add_handler(CommandHandler("start_list", start_list))
    app.add_handler(CommandHandler("list_expenses", list_expenses))
    app.add_handler(CommandHandler("list_expenses_weeks", list_expenses_weeks))
    app.add_handler(CommandHandler("list_expenses_months", list_expenses_months))
    app.add_handler(CommandHandler("list_food_expenses_full", list_food_expenses_full))
    app.add_handler(CommandHandler("list_food_expenses_day", list_food_expenses_day))
    app.add_handler(CommandHandler("list_food_expenses_week", list_food_expenses_week))
    app.add_handler(CommandHandler("list_food_expenses_month", list_food_expenses_month))
    app.add_handler(CommandHandler("list_food_expenses_year", list_food_expenses_year))
    app.add_handler(CommandHandler("list_sales_income_day", list_sales_income_day))
    app.add_handler(CommandHandler("list_sales_income_week", list_sales_income_week))
    app.add_handler(CommandHandler("list_sales_income_month", list_sales_income_month))
    app.add_handler(CommandHandler("list_sales_income_year", list_sales_income_year))
    app.add_handler(CommandHandler("list_sales_income_day", list_sales_income_full))
    app.add_handler(CommandHandler("list_service_expenses_full", list_service_expenses_full))
    app.add_handler(CommandHandler("list_service_expenses_day", list_service_expenses_day))
    app.add_handler(CommandHandler("list_service_expenses_week", list_service_expenses_week))
    app.add_handler(CommandHandler("list_service_expenses_month", list_service_expenses_month))
    app.add_handler(CommandHandler("list_service_expenses_year", list_service_expenses_year))
    app.add_handler(CommandHandler("list_transport_expenses_full", list_transport_expenses_full))
    app.add_handler(CommandHandler("list_transport_expenses_day", list_transport_expenses_day))
    app.add_handler(CommandHandler("list_transport_expenses_week", list_transport_expenses_week))
    app.add_handler(CommandHandler("list_transport_expenses_month", list_transport_expenses_month))
    app.add_handler(CommandHandler("list_transport_expenses_year", list_transport_expenses_year))
    app.add_handler(CommandHandler("list_sales_income_day", list_sales_income_day))
    app.add_handler(CommandHandler("list_sales_income_week", list_sales_income_week))
    app.add_handler(CommandHandler("list_sales_income_month", list_sales_income_month))
    app.add_handler(CommandHandler("list_sales_income_year", list_sales_income_year))
    app.add_handler(CommandHandler("list_sales_income_full", list_sales_income_full))
    app.add_handler(CommandHandler("list_rental_income_day", list_rental_income_day))
    app.add_handler(CommandHandler("list_rental_income_week", list_rental_income_week))
    app.add_handler(CommandHandler("list_rental_income_month", list_rental_income_month))
    app.add_handler(CommandHandler("list_rental_income_year", list_rental_income_year))
    app.add_handler(CommandHandler("list_rental_income_full", list_rental_income_full))
    app.add_handler(CommandHandler("remove_expenses", remove_expenses))
    app.add_handler(CommandHandler("clear_expenses", clear_expenses))
    app.add_handler(CommandHandler("start_list_income", start_list_income))
    app.add_handler(CommandHandler("remove_income", remove_income))
    app.add_handler(CommandHandler("clear_income", clear_income))

    app.run_polling()


if __name__ == '__main__':
    run()
