# -*- coding: utf-8 -*-
"""As 119 pecas de texto da pagina inicial, em ingles e em frances.

A chave e a frase portuguesa exacta, tal como esta no HTML. O gerador procura
no de texto a no de texto e so troca quando a frase inteira bate certo, nunca
por pedaco: assim o "SEO" solto do formulario nunca toca no "SEO tecnico e
consultoria" do cartao.

Regras que valem nas tres linguas, porque sao da marca e nao da gramatica:
sem travessoes, sem pontos de exclamacao, frases curtas e declarativas,
numeros concretos. Nunca escrever que o Mauro e advogado: e assistente
administrativo num escritorio de advogados, com formacao em contabilidade. Os
clientes nao sao nomeados, por isso o caso continua a ser "um escritorio de
advogados em Lisboa" e nao o nome da casa.

A grafia pre-acordo e so do portugues e nao se aplica aqui.

No frances leva espaco fino inquebravel, U+202F, antes de ? ! ; e :, que e a
regra tipografica da lingua e o que distingue um texto escrito em frances de
um texto traduzido a pressa.
"""

FINO = ' '   # espaco fino inquebravel do frances

# Pecas que ficam como estao nas tres linguas: nomes proprios, numeros de
# referencia, o endereco de email e o numero de telefone.
IGUAIS = [
    'Mauro Cordeiro', '01', '02', '03', '04', 'WPM-INF-04', 'SEO',
    'geral@wandofi.pt', 'WhatsApp +351 937 733 527', 'Sprint',
]

EN = {
    # --- topo do hero
    'Consultor de projectos, Lisboa': 'Project consultant, Lisbon',
    'SEO · Sites · Automações · Lisboa': 'SEO · Websites · Automation · Lisbon',
    'Consultor de SEO que': 'An SEO consultant who',
    'constrói': 'builds',
    'o que recomenda.': 'what he recommends.',
    'SEO e project management para negócios em formação: ponho o seu negócio a aparecer no Google e monto a estrutura que aguenta o que vem a seguir. Sem agência pelo meio e sem avença obrigatória.':
        'SEO and project management for businesses being built: I get your business showing up on Google '
        'and set up the structure that holds what comes next. No agency in between and no mandatory retainer.',
    'Marcar diagnóstico': 'Book a call',
    'Ver o que faço': 'See what I do',
    '15 minutos, por videochamada. Sai da conversa com os próximos passos definidos, avance ou não comigo.':
        'Fifteen minutes, by video call. You leave with the next steps defined, whether or not you go ahead with me.',
    '+55 contactos orgânicos': '+55 organic enquiries',
    'em 3 meses para um escritório de advogados em Lisboa.': 'in 3 months for a law firm in Lisbon.',
    'Ver o caso': 'See the case',
    'Resposta em 24 horas': 'Reply within 24 hours',
    'Lisboa e remoto': 'Lisbon and remote',
    'Sem retainer obrigatório': 'No mandatory retainer',

    # --- grelha de servicos
    'O que faço': 'What I do',
    'Infraestrutura antes da escala': 'Infrastructure before scale',
    'Sete frentes. Na maior parte dos projectos entram duas ou três, nunca todas ao mesmo tempo.':
        'Seven fronts. Most projects use two or three, never all at once.',
    'SEO técnico e consultoria': 'Technical SEO and consulting',
    'Schema, canonicals, sitemaps, indexação e medição de conversão. Também entro como':
        'Schema, canonicals, sitemaps, indexing and conversion tracking. I also come in as an',
    'consultor de SEO': 'SEO consultant',
    'em projectos que já têm quem execute.': 'on projects that already have someone doing the work.',
    'Ver SEO ↗': 'See SEO ↗',
    'Criação de sites': 'Website build',
    'Sites novos, rápidos e indexáveis, feitos para durar e para o cliente conseguir gerir sozinho.':
        'New sites, fast and indexable, built to last and for the client to run on their own.',
    'Ver criação de sites ↗': 'See website build ↗',
    'Migração de sites': 'Site migration',
    'Mudar de plataforma sem perder posições, histórico nem email. Astro, Cloudflare Pages e GitHub, com MX e redireccionamentos preservados.':
        'Change platform without losing rankings, history or email. Astro, Cloudflare Pages and GitHub, '
        'with MX records and redirects preserved.',
    'Ver SEO técnico ↗': 'See technical SEO ↗',
    'Automações e integrações': 'Automation and integrations',
    'Apps Script, CRM, reconciliação bancária, fluxos documentais e agentes de IA à medida. O trabalho repetitivo que rouba horas todos os meses.':
        'Apps Script, CRM, bank reconciliation, document flows and custom AI agents. '
        'The repetitive work that takes hours every month.',
    'Ver automações ↗': 'See automation ↗',
    'Estrutura e burocracia': 'Structure and paperwork',
    'Apoio técnico e operacional, com conhecimento dos processos jurídicos e contabilísticos para identificar quando envolver advogados e contabilistas e coordenar a sua participação. Sem prestar aconselhamento jurídico ou contabilístico.':
        'Technical and operational support, with knowledge of the legal and accounting processes needed to '
        'spot when to bring in lawyers and accountants and to coordinate their part. '
        'Without providing legal or accounting advice.',
    # Esta aponta para um artigo que so existe em portugues, por isso o rotulo
    # fica em portugues e a ligacao leva hreflang. E o mesmo que o rodape
    # ingles ja faz com "Casos" e "Blog": diz-se ao leitor que vai mudar de
    # lingua, em vez de o levar la sem aviso.
    'Como abrir uma empresa ↗': 'Como abrir uma empresa ↗',
    'Plataformas e LMS': 'Platforms and LMS',
    'Áreas de cliente, escolas online em Moodle, pagamentos com Stripe e certificação.':
        'Client areas, online schools on Moodle, payments with Stripe and certification.',
    'Ver casos ↗': 'See case studies ↗',
    'Novo desde Agosto de 2026': 'New since August 2026',
    'Gestão de tráfego, incluindo anúncios no ChatGPT': 'Paid traffic, including ChatGPT ads',
    'Google Ads, Meta Ads e o canal novo: a publicidade dentro do ChatGPT, já aberta a Portugal. Na Europa não há audiências, só contexto, por isso quem decide o resultado é a medição e a página de destino.':
        'Google Ads, Meta Ads and the new channel: advertising inside ChatGPT, now open to Portugal. '
        'In Europe there are no audiences, only context, so what decides the result is the measurement '
        'and the landing page.',
    'Ver anúncios no ChatGPT ↗': 'Ver anúncios no ChatGPT ↗',
    'Ver gestão de tráfego ↗': 'See digital marketing ↗',

    # --- faixa do meio
    'Não sabe por onde começar?': 'Not sure where to start?',
    'É exactamente para isso que serve o diagnóstico. Vemos o site, a indexação e o que está a travar, e sai daqui com uma lista por ordem de prioridade.':
        'That is exactly what the call is for. We look at the site, the indexing and what is holding it '
        'back, and you leave with a list in priority order.',
    '15 minutos. Abre o calendário numa nova janela.': 'Fifteen minutes. Opens the calendar in a new window.',
    # O teste de diagnostico so existe em portugues, por isso aqui a saida e o
    # email, que serve em qualquer lingua. A forma da frase mantem-se.
    'Ainda não quer falar?': 'Not ready to talk yet?',
    'Faça o teste de 2 minutos': 'Write to geral@wandofi.pt',
    'e fique com uma estimativa.': 'and I reply within 24 hours.',

    # --- processo e diagrama
    'Processo': 'Process',
    'Do diagnóstico à entrega': 'From the call to delivery',
    'Diagnóstico': 'Diagnostic',
    'Conversa guiada e leitura dos documentos, ferramentas e bloqueios.':
        'A guided conversation and a read of the documents, tools and blockers.',
    'Priorização, implementação e coordenação dos fornecedores.':
        'Prioritisation, implementation and coordination of suppliers.',
    'Entrega': 'Delivery',
    'Sistema pronto, decisões documentadas e próximos passos claros.':
        'System ready, decisions documented and next steps clear.',
    'Ref': 'Ref',
    '· vista explodida': '· exploded view',
    'Quatro camadas · escala 1:1': 'Four layers · scale 1:1',
    'Gestão de projecto': 'Project management',
    'Fornecedores, prazos e decisões coordenados por uma pessoa.':
        'Suppliers, deadlines and decisions coordinated by one person.',
    'Marca e presença': 'Brand and presence',
    'Site, SEO, anúncios e materiais a dizer a mesma coisa.':
        'Site, SEO, ads and materials all saying the same thing.',
    'Sistemas': 'Systems',
    'Ferramentas ligadas, automações e fluxos documentais.':
        'Tools connected, automation and document flows.',
    'Estrutura': 'Structure',
    'Forma jurídica, registos, contabilidade e contratos no sítio.':
        'Legal form, registrations, accounting and contracts in place.',
    'A infraestrutura de um negócio pequeno, por camadas. Cada projecto monta ou arruma uma delas; o diagnóstico diz qual vem primeiro.':
        'The infrastructure of a small business, in layers. Each project builds or tidies one of them; '
        'the call says which comes first.',
    'Três passos. Sem retainer obrigatório, sem propostas longas.':
        'Three steps. No mandatory retainer, no long proposals.',

    # --- bloco de ligacoes
    'Gestão de tráfego': 'Digital marketing',
    'SEO por sector': 'SEO by sector',
    'Casos': 'Case studies',
    'Sobre': 'About',
    'Contactos': 'Contactos',

    # --- sobre
    'Construído por dentro, não estudado por fora': 'Built from the inside, not studied from the outside',
    'A Wandofi PM é a actividade de project management de Mauro Cordeiro, com implementação de sites e automações. Baseada em Lisboa, trabalha remotamente para Portugal. Um consultor com capacidade para gerir o projecto completo, da estratégia à implementação e à coordenação de fornecedores. Presta apoio técnico e operacional, não aconselhamento jurídico ou contabilístico.':
        'Wandofi PM is the project management practice of Mauro Cordeiro, with website and automation '
        'implementation. Based in Lisbon, working remotely across Portugal. One consultant able to run the '
        'whole project, from strategy to implementation and supplier coordination. Technical and '
        'operational support, not legal or accounting advice.',

    # --- perguntas frequentes
    'Antes de marcar': 'Before you book',
    'Perguntas frequentes': 'Frequently asked questions',
    'Quanto custa trabalhar consigo?': 'What does it cost to work with you?',
    'O diagnóstico é uma conversa de 15 minutos e serve para perceber o que faz falta. O orçamento vem depois, fechado e por projecto, sem retainer obrigatório e sem propostas de vinte páginas.':
        'The call is fifteen minutes and is there to work out what is needed. The quote comes after, fixed '
        'and per project, with no mandatory retainer and no twenty page proposals.',
    'Em quanto tempo vejo resultados de SEO?': 'How long until I see SEO results?',
    'Correcções técnicas e de indexação podem aparecer em semanas. Ganhos de posição em pesquisas com concorrência levam tipicamente três a seis meses. Quem prometer primeira página em trinta dias está a vender outra coisa.':
        'Technical and indexing fixes can show in weeks. Position gains on competitive searches typically '
        'take three to six months. Anyone promising first page in thirty days is selling something else.',
    'O que precisa de mim para começar?': 'What do you need from me to start?',
    'Acesso de leitura ao Google Analytics e ao Search Console, se existirem, e acesso ao site. Se não existir nada montado, isso passa a ser o primeiro ponto do plano.':
        'Read access to Google Analytics and Search Console, if they exist, and access to the site. '
        'If nothing is set up, that becomes the first item in the plan.',

    # --- fecho
    'Vamos ver o que está a travar o seu site': 'Let us see what is holding your site back',
    'Migração, rebuild, SEO, automação ou estrutura de raiz. Começa sempre pela mesma conversa de 15 minutos.':
        'Migration, rebuild, SEO, automation or structure from scratch. It always starts with the same '
        'fifteen minute conversation.',
    'Se preferir trabalhar em inglês ou em francês, comece por':
        'If you would rather work in Portuguese or in French, start at',
    'SEO in English': 'Wandofi PM em português',
    'ou por': 'or at',
    'Consultant SEO à Lisbonne': 'Consultant SEO à Lisbonne',
    'Prefere escrever? WhatsApp ou email, chega ao mesmo sítio e respondo em 24 horas.':
        'Prefer to write? WhatsApp or email reach the same place, and I reply within 24 hours.',

    # --- a hora paga
    'Revisão de projecto, uma hora': 'Project review, one hour',
    '80 € a hora, sempre paga.': '80 € an hour, always paid.',
    'É diferente do diagnóstico: aqui olho ao detalhe para o que já existe e sai de lá com a lista do que corrigir, por ordem. Peça por email ou por WhatsApp e combinamos a hora. Na resposta digo se acresce IVA.':
        'Different from the free call: here I go through what already exists in detail and you leave with '
        'the list of what to fix, in order. Ask by email or WhatsApp and we set the time. '
        'I confirm in the reply whether VAT is added.',
    'Pedir por email': 'Ask by email',
    'Pedir por WhatsApp': 'Ask on WhatsApp',

    # --- formulario
    'Ou escreva aqui o essencial': 'Or write the essentials here',
    'Respondo em 24 horas com uma proposta de hora. Sem compromisso e sem lista de envio.':
        'I reply within 24 hours with a time to suit you. No commitment and no mailing list.',
    'Nome': 'Name',
    'Negócio e site actual': 'Business and current site',
    'O que precisa': 'What you need',
    'Site': 'Website',
    'Automações': 'Automation',
    'Email ou WhatsApp': 'Email or WhatsApp',
    'Autorizo o contacto por email ou WhatsApp sobre este pedido.':
        'I agree to be contacted by email or WhatsApp about this request.',
    'Política de privacidade': 'Política de privacidade',
    'Não preencher': 'Do not fill in',
    'Pedir diagnóstico': 'Request a call',
    'Os dados servem só para lhe responder.': 'The data is only used to reply to you.',
}

FR = {
    'Consultor de projectos, Lisboa': 'Consultant en projets, Lisbonne',
    'SEO · Sites · Automações · Lisboa': 'SEO · Sites · Automatisation · Lisbonne',
    'Consultor de SEO que': 'Un consultant SEO qui',
    'constrói': 'construit',
    'o que recomenda.': 'ce qu’il recommande.',
    'SEO e project management para negócios em formação: ponho o seu negócio a aparecer no Google e monto a estrutura que aguenta o que vem a seguir. Sem agência pelo meio e sem avença obrigatória.':
        'SEO et gestion de projet pour les entreprises en construction' + FINO + ': je fais apparaître votre '
        'entreprise sur Google et je monte la structure qui tiendra la suite. Sans agence au milieu et '
        'sans forfait obligatoire.',
    'Marcar diagnóstico': 'Prendre rendez-vous',
    'Ver o que faço': 'Voir ce que je fais',
    '15 minutos, por videochamada. Sai da conversa com os próximos passos definidos, avance ou não comigo.':
        'Quinze minutes, en visioconférence. Vous repartez avec les prochaines étapes définies, '
        'que vous continuiez avec moi ou non.',
    '+55 contactos orgânicos': '+55 contacts organiques',
    'em 3 meses para um escritório de advogados em Lisboa.': 'en 3 mois pour un cabinet d’avocats à Lisbonne.',
    'Ver o caso': 'Voir le cas',
    'Resposta em 24 horas': 'Réponse sous 24 heures',
    'Lisboa e remoto': 'Lisbonne et à distance',
    'Sem retainer obrigatório': 'Sans forfait obligatoire',

    'O que faço': 'Ce que je fais',
    'Infraestrutura antes da escala': 'L’infrastructure avant l’échelle',
    'Sete frentes. Na maior parte dos projectos entram duas ou três, nunca todas ao mesmo tempo.':
        'Sept fronts. Dans la plupart des projets il y en a deux ou trois, jamais tous en même temps.',
    'SEO técnico e consultoria': 'SEO technique et conseil',
    'Schema, canonicals, sitemaps, indexação e medição de conversão. Também entro como':
        'Schema, canonicals, sitemaps, indexation et mesure des conversions. J’interviens aussi comme',
    'consultor de SEO': 'consultant SEO',
    'em projectos que já têm quem execute.': 'sur des projets qui ont déjà quelqu’un pour exécuter.',
    'Ver SEO ↗': 'Voir le SEO ↗',
    'Criação de sites': 'Création de sites',
    'Sites novos, rápidos e indexáveis, feitos para durar e para o cliente conseguir gerir sozinho.':
        'Des sites neufs, rapides et indexables, faits pour durer et pour que le client les gère seul.',
    'Ver criação de sites ↗': 'Voir la création de sites ↗',
    'Migração de sites': 'Migration de sites',
    'Mudar de plataforma sem perder posições, histórico nem email. Astro, Cloudflare Pages e GitHub, com MX e redireccionamentos preservados.':
        'Changer de plateforme sans perdre les positions, l’historique ni le courriel. Astro, '
        'Cloudflare Pages et GitHub, avec les MX et les redirections préservés.',
    'Ver SEO técnico ↗': 'Voir le SEO technique ↗',
    'Automações e integrações': 'Automatisation et intégrations',
    'Apps Script, CRM, reconciliação bancária, fluxos documentais e agentes de IA à medida. O trabalho repetitivo que rouba horas todos os meses.':
        'Apps Script, CRM, rapprochement bancaire, flux documentaires et agents d’IA sur mesure. '
        'Le travail répétitif qui prend des heures tous les mois.',
    'Ver automações ↗': 'Voir l’automatisation ↗',
    'Estrutura e burocracia': 'Structure et démarches',
    'Apoio técnico e operacional, com conhecimento dos processos jurídicos e contabilísticos para identificar quando envolver advogados e contabilistas e coordenar a sua participação. Sem prestar aconselhamento jurídico ou contabilístico.':
        'Appui technique et opérationnel, avec la connaissance des processus juridiques et comptables '
        'pour repérer quand faire intervenir avocats et comptables et coordonner leur part. '
        'Sans fournir de conseil juridique ni comptable.',
    'Como abrir uma empresa ↗': 'Como abrir uma empresa ↗',
    'Plataformas e LMS': 'Plateformes et LMS',
    'Áreas de cliente, escolas online em Moodle, pagamentos com Stripe e certificação.':
        'Espaces client, écoles en ligne sur Moodle, paiements avec Stripe et certification.',
    'Ver casos ↗': 'Voir les références ↗',
    'Novo desde Agosto de 2026': 'Nouveau depuis août 2026',
    'Gestão de tráfego, incluindo anúncios no ChatGPT': 'Publicité en ligne, y compris les annonces dans ChatGPT',
    'Google Ads, Meta Ads e o canal novo: a publicidade dentro do ChatGPT, já aberta a Portugal. Na Europa não há audiências, só contexto, por isso quem decide o resultado é a medição e a página de destino.':
        'Google Ads, Meta Ads et le nouveau canal' + FINO + ': la publicité dans ChatGPT, désormais ouverte '
        'au Portugal. En Europe il n’y a pas d’audiences, seulement du contexte, donc ce qui décide du '
        'résultat est la mesure et la page de destination.',
    'Ver anúncios no ChatGPT ↗': 'Ver anúncios no ChatGPT ↗',
    'Ver gestão de tráfego ↗': 'Voir la publicité en ligne ↗',

    'Não sabe por onde começar?': 'Vous ne savez pas par où commencer' + FINO + '?',
    'É exactamente para isso que serve o diagnóstico. Vemos o site, a indexação e o que está a travar, e sai daqui com uma lista por ordem de prioridade.':
        'C’est exactement à cela que sert l’entretien. Nous regardons le site, l’indexation et ce qui '
        'bloque, et vous repartez avec une liste par ordre de priorité.',
    '15 minutos. Abre o calendário numa nova janela.': 'Quinze minutes. Ouvre le calendrier dans une nouvelle fenêtre.',
    'Ainda não quer falar?': 'Vous préférez ne pas encore parler' + FINO + '?',
    'Faça o teste de 2 minutos': 'Écrivez à geral@wandofi.pt',
    'e fique com uma estimativa.': 'et je réponds sous 24 heures.',

    'Processo': 'Processus',
    'Do diagnóstico à entrega': 'De l’entretien à la livraison',
    'Diagnóstico': 'Diagnostic',
    'Conversa guiada e leitura dos documentos, ferramentas e bloqueios.':
        'Un entretien guidé et une lecture des documents, des outils et des blocages.',
    'Priorização, implementação e coordenação dos fornecedores.':
        'Priorisation, mise en œuvre et coordination des prestataires.',
    'Entrega': 'Livraison',
    'Sistema pronto, decisões documentadas e próximos passos claros.':
        'Système prêt, décisions documentées et prochaines étapes claires.',
    'Ref': 'Réf',
    '· vista explodida': '· vue éclatée',
    'Quatro camadas · escala 1:1': 'Quatre couches · échelle 1:1',
    'Gestão de projecto': 'Gestion de projet',
    'Fornecedores, prazos e decisões coordenados por uma pessoa.':
        'Prestataires, délais et décisions coordonnés par une seule personne.',
    'Marca e presença': 'Marque et présence',
    'Site, SEO, anúncios e materiais a dizer a mesma coisa.':
        'Site, SEO, annonces et supports qui disent la même chose.',
    'Sistemas': 'Systèmes',
    'Ferramentas ligadas, automações e fluxos documentais.':
        'Outils reliés, automatisation et flux documentaires.',
    'Estrutura': 'Structure',
    'Forma jurídica, registos, contabilidade e contratos no sítio.':
        'Forme juridique, immatriculations, comptabilité et contrats en place.',
    'A infraestrutura de um negócio pequeno, por camadas. Cada projecto monta ou arruma uma delas; o diagnóstico diz qual vem primeiro.':
        'L’infrastructure d’une petite entreprise, par couches. Chaque projet en monte ou en range une'
        + FINO + '; l’entretien dit laquelle vient en premier.',
    'Três passos. Sem retainer obrigatório, sem propostas longas.':
        'Trois étapes. Sans forfait obligatoire, sans longues propositions.',

    'Gestão de tráfego': 'Publicité en ligne',
    'SEO por sector': 'SEO par secteur',
    'Casos': 'Références',
    'Sobre': 'À propos',
    'Contactos': 'Contactos',

    'Construído por dentro, não estudado por fora': 'Construit de l’intérieur, pas étudié de l’extérieur',
    'A Wandofi PM é a actividade de project management de Mauro Cordeiro, com implementação de sites e automações. Baseada em Lisboa, trabalha remotamente para Portugal. Um consultor com capacidade para gerir o projecto completo, da estratégia à implementação e à coordenação de fornecedores. Presta apoio técnico e operacional, não aconselhamento jurídico ou contabilístico.':
        'Wandofi PM est l’activité de gestion de projet de Mauro Cordeiro, avec la mise en œuvre de sites '
        'et d’automatisations. Basée à Lisbonne, elle travaille à distance pour tout le Portugal. '
        'Un consultant capable de mener le projet complet, de la stratégie à la mise en œuvre et à la '
        'coordination des prestataires. Appui technique et opérationnel, pas de conseil juridique '
        'ni comptable.',

    'Antes de marcar': 'Avant de réserver',
    'Perguntas frequentes': 'Questions fréquentes',
    'Quanto custa trabalhar consigo?': 'Combien coûte de travailler avec vous' + FINO + '?',
    'O diagnóstico é uma conversa de 15 minutos e serve para perceber o que faz falta. O orçamento vem depois, fechado e por projecto, sem retainer obrigatório e sem propostas de vinte páginas.':
        'L’entretien dure quinze minutes et sert à comprendre ce qu’il faut. Le devis vient après, fermé '
        'et par projet, sans forfait obligatoire et sans propositions de vingt pages.',
    'Em quanto tempo vejo resultados de SEO?': 'En combien de temps vois-je des résultats SEO' + FINO + '?',
    'Correcções técnicas e de indexação podem aparecer em semanas. Ganhos de posição em pesquisas com concorrência levam tipicamente três a seis meses. Quem prometer primeira página em trinta dias está a vender outra coisa.':
        'Les corrections techniques et d’indexation peuvent apparaître en quelques semaines. Les gains de '
        'position sur des recherches concurrentielles prennent en général trois à six mois. Qui promet la '
        'première page en trente jours vend autre chose.',
    'O que precisa de mim para começar?': 'Que vous faut-il de ma part pour commencer' + FINO + '?',
    'Acesso de leitura ao Google Analytics e ao Search Console, se existirem, e acesso ao site. Se não existir nada montado, isso passa a ser o primeiro ponto do plano.':
        'Un accès en lecture à Google Analytics et à la Search Console, s’ils existent, et l’accès au site. '
        'S’il n’y a rien en place, cela devient le premier point du plan.',

    'Vamos ver o que está a travar o seu site': 'Voyons ce qui bloque votre site',
    'Migração, rebuild, SEO, automação ou estrutura de raiz. Começa sempre pela mesma conversa de 15 minutos.':
        'Migration, refonte, SEO, automatisation ou structure de zéro. Cela commence toujours par le même '
        'entretien de quinze minutes.',
    'Se preferir trabalhar em inglês ou em francês, comece por':
        'Si vous préférez travailler en anglais ou en portugais, commencez par',
    'SEO in English': 'SEO in English',
    'ou por': 'ou par',
    'Consultant SEO à Lisbonne': 'Wandofi PM em português',
    'Prefere escrever? WhatsApp ou email, chega ao mesmo sítio e respondo em 24 horas.':
        'Vous préférez écrire' + FINO + '? WhatsApp et le courriel arrivent au même endroit, '
        'et je réponds sous 24 heures.',

    'Revisão de projecto, uma hora': 'Revue de projet, une heure',
    '80 € a hora, sempre paga.': '80 € l’heure, toujours payante.',
    'É diferente do diagnóstico: aqui olho ao detalhe para o que já existe e sai de lá com a lista do que corrigir, por ordem. Peça por email ou por WhatsApp e combinamos a hora. Na resposta digo se acresce IVA.':
        'Ce n’est pas le diagnostic' + FINO + ': ici je regarde en détail ce qui existe déjà et vous '
        'repartez avec la liste de ce qu’il faut corriger, dans l’ordre. Demandez par courriel ou par '
        'WhatsApp et on fixe l’heure. Je confirme dans la réponse si la TVA s’ajoute.',
    'Pedir por email': 'Demander par courriel',
    'Pedir por WhatsApp': 'Demander par WhatsApp',

    'Ou escreva aqui o essencial': 'Ou écrivez ici l’essentiel',
    'Respondo em 24 horas com uma proposta de hora. Sem compromisso e sem lista de envio.':
        'Je réponds sous 24 heures avec une proposition d’horaire. Sans engagement et sans liste de diffusion.',
    'Nome': 'Nom',
    'Negócio e site actual': 'Activité et site actuel',
    'O que precisa': 'Ce qu’il vous faut',
    'Site': 'Site',
    'Automações': 'Automatisation',
    'Email ou WhatsApp': 'Courriel ou WhatsApp',
    'Autorizo o contacto por email ou WhatsApp sobre este pedido.':
        'J’autorise le contact par courriel ou WhatsApp au sujet de cette demande.',
    'Política de privacidade': 'Política de privacidade',
    'Não preencher': 'Ne pas remplir',
    'Pedir diagnóstico': 'Demander un rendez-vous',
    'Os dados servem só para lhe responder.': 'Les données servent uniquement à vous répondre.',
}

# --- atributos que a pessoa le ------------------------------------------
# Texto que o visitante le mas que vive num atributo. O traduz() so olha para o
# que esta entre > e <, por isso isto tem de vir a mao. As tres cotas dos
# passos do processo (data-cota) estiveram em portugues nas iniciais inglesa e
# francesa ate 16/11/2026, sem nada se queixar, porque faltavam aqui.
ATRIBUTOS = {
    'en': {
        'O seu nome': 'Your name',
        'Barbearia em Alvalade, sem site': 'Barber shop in Alvalade, no website',
        'Onde lhe respondo': 'Where I reply to you',
        '15 min · videochamada': '15 min · video call',
        '2 a 8 semanas': '2 to 8 weeks',
        'documentado · sem retainer': 'documented · no retainer',
    },
    'fr': {
        'O seu nome': 'Votre nom',
        'Barbearia em Alvalade, sem site': 'Salon de coiffure à Alvalade, sans site',
        'Onde lhe respondo': 'Où je vous réponds',
        '15 min · videochamada': '15 min · visioconférence',
        '2 a 8 semanas': '2 à 8 semaines',
        'documentado · sem retainer': 'documenté · sans forfait',
    },
}

# --- frases que vivem dentro do guiao da inicial -------------------------
# Sao as que a pessoa ve quando o formulario responde. As chaves do que e
# enviado para a folha ficam em portugues de proposito: a folha e do Mauro e
# tem de se ler num vocabulario so.
GUIAO = {
    'en': {
        'Falta o nome.': 'Your name is missing.',
        'Falta o email ou o WhatsApp.': 'The email or WhatsApp is missing.',
        'Falta a autorização de contacto.': 'The contact permission is missing.',
        'Recebido.': 'Received.',
        'Respondo em 24 horas. Se for mais urgente, o WhatsApp é o caminho mais rápido.':
            'I reply within 24 hours. If it is more urgent, WhatsApp is the fastest way.',
        'A enviar...': 'Sending...',
        'Olá, vim do site da Wandofi. Nome: ': 'Hello, I came from the Wandofi site. Name: ',
        '. Negócio: ': '. Business: ',
        '. Preciso de: ': '. I need: ',
        'não indicado': 'not given',
        'Não consegui enviar daqui. ': 'I could not send from here. ',
        'Enviar o mesmo por WhatsApp': 'Send the same on WhatsApp',
        '"directo"': '"direct"',
        # Tem de ser a linha inteira. A primeira versao trocava so "inicial" e
        # apanhava tambem o classList.contains("inicial") que liga o guiao: a
        # condicao passava a procurar uma classe que nao existe, o guiao saia
        # logo na primeira linha e a vitrine ficava vazia nas duas linguas.
        'origem: "inicial"': 'origem: "inicial-en"',
    },
    'fr': {
        'Falta o nome.': 'Il manque le nom.',
        'Falta o email ou o WhatsApp.': 'Il manque le courriel ou le WhatsApp.',
        'Falta a autorização de contacto.': 'Il manque l’autorisation de contact.',
        'Recebido.': 'Bien reçu.',
        'Respondo em 24 horas. Se for mais urgente, o WhatsApp é o caminho mais rápido.':
            'Je réponds sous 24 heures. Si c’est plus urgent, le WhatsApp est le chemin le plus rapide.',
        'A enviar...': 'Envoi en cours...',
        'Olá, vim do site da Wandofi. Nome: ': 'Bonjour, je viens du site Wandofi. Nom: ',
        '. Negócio: ': '. Activité: ',
        '. Preciso de: ': '. J’ai besoin de: ',
        'não indicado': 'non indiqué',
        'Não consegui enviar daqui. ': 'Je n’ai pas pu envoyer d’ici. ',
        'Enviar o mesmo por WhatsApp': 'Envoyer la même chose par WhatsApp',
        '"directo"': '"direct"',
        'origem: "inicial"': 'origem: "inicial-fr"',
    },
}

# --- para onde aponta cada ligacao de dentro do <main> -------------------
# O que nao tem par na lingua fica a apontar para a pagina portuguesa, e o
# gerador marca-a com hreflang e lang para o leitor saber que muda de lingua.
# E o mesmo que o rodape ingles ja faz.
LIGACOES = {
    'en': {
        '/casos/': '/en/case-studies/',
        '/seo/': '/en/seo-consultant-lisbon/',
        '/seo/consultor-seo/': '/en/seo-consultant-lisbon/',
        '/seo/seo-tecnico/': '/en/seo-consultant-lisbon/',
        '/seo/sectores/': '/en/seo-consultant-lisbon/',
        '/criacao-de-sites/': '/en/websites/',
        '/automacoes/': '/en/automation/',
        '/sobre/': '/en/about/',
        '/gestao-de-trafego/': '/en/digital-marketing-lisbon/',
        '/diagnostico/': 'mailto:geral@wandofi.pt',
        '/en/': '/',
    },
    'fr': {
        '/casos/': '/fr/references/',
        '/seo/': '/fr/seo/',
        '/seo/consultor-seo/': '/fr/seo/',
        '/seo/seo-tecnico/': '/fr/seo/',
        '/seo/sectores/': '/fr/seo/',
        '/criacao-de-sites/': '/fr/sites-web/',
        '/automacoes/': '/fr/automatisation/',
        '/sobre/': '/fr/a-propos/',
        '/gestao-de-trafego/': '/fr/publicite-en-ligne/',
        '/diagnostico/': 'mailto:geral@wandofi.pt',
        '/fr/': '/',
    },
}

# Ligacoes que ficam a apontar para portugues de propósito, e por isso levam
# hreflang="pt-PT" lang="pt-PT".
EM_PORTUGUES = [
    '/blog/como-abrir-uma-empresa-em-portugal/',
    '/gestao-de-trafego/chatgpt-ads/',
    '/contactos/',
    '/privacidade/',
    '/',
]

# --- cabeca ---------------------------------------------------------------
CABECA = {
    'en': {
        'lang': 'en',
        'locale': 'en_GB',
        'title': 'SEO Consultant and Project Manager in Lisbon | Wandofi PM',
        'description': 'SEO consultant and project manager in Lisbon. Technical SEO, website builds and '
                       'migrations, and automation for businesses that need to show up on Google. '
                       'A fifteen minute call to start.',
        'og_description': 'Technical SEO, websites and automation for businesses in Portugal. '
                          'A fifteen minute call, no mandatory retainer.',
        'canonical': 'https://wandofi.pt/en/',
        'jobTitle': 'SEO Consultant and Project Manager',
        'ld_description': 'SEO consultant in Lisbon. Technical SEO, website builds and migrations, '
                          'and automation for businesses in Portugal.',
        'knowsAbout': ['Technical SEO', 'SEO consulting', 'Site migration', 'Process automation',
                       'LMS', 'Business structure'],
        'serviceType': ['SEO consulting', 'Technical SEO', 'Website build', 'Site migration',
                        'Automation and integrations', 'Structure and paperwork', 'Platforms and LMS'],
    },
    'fr': {
        'lang': 'fr',
        'locale': 'fr_FR',
        'title': 'Consultant SEO et chef de projet à Lisbonne | Wandofi PM',
        'description': 'Consultant SEO et chef de projet à Lisbonne. SEO technique, création et migration '
                       'de sites, et automatisation pour les entreprises qui doivent apparaître sur '
                       'Google. Un entretien de quinze minutes pour commencer.',
        'og_description': 'SEO technique, sites et automatisation pour les entreprises au Portugal. '
                          'Un entretien de quinze minutes, sans forfait obligatoire.',
        'canonical': 'https://wandofi.pt/fr/',
        'jobTitle': 'Consultant SEO et chef de projet',
        'ld_description': 'Consultant SEO à Lisbonne. SEO technique, création et migration de sites, '
                          'et automatisation pour les entreprises au Portugal.',
        'knowsAbout': ['SEO technique', 'Conseil SEO', 'Migration de sites', 'Automatisation des processus',
                       'LMS', 'Structure d’entreprise'],
        'serviceType': ['Conseil SEO', 'SEO technique', 'Création de sites', 'Migration de sites',
                        'Automatisation et intégrations', 'Structure et démarches', 'Plateformes et LMS'],
    },
}
