
import sqlite3
import schema


def init_or_open_db(args):
	"""
	if the db doesn't exist, wpget will create a new one and setup
	the database schema. otherwise it will open the existing db and
	assume that it has the right schema.
	"""
	conn = sqlite3.connect(args.database.name)
	c = conn.cursor()
	c.execute("select * from sqlite_master where type='table';")
	tables = c.fetchall()
	if len(tables) == 0:
		# empty database
		c.executescript(schema.create_db_schema)
		conn.commit()
	else:
		# validate existing database
		if 'wpget_meta' not in tables:
			raise DBError("invalid database (non-empty and table wpget_meta does not exist)")
		c.execute("select version from wpget_meta")
		v = c.fetchone()
		if v != schema.version:
			raise DBError("wrong db schema version (is %s, expecting %s). Sorry, migration not implemented yet" % (v, schema.version))
	return conn

	
def store_page(conn, id, title, content):
	conn.execute("insert or replace into page values (?, ?, ?, ?)", (id, title, content, _now()))
	conn.commit()
	

def store_category(conn, id, title, content):
	conn.execute("insert or replace into category values (?, ?, ?, ?)", (id, title, content, _now()))
	conn.commit()


def store_pagecat(conn, page_id, cat_id):
	conn.execute("insert or replace into page2category values (?, ?, ?)", (page_id, cat_id, _now()))
	conn.commit()
	

def _now():
	import datetime
	return datetime.datetime.now().isoformat(" ")


class DBError(Exception):
	pass