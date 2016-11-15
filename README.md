### ORM Challenge ###
#### Solution by Grant Toeppen ####


#### Basics ####
__Setup__
Fire up your terminal and select your local directory of choice.
`git clone `

The `test.db` file contains the sample data and is referenced throughout
my code.
__Running Tests__

#### Strategy ####
My main experience with ORMs is with SQLAlchemy, an overwhelmingly 
featured Python ORM that has become almost default for enterprises. In
the time provided for this exercise, I couldn't hope to replicate that 
library, but it served as a background for some of the steps I took in
development.



#### Resources ####
[SQLite Docs](https://www.sqlite.org/docs.html)
[sqlite3 Docs](https://docs.python.org/2/library/sqlite3.html)
[SQLAlchemy Docs](https://docs.sqlalchemy.org/en/latest/)
[Chinook Sample Database](http://chinookdatabase.codeplex.com/)
[StackOverflow](https://http://stackoverflow.com/)

#### Known Issues and Future Development #### 
* The design pattern for `IS NULL` comparisons is not robust. Ideally 
I'd use some sort of more semantic strategy for null comparisons as well
as greater than/less than comparisons.
* String formatting is an inadequate solution for value substitution in
forming SQL operations. It leaves the code vulnerable to SQL injection 
attacks. With more time, I'd immediately refactor that to use sqlite's 
`?` operator for safe substitution.
* Abstraction of SQL construction into its own translation method would
be a good addition.