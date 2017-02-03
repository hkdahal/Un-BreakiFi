# Un-BreakiFi
An app to help couples not break up because of financial issues. 

Django app. Has an internal API that feeds data to the Graphical Tool available at the web page.

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
1. add user (upload csv files)
```
    localhost:8000/add-user
```
2. profile 
```
    localhost:8000/user-<auth_id>/profile
```
3. income vs transaction details

```
    localhost:8000/user-<auth_id>/ie
```
4. housing expenses
```
    localhost:8000/user-<auth_id>/housing
```
    
5. transactions over time
```
    localhost:8000/user-<auth_id>/dates
```
6. transportation related details

```
    localhost:8000/user-<auth_id>/transport
```
7. vendors

```
    localhost:8000/user-<auth_id>/vendors
```
8. vendor specific transactions
    
```    
    localhost:8000/user-<auth_id>/<vendor_id>
```
9. vendors vs expense

```
    localhost:8000/user-624/vendors/expense
```
10. vendors vs number of transactions

```
    localhost:8000/user-<auth_id>/vendors/transactions
```
