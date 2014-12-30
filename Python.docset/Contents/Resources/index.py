#!/usr/bin/env python3
import bs4, os, re, sqlite3
os.chdir(os.path.dirname(__file__))
if os.path.isfile("docSet.dsidx"):
    os.remove("docSet.dsidx")
db = sqlite3.connect("docSet.dsidx")
cursor = db.cursor()
cursor.execute("CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);")
cursor.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")
root = "https://docs.python.org/3/"
for fname in ("genindex-all.html",):
    page = open(os.path.join("Documents", fname)).read()
    soup = bs4.BeautifulSoup(page)
    for tag in soup.find_all("a", {"href": re.compile("library/")}):
        name = tag.attrs["href"].strip()
        name = name.split("#")[-1]
        if not name: continue
        if name.startswith("cmdoption-"): continue
        if name.startswith("index-"): continue
        if name.startswith("opcode-"): continue
        if name.startswith("module-"):
            name = name.replace("module-", "")
        path = root + tag.attrs["href"].strip()
        print("{}: {}".format(name, path))
        cursor.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)",
                       (name, "func", path))

db.commit()
db.close()
