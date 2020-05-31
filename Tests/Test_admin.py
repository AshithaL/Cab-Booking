import unittest
from Admin import Admin
import SqlConnection
from mock import patch

class Test_admin(unittest.TestCase):

    def testCheckTotalBooking(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.check_total_bookings)
            assert(X, "Success")

    def testCheckEmpBooking(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.check_emp_booking)
            assert(X, "Success")

    def testAddNewCab(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['aims.db']
            X = bool(Admin.add_new_cab)
            assert(X, "Success")

    def testUpdateCab(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.update_cab)
            assert(X, "Success")

    def testAddEmployee(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.add_employee)
            assert(X, "Success")

    def testUpdateEmployee(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.update_employee)
            assert(X, "Success")

    def testDeleteEmployee(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.delete_employee)
            assert(X, "Success")

    def testShowEmployess(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.show_employees)
            assert(X, "Success")

    def testVisualize(self):
        with patch('Admin.sqlite3') as test:
            test.connect().cursor().fetchall().return_value = ['cab.db']
            X = bool(Admin.visualize)
            assert(X, "Success")


if __name__ == '__main__':
    unittest.main()
