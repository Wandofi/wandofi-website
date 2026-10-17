/* Silvia Paz Beauty — comportamento da página. Sem dependências. */
(function () {
  'use strict';

  var root = document.documentElement;
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ---------- Menu hambúrguer ---------- */
  var toggle = document.querySelector('.nav__toggle');
  var list = document.getElementById('nav-lista');

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    list.classList.toggle('is-open', open);
  }

  if (toggle && list) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    list.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && list.classList.contains('is-open')) {
        setMenu(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (list.classList.contains('is-open') && !e.target.closest('.nav')) setMenu(false);
    });
  }

  /* ---------- Clique nos botões: gota de brilho a partir do ponto tocado ---------- */
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest('.btn, .icon-btn, .rede');
    if (!b || calm.matches) return;
    var r = b.getBoundingClientRect();
    b.style.setProperty('--x', (e.clientX - r.left) + 'px');
    b.style.setProperty('--y', (e.clientY - r.top) + 'px');
    b.classList.remove('is-tap');
    void b.offsetWidth; // reinicia a animação em cliques seguidos
    b.classList.add('is-tap');
  }, { passive: true });
  document.addEventListener('animationend', function (e) {
    if (e.animationName === 'sp-tap') e.target.classList.remove('is-tap');
  });

  /* Brilho do ouro do monograma: parado com «reduzir movimento» */
  /* Ouro do topo: o brilho passa uma única vez, pouco depois de a página abrir */
  var brilho = document.getElementById('brilho-hero');
  if (brilho && brilho.beginElement && !calm.matches) {
    var passar = function () { setTimeout(function () { brilho.beginElement(); }, 700); };
    if (document.readyState === 'complete') passar(); else window.addEventListener('load', passar, { once: true });
  }

  /* O filtro de relevo é pesado: o brilho só corre com o rodapé à vista */
  var ouro = document.querySelector('.rodape__mono');
  if (ouro && ouro.pauseAnimations) {
    ouro.pauseAnimations();
    if (!calm.matches && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) ouro.unpauseAnimations(); else ouro.pauseAnimations();
      }).observe(ouro);
    }
  }

  /* ---------- Intro do topo: fallback com IntersectionObserver ---------- */
  var hero = document.querySelector('.hero');
  if (hero && root.classList.contains('sp-io') && 'IntersectionObserver' in window) {
    var marks = hero.querySelectorAll('.hero__mark');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var passed = !entry.isIntersecting && entry.boundingClientRect.top < 0;
        hero.classList.toggle('is-stage-' + entry.target.dataset.stage, passed);
      });
    }, { threshold: 0 });
    marks.forEach(function (m) { io.observe(m); });
  }

  /* ---------- Agenda Google: só carrega com um URL real ---------- */
  var agenda = document.querySelector('.agenda');
  if (agenda) {
    var url = agenda.getAttribute('data-agenda') || '';
    if (/^https:\/\/calendar\.google\.com\//.test(url)) {
      var frame = agenda.querySelector('iframe');
      frame.src = url;
      frame.hidden = false;
      agenda.classList.add('is-live');
    } else {
      montarMascara(agenda.querySelector('.agenda__vazio'));
    }
  }

  /* ---------- Máscara da agenda ----------
     Enquanto não há URL real, mostra como fica a página de marcações do Google Calendar
     embebida: semana, dias, horários e o passo de confirmação. Horários fictícios,
     nenhum dado é pedido nem guardado. Desaparece quando o iframe real entra. */
  function montarMascara(box) {
    if (!box) return;
    var MESES = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
    var DIAS = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'];
    var CURTO = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
    // Horários de exemplo por dia da semana (1 = segunda ... 6 = sábado)
    var HORAS = { 1: ['09:30', '11:00', '14:30', '16:00'], 2: ['10:00', '13:30', '17:00'], 3: ['09:30', '11:00', '15:00', '16:30'],
                  4: ['11:00', '14:30'], 5: ['09:30', '10:30', '14:00', '16:00', '17:30'], 6: ['09:00', '10:30'] };

    var hoje = new Date(); hoje.setHours(0, 0, 0, 0);
    var base = new Date(hoje); base.setDate(base.getDate() + 2);
    base.setDate(base.getDate() - ((base.getDay() + 6) % 7)); // segunda-feira dessa semana
    var semana = 0;

    box.classList.add('demo');
    box.setAttribute('role', 'region');
    box.setAttribute('aria-label', 'Pré-visualização da agenda de marcações');
    box.innerHTML =
      '<p class="demo__aviso"><strong>Pré-visualização.</strong> A agenda real do Google Calendar substitui este exemplo quando for colocado o endereço [URL_AGENDA_GOOGLE]. Os horários são fictícios.</p>' +
      '<div class="demo__corpo">' +
        '<div class="demo__info">' +
          '<span class="demo__avatar" aria-hidden="true"><svg viewBox="0 0 416 506"><use href="#monograma"/></svg></span>' +
          '<p class="demo__dono">Silvia Paz Beauty</p>' +
          '<h3 class="demo__titulo">Marcação de serviço</h3>' +
          '<ul class="demo__lista">' +
            '<li><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>1 h</li>' +
            '<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6.1-6.5-11a6.5 6.5 0 0 1 13 0c0 4.9-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.3"/></svg>Avenida Canto e Castro, 7A, Amadora</li>' +
            '<li><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5.5" width="17" height="13" rx="2"/><path d="m4 7 8 6 8-6"/></svg>Confirmação por e-mail</li>' +
          '</ul>' +
        '</div>' +
        '<div class="demo__agenda">' +
          '<div class="demo__nav">' +
            '<button type="button" class="demo__seta" data-dir="-1" aria-label="Semana anterior">‹</button>' +
            '<button type="button" class="demo__seta" data-dir="1" aria-label="Semana seguinte">›</button>' +
            '<p class="demo__semana" aria-live="polite"></p>' +
            '<p class="demo__fuso">Hora de Lisboa</p>' +
          '</div>' +
          '<div class="demo__dias"></div>' +
          '<div class="demo__escolha" hidden>' +
            '<p class="demo__escolhido"></p>' +
            '<p>Na agenda real, a cliente escreve o nome e o e-mail e recebe a confirmação no e-mail.</p>' +
            '<button type="button" class="demo__voltar">Escolher outro horário</button>' +
          '</div>' +
        '</div>' +
      '</div>';

    var dias = box.querySelector('.demo__dias');
    var rotulo = box.querySelector('.demo__semana');
    var escolha = box.querySelector('.demo__escolha');
    var escolhido = box.querySelector('.demo__escolhido');
    var anterior = box.querySelector('[data-dir="-1"]');

    function desenhar() {
      var ini = new Date(base); ini.setDate(ini.getDate() + semana * 7);
      var fim = new Date(ini); fim.setDate(fim.getDate() + 5);
      rotulo.textContent = ini.getMonth() === fim.getMonth()
        ? ini.getDate() + ' a ' + fim.getDate() + ' de ' + MESES[fim.getMonth()] + ' de ' + fim.getFullYear()
        : ini.getDate() + ' de ' + MESES[ini.getMonth()] + ' a ' + fim.getDate() + ' de ' + MESES[fim.getMonth()];
      anterior.disabled = semana === 0;
      var html = '';
      for (var i = 0; i < 6; i++) {
        var d = new Date(ini); d.setDate(d.getDate() + i);
        var horas = HORAS[d.getDay()] || [];
        html += '<div class="demo__dia"><p class="demo__data"><span>' + CURTO[d.getDay()] + '</span><strong>' + d.getDate() + '</strong></p>';
        horas.forEach(function (h) {
          html += '<button type="button" class="demo__hora" data-dia="' + d.getTime() + '" data-hora="' + h + '">' + h + '</button>';
        });
        if (!horas.length) html += '<p class="demo__sem">Sem vagas</p>';
        html += '</div>';
      }
      dias.innerHTML = html;
    }

    box.addEventListener('click', function (e) {
      var seta = e.target.closest('.demo__seta');
      var hora = e.target.closest('.demo__hora');
      if (seta && !seta.disabled) { semana = Math.max(0, semana + Number(seta.dataset.dir)); desenhar(); }
      if (hora) {
        var d = new Date(Number(hora.dataset.dia));
        var h = hora.dataset.hora.split(':');
        var fimH = String(Number(h[0]) + 1).padStart(2, '0') + ':' + h[1];
        escolhido.textContent = DIAS[d.getDay()] + ', ' + d.getDate() + ' de ' + MESES[d.getMonth()] + ' · ' + hora.dataset.hora + ' a ' + fimH;
        dias.hidden = true; escolha.hidden = false;
        box.querySelector('.demo__voltar').focus();
      }
      if (e.target.closest('.demo__voltar')) { escolha.hidden = true; dias.hidden = false; }
    });

    desenhar();
  }

  /* ---------- Intro animada ----------
     A foto é o LCP e o texto alternativo. O vídeo só começa a descarregar depois
     do load, entra por cima com um fade quando já está a tocar (o primeiro
     fotograma é a própria foto) e fica parado no último fotograma. */
  var conn = navigator.connection || {};
  var img = document.querySelector('.hero__media img');

  function startIntro() {
    if (!img || calm.matches || window.scrollY > window.innerHeight) return;
    var slow = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '') || conn.effectiveType === '3g';
    var v = document.createElement('video');
    v.muted = true;
    v.defaultMuted = true;
    v.playsInline = true;
    v.setAttribute('playsinline', '');
    v.setAttribute('muted', '');
    v.setAttribute('aria-hidden', 'true');
    v.setAttribute('tabindex', '-1');
    v.disablePictureInPicture = true;
    v.preload = 'auto';
    v.className = 'hero__video';
    v.src = slow ? 'assets/video/intro-640.mp4' : 'assets/video/intro-856.mp4';
    v.addEventListener('playing', function () { v.classList.add('is-on'); }, { once: true });
    v.addEventListener('ended', function () { v.pause(); });
    v.addEventListener('error', function () { v.remove(); });
    img.parentNode.appendChild(v);
    var p = v.play();
    if (p && p.catch) p.catch(function () { v.remove(); }); // autoplay bloqueado: fica a foto
  }

  if (conn.saveData) {
    // Poupança de dados ligada: fica só a foto
  } else if (document.readyState === 'complete') {
    setTimeout(startIntro, 300);
  } else {
    window.addEventListener('load', function () { setTimeout(startIntro, 300); }, { once: true });
  }
})();
