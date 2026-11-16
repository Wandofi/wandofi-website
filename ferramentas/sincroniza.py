# -*- coding: utf-8 -*-
"""Copia a navegacao e o rodape da inicial de cada lingua para as irmas.

O selector de lingua vive dentro da navegacao mas NAO e copiado: cada pagina
tem o seu, porque aponta para a pagina equivalente e nao para a inicial. Se
fosse copiado como o resto, uma passagem por aqui punha as 66 paginas a
apontar todas para /en/ e /fr/, que foi exactamente o erro que o
ferramentas/linguas.py veio corrigir. Por isso, ao escrever a navegacao nova,
o bloco <span class="idiomas"> de cada pagina e guardado antes e reposto
depois. As paginas que ainda nao tenham selector recebem o da fonte, que e o
comportamento antigo e serve para arrancar.
"""
import io, os, re, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

IDIOMAS = re.compile(r'<span class="idiomas".*?<!--/idiomas--></span>', re.S)


def poe_nav(h, nav_nova):
    """Escreve a navegacao nova, mas mantem o selector de lingua desta pagina.

    Os selectores sao repostos pela ordem em que aparecem: ha dois por pagina,
    o da barra e o do menu do telemovel, e sao iguais entre si."""
    meus = IDIOMAS.findall(h)
    seguinte = iter(meus)

    def repoe(_m):
        # Se a navegacao nova trouxer mais selectores do que a pagina tinha,
        # os que sobram levam o ultimo conhecido, que e o desta pagina na
        # mesma. O contador vive nesta chamada e nao entre paginas.
        return next(seguinte, meus[-1])

    nav = IDIOMAS.sub(repoe, nav_nova) if meus else nav_nova
    return re.sub(r'<header class="nav"[^>]*>.*?</header>', lambda _m: nav, h, flags=re.S)


def sincroniza(fonte, padrao, salta, etiqueta, arruma_ancoras=False):
    if not os.path.isfile(fonte):
        return
    casa = io.open(fonte, encoding='utf-8').read()
    nav = re.search(r'(<header class="nav">.*?</header>)', casa, re.S).group(1)
    if arruma_ancoras:
        for a in ('casos', 'servicos', 'contacto'):
            nav = nav.replace(f'href="#{a}"', f'href="/#{a}"')
    rodape = re.search(r'(<footer class="footer">.*?</footer>)', casa, re.S).group(1)

    n = 0
    for p in (x.replace(os.sep, '/') for x in glob.glob(padrao, recursive=True)):
        if p.startswith('propostas/') or p == fonte or salta(p):
            continue
        h = io.open(p, encoding='utf-8').read()
        antes = h
        h = poe_nav(h, nav)
        h = re.sub(r'<footer class="footer"[^>]*>.*?</footer>', lambda _m: rodape, h, flags=re.S)
        if h != antes:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
            n += 1
    print(f'nav e rodape {etiqueta} sincronizados em {n} paginas')


# As paginas portuguesas: fonte na inicial, e as ancoras passam a absolutas,
# porque numa pagina interna o #servicos sozinho nao vai dar a lado nenhum.
sincroniza('index.html', '**/index.html',
           lambda p: p.startswith('en/') or p.startswith('fr/'), 'em portugues',
           arruma_ancoras=True)

# Cada lingua tem navegacao e rodape proprios, com a fonte na sua inicial.
sincroniza('en/index.html', 'en/**/index.html', lambda p: False, 'em ingles')
sincroniza('fr/index.html', 'fr/**/index.html', lambda p: False, 'em frances')
