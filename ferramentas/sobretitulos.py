# -*- coding: utf-8 -*-
"""Tira os sobretitulos que nao dizem nada que o titulo a seguir ja nao diga.

A regra, por ordem de aplicacao:

1. O primeiro sobretitulo de cada pagina fica sempre. E o que orienta quem
   chega de fora, e nunca repete o titulo porque esta noutro registo.
2. Sai o que e so um numero. Sao as etiquetas 01, 02, 03 das seccoes dos
   artigos, que numeram uma coisa que ninguem conta.
3. Sai o que esta numa lista de etiquetas de estrutura: "Proximo passo",
   "A seguir", "Perguntas frequentes" e os equivalentes em ingles. Nenhuma
   delas diz o assunto da seccao, dizem a posicao da seccao na pagina, coisa
   que a propria pagina ja mostra.
4. Sai o que e um decalque do titulo logo a seguir, ou seja quando as suas
   palavras de conteudo ja estao todas nesse titulo.
5. Tudo o resto fica.

Correr da raiz. Sem argumentos faz so as contas; com "aplicar" grava.
"""
import io, os, re, sys, glob, collections, unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

APLICAR = len(sys.argv) > 1 and sys.argv[1] == 'aplicar'

ESTRUTURA = {
    'proximo passo', 'a seguir', 'next', 'next step', 'perguntas frequentes',
    'questions', 'relacionado', 'relacionados', 'faq',
}
# palavras sem peso, para comparar um sobretitulo com o titulo
VAZIAS = {'o', 'a', 'os', 'as', 'de', 'do', 'da', 'dos', 'das', 'que', 'e', 'em',
          'um', 'uma', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'the', 'of'}

MAIN = re.compile(r'<main[^>]*id="main"[^>]*>(.*?)</main>', re.S)
PAR = re.compile(r'<p class="eyebrow">(.*?)</p>(\s*)(<h[12][^>]*>(.*?)</h[12]>)?', re.S)


def nu(t):
    t = re.sub(r'<[^>]+>', '', t)
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', t).strip().lower()


def palavras(t):
    return {p for p in re.findall(r'[a-z0-9]+', nu(t)) if p not in VAZIAS}


paginas = sorted(q.replace(os.sep, '/') for q in glob.glob('**/index.html', recursive=True)
                 if not q.replace(os.sep, '/').startswith('propostas/'))

motivos = collections.Counter()
tocadas = fora = fica = 0
detalhe = []

for p in paginas:
    h = io.open(p, encoding='utf-8').read()
    m = MAIN.search(h)
    if not m:
        continue
    miolo = m.group(1)
    primeiro = True
    saiu_aqui = []

    def decide(x):
        global primeiro, fora, fica
        etiqueta, titulo = x.group(1), x.group(4) or ''
        e = nu(etiqueta)
        if primeiro:
            primeiro = False
            fica += 1
            return x.group(0)
        motivo = None
        if re.fullmatch(r'\d{1,2}', e):
            motivo = 'numero'
        elif e in ESTRUTURA:
            motivo = 'etiqueta de estrutura'
        elif titulo and palavras(etiqueta) and palavras(etiqueta) <= palavras(titulo):
            motivo = 'decalque do titulo'
        if motivo:
            motivos[motivo] += 1
            fora += 1
            saiu_aqui.append((etiqueta.strip(), motivo))
            # deixa o titulo e o espacamento, tira so a etiqueta
            return (x.group(3) or '') if x.group(3) else ''
        fica += 1
        return x.group(0)

    novo_miolo = PAR.sub(decide, miolo)
    if novo_miolo != miolo:
        tocadas += 1
        detalhe.append(('/' + p[:-len('index.html')], saiu_aqui))
        if APLICAR:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(
                h[:m.start(1)] + novo_miolo + h[m.end(1):])

print('MODO:', 'APLICADO' if APLICAR else 'so contas, nada gravado')
print(f'paginas tocadas: {tocadas} de {len(paginas)}')
print(f'sobretitulos removidos: {fora}   mantidos: {fica}')
print()
for k, v in motivos.most_common():
    print(f'  {v:>4}  {k}')
print()
print('=== o que sai, por pagina ===')
for u, itens in detalhe:
    if itens:
        print(f'{u}')
        for t, mo in itens:
            print(f'      {t[:38]:<40} {mo}')
