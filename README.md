# Family Expense Tracker

This is a program I wrote to track the incomes and outcomes of my family. The app has two parts to it:

### 1. Getting the expenses

To get the expenses, we use a telegram bot. The bot is inside a family group dedicated to this app.
Every time a family member spend money - he will write a message about it in the group. The bot will parse the expanse and add it to a google sheet's spread sheet.
The reasons we are using telegram are:
1. It's very intuitive
2. It's good for the entire family to see the cashflow. It helps to not over spend money.

We use google sheets (and not SQL or so) so we can edit it manually

### 2. Displaying the expenses

I built an interactive dashboard to display the balance and cashflow


### usage

1. add the bot to a telegram group with the family
2. start sending messages every time you spend money

### to do list:

* add knows categories that the bot will match and suggest a known category - if the bot didnt recognize the category, he can offer a similar one. (ML?)
* graphic display of the data and a interactive dashboard
