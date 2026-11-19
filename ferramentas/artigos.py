# -*- coding: utf-8 -*-
"""A que paginas de servico pertence cada artigo do blog.

PORQUE E QUE ISTO EXISTE

Ate 19 de Novembro de 2026 esta informacao estava espalhada pelo JUNTAR do
ferramentas/linkagem.py: cada pagina de servico listava os artigos dela. Para
saber onde um artigo aparecia era preciso ler a tabela toda, e para ligar um
artigo novo era preciso lembrar-se de ir a quatro ou cinco sitios diferentes.

Foi isso que deixou coisas por fazer sem ninguem reparar:

  - o /blog/criar-site-com-ia/ ficou com uma porta so de fora do blog, e foi o
    unico dos seis artigos de Novembro que o Google nao indexou;
  - o /blog/agentes-de-ia-simples-grok-bot-muse-dots/ aparecia nas paginas de
    automacoes sem estar declarado em lado nenhum, ou seja o site tinha uma
    ligacao que a configuracao nao conhecia.

Aqui e ao contrario: cada artigo diz a que servicos pertence, numa linha. O
linkagem.py le isto e poe as paginas de servico a apontar para os artigos
delas. Ha um sitio so a dizer cada coisa.

COMO SE ACRESCENTA UM ARTIGO

Escreve-se a linha aqui. Se faltar, o linkagem.py recusa correr e diz qual e:
um artigo que ninguem liga fica dependente do sitemap, e ja se viu o que isso
da. Para um artigo que de facto nao pertence a servico nenhum, escreve-se uma
lista vazia de proposito, e a ferramenta aceita sem se queixar.

A ESCOLHA E DE CONTEUDO, NAO DE SEO

Cada servico aqui e um sitio onde o leitor DAQUELA pagina quereria mesmo ler
AQUELE artigo. Uma ligacao que nao faz sentido ao leitor tambem nao faz ao
Google, e um bloco de relacionados cheio de enchimento e pior do que um bloco
curto.
"""

SERVICOS = {
    # --- automacoes ---------------------------------------------------------
    '/blog/agentes-de-ia-a-medida/':
        ['/automacoes/', '/automacoes/agentes-de-ia/', '/automacoes/chatbot-whatsapp/'],
    '/blog/agentes-de-ia-simples-grok-bot-muse-dots/':
        ['/automacoes/', '/automacoes/agentes-de-ia/'],
    '/blog/n8n-o-que-e-para-que-serve/':
        ['/automacoes/', '/automacoes/agentes-de-ia/', '/automacoes/chatbot-whatsapp/'],
    '/blog/reconciliacao-bancaria-toconline/':
        ['/automacoes/', '/automacoes/agentes-de-ia/', '/casos/', '/seo/contabilistas/'],

    # --- anuncios -----------------------------------------------------------
    '/blog/ai-act-ia-no-marketing/':
        ['/gestao-de-trafego/', '/gestao-de-trafego/google-ads/', '/gestao-de-trafego/meta-ads/'],

    # --- sites --------------------------------------------------------------
    '/blog/criar-site-com-ia/':
        ['/criacao-de-sites/', '/criacao-de-sites/marvila/', '/criacao-de-sites/queluz/',
         '/criacao-de-sites/sintra/'],
    '/blog/php2shell-dados-de-clientes/':
        ['/criacao-de-sites/', '/criacao-de-sites/apps-android-angola/', '/seo/seo-tecnico/'],
    '/blog/sites-e-ia-em-2027/':
        ['/criacao-de-sites/', '/seo/geo-aeo/', '/seo/seo-local/'],

    # --- SEO e respostas de IA ----------------------------------------------
    '/blog/aparecer-nas-respostas-do-chatgpt/':
        ['/gestao-de-trafego/chatgpt-ads/', '/seo/', '/seo/geo-aeo/'],
    '/blog/google-preferred-sources/':
        ['/seo/geo-aeo/', '/seo/seo-tecnico/'],
    '/blog/siglas-seo-marketing-digital/':
        ['/seo/', '/seo/seo-tecnico/'],
    '/blog/tendencias-de-ia-em-portugal/':
        ['/seo/geo-aeo/', '/seo/sectores/'],
    # o que mudou nas pesquisas mudou-as em todos os sectores
    '/blog/seo-ai-overviews-modo-ia-google/':
        ['/seo/advogados/', '/seo/clinicas/', '/seo/escolas-de-linguas/', '/seo/geo-aeo/',
         '/seo/imobiliarias/', '/seo/seo-local/'],
    # um core update mexe com quem trabalha SEO, seja onde for
    '/blog/google-core-update-novembro-2026/':
        ['/seo/', '/seo/agencia-seo-lisboa/', '/seo/agencia-seo-porto/', '/seo/consultor-seo/',
         '/seo/geo-aeo/', '/seo/seo-local/', '/seo/seo-para-empresas/', '/seo/seo-tecnico/'],

    # --- negocio ------------------------------------------------------------
    '/blog/como-abrir-uma-empresa-em-portugal/':
        ['/seo/contabilistas/', '/seo/seo-para-empresas/'],
    '/blog/lancar-um-negocio-em-2027/':
        ['/automacoes/', '/criacao-de-sites/', '/gestao-de-trafego/', '/seo/'],
}


def por_servico():
    """Vira o mapa: para cada pagina de servico, os artigos que lhe pertencem.

    A ordem dentro de cada servico e a de publicacao, do mais recente para o
    mais antigo, para o bloco de relacionados mostrar primeiro o que e novo.
    Isso decide-se aqui e nao no linkagem.py, para quem leia este ficheiro
    saber tudo o que ha para saber sobre esta ligacao.
    """
    import glob, io, os, re
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    datas = {}
    for p in glob.glob(os.path.join(base, 'blog', '*', 'index.html')):
        u = '/blog/' + os.path.basename(os.path.dirname(p)) + '/'
        m = re.search(r'"datePublished"\s*:\s*"([^"]+)"',
                      io.open(p, encoding='utf-8').read())
        datas[u] = m.group(1)[:10] if m else '0000-00-00'

    saida = {}
    for artigo in sorted(SERVICOS, key=lambda a: datas.get(a, ''), reverse=True):
        for servico in SERVICOS[artigo]:
            saida.setdefault(servico, []).append(artigo)
    return saida


def confere(artigos_no_disco, ancoras):
    """Diz o que esta por declarar e o que esta declarado a mais.

    Devolve uma lista de queixas, vazia quando esta tudo bem.
    """
    queixas = []
    for a in sorted(set(artigos_no_disco) - set(SERVICOS)):
        queixas.append(f'artigo sem servicos declarados no ferramentas/artigos.py: {a}')
    for a in sorted(set(SERVICOS) - set(artigos_no_disco)):
        queixas.append(f'declarado mas sem artigo no disco: {a}')
    for a, servs in sorted(SERVICOS.items()):
        for s in servs:
            if s not in ancoras:
                queixas.append(f'{a} aponta para {s}, que nao tem ancora')
    return queixas
