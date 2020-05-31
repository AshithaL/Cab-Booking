import mysql.connector as connector
import schedule
import time
from datetime import datetime, timedelta


def update_booking_status():
    """
    this method is used to update booking status for old rides.
    :return:
    """
    mydb = connector.connect(
        host='localhost',
        user='root',
        password='nineleaps',
        database='cab'
    )

    c = mydb.cursor()
    c.execute("SELECT * from Bookings JOIN routes ON bookings.route_id=routes.id WHERE status=2;")
    result = c.fetchall()
    print(result)
    if len(result) > 0:
        for row in result:
            t = datetime.now().strftime("%H:%M:%S")
            t = datetime.strptime(t, '%H:%M:%S').time()
            current_time = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
            print(row[11] + timedelta(minutes=30))
            if current_time > row[11] + timedelta(minutes=30):
                c.execute("UPDATE bookings SET status=1 WHERE id={}".format(row[0]))
                c.execute("UPDATE routes SET seats_available=seats_available+{} WHERE id={}"
                          .format(row[5], row[2]))
                mydb.commit()
                print("\nRide complete.")

    mydb.close()


if __name__ == "__main__":

    schedule.every(10).seconds.do(update_booking_status)

    while 1:
        schedule.run_pending()