# -*- coding: utf-8 -*-
"""Deixa o destaque a vermelho no titulo so onde ele quer dizer alguma coisa.

O destaque estava em 52 das 54 paginas, e em 50 delas na ultima palavra da
frase. Deixa de ser um recurso e passa a ser um tique quando aparece em todo
o lado: "Google" estava destacado em cinco paginas diferentes, "fixo" em tres,
"passo" em duas.

A regra: o destaque marca a palavra que a pagina defende, nunca a palavra por
ser a ultima, nunca a mesma palavra em duas paginas, e nunca uma palavra que
a frase nega. Fica nas paginas da lista GUARDA e sai em todas as outras. A
marcacao sai por inteiro, o texto do titulo nao muda.

Correr da raiz. Sem argumentos faz so as contas; com "aplicar" grava.
"""
import io, os, re, sys, glob

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
APLICAR = len(sys.argv) > 1 and sys.argv[1] == 'aplicar'

# onde o destaque fica, e porque. Uma palavra, uma pagina, sem repeticoes.
GUARDA = {
    '/':                     'a frase da marca, e a palavra que a explica',
    '/seo/':                 'clientes, que e o que a pagina promete',
    '/seo/consultor-seo/':   'constroi, que e o posicionamento inteiro',
    '/sobre/':               'pratica, que e de onde vem a autoridade',
    '/gestao-de-trafego/':   'orcamento, que e a objeccao que a pagina responde',
    '/casos/':               'funcionar, que e o criterio dos casos',
}

DESTAQUE = re.compile(r'<span class="dm-bloco-cor dm-cinetico">(.*?)</span>', re.S)
H1 = re.compile(r'(<h1[^>]*>)(.*?)(</h1>)', re.S)

paginas = sorted(q.replace(os.sep, '/') for q in glob.glob('**/index.html', recursive=True)
                 if not q.replace(os.sep, '/').startswith('propostas/'))

fora, fica, saltadas = [], [], 0
for p in paginas:
    url = '/' + p[:-len('index.html')]
    h = io.open(p, encoding='utf-8').read()
    m = H1.search(h)
    if not m:
        continue
    d = DESTAQUE.search(m.group(2))
    if not d:
        saltadas += 1
        continue
    if url in GUARDA:
        fica.append((url, d.group(1).strip()))
        continue
    novo_h1 = m.group(1) + DESTAQUE.sub(lambda x: x.group(1), m.group(2)) + m.group(3)
    fora.append((url, d.group(1).strip()))
    if APLICAR:
        io.open(p, 'w', encoding='utf-8', newline='\n').write(
            h[:m.start()] + novo_h1 + h[m.end():])

print('MODO:', 'APLICADO' if APLICAR else 'so contas, nada gravado')
print(f'destaques removidos: {len(fora)}   mantidos: {len(fica)}   paginas que ja nao tinham: {saltadas}')
print()
print('=== fica ===')
for u, pal in fica:
    print(f'  {pal:<14} {u:<28} {GUARDA[u]}')
print()
print('=== sai ===')
for u, pal in fora:
    print(f'  {pal:<14} {u}')
