import sys
import re
from db import ExpenseDB
from view_console import ViewConsole

from datetime import datetime, date


class Controller:
    def __init__(self):
        self.db = ExpenseDB()
        self.view = ViewConsole()

    def match_start_options(self):
        self.view.start_options()
        opt = input("Choose option: ")
        match opt:
            case "1":
                self.match_add_options()
            case "2":
                self.match_read_options()
            case "3":
                self.match_delete_options()
            case "q" | "quit":
                sys.exit()
            case _:
                print("Incorrect choice! Try again!")
                self.match_start_options()

    def match_add_options(self):
        self.view.add_options()
        opt = input("Choose option: ")
        match opt:
            case "1":
                print('Add username: ')
                validated_username = (self.validate_word(),)  # convert in tuple for quering
                print(validated_username)
                self.db.insert_users_data(validated_username)
            case "2":
                validated_expenses = self.validate_expenses_input()
                validated_expenses.insert(0, str(self.get_fk_user_id()))
                validated_expenses_tuple = tuple(validated_expenses)  # convert in tuple for quering
                self.db.insert_expenses_data(validated_expenses_tuple)
            case "3":
                fk_user_id = self.get_fk_user_id()
                print('Change username: ')
                update_name = self.validate_word()
                self.db.change_user_name(fk_user_id, update_name)

            case "b" | "back":
                self.match_start_options()
            case "m" | "menu":
                self.match_start_options()
            case "q" | "quit":
                sys.exit()
            case _:
                print("Incorrect choice! Try again!")
                self.match_add_options()

    def match_read_options(self):
        self.view.read_options()
        opt = input("Choose option: ")
        match opt:
            case "1":
                users_data = self.db.read_all_table_data('users')
                self.view.show_users_table(users_data)
            case "2":
                expences_data = self.db.read_expenses_for_all_users()
                self.view.show_expenses_data(expences_data)
            case "3":
                fk_user_id = self.get_fk_user_id()
                self.view.show_expenses_data(self.db.read_expenses_for_concrete_user(fk_user_id))
            case "4":
                fk_user_id = self.get_fk_user_id()
                print(fk_user_id)
                print('Watch expenses of concrete user by period: ')
                specific_period = self.choose_display_date()
                self.view.show_expenses_by_period(self.db.read_user_exp_by_period(fk_user_id, specific_period))
            case "5":
                print('Watch expenses of all users by period: ')
                specific_period = self.choose_display_date()
                self.view.show_expenses_by_period(self.db.read_all_exp_by_period(specific_period))
            case "6":
                fk_user_id = self.get_fk_user_id()
                self.view.show_categories_only(self.db.select_category_for_concrete_user(fk_user_id))
                print("Watch expenses of concrete user by category.\nInput category:")
                validated_category = self.get_category(fk_user_id)
                self.view.show_expenses_category(self.db.read_user_exp_by_category(fk_user_id, validated_category))
            case "7":
                self.view.show_categories_only(self.db.select_category_for_all_users())
                print('Watch expenses of all users by category.\nInput category:')
                validated_category = self.get_category()
                self.view.show_expenses_category(self.db.read_all_exp_by_category(validated_category))
            case "8":
                fk_user_id = self.get_fk_user_id()
                print(fk_user_id)
                print('Watch sum expenses of concrete user by period, category: ')
                specific_period = self.choose_display_date()
                print(specific_period)
                self.view.show_sum_expenses_by_period(
                    self.db.read_sum_concrete_user_expenses(fk_user_id, specific_period))
            case "9":
                specific_period = self.choose_display_date()
                print(specific_period)
                self.view.show_sum_expenses_by_period((self.db.read_sum_all_users_expenses(specific_period)))
            case "b" | "back":
                self.match_start_options()
            case "m" | "menu":
                self.match_start_options()
            case "q" | "quit":
                sys.exit()
            case _:
                print("Incorrect choice! Try again!")
                self.match_read_options()

    def match_delete_options(self):
        self.view.delete_options()
        opt = input("Choose option: ")
        match opt:
            case "1":
                self.db.delete_exp_last_record()
            case "2":
                self.db.delete_specific_record('expenses', 'exp_id', self.get_row_id())
            case "3":
                self.choice_for_deleting_user_rows()
            case "4":
                self.db.delete_table("expenses")
            case "5":
                self.db.delete_table("users")
            case "6":
                fk_user_id = self.get_fk_user_id()
                print("Delete expenses of concrete user by category.\nInput category:")
                validated_category = self.get_category(fk_user_id)
                self.db.delete_exp_by_id_category(fk_user_id, validated_category)
            case "7":
                self.db.delete_exp_by_category(self.get_category())
            case "8":
                fk_user_id = self.get_fk_user_id()
                valid_date = self.validate_date()
                self.db.delete_exp_by_id_period(fk_user_id, valid_date)
            case "9":
                valid_date = self.validate_date()
                self.db.delete_exp_by_period(valid_date)
            case "b" | "back":
                self.match_start_options()
            case "m" | "menu":
                self.match_start_options()
            case "q" | "quit":
                sys.exit()
            case _:
                print("Incorrect choice! Try again!")
                self.match_delete_options()

    def get_category(self, fk_user_id=None):
        """Getting category with fk_user_id or without"""
        if fk_user_id:
            cat_list = list(self.db.select_category_for_concrete_user(fk_user_id))
            self.view.show_categories_only(self.db.select_category_for_concrete_user(fk_user_id))
        else:
            cat_list = list(self.db.select_category_for_all_users())
            self.view.show_categories_only(self.db.select_category_for_all_users())

        cat_list_for_valid = [item[0] for item in cat_list]
        print(cat_list_for_valid)
        for _ in range(3):
            try:
                print("Input category: ")
                cat = self.validate_word()

                if cat in cat_list_for_valid:
                    return cat
                else:
                    print("This category does not exist")
            except ValueError:
                print("Your input is wrong")

    def get_row_id(self):
        """Getting row id for deleting from expenses table"""
        expenses_data = list(self.db.read_expenses_for_all_users())

        self.view.show_expenses_data(self.db.read_expenses_for_all_users())
        row_ids = [item[0] for item in expenses_data]
        print(row_ids)
        for _ in range(3):
            try:
                row_id = int(input("Choose row id to delete: \n"))

                if row_id in row_ids:
                    return row_id
                else:
                    print("This row id does not exist")
            except ValueError:
                print("Your input is not a number")

    def get_fk_user_id(self) -> int:
        """Getting for defining user. Get foreign key"""
        users_data = list(self.db.read_all_table_data('users'))
        # Display users
        self.view.show_users_table(users_data)
        users_fk_id = [item[0] for item in users_data]
        for _ in range(3):
            try:
                fk_id = int(input("Choose user by id after 'User_': \n"))

                if fk_id in users_fk_id:
                    return fk_id
                else:
                    print("This user does not exist")

            except ValueError:
                print("Your input is not a number")

    def choose_display_date(self):
        """Perform date options for show or delete operations"""
        self.view.show_date_options()
        for _ in range(3):
            try:
                define_exp_period = input()
                match define_exp_period:
                    case "1":
                        return self.get_day_period()
                    case "2":
                        return self.get_month_period()
                    case "3":
                        return self.get_year_period()

            except ValueError:
                print("Your choice is wrong! Try again")

    @staticmethod
    def get_day_period():
        return date.today().strftime("%d.%m.%y")

    @staticmethod
    def get_month_period():
        first_day_of_month = datetime.today().replace(day=1).date()
        dotted_first_day_of_month = first_day_of_month.strftime("%d.%m.%Y")
        return dotted_first_day_of_month

    @staticmethod
    def get_year_period():
        first_day_of_year = datetime.today().replace(day=1, month=1).date()
        dotted_first_day_of_year = first_day_of_year.strftime("%d.%m.%Y")
        return dotted_first_day_of_year

    def validate_date(self):
        """Validate single date"""
        for _ in range(3):
            try:
                date_input = input("Enter date in format [dd.mm.yyyy]: \n")
                print([date_input])
                if date_input in ('q', 'quit'):
                    break
                pattern = r"^\s*((\d{2}[^a-zA-Z\d\s]\d{2}[^a-zA-Z\d\s](?:20[1-1][0-9]|200[0-9]|202[0-1]))\s*)$"

                dotted_date = self.replace_date_with_dots(pattern, date_input)
                self.compare_dates(dotted_date)

            except AttributeError:
                print("Try Again! Something wrong with date")
            except ValueError:
                print("Wrong day or month. Try again!")
            else:
                print(dotted_date)
                return dotted_date

    @staticmethod
    def validate_word():
        for _ in range(3):
            try:
                word = input()
                if word in ('q', 'quit'):
                    break

                pat = r"^[a-zA-Z_][a-zA-Z0-9_]+$"  # work reg expression
                m = re.match(pat, word)
                group = m.group()

            except AttributeError:
                print("Try Again or enter: q, quit for exit")
            # except ValueError as error:
            #     print(error, "Wrong input??")
            else:
                return group

    def validate_expenses_input(self) -> list:
        """Validate user input in specific format"""
        for _ in range(3):
            try:
                expenses_input = input("Enter expense in format [dd.mm.yyyy] [category] - [expense]\n"
                                       "                                 or  [category] - [expense]:\n")
                if expenses_input in ('q', 'quit'):
                    break
                # regex for validation string in format: dd.mm.yyyy alphanumeric - number
                if len(expenses_input.split()) == 4:
                    pattern = r"^\s*((\d{2}[^a-zA-Z\d\s]\d{2}[^a-zA-Z\d\s](?:20[1-1][0-9]|200[0-9]|202[0-1]))" \
                              r"(\s+[a-zA-Z_][a-zA-Z0-9_]+\s+)(?:-)(\s+[1-9][0-9]*|[0]?)\s*)$"

                    dotted_date_and_expenses = self.replace_date_with_dots(pattern, expenses_input)

                    expenses_data_list = dotted_date_and_expenses.split()
                    expenses_data_list.pop(-2)  # remove '-' from list

                    # compare input date with today date
                    # input date can't be bigger than today date
                    self.compare_dates(expenses_data_list[0])
                    return expenses_data_list
                if len(expenses_input.split()) == 3:
                    pattern = r"^(\s*[a-zA-Z_][a-zA-Z0-9_]+\s+)(?:-)(\s+[1-9][0-9]*|[0]?)\s*$"

                    m = re.match(pattern, expenses_input)
                    group = m.group()

                    expenses_data_list = group.split()
                    expenses_data_list.pop(-2)  # remove '-' from list
                    expenses_data_list.insert(0, date.today().strftime("%d.%m.%Y"))
                    print(expenses_data_list)
                    # self.compare_dates(expenses_data_list[0])
                    return expenses_data_list
            except AttributeError:
                print("Try Again!")
            except ValueError:
                print("Wrong input")
            # else:
            #     return expenses_data_list

    @staticmethod
    def compare_dates(input_date: str):
        """The date input can not be bigger than today date"""
        format_date = "%d.%m.%Y"
        input_date_obj = datetime.strptime(input_date, format_date).date()

        today_date = date.today()
        if input_date_obj > today_date:
            raise ValueError("Date should not be more than current.")

    @staticmethod
    def replace_date_with_dots(date_pattern, inp_date):
        """Replace symbols between digits in date with dots"""
        inp_date = inp_date.strip()
        m = re.match(date_pattern, inp_date)
        group = m.group()
        group = re.sub("[\W?]", ".", group, 2)  # replaces single symbols in date with dots
        return group

    def choice_for_deleting_user_rows(self):
        """Method for deleting all expenses data of concrete user.
            Without or with deleting user from db"""

        choose_user = self.get_fk_user_id()
        self.view.show_options_for_deleting_rows()
        for _ in range(3):
            try:
                choice = input("Choose deleting option: ")
                if choice == "1":
                    return self.db.delete_specific_record('expenses', 'fk_user_id', choose_user)
                elif choice == "2":
                    return self.db.delete_specific_record('users', 'user_id', choose_user)
                else:
                    print("Wrong choice! Try again.")

            except ValueError:
                print("Your input is not a number")

    def get_last_row_drop_id(self):
        """Get last row of expenses table"""
        last_row_id = list(self.db.read_all_table_data("expenses"))[-1][1]
        return last_row_id

    def run(self):
        # Creating tables
        self.db.create_users_table()
        self.db.create_expenses_table()

        self.match_start_options()
