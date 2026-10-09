# -*- coding: utf-8 -*-
import io, os, re, os, glob, collections
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(BASE)

def url(p):
    r=os.path.relpath(p,BASE)
    return '/' if r=='index.html' else '/'+os.path.dirname(r)+'/'

paginas={}
for p in [q for q in glob.glob('**/index.html', recursive=True) if not q.startswith('propostas/')]:
    u='/' if p=='index.html' else '/'+os.path.dirname(p)+'/'
    paginas[u]=p
paginas['/']='index.html'   # a home a publicar

saida=collections.defaultdict(set); entrada=collections.Counter()
for u,p in paginas.items():
    h=io.open(p,encoding='utf-8').read()
    corpo=re.search(r'<main.*?</main>', h, re.S)
    corpo=corpo.group(0) if corpo else h
    for href in re.findall(r'href="(/[^"#?]*)"', corpo):
        if re.search(r'\.(css|js|png|jpg|jpeg|webp|svg|ico|xml|txt)$', href): continue
        if not href.endswith('/'): href=href+'/'
        if href==u: continue
        saida[u].add(href); entrada[href]+=1

partidos=sorted({h for s in saida.values() for h in s} - set(paginas))
# profundidade BFS a partir de /
prof={'/':0}; fila=['/']
while fila:
    x=fila.pop(0)
    for y in saida.get(x,()):
        if y in paginas and y not in prof:
            prof[y]=prof[x]+1; fila.append(y)
orfas=[u for u in paginas if u!='/' and entrada[u]==0]
smap=set(re.findall(r'<loc>https://wandofi\.pt(/[^<]*)</loc>', io.open('sitemap.xml',encoding='utf-8').read()))

print(f"paginas: {len(paginas)}  |  ligacoes de conteudo: {sum(len(v) for v in saida.values())}")
print(f"profundidade maxima: {max(prof.values())} | media: {sum(prof.values())/len(prof):.2f}")
print(f"sem caminho desde a home: {[u for u in paginas if u not in prof] or 'nenhuma'}")
print(f"orfas: {orfas or 'nenhuma'}")
print(f"partidos: {partidos or 'nenhum'}")
print(f"fora do sitemap: {sorted(set(paginas)-smap) or 'nenhuma'}")
print(f"no sitemap mas sem pagina: {sorted(smap-set(paginas)) or 'nenhuma'}")
print("\nmais ligadas:")
for u,n in entrada.most_common(12):
    print(f"  {u:42} {n:3} entradas   prof {prof.get(u,'-')}")
