This level is much more complicated than the last challenge where you just need to input a simple sql query injection. When confronted with the challenge, an initial attempt with a query such as:
```
"yes" union select * from password; #test"
```
didn't yield any results and instead flagged an error.


From the source code, we can see that the application is checking for the existence of a user based on the inputted username. When a username is provided via the $_REQUEST array, there is a SQL query to check if the given username exists in the database. If a record is found, it simply returns that the user exists. 
We also can see that there is no easy way to immediately guess the password so, we need to change our strategy.

#### The Blind SQL Injection Approach
Blind SQL Injection is used when a web application is vulnerable to an SQL injection but the results of the injection are not visible to the attacker. The attacker can still retrieve data by asking a series of True/False questions through SQL statements.

After an extensive period of testing and exploring, a realisation was reached that what's needed here is a Blind SQL injection.

The core of the Blind SQL injection in this case was the following template:
``` 
'natas16" AND LIKE BINARY password like "<password so far + trying char>"%% #
```
where:
- BINARY ensures case-sensitive matches.
- %% are wildcards in SQL which matches 0 or more characters.

#### Implementation Strategy

The approach was to create a loop in which each character of the potential password is verified against the database using the Blind SQL Injection template above. 

You can also refer to the source code provided for a demonstration.
