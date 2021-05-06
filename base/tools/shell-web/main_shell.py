import json
import re

from N4Tools.Design import ThreadAnimation
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.data import JsonLexer

from html_shell import HtmlShell
from source import Source
from shell import BaseShell

class MainShell(BaseShell):  # Main Shell
    ToolName = "Shell-Web"

    def __init__(self,value, html, url, *args, **kwargs):
        super(MainShell, self).__init__(*args, *kwargs)
        self.value = value
        self.html = html
        self.url = url
        self.Names = {"rest": []}  # Mode: [ Urls ]
        for x in re.findall('"((http|ftp)s?://.*?)"', html.prettify()):
            x = x[0]
            if x.endswith('/'):
                self.Names["rest"].append(x)
            else:
                line = x.split('/')[-1]
                if '.' in line:
                    line = line.split('.')[-1]
                    if [c for c in re.findall('[\W]*', line) if c] or '_' in line:
                        self.Names["rest"].append(x)
                    else:
                        if line in self.Names:
                            self.Names[line].append(x)
                        else:
                            self.Names[line] = [x]
                else:
                    self.Names["rest"].append(x)
        self.Names = {
            a: list(set(self.Names[a]))
            for a in sorted(list(self.Names.keys()))
        }

    def do_html(self, arg):  # html Shell
        HtmlShell(self.html).cmdloop()

    def do_Flask(self, arg):
        if self.url:
            all = BeautifulSoup(arg, "html.parser")
            try:
                if (get := all.find("flask").get('filename')):
                    obj = Source(self.url, get, self.html.prettify())
                    obj.Start()
                else:
                    print("Flask <flask filename='Name' />")
            except NameError:
                print("Flask <flask filename='Name' />")
        else:
            print("Not URL...!")

    def complete_Flask(self, *args):
        return ["<flask filename=' ' />"]

    @ThreadAnimation()
    def Lexer_Json(self, Thread, Code):
        out = highlight(Code, JsonLexer(), TerminalFormatter())
        Thread.kill = True
        return out

    def do_Info(self, arg):
        if type(self.value) == str:
            print("Not info...!")
        elif len((f := [x for x in re.findall("[\W]*", arg.strip()) if x])) > 0:
            print(f"Not {f}...!")
        else:
            try:
                temp = eval(f'self.value.{arg}')
            except Exception as e:
                print("\033[1;31mERROR:\033[0m", e)
            else:
                if type(temp) == dict or arg == "headers":
                    print(
                        self.Lexer_Json(
                            str(
                                json.dumps(
                                    dict(temp),
                                    indent=3
                                )
                            )
                        )
                    )
                else:
                    print(temp)

    def complete_Info(self, line, *args):
        if type(self.value) == str:
            return ["None"]
        Del = ["text", "_content", "iter_content", "iter_lines", "json"]
        all = [
            x for x in dir(self.value)
            if not x.startswith('__') and x not in Del
        ]
        return [x for x in all if x.startswith(line)] if line else all

    def do_Link(self, arg):  # Links-Urls
        if arg:
            for x in (self.Names[arg]):
                print(f'\033[1;31m-> \033[1;37m{x}\033[0m')

    def complete_Link(self, line, *args):
        all = list(self.Names.keys()) + ["rest"]
        return [x for x in all if x.startswith(line)] if line else all
