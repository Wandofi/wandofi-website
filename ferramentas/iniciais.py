# -*- coding: utf-8 -*-
"""Faz de /en/ e /fr/ a mesma pagina inicial que /, so que noutra lingua.

O PROBLEMA QUE ISTO RESOLVE
O Mauro carregou em EN na pagina inicial e caiu numa pagina que nao tinha nada
a ver. A razao: /en/ e /fr/ nunca foram traducoes da inicial. Foram feitas a
partir do molde das paginas internas de servico, com migalhas, bloco de
resposta, "Who this is for", perguntas frequentes e "Where to go from here".
Eram paginas de servico a fazer de inicial. Alem disso /en/ disputava
"SEO consultant in Lisbon" com /en/seo-consultant-lisbon/, que e a pagina
feita para esse termo: duas paginas a competir uma com a outra.

O QUE ESTE GERADOR FAZ
Troca o <main> de cada uma pelo <main> da inicial portuguesa, traduzido, e
leva atras o que faz a inicial ser a inicial: a classe no body, o bloco de
estilo proprio, e o guiao da vitrine, do titulo e do formulario. Nada mais.

O QUE NAO TOCA, DE PROPOSITO
A navegacao e o rodape de cada lingua ficam como estao. Ja estao escritos e,
mais importante, o ferramentas/sincroniza.py copia-os daqui para as sete
paginas irmas de cada lingua: mexer-lhes aqui mudava catorze paginas sem
ninguem pedir. O mesmo para o banner de cookies, a barra de baixo e o bloco
<style id="home-light">, que e o ferramentas/refresca_css.py que escreve.

E IDEMPOTENTE
Correr duas vezes da o mesmo resultado. Cada peca e procurada antes de ser
posta, e o <main> e sempre substituido por inteiro a partir do portugues, por
isso o portugues manda sempre e nunca ha duas versoes a conviver.

ORDEM
Correr sempre DEPOIS de mexer na inicial portuguesa e SEMPRE seguido do
ferramentas/linguas.py: o <main> que vem do portugues traz dentro o selector
de lingua da pagina portuguesa, e e o linguas.py que o poe a apontar para as
irmas certas. A ordem completa de uma sessao que mexa na inicial e:

    py ferramentas/refresca_css.py     # se mexeu em CSS
    py ferramentas/iniciais.py         # leva a inicial para ingles e frances
    py ferramentas/sincroniza.py       # se mexeu em nav ou rodape
    py ferramentas/linguas.py          # sempre a seguir aos dois de cima
    py ferramentas/auditoria.py        # sempre, antes de commit

AO MUDAR TEXTO DA INICIAL
A traducao vive no ferramentas/textos_iniciais.py, com a frase portuguesa
exacta como chave. Se a frase portuguesa mudar e a chave nao, o gerador avisa
no fim com "sem traducao" e diz qual e: nao falha em silencio.
"""
import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textos_iniciais as textos

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PT = os.path.join(REPO, 'index.html')
DESTINOS = {'en': os.path.join(REPO, 'en', 'index.html'),
            'fr': os.path.join(REPO, 'fr', 'index.html')}

fonte = io.open(PT, encoding='utf-8').read()
avisos = []


def conta(texto, marca):
    """Conta a marca como palavra inteira, nao como pedaco de outra.

    Isto nasceu de a propria prova desta ferramenta ter caido na armadilha.
    Para testar a conferencia da funcao montaVitrine, a prova renomeava-a para
    montaVitrineQueJaNaoEChamada. O nome novo comeca pelo antigo, por isso um
    count simples continuava a contar uma ocorrencia, a conferencia passava e
    a prova dizia que a rede nao funcionava quando o problema era a medicao.

    E a mesma lei de que uma marca so confere presenca se for unica, vista por
    outro lado: o texto tem de acabar onde a marca acaba. Quando a marca ja
    acaba num sinal que nao e letra, como { ou aspas, nao e preciso limite."""
    if marca[-1].isalnum() or marca[-1] == '_':
        return len(re.findall(re.escape(marca) + r'\b', texto))
    return texto.count(marca)


# ----------------------------------------------------------------- pecas da fonte
def entre(texto, abre, fecha, nome):
    i = texto.find(abre)
    if i < 0:
        raise SystemExit(f'nao encontrei {nome}')
    j = texto.index(fecha, i) + len(fecha)
    return texto[i:j]


def corta_main(texto):
    """Corta o <main>. Procura a abertura so depois do ultimo </style>, porque
    ha texto dentro dos blocos de estilo que se parece com a etiqueta."""
    fim_estilo = texto.rindex('</style>')
    m = re.search(r'<main\b[^>]*>', texto[fim_estilo:])
    if not m:
        raise SystemExit('nao encontrei a abertura do <main>')
    i = fim_estilo + m.start()
    j = texto.rindex('</main>') + len('</main>')
    return texto[i:j]


MAIN_PT = corta_main(fonte)
ESTILO_PAGINA = entre(fonte, '<style id="pagina">', '</style>', 'o <style id="pagina">')
GUIAO_PT = entre(fonte, '<!-- inicial cinzenta -->', '</script>', 'o guiao da inicial')

# Os comentarios do CSS ja escreveram a etiqueta por extenso e enganaram esta
# procura, que foi buscar um pedaco de comentario a meio do ficheiro em vez do
# bloco. O ingles e o frances ficaram sem o CSS da vitrine e do formulario, e
# nao houve erro nenhum: so uma pagina errada. Agora e conferido.
#
# As marcas sao escolhidas por aparecerem UMA so vez no bloco. A primeira
# versao desta conferencia procurava "body.inicial .vitrine{", que aparece
# duas vezes, a regra principal e a do telemovel: apagar a principal deixava a
# outra a tapar o buraco e a conferencia dizia que estava tudo bem. Foi uma
# prova a estragar o ficheiro de proposito que deu por isso, e e por isso que
# essa prova existe. Uma conferencia que nunca dispara nao e uma rede.
MARCAS_ESTILO = ('body.inicial .vitrine__inclina{', '@keyframes in-desliza',
                 'body.inicial .hero__quem{', 'body.inicial .cartao span{')
MINIMO_REGRAS = 30
for marca in MARCAS_ESTILO:
    n = conta(ESTILO_PAGINA, marca)
    if n != 1:
        raise SystemExit(f'o bloco de estilo da inicial tem "{marca}" {n} vezes em vez '
                         f'de uma: apanhei a coisa errada, {len(ESTILO_PAGINA)} bytes')
if ESTILO_PAGINA.count('body.inicial') < MINIMO_REGRAS:
    raise SystemExit(f'o bloco de estilo da inicial so tem '
                     f'{ESTILO_PAGINA.count("body.inicial")} regras body.inicial, '
                     f'menos do que as {MINIMO_REGRAS} que se esperam: '
                     f'apanhei a coisa errada, {len(ESTILO_PAGINA)} bytes')
if '<main' in MAIN_PT[10:]:
    raise SystemExit('o corte do <main> apanhou mais do que devia')
print(f'da fonte: main {len(MAIN_PT)} bytes, estilo {len(ESTILO_PAGINA)} bytes, '
      f'guiao {len(GUIAO_PT)} bytes\n')
LD_PT = re.search(r'<script type="application/ld\+json">(.*?)</script>', fonte, re.S).group(1)


# ----------------------------------------------------------------- traducao
def traduz_nos(html, dic, lingua):
    """Troca no de texto a no de texto, e so quando a frase inteira bate certo.

    Por frase inteira, nunca por pedaco: o "SEO" solto do formulario nao pode
    tocar no "SEO tecnico e consultoria" do cartao. O espaco a volta fica como
    estava, para a indentacao do ficheiro nao mudar."""
    naotraduzidas = []

    def troca(m):
        bruto = m.group(1)
        chave = re.sub(r'\s+', ' ', bruto).strip()
        if not chave or chave in textos.IGUAIS:
            return m.group(0)
        if chave in dic:
            esq = bruto[:len(bruto) - len(bruto.lstrip())]
            dir_ = bruto[len(bruto.rstrip()):]
            return '>' + esq + dic[chave] + dir_ + '<'
        if len(chave) > 2 and re.search(r'[a-zA-ZáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]{3}', chave):
            naotraduzidas.append(chave)
        return m.group(0)

    # fora dos guioes e dos desenhos: esses levam tratamento proprio
    partes = re.split(r'(<(?:script|svg)\b.*?</(?:script|svg)>)', html, flags=re.S | re.I)
    for k in range(0, len(partes), 2):
        partes[k] = re.sub(r'>([^<>]+)<', troca, partes[k])
    return ''.join(partes), naotraduzidas


def traduz_atributos(html, lingua):
    """Texto que o visitante le mas que vive num atributo, nao entre etiquetas.

    O traduz() so olha para o que esta entre > e <, por isso texto dentro de um
    atributo passava-lhe ao lado sem erro nenhum. Foi o que aconteceu as cotas
    dos tres passos do processo, o data-cota: a inicial inglesa e a francesa
    mostravam "30 min . videochamada" em portugues desde que foram geradas, e
    nada se queixou. Qualquer atributo novo que leve texto visivel tem de ser
    acrescentado aqui.
    """
    for pt, novo in textos.ATRIBUTOS[lingua].items():
        html = html.replace(f'placeholder="{pt}"', f'placeholder="{novo}"')
        html = html.replace(f'data-cota="{pt}"', f'data-cota="{novo}"')
    return html


def reaponta(html, lingua):
    """Reaponta as ligacoes internas para a pagina equivalente da lingua.

    O que nao tem equivalente fica a apontar para a pagina portuguesa e leva
    hreflang e lang, para o leitor saber que muda de lingua antes de carregar.
    E a mesma convencao que o rodape ingles ja usava."""
    mapa = textos.LIGACOES[lingua]

    def troca(m):
        attrs = m.group(1)
        u = re.search(r'href="([^"]*)"', attrs)
        if not u:
            return m.group(0)
        destino = u.group(1)
        if destino in mapa:
            attrs = attrs.replace(f'href="{destino}"', f'href="{mapa[destino]}"', 1)
            destino = mapa[destino]
        if destino in textos.EM_PORTUGUES and 'hreflang=' not in attrs:
            attrs = attrs.replace(f'href="{destino}"',
                                  f'href="{destino}" hreflang="pt-PT" lang="pt-PT"', 1)
        return '<a' + attrs + '>'

    return re.sub(r'<a\b([^>]*)>', troca, html)


def traduz_guiao(guiao, lingua):
    for pt, novo in textos.GUIAO[lingua].items():
        if pt not in guiao:
            avisos.append(f'{lingua}: a frase do guiao "{pt[:40]}" nao estava la')
        guiao = guiao.replace(pt, novo)
    # O guiao inteiro esta atras desta condicao. Se uma troca lhe tocar, nada
    # corre e a vitrine fica vazia sem erro nenhum na consola: foi o que
    # aconteceu quando a troca do campo origem apanhou tambem esta linha.
    if 'classList.contains("inicial")' not in guiao:
        raise SystemExit(f'{lingua}: a traducao estragou a condicao que liga o guiao')

    # Estas marcas sao as DEFINICOES, nao os nomes soltos, e sao exigidas uma e
    # uma so vez. A primeira versao procurava "montaVitrine" e "URL_FOLHA" por
    # presenca: aparecem 4 e 3 vezes, entre definicao e usos, por isso apagar a
    # definicao deixava os usos a tapar o buraco e a conferencia passava com o
    # guiao ja partido. E a mesma lei que apanhou a regra da vitrine pela media
    # query: uma marca so confere presenca se for unica, e nada garante que
    # continue unica. Exigir exactamente uma avisa no dia em que deixar de ser.
    MARCAS_GUIAO = ('function montaVitrine', 'var URL_FOLHA', '"formulario_inicial"',
                    'function parteTitulo', 'function formulario', 'empresa_web.value')
    for marca in MARCAS_GUIAO:
        n = conta(guiao, marca)
        if n != 1:
            raise SystemExit(f'{lingua}: o guiao tem "{marca}" {n} vezes em vez de uma')
    # E um piso, para apanhar o que nenhuma marca cobre. Hoje sao 26.
    if guiao.count('function ') < 18:
        raise SystemExit(f'{lingua}: o guiao so tem {guiao.count("function ")} funcoes, '
                         f'menos do que as 18 que se esperam: perdeu-se alguma coisa')
    return guiao


def traduz_ld(lingua):
    """Reescreve os dados estruturados na lingua, a partir do bloco portugues.

    Percorre o JSON e troca qualquer texto que esteja no dicionario. As
    perguntas frequentes sao exactamente as frases que ja foram traduzidas no
    <main>, por isso saem iguais ao que a pagina mostra, que e a condicao para
    o schema ser valido."""
    cab = textos.CABECA[lingua]
    dic = textos.EN if lingua == 'en' else textos.FR
    dados = json.loads(LD_PT)

    def anda(o):
        if isinstance(o, dict):
            return {k: anda(v) for k, v in o.items()}
        if isinstance(o, list):
            return [anda(v) for v in o]
        if isinstance(o, str):
            if o in dic:
                return dic[o]
            if o == 'https://wandofi.pt/':
                return cab['canonical']
            return o
        return o

    dados = anda(dados)
    for no in dados['@graph']:
        if no.get('@type') == 'Person' and 'jobTitle' in no:
            no['jobTitle'] = cab['jobTitle']
            no['knowsAbout'] = cab['knowsAbout']
        if no.get('@type') == 'ProfessionalService':
            no['description'] = cab['ld_description']
            no['serviceType'] = cab['serviceType']
    return json.dumps(dados, ensure_ascii=False)


# ----------------------------------------------------------------- cabeca
def arruma_cabeca(h, lingua):
    cab = textos.CABECA[lingua]
    outras = {'en': ('fr', 'https://wandofi.pt/fr/'), 'fr': ('en', 'https://wandofi.pt/en/')}
    passos = []

    def poe(padrao, novo, nome):
        nonlocal h
        h, n = re.subn(padrao, lambda _m: novo, h, count=1)
        passos.append(('ok   ' if n else 'FALTA', nome))

    poe(r'<html lang="[^"]*">', f'<html lang="{cab["lang"]}">', 'lang do html')
    poe(r'<title>.*?</title>', f'<title>{cab["title"]}</title>', 'title')
    poe(r'<meta name="description" content="[^"]*" />',
        f'<meta name="description" content="{cab["description"]}" />', 'description')
    poe(r'<link rel="canonical" href="[^"]*" />',
        f'<link rel="canonical" href="{cab["canonical"]}" />', 'canonical')
    poe(r'<meta property="og:url" content="[^"]*" />',
        f'<meta property="og:url" content="{cab["canonical"]}" />', 'og:url')
    poe(r'<meta property="og:title" content="[^"]*" />',
        f'<meta property="og:title" content="{cab["title"]}" />', 'og:title')
    poe(r'<meta property="og:description" content="[^"]*" />',
        f'<meta property="og:description" content="{cab["og_description"]}" />', 'og:description')
    poe(r'<meta property="og:locale" content="[^"]*" />',
        f'<meta property="og:locale" content="{cab["locale"]}" />', 'og:locale')
    poe(r'<meta name="twitter:title" content="[^"]*" />',
        f'<meta name="twitter:title" content="{cab["title"]}" />', 'twitter:title')
    poe(r'<meta name="twitter:description" content="[^"]*" />',
        f'<meta name="twitter:description" content="{cab["og_description"]}" />', 'twitter:description')

    # hreflang reciproco: cada lingua aponta para as outras duas e para si
    outra_cod, outra_url = outras[lingua]
    alt = (f'    <link rel="alternate" hreflang="pt-PT" href="https://wandofi.pt/" />\n'
           f'    <link rel="alternate" hreflang="{cab["lang"]}" href="{cab["canonical"]}" />\n'
           f'    <link rel="alternate" hreflang="{outra_cod}" href="{outra_url}" />\n'
           f'    <link rel="alternate" hreflang="x-default" href="https://wandofi.pt/" />\n')
    h, n = re.subn(r'(?:[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*" />\n)+',
                   lambda _m: alt, h, count=1)
    passos.append(('ok   ' if n else 'FALTA', 'hreflang reciproco'))

    # dados estruturados
    h, n = re.subn(r'(<script type="application/ld\+json">)(.*?)(</script>)',
                   lambda m: m.group(1) + traduz_ld(lingua) + m.group(3), h, count=1, flags=re.S)
    passos.append(('ok   ' if n else 'FALTA', 'dados estruturados'))

    # a bandeira que esconde o titulo ate haver decisao sobre a entrada
    if 'in-js' not in h:
        h, n = re.subn(r"(window\.wandofiConsent=v;)",
                       lambda m: m.group(1) + "\n        document.documentElement.classList.add('in-js');",
                       h, count=1)
        passos.append(('ok   ' if n else 'FALTA', 'bandeira in-js'))
    else:
        passos.append(('ja la', 'bandeira in-js'))

    return h, passos


# ----------------------------------------------------------------- corpo
def arruma_corpo(h, lingua):
    passos = []
    dic = textos.EN if lingua == 'en' else textos.FR

    # 1. a classe que liga tudo o que e proprio da inicial
    if 'class="inicial"' in h:
        passos.append(('ja la', 'classe inicial no body'))
    else:
        h, n = re.subn(r'<body([^>]*)>', lambda m: (
            f'<body class="inicial"{m.group(1)}>' if 'class=' not in m.group(1)
            else re.sub(r'class="([^"]*)"', r'class="\1 inicial"', m.group(0))), h, count=1)
        passos.append(('ok   ' if n else 'FALTA', 'classe inicial no body'))

    # 2. o <main> inteiro, vindo do portugues e traduzido
    novo_main, faltam = traduz_nos(MAIN_PT, dic, lingua)
    novo_main = traduz_atributos(novo_main, lingua)
    novo_main = reaponta(novo_main, lingua)
    if faltam:
        for f in dict.fromkeys(faltam):
            avisos.append(f'{lingua}: sem traducao -> "{f[:70]}"')
    i = h.rindex('</style>')
    m = re.search(r'<main\b[^>]*>', h[i:])
    if not m:
        raise SystemExit(f'{lingua}: nao encontrei o <main> de destino')
    ini = i + m.start()
    fim = h.rindex('</main>') + len('</main>')
    h = h[:ini] + novo_main + h[fim:]
    passos.append(('ok   ', f'<main> trocado, {len(novo_main)} bytes'))

    # 3. o bloco de estilo proprio da inicial, logo a seguir ao home-light
    if '<style id="pagina">' in h:
        h = re.sub(r'<style id="pagina">.*?</style>', lambda _m: ESTILO_PAGINA, h, count=1, flags=re.S)
        passos.append(('refeito', '<style id="pagina">'))
    else:
        h, n = re.subn(r'(<style id="home-light">.*?</style>)',
                       lambda m: m.group(1) + '\n    ' + ESTILO_PAGINA, h, count=1, flags=re.S)
        passos.append(('ok   ' if n else 'FALTA', '<style id="pagina">'))

    # 4. o guiao da vitrine, do titulo e do formulario, logo a seguir ao </main>
    guiao = traduz_guiao(GUIAO_PT, lingua)
    if '<!-- inicial cinzenta -->' in h:
        h = re.sub(r'<!-- inicial cinzenta -->.*?</script>', lambda _m: guiao, h, count=1, flags=re.S)
        passos.append(('refeito', 'guiao da inicial'))
    else:
        h = h.replace('</main>', '</main>\n    ' + guiao, 1)
        passos.append(('ok   ', 'guiao da inicial'))

    return h, passos


# ----------------------------------------------------------------- correr
for lingua, caminho in DESTINOS.items():
    print(f'=========== {lingua.upper()}  {caminho}')
    h = io.open(caminho, encoding='utf-8').read()
    antes = len(h)
    h, p1 = arruma_cabeca(h, lingua)
    h, p2 = arruma_corpo(h, lingua)
    for marca, nome in p1 + p2:
        print(f'  {marca:8} {nome}')
    io.open(caminho, 'w', encoding='utf-8', newline='\n').write(h)
    print(f'  gravado: {antes} -> {len(h)} bytes\n')

# O linkagem.py reescreve o bloco <div class="related"> das paginas que estao
# no JUNTAR dele, com texto de ancora fixo e em portugues. Hoje nao toca em
# nenhuma pagina de en/ nem de fr/, e as tres iniciais nem sequer tem esse
# bloco, por isso nao ha choque. Mas se alguem acrescentar uma pagina de outra
# lingua ao JUNTAR, as duas ferramentas passam a escrever no mesmo sitio e uma
# desfaz a outra a cada corrida: a pagina aparece sempre suja no git e ninguem
# percebe porque. Fica aqui a dar o aviso antes de isso acontecer.
_linkagem = os.path.join(REPO, 'ferramentas', 'linkagem.py')
if os.path.isfile(_linkagem):
    _fonte = io.open(_linkagem, encoding='utf-8').read()
    _juntar = re.search(r'JUNTAR\s*=\s*\{(.*?)\n\}', _fonte, re.S)
    if _juntar:
        _chaves = re.findall(r"^\s*'(/[^']*)'\s*:", _juntar.group(1), re.M)
        _outras = [c for c in _chaves if c.startswith(('/en/', '/fr/'))]
        if _outras:
            avisos.append('o linkagem.py passou a escrever em ' + ', '.join(_outras)
                          + ': confere os textos de ancora contra o ANCORA, senao as '
                            'duas ferramentas desfazem-se uma a outra')

if avisos:
    print('=========== AVISOS')
    for a in dict.fromkeys(avisos):
        print('  ' + a)
    print(f'\ntotal: {len(set(avisos))}')
else:
    print('sem avisos: todas as pecas tinham traducao')
