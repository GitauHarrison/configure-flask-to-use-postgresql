# Configure Flask To Use PostgreSQL

This project demonstrates how to use the popular postgreSQL database with Flask. Moving away from the disk-based SQLite database, postgreSQL can actually work very well with flask, allowing for benefits of using it.

![Demo App](app/static/css/images/postgres_demo_app.gif)

### Table of Contents

 - [Technologies Used](#technologies-used)
 - [Features](#features)
 - [Configure PostgreSQL Database](#configure-postgresql-database)
 - [Testing the Application Locally](#testing-the-application-locally)

## Technologies Used

- Flask
- PostgreSQL

## Features

- [x] Basic User Authentication
- [x] User posts


## Configure PostgreSQL Database

If you are interested in learning how to use postgreSQL with Flask, you can check the project's full tutorial [here](https://github.com/GitauHarrison/notes/blob/master/databases/project_configure_postgres_in_flask.md).

### Step 1: Access PostgreSQL from PSQL

PSQL is a terminal front-end tool used to access the postgreSQL database. If you have reviewed the lesson [Access PostgreSQL using `psql`](https://github.com/GitauHarrison/notes/blob/master/databases/access_postgresql/psql.md), this will be quite easy. If you haven't, I recommend that you start there.

Log into postgreSQL as the `postgres` user by running this command in the terminal:

```sql
(venv)$ sudo -u postgres psql

# Output
psql (14.5 (Ubuntu 14.5-1.pgdg20.04+1))
Type "help" for help.

postgres=# 
```

You can split your VS Code terminal into two so that one window runs the flask server, while the other allows you to access the postgreSQL database. Alternatively, you can stop the flask server by pressing "Ctrl + C" before running the command above.

### Step 2: Create a New User

Notice that the prompt on the terminal has changed to `postgres=#`. We can issue our first postgres command to create another user called `muthoni` by running:

```sql
postgres=# CREATE USER muthoni SUPERUSER;
CREATE ROLE
```

### Step 3: List all Users

List all the available database users by running:

```sql
postgres=# \du
                                   List of roles
 Role name |                         Attributes                         | Member of 
-----------+------------------------------------------------------------+-----------
 harry     | Superuser                                                  | {}
 muthoni   | Superuser                                                  | {}
 postgres  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 taste     |                                                            | {}

postgres=# 
```

You can see that `muthoni` is now a super user. A super user by-passes all database checks, so you should be VERY CAREFULL when doing this.


### Step 4: Add User Password

To help secure user `muthoni`, we can assign her a password. 

```sql
postgres=# ALTER USER muthoni WITH PASSWORD 'muthoni';
ALTER ROLE
```

Now, every time `muthoni` tries to access the postgres database, she will be required to identify herself by providing the password "muthoni".


### Step 5: Create A DATABASE

At this stage, we can create a database and make `muthoni` an owner.

```sql
postgres=# CREATE DATABASE demo_postgres_app WITH OWNER muthoni;
```

Remember our `DATABASE_URL` environment variable earlier?

```python
# .env

DATABASE_URL=postgresql://muthoni:muthoni@localhost:5432/demo_postgres_app
```

Be sure to update it accordingly if your user and database are named differently. Refer to this [postgreSQL formart](https://github.com/GitauHarrison/notes/blob/master/databases/project_configure_postgres_in_flask.md#step-6-postgresql-url-format).

### Step 6: See All Your Databases

To see a list of all your databases, you can run this command:

```sql
postgres=# \l

# Output
                                      List of databases
       Name        |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges   
-------------------+----------+----------+-------------+-------------+-----------------------
 demo_postgres_app | muthoni  | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 newsletter_app    | harry    | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres          | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | 
 postgres_test     | taste    | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =Tc/taste            +
                   |          |          |             |             | taste=CTc/taste
 template0         | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                   |          |          |             |             | postgres=CTc/postgres
 template1         | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
                   |          |          |             |             | postgres=CTc/postgres
(6 rows)
```

You can see that `muthoni` is the owner of `demo_postgres_app` database.

And, that is it! Your Flask application is now ready to use the postgreSQL database. 


## Testing the Application Locally

- Clone this repository:

```python
$ git clone git@github.com:GitauHarrison/configure-flask-to-use-postgresql.git
```

- Change directory to the cloned folder:

```python
$ cd configure-flask-to-use-postgresql
```

- Create and activate a virtual environment.

```python
$ python3 -m venv venv
$ source venv/bin/activate
```

- Install project dependancies.

```python
(venv)$ pip3 install -r requirements.txt
```

- Update project configurations as seen in the `.env-template` file.

```python
(venv)$ cp .env-template .env
```

- Start the server.

```python
(venv)$ flask run
```

- Navigate to your browser and paste the link http://127.0.0.1:5000 to see the actual application.