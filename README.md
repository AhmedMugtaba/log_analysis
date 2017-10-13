# Project Description
A cml script that will connect to database, use SQL queries to analyze the log data, and print out the answers to some questions.
### Questions
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?
### Getting Started 
#### Pre-requisite
Python, virtual machine, vagrant, VirtualBox
#### Download pre-requisite
Install python: <br />
To install python go to: https://www.python.org/downloads/ <br />
Install Vagrant:<br />
To install vagrant go to: https://www.vagrantup.com/downloads.html <br />
Install Virtualbox: <br />
To Install Virtual Box go to: https://www.virtualbox.org/wiki/Downloads 
Install the virtual machine (VM):<br />
To install VM go to: https://github.com/udacity/fullstack-nanodegree-vm <br />
How to start the VM:<br />
  * After downloading the VM ```cd``` to the VM and from the terminal, ```cd``` to directory called vagrant <br /> 
 then from the terminal, inside the vagrant subdirectory, run the command <br /> 
  ```vagrant up``` <br />
  * When ```vagrant up``` is finished, you can run this command below to login to the VM!<br />
  ```vagrant ssh``` 
  * Inside the VM, change directory and ```cd``` to  ```/vagrant```
## Running the database: 
After login to the VM the PostgreSQL database server will automatically be started inside the VM. You can use the ```psql``` command-line tool to access it and run SQL statements<br />
Logging out and in <br />
If you type ```exit``` or ```Ctrl-D``` at the shell prompt inside the VM, you will be logged out, and put back into your host computer's shell. To log back in, make sure you're in the same directory and type ```vagrant ssh``` again.
### Download the "news" database: 
Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), You will need to unzip this file after downloading it. The file inside is called ```sql newsdata.sql```. Put this file into the ```vagrant``` directory, which is shared with your virtual machine.<br />
To load the data ```cd``` into the ```vagrant``` <br />
  And then use the command <br />
  ```psql -d news -f newsdata.sql``` <br />
#### To intract with data use these command <br />
  * ```psql``` — the PostgreSQL command line program
  * ```-d news``` — connect to the database named news which has been set up in the VM
  * ```-f newsdata.sql ```— run the SQL statements in the file newsdata.sql
## Exploring the date<br />
Once you have the data loaded into your database, connect to your database using ```sql psql -d news``` and explore the tables using the ```\dt``` and ```\d```.to display tables<br />

The database includes three tables:<br />

The ```authors``` table includes information about the authors of articles.
The ```articles``` table includes the articles themselves.
The ```log``` table includes one entry for each time a user has accessed the site.

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

## Running the Program:  
### After creating the view and from inside the vm run <br />
``` python 
python pgsql.py
```
