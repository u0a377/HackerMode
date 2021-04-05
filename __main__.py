import sys
from setup import Installer

class HackerMode:
    argv = [
        'install',
        'update',
        'upgrade',
        'check'
    ]

    def start(self,argv):
        if argv[1:]:
            for argv in argv[1:]:
                try:
                    getattr(self,argv)()
                except AttributeError:
                    print ('help msg')
        else:
            from base.shell import MainShell
            from rich.traceback import install
            from base.system import AppApi
            install()
            Shell = MainShell()
            if not AppApi.activ():
                print("# Time out.\n# Refresh the time from within the 'Hacker Mode' application.")
                return
            while True:
                try:
                    Shell.cmdloop()
                except KeyboardInterrupt:
                    print('')

    def install(self):
        Installer.install()

    def update(self):
        Installer.update()

    def upgrade(self):
        Installer.install()

    def check(self):
        Installer.check()

if __name__ == '__main__':
    HackerMode = HackerMode()
    HackerMode.start(sys.argv)
