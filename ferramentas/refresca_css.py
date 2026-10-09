# -*- coding: utf-8 -*-
"""Reescreve o bloco <style id="home-light"> em TODAS as paginas, blog incluido."""
import io, os, re, os, glob
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),'')
os.chdir(BASE)
home=io.open('index.html',encoding='utf-8').read()
CSS_BASE=re.search(r'<style id="home-light">(.*?)</style>',home,re.S).group(1)
CSS_PAG=io.open(S+'paginas.css',encoding='utf-8').read()
NOVO='<style id="home-light">\n'+CSS_BASE+CSS_PAG+'    </style>'
n=0
for p in [q for q in glob.glob('**/index.html',recursive=True) if not q.startswith('propostas/')]:
    if p=='index.html': continue
    h=io.open(p,encoding='utf-8').read()
    if '<style id="home-light">' not in h: continue
    novo=re.sub(r'<style id="home-light">.*?</style>', lambda m: NOVO, h, flags=re.S)
    if novo!=h: io.open(p,'w',encoding='utf-8').write(novo); n+=1
print(f"CSS refrescado em {n} paginas")
