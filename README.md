# Un-BreakiFi
An app to help couples not break up because of financial issues. 

Django app. Has an internal API that feeds data to the Graphical Tool available at the web page. Data can be either loaded using web or CLI.

Developed in Python 3.5 using following packages:

1. django==1.9.1

2. djangorestframework==3.5.3

3. pygments==2.2.0

4. python-dateutil==2.6.0

Install requirements:

     pip install -r requirements.txt

Run the server:

    python manage.py runserver
  
Then go to: localhost:8000

Load data via CLI:

    python interact.py --parse   # load data
    python interact.py --delete  # delete all from the db
    
API Calls:
    
    localhost:8000/api/v1/users           # see all users and their features
    localhost:8000/api/v1/user-<auth_id>/ # specific user's features


General urls:
add user (upload csv files)

```
    localhost:8000/add-user
```
profile with features
```
    localhost:8000/user-<auth_id>/profile
```
income vs transaction details

```
    localhost:8000/user-<auth_id>/ie
```
housing expenses
```
    localhost:8000/user-<auth_id>/housing
```
    
transactions over time
```
    localhost:8000/user-<auth_id>/dates
```
transportation related details

```
    localhost:8000/user-<auth_id>/transport
```
vendors

```
    localhost:8000/user-<auth_id>/vendors
```
vendor specific transactions
    
```    
    localhost:8000/user-<auth_id>/<vendor_id>
```
vendors vs expense

```
    localhost:8000/user-624/vendors/expense
```
vendors vs number of transactions

```
    localhost:8000/user-<auth_id>/vendors/transactions
```
