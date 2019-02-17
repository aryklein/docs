PostgresSQL cheat sheet
=======================

This is a personal Postgres cheat sheet. All these commands were tested on Postgres 11.
If you have reached this document, please use it with caution. For better information, 
refer to the official Postgres documentation.

PostgreSQL Permission Concepts
------------------------------

PostgresSQL manages permissions through the concept of **roles**, which is akin to a user.
Roles can represent groups of users in the PostgreSQL ecosystem as well. Roles can be
members of other roles, allowing them to take permissions of previously defined roles.
PostgreSQL establishes the capacity for roles to assign privileges to database objects they
own, enabling access and actions to those objects.


How to view roles in PostgreSQL
-------------------------------

In the PostgreSQL prompt interface, run:

.. code-block:: sql

    postgres=# \du


Creating roles in PostgreSQL
----------------------------

From the Postgres interface (using ``psql``), to create a role that has the ``LOGIN`` attribute
and a non-empty MD5-encrypted password:

.. code-block:: sql

    postgres=# CREATE ROLE <role_name> WITH LOGIN ENCRYPTED PASSWORD '<password>';
    
From the Linux shell using the ``createuser`` command, to create a non-superuser role that has
the LOGIN attribute:

.. code-block:: bash

    $ sudo -i -u postgres
    $ createuser -PE role_name 

``-P`` prompts to set a password for the new role and ``-E`` indicates that the password should
be stored as an `MD5-encrypted` string.

To create a Superuser role from the PostgreSQL interface:

.. code-block:: sql

    postgres=#CREATE ROLE <role_name> WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD '<password>';

From Linux shell with ``-s`` flag:

.. code-block:: bash

    $ sudo -i -u postgres
    $ createuser -sPE role_name

A list of valid `parameters` for a role can be found here:
https://www.postgresql.org/docs/current/sql-createrole.html


Dropping a role
---------------

From Postgres interface (``psql``):

.. code-block:: sql

    postgres=# DROP ROLE <role_name>;

From Linux shell:

.. code-block:: bash

    $ sudo -i -u postgres
    $ dropuser -i role_name

``-i`` provides a confirmation prompt, which is a good safety measure when running a potentially
destructive command.


Change role password
--------------------

To modify the password of a role:

.. code-block:: sql

    postgres=# ALTER ROLE <role_name> WITH PASSWORD '<new_password>';

To remove the password:

.. code-block:: sql

    postgres=# ALTER ROLE <role_name> WITH PASSWORD NULL;


Change the attribute of a PostgreSQL role
-----------------------------------------

Use ``ALTER ROLE`` to change the attribute of a role:

.. code-block:: sql

    postgres=# ALTER ROLE <role_name> WITH <option>;

To see a full list of the options:

.. code-block:: sql

    postgres=# \h ALTER ROLE


Create a database
-----------------

From the PostgreSQL interface (``psql``) to create new database with some role as a owner:

.. code-block:: sql

    postgres=# CREATE DATABASE <db_name> OWNER <role_name>;

If no owener is specified, ``postgres`` user will be the owner.

To list all databases, run:

.. code-block:: sql

    postgres=# \l+

To connect to the new databases, run:

.. code-block:: sql

    postgres=# \c <db_name>
    postgres=# \conninfo


How to Grant Permissions in PostgreSQL
--------------------------------------

When a database or table is created, usually only the role that created it (not including
roles with superuser status) has permission to modify it. We can alter this behavior by
granting permissions to other roles.

We can grant permissions using the ``GRANT`` command. The general syntax is:

.. code-block:: sql

    postgres=# GRANT <permission_type> ON <table_name> TO <role_name>;

To see all permissions type, run:

.. code-block:: sql

    postgres=# \h GRANT

How to Remove Permissions in PostgreSQL
---------------------------------------

You can remove permissions using the ``REVOKE`` command. The revoke command uses almost
the same syntax as ``GRANT``:

.. code-block:: sql

    postgres=# REVOKE permission_type ON table_name FROM user_name;

Create a readonly user
----------------------

Read this article:
https://marcyes.com/2016/0922-messing-with-postgresql-users-and-permissions/
