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

Determined the features based on following:<br />
     Student - Transactions related to books such as Science, Mathematics, Biology  <br />
     Artist or into arts - Transactions related to art, paint, craft <br />
     Into music - Transactions related to Guitar, Music, Piano <br />
     Figurine stuffs - Transactions related to Figurines <br />
     Recently moved - Transactions related to Depot, Furniture, Movers <br />
     Likes peace - Transactions related to Library, Book Store, Museum <br />
     Proposing - Transactions related to Wedding Planners, Jewelry shopping <br />
     Athletic - Transactions related to Dick's Sports, Sports, NFl, NBA, Athletic events, Vitamin shopping, Biking, Gym <br />
     Divorced - Transactions related to Divorced Lawyer Fees <br />
     Outgoing - Transactions related to Bar, Beach, Bowling, Skating, Theater, Concert, Wine <br />
     Has Kids - Transactions related to babies <br />
     Paying Student Loans - Transactions related to Student Loans <br />
     Pets - Transactions related to pet supplies <br />
