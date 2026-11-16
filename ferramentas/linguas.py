# -*- coding: utf-8 -*-
"""Poe cada botao de lingua a apontar para a pagina equivalente, e o hreflang
a dizer a verdade. Correr sempre DEPOIS do sincroniza.py.

O QUE ISTO VEIO CORRIGIR
Todos os botoes EN e FR do site apontavam para /en/ e /fr/, fosse qual fosse a
pagina. De /seo/contabilistas/ carregava-se em EN e caia-se na inicial
inglesa; de la, o PT trazia para a inicial portuguesa, e nao para onde se
estava. A ida e volta nunca fechava: eram 126 casos.

Pior, cada pagina declarava <link rel="alternate" hreflang="en"> para /en/
mesmo quando /en/ nao era traducao nenhuma dela. Dizer a um motor de busca que
duas paginas sao a mesma coisa noutra lingua, quando nao sao, e dizer-lhe uma
coisa falsa sobre o site inteiro.

COMO FUNCIONA
Ha grupos de paginas que sao mesmo a mesma coisa em linguas diferentes, e
estao na lista GRUPOS aqui em baixo. Dentro de um grupo, cada botao leva a
irma e a pagina declara os alternate. Fora dos grupos, que e a maior parte do
site (artigos do blog, paginas de sector, paginas legais), os botoes levam a
inicial da lingua, que e o unico destino honesto, e a pagina nao declara
alternate nenhum, porque nao tem traducao.

AO ACRESCENTAR UMA PAGINA TRADUZIDA
Acrescentar uma linha ao GRUPOS e correr isto. Mais nada.
"""
import glob, io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cada grupo diz o que existe em cada lingua. None quando ainda nao ha.
GRUPOS = [
    {'pt': '/',                    'en': '/en/',                        'fr': '/fr/'},
    {'pt': '/seo/',                'en': '/en/seo-consultant-lisbon/',  'fr': '/fr/seo/'},
    {'pt': '/criacao-de-sites/',   'en': '/en/websites/',               'fr': '/fr/sites-web/'},
    {'pt': '/automacoes/',         'en': '/en/automation/',             'fr': '/fr/automatisation/'},
    {'pt': '/casos/',              'en': '/en/case-studies/',           'fr': '/fr/references/'},
    {'pt': '/sobre/',              'en': '/en/about/',                  'fr': '/fr/a-propos/'},
    {'pt': '/gestao-de-trafego/',  'en': None,                          'fr': '/fr/publicite-en-ligne/'},
]
CASA = {'pt': '/', 'en': '/en/', 'fr': '/fr/'}
ROTULO = {'pt': ('PT', 'pt-PT', 'Português'),
          'en': ('EN', 'en', 'English'),
          'fr': ('FR', 'fr', 'Français')}


def endereco(caminho):
    d = os.path.dirname(caminho.replace(os.sep, '/'))
    return '/' + (d + '/' if d else '')


def lingua_de(url):
    if url.startswith('/en/'):
        return 'en'
    if url.startswith('/fr/'):
        return 'fr'
    return 'pt'


def grupo_de(url):
    for g in GRUPOS:
        if url in g.values():
            return g
    return None


def selector(aqui, grupo):
    """Os tres botoes. O da lingua em uso fica marcado e sem ligacao: dizer
    para onde se vai nao chega, tem de se ver tambem onde se esta."""
    minha = lingua_de(aqui)
    pecas = []
    for codigo in ('pt', 'en', 'fr'):
        sigla, hl, nome = ROTULO[codigo]
        if codigo == minha:
            pecas.append(f'<span aria-current="true" lang="{hl}">{sigla}</span>')
            continue
        destino = (grupo or {}).get(codigo) or CASA[codigo]
        pecas.append(f'<a href="{destino}" hreflang="{hl}" lang="{hl}" title="{nome}">{sigla}</a>')
    return ('<span class="idiomas" role="group" aria-label="Idioma">'
            + ''.join(pecas) + '<!--/idiomas--></span>')


def alternates(grupo):
    """Os <link rel="alternate">. So existem quando ha mesmo traducao."""
    if not grupo:
        return ''
    linhas = []
    for codigo, hl in (('pt', 'pt-PT'), ('en', 'en'), ('fr', 'fr')):
        if grupo.get(codigo):
            linhas.append(f'    <link rel="alternate" hreflang="{hl}" '
                          f'href="https://wandofi.pt{grupo[codigo]}" />\n')
    linhas.append('    <link rel="alternate" hreflang="x-default" '
                  f'href="https://wandofi.pt{grupo["pt"] or "/"}" />\n')
    return ''.join(linhas)


def paginas():
    for p in sorted(glob.glob('**/index.html', recursive=True)):
        p = p.replace(os.sep, '/')
        if not p.startswith('propostas/'):
            yield p


def principal():
    os.chdir(BASE)
    mexidas = com = sem = 0
    for p in paginas():
        aqui = endereco(p)
        grupo = grupo_de(aqui)
        h = io.open(p, encoding='utf-8').read()
        antes = h

        h, n = re.subn(r'<span class="idiomas".*?<!--/idiomas--></span>',
                       lambda _m: selector(aqui, grupo), h, flags=re.S)
        if not n:
            print(f'   {p}: AVISO, esta pagina nao tem selector de lingua')

        alt = alternates(grupo)
        h, k = re.subn(r'(?:[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n)+',
                       lambda _m: alt, h, count=1)
        if alt and not k:
            h, k = re.subn(r'(<link rel="canonical" href="[^"]*" />\n)',
                           lambda m: m.group(1) + alt, h, count=1)
            if not k:
                print(f'   {p}: AVISO, nao achei onde por os alternate')

        if h != antes:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
            mexidas += 1
        if grupo:
            com += 1
        else:
            sem += 1

    print(f'selectores de lingua: {mexidas} paginas mexidas')
    print(f'  com traducao declarada: {com}')
    print(f'  sem traducao, botoes para a inicial da lingua: {sem}')


if __name__ == '__main__':
    principal()
