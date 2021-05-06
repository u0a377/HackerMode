import os
import re

import requests
from N4Tools.Design import ThreadAnimation
from bs4 import BeautifulSoup

with open(os.path.abspath(__file__).rsplit("/",1)[0]+"/flask_app.py") as file:
    app = file.read()

class Source:
    def __init__(self, url, Name, html):
        # url -> domin
        self.url = url
        self.domin = '//'.join([x for x in url.split('/') if x][:2])
        self.html = BeautifulSoup(html, "html.parser")
        self.urls = []
        self.Name = Name
        # paths -> app
        self.Paths = [
            f"{Name}",
            f"{Name}/__main__.py",
            f"{Name}/static",
            f"{Name}/templates",
        ]

    def write(self, Name, text):
        with open(Name, "wb") as f:
            f.write(text)

    def Text(self, text):
        for nc in range(8):
            text = text.replace(f"${nc}", f"\033[1;3{nc}m")
        return text.replace("$$", "\033[0m")

    @ThreadAnimation()
    def Install(Thread, self, url):
        out = None
        try:
            out = requests.get(url)
        except Exception as e:
            print(f"\033[1;31mERROR    \033[1;32m: \033[0m{e}")
            out = None
        Thread.kill()
        return out

    def Create(self, tag, attr, expr):
        Name = self.Name
        isurl = lambda u: True if re.findall('((http|ftp)s?://.*?)', get) else False
        for src in self.html.find_all(tag):
            if (get := src.get(attr)) and (get := get.strip()) and not get.endswith('/'):
                path = f"{{{{ url_for('static', filename='{get.split('/')[-1].replace(' ', '_')}') }}}}"
                if isurl(get):
                    self.urls.append(get)
                    src[attr] = path
                elif ((st := get.startswith('/')) or expr):
                    self.urls.append(self.domin + ("/" if not st else '') + get)
                    src[attr] = path

    def Setup(self):
        Name = self.Name
        # print -> Setup: NameFile
        for s in self.Paths:
            if not os.path.exists(s) and not s.endswith('index.py'):
                if s.endswith('__main__.py'):
                    # write __main__.py -> Flask server
                    self.write(s, app.encode())
                else:
                    os.mkdir(s)
                print(self.Text(f"$2Setup    $1: $$") + s)
            else:
                print(self.Text(f"$3Exists   $1: $$") + s)
        index = os.path.join(Name, "templates", "index.html")
        print(self.Text(f"$2Setup    $1: $$") + index)

    def Start(self):
        # Setup dir and file -> app
        self.Setup()
        self.Create("link", "href", True)
        self.Create("script", "src", True)
        self.Create("img", "src", True)
        # self.Create("meta", "content", False)
        self.write(os.path.join(self.Name, "templates", "index.html"), self.html.prettify().encode())

        for url in set(self.urls):
            path = os.path.join(self.Name, "static", url.split('/')[-1])
            print(self.Text(f"$2Download$1 :$$ {path}"))
            if (install := self.Install(url)):
                self.write(path, install.content)
            else:
                print(self.Text(f"$1ERROR    :$$ {url}"))
