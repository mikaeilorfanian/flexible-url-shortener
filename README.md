#A URL Shortener Using Python and Django

#Intro
An important feature of this application is the ability to restrict the length of the path component of the shortened URL. You can do this in `settings.py`.  
So, if you set `SHORT_URL_LENGTH_BOUND` to `(2, 5)`, then the app will make short URLs like this  
```buildoutcfg
www.somedomain.com/xx
www.somedomain.com/xxx
www.somedomain.com/xxxx
www.somedomain.com/xxxxx
```
where x can be a character in `CHARSET` defined also in `settings.py`.  
Most URL shortener tutorials on the web use hashing algorithms to convert a long URL to a short one. When a request comes in, they decode the short code and search for it in the database.  
This approach is very well understood, therefore, it's a bit boring. So, I've decided to come up with a more interesting solution.  
#My Solution
##Core Assumption
This application is never going to be popular. Meaning that the total number of short URLs generated won't be greater than a few hundred thousand.  
To understand why this assumption is key, read on.
##How the Solution Works
Before users can use the website, we have to populate the `ShortURLCombination` model(or table) with all possible path components(as per instructions below).  
These combinations depend on the value of `CHARSET` defined in `settings.py`.  
Every time we generate a short URL, we take an unused path component from the `ShortURLCombination` model. Eventually, we will run out of unused path components from this table, so we will have to repopulate this table with more path components. I didn't implement this re-population mechanism in this solution.  
##How to Run the App
All the below commands should be run from the folder where the app's `manage.py` is.   
First, install dependencies from `requirements.txt`.
###Crate the Database
```bash
python manage.py makemigrations shorturl
python manage.py migrate
```
###Populate the Database with Fake Users
```bash
python manage.py make_fake_users 100
```
The above commands populates the `User` table with 100 fake users fetched fetched from `https://randomuser.me/`.
###Define the Range of Combinations
To define how the path component of short URLs should look like, you can change `CHARSET` and `SHORT_URL_LENGTH_BOUND` in `settings.py`. 
###Populate the Database with Combinations
Run this command in your terminal
```bash
python manage.py generate_path_component_combinations
```
####An Illustration
If we set 
```python
SHORT_URL_LENGTH_BOUND = (3, 8)
PATH_COMPONENT_CHARSET = 'ABC'
```
in `settings.py`, then running the above command would generate `9828` path component combinations and populate the `ShortURLCombination` model with them.   
From now on, every time a new short URL is generated, our app will use one of the combinations we just generated.   
###Run Tests
```bash
python manage.py test shorturl.tests
```
###Run the app
```bash
python manage.py runserver
```
##Analysis
Problems usually have multiple solutions and trade-offs determine which solution gets implemented.  
2 factors were important in my decision to implement this solution:
1. It should not work like the other thousands of URL shorteners on the web.
2. Setting up the app and reading the code should be easy.  
Now, let's analyze the weaknesses and strengths of this app.
###Weaknesses
* We put the combinations into a table in a relational database. If we were dealing with tens of millions of URLs, other options like  key-value databases like `redis` could be a better choice for this application. 
* The choice of having `CHARSET` as a variable that can be change has bad consequences. It introduces dependencies in URL configurations. Also, it almost duplicates what `SHORT_URL_LENGTH_BOUND` does.
* When we run out of unused combinations, we have to manually change `settings.py` add more combinations to the database.
###Strengths
* Since we're not using any hashing algorithms, converting long URLs to short ones involves no calculations. This comes with a price of: we're using two tables and each request requires a `join` operation.
* Again, due to lack of encoding or decoding algorithms, the code is easy to read and maintain.
#Conclusion
I wouldn't use this solution in a real production environment. Instead, I'd use a hashing algorithm which doesn't require combinations to be defined beforehand.  
Also, I would consider using non-relational databases if the app has a real need for being scalable.  