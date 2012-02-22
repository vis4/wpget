	
from wikitools import wiki
from wikitools import api

from db import *

def init_wp_api(args):
	global site
	site = wiki.Wiki('http://%s.wikipedia.org/w/api.php' % args.lang)
	

def process_category(title, args):
	"""entry point when starting with a category"""
	init_wp_api(args)
	
	db = init_or_open_db(args)
	categories = _load_category('category:'+title, db, recursive=args.recursive)
	category_contents = _page_sources(ids=categories)
	for cat in category_contents:
		prefix,title = cat['title'].split(':')
		print "stored category", title
		store_category(db, cat['pageid'], title, cat['content'])
		
	
def _load_category(cat, db, parent_categories=[], recursive=False):
	""" recursivly load categories and their pages """
	# store category title for we will load its content later
	
	if isinstance(cat, (str,unicode)):
		cat = _page_info(cat)
	parent_categories.append(cat)
	
	print cat['title']

	# load a list of pages and sub categories
	pages,subcat = _category_members(cat['title'])
	print "found %d pages" % len(pages)
	
	# load page contents
	pageids = map(lambda p:p['pageid'], pages)
	page_contents = _page_sources(ids=pageids)

	# store pages and categories
	for page in page_contents:
		#print "stored page", page['title']
		store_page(db, page['pageid'], page['title'], page['content'])
		for cat in parent_categories:
			store_pagecat(db, page['pageid'], cat['pageid'])
	
	all_cat_ids = set()
	all_cat_ids.add(cat['pageid'])
	
	if recursive:
		for cat in subcat:
			cat_ids = _load_category(cat, db, parent_categories[:], recursive)
			for c in cat_ids:
				all_cat_ids.add(c)
	return all_cat_ids
	


def _page_info(title):
	""" return the page id for a given page title """
	res = wp_query(prop='info', titles=title)
	ids = list(res['query']['pages'])
	return res['query']['pages'][ids[0]]


def process_page(args):
	print "page", args.url
	init_wp_api(args)
	src = page_sources([args.url])[0][1]
	
	print src
	db = init_or_open_db(args)
	#store_page(db, 
	

def _page_sources(titles=None, ids=None):
	""" return source text of latest revision for a set of pages """
	params = dict(prop='revisions', rvprop='content')
	res = []
	if titles:
		pkey = 'titles'
		values = titles
	else:
		pkey = 'pageids'
		values = map(str, ids)
		
	# max 50 pages per request, so split up if needed
	for start in range(0, len(values), 50):
		end = min(len(values),start+50)
		vals = values[start:end]
		params[pkey] = '|'.join(vals)
		result = wp_query(**params)
		pages = result['query']['pages']
		keys = list(pages)
		print 'loading page %d to %d (%s ... %s)' % (start, end, pages[keys[0]]['title'], pages[keys[len(keys)-1]]['title'])
		for key in pages:
			page = pages[key]
			res.append(dict(pageid=page['pageid'], title=page['title'], content=page['revisions'][0]['*']))
	print len(values), len(res)
	return res

	
def _category_members(cat):
	""" returns a list of pages and sub-categories to a category """
	result = wp_query(list='categorymembers', cmlimit=500, cmtitle=cat)
	pages = []
	subcat = []
	res_pages = result['query']['categorymembers']
	for res in res_pages:
		if res['ns'] == 0: pages.append(res)
		elif res['ns'] == 14: subcat.append(res)
	return pages, subcat
	
	
def wp_query(**kwargs):
	""" wrapping the wikitools api """	
	kwargs['action'] = 'query'
	request = api.APIRequest(site, kwargs)
	
	result = request.query()
	return result

