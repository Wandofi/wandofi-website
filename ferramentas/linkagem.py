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
 '/gestao-de-trafego/angola/':   'Anúncios em Angola',
 '/criacao-de-sites/apps-android-angola/': 'Apps Android em Angola',
 '/privacidade/':                'Política de Privacidade',
 '/termos/':                     'Termos de Utilização',
 '/automacoes/agentes-de-ia/':   'Agentes de IA à medida',
 '/blog/reconciliacao-bancaria-toconline/': 'Reconciliação bancária com o TOConline',
 '/blog/aparecer-nas-respostas-do-chatgpt/': 'Aparecer nas respostas do ChatGPT',
 '/blog/php2shell-dados-de-clientes/': 'PHP2Shell e os dados dos clientes',
 '/automacoes/':                 'Automações',
 '/automacoes/chatbot-whatsapp/': 'Chatbot de WhatsApp',
 '/blog/n8n-o-que-e-para-que-serve/': 'n8n: o que é e para que serve',
 '/casos/':                      'Casos',
 '/casos/#caso-reconciliacao':   'Caso: reconciliação bancária',
 '/sobre/':                      'Sobre',
 '/contactos/':                  'Contactos',
 '/diagnostico/':                'Teste de diagnóstico',
 '/blog/':                       'Blog',
 '/blog/google-preferred-sources/':          'Fonte preferida no Google',
 '/blog/agentes-de-ia-simples-grok-bot-muse-dots/': 'Grok Bot, Muse e Dots',
 '/blog/tendencias-de-ia-em-portugal/':      'Tendências de IA em Portugal',
 '/blog/agentes-de-ia-a-medida/':            'Agentes de IA à medida',
 '/blog/ai-act-ia-no-marketing/':            'IA no marketing e o AI Act',
 '/blog/como-abrir-uma-empresa-em-portugal/':'Como abrir uma empresa',
 '/en/':                         'SEO in English',
}

SECTORES = ['/seo/advogados/', '/seo/clinicas/', '/seo/contabilistas/',
            '/seo/imobiliarias/', '/seo/escolas-de-linguas/']

# Ligacoes a acrescentar ao bloco "related" de cada pagina.
# A ordem conta: o que estiver primeiro fica primeiro.
JUNTAR = {
 '/automacoes/agentes-de-ia/': ['/automacoes/', '/automacoes/chatbot-whatsapp/', '/blog/n8n-o-que-e-para-que-serve/', '/blog/agentes-de-ia-a-medida/', '/blog/reconciliacao-bancaria-toconline/', '/diagnostico/'],
 '/automacoes/chatbot-whatsapp/': ['/automacoes/', '/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/', '/diagnostico/'],
 '/seo/':                     ['/seo/consultor-seo/', '/seo/sectores/', '/seo/seo-tecnico/',
                               '/seo/seo-local/', '/seo/seo-para-empresas/', '/seo/geo-aeo/',
                               '/seo/agencia-seo-lisboa/', '/seo/agencia-seo-porto/',
                               '/blog/', '/diagnostico/'],
 '/seo/sectores/':            SECTORES + ['/diagnostico/'],
 '/seo/consultor-seo/':       ['/seo/sectores/', '/sobre/', '/diagnostico/'],
 '/seo/geo-aeo/':             ['/blog/aparecer-nas-respostas-do-chatgpt/', '/gestao-de-trafego/chatgpt-ads/', '/blog/google-preferred-sources/', '/blog/tendencias-de-ia-em-portugal/', '/diagnostico/'],
 '/seo/seo-tecnico/':         ['/blog/php2shell-dados-de-clientes/', '/seo/consultor-seo/', '/diagnostico/'],
 '/seo/seo-local/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/seo-para-empresas/':   ['/seo/sectores/', '/diagnostico/'],
 '/seo/agencia-seo-lisboa/':  ['/seo/consultor-seo/', '/diagnostico/'],
 '/seo/agencia-seo-porto/':   ['/seo/consultor-seo/', '/seo/', '/diagnostico/'],
 '/seo/advogados/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/clinicas/':            ['/seo/sectores/', '/diagnostico/'],
 '/seo/contabilistas/':       ['/seo/sectores/', '/blog/como-abrir-uma-empresa-em-portugal/', '/diagnostico/'],
 '/seo/imobiliarias/':        ['/seo/sectores/', '/diagnostico/'],
 '/seo/escolas-de-linguas/':  ['/seo/sectores/', '/diagnostico/'],
 '/criacao-de-sites/':        ['/criacao-de-sites/apps-android-angola/', '/seo/seo-local/', '/blog/php2shell-dados-de-clientes/', '/diagnostico/'],
 '/criacao-de-sites/sintra/': ['/diagnostico/'],
 '/criacao-de-sites/queluz/': ['/diagnostico/'],
 '/criacao-de-sites/marvila/':['/diagnostico/'],
 '/gestao-de-trafego/':       ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/blog/ai-act-ia-no-marketing/', '/diagnostico/'],
 '/gestao-de-trafego/google-ads/': ['/gestao-de-trafego/chatgpt-ads/', '/blog/ai-act-ia-no-marketing/', '/diagnostico/'],
 '/gestao-de-trafego/meta-ads/':   ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/diagnostico/'],
 '/gestao-de-trafego/angola/':     ['/gestao-de-trafego/meta-ads/', '/gestao-de-trafego/google-ads/', '/criacao-de-sites/apps-android-angola/', '/criacao-de-sites/', '/diagnostico/'],
 '/criacao-de-sites/apps-android-angola/': ['/gestao-de-trafego/angola/', '/criacao-de-sites/', '/automacoes/', '/diagnostico/'],
 '/gestao-de-trafego/chatgpt-ads/':['/seo/geo-aeo/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/gestao-de-trafego/', '/diagnostico/'],
 '/automacoes/':              ['/automacoes/chatbot-whatsapp/', '/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/', '/blog/reconciliacao-bancaria-toconline/', '/blog/agentes-de-ia-a-medida/', '/diagnostico/'],
 # O blog. Cada artigo leva artigos vizinhos e as paginas de servico do tema.
 '/blog/':                    ['/seo/consultor-seo/', '/automacoes/', '/diagnostico/'],
 '/blog/agentes-de-ia-simples-grok-bot-muse-dots/': ['/automacoes/', '/blog/agentes-de-ia-a-medida/', '/seo/geo-aeo/', '/diagnostico/'],
 '/blog/agentes-de-ia-a-medida/':            ['/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/ai-act-ia-no-marketing/':            ['/blog/tendencias-de-ia-em-portugal/', '/gestao-de-trafego/'],
 '/blog/aparecer-nas-respostas-do-chatgpt/': ['/blog/google-preferred-sources/'],
 '/blog/como-abrir-uma-empresa-em-portugal/':['/seo/contabilistas/', '/blog/reconciliacao-bancaria-toconline/'],
 '/blog/google-preferred-sources/':          ['/blog/aparecer-nas-respostas-do-chatgpt/', '/seo/consultor-seo/'],
 '/blog/n8n-o-que-e-para-que-serve/':        ['/blog/php2shell-dados-de-clientes/'],
 '/blog/php2shell-dados-de-clientes/':       ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/reconciliacao-bancaria-toconline/':  ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/tendencias-de-ia-em-portugal/':      ['/blog/agentes-de-ia-a-medida/'],
 '/casos/':                   ['/blog/reconciliacao-bancaria-toconline/', '/blog/', '/diagnostico/'],
 '/sobre/':                   ['/en/', '/diagnostico/'],
 '/contactos/':               ['/sobre/', '/en/', '/diagnostico/'],
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
        io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
    relat.append((u, len(atuais), len(final), final))

print(f"{len(relat)} paginas com a ligacao interna refeita\n")
for u, a, d, f in relat:
    print(f"  {u:34} {a} -> {d}")

# A lista "Outros artigos do blog" de cada artigo, refeita a partir do indice
# do blog. O indice ja esta por ordem, do mais recente para o mais antigo, e e
# a unica fonte do titulo e da data. Sem isto a lista envelhece sozinha: havia
# artigos de Agosto a mostrar vizinhos de Outubro e a ignorar os de Novembro.
#
# Cada artigo leva os MAIS seguintes na ordem do indice, a dar a volta no fim.
# Assim cada artigo aparece em exactamente MAIS listas. Uma lista so com os
# mais recentes daria 13 entradas aos novos e 3 aos antigos, que e o contrario
# do que uma ligacao interna deve fazer.
MAIS = 4

indice = io.open('blog/index.html', encoding='utf-8').read()
corpo = re.search(r'<main id="main".*?</main>', indice, re.S).group(0)
artigos = re.findall(r'<a class="post__link" href="(/blog/[^"]+/)".*?'
                     r'<time datetime="([\d-]+)">([^<]*)</time>.*?'
                     r'<h[23] class="post__title">(.*?)</h[23]>', corpo, re.S)

def vizinhos(atual):
    i = [a[0] for a in artigos].index(atual)
    janela = [artigos[(i + k) % len(artigos)] for k in range(1, MAIS + 1)]
    itens = ''.join(
        f'<li><a href="{u}"><time datetime="{iso}">{dia}</time>'
        f'<span class="t">{titulo}</span></a></li>'
        for u, iso, dia, titulo in janela)
    return f'<ul class="morelist">{itens}</ul>'

n = 0
for u, _, _, _ in artigos:
    p = caminho(u)
    h = io.open(p, encoding='utf-8').read()
    novo = re.sub(r'<ul class="morelist">.*?</ul>', lambda m: vizinhos(u), h,
                  count=1, flags=re.S)
    if novo != h:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(novo)
        n += 1

print(f"\n{len(artigos)} artigos no indice, {n} com a lista de vizinhos refeita")
