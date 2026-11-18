# -*- coding: utf-8 -*-
"""Escreve o /feed.xml a partir dos proprios artigos do blog.

PORQUE E QUE O SITE PRECISA DE UM

Nao havia nenhum. Com autoridade de dominio 4, a frescura e a unica alavanca
que funciona, e um feed e a maneira mais barata de dizer ao Google e aos
agregadores que saiu coisa nova, sem esperar que alguem volte a rastrear a
listagem do blog.

E ha um caso concreto a puxar por isto. A 18 de Novembro de 2026 o Search
Console dizia, sobre o artigo "Criar um site com IA":

    Deteccao, Sitemaps: https://wandofi.pt/sitemap.xml
    Pagina de referencia: Nenhuma pagina foi detectada
    Ultimo rastreamento: N/D

Ou seja, o Google soube do artigo so pelo sitemap, nunca viu ninguem a apontar
para ele, e nunca la foi. Os outros cinco artigos de Novembro foram indexados.
Este ficou a ser uma linha num ficheiro.

DE ONDE VEM O QUE ESTA NO FEED

Dos artigos, nao da listagem. A listagem e marcacao que muda de forma quando
alguem mexe no desenho; o <title>, a meta description e o datePublished dos
dados estruturados sao os mesmos campos que o Google le, e se divergirem do
feed o problema esta no artigo e nao aqui.

CORRER depois de publicar um artigo, antes do auditoria.py.
"""
import glob, io, os, re, sys
from email.utils import format_datetime
from datetime import datetime, timezone
from xml.sax.saxutils import escape

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

SITE = 'https://wandofi.pt'
TITULO = 'Wandofi PM, blog'
DESCRICAO = ('SEO, sites e automacoes para negocios em Portugal. '
             'Escrito por Mauro Cordeiro, consultor de projectos em Lisboa.')
QUANTOS = 20


def campo(texto, padrao):
    m = re.search(padrao, texto, re.S)
    return m.group(1).strip() if m else None


artigos = []
for p in sorted(glob.glob('blog/*/index.html')):
    t = io.open(p, encoding='utf-8').read()
    url = SITE + '/' + p.replace(os.sep, '/').replace('index.html', '')

    titulo = campo(t, r'<title>(.*?)</title>')
    descricao = campo(t, r'<meta name="description" content="([^"]*)"')
    data = campo(t, r'"datePublished"\s*:\s*"([^"]+)"')

    faltas = [n for n, v in (('title', titulo), ('description', descricao),
                             ('datePublished', data)) if not v]
    if faltas:
        print(f'  SALTADO {p}: sem {", ".join(faltas)}')
        continue

    # o titulo das paginas acaba sempre em " | Wandofi PM"; no feed isso e ruido
    titulo = titulo.split('|')[0].strip()

    try:
        d = datetime.fromisoformat(data.replace('Z', '+00:00'))
    except ValueError:
        print(f'  SALTADO {p}: data ilegivel "{data}"')
        continue
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)

    artigos.append({'url': url, 'titulo': titulo, 'descricao': descricao, 'data': d})

if not artigos:
    sys.exit('nao encontrei artigos: nada escrito')

artigos.sort(key=lambda a: a['data'], reverse=True)
artigos = artigos[:QUANTOS]

itens = []
for a in artigos:
    itens.append(
        '    <item>\n'
        f'      <title>{escape(a["titulo"])}</title>\n'
        f'      <link>{escape(a["url"])}</link>\n'
        f'      <guid isPermaLink="true">{escape(a["url"])}</guid>\n'
        f'      <pubDate>{format_datetime(a["data"])}</pubDate>\n'
        f'      <description>{escape(a["descricao"])}</description>\n'
        '    </item>')

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    '  <channel>\n'
    f'    <title>{escape(TITULO)}</title>\n'
    f'    <link>{SITE}/blog/</link>\n'
    f'    <description>{escape(DESCRICAO)}</description>\n'
    '    <language>pt-PT</language>\n'
    f'    <lastBuildDate>{format_datetime(artigos[0]["data"])}</lastBuildDate>\n'
    f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml" />\n'
    + '\n'.join(itens) + '\n'
    '  </channel>\n'
    '</rss>\n')

# Nao gravar sem saber que o que saiu e XML valido: um feed partido e pior do
# que nenhum, porque o agregador deixa de voltar.
from xml.etree import ElementTree
try:
    ElementTree.fromstring(xml)
except ElementTree.ParseError as e:
    sys.exit(f'o XML que saiu nao e valido, nada gravado: {e}')

io.open('feed.xml', 'w', encoding='utf-8', newline='\n').write(xml)
print(f'feed.xml escrito com {len(artigos)} artigos, o mais recente de '
      f'{artigos[0]["data"].date()}')

# A ligacao de descoberta, no <head> da listagem e da inicial. E por estas duas
# paginas que o Google passa mais vezes.
LIGACAO = ('<link rel="alternate" type="application/rss+xml" '
           f'title="{TITULO}" href="{SITE}/feed.xml" />')
postos = 0
for p in ('blog/index.html', 'index.html'):
    t = io.open(p, encoding='utf-8').read()
    if 'application/rss+xml' in t:
        continue
    m = re.search(r'<link rel="canonical"[^>]*/>', t)
    if not m:
        print(f'  {p}: sem canonico, nao soube onde por a ligacao do feed')
        continue
    indent = '\n    '
    t = t[:m.end()] + indent + LIGACAO + t[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
    postos += 1
print(f'ligacao do feed posta em {postos} paginas')
