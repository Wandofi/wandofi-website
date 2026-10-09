# -*- coding: utf-8 -*-
"""Organiza a ligacao interna do site da Wandofi."""
import io, os, re, os, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

# Texto canonico de cada ligacao. Uma pagina, uma ancora, sempre igual.
ANCORA = {
 '/seo/':                        'SEO',
 '/seo/consultor-seo/':          'Consultor de SEO',
 '/seo/seo-tecnico/':            'SEO técnico',
 '/seo/seo-local/':              'SEO local',
 '/seo/seo-para-empresas/':      'SEO para empresas',
 '/seo/geo-aeo/':                'GEO e AEO',
 '/seo/agencia-seo-lisboa/':     'SEO em Lisboa',
 '/seo/agencia-seo-porto/':      'SEO no Porto',
 '/seo/sectores/':               'SEO por sector',
 '/seo/advogados/':              'SEO para advogados',
 '/seo/clinicas/':               'SEO para clínicas',
 '/seo/contabilistas/':          'SEO para contabilistas',
 '/seo/imobiliarias/':           'SEO para imobiliárias',
 '/seo/escolas-de-linguas/':     'SEO para escolas de línguas',
 '/criacao-de-sites/':           'Criação de sites',
 '/criacao-de-sites/sintra/':    'Sites em Sintra',
 '/criacao-de-sites/queluz/':    'Sites em Queluz',
 '/criacao-de-sites/marvila/':   'Sites em Marvila',
 '/gestao-de-trafego/':          'Gestão de tráfego',
 '/gestao-de-trafego/google-ads/':'Google Ads',
 '/gestao-de-trafego/meta-ads/': 'Meta Ads',
 '/gestao-de-trafego/chatgpt-ads/':'Anúncios no ChatGPT',
 '/automacoes/':                 'Automações',
 '/casos/':                      'Casos',
 '/sobre/':                      'Sobre',
 '/contactos/':                  'Contactos',
 '/diagnostico/':                'Teste de diagnóstico',
 '/blog/':                       'Blog',
 '/blog/google-preferred-sources/':          'Fonte preferida no Google',
 '/blog/tendencias-de-ia-em-portugal/':      'Tendências de IA em Portugal',
 '/blog/agentes-de-ia-a-medida/':            'Agentes de IA à medida',
 '/blog/ai-act-ia-no-marketing/':            'IA no marketing e o AI Act',
 '/blog/como-abrir-uma-empresa-em-portugal/':'Como abrir uma empresa',
}

SECTORES = ['/seo/advogados/', '/seo/clinicas/', '/seo/contabilistas/',
            '/seo/imobiliarias/', '/seo/escolas-de-linguas/']

# Ligacoes a acrescentar ao bloco "related" de cada pagina.
# A ordem conta: o que estiver primeiro fica primeiro.
JUNTAR = {
 '/seo/':                     ['/seo/consultor-seo/', '/seo/sectores/', '/seo/seo-tecnico/',
                               '/seo/seo-local/', '/seo/seo-para-empresas/', '/seo/geo-aeo/',
                               '/seo/agencia-seo-lisboa/', '/seo/agencia-seo-porto/',
                               '/blog/', '/diagnostico/'],
 '/seo/sectores/':            SECTORES + ['/diagnostico/'],
 '/seo/consultor-seo/':       ['/seo/sectores/', '/sobre/', '/diagnostico/'],
 '/seo/geo-aeo/':             ['/gestao-de-trafego/chatgpt-ads/', '/blog/google-preferred-sources/', '/blog/tendencias-de-ia-em-portugal/', '/diagnostico/'],
 '/seo/seo-tecnico/':         ['/seo/consultor-seo/', '/diagnostico/'],
 '/seo/seo-local/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/seo-para-empresas/':   ['/seo/sectores/', '/diagnostico/'],
 '/seo/agencia-seo-lisboa/':  ['/seo/consultor-seo/', '/diagnostico/'],
 '/seo/agencia-seo-porto/':   ['/seo/consultor-seo/', '/seo/', '/diagnostico/'],
 '/seo/advogados/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/clinicas/':            ['/seo/sectores/', '/diagnostico/'],
 '/seo/contabilistas/':       ['/seo/sectores/', '/blog/como-abrir-uma-empresa-em-portugal/', '/diagnostico/'],
 '/seo/imobiliarias/':        ['/seo/sectores/', '/diagnostico/'],
 '/seo/escolas-de-linguas/':  ['/seo/sectores/', '/diagnostico/'],
 '/criacao-de-sites/':        ['/seo/seo-local/', '/diagnostico/'],
 '/criacao-de-sites/sintra/': ['/diagnostico/'],
 '/criacao-de-sites/queluz/': ['/diagnostico/'],
 '/criacao-de-sites/marvila/':['/diagnostico/'],
 '/gestao-de-trafego/':       ['/gestao-de-trafego/chatgpt-ads/', '/blog/ai-act-ia-no-marketing/', '/diagnostico/'],
 '/gestao-de-trafego/google-ads/': ['/gestao-de-trafego/chatgpt-ads/', '/diagnostico/'],
 '/gestao-de-trafego/meta-ads/':   ['/gestao-de-trafego/chatgpt-ads/', '/diagnostico/'],
 '/gestao-de-trafego/chatgpt-ads/':['/seo/geo-aeo/', '/gestao-de-trafego/', '/diagnostico/'],
 '/automacoes/':              ['/blog/agentes-de-ia-a-medida/', '/sobre/', '/diagnostico/'],
 '/casos/':                   ['/diagnostico/'],
 '/sobre/':                   ['/diagnostico/'],
 '/contactos/':               ['/sobre/', '/diagnostico/'],
 '/diagnostico/':             ['/seo/', '/criacao-de-sites/', '/automacoes/', '/casos/'],
}

MAX = 6
# O hub do SEO e um indice: leva o conjunto todo, sem tecto de 6.
TECTO = {'/seo/': 10}

def caminho(u):
    return 'index.html' if u == '/' else u.strip('/') + '/index.html'

def bloco(ligacoes):
    itens = ''.join(f'<a href="{u}">{ANCORA[u]}</a>' for u in ligacoes)
    return f'<div class="related">{itens}</div>'

relat = []
for u, juntar in sorted(JUNTAR.items()):
    p = caminho(u)
    h = io.open(p, encoding='utf-8').read()
    antes = h

    blocos = list(re.finditer(r'<div class="related">(.*?)</div>', h, re.S))
    if blocos:
        alvo = blocos[-1]
        atuais = re.findall(r'href="([^"]+)"', alvo.group(1))
    else:
        alvo, atuais = None, []

    final = []
    for x in atuais + juntar:
        if x == u or x in final or x not in ANCORA:
            continue
        final.append(x)
    final = final[:TECTO.get(u, MAX)]

    novo = bloco(final)
    if alvo:
        h = h[:alvo.start()] + novo + h[alvo.end():]
    else:
        # sem bloco: colocar antes do CTA final, ou antes de fechar o main
        marca = '<section class="section cta final"'
        if marca in h:
            h = h.replace(marca,
                '<section class="section"><div class="container">'
                '<header class="section__head"><p class="eyebrow">A seguir</p>'
                '<h2 class="h2">Onde ir a partir daqui</h2></header>'
                + novo + '</div></section>\n' + marca, 1)
        else:
            h = h.replace('    </main>',
                '      <section class="section"><div class="container">'
                '<header class="section__head"><p class="eyebrow">A seguir</p>'
                '<h2 class="h2">Onde ir a partir daqui</h2></header>'
                + novo + '</div></section>\n    </main>', 1)

    if h != antes:
        io.open(p, 'w', encoding='utf-8').write(h)
    relat.append((u, len(atuais), len(final), final))

print(f"{len(relat)} paginas com a ligacao interna refeita\n")
for u, a, d, f in relat:
    print(f"  {u:34} {a} -> {d}")
