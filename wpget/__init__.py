# coding=utf-8
"""
a cool small utility for loading stuff from wikipedia
"""

import argparse

from parser import *

wp_langs = set(["vo", "io", "ia", "an", "kw", "nrm", "se", "gd", "is", "lb", "ga", "nn", "no", "eo", "bpy", "et", "eu", "fo", "csb", "br", "ksh", "sv", "new", "sl", "fi", "sa", "fiu-vro", "cy", "frp", "ast", "wa", "nl", "co", "da", "lt", "fy", "sk", "to", "lad", "bs", "pl", "he", "gl", "lv", "hr", "cs", "rm", "ca", "lmo", "dv", "mk", "oc", "de", "pdc", "it", "hu", "mi", "pms", "sr", "fr", "ka", "vec", "fur", "os", "bg", "ja", "cv", "sq", "mt", "ro", "el", "li", "en", "tg", "nap", "uk", "pag", "pam", "yi", "af", "sco", "pt", "nah", "ceb", "tr", "be-x-old", "scn", "nds", "ht", "be", "ru", "ms", "war", "diq", "es", "ko", "th", "tt", "ku", "hy", "udm", "te", "su", "id", "fa", "ilo", "als", "uz", "qu", "vi", "az", "map-bms", "yo", "ba", "ta", "sw", "zh", "kn", "mr", "am", "ar", "jv", "mn", "sc", "ml", "bn", "ks", "tpi", "ln", "tl", "zh-yue", "ur", "zh-min-nan", "mg", "hi", "ne", "ps", "si", "gu", "pa"])

wp_category_prefixes = set(['category', 'kategorie', 'catégorie'])


def cli():
    """command line stuff"""
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
        ns, title = args.url.split(':')
        if ns.lower() in wp_category_prefixes:
            process_category(title, args)
            exit()
        else:
            print "unknown namespace %s. try 'Category:' instead."
            exit(-1)
    else:
        process_page(args)
