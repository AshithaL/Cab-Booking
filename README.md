# Cab Booking System 

Introduction
----
Cab Booking System is a Simple Console Application where a user can book a cab between different client locations. Multiple employees can book the same cab to travel to client locations or in between stops. Each cab will have a dedicated route and will travel to and fro at different timings. 

### Configuration 
**Username and Password** are the configuration parameter required to make the login for each user.

### Roles / Functionalities in project 

**Admin:** This role of Admin is where admin can perform CRUD operation for employees and see all the bookings done by 
employees. Admin can also perform CRUD operation on cabs and also see the bookings of cabs between any period of time.

**Employee:** This role is for employees, where they can book cabs and see their past and upcoming bookings. Employees 
can also cancel their bookings prior to 30 min.

### SqlConnection.py
This file has the mysql connection code and login code where after giving the right credentials schema.py file is called.
### Script.py
This file has all the schemas of the respective tables.
### Admin.py
This file all the functionalities of admin related tasks.
### Employee.py
This file is used to carry out all the Employee related functions.


Login credentials for Admin
---
```   
email: ashitha@gmail.com
password: ashitha@123
```

Setup for Running the Project
---
```   
1. Open the project CAB
2. Run python file 'run.py'
    -> python run.py

```

Setup for running CRON jobs
---
```
1. Open new terminal
2. Go the project CAB
3. Run pythonn file 'booking_status_cron_job.py'
    -> python booking_status_cron_job.py
```

### DIRECTORY STRUCTURE
```
+-- CAB
|  +--SqlConnection.py
|  +--Admin.py
|  +--Employee.py
|  +--Script.py
|  +--booking_status_cron_job.py
```

