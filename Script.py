""" Create all necessary tables required in the project."""


class Schema:

    def __init__(self, connection):
        self.conn = connection

    def setup_admin(self):
        """
        Create table employees & users if not exists and insert one row with given pre-details of admin.
        :return: True/False
        """
        try:
            c = self.conn.cursor()

            c.execute("SELECT count(*) FROM information_schema.tables WHERE table_name ='employees';")

            # if the count is not 1, then create table employees, users and add 1st Admin
            if c.fetchone()[0] != 1:
                c.execute('''CREATE TABLE employees
                            (ID             INTEGER     PRIMARY KEY AUTO_INCREMENT  NOT NULL,
                             FNAME          VARCHAR(20)                             NOT NULL,
                             LNAME          VARCHAR(20)                             NOT NULL,
                             EMAIL          VARCHAR(50)     UNIQUE                  NOT NULL,
                             PHONE          VARCHAR(10)                             NOT NULL);''')

                c.execute("INSERT INTO employees(ID, FNAME, LNAME, EMAIL, PHONE)  \
                            VALUES(1211, 'sayan', 'mandal', 'sayan@gmail.com', '7001621385  ')")

                c.execute('''CREATE TABLE users
                            (EMAIL          VARCHAR(50)    UNIQUE        NOT NULL,
                             PASSWORD       VARCHAR(16)                  NOT NULL,
                             ROLE           INTEGER                      NOT NULL,
                             FOREIGN KEY(EMAIL) REFERENCES employees(EMAIL));''')

                c.execute("INSERT INTO users(EMAIL, PASSWORD, ROLE) \
                            VALUES('sayan@gmail.com', 'Sayan@1', 11)")
                self.conn.commit()
                return True

        except Exception as e:
            print(type(e), ": ", e)
            return False

    def create_tables(self):
        """
        Create tables only if they don't exist in database.
        :return: True/False
        """
        try:
            c = self.conn.cursor()

            # create table cabs if not exist
            c.execute('''CREATE TABLE if not exists cabs
                        (ID             INTEGER         PRIMARY KEY AUTO_INCREMENT    NOT NULL,
                         CAB_NO         VARCHAR(15)     UNIQUE                        NOT NULL,
                         RIDER_NAME     VARCHAR(50)                                   NOT NULL,
                         RIDER_NO       VARCHAR(10)                                   NOT NULL,
                         CAPACITY       INTEGER                                       NOT NULL);''')

            c.execute("ALTER TABLE cabs AUTO_INCREMENT = 111;")

            # create table routes if not exist
            c.execute('''CREATE TABLE if not exists routes
                        (ID                 INTEGER         NOT NULL    PRIMARY KEY AUTO_INCREMENT,
                         CAB_ID             INTEGER         NOT NULL    REFERENCES cabs(ID),
                         SOURCE             VARCHAR(20)     NOT NULL,
                         DESTINATION        VARCHAR(20)     NOT NULL,
                         TIMING             TIME            NOT NULL,
                         SEATS_AVAILABLE    INTEGER         NOT NULL);''')

            c.execute("ALTER TABLE routes AUTO_INCREMENT = 1510;")

            # create table bookings if not exist
            c.execute('''CREATE TABLE if not exists bookings
                        (ID             INTEGER      NOT NULL   PRIMARY KEY AUTO_INCREMENT,
                         EMP_ID         INTEGER      NOT NULL   REFERENCES employees(ID),
                         ROUTE_ID       INTEGER      NOT NULL   REFERENCES routes(ID),
                         DATE           DATE         NOT NULL,
                         TIME           TIME         NOT NULL,
                         OCCUPANCY      INTEGER      NOT NULL,
                         STATUS         INTEGER      NOT NULL);''')

            c.execute("ALTER TABLE bookings AUTO_INCREMENT = 1021;")

            self.conn.commit()
            return True

        except Exception as e:
            print(type(e), ": ", e)
            return False