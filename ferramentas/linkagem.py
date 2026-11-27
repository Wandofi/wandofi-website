# -*- coding: utf-8 -*-
"""Organiza a ligacao interna do site da Wandofi.

Quem manda nas ligacoes PARA artigos do blog e o ferramentas/artigos.py, onde
cada artigo diz a que paginas de servico pertence. Aqui ficam as ligacoes
entre paginas de servico e os indices. Sao dois ficheiros porque sao duas
decisoes diferentes: uma e de conteudo, a outra e de arrumacao do site.
"""
import io, os, re, os, glob

import artigos as mapa_artigos

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
 '/blog/mcp-execucao-de-codigo/': 'O MCP e a execução de código agêntica',
 '/blog/anuncios-chatgpt-google-ai-mode/': 'O novo mapa dos anúncios com IA',
 '/blog/business-hub-chatgpt/': 'Reclamar o negócio no ChatGPT',
 '/casos/':                      'Casos',
 '/casos/#caso-reconciliacao':   'Caso: reconciliação bancária',
 '/sobre/':                      'Sobre',
 '/contactos/':                  'Contactos',
 '/diagnostico/':                'Teste de diagnóstico',
 '/precos/':                     'Preços',
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
 '/blog/criar-site-com-ia/':                 'Criar um site com IA',
 '/blog/sites-e-ia-em-2027/':                'Sites e IA em 2027',
 '/blog/lancar-um-negocio-em-2027/':         'Lançar um negócio em 2027',
 '/en/':                         'SEO in English',
}

SECTORES = ['/seo/advogados/', '/seo/clinicas/', '/seo/contabilistas/',
            '/seo/imobiliarias/', '/seo/escolas-de-linguas/']

# Ligacoes a acrescentar ao bloco "related" de cada pagina.
# A ordem conta: o que estiver primeiro fica primeiro.
JUNTAR = {
 '/automacoes/agentes-de-ia/': ['/automacoes/', '/automacoes/chatbot-whatsapp/', '/diagnostico/'],
 '/automacoes/chatbot-whatsapp/': ['/automacoes/', '/automacoes/agentes-de-ia/', '/casos/', '/diagnostico/'],
 '/seo/':                     ['/seo/consultor-seo/', '/seo/sectores/', '/seo/seo-tecnico/',
                               '/seo/seo-local/', '/seo/seo-para-empresas/', '/seo/geo-aeo/',
                               '/seo/agencia-seo-lisboa/', '/seo/agencia-seo-porto/',
                               '/blog/', '/diagnostico/'],
 '/seo/sectores/':            SECTORES + ['/diagnostico/'],
 # O artigo do core update entra nas paginas de SEO todas. E noticia datada:
 # quando a actualizacao acabar, o valor desta ligacao cai e sai daqui.
 '/seo/consultor-seo/':       ['/seo/agencia-seo-lisboa/', '/seo/sectores/', '/sobre/', '/diagnostico/'],
 '/seo/geo-aeo/':             ['/gestao-de-trafego/chatgpt-ads/', '/diagnostico/'],
 '/seo/seo-tecnico/':         ['/seo/consultor-seo/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/seo/seo-local/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/seo-para-empresas/':   ['/seo/sectores/', '/diagnostico/'],
 '/seo/agencia-seo-lisboa/':  ['/seo/consultor-seo/', '/diagnostico/'],
 '/seo/agencia-seo-porto/':   ['/seo/consultor-seo/', '/seo/', '/diagnostico/'],
 '/seo/advogados/':           ['/seo/sectores/', '/diagnostico/'],
 '/seo/clinicas/':            ['/seo/sectores/', '/diagnostico/'],
 '/seo/contabilistas/':       ['/seo/sectores/', '/diagnostico/'],
 '/seo/imobiliarias/':        ['/seo/sectores/', '/diagnostico/'],
 '/seo/escolas-de-linguas/':  ['/seo/sectores/', '/diagnostico/'],
 # A criacao de sites nao tinha artigo nenhum no bloco. Os dois de 15 de
 # Novembro sao os primeiros escritos para quem compra um site.
 '/criacao-de-sites/':        ['/criacao-de-sites/apps-android-angola/', '/seo/seo-local/', '/diagnostico/'],
 # As tres paginas de bairro nao apontavam sequer para o servico de que sao
 # filhas: so umas para as outras e para o diagnostico. Quem chega por "sites
 # em Sintra" ficava sem caminho nenhum para a pagina que vende o servico.
 '/criacao-de-sites/sintra/': ['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/criacao-de-sites/queluz/': ['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/criacao-de-sites/marvila/':['/criacao-de-sites/', '/seo/seo-local/', '/seo/agencia-seo-lisboa/', '/diagnostico/'],
 '/gestao-de-trafego/':       ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/precos/', '/diagnostico/'],
 '/gestao-de-trafego/google-ads/': ['/gestao-de-trafego/chatgpt-ads/', '/diagnostico/'],
 '/gestao-de-trafego/meta-ads/':   ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/angola/', '/diagnostico/'],
 '/gestao-de-trafego/angola/':     ['/gestao-de-trafego/meta-ads/', '/gestao-de-trafego/google-ads/', '/criacao-de-sites/apps-android-angola/', '/criacao-de-sites/', '/diagnostico/'],
 '/criacao-de-sites/apps-android-angola/': ['/gestao-de-trafego/angola/', '/criacao-de-sites/', '/automacoes/', '/diagnostico/'],
 '/gestao-de-trafego/chatgpt-ads/':['/seo/geo-aeo/', '/gestao-de-trafego/', '/diagnostico/'],
 '/automacoes/':              ['/automacoes/chatbot-whatsapp/', '/automacoes/agentes-de-ia/', '/diagnostico/'],
 # O blog. Cada artigo leva artigos vizinhos e as paginas de servico do tema.
 '/blog/business-hub-chatgpt/': ['/seo/geo-aeo/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/seo/seo-local/', '/gestao-de-trafego/chatgpt-ads/', '/blog/anuncios-chatgpt-google-ai-mode/', '/diagnostico/'],
 '/blog/anuncios-chatgpt-google-ai-mode/': ['/gestao-de-trafego/chatgpt-ads/', '/gestao-de-trafego/', '/seo/geo-aeo/', '/criacao-de-sites/', '/blog/seo-ai-overviews-modo-ia-google/', '/blog/sites-e-ia-em-2027/', '/diagnostico/'],
 '/blog/':                    ['/blog/criar-site-com-ia/', '/blog/sites-e-ia-em-2027/', '/blog/google-core-update-novembro-2026/', '/blog/siglas-seo-marketing-digital/', '/seo/consultor-seo/', '/automacoes/', '/diagnostico/'],
 '/blog/google-core-update-novembro-2026/':  ['/blog/seo-ai-overviews-modo-ia-google/', '/seo/consultor-seo/', '/seo/seo-tecnico/', '/blog/siglas-seo-marketing-digital/', '/seo/', '/diagnostico/'],
 # Os dois de 15 de Novembro falam um com o outro: um e sobre como o site e
 # feito, o outro sobre quem o vai ler. Ambos levam a criacao de sites.
 '/blog/criar-site-com-ia/':  ['/criacao-de-sites/', '/blog/sites-e-ia-em-2027/', '/seo/seo-tecnico/', '/casos/', '/seo/consultor-seo/', '/diagnostico/'],
 '/blog/sites-e-ia-em-2027/': ['/seo/geo-aeo/', '/blog/criar-site-com-ia/', '/blog/seo-ai-overviews-modo-ia-google/', '/seo/seo-local/', '/criacao-de-sites/', '/diagnostico/'],
 '/blog/agentes-de-ia-simples-grok-bot-muse-dots/': ['/automacoes/', '/blog/agentes-de-ia-a-medida/', '/seo/geo-aeo/', '/diagnostico/'],
 '/blog/agentes-de-ia-a-medida/':            ['/automacoes/agentes-de-ia/', '/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/ai-act-ia-no-marketing/':            ['/blog/tendencias-de-ia-em-portugal/', '/gestao-de-trafego/'],
 '/blog/aparecer-nas-respostas-do-chatgpt/': ['/blog/business-hub-chatgpt/', '/blog/seo-ai-overviews-modo-ia-google/', '/blog/google-preferred-sources/', '/blog/google-core-update-novembro-2026/'],
 '/blog/seo-ai-overviews-modo-ia-google/':   ['/blog/siglas-seo-marketing-digital/', '/seo/geo-aeo/', '/blog/aparecer-nas-respostas-do-chatgpt/', '/blog/google-preferred-sources/', '/seo/consultor-seo/', '/casos/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/blog/siglas-seo-marketing-digital/':      ['/blog/seo-ai-overviews-modo-ia-google/', '/seo/geo-aeo/', '/gestao-de-trafego/', '/blog/como-abrir-uma-empresa-em-portugal/', '/seo/consultor-seo/', '/blog/google-core-update-novembro-2026/', '/diagnostico/'],
 '/blog/como-abrir-uma-empresa-em-portugal/':['/seo/contabilistas/', '/blog/lancar-um-negocio-em-2027/', '/blog/reconciliacao-bancaria-toconline/'],
 # O pilar do lancamento. Toca em todas as frentes, por isso entra nas quatro
 # paginas de servico e puxa para o artigo da burocracia, que e o passo um.
 '/blog/lancar-um-negocio-em-2027/': ['/criacao-de-sites/', '/seo/', '/gestao-de-trafego/', '/automacoes/', '/blog/como-abrir-uma-empresa-em-portugal/', '/diagnostico/'],
 '/blog/google-preferred-sources/':          ['/blog/aparecer-nas-respostas-do-chatgpt/', '/seo/consultor-seo/', '/blog/google-core-update-novembro-2026/'],
 '/blog/n8n-o-que-e-para-que-serve/':        ['/blog/php2shell-dados-de-clientes/'],
 '/blog/php2shell-dados-de-clientes/':       ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/reconciliacao-bancaria-toconline/':  ['/blog/n8n-o-que-e-para-que-serve/'],
 '/blog/tendencias-de-ia-em-portugal/':      ['/blog/agentes-de-ia-a-medida/'],
 '/precos/':                  ['/diagnostico/', '/seo/', '/criacao-de-sites/', '/automacoes/', '/casos/', '/sobre/'],
 '/casos/':                   ['/seo/agencia-seo-lisboa/', '/blog/', '/precos/', '/diagnostico/'],
 '/sobre/':                   ['/en/', '/casos/', '/precos/', '/diagnostico/'],
 '/contactos/':               ['/sobre/', '/en/', '/diagnostico/'],
 # Faltava aqui um dos quatro pilares: quem acaba o diagnostico via SEO,
 # sites e automacoes, e nao via a gestao de trafego nem o blog.
 '/diagnostico/':             ['/precos/', '/seo/', '/criacao-de-sites/', '/automacoes/', '/gestao-de-trafego/', '/casos/', '/blog/'],
}

# As ligacoes das paginas de servico para os artigos delas entram aqui,
# calculadas a partir do ferramentas/artigos.py. Vao a FRENTE do que estiver
# escrito a mao no JUNTAR: um artigo novo nao pode ficar de fora do bloco so
# porque a pagina ja tinha ligacoes antigas a ocupar o tecto, que foi
# exactamente o que aconteceu ao /blog/criar-site-com-ia/.
for _servico, _arts in mapa_artigos.por_servico().items():
    JUNTAR[_servico] = _arts + [x for x in JUNTAR.get(_servico, []) if x not in _arts]

# Um artigo que ninguem declare fica dependente do sitemap, e ja se viu o que
# isso da. Mais vale a ferramenta recusar correr do que publicar um site com um
# artigo esquecido.
_queixas = mapa_artigos.confere(
    ['/blog/' + os.path.basename(os.path.dirname(p)) + '/'
     for p in glob.glob('blog/*/index.html')],
    ANCORA)
if _queixas:
    import sys
    print('O mapa de artigos e servicos nao bate certo com o que esta no disco:')
    for q in _queixas:
        print('  ' + q)
    sys.exit('nada escrito')

MAX = 7
# Os indices levam o conjunto todo, sem tecto de 6. O /seo/sectores/ estava a
# cortar no sexto item e ficava sem as escolas de linguas, ou seja, o indice
# dos cinco sectores so mostrava quatro. Um indice que esconde um dos seus
# itens esta errado, nao e uma questao de gosto.
# As paginas abaixo levam mais do que o tecto normal porque sao indices ou
# paginas com muitos vizinhos legitimos. A fusao e "atuais + juntar" cortada no
# tecto, por isso uma pagina cheia ignora o que se lhe acrescente; desde
# 18/11/2026 a ferramenta queixa-se quando isso acontece, em vez de o fazer
# calada. Subir um tecto acrescenta sem tirar nada, que e o contrario de trocar
# uma ligacao por outra.
#
# 18 de Novembro de 2026: o Mauro decidiu subir o MAX de 6 para 7, e isso
# apagou dezassete linhas desta tabela de uma vez, que era o que a nota antiga
# previa. A outra decisao que estava em cima da mesa, dar prioridade ao JUNTAR
# sobre as ligacoes ja presentes, fica por tomar e deixou de ser urgente: a
# ferramenta passou a dizer quando uma ligacao nao cabe.
#
# 11 de Novembro de 2026: o artigo do core update entrou e obrigou a mais seis
# excepcoes. Onze linhas de excepcao para um tecto de seis e a prova de que o
# tecto esta errado, nao de que as paginas sao especiais. MAX = 7 apagava esta
# tabela quase toda, e continua a ser decisao do Mauro.
#
# 15 de Novembro de 2026: mais tres excepcoes, pelos dois artigos novos. A
# /criacao-de-sites/ nao tinha artigo nenhum no bloco e passa a ter dois.
TECTO = {'/seo/': 14,
'/casos/': 8,
'/automacoes/agentes-de-ia/': 8,
'/seo/agencia-seo-porto/': 8,
'/seo/contabilistas/': 8,
         '/seo/sectores/': 9,
         '/seo/geo-aeo/': 11,
         '/seo/consultor-seo/': 8,
         '/seo/seo-tecnico/': 9,
         '/seo/seo-local/': 8,
         '/criacao-de-sites/': 9,
         '/automacoes/': 11,
         '/gestao-de-trafego/': 8,
         # 26/11/2026: subiu de 7 para 8 para a pagina de servico mostrar o
         # artigo de analise do proprio canal, sem tirar nada do que la estava.
         '/gestao-de-trafego/chatgpt-ads/': 8,
         # 27/11/2026: o artigo do Business Hub e o guia de aparecer nas respostas
         # falam um do outro, e o GEO e AEO leva o artigo novo sem perder nenhum.
         '/blog/aparecer-nas-respostas-do-chatgpt/': 9,
         '/blog/business-hub-chatgpt/': 10,
         '/blog/seo-ai-overviews-modo-ia-google/': 8,
         '/blog/': 10}

def caminho(u):
    return 'index.html' if u == '/' else u.strip('/') + '/index.html'

def bloco(ligacoes):
    itens = ''.join(f'<a href="{u}">{ANCORA[u]}</a>' for u in ligacoes)
    return f'<div class="related">{itens}</div>'

relat = []
cortados = []
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

    # O que se pediu e nao coube. A fusao e "atuais + juntar" cortada no tecto,
    # por isso uma pagina cheia ignora tudo o que se lhe acrescente ao JUNTAR.
    # Ate 18/11/2026 ignorava EM SILENCIO, e isso ja tinha custado uma ligacao
    # a serio: o /gestao-de-trafego/chatgpt-ads/ tinha o artigo de aparecer nas
    # respostas do ChatGPT no JUNTAR desde sempre, e a pagina nunca o mostrou.
    # Quem olhasse para a configuracao via uma ligacao que nao existia.
    #
    # Nao da para decidir aqui se o tecto sobe: isso muda os blocos de dezenas
    # de paginas e e decisao do Mauro, e esta escrita na nota do TECTO. O que
    # da, e o que falta, e dizer. Uma ferramenta que engole o que lhe pedem sem
    # se queixar poe a configuracao a mentir sobre o site.
    for x in juntar:
        if x in ANCORA and x != u and x not in final:
            cortados.append((u, x))

    novo = bloco(final)
    if alvo:
        h = h[:alvo.start()] + novo + h[alvo.end():]
    else:
        # sem bloco: colocar antes do CTA final, ou antes de fechar o main
        marca = '<section class="section cta final"'
        if marca in h:
            h = h.replace(marca,
                '<section class="section"><div class="container">'
                '<header class="section__head">'
                '<h2 class="h2">Onde ir a partir daqui</h2></header>'
                + novo + '</div></section>\n' + marca, 1)
        else:
            h = h.replace('    </main>',
                '      <section class="section"><div class="container">'
                '<header class="section__head">'
                '<h2 class="h2">Onde ir a partir daqui</h2></header>'
                + novo + '</div></section>\n    </main>', 1)

    if h != antes:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(h)
    relat.append((u, len(atuais), len(final), final))

print(f"{len(relat)} paginas com a ligacao interna refeita\n")
for u, a, d, f in relat:
    print(f"  {u:34} {a} -> {d}")

if cortados:
    print(f"\nPEDIDAS NO JUNTAR E NAO MOSTRADAS: {len(cortados)}")
    print("  A pagina estava no tecto e o que ja la estava ganhou o lugar.")
    print("  Ou se sobe o tecto dessa pagina, ou se tira a ligacao do JUNTAR,")
    print("  senao a configuracao fica a dizer uma coisa e o site a mostrar outra.")
    for u, x in cortados:
        print(f"    {u:34} queria mostrar {x}")

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
