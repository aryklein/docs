Frequently used commands
========================

Showing databases
-----------------

SHOW DATABASES lists the databases on the Mariadb server host:

::

  $ mysql -uusername -ppassword
  MariaDB [(none)]> show databases;


Dumping a database
------------------

Dumping only one database:

::

  $ mysqldump -uUSER -pPASSWORD [database_name] > filename.sql


Backup a single database to compressed version of the sql file

::

  $ mysqldump -uUSER -pPASSWORD [database_name] | gzip > filename.sql.gz
  $ mysqldump -uUSER -pPASSWORD [database_name] | bzip2 > filename.sql.bz2


You can backup more than one database at the same time:

::

  $ mysqldump -uUSER -pPASSWORD --databases [database_name_1] [database_name_2] [database_name_n] > filename.sql


Dumping ALL databases:

::

  $ mysqldump --all-databases -uUSER -pPASSWORD > filename.sql




Restoring
---------

Using the dump file, it is possible to restore the database with all its tables to a new MySQL server.

Create the database:

::

  $ mysql -uUSER -pPASSWORD

The USER in this case will usually be root. At the MariaDB console run:

::

  MariaDB [(none)]> create database [database_name];
  MariaDB [(none)]> grant all privileges on [database_name].* to '[new_user]'@'[hostname]' identified by '[new_user_password]';
  MariaDB [(none)]> exit;


``[hostname]`` could be '%' that means ALL hosts


Restoring a database dump file:

::

  mysql -uUSER -pPASSWORD [database_name] < filename.sql


Restoring ALL

::

  mysql -uUSER -pPASSWORD < alldb.sql
  mysql 'flush privileges;'


