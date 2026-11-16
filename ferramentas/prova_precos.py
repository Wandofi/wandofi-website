# -*- coding: utf-8 -*-
"""Prova que a conferencia do ferramentas/precos.py apanha paginas partidas.

Uma rede de seguranca que nunca se viu a apanhar nada nao e uma rede de
seguranca. Esta prova pega na pagina publicada, estraga-a de nove maneiras, e
confirma que a conferencia se queixa das nove e deixa passar a boa. Nao
escreve nada: trabalha so em memoria.

DUAS LICOES QUE ESTAO AQUI DENTRO, as duas aprendidas a errar.

A primeira: a primeira versao desta prova punha o erro antigo de volta no
gerador e esperava que a conferencia o apanhasse. Nao apanhou. Desde que os
comentarios do CSS deixaram de escrever a etiqueta do bloco por extenso, o
erro antigo ja nao se reproduz, por isso a prova so estava a dizer que a fonte
esta limpa. Uma prova indirecta pode passar por motivos que nada tem a ver com
o que ela julga medir. Por isso esta vai directa a rede.

A segunda, que veio da sessao das iniciais traduzidas: uma marca que aparece
mais do que uma vez nao confere nada. A conferencia dela procurava uma regra
que existe duas vezes, a principal e a do telemovel dentro de uma media query,
e apagada a principal dizia que estava tudo bem. O mesmo buraco estava aqui,
em ".res__valor" e ".captura", que sao prefixo de outras classes. Hoje a
conferencia exige que cada marca apareca uma e so uma vez, e dois dos estragos
aqui em baixo existem so para provar isso.

CORRER depois de mexer no precos.py ou no CSS dos cartoes.
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

# A funcao vive dentro de um guiao que faz trabalho ao ser importado, por isso
# e tirada de la pelo texto em vez de importada.
fonte = io.open('ferramentas/precos.py', encoding='utf-8').read()
m = re.search(r'\ndef confere\(texto\):\n(?:.*?\n)*?    return problemas\n', fonte)
if not m:
    sys.exit('nao encontrei a funcao confere no gerador')
ambito = {'re': re}          # o re tem de ir no ambito: o exec nao herda nada
exec(m.group(0), ambito)
confere = ambito['confere']

boa = io.open('precos/index.html', encoding='utf-8').read()


def _bloco_proprio(h):
    abre_h = h.index('<style id="home-light">')
    fim_h = h.index('</style>', abre_h) + len('</style>')
    abre_p = h.find('<style id="pagina">', fim_h)
    return abre_p, h.index('</style>', abre_p)


def move_css_para_o_bloco_partilhado(h):
    """O erro que aconteceu de verdade: o CSS dos cartoes escrito no bloco que
    o refresca_css.py reescreve por inteiro, e que o apaga a seguir."""
    abre_h = h.index('<style id="home-light">')
    fecha_h = h.index('</style>', abre_h)
    abre_p, fecha_p = _bloco_proprio(h)
    bloco_p = h[abre_p:fecha_p]
    i = bloco_p.index('.precos{display:grid')
    return h[:fecha_h] + bloco_p[i:] + h[fecha_h:abre_p + i] + h[fecha_p:]


def tira_regras_sem_marca(h):
    """Tira regras que nenhuma marca cobre, para a contagem minima ter de ser
    ela a apanhar o estrago. Sem isto, a contagem nunca se via a trabalhar."""
    for regra in ('.preco__quando{', '.preco__txt{', '.preco__accoes{',
                  '.preco__nota{', '.preco__prazo{', '.preco--destaque{'):
        i = h.find(regra)
        if i >= 0:
            h = h[:i] + h[h.index('}', i) + 1:]
    return h


def apaga_a_principal_e_deixa_a_do_telemovel(h):
    """A regra dos cartoes existe duas vezes, a principal e a do telemovel.
    Apagada a principal, uma conferencia que so procure presenca encontra a
    outra e diz que esta tudo bem, com a pagina mesmo sem a grelha."""
    i = h.index('.precos{display:grid')
    return h[:i] + h[h.index('}', i) + 1:]


def duplica_uma_marca(h):
    """Uma marca que deixa de ser unica deixa de conferir, e a ferramenta tem
    de o dizer em vez de continuar calada a fazer de conta."""
    return h.replace('.preco__rotulo{', '.preco__rotulo{color:inherit}\n.preco__rotulo{', 1)


def corta_o_bloco_a_meio(h):
    abre_p, fecha_p = _bloco_proprio(h)
    bloco = h[abre_p:fecha_p]
    return h[:abre_p] + bloco[:len('<style id="pagina">')] + bloco[len(bloco) // 2:] + h[fecha_p:]


ESTRAGOS = [
    ('o CSS dos cartoes vai para o bloco partilhado', move_css_para_o_bloco_partilhado),
    ('tiradas regras que nenhuma marca cobre', tira_regras_sem_marca),
    ('apagada a regra principal, fica so a do telemovel', apaga_a_principal_e_deixa_a_do_telemovel),
    ('uma marca deixou de ser unica', duplica_uma_marca),
    ('o bloco de estilo foi cortado a meio', corta_o_bloco_a_meio),
    ('o CSS do teste nao veio do diagnostico', lambda h: h.replace('.quiz{', '.naoexiste{', 1)),
    ('o cartao da estimativa desapareceu do corpo',
     lambda h: h.replace('id="cartao-estimativa"', 'id="outra-coisa"', 1)),
    ('um comentario do CSS ficou por fechar',
     lambda h: h.replace('/* O terceiro cartao: dois estados, um de cada vez. */',
                         '/* O terceiro cartao: dois estados, um de cada vez.', 1)),
    ('o canonico ficou o da pagina de onde veio',
     lambda h: h.replace('rel="canonical" href="https://wandofi.pt/precos/"',
                         'rel="canonical" href="https://wandofi.pt/diagnostico/"', 1)),
]

print('=== a pagina boa tem de passar ===')
limpos = confere(boa)
if limpos:
    print('  FALHA: a rede queixa-se da pagina que esta publicada:')
    for x in limpos:
        print('    - ' + x)
    sys.exit(1)
print('  passa, sem queixas')

print('\n=== cada estrago tem de ser apanhado ===')
falhou = False
for nome, estraga in ESTRAGOS:
    partida = estraga(boa)
    if partida == boa:
        print(f'  AVISO   : "{nome}" nao chegou a mudar nada, prova desactualizada')
        falhou = True
        continue
    queixas = confere(partida)
    if queixas:
        print(f'  apanhado: {nome}')
        print(f'            -> {queixas[0]}')
    else:
        print(f'  FALHA   : {nome} passou sem queixa nenhuma')
        falhou = True

print('\n=== veredicto ===')
if falhou:
    print('  a rede tem buracos')
    sys.exit(1)
print(f'  a rede apanha os {len(ESTRAGOS)} estragos e deixa passar a pagina boa')
