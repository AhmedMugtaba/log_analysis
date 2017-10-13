#! /usr/bin/env python

import psycopg2 as pg2

# connect to the database


def connect():
    try:
        db = pg2.connect(dbname='news')
        cursor = db.cursor()
        return db, cursor
    except:
        print "<Unable to conncet to the database>"


# Q1 - What are the most popular three articles of all time?


def Top_articles():
    db, cursor = connect()
    query = """
        select title, count(*) as page_views
        from articles join log
        on log.path = concat('/article/', articles.slug)
        where status !='/'
        group by articles.title
        order by page_views desc
        LIMIT 3;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


print "Most popular articles:"
for (title, count) in Top_articles():
    print "    {} - {} views".format(title, count)
print "-" * 70

# Q2 - Who are the most popular article authors of all time?


def Top_authors():
    db, cursor = connect()
    query = """
        select name, page_views as views
        from top_authors
        join authors on top_authors.author = authors.id
        limit 4;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


print "Most popular authors:"
for (name, views) in Top_authors():
    print "    {} - {} views".format(name, views)
print "-" * 70

# Q3 - On which days did more than 1% of requests lead to errors?


def daily_error():
    db, cursor = connect()
    query = """
        select date, daily_error
        from daily_error
        where daily_error > 1;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


print "Days with more than 1% requests error:"
for (date, daily_error) in daily_error():
    print "    {} - {:}% errors ".format(date, daily_error)
