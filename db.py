import sqlite3


class ExpenseDB:
    def __init__(self):

        self.my_db = "expense.db"

    def create_users_table(self):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                user_id INTEGER PRIMARY KEY,
                                user_name VARCHAR(20) NOT NULL UNIQUE);""")

            print("SQLite users table created")
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("Error while creating users table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def create_expenses_table(self):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS expenses(
                                fk_user_id INTEGER NOT NULL,
                                exp_id INTEGER PRIMARY KEY,
                                exp_date DATE NOT NULL,
                                exp_category TEXT NOT NULL,
                                exp_cost INTEGER NOT NULL,
                                FOREIGN KEY (fk_user_id) REFERENCES users (user_id)
                                    ON UPDATE CASCADE
                                    ON DELETE CASCADE
                                    );""")
            print("SQLite expenses table created")
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("Error while creating expenses table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def insert_users_data(self, user_col: tuple):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = """INSERT INTO users (user_name) VALUES
                                            (?);"""
            cur.execute(query, user_col)
            conn.commit()
            print("New record was added to users table")
            conn.close()
        except sqlite3.IntegrityError as error:
            print("This name is already exist! User should be unique")
        except sqlite3.Error as error:
            print("Error while inserting new record in users table")
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def insert_expenses_data(self, cols: tuple):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""INSERT OR IGNORE INTO expenses
                                            (fk_user_id, exp_date, exp_category, exp_cost) VALUES
                                            (?, ?, ?, ?);"""
            cur.execute(query, cols)
            conn.commit()
            print("New record was added to expenses table")
            conn.close()
        except sqlite3.Error as error:
            print("Error while inserting new record in expenses table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def change_user_name(self, user_id: int, new_user_name: str):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""UPDATE users SET user_name = '{new_user_name}'
                    WHERE user_id = {user_id}"""
            cur.execute(query)
            conn.commit()
            print(f"User was successfully renamed to: {new_user_name}")
            conn.close()
        except sqlite3.Error as error:
            print("Failed to updated user name", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_all_table_data(self, table_name: str):
        """Read user table. Or read expenses table for getting fk_user_id"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"SELECT * FROM {table_name};"
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row
            conn.commit()
            print(f"Read all {table_name} table data successfully")
            conn.close()
        except sqlite3.Error as error:
            print(f"Failed to read date from sqlite {table_name} table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def select_category_for_concrete_user(self, fk_id: int):
        """Show category for specific user"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""SELECT DISTINCT	exp_category FROM expenses
                        WHERE fk_user_id = {fk_id};"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row
            conn.commit()
            print(f"Categories for concrete user was selected")
            conn.close()
        except sqlite3.Error as error:
            print(f"Failed to select concrete user's categories", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def select_category_for_all_users(self):
        """Show category for all users"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"SELECT DISTINCT exp_category FROM expenses;"
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row
            conn.commit()
            print(f"Categories for all users was selected")
            conn.close()
        except sqlite3.Error as error:
            print(f"Failed to select all users categories", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_expenses_for_all_users(self):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""SELECT exp_id, user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        ORDER BY exp_date;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row
            conn.commit()
            print("Read expenses for all users")
            conn.close()
        except sqlite3.Error as error:
            print(f"Failed to read date from sqlite expenses for all users", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_expenses_for_concrete_user(self, fk_id: int):
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""SELECT exp_id, user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE fk_user_id = {fk_id}
                        ORDER BY exp_date;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row
            conn.commit()
            print("Read expenses for concrete user")
            conn.close()
        except sqlite3.Error as error:
            print(f"Failed to read date from sqlite expenses for concrete user", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_user_exp_by_period(self, user_id: int, period: str):
        """Show expenses of concrete user for specific period."""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE user_id = {user_id} AND (exp_date >= '{period}')
                        ORDER BY exp_date;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read user's data for specific period")

        except sqlite3.Error as error:
            print(f"Failed to read user's data for specific period", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_all_exp_by_period(self, period: str):
        """Show expenses of all users for specific period."""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE exp_date > '{period}'
                        ORDER BY exp_date;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read all users data for specific period")

        except sqlite3.Error as error:
            print(f"Failed to read all users data for specific period", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_user_exp_by_category(self, user_id: int, category: str):
        """Show expenses of concrete user by category."""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE user_id = {user_id} AND (exp_category IN ('{category}'));"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read user's data by category")

        except sqlite3.Error as error:
            print(f"Failed to read user's data by category", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_all_exp_by_category(self, category: str):
        """Show expenses of all users by category."""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, exp_cost FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE exp_category IN ('{category}');"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read all users data by category")

        except sqlite3.Error as error:
            print(f"Failed to read all users data by category", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_sum_concrete_user_expenses(self, user_id: int, period: str):
        """Select sum of concrete user expenses by period, category"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, SUM(exp_cost) FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE user_id = {user_id} AND (exp_date >= '{period}')
                        GROUP BY user_name, exp_date, exp_category;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read sum of concrete user expenses by period, category")

        except sqlite3.Error as error:
            print(f"Failed to read sum of concrete user expenses by period, category", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def read_sum_all_users_expenses(self, period: str):
        """Select sum of all users expenses by period"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            # query sorted by exp_date
            query = f"""SELECT user_name, exp_date, exp_category, SUM(exp_cost) FROM expenses
                        LEFT OUTER JOIN users ON users.user_id = expenses.fk_user_id
                        WHERE exp_date >= '{period}'
                        GROUP BY user_name, exp_date, exp_category;"""
            cur.execute(query)
            results = cur.fetchall()
            for row in results:
                yield row

            conn.close()
            print(f"Read sum of all users expenses by period, category")

        except sqlite3.Error as error:
            print(f"Failed to read sum of all users expenses by period, category", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_exp_last_record(self):
        """Delete last row of expenses table"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"DELETE FROM expenses WHERE exp_id = (SELECT MAX(exp_id) FROM expenses);"
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Last record was deleted from expenses table!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete last record from expenses table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_specific_record(self, table_name: str, id_name: str, value: int):
        """Delete specific row of expenses table"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"DELETE FROM {table_name} WHERE {id_name} = {value};"
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Specific record was deleted from {table_name} table!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete specific record from {table_name} table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_exp_by_id_category(self, id_num: int, category: str):
        """Delete expenses of concrete user by category"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""DELETE FROM expenses
                        WHERE fk_user_id = {id_num} AND (exp_category IN ('{category}'));"""
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Deleted rows by user_id and category!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete rows by user_id and category!!!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_exp_by_category(self, category: str):
        """Delete all expenses data by category"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""DELETE FROM expenses
                        WHERE exp_category IN ('{category}');"""
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Deleted rows of all users by category!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete rows of all users by category!!!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")


    def delete_exp_by_id_period(self, id_num: int, period: str):
        """Delete all expenses data of concrete user by period"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""DELETE FROM expenses
                        WHERE fk_user_id = {id_num}  AND (exp_date >= '{period}');"""
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Deleted rows by user_id and period!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete rows by user_id and period!!!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_exp_by_period(self, period: str):
        """Delete all expenses data by category"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""DELETE FROM expenses
                        WHERE exp_date >= '{period}';"""
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Deleted rows of all users by category!!!")
        except sqlite3.Error as error:
            print(f"Failed to delete rows of all users by category!!!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def delete_table(self, table_name: str):
        """Clear table data"""
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"""DELETE FROM {table_name};"""
            cur.execute(query)
            conn.commit()
            conn.close()
            print(f"Clear table!!!")
        except sqlite3.Error as error:
            print(f"Failed to clear table!!!", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")

    def drop_table(self, table_name):
        # Delete table
        try:
            conn = sqlite3.connect(self.my_db)
            cur = conn.cursor()
            query = f"DROP TABLE IF EXISTS {table_name};"
            cur.execute(query)
            conn.commit()
            conn.close()
            print("expenses table was deleted !!!")
        except sqlite3.Error as error:
            print("Failed to delete expenses table", error)
        finally:
            if conn:
                conn.close()
                print("The SQLite connection is closed")
