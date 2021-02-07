import os
size=os.path
import sys
class Size:
    def __init__(self,namefile):
        self.namefile=namefile
    def sizenumFile(self):
        return[os.path.getsize(self.namefile),self.namefile]
    def sizenumDir(self):                                                                                                                                                                if os.path.isfile(self.namefile):return self.sizenumFile()
        elif os.path.isdir(self.namefile):
            s=0
            for d,i,r in  os.walk(self.namefile):
                for n in r:s+=os.path.getsize(os.path.join(d,n))
            return[s,self.namefile]
        else:
            print (f"[Errno 2] No such file or directory: '{os.path.join('/',*__file__.split('/')[:-1],self.namefile)}'");os.sys.exit()
    def GetSize(self):
        F=self.sizenumDir()
        s=F[0]
        G=s/1024
        S='kB'
        if G>1024:
            G=G/1024
            S='MB'
            if G>1024:
                G=G/1024
                S='GB'
        G=str(G).split('.')
        return f'{F[1]} : \033[94m{G[0]}.{G[1][0:2]} {S}'
for p in sys.argv[1:]:
    print (f"\033[93m{Size(p).GetSize()}\033[0m")
