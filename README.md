### ORM Challenge ###
#### Solution by Grant Toeppen ####


#### Basics ####
__Setup__
Fire up your terminal and select your local directory of choice.
```git clone git@github.com:grantt/orm_test.git```

The `test.db` file contains the sample data and is referenced throughout
my code.

__Running Tests__
There are several simple unit tests I wrote while working on the 
challenge, they can be run with the following command:
```python -m unittest -v test```

#### Strategy ####
My main experience with ORMs is with SQLAlchemy, an overwhelmingly 
featured Python ORM that has become almost default for enterprises. In
the time provided for this exercise, I couldn't hope to replicate that 
library, but it served as a background for some of the steps I took in
development.

First, I gave myself some sample data in a SQLite database in order to 
test against something realish. Relying on the `sqlite3` library, I stubbed 
out a `Session` class with `connect` and `disconnect` methods, as well 
as access to the cursor to traverse returned records. This was followed 
by an `execute` method to run arbitrary commands in explicit SQL as well 
as a `commit` method for persistence of changes.

My next step was to develop an `Entity` model to resolve the SQLite rows 
into Python objects. `Entity` is a simple construction with a mapping of 
a `__table_name__`, `__primary_key__`, and `__fields__` dictionary. 
`__fields__` is a key-value store of a table's columns to deserialize into 
the Python object, along with the transform function used to translate 
SQLite's simple types (note that `sqlite3` only handles `NULL`, 
`INTEGER`, `REAL`, `TEXT`, and `BLOB` by default) into useful pythonic 
types. This led me to build specific models for the sample data, namely 
`Customer` and `Invoice`, as well as build out some custom handlers for 
nullable integers and dates.

With `Entity` constructed, I focused back on generating usable SQL from 
the `Session` class. This was done with substitution of primary
key and column values with the particular method called `get`, `get_all`, 
or `insert` handling the construction of a `SELECT` or `INSERT` clause. 

Finally, I opted to implement `IS NULL` comparison and basic filtering 
by passing in a dictionary keyed by `Entity` fields and conditionally 
creating a `WHERE` clause.

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
* Type handling upstream is untested and needs work.