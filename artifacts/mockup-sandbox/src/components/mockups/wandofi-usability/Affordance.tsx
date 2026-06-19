import { Mail, ArrowRight, Github, Linkedin, Instagram } from "lucide-react";
import "./_group.css";

export function Affordance() {
  return (
    <div className="relative w-full h-[100vh] min-h-[720px] bg-[#050505] text-[#f4f4f3] font-['Inter'] overflow-hidden flex flex-col">
      {/* background glow */}
      <div 
        className="absolute inset-0 pointer-events-none"
        style={{
          background: "radial-gradient(40% 50% at 75% 50%, rgba(225,37,27,0.15) 0%, transparent 100%)",
          mixBlendMode: "screen"
        }}
      />
      {/* Nav */}
      <header className="relative z-30 w-full max-w-[1440px] mx-auto px-8 py-6 flex justify-between items-center">
        {/* Availability Pill */}
        <div className="flex items-center gap-3 px-4 py-2 bg-[#101012] border border-[rgba(255,255,255,0.09)] rounded-full shadow-sm">
          <span className="w-2 h-2 rounded-full bg-[#e1251b] shadow-[0_0_8px_1px_rgba(225,37,27,0.6)] animate-pulse" />
          <span className="text-sm font-medium text-[#f4f4f3]">Disponível para projecto</span>
        </div>

        <nav className="flex items-center gap-2 p-1.5 bg-[#0b0b0c] border border-[rgba(255,255,255,0.09)] rounded-full">
          {["Trabalho", "Serviços", "Experiência", "Contacto"].map((item, i) => (
            <a 
              key={item} 
              href="#"
              className="px-5 py-2 text-sm font-medium text-[#9a9a9d] rounded-full hover:bg-[rgba(255,255,255,0.08)] hover:text-[#f4f4f3] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#e1251b] focus-visible:text-[#f4f4f3] transition-all"
            >
              {item}
              {i < 2 && <span className="ml-1.5 text-[#e1251b] text-xs font-bold">[6]</span>}
            </a>
          ))}
        </nav>
      </header>
      {/* Main Content */}
      <main className="relative z-20 flex-1 w-full max-w-[1440px] mx-auto px-8 flex items-center">
        {/* Left: Content */}
        <div className="w-full max-w-2xl pt-10 pb-20">
          <p className="text-[#9a9a9d] text-sm uppercase tracking-widest font-semibold mb-6 flex items-center gap-3">
            <span className="w-8 h-[1px] bg-[#e1251b]" />
            Project Manager Operacional
          </p>

          <h1 className="font-['Fraunces'] text-6xl lg:text-7xl font-medium leading-[1.05] tracking-tight mb-8">
            Mauro Cordeiro
          </h1>

          <p className="text-lg leading-relaxed mb-10 max-w-xl text-muted-foreground">
            A maioria dos negócios não falha por falta de talento, mas por falta de <strong className="text-[#f4f4f3] font-semibold">infraestrutura</strong>. Eu ajudo a traduzir o que está na tua cabeça em estrutura concreta.
          </p>

          {/* Explicit Actions */}
          <div className="flex flex-wrap items-center gap-4 mb-12">
            <a 
              href="#contacto"
              className="flex items-center gap-3 px-8 py-4 bg-[#e1251b] text-white rounded-lg font-semibold text-lg hover:-translate-y-1 hover:shadow-[0_8px_30px_-6px_rgba(225,37,27,0.7)] focus-visible:outline focus-visible:outline-4 focus-visible:outline-[#e1251b] focus-visible:outline-offset-4 transition-all"
            >
              Vamos falar
              <ArrowRight className="w-5 h-5" />
            </a>

            <a 
              href="#trabalho"
              className="flex items-center gap-3 px-8 py-4 bg-[#101012] text-[#f4f4f3] rounded-lg font-medium text-lg border border-[rgba(255,255,255,0.16)] hover:bg-[rgba(255,255,255,0.05)] hover:border-[rgba(255,255,255,0.3)] focus-visible:outline focus-visible:outline-4 focus-visible:outline-[#9a9a9d] focus-visible:outline-offset-4 transition-all"
            >
              Ver trabalho
            </a>
          </div>

          {/* Contact Fast Path */}
          <div className="flex items-center gap-6 p-6 bg-[#0b0b0c] border border-[rgba(255,255,255,0.09)] rounded-xl max-w-md">
            <div className="w-12 h-12 bg-[#101012] border border-[rgba(255,255,255,0.1)] rounded-full flex items-center justify-center text-[#9a9a9d]">
              <Mail className="w-5 h-5" />
            </div>
            <div>
              <p className="text-sm text-[#9a9a9d] mb-1">Contacto directo</p>
              <a 
                href="mailto:main@wandofi.pt"
                className="text-[#f4f4f3] font-medium text-lg hover:text-[#e1251b] underline underline-offset-4 decoration-[rgba(255,255,255,0.2)] hover:decoration-[#e1251b] transition-all focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#e1251b] focus-visible:outline-offset-4 rounded-sm"
              >
                main@wandofi.pt
              </a>
            </div>
          </div>
        </div>

        {/* Right: Portrait */}
        <div className="absolute right-0 bottom-0 w-[45%] max-w-[700px] h-[85%] flex justify-end items-end pointer-events-none">
          {/* Framed backdrop for affordance of the "person" */}
          <div className="relative w-full h-full flex items-end justify-center">
            <div className="absolute bottom-0 w-[80%] h-[70%] bg-gradient-to-t from-[#e1251b]/10 to-transparent border-t border-x border-[#e1251b]/20 rounded-t-[2rem]" />
            <img 
              src="/__mockup/images/portrait.png" 
              alt="Mauro Cordeiro" 
              className="relative z-10 w-auto h-full object-contain object-bottom drop-shadow-2xl"
            />
          </div>
        </div>
      </main>
      {/* Socials - Fixed to bottom right for clear affordance */}
      <div className="absolute bottom-8 right-8 z-30 flex gap-3">
        {[
          { icon: Linkedin, label: "LinkedIn" },
          { icon: Github, label: "GitHub" },
          { icon: Instagram, label: "Instagram" }
        ].map((social, i) => (
          <a
            key={i}
            href="#"
            aria-label={social.label}
            className="w-12 h-12 flex items-center justify-center bg-[#101012] border border-[rgba(255,255,255,0.09)] rounded-lg text-[#9a9a9d] hover:bg-[#e1251b] hover:text-white hover:border-[#e1251b] hover:-translate-y-1 focus-visible:outline focus-visible:outline-2 focus-visible:outline-[#e1251b] focus-visible:outline-offset-4 transition-all shadow-sm"
          >
            <social.icon className="w-5 h-5" />
          </a>
        ))}
      </div>
    </div>
  );
}
