# -*- coding: utf-8 -*-
"""Rotula as celulas dos quadros, para o telemovel os poder mostrar em cartoes.

A 390 px um quadro de quatro colunas nao cabe no ecra: desliza para o lado
dentro do .quadro-wrap e a ultima coluna, que costuma ser a mais util, nasce
fora do ecra. O CSS resolve isso empilhando cada linha como um cartao, mas para
o cartao se ler e preciso que cada valor leve o nome da sua coluna.

Este programa le o <thead> de cada quadro e escreve esse nome em data-r="" nas
celulas do corpo. Quadros com tres ou mais colunas recebem tambem a classe
quadro--cartoes, que e o que o CSS procura. Quadros de duas colunas ficam como
estao, porque esses cabem no ecra.

Correr da raiz do repositorio, sempre que se acrescentar ou alterar um quadro.
E idempotente: correr duas vezes da o mesmo resultado.
"""
import io, os, re, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

MIN_COLUNAS = 3

QUADRO = re.compile(r'<table class="quadro(?: quadro--cartoes)?">(.*?)</table>', re.S)
CABECA = re.compile(r'<thead>\s*<tr>(.*?)</tr>\s*</thead>', re.S)
CELULA_TH = re.compile(r'<th[^>]*>(.*?)</th>', re.S)
LINHA = re.compile(r'<tr>(.*?)</tr>', re.S)
CELULA_TD = re.compile(r'<td(\s[^>]*?)?>', re.S)


def texto(bruto):
    """Tira as etiquetas e aperta os espacos, para o nome caber num atributo."""
    t = re.sub(r'<[^>]+>', '', bruto)
    t = re.sub(r'\s+', ' ', t).strip()
    return t.replace('"', '&quot;')


def rotula_linha(linha, nomes):
    """Reescreve os data-r de uma linha do corpo, pela ordem das colunas."""
    partes = []
    fim = 0
    for i, m in enumerate(CELULA_TD.finditer(linha)):
        partes.append(linha[fim:m.start()])
        atrs = (m.group(1) or '')
        atrs = re.sub(r'\s+data-r="[^"]*"', '', atrs)
        if i < len(nomes) and nomes[i]:
            atrs = atrs + ' data-r="' + nomes[i] + '"'
        partes.append('<td' + atrs + '>')
        fim = m.end()
    partes.append(linha[fim:])
    return ''.join(partes)


def trata(miolo):
    cab = CABECA.search(miolo)
    if not cab:
        return None, 0
    nomes = [texto(t) for t in CELULA_TH.findall(cab.group(1))]
    if len(nomes) < MIN_COLUNAS:
        return None, len(nomes)
    corpo_ini = cab.end()
    cabeca, corpo = miolo[:corpo_ini], miolo[corpo_ini:]
    corpo = LINHA.sub(lambda m: '<tr>' + rotula_linha(m.group(1), nomes) + '</tr>', corpo)
    return cabeca + corpo, len(nomes)


paginas = [q for q in (x.replace(os.sep, '/') for x in glob.glob('**/*.html', recursive=True))
           if not q.startswith('propostas/')]

tocadas = quadros = cartoes = curtos = 0
for p in paginas:
    h = io.open(p, encoding='utf-8').read()
    if '<table class="quadro' not in h:
        continue

    def troca(m):
        global quadros, cartoes, curtos
        quadros += 1
        novo, n = trata(m.group(1))
        if novo is None:
            curtos += 1
            return '<table class="quadro">' + m.group(1) + '</table>'
        cartoes += 1
        return '<table class="quadro quadro--cartoes">' + novo + '</table>'

    novo = QUADRO.sub(troca, h)
    if novo != h:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(novo)
        tocadas += 1

print(f"quadros {quadros}, em cartoes {cartoes}, de duas colunas {curtos}, paginas reescritas {tocadas}")
