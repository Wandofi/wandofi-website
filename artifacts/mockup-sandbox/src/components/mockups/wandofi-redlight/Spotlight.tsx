import React from "react";

const INK = "#050505";
const WHITE = "#f4f4f3";
const MUTE = "#9a9a9d";
const RED = "#e1251b";
const RED_GLOW = "rgba(225, 37, 27, 0.55)";

export function Spotlight() {
  return (
    <div
      className="relative w-full overflow-hidden"
      style={{
        height: "100vh",
        minHeight: 720,
        background: INK,
        fontFamily: "'Inter', system-ui, sans-serif",
        color: WHITE,
      }}
    >
      {/* Background ambient dark base */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0"
        style={{
          background: "radial-gradient(circle at 50% 100%, #110302 0%, transparent 50%)",
        }}
      />

      {/* RAKING SPOTLIGHT BEAM */}
      <div
        aria-hidden
        className="pointer-events-none absolute left-1/2 top-[-10%]"
        style={{
          width: "800px",
          height: "120vh",
          marginLeft: "-400px",
          background: `linear-gradient(to bottom, rgba(225,37,27,0.8) 0%, rgba(225,37,27,0.15) 50%, transparent 100%)`,
          clipPath: "polygon(40% 0, 60% 0, 100% 100%, 0 100%)",
          filter: "blur(60px)",
          mixBlendMode: "screen",
          opacity: 0.85,
          transform: "perspective(1000px) rotateX(20deg)",
          transformOrigin: "top center",
        }}
      />

      {/* NAV */}
      <header className="absolute left-0 right-0 top-0 z-30 px-10 py-7">
        <div className="relative flex items-center">
          <span
            className="flex items-center gap-2 text-[0.9rem]"
            style={{ color: MUTE }}
          >
            <span
              className="inline-block h-[7px] w-[7px] rounded-full"
              style={{ background: RED, boxShadow: `0 0 10px 1px ${RED_GLOW}` }}
            />
            Disponível para projecto
          </span>
          <nav
            className="absolute left-1/2 flex -translate-x-1/2 gap-7 text-[0.9rem]"
            style={{ color: MUTE }}
          >
            <a href="#">
              Trabalho <span style={{ color: RED }}>[6]</span>
            </a>
            <a href="#">
              Serviços <span style={{ color: RED }}>[6]</span>
            </a>
            <a href="#">Experiência</a>
            <a href="#">Contacto</a>
          </nav>
          <a
            href="#"
            className="ml-auto rounded-full px-[1.15rem] py-[0.6rem] text-[0.85rem] font-medium"
            style={{ background: WHITE, color: INK }}
          >
            Vamos falar <span aria-hidden>↗</span>
          </a>
        </div>
      </header>

      {/* STAGE: wordmark + spotlight portrait */}
      <div className="absolute inset-0 z-10 flex items-center justify-center px-[4rem]">
        <div className="relative flex w-full max-w-[1320px] items-center justify-between">
          <span
            className="select-none"
            style={{
              fontFamily: "'Fraunces', Georgia, serif",
              fontWeight: 500,
              fontSize: "clamp(3rem, 13vw, 12rem)",
              lineHeight: 0.84,
              letterSpacing: "-0.03em",
              color: WHITE,
              textShadow: "0 0 30px rgba(225,37,27,0.2)",
            }}
          >
            WAN
          </span>
          <span
            className="select-none"
            style={{
              fontFamily: "'Fraunces', Georgia, serif",
              fontWeight: 500,
              fontSize: "clamp(3rem, 13vw, 12rem)",
              lineHeight: 0.84,
              letterSpacing: "-0.03em",
              color: "transparent",
              WebkitTextStroke: "1.5px rgba(244,244,243,0.6)",
              textShadow: "0 0 40px rgba(225,37,27,0.1)",
            }}
          >
            DOFI
          </span>
        </div>

        {/* The portrait in the spotlight (no border box) */}
        <div className="absolute left-1/2 top-[54%] z-20 -translate-x-1/2 -translate-y-1/2">
          <div className="relative flex items-end justify-center" style={{ width: 372, height: 540 }}>
            {/* Ambient rim light directly behind subject */}
            <div
              className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
              style={{
                width: 250,
                height: 400,
                background: `radial-gradient(ellipse at center, rgba(225,37,27,0.6) 0%, transparent 70%)`,
                filter: "blur(40px)",
                mixBlendMode: "screen",
              }}
            />

            {/* portrait */}
            <img
              src="/__mockup/images/portrait.png"
              alt="Mauro Cordeiro — Wandofi"
              className="pointer-events-none relative z-10"
              style={{
                width: 340,
                maxWidth: "none",
                filter: "drop-shadow(0 24px 60px rgba(0,0,0,0.8)) drop-shadow(0 -10px 30px rgba(225,37,27,0.3))",
              }}
            />

            {/* Grounding pool of light */}
            <div
              className="pointer-events-none absolute bottom-0 left-1/2 z-0 -translate-x-1/2 rounded-[100%]"
              style={{
                width: 300,
                height: 40,
                background: "rgba(225,37,27,0.5)",
                filter: "blur(20px)",
                mixBlendMode: "screen",
                transform: "translateY(50%)",
              }}
            />

            {/* Fade the figure base into the dark floor */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-x-[-100px] bottom-0 z-20"
              style={{
                height: 120,
                background: `linear-gradient(to bottom, transparent, ${INK} 85%)`,
              }}
            />
          </div>
        </div>
      </div>

      {/* META */}
      <div className="absolute bottom-0 left-0 right-0 z-30 flex items-end justify-between px-10 pb-9">
        <div>
          <p
            className="mb-4 text-[0.78rem] uppercase tracking-[0.22em]"
            style={{ color: MUTE }}
          >
            Project Manager Operacional
          </p>
          <div className="flex gap-3">
            <a
              href="#"
              className="rounded-full px-[1.25rem] py-[0.7rem] text-[0.9rem] font-medium"
              style={{ background: WHITE, color: INK }}
            >
              Vamos falar <span aria-hidden>↗</span>
            </a>
            <a
              href="#"
              className="rounded-full px-[1.25rem] py-[0.7rem] text-[0.9rem]"
              style={{ border: "1px solid rgba(255,255,255,0.16)", color: WHITE }}
            >
              Ver trabalho
            </a>
          </div>
        </div>
        <ul
          className="flex flex-col items-end gap-2 text-[0.85rem]"
          style={{ color: MUTE }}
        >
          <li>
            <a href="#">LinkedIn</a>
          </li>
          <li>
            <a href="#">GitHub</a>
          </li>
          <li>
            <a href="#">Instagram</a>
          </li>
          <li style={{ color: WHITE }}>
            <a href="#">main@wandofi.pt</a>
          </li>
        </ul>
      </div>
    </div>
  );
}
