# -*- coding: utf-8 -*-
"""Poe a rede do gerador das iniciais a prova, estragando a fonte de proposito.

PORQUE E QUE ISTO E PRECISO
O gerador tem conferencias que o fazem parar antes de gravar. Mas uma
conferencia que nunca dispara nao e uma rede, e uma linha que da conforto. A
unica maneira de saber que funciona e estragar a pagina de proposito e ver se
ela se queixa.

E ha uma armadilha dentro da propria prova, que vale a pena dizer por extenso.
A maneira obvia de testar era repor o erro antigo, os comentarios do CSS com a
etiqueta escrita por extenso, e esperar que a rede o apanhasse. Isso nao prova
nada: desde que a etiqueta saiu dos comentarios, procurar desde o principio do
ficheiro encontra hoje a etiqueta certa por acaso, e a prova passaria por o
erro ja nao se reproduzir, nao por a rede funcionar. Por isso cada estrago aqui
ataca a rede directamente, e nao a causa antiga.

COMO CORRE
Faz uma copia do que e preciso numa pasta descartavel, com a mesma arrumacao
que o repositorio tem, e corre o gerador la. Nao toca no repositorio a serio,
que esta a ser usado por outra sessao ao mesmo tempo.
"""
import io, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(os.path.abspath(__file__))


def monta(destino):
    """Copia uma arrumacao minima do repositorio: o gerador precisa do
    index.html na raiz e das duas paginas de destino."""
    os.makedirs(os.path.join(destino, 'ferramentas'), exist_ok=True)
    os.makedirs(os.path.join(destino, 'en'), exist_ok=True)
    os.makedirs(os.path.join(destino, 'fr'), exist_ok=True)
    for f in ('iniciais.py', 'textos_iniciais.py'):
        shutil.copy2(os.path.join(REPO, 'ferramentas', f),
                     os.path.join(destino, 'ferramentas', f))
    shutil.copy2(os.path.join(REPO, 'index.html'), os.path.join(destino, 'index.html'))
    shutil.copy2(os.path.join(REPO, 'en', 'index.html'), os.path.join(destino, 'en', 'index.html'))
    shutil.copy2(os.path.join(REPO, 'fr', 'index.html'), os.path.join(destino, 'fr', 'index.html'))


def corre(destino):
    r = subprocess.run([sys.executable, '-X', 'utf8',
                        os.path.join(destino, 'ferramentas', 'iniciais.py')],
                       capture_output=True, text=True, encoding='utf-8', cwd=destino)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


# ----------------------------------------------------- os estragos
def tira_regra_da_vitrine(h):
    """Apaga a regra principal da vitrine dentro do bloco de estilo.

    A regra existe duas vezes, a principal e a do telemovel. Este estrago tira
    so a principal, que e o caso dificil: a primeira versao da conferencia
    procurava um texto comum as duas e por isso deixava passar."""
    return h.replace('body.inicial .vitrine__inclina{',
                     'body.inicial .vitrine__apagada{', 1)


def troca_bloco_por_comentario(h):
    """Poe um <style id="pagina"> falso dentro do bloco partilhado, antes do
    verdadeiro. E a forma generica da armadilha antiga: qualquer texto que se
    pareca com a etiqueta e que apareca primeiro leva o gerador atras."""
    i = h.index('<style id="home-light">')
    j = h.index('\n', i) + 1
    return h[:j] + '/* isto parece <style id="pagina"> mas e so texto */\n' + h[j:]


def parte_a_condicao(h):
    """Muda a classe que o guiao procura. Foi o erro a serio: o guiao saia na
    primeira linha, a vitrine ficava vazia e nao havia erro nenhum."""
    return h.replace('classList.contains("inicial")', 'classList.contains("inicial-outra")', 1)


def tira_a_vitrine_do_guiao(h):
    """Apaga SO a definicao da funcao, e deixa os tres usos de pe.

    A primeira versao deste estrago trocava o nome em todo o lado, por isso
    qualquer conferencia de presenca o apanhava e a prova nao dizia nada sobre
    o caso dificil. Apagar so a definicao e o caso a serio: o guiao fica
    partido e o nome continua la tres vezes.

    O nome novo nao pode comecar pelo antigo. A segunda versao chamava-lhe
    montaVitrineQueJaNaoEChamada e a prova falhou por isso: a marca antiga
    continuava la dentro do nome novo. Foi dai que saiu o limite de palavra na
    contagem do gerador."""
    return h.replace('function montaVitrine', 'function jaNaoMontaNada', 1)


def tira_regras_que_nenhuma_marca_cobre(h):
    """Esvazia o bloco de estilo sem tocar em nenhuma das marcas.

    Este estrago existe por uma razao so: sem ele, a contagem minima de regras
    nunca se via a trabalhar. Todos os outros estragos disparam por uma marca,
    por isso a contagem ficava por provar e eu ficava com a ideia de que estava
    provada, que e o mesmo erro de ter uma conferencia que nunca dispara.

    Renomeia body.inicial em todas as linhas EXCEPTO nas que levam uma marca,
    por isso as quatro marcas continuam la e unicas. So a contagem o pode
    apanhar."""
    marcas = ('body.inicial .vitrine__inclina{', '@keyframes in-desliza',
              'body.inicial .hero__quem{', 'body.inicial .cartao span{')
    saida = []
    for linha in h.split('\n'):
        if 'body.inicial' in linha and not any(m in linha for m in marcas):
            linha = linha.replace('body.inicial', 'body.outra')
        saida.append(linha)
    return '\n'.join(saida)


def muda_uma_frase(h):
    """Muda uma frase portuguesa sem mudar a chave da traducao. O gerador nao
    deve parar, mas tem de dizer em voz alta que aquela ficou por traduzir."""
    return h.replace('Resposta em 24 horas', 'Resposta em 12 horas', 1)


ESTRAGOS = [
    ('a regra principal da vitrine sai do bloco de estilo', tira_regra_da_vitrine, 'para',
     'vezes em vez de uma'),
    ('texto que se parece com a etiqueta, antes do bloco', troca_bloco_por_comentario, 'para',
     'apanhei a coisa errada'),
    ('a condicao que liga o guiao e mudada', parte_a_condicao, 'para',
     'estragou a condicao que liga o guiao'),
    ('o guiao perde a definicao da vitrine, e os usos ficam', tira_a_vitrine_do_guiao, 'para',
     '"function montaVitrine" 0 vezes'),
    ('o estilo perde regras que nenhuma marca cobre', tira_regras_que_nenhuma_marca_cobre,
     'para', 'regras body.inicial'),
    ('uma frase portuguesa muda e a chave nao', muda_uma_frase, 'avisa',
     'sem traducao'),
]

print('=' * 74)
print('PROVA 0: a pagina boa tem de passar e gravar as duas linguas')
print('=' * 74)
base = tempfile.mkdtemp(prefix='prova-boa-')
monta(base)
codigo, saida = corre(base)
# O gerador e idempotente, por isso correr sobre paginas ja geradas devolve os
# mesmos bytes: medir a mudanca de tamanho nao diz nada. O que tem de ser
# verdade e que o resultado tem mesmo a pagina inicial la dentro.
saiu_bem = True
for l in ('en', 'fr'):
    h = io.open(os.path.join(base, l, 'index.html'), encoding='utf-8').read()
    for marca in ('class="inicial"', 'class="vitrine"', 'body.inicial .vitrine__inclina{',
                  'id="pedido"', '<!-- inicial cinzenta -->'):
        if marca not in h:
            print(f'  {l}: ficou sem {marca}')
            saiu_bem = False
passou = codigo == 0 and 'sem avisos' in saida and saiu_bem
print(f'  saiu com {codigo}, "sem avisos" presente: {"sem avisos" in saida}, '
      f'as duas paginas tem as pecas todas: {saiu_bem}')
print(f'  -> {"PASSOU" if passou else "FALHOU"}')
shutil.rmtree(base, ignore_errors=True)

falhas = 0 if passou else 1
for n, (nome, estrago, esperado, pista) in enumerate(ESTRAGOS, 1):
    print()
    print('=' * 74)
    print(f'PROVA {n}: {nome}')
    print(f'   esperado: o gerador {esperado}, a dizer "{pista}"')
    print('=' * 74)
    d = tempfile.mkdtemp(prefix=f'prova-{n}-')
    monta(d)
    alvo = os.path.join(d, 'index.html')
    h = io.open(alvo, encoding='utf-8').read()
    novo = estrago(h)
    if novo == h:
        print('  o estrago nao mudou nada: a prova nao prova nada')
        falhas += 1
        shutil.rmtree(d, ignore_errors=True)
        continue
    io.open(alvo, 'w', encoding='utf-8', newline='\n').write(novo)

    tamanhos = {l: os.path.getsize(os.path.join(d, l, 'index.html')) for l in ('en', 'fr')}
    codigo, saida = corre(d)
    agora = {l: os.path.getsize(os.path.join(d, l, 'index.html')) for l in ('en', 'fr')}

    if esperado == 'para':
        bem = codigo != 0 and pista in saida and agora == tamanhos
        print(f'  saiu com {codigo} (devia ser diferente de 0)')
        print(f'  disse "{pista}": {pista in saida}')
        print(f'  deixou os ficheiros em paz: {agora == tamanhos}')
    else:
        bem = codigo == 0 and pista in saida
        print(f'  saiu com {codigo} (devia ser 0)')
        print(f'  avisou "{pista}": {pista in saida}')
        for linha in saida.splitlines():
            if pista in linha:
                print(f'     {linha.strip()}')
    print(f'  -> {"PASSOU" if bem else "FALHOU"}')
    if not bem:
        falhas += 1
        print('  --- o que o gerador disse ---')
        for linha in saida.strip().splitlines()[-8:]:
            print('      ' + linha)
    shutil.rmtree(d, ignore_errors=True)

print()
print('=' * 74)
print(f'{len(ESTRAGOS) + 1 - falhas} de {len(ESTRAGOS) + 1} provas passaram')
sys.exit(1 if falhas else 0)
