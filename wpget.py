# coding=utf-8

import argparse
from wikitools import wiki
from wikitools import api
	
wp_langs = set(["vo","io","ia","an","kw","nrm","se","gd","is","lb","ga","nn","no","eo","bpy","et","eu","fo","csb","br","ksh","sv","new","sl","fi","sa","fiu-vro","cy","frp","ast","wa","nl","co","da","lt","fy","sk","to","lad","bs","pl","he","gl","lv","hr","cs","rm","ca","lmo","dv","mk","oc","de","pdc","it","hu","mi","pms","sr","fr","ka","vec","fur","os","bg","ja","cv","sq","mt","ro","el","li","en","tg","nap","uk","pag","pam","yi","af","sco","pt","nah","ceb","tr","be-x-old","scn","nds","ht","be","ru","ms","war","diq","es","ko","th","tt","ku","hy","udm","te","su","id","fa","ilo","als","uz","qu","vi","az","map-bms","yo","ba","ta","sw","zh","kn","mr","am","ar","jv","mn","sc","ml","bn","ks","tpi","ln","tl","zh-yue","ur","zh-min-nan","mg","hi","ne","ps","si","gu","pa"])

wp_category_prefixes = set(['category', 'kategorie', 'catégorie'])

def cli():
	"""wrangling the command line stuff"""
	parser = argparse.ArgumentParser(description='retreives a reasonable set of wikipedia pages. limited to 500 pages per category.')
	parser.add_argument('--recursive', '-r', action='count', default=False, help='if a category url is given, wpget will also process sub-categories recursivly')
	parser.add_argument('--lang', '-l', type=str, choices=wp_langs, metavar='LANG', default='en', help='retreive pages from different locales than"en"')
	parser.add_argument('url', type=str, metavar='TARGET', help='name of page or category, eg"Barack Obama" or"Category:Presidents_of_the_United_States"')
	parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
	parser.add_argument('--database', '-d', metavar='FILE', type=argparse.FileType('w'), default='wpget.db', help='specifies which database wpget should write to (defaults to wpget.db)')
	parser.add_argument('--content-dir', '-c', metavar='PATH', type=argparse.FileType('w'), help='specifies the path where wpget should store page contents (one file per page). otherwise content will be stored in sqlite database')
	args = parser.parse_args()
	main(args)	


def main(args):
	"""this is where the scraping happens"""
	if ':' in args.url:
		ns,title = args.url.split(':')
		if ns.lower() in wp_category_prefixes:
			process_category(title, args)
			exit()
		else:
			print "unknown namespace %s. try 'Category:' instead."
			exit(-1)
	process_page(args)
	

def init_wp_api(args):
	global site
	site = wiki.Wiki('http://%s.wikipedia.org/w/api.php' % args.lang)
	

def process_category(title, args):
	print "category", title
	init_wp_api(args)
	pages,subcat = category_members('Category:'+title)
	print pages


def process_page(args):
	print "page", args.url
	init_wp_api(args)
	src = page_source([args.url])
	print src
	

def page_source(pagetitles):
	""" return source text of latest revision for a set of pages """
	result = wp_query(prop='revisions', titles=pagetitles, rvprop='content')
	pages = result['query']['pages']
	res = []
	for key in pages:
		page = pages[key]
		res.append(page['revisions'][0]['*'])
	return res[0]

	
def category_members(cat):
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
