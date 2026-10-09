# -*- coding: utf-8 -*-
"""Poe as paginas internas a usar as mesmas classes da pagina inicial."""
import io, os, re, os, glob
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),'')
os.chdir(BASE)

home=io.open('index.html',encoding='utf-8').read()
CSS_BASE=re.search(r'<style id="home-light">(.*?)</style>',home,re.S).group(1)
CSS_PAG=io.open(S+'paginas.css',encoding='utf-8').read()
NOVO='    <style id="home-light">\n'+CSS_BASE+CSS_PAG+'    </style>'

alvos=[p for p in [q for q in glob.glob('**/index.html',recursive=True) if not q.startswith('propostas/')]
       if p!='index.html' and not (p.startswith('blog/') and p!='blog/index.html')
       and p!='diagnostico/index.html']

rel=[]
for p in alvos:
    h=io.open(p,encoding='utf-8').read(); antes=h; notas=[]

    # 1. CSS: substituir o bloco embutido pelo novo
    h=re.sub(r'<style id="home-light">.*?</style>', lambda m: NOVO, h, flags=re.S)

    # 2. o titulo, o sobretitulo e o lead passam a usar as classes da home
    n=len(re.findall(r'class="page-hero__title"',h))
    h=h.replace('class="page-hero__title"','class="h1 page-hero__title"')
    h=h.replace('class="page-hero__eyebrow"','class="eyebrow"')
    h=h.replace('class="page-hero__lead"','class="lead page-hero__lead"')
    if n: notas.append('hero')

    # 3. corridas de prosa: a segunda seccao seguida nao soma padding
    corpo=re.search(r'<main.*?</main>',h,re.S)
    if corpo:
        m0=corpo.group(0); m=m0
        def simples(tag):
            return ('class="section"' in tag)
        # percorrer as seccoes por ordem
        secs=list(re.finditer(r'<section class="section"><div class="container"><div class="prose">',m))
        # marcar as que vem imediatamente depois de outra igual
        saltos=0
        partes=re.split(r'(<section class="[^"]*">)',m)
        saida=[]; anterior_prosa=False
        for i,parte in enumerate(partes):
            if parte.startswith('<section class="'):
                cls=re.match(r'<section class="([^"]*)"',parte).group(1)
                seguinte=partes[i+1] if i+1<len(partes) else ''
                eh_prosa=(cls=='section') and seguinte.lstrip().startswith('<div class="container"><div class="prose">')
                if eh_prosa and anterior_prosa:
                    parte='<section class="section section--seguida">'; saltos+=1
                anterior_prosa=eh_prosa
            saida.append(parte)
        m=''.join(saida)
        if saltos: notas.append(f'{saltos} seccoes coladas')
        h=h.replace(m0,m)

    if h!=antes:
        io.open(p,'w',encoding='utf-8').write(h)
    rel.append((p,', '.join(notas) or '-'))

print(f"{len(rel)} paginas normalizadas")
for p,n in rel: print(f"  {p:50} {n}")
