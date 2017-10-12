import psycopg2 as pg2


# Q1 - What are the most popular three articles of all time?


def Top_articles (): 
	conn = pg2.connect(dbname='news')
	cur = conn.cursor()
	cur.execute(""" 
	select title, count(*) as page_views
	from articles join log
	on log.path = concat('/article/', articles.slug)
	where status !='/'
	group by articles.title
	order by page_views desc 
	LIMIT 3;
		""")
	result = cur.fetchall()
	conn.close()
	return result
print 'top 3 articles are :', Top_articles()

# Q2 - Who are the most popular article authors of all time?

def Top_authors (): 
	conn = pg2.connect(dbname='news')
	cur = conn.cursor()
	cur.execute(""" 
	 select name, page_views as views 
	 from top_authors 
	 join authors on top_authors.author = authors.id 
	 limit 4;
		""")
	result = cur.fetchall()
	conn.close()
	return result
print 'top 3 authors are:', Top_authors()

# Q3 - On which days did more than 1% of requests lead to errors? 

