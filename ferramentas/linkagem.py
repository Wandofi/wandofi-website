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
 '/blog/seo-ai-overviews-modo-ia-google/':   'O SEO e as respostas de IA',
 '/blog/siglas-seo-marketing-digital/':      'Siglas de SEO e marketing',
 '/blog/google-core-update-novembro-2026/':  'Core update de Novembro de 2026',
 '/en/':                         'SEO in English',
}

SECTORES = ['/seo/advogados/', '/seo/clinicas/', '/seo/contabilistas/',
            '/seo/imobiliarias/', '/seo/escolas-de-linguas/']

# Ligacoes a acrescentar ao bloco "related" de cada pagina.
# A ordem conta: o que estiver primeiro fica primeiro.
JUNTAR = {
 '/automacoes/agentes-de-ia/': ['/automacoes/', '/automacoes/chatbot-whatsapp/', '/blog/n8n-o-que-e-para-que-serve/', '/blog/agentes-de-ia-a-medida/', '/blog/reconciliacao-bancaria-toconline/', '/diagnostico/'],
 '/automacoes/chatbot-whatsapp/': ['/automacoes/', '/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/', '/blog/agentes-de-ia-a-medida/', '/casos/', '/diagnostico/'],
 '/seo/':                     ['/seo/consultor-seo/', '/seo/sectores/', '/seo/seo-tecnico/',
                               '/seo/seo-local/', '/seo/seo-para-empresas/', '/seo/geo-aeo/',
                               '/seo/agencia-seo-lisboa/', '/seo/agencia-seo-porto/',
                               '/blog/google-core-update-novembro-2026/',
                               '/blog/', '/diagnostico/'],
 '/seo/sectores/':            SECTORES + ['/diagnostico/'],
 # O artigo do core update entra nas paginas de SEO todas. E noticia datada:
 # quando a actualizacao acabar, o valor desta ligacao cai e sai daqui.
 '/seo/consultor-seo/':       ['/seo/sectores/', '/blog/google-core-update-novembro-2026/', '/sobre/', '/diagnostico/'],
 '/seo/geo-aeo/':             ['/blog/seo-ai-overviews-modo-ia-google/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/gestao-de-trafego/chatgpt-ads/', '/blog/google-preferred-sources/', '/blog/tendencias-de-ia-em-portugal/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/seo/seo-tecnico/':         ['/blog/php2shell-dados-de-clientes/', '/seo/consultor-seo/', '/blog/siglas-seo-marketing-digital/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/seo/seo-local/':           ['/seo/sectores/', '/blog/seo-ai-overviews-modo-ia-google/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/seo/seo-para-empresas/':   ['/seo/sectores/', '/blog/como-abrir-uma-empresa-em-portugal/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/seo/agencia-seo-lisboa/':  ['/seo/consultor-seo/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/seo/agencia-seo-porto/':   ['/seo/consultor-seo/', '/seo/', '/diagnostico/'],
 '/seo/advogados/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/clinicas/':            ['/seo/sectores/', '/diagnostico/'],
 '/seo/contabilistas/':       ['/seo/sectores/', '/blog/como-abrir-uma-empresa-em-portugal/', '/diagnostico/'],
 '/seo/imobiliarias/':        ['/seo/sectores/', '/diagnostico/'],
 '/seo/escolas-de-linguas/':  ['/seo/sectores/', '/diagnostico/'],
 '/criacao-de-sites/':        ['/criacao-de-sites/apps-android-angola/', '/seo/seo-local/', '/blog/php2shell-dados-de-clientes/', '/diagnostico/'],
 # As tres paginas de bairro nao apontavam sequer para o servico de que sao
 # filhas: so umas para as outras e para o diagnostico. Quem chega por "sites
 # em Sintra" ficava sem caminho nenhum para a pagina que vende o servico.
 '/criacao-de-sites/sintra/': ['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/criacao-de-sites/queluz/': ['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/criacao-de-sites/marvila/':['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/gestao-de-trafego/':       ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/blog/ai-act-ia-no-marketing/', '/diagnostico/'],
 '/gestao-de-trafego/google-ads/': ['/gestao-de-trafego/chatgpt-ads/', '/blog/ai-act-ia-no-marketing/', '/diagnostico/'],
 '/gestao-de-trafego/meta-ads/':   ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/diagnostico/'],
 '/gestao-de-trafego/angola/':     ['/gestao-de-trafego/meta-ads/', '/gestao-de-trafego/google-ads/', '/criacao-de-sites/apps-android-angola/', '/criacao-de-sites/', '/diagnostico/'],
 '/criacao-de-sites/apps-android-angola/': ['/gestao-de-trafego/angola/', '/criacao-de-sites/', '/automacoes/', '/blog/php2shell-dados-de-clientes/', '/diagnostico/'],
 '/gestao-de-trafego/chatgpt-ads/':['/seo/geo-aeo/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/gestao-de-trafego/', '/diagnostico/'],
 '/automacoes/':              ['/automacoes/chatbot-whatsapp/', '/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/', '/blog/reconciliacao-bancaria-toconline/', '/blog/agentes-de-ia-a-medida/', '/diagnostico/'],
 # O blog. Cada artigo leva artigos vizinhos e as paginas de servico do tema.
 '/blog/':                    ['/blog/google-core-update-novembro-2026/', '/blog/siglas-seo-marketing-digital/', '/seo/consultor-seo/', '/automacoes/', '/diagnostico/'],
 '/blog/google-core-update-novembro-2026/':  ['/blog/seo-ai-overviews-modo-ia-google/', '/seo/consultor-seo/', '/seo/seo-tecnico/', '/blog/siglas-seo-marketing-digital/', '/seo/', '/diagnostico/'],
 '/blog/agentes-de-ia-simples-grok-bot-muse-dots/': ['/automacoes/', '/blog/agentes-de-ia-a-medida/', '/seo/geo-aeo/', '/diagnostico/'],
 '/blog/agentes-de-ia-a-medida/':            ['/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/ai-act-ia-no-marketing/':            ['/blog/tendencias-de-ia-em-portugal/', '/gestao-de-trafego/'],
 '/blog/aparecer-nas-respostas-do-chatgpt/': ['/blog/seo-ai-overviews-modo-ia-google/', '/blog/google-preferred-sources/', '/blog/google-core-update-novembro-2026/'],
 '/blog/seo-ai-overviews-modo-ia-google/':   ['/blog/siglas-seo-marketing-digital/', '/seo/geo-aeo/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/blog/google-preferred-sources/', '/seo/consultor-seo/', '/casos/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/blog/siglas-seo-marketing-digital/':      ['/blog/seo-ai-overviews-modo-ia-google/', '/seo/geo-aeo/', '/gestao-de-trafego/', '/blog/como-abrir-uma-empresa-em-portugal/', '/seo/consultor-seo/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/blog/como-abrir-uma-empresa-em-portugal/':['/seo/contabilistas/', '/blog/reconciliacao-bancaria-toconline/'],
 '/blog/google-preferred-sources/':          ['/blog/aparecer-nas-respostas-do-chatgpt/', '/seo/consultor-seo/', '/blog/google-core-update-novembro-2026/'],
 '/blog/n8n-o-que-e-para-que-serve/':        ['/blog/php2shell-dados-de-clientes/'],
 '/blog/php2shell-dados-de-clientes/':       ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/reconciliacao-bancaria-toconline/':  ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/tendencias-de-ia-em-portugal/':      ['/blog/agentes-de-ia-a-medida/'],
 '/casos/':                   ['/blog/reconciliacao-bancaria-toconline/', '/blog/', '/diagnostico/'],
 '/sobre/':                   ['/en/', '/casos/', '/diagnostico/'],
 '/contactos/':               ['/sobre/', '/en/', '/diagnostico/'],
 # Faltava aqui um dos quatro pilares: quem acaba o diagnostico via SEO,
 # sites e automacoes, e nao via a gestao de trafego nem o blog.
 '/diagnostico/':             ['/seo/', '/criacao-de-sites/', '/automacoes/', '/gestao-de-trafego/', '/casos/', '/blog/'],
}

MAX = 6
# Os indices levam o conjunto todo, sem tecto de 6. O /seo/sectores/ estava a
# cortar no sexto item e ficava sem as escolas de linguas, ou seja, o indice
# dos cinco sectores so mostrava quatro. Um indice que esconde um dos seus
# itens esta errado, nao e uma questao de gosto.
# As paginas abaixo levam 7 porque ja estavam no tecto e o artigo novo nao
# entrava: a fusao e "atuais + juntar", por isso uma pagina cheia ignora em
# silencio tudo o que se lhe acrescente. Subir o tecto acrescenta sem tirar
# nada, que e o contrario de trocar uma ligacao por outra.
#
# ATENCAO: esta lista cresce um pouco a cada artigo novo, e isso e sintoma.
# Ha duas decisoes por tomar, as duas do Mauro, e ambas mexem no site inteiro:
# subir o MAX de 6 para 7 em todas as paginas, ou dar prioridade ao JUNTAR
# sobre as ligacoes ja presentes, o que reordena os blocos de 40 paginas.
# Enquanto nao estiver decidido, cada excepcao fica escrita aqui.
#
# 11 de Novembro de 2026: o artigo do core update entrou e obrigou a mais seis
# excepcoes. Onze linhas de excepcao para um tecto de seis e a prova de que o
# tecto esta errado, nao de que as paginas sao especiais. MAX = 7 apagava esta
# tabela quase toda, e continua a ser decisao do Mauro.
TECTO = {'/seo/': 11,
         '/seo/sectores/': 8,
         '/seo/geo-aeo/': 8,
         '/seo/consultor-seo/': 7,
         '/seo/seo-tecnico/': 7,
         '/seo/seo-local/': 7,
         '/seo/seo-para-empresas/': 7,
         '/seo/agencia-seo-lisboa/': 7,
         '/blog/aparecer-nas-respostas-do-chatgpt/': 8,
         '/blog/seo-ai-overviews-modo-ia-google/': 8,
         '/blog/siglas-seo-marketing-digital/': 7,
         '/blog/google-preferred-sources/': 7,
         '/blog/': 8}

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
