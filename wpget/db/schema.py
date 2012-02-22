
import datetime

version = "0.0.1"
created_at = datetime.datetime.now().isoformat(" ")

create_db_schema = """

create table wpget_meta(
	version,
	created_at,
	last_updated_at
);

insert into wpget_meta values ("%s", "%s", "%s");

create table page(
	id int,
	title,
	content,
	last_scraped_at
);

create unique index pageid on page ( id );

create table category(
	id int,
	title,
	content,
	last_scraped_at
);

create unique index catid on category ( id );

create table page2category(
	page_id int,
	category_id int,
	last_scraped_at
);

create unique index page2cat on page2category ( page_id, category_id );

""" % (version, created_at, created_at)

