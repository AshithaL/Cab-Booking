import MySQLdb
from MySQLdb import Error
from Script import Schema
from Employee import Employee
from Admin import Admin

def sql_connection():
    """
    connection with sql database
    :return: True/False
    """
    try:
        mydb = MySQLdb.connect(host='localhost',
                               user='root',
                               passwd='nineleaps',
                               db='cab')
        print(mydb)
        return mydb
    except Error as e:
        print(e)

class Run:

    def __init__(self, connection):
        self.conn = connection

    def get_role(self, username, pswd):
        """
        Validate whether the email and password is of a valid user.
        :param username: email given by the user
        :param pswd: password given by the user
        :return: role_id/0
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * from users WHERE lower(username)='{}' and password='{}'"
                      .format(username, pswd))
            result = c.fetchone()
            if result is not None:
                return result[2]
            else:
                return 0
        except Exception as e:
            print(type(e), ": ", e)
            return 0

    def login_menu(self):
        """ Display Login options for users to choose.
        :return: True
        """
        print("LOGIN MENU")
        username = input("Username: ").lower()
        pswd = input("Password: ")

        role = self.get_role(username, pswd)

        if role == 22:
            Employee(self.conn).select(username)

        elif role == 11:
            Admin(self.conn).select(username)
        else:
            print("\nWrong Credentials!  Try again.")

            self.login_menu()

        return True


def main():
    """
    :return: True/False
    """
    try:
        conn = sql_connection()

        if conn is None:
            print("Error. Try again")
        else:
            Schema(conn).setup_admin()
            Schema(conn).create_tables()
            Run(conn).login_menu()
            conn.close()
            return True
    except Exception as e:
        print(type(e), ": ", e)

    return False


if __name__ == "__main__":
    main()