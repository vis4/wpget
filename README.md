# wpget

**wpget** is a Python script that downloads a set of pages from Wikipedia into a local sqlite database.

ToDos:

* design db schema
* set up sqlite database 

Usage:

```bash
# retrieve all pages in a category and their sub categories
$ wpget --recursive Category:Media_companies_of_Germany
# retrieve a page from the German wikipedia
$ wpget --lang=de "Axel Springer AG"
```

