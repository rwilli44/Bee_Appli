# Django TP: Rachel Williams
## 12/01/2024 - Diginamic

This app was developed as part of the Python software developer training program at diginamic. The purpose of the app is to provide beekeepers a means of managing data on their beeyards and beehives. Some details of the hives as well as contact information for the beekeepers who give their consent is shared via a public API. It also includes an example of templating to show the beeyards and hives of the connected user and provide the possibility to list their interventions.

### Installation

1. Clone the repository to your local machine.
2. Create a virtual environment using **python -m venv .venv** and activate it (**./.venv/Script/activate** on Windows).
3. Make sure you are in the base folder and run **pip install -r requirements.txt** to add all of the dependencies.
4. Change the **.env-template** file name to **.env**. It is filled with default data for a postgres database named __test_db__. Make any adjustments necessary adjustments to this file so that it corresponds to your system. This is done to facilitate testing and grading this project and this sort of information should never be included directly in production code.
5. **Create a postgres database** of the expected name on your machine.
6. Run **python manage.py migrate** to create the initial database setup.
7. Run **python manage.py filltestdb** to automatically add dummy data to the database. __Note that this creates an admin user with the username/password **admin:admin**.__ (Obviously, this should only be used for test purposes.) It also creates several beekeeper users such as IdgieThreadgood:Bees4ever! for which can be used for manual testing.
8. Multiple tests have been created in the test.py file. To run them, make sure you are still in the base directory and run **coverage run manage.py test apiary -v 2** . The expected result is 8 successful tests. This does not cover the entire app but includes testing the action function which allows a beekeeper to log a health check of all the hives in one beeyard at once. It also tests using POST to create a contamination log and tests whether users can access the expected data depending on their authentication status.
9. To start the app, run **python manage.py runserver**.
10. These are the key urls for testing the application:
- Public API: http://127.0.0.1:8000/public_api/
- Admin Login: http://127.0.0.1:8000/apiaryadminaccessportal/ (Reminder: running filltestdb creates an admin:admin user)
- Admin Honeypot: http://127.0.0.1:8000/admin
- Beekeeper Login: http://127.0.0.1:8000/apiary/login  
  One possible test login is **IdgieThreadgood:Bees4ever!**
- The login leads to the Beekeeper template page: http://127.0.0.1:8000/apiary/
- The user can click on each hive's intervention link to see a list of interventions affecting the hive. The URL pattern for this is: http://127.0.0.1:8000/apiary/interventions/?hive=HIVE_ID . The authenticated user should only be able to access information on their own hives.
- Private API (requiring authentication as a beekeeper user such as IdgieThreadgood:Bees4ever!): http://127.0.0.1:8000/ The authenticated user should only be able to access information on their hives. Filters are available on both APIs. The admin user has no beehives, to see data in the private API login with the provided beekeeper username.
9. Axes is used to log access and failed access attempts. After three failed logins, the IP is locked out. If this occurs, run **python manage.py axes_reset** to reset the login attempts.

### Thank you to our teacher, Cedric JANNOT for the fun project. I learned a lot in a very short time. 
