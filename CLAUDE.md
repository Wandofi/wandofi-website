# wandofi.pt — instruções de trabalho

Site da Wandofi PM, de Mauro Cordeiro. Consultor de SEO e project
manager em Lisboa. Objectivo comercial único: **ser encontrado e
contratado**. Tudo neste repositório serve isso.

Leia este ficheiro inteiro antes da primeira alteração. Há três coisas
aqui que parecem detalhes e partem o site se forem ignoradas.

---

## 1. Como o site é publicado

| | |
|---|---|
| Repositório | `Wandofi/wandofi-website` |
| Ramo de deploy | **`gh-pages`** |
| Alojamento | GitHub Pages, com `CNAME` para `wandofi.pt` |
| Jekyll | desligado (existe `.nojekyll`), os ficheiros são servidos tal como estão |

Um push para `gh-pages` republica o site. Não há build, não há framework,
não há passo de compilação. O que está no ramo é o que fica online.

**O Replit já não publica.** Publicava até Setembro de 2026 e foi
desligado de propósito, porque dois publicadores no mesmo ramo acabam
sempre com um a apagar o trabalho do outro. Se alguém voltar a ligar o
deploy do Replit, isto volta a partir.

### Antes de cada sessão de trabalho

```bash
git fetch origin && git status
git log --oneline -3 origin/gh-pages
```

Confirme que o local não está atrasado em relação ao remoto antes de
mexer em ficheiros. Já aconteceu uma versão ficar por publicar durante
duas semanas sem ninguém dar por nada.

---

## 2. As três armadilhas

### 2.1 O CSS está embutido em cada página, e isso é de propósito

Cada página tem o CSS completo dentro de um bloco
`<style id="home-light">` no `<head>`. Não há folha de estilo externa.

Isto nasceu de uma limitação do Replit, que não servia ficheiros CSS
novos. O Replit já saiu, por isso a limitação técnica desapareceu, mas a
estrutura ficou e **não deve ser mudada sem uma decisão explícita do
Mauro**. Passar a CSS externo é um refactor de 35 páginas com risco real
de partir tudo, para ganhar uns kilobytes.

**Como se altera CSS, então:**

1. Para estilos partilhados por todas as páginas: editar o bloco
   `<style id="home-light">` dentro de `index-novo.html`.
2. Para estilos só das páginas internas: editar `ferramentas/paginas.css`.
3. Correr `python3 ferramentas/refresca_css.py`, que reescreve o bloco
   em todas as páginas a partir dessas duas fontes.

Nunca edite o bloco `<style>` de uma página interna à mão. Na próxima
vez que alguém correr o refrescador, a alteração desaparece.

### 2.2 `index.html` e `index-novo.html`

No ramo `gh-pages`, `index.html` é a página inicial publicada.

Na árvore de trabalho pode encontrar também `index-novo.html`, que é a
fonte da página inicial e a **fonte do CSS de todo o site**. É um
resto do método antigo, em que o zip mapeava `index-novo.html` para o
`index.html` publicado.

**Isto tem de ser arrumado e é a tarefa número um de quem herdar o
repositório.** Enquanto os dois existirem, há risco de se editar o
ficheiro errado e de o trabalho não aparecer no site. Antes de arrumar,
confirme com o Mauro e verifique qual dos dois está de facto publicado:

```bash
git show origin/gh-pages:index.html | grep -c 'home-light'
```

### 2.3 Ficheiros antigos que ainda lá estão

`styles.css`, `pages.css`, `blog.css` e `main.js` são do tema escuro
anterior. **Nenhuma página os referencia**, depois de os cinco artigos do
blog terem passado a claros.

Podem ser apagados, mas **só depois de confirmar que a versão publicada
já não os usa**. Se apagar antes, os artigos do blog ficam sem estilo
nenhum no site a sério. Verifique assim:

```bash
git show origin/gh-pages:blog/ai-act-ia-no-marketing/index.html | grep -c 'styles.css'
```

Zero, pode apagar. Diferente de zero, espere.

---

## 3. Marca

Paleta de três cores. Vermelho é acento, nunca fundo de área grande. Se
o vermelho aparecer em mais de três elementos visíveis ao mesmo tempo,
há erro.

```
--ink        #050505    texto principal
--paper      #ffffff    fundo
--red        #e1251b    acento, só em acção
--red-deep   #99140f    hover
--livre      #12855a    verde de estado: disponível para projecto
```

O `--livre` é **cor de estado, não é acento de marca**. Foi introduzido
porque o ponto de disponibilidade era vermelho e lia-se como ocupado.
Cor semântica (disponível, aviso, erro) é uma família separada e não
conta para a regra das três cores.

Tipografia, toda do Google Fonts:

- **Instrument Serif** para títulos (`--serif`)
- **Instrument Sans** para interface e corpo (`--ui`)
- **JetBrains Mono** para datas, números e etiquetas (`--mono`)

Medidas de referência, iguais em todas as páginas, a 1280 px: H1 69,6 px,
H2 43,5 px, lead 19,2 px, corpo 16 px com entrelinha 25,9 px, container
1180 px com margem lateral 48 px, secções 69,1 px em cima e em baixo,
texto a 52 caracteres por linha, títulos a 15.

**Anti-marca:** sem gradientes de SaaS, sem `rounded-full` em cartões e
botões, sem fotografias de stock, sem emojis, sem pontos de exclamação,
sem "transformar", "alavancar", "potenciar" ou "revolucionar". Nunca
escrever que o Mauro é advogado: é assistente administrativo num
escritório de advogados, com formação em contabilidade.

---

## 4. Regras de escrita, sem excepção

1. **Português europeu, pré-acordo ortográfico.** "acção", "directo",
   "objectivo", "facto", "óptimo". Nunca português do Brasil.
2. **Sem travessões (—).** Nenhum, em lado nenhum.
3. **Sem hífenes de clítico.** Nada de "faz-se", "nota-se", "executá-lo",
   "falta-lhe". Reescreva a frase em vez de forçar.
4. **Sem pontos de exclamação.**
5. Frases curtas e declarativas. Números concretos em vez de vagos.
6. Nomear ferramentas e contextos portugueses quando for verdade:
   TOConline, Moloni, Avaza, OCC, ENI, IES, ANACOM.

Verificação antes de cada commit:

```bash
grep -rn '—' --include=index.html . | head
grep -rnoE '\w+-(se|lo|la|los|las|lhe|lhes)\b' --include=index.html . | head
```

Ambos têm de devolver vazio.

---

## 5. Ferramentas

Em `ferramentas/`. Correm da raiz do repositório e não precisam de nada
instalado além de Python 3.

| Script | O que faz |
|---|---|
| `refresca_css.py` | Reescreve o bloco `<style id="home-light">` em todas as páginas, a partir do `index-novo.html` e do `paginas.css`. **Correr sempre depois de mexer em CSS.** |
| `sincroniza.py` | Copia a navegação e o rodapé do `index-novo.html` para todas as páginas. Correr depois de mexer no menu ou no rodapé. |
| `linkagem.py` | Reescreve os blocos "Onde ir a partir daqui". Tem um dicionário `ANCORA` com um texto de âncora fixo por destino, e um `JUNTAR` com as ligações a acrescentar por página. **Uma página, uma âncora, sempre igual.** |
| `auditoria.py` | Verifica ligações internas: órfãs, links partidos, profundidade, coerência com o sitemap. **Correr antes de cada commit.** |
| `normaliza.py` | Mantém as páginas internas com as mesmas classes da página inicial. |

`paginas.css` não é servido ao público: é fonte para o refrescador.

### Ordem normal de trabalho

```bash
python3 ferramentas/refresca_css.py     # se mexeu em CSS
python3 ferramentas/sincroniza.py       # se mexeu em nav ou rodapé
python3 ferramentas/linkagem.py         # se acrescentou páginas
python3 ferramentas/auditoria.py        # sempre, antes de commit
```

A auditoria tem de terminar com órfãs `nenhuma`, partidos `nenhum`, e
nada fora do sitemap.

---

## 6. Páginas novas

Ao criar uma página:

1. Copie a estrutura de uma página de serviço existente, por exemplo
   `automacoes/agentes-de-ia/index.html`.
2. Actualize `<title>`, `description`, `canonical`, Open Graph e os três
   blocos de dados estruturados: `Service`, `FAQPage`, `BreadcrumbList`.
3. Acrescente ao `sitemap.xml`.
4. Acrescente ao `ANCORA` e ao `JUNTAR` em `ferramentas/linkagem.py`.
5. Corra o refrescador, a linkagem e a auditoria.

Estrutura que funciona, por esta ordem: migalhas, sobretítulo, H1, lead,
acções, três metas, resposta directa citável, secções de conteúdo,
barra de números quando houver números reais, o que entrego, perguntas
frequentes com schema, "Onde ir a partir daqui", fecho com CTA, caixa da
fonte preferida.

---

## 7. Integrações a funcionar

**GA4** `G-510WQZ4YQ7`. Eventos próprios: `clique_diagnostico`,
`contacto_email`, `fonte_preferida`, `diagnostico_concluido`,
`diagnostico_contacto`, `diagnostico_envio_as_cegas`.

Esse último é um alarme: dispara quando o teste de diagnóstico tem de
enviar sem conseguir ler a resposta, o que significa que a implantação do
Apps Script está a devolver erro e há pedidos a perder-se. Se aparecer
nos relatórios, é para investigar no dia.

**Calendly** `https://calendly.com/wandofi`. É a página de perfil. Se o
Mauro indicar o nome do evento, trocar pelo link directo.

**Teste de diagnóstico** em `/diagnostico/`. Envia para um Web App do
Google Apps Script que escreve numa folha do Drive do Mauro. No topo do
script da página estão `PRECOS_CONFIRMADOS`, `URL_FOLHA` e o bloco
`CONFIG` com os preços.

Regra do Apps Script que já custou duas semanas de contactos perdidos:
**guardar o script não chega**. É preciso Implantar, Gerir implantações,
lápis, Versão: Nova versão, Implantar. Senão o site continua a chamar a
versão antiga, sem aviso nenhum.

---

## 8. Onde o site está, em SEO

Medido em Setembro de 2026:

- Autoridade de domínio **4**, Trust Flow **0**, **um** IP a apontar.
- Uma única palavra no Google: "consultor seo lisboa", **posição 11**.
- Todas as outras fora do top 100. Visitas estimadas: zero.

O que isto quer dizer para quem escrever conteúdo: **com autoridade 4 não
se ganha um termo estabelecido**. As primeiras páginas das pesquisas que
interessam têm domínios entre 25 e 85.

A única alavanca que funciona neste estado é a **frescura**. Quando uma
regra muda, ninguém publicou ainda, e uma página rápida e bem estruturada
entra na primeira página a partir de um domínio fraco durante dias ou
semanas. Por isso, conteúdo noticioso e datado vale mais do que conteúdo
perene, enquanto a autoridade não subir.

Procura medida no mercado português, para não perder tempo:

| Tema | Por mês | Veredicto |
|---|---|---|
| Facturação electrónica (agrupamento) | 3 400 | **Vale a pena.** Dificuldade 13 a 23 |
| abrir empresa em portugal | 560 | Vale. CPC 4,86 €. Já existe artigo |
| consultor seo | 560 | Primeira página cheia. Difícil |
| agentes de IA, chatbots | 30 | Plantar, não colher |
| acessibilidade digital | 10 | Não existe procura |
| recibos verdes, portal das finanças | 25 400 | **Armadilha.** É navegação para o portal do Estado |

Três coisas mexem mais a agulha do que qualquer artigo, por ordem:
perfil de empresa no Google (seis das nove pesquisas seguidas mostram
Map Pack e o site está fora dele), backlinks, e a página de privacidade.

---

## 9. Por fazer

1. **`/privacidade/` não existe.** O teste de diagnóstico recolhe nome e
   email com consentimento explícito e não há para onde apontar. É risco,
   não é pendência.
2. **Perfil de empresa no Google.** Não está feito. É de graça.
3. **Arrumar `index.html` contra `index-novo.html`.** Ver 2.2.
4. **Apagar os ficheiros do tema escuro.** Ver 2.3.
5. **WhatsApp.** Bloco escrito e comentado no fim da secção de contacto da
   página inicial. Falta o número.
6. **Página do Porto.** `/seo/agencia-seo-porto/` existe e está ligada,
   mas não há cliente do Porto. Decisão do Mauro: fica com nota de
   trabalho remoto, ou sai com 301 para a de Lisboa.
7. **Multiplicadores de preço.** Proposta por aprovar: geografia só no
   SEO, volume de páginas em vez de número de pessoas, e nenhum
   multiplicador na burocracia, automações e plataformas.

---

## 10. Não faça isto sem perguntar ao Mauro

- **Nomear clientes.** VPA e BestAccount só podem ser nomeados com
  autorização escrita. A relação com a VPA é ao mesmo tempo laboral e de
  fornecedor e ainda não está arrumada por escrito. O site fala destes
  trabalhos de forma anónima, como "um escritório jurídico em Lisboa", e
  assim pode continuar sem autorização nenhuma.
- **Publicar números de clientes.** Só com acordo prévio de quem os
  fornece.
- **Publicar preços novos ou alterados.** Os que estão publicados foram
  decididos um a um.
- **Afirmações sobre funcionalidades recentes.** Verifique na fonte
  primária antes de escrever. Já foi preciso corrigir informação inflada
  que circulava sobre o Preferred Sources e sobre os ChatGPT Ads.
- **Mudar a estrutura de CSS embutido.** Ver 2.1.
- **Apagar ou reescrever páginas existentes.** Acrescentar é livre,
  remover não.

---

## 11. Verificação antes de cada push

```bash
python3 ferramentas/auditoria.py
grep -rn '—' --include=index.html . | head
grep -rnoE '\w+-(se|lo|la|los|las|lhe|lhes)\b' --include=index.html . | head
```

Se mexeu em aspecto, veja a página a 1280 px e a 390 px antes de
publicar, e confirme que `document.documentElement.scrollWidth` é igual à
largura da janela nas duas. Barra de deslocação horizontal em telemóvel é
erro, sempre.

Mensagem de commit em português, a dizer o que mudou e porquê.
