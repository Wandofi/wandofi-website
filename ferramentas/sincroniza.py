# -*- coding: utf-8 -*-
import io, os,re,os,glob
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(BASE)
home=io.open('index.html',encoding='utf-8').read()
NAV=re.search(r'(<header class="nav">.*?</header>)',home,re.S).group(1).replace('href="#casos"','href="/#casos"')
FOOT=re.search(r'(<footer class="footer">.*?</footer>)',home,re.S).group(1)
n=0
for p in [q for q in glob.glob('**/index.html',recursive=True) if not q.startswith('propostas/')]:
    if p=='index.html' or (p.startswith('blog/') and p!='blog/index.html'): continue
    h=io.open(p,encoding='utf-8').read(); a=h
    h=re.sub(r'<header class="nav"[^>]*>.*?</header>', lambda m:NAV, h, flags=re.S)
    h=re.sub(r'<footer class="footer"[^>]*>.*?</footer>', lambda m:FOOT, h, flags=re.S)
    if h!=a: io.open(p,'w',encoding='utf-8').write(h); n+=1
print(f"nav e rodape sincronizados em {n} paginas")
