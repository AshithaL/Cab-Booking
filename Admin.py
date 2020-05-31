import calendar
import datetime
import re
import uuid
import matplotlib.pyplot as plt
import pandas as pd

from cryptography.fernet import Fernet
import pandas as pd
import matplotlib.pyplot as plot
import SqlConnection as con
from MySQLdb import Error

class Admin:

    def __init__(self, connection):
        self.conn = connection

        # regular expression for validating username which is their email id
        self.regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"

    def select(self, username):

        option = {

            "1": ("Check total bookings", self.check_total_bookings),
            "2": ("Check booking of an emp", self.check_emp_booking),
            "3": ("Add new cab", self.add_new_cab),
            "4": ("Update Cab route & timings", self.update_cab),
            "5": ("Add Employee", self.add_employee),
            "6": ("Update Employee", self.update_employee),
            "7": ("Delete Employee", self.delete_employee),
            "8": ("Show Employees", self.show_employees),
            "9": ("Visualize", self.visualize)
        }

        ans = input("Choose:\n"
                "1.Check total bookings.\n"
                "2.Check booking of an employee.\n"
                "3.Add new cab.\n"
                "4.Update cab route and timings.\n"
                "5.Add Emplpyee.\n"
                "6.Update Employee.\n"
                "7.Visualize.\n")

        option.get(ans)[1](con)

    def check_total_bookings(self):
        """
                Show all bookings for a particular period.
                :return: True/False
                """
        from_date = input("From Date (YYYY-MM-DD): ")
        to_date = input("To Date (YYYY-MM-DD): ")

        try:
            c = self.conn.cursor()
            c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM Bookings  \
                               JOIN routes ON Routes.ID=bookings.route_ID \
                               JOIN cabs ON cabs.ID=routes.CAB_ID \
                               WHERE DATE>='{}' AND DATE<='{}'"
                      .format(from_date, to_date))
            result = c.fetchall()
            if len(result) > 0:
                print("\nBOOKING DETAILS\n---------------")
                print("\nCAB NO\tSOURCE\tDESTINATION\tDATE\tTIME\tOCCUPANCY\tSTATUS")
                print("------\t------\t-----------\t----\t----\t---------\t------")

                for row in result:
                    status = 'COMPLETED' if row[6] == 1 else 'CANCELED' if row[6] == 0 else 'UPCOMING'
                    print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}"
                          .format(row[7], row[10], row[11], row[3], row[4], row[5], status))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def check_emp_booking(self):
        """
                Show all bookings for a particular employee
                :return: True/False
                """
        emp_email = input("\nEmployee email: ")

        try:
            c = self.conn.cursor()
            c.execute("SELECT id FROM employees WHERE lower(email)='{}'".format(emp_email))
            emp_id = c.fetchone()
            if emp_id:
                c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM bookings  \
                                    JOIN routes ON routes.ID=bookings.ROUTE_ID \
                                    JOIN cabs ON cabs.ID=routes.CAB_ID WHERE emp_id={}"
                          .format(emp_id[0]))
                result = c.fetchall()
                if len(result) > 0:
                    print("\nBOOKING DETAILS\n---------------")
                    print("\nCAB NO\tSOURCE\tDESTINATION\tDATE\tTIME\tOCCUPANCY\tSTATUS")
                    print("------\t------\t-----------\t----\t----\t---------\t------")

                    for row in result:
                        status = 'COMPLETED' if row[6] == 1 else 'CANCELED' if row[6] == 0 else 'UPCOMING'
                        print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}"
                              .format(row[7], row[10], row[11], row[3], row[4], row[5], status))
                    return True
                else:
                    print("\nNo data found.")
            else:
                print("\nNo record found with '{}'".format(emp_email))
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def add_new_cab(self):
        """
                Get input from user for cab details.
                :return: True/False
                """
        print("\nAdd Cab\n-------")
        cab_no = input("Cab no.: ").upper()
        rider_name = input("Rider Name: ")
        rider_no = input("Rider No.: ")
        capacity = int(input("Capacity: "))

        cab_no = re.sub(' +', ' ', cab_no)

        return self.add_cab_action(cab_no, rider_name, rider_no, capacity)

    def add_cab_action(self,cab_no, rider_name, rider_no, capacity):
        """
                Insert cab details in database.
                :param cab_no: cab registered no.
                :param rider_name: rider name
                :param rider_no: rider phone no.
                :param capacity: max occupancy of the cab
                :return: True/False
                """
        try:
            c = self.conn.cursor()
            c.execute("INSERT INTO cabs(CAB_NO,RIDER_NAME,RIDER_NO,CAPACITY) VALUES('{}','{}','{}',{})"
                      .format(cab_no, rider_name, rider_no, capacity))
            self.conn.commit()
            print("\n'{}' added as Cab".format(cab_no))
            return self.update_cab(cab_no)
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def update_cab(self, cab_num=None):
        """
               Update routes of the cab for the given cab_no.
               :param cab_num: cab no.
               :return: True/False
               """
        print("\nUpdate Cab\n----------")
        if cab_num is None:
            cab_num = input("\nEnter Cab No.: ").upper()
            cab_num = re.sub(' +', ' ', cab_num)

        try:
            c = self.conn.cursor()
            c.execute("SELECT id,capacity FROM cabs WHERE upper(cab_no)='{}'".format(cab_num))
            cab_data = c.fetchone()

            if cab_data:
                print("Enter routes for cab - {}".format(cab_num))
                print("Enter # to GO Back.")

                while True:
                    print()
                    source = input("Source: ")
                    if source == '#':
                        break
                    destination = input("Destination: ")
                    if destination == '#':
                        break
                    timing = input("Timing (hh:mm): ")
                    if timing == '#':
                        break

                    c.execute("INSERT INTO routes(cab_id,source,destination,timing,seats_available) \
                                       VALUES({},'{}','{}','{}',{})"
                              .format(cab_data[0], source, destination, timing, cab_data[1]))
                    self.conn.commit()

                print("\nRoutes Updated.")
                return True
            else:
                print("No data found.")

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def update_cab_route_timings(self):
        pass

    def add_employee(self):
        """
        Fetch employee details from user.
        :return: True/False
        """
        print("\nAdd Employee\n------------")
        fname = input("First Name: ")
        lname = input("Last Name: ")
        email = input("Email: ").lower()
        phone = input("Phone no.: ")

        if re.search(self.regex, email):
            if self.add_employee_action(fname, lname, email, phone):
                return True
        else:
            print("\nInvalid email.")
        return False

    def visualize(self):
        """
            Function to visualize data.
            """
        df = pd.read_sql_table("Bookings",con)
        df['date'] = df['date'].dt.date
        print(df)

        plt.plot(df['date'], df.groupby(['booking_id', 'date']).count())
        plt.xticks(rotation=90)
        fig = plt.gcf()
        fig.savefig('plot.png')

    def add_employee_action(self, fname, lname, email, phone):
        """
        Add employee with the given data.
        :param fname: first name of member
        :param lname: last name of member
        :param email: email of member
        :param phone: phone no. of member
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))
            if c.fetchone()[0] < 1:
                if re.search("^[a-zA-Z]+$", fname):
                    if re.search("^[a-zA-Z]+$", lname):
                        if len(phone) == 10:
                            c.execute("INSERT INTO employees (FNAME,LNAME,EMAIL,PHONE) VALUES('{}','{}','{}','{}')"
                                      .format(fname, lname, email, phone))
                            c.execute("INSERT INTO users VALUES('{}','{}',{})"
                                      .format(email, fname.lower() + '@' + str(123), 22))
                            self.conn.commit()
                            print("\n'{}' added as Employee".format(fname))
                            return True
                        else:
                            print("\nInvalid Phone No.")
                    else:
                        print("\n Only letters are allowed in last name.")
                else:
                    print("\n Only letters are allowed in first name.")
            else:
                print("\n'{}' already exists.\nTry again with new Email".format(email))
        except Exception as e:
            print(type(e).__name__, ": ", e)
        return False

    def update_employee(self):
        """
        Fetch record of employee w.r.t. employee email.
        :return: True/False
        """
        print("\nUpdate Employee\n---------------")
        email = input("Enter email: ").lower()

        try:
            c = self.conn.cursor()
            c.execute("SELECT * from employees WHERE lower(email)='{}'".format(email))
            member = c.fetchone()
            if member is None:
                print("\nNo matching record found with '{}'.".format(email))
            else:
                print("\nEnter new details for '{}'\n(Press ENTER to skip the change in value.)".format(email))
                fname = input("First Name: ") or member[1]
                lname = input("Last Name: ") or member[2]
                new_email = input("Email: ").lower() or member[3]
                phone = input("Phone no.: ") or member[4]

                if self.update_member_validation(fname, lname, email, new_email, phone, member[0]):
                    return True

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def update_member_validation(self, fname, lname, old_email, email, phone, member_id):
        """
        Check whether the email already exists in database or not.
        :param fname: first name of member
        :param lname: last name of member
        :param old_email: previous email stored in database
        :param email: email of member
        :param phone: phone no. of member
        :param member_id: id of member
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            if re.search(self.regex, email):
                c.execute("SELECT count(*) from employees WHERE lower(email)='{}'".format(email))
                if c.fetchone()[0] < 1:
                    return self.update_member_action(fname, lname, old_email, email, phone, member_id)
                else:
                    c.execute("SELECT count(*) from employees WHERE lower(email)='{}' and ID={}"
                              .format(email, member_id))
                    if c.fetchone()[0] > 0:
                        return self.update_member_action(fname, lname, old_email, email, phone, member_id)
                    else:
                        print("\n'{}' already exists.\nTry again with new Email".format(email))
            else:
                print("\nInvalid email.")
        except Exception as e:
            print("\n", type(e), ": ", e)

        return False

    def update_member_action(self, fname, lname, old_email, email, phone, member_id):
        """
        Update the member details w.r.t. member id
        :param fname: first name of member
        :param lname: last name of member
        :param old_email: previous email stored in database
        :param email: email of member
        :param phone: phone no. of member
        :param member_id: id of member
        :return: True/False
        """
        if re.search("^[a-zA-Z]+$", fname):
            if re.search("^[a-zA-Z]+$", lname):
                if len(phone) == 10:
                    try:
                        c = self.conn.cursor()
                        c.execute("DELETE from users WHERE EMAIL='{}'".format(old_email))
                        c.execute("UPDATE employees SET FNAME='{}',LNAME='{}',EMAIL='{}',PHONE='{}' WHERE ID={}"
                                  .format(fname, lname, email, phone, member_id))
                        c.execute("INSERT INTO users VALUES('{}','{}',{})"
                                  .format(email, fname.lower() + '@' + str(123), 22))
                        self.conn.commit()
                        print("\nRecord Updated.")
                        return True
                    except Exception as e:
                        print("\n", type(e), ": ", e)
                else:
                    print("\nInvalid Phone No.")
            else:
                print("\n Only letters are allowed in last name.")
        else:
            print("\n Only letters are allowed in first name.")

    def delete_employee(self):
        """
        Delete employee.
        :return: True/False
        """
        print("\nDelete Employee\n---------------")
        email = input("Enter email: ").lower()

        try:
            c = self.conn.cursor()
            c.execute("SELECT * from employees WHERE lower(email)='{}'".format(email))
            if c.fetchone() is not None:
                ch = input("Want to delete '{}' (y/n): ".format(email))
                if ch == 'y' or ch == 'Y':
                    c.execute("DELETE from users WHERE lower(email)='{}'".format(email))
                    c.execute("DELETE from employees WHERE lower(email)='{}'".format(email))
                    self.conn.commit()
                    print("\nRecord deleted.")
                    return True
                else:
                    print("\nAction aborted!")
            else:
                print("\nNo record found with '{}'".format(email))
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def show_employees(self):
        """
        Display all employees.
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM employees;")
            result = c.fetchall()
            if len(result) > 0:
                print("\nEMPLOYEES LIST\n------------")
                print("\nFNAME\tLNAME\tEMAIL\tPHONE NO.")
                print("-----\t-----\t-----\t---------")
                for row in result:
                    print("{}\t\t{}\t\t{}\t\t{}"
                          .format(row[1], row[2], row[3], row[4]))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False





