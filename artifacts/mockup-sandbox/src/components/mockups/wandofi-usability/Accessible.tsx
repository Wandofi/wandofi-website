import "./_group.css";

const INK = "#050505";
const WHITE = "#f4f4f3";
const RED = "#e1251b";

export function Accessible() {
  return (
    <div
      className="w-full flex flex-col relative overflow-hidden"
      style={{
        minHeight: "100vh",
        background: INK,
        color: WHITE,
        fontFamily: "'Inter', system-ui, sans-serif",
      }}
    >
      <header className="w-full px-10 py-10 flex items-center justify-between z-20">
        <div className="flex items-center gap-4">
          <span
            className="w-4 h-4 rounded-full"
            style={{ background: RED }}
            aria-hidden="true"
          />
          <span className="text-xl font-semibold tracking-wide">
            Disponível para projecto
          </span>
        </div>

        <nav className="flex gap-10 text-xl font-semibold">
          <a
            href="#"
            className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
          >
            Trabalho <span className="text-[#e1251b] font-bold">[6]</span>
          </a>
          <a
            href="#"
            className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
          >
            Serviços <span className="text-[#e1251b] font-bold">[6]</span>
          </a>
          <a
            href="#"
            className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
          >
            Experiência
          </a>
          <a
            href="#"
            className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
          >
            Contacto
          </a>
        </nav>
      </header>

      <main className="flex-1 w-full flex">
        <div className="flex-1 flex flex-col justify-center pl-10 pr-6 lg:pl-16 xl:pl-24 z-20 pb-12">
          <div className="max-w-[760px] flex flex-col gap-10">
            <h1
              className="text-7xl xl:text-8xl leading-[1.1] font-medium"
              style={{ fontFamily: "'Fraunces', serif" }}
            >
              Mauro Cordeiro
              <br />
              <span className="block mt-4 text-5xl xl:text-6xl text-[#d7d7d6]">
                Project Manager Operacional
              </span>
            </h1>

            <p className="text-2xl leading-relaxed max-w-[650px] font-medium" style={{ color: "#c1c1c1" }}>
              Infraestrutura antes da escala. A maioria dos negócios não falha por falta de talento, falha por falta de estrutura. 
              Ajudo a traduzir o que está na cabeça em organização concreta.
            </p>

            <div className="flex flex-wrap gap-6 pt-4">
              <a
                href="#"
                className="acc-focus-ring inline-flex items-center justify-center min-h-[64px] px-10 text-xl font-bold rounded bg-[#f4f4f3] text-[#050505] transition-colors hover:bg-white hover:opacity-90"
              >
                Vamos falar <span className="ml-3 font-black text-2xl" aria-hidden>↗</span>
              </a>
              <a
                href="#"
                className="acc-focus-ring inline-flex items-center justify-center min-h-[64px] px-10 text-xl font-bold rounded border-[3px] border-[#f4f4f3] text-[#f4f4f3] transition-colors hover:bg-white hover:text-black"
              >
                Ver trabalho
              </a>
            </div>

            <div className="flex flex-wrap items-center gap-8 pt-16 mt-auto text-xl font-semibold">
              <a
                href="#"
                className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
              >
                LinkedIn
              </a>
              <a
                href="#"
                className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
              >
                GitHub
              </a>
              <a
                href="#"
                className="acc-focus-ring hover:underline underline-offset-8 decoration-2 decoration-[#e1251b]"
              >
                Instagram
              </a>
              <span className="w-2 h-2 rounded-full bg-white opacity-40" aria-hidden></span>
              <a
                href="mailto:main@wandofi.pt"
                className="acc-focus-ring hover:underline underline-offset-8 decoration-2 text-[#e1251b] font-bold"
              >
                main@wandofi.pt
              </a>
            </div>
          </div>
        </div>

        <div className="w-[45%] relative flex items-end justify-center pointer-events-none">
          <div className="absolute inset-0 acc-red-light z-0 mix-blend-screen opacity-90" />
          <img
            src="/__mockup/images/portrait.png"
            alt="Fotografia de Mauro Cordeiro"
            className="relative z-10 w-[90%] max-w-[700px] object-contain object-bottom h-[85%]"
            style={{ filter: "drop-shadow(0 20px 40px rgba(0,0,0,0.8))" }}
          />
        </div>
      </main>
    </div>
  );
}
