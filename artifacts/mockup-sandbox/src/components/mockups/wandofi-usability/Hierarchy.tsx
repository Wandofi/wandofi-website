import React from "react";

const INK = "#050505";
const WHITE = "#f4f4f3";
const MUTE = "#9a9a9d";
const RED = "#e1251b";
const RED_GLOW = "rgba(225, 37, 27, 0.55)";

export function Hierarchy() {
  return (
    <div
      className="relative w-full overflow-hidden flex flex-col font-['Inter']"
      style={{
        height: "100vh",
        minHeight: 720,
        background: INK,
        color: WHITE,
      }}
    >
      {/* Background red glow */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 z-0"
        style={{
          background:
            "radial-gradient(40% 50% at 75% 50%, rgba(225,37,27,0.15), rgba(225,37,27,0.05) 50%, transparent 80%)",
          mixBlendMode: "screen",
        }}
      />

      {/* Top Nav */}
      <header className="relative z-30 flex items-center justify-between px-10 py-8">
        <div className="flex items-center gap-6">
          <span
            className="select-none text-xl font-medium tracking-tight"
            style={{ fontFamily: "'Fraunces', serif", color: WHITE }}
          >
            WANDOFI
          </span>
          <span
            className="flex items-center gap-2 text-sm"
            style={{ color: MUTE }}
          >
            <span
              className="inline-block h-2 w-2 rounded-full"
              style={{ background: RED, boxShadow: `0 0 10px 1px ${RED_GLOW}` }}
            />
            Disponível para projecto
          </span>
        </div>
        <nav className="flex items-center gap-8 text-sm" style={{ color: MUTE }}>
          <a href="#" className="hover:text-white transition-colors">
            Trabalho <span style={{ color: RED }}>[6]</span>
          </a>
          <a href="#" className="hover:text-white transition-colors">
            Serviços <span style={{ color: RED }}>[6]</span>
          </a>
          <a href="#" className="hover:text-white transition-colors">Experiência</a>
          <a href="#" className="hover:text-white transition-colors">Contacto</a>
        </nav>
      </header>

      {/* Main Content Area */}
      <main className="relative z-10 flex-1 flex items-center px-16 max-w-[1400px] mx-auto w-full">
        {/* Left Column: Information Hierarchy */}
        <div className="flex-1 max-w-[700px] pr-12 flex flex-col gap-8">
          <div className="space-y-6">
            <div>
              <p
                className="text-xs uppercase tracking-[0.25em] font-medium mb-3"
                style={{ color: RED }}
              >
                Mauro Cordeiro — Project Manager Operacional
              </p>
              <h1
                className="text-5xl lg:text-6xl leading-[1.1] tracking-tight font-medium"
                style={{ fontFamily: "'Fraunces', serif" }}
              >
                Migração, criação de sites, SEO técnico e automações.
              </h1>
            </div>

            <p className="text-lg leading-relaxed max-w-[540px]" style={{ color: MUTE }}>
              A maioria dos negócios pequenos não falha por falta de talento. Falha por falta de infraestrutura que o sustente. Traduzo o que está na sua cabeça em estrutura digital concreta.
            </p>
          </div>

          <div className="flex items-center gap-4 pt-2">
            <a
              href="#"
              className="inline-flex items-center justify-center rounded-sm px-8 py-4 text-sm font-medium transition-transform hover:-translate-y-0.5"
              style={{ background: RED, color: WHITE, boxShadow: `0 4px 20px -5px ${RED_GLOW}` }}
            >
              Vamos falar <span aria-hidden className="ml-2">↗</span>
            </a>
            <a
              href="#"
              className="inline-flex items-center justify-center rounded-sm px-8 py-4 text-sm font-medium transition-colors hover:bg-white/5"
              style={{ border: "1px solid rgba(255,255,255,0.16)", color: WHITE }}
            >
              Ver trabalho
            </a>
          </div>

          <div className="pt-12 mt-auto">
            <ul className="flex items-center gap-6 text-sm" style={{ color: MUTE }}>
              <li><a href="#" className="hover:text-white transition-colors">LinkedIn</a></li>
              <li><a href="#" className="hover:text-white transition-colors">GitHub</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Instagram</a></li>
              <li className="ml-auto" style={{ color: WHITE }}>
                <a href="mailto:main@wandofi.pt" className="hover:text-red-400 transition-colors">main@wandofi.pt</a>
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column: Portrait */}
        <div className="flex-1 relative flex justify-end h-full items-end pb-0">
          {/* Subtle Wordmark behind portrait */}
          <div 
            className="absolute right-0 top-1/4 select-none opacity-[0.03] pointer-events-none"
            style={{ 
              fontFamily: "'Fraunces', serif",
              fontSize: "14rem",
              lineHeight: 0.8,
              letterSpacing: "-0.04em",
              writingMode: "vertical-rl",
              transform: "rotate(180deg)"
            }}
          >
            WANDOFI
          </div>
          
          <img
            src="/__mockup/images/portrait.png"
            alt="Mauro Cordeiro"
            className="relative z-10 w-full max-w-[500px] object-contain drop-shadow-2xl"
            style={{
              maxHeight: "85vh",
              filter: "drop-shadow(0 24px 60px rgba(0,0,0,0.8))"
            }}
          />
          
          {/* Gradient fade at bottom to ground the portrait */}
          <div
            className="absolute bottom-0 right-0 w-full h-32 z-20 pointer-events-none"
            style={{
              background: `linear-gradient(to bottom, transparent, ${INK} 90%)`
            }}
          />
        </div>
      </main>
    </div>
  );
}
