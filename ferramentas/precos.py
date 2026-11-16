# -*- coding: utf-8 -*-
"""Constroi a pagina /precos/ a partir da pagina /diagnostico/.

PORQUE E QUE E GERADA E NAO ESCRITA A MAO

A pagina de precos tem o mesmo teste de seis perguntas que o diagnostico, mas
com outra moldura: tres maneiras de comecar, lado a lado, e a terceira so se
preenche quando alguem acaba o teste. Se o teste fosse copiado a mao, as duas
copias separavam-se na primeira vez que alguem mexesse nos precos do CONFIG, e
separavam-se em silencio. Assim ha uma fonte so, que e a pagina do
diagnostico, e este ficheiro volta a copiar de la sempre que correr.

O QUE VEM DE LA, SEM UMA LINHA DE DIFERENCA

  - o bloco <style id="pagina"> com o CSS do teste
  - a marcacao do teste, o <div class="quiz">
  - o guiao do teste, o <script> que tem o CONFIG e a conta dos precos

O QUE E SO DESTA PAGINA

  - a cabeca: titulo, descricao, canonico, Open Graph, dados estruturados
  - o hero e os tres cartoes de preco
  - o CSS dos cartoes, que vai colado a seguir ao CSS do teste
  - um guiao pequeno que fica a ver quando o resultado aparece e o copia para
    o terceiro cartao. Nao toca no teste: so observa.

CORRER DEPOIS DE MEXER NO TESTE. E depois disto, como sempre, o
refresca_css.py, o sincroniza.py, o linkagem.py e o auditoria.py.

NOTA PARA QUEM EDITAR ESTE FICHEIRO: tem acentos e tem de ficar em UTF-8 sem
BOM. Nao passe por Get-Content e Set-Content do PowerShell: a ida e volta poe
BOM e come os acentos. Ja aconteceu, e foi preciso reescrever o ficheiro.
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)

FONTE = 'diagnostico/index.html'
DESTINO = 'precos/index.html'

CALENDARIO = 'https://calendar.app.google/zDSGkBP7xeXmWkmx8'
MAIL_HORA = ('mailto:geral@wandofi.pt?subject=Revis%C3%A3o%20de%20projecto%2C%20uma%20hora'
             '&body=Ol%C3%A1%20Mauro%2C%20queria%20a%20hora%20de%20revis%C3%A3o.%20'
             'O%20meu%20site%20%C3%A9%3A%20')
WHATS_HORA = ('https://wa.me/351937733527?text=Ol%C3%A1%2C%20queria%20a%20revis%C3%A3o%20de%20'
              'projecto%20de%20uma%20hora.')

if not os.path.isfile(FONTE):
    sys.exit(f'falta {FONTE}')
h = io.open(FONTE, encoding='utf-8').read()

# ---------------------------------------------------------------- 1. a cabeca
TITULO = 'Preços | Wandofi PM'
DESCR = ('Três maneiras de começar: diagnóstico de 15 minutos grátis, hora de revisão a 80 €, '
         'e uma estimativa para o seu projecto em dois minutos. Sem avença obrigatória.')
DESCR_CURTA = ('Diagnóstico de 15 minutos grátis, hora de revisão a 80 €, e uma estimativa '
               'para o seu projecto em dois minutos.')

trocas_cabeca = [
    (r'<title>.*?</title>', f'<title>{TITULO}</title>'),
    (r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{DESCR}"'),
    (r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="https://wandofi.pt/precos/"'),
    (r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="https://wandofi.pt/precos/"'),
    (r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{TITULO}"'),
    (r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{DESCR_CURTA}"'),
    (r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{TITULO}"'),
    (r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{DESCR_CURTA}"'),
]
for padrao, novo in trocas_cabeca:
    h, n = re.subn(padrao, lambda _m, v=novo: v, h, count=1)
    if not n:
        sys.exit(f'cabeca: nao encontrei {padrao}')

# ------------------------------------------------- 2. os dados estruturados
# Tres blocos, como manda o metodo das paginas novas: o servico com a unica
# oferta que tem preco fixo, as perguntas frequentes, e as migalhas.
#
# Da oferta da hora fica de fora o IVA, de proposito. O regime ainda nao esta
# confirmado e um dado estruturado errado sobre imposto e pior do que nenhum:
# a pagina diz, em texto, que o valor do IVA vai na resposta.
DADOS = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Revisão de projecto, uma hora",
  "serviceType": "Consultoria de SEO e project management",
  "description": "Uma hora de revisão ao que já existe, com a lista do que corrigir por ordem. Paga antes da marcação.",
  "provider": { "@type": "Person", "name": "Mauro Cordeiro", "url": "https://wandofi.pt/sobre/" },
  "areaServed": { "@type": "Country", "name": "Portugal" },
  "url": "https://wandofi.pt/precos/",
  "offers": {
    "@type": "Offer",
    "price": "80",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock",
    "url": "https://wandofi.pt/precos/"
  }
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Pago antes ou depois da reunião?",
      "acceptedAnswer": { "@type": "Answer", "text": "A hora de revisão é paga antes. Marco a hora depois de confirmar o pagamento. O diagnóstico de 15 minutos é grátis, com marcação directa no calendário." }
    },
    {
      "@type": "Question",
      "name": "A estimativa do teste é um orçamento?",
      "acceptedAnswer": { "@type": "Answer", "text": "Não. É uma ordem de grandeza, para sabermos se estamos no mesmo campo antes de gastarmos tempo os dois. O valor fechado só sai depois de eu ver o que existe." }
    },
    {
      "@type": "Question",
      "name": "Há avença obrigatória?",
      "acceptedAnswer": { "@type": "Answer", "text": "Não. Os projectos são pagos de uma vez. O trabalho contínuo de SEO tem avença mensal, mas sem permanência obrigatória, e começa quando o arranque termina." }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Início", "item": "https://wandofi.pt/" },
    { "@type": "ListItem", "position": 2, "name": "Preços", "item": "https://wandofi.pt/precos/" }
  ]
}
</script>'''

todos = re.search(r'(<script type="application/ld\+json">.*?</script>)(\s*<script type="application/ld\+json">.*?</script>)*',
                  h, re.S)
if not todos:
    sys.exit('nao encontrei os dados estruturados')
h = h[:todos.start()] + DADOS + h[todos.end():]

# ----------------------------------------------------- 3. o CSS dos cartoes
CSS_CARTOES = '''
/* ===== Cartoes de preco, so nesta pagina ==============================
   Tres colunas iguais que passam a uma coluna abaixo dos 900 px. O
   terceiro cartao nasce por preencher e so ganha valor quando alguem acaba
   o teste, por isso tem dois estados e nao pode mudar de altura entre eles
   sem empurrar a pagina: leva altura minima e o conteudo troca por dentro.
   ===================================================================== */
.precos{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;align-items:stretch;margin:0}
@media (max-width:900px){.precos{grid-template-columns:1fr}}
.preco{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--r);
  background:var(--panel);padding:1.5rem 1.4rem 1.4rem;min-height:21rem}
.preco--destaque{border-color:var(--mute)}
.preco__rotulo{margin:0 0 .2rem;font-family:var(--mono);font-size:.68rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--mute)}
.preco__nome{margin:0 0 .7rem;font-family:var(--serif);font-weight:400;letter-spacing:-.015em;
  font-size:clamp(1.3rem,2.2vw,1.6rem);line-height:1.12;color:var(--ink)}
.preco__valor{margin:0 0 .15rem;font-family:var(--serif);font-weight:400;letter-spacing:-.02em;
  font-size:clamp(2rem,3.4vw,2.7rem);line-height:1;color:var(--ink)}
.preco__valor .un{font-family:var(--ui);font-size:.9rem;letter-spacing:0;color:var(--mute)}
.preco__quando{margin:0 0 .9rem;font-family:var(--mono);font-size:.72rem;letter-spacing:.06em;
  color:var(--mute)}
.preco__txt{margin:0 0 1rem;font-size:.95rem;line-height:1.6;color:var(--ink-soft)}
.preco__txt b{color:var(--ink);font-weight:600}
.preco__accoes{margin-top:auto;display:flex;flex-wrap:wrap;gap:.5rem}
.preco__accoes .btn{font-size:.92rem}
.preco__nota{margin:.8rem 0 0;font-size:.82rem;line-height:1.5;color:var(--mute)}
/* O terceiro cartao: dois estados, um de cada vez. */
.preco__cheio{display:none}
.preco.tem-valor .preco__vazio{display:none}
.preco.tem-valor .preco__cheio{display:block}
.preco.tem-valor{border-color:var(--red)}
.preco__prazo{margin:.1rem 0 .9rem;font-size:.88rem;line-height:1.5;color:var(--ink-soft)}
'''

# ------------------------------------------------ 4. o hero e os cartoes
#
# Os tres botoes dos cartoes sao todos ghost, e isso e por causa da regra das
# tres cores: o vermelho e acento e nunca pode estar em mais de tres elementos
# visiveis ao mesmo tempo. No primeiro ecra ja ha tres, o botao da barra, o
# sobretitulo e o rabisco debaixo da palavra destacada. Um quarto botao
# vermelho nos cartoes passava a conta.
#
# O unico vermelho que a pagina ganha e o "Marcar para confirmar", que so
# aparece depois de alguem acabar o teste. Nessa altura ja se rolou, o
# sobretitulo e o rabisco ficaram para tras, e o acento esta sozinho na accao
# que fecha o circulo, que e exactamente o que a regra quer.
HERO_E_CARTOES = f'''      <section class="hero" style="padding-block:clamp(2rem,4vw,3.2rem) clamp(1.2rem,2.4vw,1.8rem)">
        <div class="container">
          <div style="max-width:46rem">
            <p class="page-hero__crumb"><a href="/">Início</a><span class="sep">/</span><a href="/precos/">Preços</a></p>
            <p class="eyebrow">Preços</p>
            <h1 class="h1" style="font-size:clamp(2.1rem,4.6vw,3.4rem);margin-bottom:.9rem">Três maneiras de <em class="dm-rabisco">começar</em>.</h1>
            <p class="lead" style="max-width:54ch">Uma é grátis, uma é paga à hora, e a terceira depende do que precisa. O teste aqui em baixo diz em que ordem de grandeza está o seu caso, em dois minutos e sem dar o email.</p>
          </div>
        </div>
      </section>

      <section class="section" style="padding-top:0">
        <div class="container">
          <div class="precos">

            <div class="preco">
              <p class="preco__rotulo">Para começar</p>
              <p class="preco__nome">Diagnóstico</p>
              <p class="preco__valor">Grátis</p>
              <p class="preco__quando">15 minutos, por videochamada</p>
              <p class="preco__txt">Vemos o site, a indexação e o que está a travar. Sai da conversa com uma lista por ordem de prioridade, avance ou não comigo.</p>
              <p class="preco__accoes"><a class="btn btn--ghost" data-cta="precos-diagnostico" href="{CALENDARIO}" target="_blank" rel="noopener">Marcar diagnóstico <span class="arrow" aria-hidden="true">↗</span></a></p>
              <p class="preco__nota">Abre o calendário numa janela nova.</p>
            </div>

            <div class="preco preco--destaque">
              <p class="preco__rotulo">Para quem já tem site</p>
              <p class="preco__nome">Revisão de projecto</p>
              <p class="preco__valor">80 €<span class="un"> à hora</span></p>
              <p class="preco__quando">1 hora, por videochamada</p>
              <p class="preco__txt">Olho ao detalhe para o que já existe e sai de lá com a lista do que corrigir, por ordem. <b>Paga antes: marco a hora depois de confirmar o pagamento.</b> Peça por email ou por WhatsApp e envio os dados.</p>
              <p class="preco__accoes"><a class="btn btn--ghost" data-cta="precos-hora-email" href="{MAIL_HORA}">Pedir por email</a><a class="btn btn--ghost" data-cta="precos-hora-whatsapp" href="{WHATS_HORA}" target="_blank" rel="noopener">WhatsApp</a></p>
              <p class="preco__nota">Na resposta digo se acresce IVA.</p>
            </div>

            <div class="preco" id="cartao-estimativa">
              <p class="preco__rotulo">Para o seu caso</p>
              <p class="preco__nome">O seu projecto</p>
              <div class="preco__vazio">
                <p class="preco__valor">Por estimar</p>
                <p class="preco__quando">Seis perguntas, dois minutos</p>
                <p class="preco__txt">Responda ao teste aqui em baixo e fica com uma faixa de preço e de prazo para o que precisa. Não é preciso dar o email para ver o resultado.</p>
                <p class="preco__accoes"><a class="btn btn--ghost" href="#quiz" data-cta="precos-teste">Fazer o teste <span class="arrow" aria-hidden="true">↗</span></a></p>
              </div>
              <div class="preco__cheio">
                <p class="preco__valor" id="cartao-valor"></p>
                <p class="preco__prazo" id="cartao-prazo"></p>
                <p class="preco__txt">Valor estimado. O orçamento fechado só sai depois de eu ver o que existe, e é para isso que serve a conversa de 15 minutos.</p>
                <p class="preco__accoes"><a class="btn btn--red" data-cta="precos-confirmar" href="{CALENDARIO}" target="_blank" rel="noopener">Marcar para confirmar <span class="arrow" aria-hidden="true">↗</span></a></p>
              </div>
            </div>

          </div>
        </div>
      </section>

      <section class="section" style="padding-top:0">
        <div class="container">
          <header class="section__head" style="max-width:46rem">
            <p class="eyebrow">O teste</p>
            <h2 class="h2">Quanto custa pôr isto a funcionar?</h2>
            <p class="body" style="max-width:56ch">Seis perguntas sobre o que precisa, a dimensão do negócio e o que já existe. No fim, a estimativa sobe para o terceiro cartão aqui em cima.</p>
          </header>
'''

FECHO_QUIZ = '''        </div>
      </section>

      <section class="section section--panel">
        <div class="container">
          <header class="section__head"><h2 class="h2">Perguntas frequentes</h2></header>
          <div class="faqs">
            <details class="faq"><summary>Pago antes ou depois da reunião?</summary><div class="faq__a"><p class="body">A hora de revisão é paga antes. Marco a hora depois de confirmar o pagamento. O diagnóstico de 15 minutos é grátis, com marcação directa no calendário.</p></div></details>
            <details class="faq"><summary>A estimativa do teste é um orçamento?</summary><div class="faq__a"><p class="body">Não. É uma ordem de grandeza, para sabermos se estamos no mesmo campo antes de gastarmos tempo os dois. O valor fechado só sai depois de eu ver o que existe.</p></div></details>
            <details class="faq"><summary>Há avença obrigatória?</summary><div class="faq__a"><p class="body">Não. Os projectos são pagos de uma vez. O trabalho contínuo de SEO tem avença mensal, mas sem permanência obrigatória, e começa quando o arranque termina.</p></div></details>
          </div>
        </div>
      </section>
'''

# ------------------------------------------------- 5. o guiao do espelho
ESPELHO = '''<script>
/* O teste nao sabe que esta nesta pagina, e e assim que deve ser: a pagina do
   diagnostico e a fonte e nao leva uma linha a mais por causa desta. Este
   guiao so fica a ver quando o painel do resultado deixa de estar escondido,
   e copia o que la esta para o terceiro cartao.

   O valor vai por innerHTML porque o teste escreve ali um <span> com a
   unidade, e esse HTML e escrito pelo proprio teste, nunca pelo visitante. O
   prazo vai por textContent. */
(function () {
  "use strict";
  var painel = document.getElementById("resultado");
  var cartao = document.getElementById("cartao-estimativa");
  if (!painel || !cartao) return;

  var destinoValor = document.getElementById("cartao-valor");
  var destinoPrazo = document.getElementById("cartao-prazo");
  var jaFeito = false;

  function copia() {
    if (jaFeito || painel.hidden) return;
    var valor = document.getElementById("res-valor");
    var arranque = document.getElementById("res-arranque");
    var prazo = document.getElementById("res-prazo");
    if (!valor || !valor.innerHTML) return;
    jaFeito = true;

    destinoValor.innerHTML = valor.innerHTML;
    var linhas = [];
    if (arranque && !arranque.hidden && arranque.textContent) linhas.push(arranque.textContent);
    if (prazo && prazo.textContent) linhas.push(prazo.textContent);
    destinoPrazo.textContent = linhas.join(" ");
    cartao.classList.add("tem-valor");

    /* O teste rola para o seu proprio resultado. Aqui o que interessa e o
       cartao, que e onde a pagina poe as tres hipoteses lado a lado. Espera
       que a rolagem do teste acabe antes de pedir a sua. */
    setTimeout(function () {
      cartao.scrollIntoView({ block: "center", behavior: "smooth" });
    }, 700);

    if (typeof gtag === "function") {
      gtag("event", "precos_estimativa", { pagina: "precos" });
    }
  }

  new MutationObserver(copia).observe(painel, { attributes: true, attributeFilter: ["hidden"] });
  copia();
})();
</script>'''

# ------------------------------------------------- 6. montar o corpo
quiz = re.search(r'(          <div class="quiz" id="quiz">.*?\n          </div>\n)', h, re.S)
if not quiz:
    sys.exit('nao encontrei o bloco do teste')
BLOCO_QUIZ = quiz.group(1)

corpo = re.search(r'(<main id="main"[^>]*>)(.*?)(</main>)', h, re.S)
if not corpo:
    sys.exit('nao encontrei o main')
novo_corpo = (corpo.group(1) + '\n' + HERO_E_CARTOES + BLOCO_QUIZ + FECHO_QUIZ
              + '<section class="section"><div class="container"><header class="section__head">'
                '<h2 class="h2">Onde ir a partir daqui</h2></header><div class="related">'
                '<a href="/diagnostico/">Diagnóstico</a><a href="/seo/">SEO</a>'
                '<a href="/criacao-de-sites/">Criação de sites</a>'
                '<a href="/automacoes/">Automações</a><a href="/casos/">Casos</a>'
                '<a href="/sobre/">Sobre</a></div></div></section>\n'
              + corpo.group(3))
h = h[:corpo.start()] + novo_corpo + h[corpo.end():]

# O CSS dos cartoes vai colado ao fim do CSS do teste.
#
# Procurar <style id="pagina"> a partir do principio do ficheiro nao serve, e
# ja partiu uma vez em silencio: o bloco home-light tem comentarios que falam
# do <style id="pagina"> por escrito, e a procura apanhava o comentario em vez
# da etiqueta. O CSS ia parar ao fim do home-light, e o refresca_css.py, que
# reescreve esse bloco todo, apagava-o a seguir sem dizer nada.
#
# Por isso a procura comeca depois do home-light acabar.
abre_home = h.index('<style id="home-light">')
fim_home = h.index('</style>', abre_home) + len('</style>')
abre_pagina = h.find('<style id="pagina">', fim_home)
if abre_pagina < 0:
    sys.exit('nao encontrei o <style id="pagina"> depois do home-light')
fecha_pagina = h.index('</style>', abre_pagina)
h = h[:fecha_pagina] + CSS_CARTOES + h[fecha_pagina:]

# o espelho entra antes do fim do corpo
h, n = re.subn(r'\n</body>', lambda _m: '\n' + ESPELHO + '\n</body>', h, count=1)
if not n:
    sys.exit('nao encontrei o fim do corpo')

os.makedirs('precos', exist_ok=True)
io.open(DESTINO, 'w', encoding='utf-8', newline='\n').write(h)
print(f'{DESTINO} escrito, {len(h):,} bytes')
print('o teste veio do diagnostico sem uma linha de diferenca')
