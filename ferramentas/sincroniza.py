# -*- coding: utf-8 -*-
import io, os,re,os,glob
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(BASE)
home=io.open('index.html',encoding='utf-8').read()
NAV=re.search(r'(<header class="nav">.*?</header>)',home,re.S).group(1).replace('href="#casos"','href="/#casos"').replace('href="#servicos"','href="/#servicos"').replace('href="#contacto"','href="/#contacto"')
FOOT=re.search(r'(<footer class="footer">.*?</footer>)',home,re.S).group(1)
n=0
for p in [q for q in (x.replace(os.sep,'/') for x in glob.glob('**/index.html',recursive=True)) if not q.startswith('propostas/')]:
    if p=='index.html' or p.startswith('en/'): continue
    h=io.open(p,encoding='utf-8').read(); a=h
    h=re.sub(r'<header class="nav"[^>]*>.*?</header>', lambda m:NAV, h, flags=re.S)
    h=re.sub(r'<footer class="footer"[^>]*>.*?</footer>', lambda m:FOOT, h, flags=re.S)
    if h!=a: io.open(p,'w',encoding='utf-8',newline='\n').write(h); n+=1
print(f"nav e rodape sincronizados em {n} paginas")

# As paginas em ingles tem navegacao e rodape proprios, com a fonte em en/index.html.
if os.path.isfile('en/index.html'):
    casa=io.open('en/index.html',encoding='utf-8').read()
    NAV_EN=re.search(r'(<header class="nav">.*?</header>)',casa,re.S).group(1)
    FOOT_EN=re.search(r'(<footer class="footer">.*?</footer>)',casa,re.S).group(1)
    m=0
    for p in (x.replace(os.sep,'/') for x in glob.glob('en/**/index.html',recursive=True)):
        if p=='en/index.html': continue
        h=io.open(p,encoding='utf-8').read(); a=h
        h=re.sub(r'<header class="nav"[^>]*>.*?</header>', lambda z:NAV_EN, h, flags=re.S)
        h=re.sub(r'<footer class="footer"[^>]*>.*?</footer>', lambda z:FOOT_EN, h, flags=re.S)
        if h!=a: io.open(p,'w',encoding='utf-8',newline='\n').write(h); m+=1
    print(f"nav e rodape em ingles sincronizados em {m} paginas")
