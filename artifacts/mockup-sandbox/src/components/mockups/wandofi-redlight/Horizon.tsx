import React from "react";

const INK = "#050505";
const WHITE = "#f4f4f3";
const MUTE = "#9a9a9d";
const RED = "#e1251b";
const RED_GLOW = "rgba(225, 37, 27, 0.55)";

export function Horizon() {
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
      {/* single horizontal red line with bloom */}
      <div className="absolute left-0 right-0 top-1/2 z-0 -translate-y-1/2">
        <div
          className="w-full"
          style={{
            height: "2px",
            background: RED,
            boxShadow: `0 0 120px 20px rgba(225, 37, 27, 0.4), 0 0 40px 5px ${RED_GLOW}`,
          }}
        />
        {/* Soft bloom above and below */}
        <div
          className="absolute inset-x-0 top-1/2 -translate-y-1/2 pointer-events-none"
          style={{
            height: "500px",
            background: `linear-gradient(to bottom, transparent, rgba(225,37,27,0.08) 45%, rgba(225,37,27,0.15) 50%, rgba(225,37,27,0.08) 55%, transparent)`,
            mixBlendMode: "screen",
          }}
        />
      </div>

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
            <a href="#">Trabalho <span style={{ color: RED }}>[6]</span></a>
            <a href="#">Serviços <span style={{ color: RED }}>[6]</span></a>
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

      {/* STAGE: wordmark + portrait without the frame */}
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
            }}
          >
            DOFI
          </span>
        </div>

        {/* The portrait (no frame, just the image standing in front of the line) */}
        <div className="absolute left-1/2 top-[54%] z-20 -translate-x-1/2 -translate-y-1/2">
          <div className="relative" style={{ width: 372, height: 540 }}>
            {/* portrait: head lifts just above the middle line for depth */}
            <img
              src="/__mockup/images/portrait.png"
              alt="Mauro Cordeiro — Wandofi"
              className="pointer-events-none absolute bottom-0 left-1/2 -translate-x-1/2"
              style={{
                width: 340,
                maxWidth: "none",
                filter: "drop-shadow(0 24px 60px rgba(0,0,0,0.6))",
              }}
            />
            {/* fade the figure base into the background */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-x-0 bottom-0"
              style={{
                height: 90,
                background: `linear-gradient(to bottom, transparent, ${INK} 92%)`,
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
          <li><a href="#">LinkedIn</a></li>
          <li><a href="#">GitHub</a></li>
          <li><a href="#">Instagram</a></li>
          <li style={{ color: WHITE }}><a href="#">main@wandofi.pt</a></li>
        </ul>
      </div>
    </div>
  );
}
