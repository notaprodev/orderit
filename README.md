# orderit

My first Django app.
A local company in Albania has decided to help its employees with lunch ordering. You are its newest Django developer and to prove yourself you are asked to build the web application.

How the app will work:

2 Roles – Simple User / Administrator

Administrator:

1) He will register other users/administrators.

2) He will create the daily menu (up to 6-7 possible meals)

3) After a certain time of creation (let's say 2 hours) the menu will not allow future orders

4) Generate the daily orders for the menu.

5) Generate weekly orders in a reporting sense.

6) The administrator can define the amount of money a single user can spend on a daily/weekly menu

After the user is registered, he can access the system.

A simple user can see.

1) The daily Menu – A list of possible meals for the day

2) The opportunity to select a certain meal / meal combo (2 or 3 meals) (create an order) up to a certain value (5 $)

3) The possibility to check his previous orders (from previous days)

4) The possibility to change password.

5) Bonus: The possibility to consider previously unspent money (f.e if from Monday to Friday he spends 15 $ in total, he could be allowed to order up to 10$ on Friday)

As bonus:

Using plotting tools – Plot how much each user has spent each week

Adding ‘meal_category’ to meals or ‘department’ to User you can give out more detailed reports. Up to you what extra reports you want to generate.


Requirements

    Python >3.8 version

Project Setup Process
For Windows

    - git clone https://github.com/notaprodev/orderit.git
    - cd orderit
    - pip install -r requirements.txt
    - python manage.py runserver

For Ubuntu/ Linux

    - git clone https://github.com/notaprodev/orderit.git
    - cd orderit
    - pip3 install -r requirements.txt
    - python3 manage.py runserver
