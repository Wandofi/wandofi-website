// Hive Group: interacções da demonstração (menu, revelações, colmeia em profundidade, ano trimestral, marcação, filtros).
(() => {
  const lang = document.documentElement.lang.startsWith("pt") ? "pt" : "en";
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  // Menu móvel
  const btn = document.querySelector(".menu-btn");
  const mnav = document.getElementById("mobile-nav");
  if (btn && mnav) {
    const label = btn.querySelector("span");
    const set = (open) => {
      btn.setAttribute("aria-expanded", String(open));
      mnav.classList.toggle("is-open", open);
      label.textContent = open ? btn.dataset.close : btn.dataset.open;
    };
    btn.addEventListener("click", () => {
      const open = btn.getAttribute("aria-expanded") !== "true";
      set(open);
      if (open) mnav.querySelector("a")?.focus();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { set(false); btn.focus(); }
    });
  }

  // Revelação ao entrar no ecrã
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce.matches) {
    const io = new IntersectionObserver((entries) => {
      for (const en of entries) if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else reveals.forEach((el) => el.classList.add("is-in"));

  const hero = null;
  if (hero && !reduce.matches) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const y = Math.min(window.scrollY, hero.offsetHeight * 1.2);
      hero.style.setProperty("--hp", y.toFixed(1));
    };
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  }

  // Artefactos da marca nos fundos: cada camada desloca-se à sua profundidade
  const artSections = [...document.querySelectorAll(".has-art")];
  if (artSections.length && !reduce.matches) {
    let ticking = false;
    const update = () => {
      ticking = false;
      const vh = window.innerHeight;
      for (const s of artSections) {
        const r = s.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) continue;
        s.style.setProperty("--sy", ((r.top + r.height / 2 - vh / 2) * 0.5).toFixed(1));
      }
    };
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  // Scroll-craft (só na home): acto do ano, assinatura no símbolo e arranque do motor
  const scRoot = document.getElementById("conteudo");
  if (window.ScrollCraft && document.querySelector("[data-sc-act]")) {
    const small = window.matchMedia("(max-width: 999px), (max-height: 699px)").matches;
    // Sem movimento ou em ecrã pequeno, o hero não fixa: composição estática completa, sem scroll vazio
    if (reduce.matches || small) document.querySelectorAll("[data-hero-pin]").forEach((el) => el.removeAttribute("data-sc-act"));
    if (reduce.matches) document.querySelectorAll('[data-sc-act="pin"]').forEach((el) => el.removeAttribute("data-sc-act"));
    const api = window.ScrollCraft.mount(scRoot);

    // Uma vez só: quando um acto fixo sai por cima do ecrã, deixa de estar fixo e assenta.
    // Ao voltar para cima já não repete nem obriga a atravessar o espaço fixo.
    if (!reduce.matches && api && api.acts) {
      const html = document.documentElement;
      html.style.overflowAnchor = "none"; // compensamos o scroll à mão, sem ajuda do browser
      const pending = api.acts.filter((a) => a.pinned);
      let ticking = false;
      const settle = () => {
        ticking = false;
        let changed = false;
        for (let i = pending.length - 1; i >= 0; i--) {
          const a = pending[i];
          const r = a.el.getBoundingClientRect();
          if (r.bottom > 0) continue; // ainda não saiu por cima
          const oldH = a.el.offsetHeight;
          a.pinned = false;
          a.el.style.height = "";
          a.el.classList.remove("sc-act--pinned");
          a.el.classList.add("sc-done");
          const newH = a.el.offsetHeight;
          window.scrollBy({ top: newH - oldH, behavior: "instant" });
          pending.splice(i, 1);
          changed = true;
        }
        if (changed) { api.layout(); window.dispatchEvent(new Event("hive:settled")); }
      };
      window.addEventListener("scroll", () => { if (!ticking && pending.length) { ticking = true; requestAnimationFrame(settle); } }, { passive: true });

      // Secções em fluxo com animação ligada ao scroll: ficam no estado final depois de vistas
      document.querySelectorAll(".team[data-sc-act], .close[data-sc-act]").forEach((el) => {
        const io = new IntersectionObserver((en) => {
          if (en[0].intersectionRatio >= 0.55) { setTimeout(() => el.classList.add("sc-done"), 900); io.disconnect(); }
        }, { threshold: [0, 0.55] });
        io.observe(el);
      });
    }
  }

  // O ano: meses e trimestres a partir do progresso do acto fixo
  document.querySelectorAll("[data-year]").forEach((dial) => {
    const act = dial.closest("[data-sc-act]") || dial.closest("section");
    const names = JSON.parse(dial.dataset.year);
    const months = dial.querySelectorAll(".months span");
    const qs = dial.querySelectorAll(".qs li");
    const num = dial.querySelector(".yr-num");
    const name = dial.querySelector(".yr-name");
    let last = -1;
    const paint = (m) => {
      if (m === last) return;
      last = m;
      months.forEach((s, i) => s.classList.toggle("is-on", i < m));
      qs.forEach((q, i) => q.classList.toggle("is-on", i < Math.floor(m / 3)));
      const shown = Math.max(1, m);
      num.textContent = String(shown).padStart(2, "0");
      name.textContent = names[shown - 1];
    };
    if (reduce.matches || !act.classList.contains("sc-act--pinned")) { paint(12); return; }
    let ticking = false;
    const update = () => {
      ticking = false;
      if (act.classList.contains("sc-done")) { paint(12); return; }
      const r = act.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - window.innerHeight)));
      paint(Math.min(12, Math.floor(p * 12.99)));
    };
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  });

  // Assinatura: as barras do símbolo enchem-se com o ano (progresso da página)
  if (document.querySelector(".logo-bars")) {
    const root = document.documentElement;
    if (reduce.matches) { ["--yb1", "--yb2", "--yb3"].forEach((v) => root.style.setProperty(v, "1")); }
    else {
      let ticking = false, done = false, best = 0;
      const update = () => {
        ticking = false;
        best = Math.max(best, Math.min(1, window.scrollY / Math.max(1, root.scrollHeight - window.innerHeight)));
        const f = best;
        [0, 1, 2].forEach((i) => root.style.setProperty(`--yb${i + 1}`, Math.min(1, Math.max(0, f * 4 - i)).toFixed(3)));
        const complete = f > 0.985;
        if (complete !== done) { done = complete; root.classList.toggle("year-complete", complete); }
      };
      window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
      update();
    }
  }

  // Filtros dos insights
  document.querySelectorAll("[data-filters]").forEach((bar) => {
    const posts = document.querySelectorAll("[data-cat]");
    const count = document.querySelector("[data-filter-count]");
    bar.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      bar.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      let n = 0;
      posts.forEach((p) => { const show = b.dataset.f === "all" || p.dataset.cat === b.dataset.f; p.hidden = !show; if (show) n++; });
      if (count) count.textContent = lang === "pt" ? `${n} ${n === 1 ? "artigo" : "artigos"}` : `${n} ${n === 1 ? "article" : "articles"}`;
    });
  });

  // Marcação: calendário em Europe/Lisbon, dias úteis, do dia útil seguinte e durante seis semanas
  const MONTHS = {
    pt: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
    en: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
  };
  const SHORT = { pt: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"], en: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] };
  const DAYS = { pt: ["Seg", "Ter", "Qua", "Qui", "Sex"], en: ["Mon", "Tue", "Wed", "Thu", "Fri"] };
  const LONGDAYS = { pt: ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"], en: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] };

  function lisbonToday() {
    const s = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());
    const [y, m, d] = s.split("-").map(Number);
    return new Date(Date.UTC(y, m - 1, d));
  }
  const addDays = (d, n) => new Date(d.getTime() + n * 86400000);
  const iso = (d) => d.toISOString().slice(0, 10);
  const isWeekend = (d) => d.getUTCDay() === 0 || d.getUTCDay() === 6;
  const longLabel = (d) => lang === "pt"
    ? `${LONGDAYS.pt[d.getUTCDay() - 1]}, ${d.getUTCDate()} de ${MONTHS.pt[d.getUTCMonth()]}`
    : `${LONGDAYS.en[d.getUTCDay() - 1]} ${d.getUTCDate()} ${MONTHS.en[d.getUTCMonth()]}`;

  // Exposto para verificação automática
  window.hiveSlots = function () {
    let start = addDays(lisbonToday(), 1);
    while (isWeekend(start)) start = addDays(start, 1);
    const end = addDays(start, 42); // exclusivo: seis semanas a partir do primeiro dia útil
    const dates = [];
    for (let d = start; d < end; d = addDays(d, 1)) if (!isWeekend(d)) dates.push(d);
    const times = [];
    for (let m = 9 * 60; m <= 17 * 60 + 30; m += 30) times.push(`${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`);
    return { dates, times };
  };

  document.querySelectorAll("form[data-booking]").forEach((form, fi) => {
    const wrap = form.parentElement;
    const cal = form.querySelector("[data-cal]");
    const range = form.querySelector("[data-cal-range]");
    const hora = form.querySelector('select[name="hora"]');
    const { dates, times } = window.hiveSlots();
    const allowed = new Set(dates.map(iso));

    // Pré-selecção da área por ?area=
    const qa = new URLSearchParams(location.search).get("area");
    const areaSel = form.querySelector('select[name="area"]');
    if (qa && areaSel && [...areaSel.options].some((o) => o.value === qa)) areaSel.value = qa;

    // Grelha: linhas por semana, colunas Seg a Sex
    const head = `<div class="cal-head" aria-hidden="true">${DAYS[lang].map((d) => `<span>${d}</span>`).join("")}</div>`;
    const rows = [];
    let row = [];
    const first = dates[0];
    for (let k = 1; k < first.getUTCDay(); k++) row.push('<div class="cal-cell is-empty"></div>');
    dates.forEach((d, i) => {
      const id = `f${fi}-d${i}`;
      row.push(`<div class="cal-cell"><input type="radio" name="data" id="${id}" value="${iso(d)}" aria-label="${longLabel(d)}"><label for="${id}" aria-hidden="true">${d.getUTCDate()}<small>${SHORT[lang][d.getUTCMonth()]}</small></label></div>`);
      if (d.getUTCDay() === 5) { rows.push(`<div class="cal-row">${row.join("")}</div>`); row = []; }
    });
    if (row.length) { while (row.length < 5) row.push('<div class="cal-cell is-empty"></div>'); rows.push(`<div class="cal-row">${row.join("")}</div>`); }
    cal.innerHTML = head + rows.join("");
    const last = dates[dates.length - 1];
    range.textContent = lang === "pt"
      ? `Disponível de ${longLabel(first)} a ${longLabel(last)}. Hora de Lisboa.`
      : `Available from ${longLabel(first)} to ${longLabel(last)}. Lisbon time.`;
    hora.insertAdjacentHTML("beforeend", times.map((t) => `<option value="${t}">${lang === "pt" ? t.replace(":", "h") : t}</option>`).join(""));

    const MSG = {};
    form.querySelectorAll(".error").forEach((e) => { MSG[e.id.split("-").slice(-2, -1)[0]] = e.textContent; });
    const summary = form.querySelector(".form-summary");

    function check() {
      const fd = new FormData(form);
      const bad = [];
      const v = (k) => String(fd.get(k) || "").trim();
      if (v("nome").length < 2) bad.push("nome");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v("email"))) bad.push("email");
      if (v("telefone").replace(/\D/g, "").length < 9) bad.push("telefone");
      if (!v("area")) bad.push("area");
      if (!allowed.has(v("data"))) bad.push("data");
      if (!times.includes(v("hora"))) bad.push("hora");
      if (!fd.get("consent")) bad.push("consent");
      return bad;
    }
    function show(bad) {
      form.querySelectorAll("[data-field]").forEach((f) => {
        const k = f.dataset.field;
        const isBad = bad.includes(k);
        f.classList.toggle("has-error", isBad);
        f.querySelectorAll("input:not([type=radio]), select").forEach((el) => el.setAttribute("aria-invalid", String(isBad)));
        if (k === "data") cal.classList.toggle("is-invalid", isBad);
      });
    }
    form.addEventListener("change", () => { if (form.dataset.tried) show(check()); });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      form.dataset.tried = "1";
      const bad = check();
      show(bad);
      if (bad.length) {
        summary.querySelector("ul").innerHTML = bad.map((k) => {
          const target = k === "data" ? form.querySelector('input[name="data"]') : form.querySelector(`[name="${k}"]`);
          return `<li><a href="#${target.id}">${MSG[k]}</a></li>`;
        }).join("");
        summary.classList.add("is-visible");
        summary.focus();
        return;
      }
      summary.classList.remove("is-visible");
      const fd = new FormData(form);
      const d = new Date(fd.get("data") + "T00:00:00Z");
      const t = String(fd.get("hora"));
      wrap.querySelector("[data-success-detail]").textContent = lang === "pt"
        ? `Pedido para ${longLabel(d)}, às ${t.replace(":", "h")}.`
        : `Requested for ${longLabel(d)} at ${t}.`;
      form.hidden = true;
      const ok = wrap.querySelector(".form-success");
      ok.classList.add("is-visible");
      ok.focus();
    });
    summary.addEventListener("click", (e) => {
      const a = e.target.closest("a");
      if (!a) return;
      e.preventDefault();
      document.getElementById(a.getAttribute("href").slice(1))?.focus();
    });
  });
})();
