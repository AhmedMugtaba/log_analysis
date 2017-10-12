# Project Description
A cml scrip that will connect to database, use SQL queries to analyze the log data, and print out the answers to some questions.
### Questions
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?
### Getting Started 
#### Prerequisite
Python3, virtual machine, vagrant
#### Running project
Install Vagrant:<br />
https://www.vagrantup.com/downloads.html <br />
Download the VM:<br />
https://github.com/udacity/fullstack-nanodegree-vm <br />
Start the VM:<br />
  * From the terminal, inside the vagrant subdirectory, run the command ```vagrant up``` <br />
  * When vagrant up is finished running,you can run ```vagrant ssh``` to log in the VM! <br />
  * Inside the VM, change directory to /vagrant
### Download the data
### To load the data  
```cd``` into the ```vagrant``` <br />
  And then use the command <br />
  ```psql -d news -f newsdata.sql``` <br />
#### To intract with data use these command 
  * ```psql``` — the PostgreSQL command line program
  * ```-d news``` — connect to the database named news which has been set up for you
  * ```-f newsdata.sql ```— run the SQL statements in the file newsdata.sql
## create the following views 

```sql
   Create view top_authors as
   select author, count(*) as page_views
   from articles join log
   on log.path = concat('/article/', articles.slug)
   where status !='/'
   group by articles.author 
   order by page_views desc
   limit 3;
```

```sql
  Create view Requests as 
  select time ::timestamp::date as date, count(*) as total_requests
  from log
  group by date
  order by total_requests desc;
```
```sql
 Create view error as 
 select time ::timestamp::date as date, count(*) as requests_failures
 from log
 where status = '404 NOT FOUND'
 group by date
 order by requests_failures desc;
```
```sql
Create view daily_error as 
select error.date, round( 100 * (cast(error.requests_failures as decimal)/cast(Requests.total_requests as decimal)),2) as daily_error
from Requests join error
on Requests.date = error.date
order by daily_error desc;
```
