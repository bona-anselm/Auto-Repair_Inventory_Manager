# AUTOINVENTO
-------------
AutoInvento is an automobile inventory management software that can also be
adopted as an inventory management system for any sector or industry including e-commerce.


### Brief Decription
--------------------
A user (mechanic) login and from his/her dashboard request for an inventory item to use,
the request is sent to owner who also receives an email notification for the request.

He can either approve or reject any pending request from any mechanic.
Each of the mechanics can view their request status.

From the dashboard, both the mechanic and the owner can view so many information about the inventory
items, mechanics or suppliers.

Inventory items that are <= 10 which is the low_threshold, turns orange when viewed in the list of inventories, any one that's = 0 turns red, the rest have default page colour.

The owner have different charts to visualize suppliers and total number of items they supplied, as well as the mechanics usage data.

When the owner approves requests, the quantity of items in that request are deducted from that item's quantity in the inventory table.

Only the owner who is a super user can create mechanics and the app can only be used when logged in. Forgotten passwords can be reset.



### Installation
-----------------
To use the app, install it be running the following command preferably in a virtual environment.

```pip install -r requirements.txt```

After the dependencies have been installed, to run the app, use the command

```python3 run.py``` or ```python3 -m run``` 



### Contributors
-----------------
Bonaventure Anselm

Aina Rachael Damilola
