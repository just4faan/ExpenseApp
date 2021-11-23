
class ViewConsole:

    @staticmethod
    def start_options():
        print("\t START OPTIONS")
        print("---------------")
        print("1. Add data")
        print("2. Show data")
        print("3. Delete data")

    @staticmethod
    def add_options():
        print("---------------")
        print("1. Add users")
        print("2. Add expenses data")
        print("3. Change user name")

    @staticmethod
    def read_options():
        print("---------------")
        print("1. Show all users")
        print("2. Show expenses of all users")
        print("3. Show expenses of concrete user")
        print("4. Show concrete expenses by period: day, month, year")
        print("5. Show all users expenses by period: day, month, year")
        print("6. Show concrete user expenses data by category")
        print("7. Show all users expenses data by category")
        print("8. Show sum of expenses of concrete user by period")
        print("9. Show sum of expenses of all users by period")

    @staticmethod
    def delete_options():
        print("---------------")
        print("1. Delete last expenses record")
        print("2. Delete specific expenses single record")
        print("3. Delete all expenses data of concrete user")

        print("4. Delete all expenses")
        print("5. Delete all users")
        print("6. Delete concrete user expenses by category")
        print("7. Delete all expenses data by category")
        print("8. Delete concrete user expenses by period")
        print("9. Delete all expenses data by period")

    @staticmethod
    def show_date_options():
        print("1. Day")
        print("2. Month")
        print("3. Year")

    @staticmethod
    def show_options_for_deleting_rows():
        print("1. Don't delete from users db")
        print("2. Delete from users db")

    @staticmethod
    def show_users_table(users_table_func):
        print("---------------")
        for val in list(users_table_func):
            print(f"User_{val[0]}:", val[1])

    # show expenses of concrete or all users
    @staticmethod
    def show_expenses_data(expenses_table_func):
        print("---------------")
        for row in list(expenses_table_func):
            print(row[0], row[1], row[2], row[3], row[4])

    @staticmethod
    def show_expenses_by_period(expenses_table_func):
        print("---------------")
        for row in list(expenses_table_func):
            print(row[0], row[1], row[2], row[3])

    @staticmethod
    def show_expenses_category(expenses_table_func):
        print("---------------")
        for row in list(expenses_table_func):
            print(row[0], row[1], row[2], row[3])

    @staticmethod
    def show_categories_only(list_of_categories):
        print("---------------")
        for row in list(list_of_categories):
            print(row[0])

    @staticmethod
    def show_sum_expenses_by_period(list_of_categories):
        print("---------------")
        for row in list(list_of_categories):
            print(row[0], row[1], row[2], row[3])
