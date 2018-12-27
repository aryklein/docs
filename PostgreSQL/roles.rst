PostgreSQL Permission Concepts
==============================

PostgresSQL manages permissions through the concept of **roles**, which is akin to a user.
Roles can represent groups of users in the PostgreSQL ecosystem as well. Roles can be
members of other roles, allowing them to take permissions of previously defined roles.
PostgreSQL establishes the capacity for roles to assign privileges to database objects they
own, enabling access and actions to those objects.

How to View Roles in PostgreSQL
-------------------------------

In the PostgreSQL prompt interface, run:

::

    postgres=# \du

Creating Roles in PostgreSQL
----------------------------

One of the ways to create a new roles is from the Postgres interface:

::

    postgres=# CREATE ROLE new_role_name;
    
Another way is from the Linux Shell using the ``createuser`` command.

::

    $ createuser new_user
