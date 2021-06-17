# **Sumino** 
#### _(Boomino test task)_

![logo_gray](https://github.com/maripillon/Sumino/blob/master/logo/cover1.png?raw=true)

**Sumino** Is a simple system for adding two numbers, including following APIs:

    - Get sum of two numbers (a,b)
    - Get all of numbers (a,b)
    - Get the sum of total numbers


## APIs

You can download and use the export file of Postman's collection [here](https://github.com/maripillon/Sumino/tree/master/postman).

The functionality of each API is pretty straightforward. 

## Database

Knowing that our language is Python and our framework is Django Rest, in my opinion, the first step of the system design is designing its database.

This system uses two different databases (Postgres and Redis). Since there are no strong relations between our data and it would come to mind to just use **Redis** for this task. However, we need a reliable database like **Postgres** to store, calculate and retrieve many rows of numbers (using selects and aggregation functions).

We just have a table in our Postgres database to store the two numbers (a, b).

Although we have a reliable database (postgres), to store the number of users' requests, we need a faster database.
These numbers have expiration dates and will not be stored for a long time.

Therefore, we use Redis to store requests counts in this format:
- user-ip_sum : sum_request_count expiration_time
- user-ip_wrong : wrong_request_count expiration_time

_Expiration time is the total seconds remaining to the next hour._

In order to improve our system's response time (performance), we could store the total value in memory. So, we do not have to use the Postgres database each time the /total/ API is called, and there are two ways of implementing that:
+ Calculate the total value each time the Django server runs itself and store it in a global variable. The value will be updated each time the /sum/ API is called.
    
    _Drawback: If we scale up the system then we would have more than one Django server and based on which server accepts each API request, the total value could be unreliable._
    
+ Calculate and store the total value in the Redis database and update it each time the sum API is called.

Clearly, the second approach is better. However, right now we are not dealing with a great amount of data (numbers), and calculating the total value from the 'number' table is good enough for this purpose.

_To download the SQL dump file you can click [here](https://github.com/maripillon/Sumino/tree/master/db%20dump)_ 


## System Design

### Views

Having in mind that the framework is Django Rest, I needed to choose between two different implementations for the views:
- Class-based views
- Function-based views

Although class-based views increase the code readability, we do not need to use all of the CRUD methods in this specific project. We also do not have many models to use and our APIs do not have anything in common. Therefore, it is better to use the function-based views for this implementation.

Note 1: _In order to scale up the system in the future, we can change the implementation method to class-based._

### Permissions

At first, I was controlling the request counts inside of each view but in order to make the system's performance better and make it scalable, I decided to consider each blocking situation as a permission to access a view, so it does not have to go inside it.


Note 2: _For further explainations, please refer to the code._










