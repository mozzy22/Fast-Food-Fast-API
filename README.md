# **Fast-Food-Fast**
___
## > A food delivery service app for a restaurant

___

## APPLICATION  FEATURES
1. Users can create an account and log in
2. A user can order for food
3. The admin can add,edit or delete the fast-food items
4. The admin can see a list of fast-food items
5. The Admin user can do the following:
  + See a list of orders
  + Accept and decline orders
  + Mark orders as completed
6. A user can see the history of ordered food
7. A user is assigned a JWT on login for authourization

___
### See the  Features and their endpoints

| FEATURE | METHOD | END POINT|
| --- | --- |--- |
| Signup | POST | api/v1/auth/signup|
| Login | POST | api/v1/auth/login|
| Get all orders | GET | api/v1/orders|
| Place anew order | POST | api/v1/users/orders|
| Get user order hitory | Get | api/v1/users/orders|
| Fetch a specific order | GET| api/v1/orders/order-uuid|
| Update an order status | PUT | api/v1/orders/oder-uuid|
| Get all users | GET | api/v1/users|
| Fetch all food items on the menu| GET | api/v1/menu|
| Add food item to menu | POST| api/v1/menu|
| Index page | GET | /|

___
 The apllication is hosted on [Heroku HERE](https://fast-food-fast-mozzy22.herokuapp.com/)
___

[![Coverage Status](https://coveralls.io/repos/github/mozzy22/Fast-Food-Fast-API/badge.svg?branch=develop)](https://coveralls.io/github/mozzy22/Fast-Food-Fast-API?branch=develop)
[![Build Status](https://travis-ci.org/mozzy22/Fast-Food-Fast-API.svg?branch=develop)](https://travis-ci.org/mozzy22/Fast-Food-Fast-API)
<a href="https://codeclimate.com/github/mozzy22/Fast-Food-Fast-API/maintainability"><img src="https://api.codeclimate.com/v1/badges/d21a9263c5c24aac6035/maintainability" /></a>

___
      *WISH TOU ALL THE BEST AS YOU DINE AND WINE  WITH US*
___