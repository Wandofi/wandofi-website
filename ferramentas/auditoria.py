# -*- coding: utf-8 -*-
import io, os, re, os, glob, collections
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(BASE)

def url(p):
    r=os.path.relpath(p,BASE).replace(os.sep,'/')
    return '/' if r=='index.html' else '/'+os.path.dirname(r)+'/'

paginas={}
for p in [q for q in (x.replace(os.sep,'/') for x in glob.glob('**/index.html', recursive=True)) if not q.startswith('propostas/')]:
    u='/' if p=='index.html' else '/'+os.path.dirname(p)+'/'
    paginas[u]=p
paginas['/']='index.html'   # a home a publicar

saida=collections.defaultdict(set); entrada=collections.Counter()
for u,p in paginas.items():
    h=io.open(p,encoding='utf-8').read()
    corpo=re.search(r'<main id="main".*?</main>', h, re.S)
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
# Paginas com noindex. Nao sao erro nenhum: sao paginas de destino de anuncios
# ou do link da bio, que existem para quem chega por fora e nao para disputar
# pesquisas com as paginas a serio. Uma delas ESPERA-SE que esteja fora do
# sitemap, sem ligacoes de dentro, e sem caminho desde a inicial.
#
# Ate 19/11/2026 a auditoria acusava a /plano/ nessas tres linhas a cada
# corrida. Um aviso que aparece sempre e que esta sempre certo deixa de ser
# lido, e no dia em que aparecesse uma orfa a serio ninguem reparava. Uma
# verificacao so serve se estiver calada quando esta tudo bem.
#
# O que passa a ser erro e a CONTRADICAO: uma pagina noindex dentro do
# sitemap, que e pedir ao Google que a visite e que nao a guarde.
noindex={u for u,p in paginas.items()
         if re.search(r'<meta name="robots" content="[^"]*noindex', io.open(p,encoding='utf-8').read())}

orfas=[u for u in paginas if u!='/' and entrada[u]==0 and u not in noindex]
smap=set(re.findall(r'<loc>https://wandofi\.pt(/[^<]*)</loc>', io.open('sitemap.xml',encoding='utf-8').read()))
sem_caminho=[u for u in paginas if u not in prof and u not in noindex]
fora_smap=sorted(set(paginas)-smap-noindex)
contradicao=sorted(noindex & smap)

print(f"paginas: {len(paginas)}  |  ligacoes de conteudo: {sum(len(v) for v in saida.values())}")
print(f"profundidade maxima: {max(prof.values())} | media: {sum(prof.values())/len(prof):.2f}")
print(f"sem caminho desde a home: {sem_caminho or 'nenhuma'}")
print(f"orfas: {orfas or 'nenhuma'}")
print(f"partidos: {partidos or 'nenhum'}")
print(f"fora do sitemap: {fora_smap or 'nenhuma'}")
print(f"no sitemap mas sem pagina: {sorted(smap-set(paginas)) or 'nenhuma'}")
print(f"noindex e no sitemap ao mesmo tempo: {contradicao or 'nenhuma'}")
if noindex:
    print(f"fora do indice de proposito: {sorted(noindex)}")
print("\nmais ligadas:")
for u,n in entrada.most_common(12):
    print(f"  {u:42} {n:3} entradas   prof {prof.get(u,'-')}")
