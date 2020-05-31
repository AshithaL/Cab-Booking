import unittest
from mock import patch
from Employee import Employee

class TestEmployee(unittest.TestCase):

    def testBookAcab(self):
        with patch('Employee') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Employee.book_a_cab(username="ashitha@gmail.com"))
            assert(X, "Success")

    def testPastBooking(self):
        with patch('Employee') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Employee.past_bookings(username="ashitha@gmail.com"))
            assert(X, "Success")

    def testUpcomingBookings(self):
        with patch('Employee') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Employee.upcoming_bookings(username="ashitha@gmail.com"))
            assert(X, "Success")

    def testCancel_booking(self):
        with patch('Employee') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Employee.cancel_booking(booking_id="some"))
            assert(X, "Success")

if __name__ == '__main__':
    unittest.main()
