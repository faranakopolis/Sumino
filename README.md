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

This system uses two different databases (Postgres and Redis). Since there are no strong relations between our data and it would come to mind to just use **Redis** for this task. However, we need a reliable database like **Postgres** to store, calculate and retrieve many rows of numbers (using selects and aggrigation functions).

We just have a table in our Postgres database to store the two numbers (a, b).

Although we have our reliable database, to store the number of users' requests, we need a faster database.
These numbers have expiration dates and will not be stored for a long time.

Therefore, we use Redis to store requests counts in this format:
- user-ip_sum : sum_request_count expiration_time
- user-ip_wrong : wrong_request_count expiration_time

_Expiration time is the total seconds remaining to the next hour._

In order to improve our system's response time (performance), we could store the total value in memory. So we do not have to use the Postgres db each time the /total/ API is being called, and there are two ways of implementing that:
+ Calculate the total value each time the Django server runs itself and store it in a global variable. The value will be updated each time the /sum/ API is called.
    
        _drawback: if we scale up this system then we would have more than one Django server and based on which server accepts each API request, the total value could be unreliable_
    
+ Calculate and store the total value in the Redis database and update it each time the sum API is being called.

Clearly, the second approach is better, but right now we are not dealing with a great amount of data and calculating the total value from the number table in the postgres is good enough for us and in my opinion this database design is good for now.

_To download the SQL dump file you can click [here](https://github.com/maripillon/Sumino/tree/master/db%20dump)_ 


## System Design

Having in mind that the framework is Django Rest, I should have chosen between two kind of implementation for my Views
- Class based views
- Function based views

Although class based views increase the code readabality but in this specific project, we don't need to use all of the CRUD method, we don't really have that many models to use and our APIs doesn't relate to eachother, therefore it's better to use the function based views for implementation.

_In order to scale up in the future we could change the implementation method to class based._









