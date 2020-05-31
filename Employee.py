import calendar
from datetime import date, datetime, timedelta
import re
import uuid

from cryptography.fernet import Fernet
import pandas as pd
import matplotlib.pyplot as plot
import SqlConnection as con
from MySQLdb import Error

class Employee:

    def __init__(self, connection):
        self.conn = connection

    def select(self, username, booking_id):

        option = {

            "1": ("Book a cab", self.book_a_cab(username)),
            "2": ("Past Bookings", self.past_bookings(username)),
            "3": ("Upcoming Bookings", self.upcoming_bookings(username)),
            "4": ("Cancel Booking", self.cancel_booking(booking_id))
        }

        ans = input("Choose:\n"
                "1.Book a cab.\n"
                "2.Past Bookings.\n"
                "3.Upcoming Bookings.\n"
                "4.Cancel Booking.\n")

        option.get(ans)[1](con)

    def book_a_cab(self,username):
        """
                Get all the required data for can booking from user.
                :param email: email of the login employee
                :return: True/False
                """
        print("\nNew Booking\n-----------")
        source = input("Source: ").lower()
        destination = input("Destination: ").lower()
        timing = input("Timing (hh:mm): ")
        occupancy = int(input("Occupancy: "))

        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM routes WHERE lower(source)='{}' AND lower(destination)='{}' AND timing>='{}' \
                                AND seats_available>={}".format(source, destination, timing, occupancy))
            result = c.fetchall()

            if len(result) > 0:
                print("\nCAB ID\tTIMING\t\tAVAILABILITY")
                print("------\t------\t\t------------")
                for row in result:
                    print("{}\t{}\t{}".format(row[0], row[4], row[5]))

                route_id = input("\nSelect Cab Id: ")

                if self.validate_route_id(route_id):
                    return self.new_booking_action(route_id, occupancy, username)
            else:
                print("\nNo cabs found.")

        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def validate_route_id(self, route_id):
        """
        Check whether the given cab id is correct or not.
        :param route_id: route id
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM routes WHERE id={}".format(route_id))
            if c.fetchone():
                return True
            else:
                print("\nInvalid Cab Id.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def new_booking_action(self, route_id, occupancy, email):
        """
         Insert a new booking with the given details in database.
         :param route_id: route id of the ride details
         :param occupancy: total no. of people travelling
         :param email: email of logged in user
         :return: True/False
               """
        ch = input("Confirm Booking (y/n): ")
        if ch == 'y' or ch == 'Y':
            try:
                c = self.conn.cursor()
                c.execute("SELECT id FROM employees WHERE lower(email)='{}'".format(email))
                emp_id = c.fetchone()[0]
                c.execute("INSERT INTO bookings(emp_id,route_id,date,time,occupancy,status)\
                            VALUES({},{},'{}','{}',{},{})"
                          .format(emp_id, route_id, date.today(), datetime.now().strftime("%H:%M"), occupancy, 2))
                c.execute("UPDATE routes SET seats_available=seats_available-{} WHERE id={}"
                          .format(occupancy, route_id))
                self.conn.commit()
                print("\nBooking Confirmed.")
                return True
            except Exception as e:
                print(type(e).__name__, ": ", e)
        else:
            print("\nAction aborted!")

            return False


    def past_bookings(self,username):
        """
                Show all the rides which are completed or canceled.
               :param email: email of the logged in user.
                :return: True/False
                """
        try:
            c = self.conn.cursor()
            c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM bookings JOIN routes ON routes.ID=bookings.ROUTE_ID \
                                JOIN cabs ON cabs.ID=routes.CAB_ID JOIN employees ON employees.ID=bookings.emp_id \
                                WHERE email='{}' AND STATUS=1 OR STATUS=0"
                      .format(date.today(), datetime.now().strftime("%H:%M"), username))
            result = c.fetchall()
            if len(result) > 0:
                print("\nBOOKING DETAILS\n---------------")
                print("\nCAB NO\t\t\tSOURCE\tDESTINATION\t\tDATE\t\tTIME\t\tOCCUPANCY\tSTATUS")
                print("------\t\t\t------\t-----------\t\t----\t\t----\t\t---------\t------")

                for row in result:
                    status = 'COMPLETED' if row[6] == 1 else 'CANCELED' if row[6] == 0 else 'UPCOMING'
                    print("{}\t{}\t\t{}\t\t{}\t{}\t{}\t\t\t{}"
                          .format(row[7], row[10], row[11], row[3], row[4], row[5], status))
                return True
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False


    def upcoming_bookings(self,username):
        """
                Show list of all the coming rides.
                :param email: email of the logged in user
                :return: True/False
                """
        try:
            c = self.conn.cursor()
            c.execute("SELECT bookings.*,cabs.cab_no,routes.* FROM bookings JOIN routes ON routes.ID=bookings.ROUTE_ID\
                                JOIN cabs ON cabs.ID=routes.CAB_ID JOIN employees ON employees.ID=bookings.emp_id\
                                WHERE email='{}' AND STATUS=2"
                      .format(username))
            result = c.fetchall()
            if len(result) > 0:
                print("\nBOOKING DETAILS\n---------------")
                print("\nBOOKING ID\tCAB NO\t\t\tSOURCE\tDESTINATION\t\tROUTE TIME\t\tDATE\t\tTIME\t\tOCCUPANCY")
                print("----------\t------\t\t\t------\t-----------\t\t----------\t\t----\t\t----\t\t---------")

                for row in result:
                    print("{}\t\t{}\t{}\t{}\t{}\t\t\t{}\t{}\t{}"
                          .format(row[0], row[7], row[10], row[11], row[12], row[3], row[4], row[5]))

                booking_id = input("\nEnter booking id to cancel: ")
                if self.validate_booking_id(booking_id):
                    return self.cancel_booking(booking_id)
            else:
                print("\nNo data found.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def validate_booking_id(self, booking_id):
        """
        Verify the booking Id.
        :param booking_id: booking id for the ride
        :return: True/False
        """
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM bookings WHERE id={} AND status=2".format(booking_id))
            if c.fetchone():
                return True
            else:
                print("\nInvalid Booking Id.")
        except Exception as e:
            print(type(e).__name__, ": ", e)

        return False

    def cancel_booking(self, booking_id):
        """
                Cancel booking for the given booking Id.
                :param booking_id: booking id of the ride
                :return: True/False"""
        ch = input("Want to cancel booking (y/n): ")
        if ch == 'y' or ch == 'Y':
            try:
                c = self.conn.cursor()
                c.execute(
                    "select r.TIMING from bookings as b inner join routes r on b.ROUTE_ID = r.id  where b.id={}".format(
                        booking_id))
                temp = c.fetchone()
                if temp:

                    mydate = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d") + temp[0]
                    mydatetime = mydate - timedelta(hours=0, minutes=30)
                    if datetime.now() > mydatetime:
                        print("can't cancel current ride.")
                        return False

                    c.execute("UPDATE bookings SET status=0 WHERE id={}".format(booking_id))
                    c.execute("SELECT route_id,occupancy FROM bookings WHERE id={}".format(booking_id))
                    data = c.fetchone()
                    c.execute("UPDATE routes SET seats_available=seats_available+{} \
                                        WHERE id={}"
                              .format(data[1], data[0]))
                    self.conn.commit()
                    print("\nBooking canceled.")
                    return True
            except Exception as e:
                print(type(e).__name__, ": ", e)
        else:
            print("\nAction aborted!")

        return False


