import {
  ArrowUp,
  ChevronDown,
  ChevronRight,

  Phone,
  Sun,
  Moon,
} from "lucide-react";
import { useEffect, useState } from "react";
import logoImg from "@/assets/logo.png";
import { THEME_KEY, applyTheme, getStoredTheme, resolveTheme, setTheme } from "@/lib/theme";
import { COMPANY, NAV, PHONE_DISPLAY, PHONE_TEL } from "@/components/site/data";

export function SectionHead({
  eyebrow,
  title,
  text,
  textClassName = "text-muted-foreground",
}: {
  eyebrow: string;
  title: string;
  text?: string;
  textClassName?: string;
}) {
  return (
    <div className="max-w-2xl">
      <span className="eyebrow">{eyebrow}</span>
      <h2 className="mt-3 text-3xl leading-tight sm:text-4xl">{title}</h2>
      <span className="accent-rule mt-4" />
      {text && <p className={`mt-4 ${textClassName}`}>{text}</p>}
    </div>
  );
}

export function Breadcrumbs({ current }: { current: string }) {
  const linkClass = "transition-colors hover:text-accent";
  return (
    <nav aria-label="Хлебные крошки" className="sticky top-16 z-40 mt-16 border-b border-border/60 bg-surface/95 backdrop-blur">
      <div className="container-page py-3">
        <ol className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-muted-foreground">
          <li>
            <a href="/" className={linkClass}>
              Главная
            </a>
          </li>
          <li aria-hidden="true" className="text-border">
            <ChevronRight className="size-4" />
          </li>
          <li>
            <a href="/#geography" className={linkClass}>
              Направления
            </a>
          </li>
          <li aria-hidden="true" className="text-border">
            <ChevronRight className="size-4" />
          </li>
          <li aria-current="page" className="text-foreground">
            {current}
          </li>
        </ol>
      </div>
    </nav>
  );
}




export function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/10 bg-ink/90 backdrop-blur">
      <div className="container-page flex h-16 items-center justify-between gap-4">
        <a
          href="/"
          onClick={(e) => {
            if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
            if (window.location.pathname === "/") {
              e.preventDefault();
              window.scrollTo({ top: 0, behavior: "smooth" });
            }
          }}
          className="flex items-center gap-2.5 text-ink-foreground"
        >
          <span className="grid size-9 place-items-center overflow-hidden rounded-md bg-accent">
            <img src={logoImg} alt="Логотип Униспектрум" className="size-full object-contain" />
          </span>
          <span className="font-display text-lg tracking-wide uppercase">Униспектрум</span>
        </a>
        <nav className="hidden items-center gap-3 lg:flex xl:gap-5" aria-label="Основная навигация">
          {NAV.map((n) => (
            <a
              key={n.href}
              href={`/${n.href}`}
              className="text-sm whitespace-nowrap text-ink-muted transition-colors hover:text-accent"
            >
              {n.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <a href={`tel:${PHONE_TEL}`} className="hidden text-sm font-semibold text-ink-foreground sm:block">
            {PHONE_DISPLAY}
          </a>
          <a href="/#contacts" className="btn-base btn-cta hover:btn-cta-hover !px-4 !py-2 !text-xs text-center">
            Свяжитесь с нами
          </a>
          <button
            className="text-ink-foreground lg:hidden"
            aria-label="Меню"
            aria-expanded={open}
            onClick={() => setOpen((v) => !v)}
          >
            <ChevronDown className={`size-6 transition-transform ${open ? "rotate-180" : ""}`} />
          </button>
        </div>
      </div>
      {open && (
        <nav className="border-t border-white/10 bg-ink lg:hidden" aria-label="Мобильная навигация">
          <div className="container-page grid gap-1 py-3">
            {NAV.map((n) => (
              <a
                key={n.href}
                href={`/${n.href}`}
                onClick={() => setOpen(false)}
                className="rounded-md px-2 py-2 text-sm text-ink-muted hover:bg-white/5 hover:text-accent"
              >
                {n.label}
              </a>
            ))}
          </div>
        </nav>
      )}
    </header>
  );
}

export function Footer() {
  return (
    <footer className="bg-ink pt-14 pb-8 text-ink-foreground">
      <div className="container-page grid gap-8 md:grid-cols-2">
        <div>
          <span className="font-display text-lg tracking-wide uppercase">Униспектрум</span>
          <p className="mt-3 text-sm text-ink-muted">
            {COMPANY}. 220024, Республика Беларусь, г. Минск, ул. Бабушкина, 54-415. УНП 101347929
          </p>
        </div>
        <nav aria-label="Навигация в подвале">
          <h2 className="text-sm">Разделы</h2>
          <ul className="mt-3 grid grid-cols-2 gap-1.5 text-sm text-ink-muted">
            {NAV.map((n) => (
              <li key={n.href}>
                <a href={`/${n.href}`} className="hover:text-accent">
                  {n.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <div className="container-page mt-10 border-t border-white/10 pt-6 text-xs text-ink-muted">
        © {new Date().getFullYear()} {COMPANY}
      </div>
    </footer>
  );
}

export function FloatingActions() {
  const [show, setShow] = useState(false);
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > 600);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // Тему уже применил инлайн-скрипт в <head>. Здесь только синхронизируем состояние,
  // чтобы свич и системная тема не переопределяли друг друга.
  useEffect(() => {
    const current = resolveTheme();
    applyTheme(current);
    setDark(current === "dark");

    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onSystemChange = (e: MediaQueryListEvent) => {
      // Системная тема учитывается, только пока пользователь не сделал явный выбор.
      if (getStoredTheme()) return;
      applyTheme(e.matches ? "dark" : "light");
      setDark(e.matches);
    };
    mq.addEventListener("change", onSystemChange);

    const onStorage = (e: StorageEvent) => {
      if (e.key !== THEME_KEY || (e.newValue !== "dark" && e.newValue !== "light")) return;
      applyTheme(e.newValue);
      setDark(e.newValue === "dark");
    };
    window.addEventListener("storage", onStorage);

    return () => {
      mq.removeEventListener("change", onSystemChange);
      window.removeEventListener("storage", onStorage);
    };
  }, []);

  const toggleTheme = () => {
    setDark((v) => {
      const next = v ? "light" : "dark";
      setTheme(next);
      return next === "dark";
    });
  };


  return (
    <div className="fixed right-4 bottom-4 z-50 flex flex-col items-end gap-2.5">
      {show && (
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          aria-label="Наверх"
          className="grid size-11 cursor-pointer place-items-center rounded-full border border-border bg-card text-foreground shadow-[var(--shadow-card)] transition-colors hover:text-accent"
        >
          <ArrowUp className="size-5" />
        </button>
      )}
      <a
        href={`tel:${PHONE_TEL}`}
        aria-label="Позвонить"
        className="grid size-13 place-items-center rounded-full bg-primary text-primary-foreground shadow-[var(--shadow-lift)]"
      >
        <Phone className="size-6" />
      </a>
      <button
        onClick={toggleTheme}
        aria-label={dark ? "Светлая тема" : "Тёмная тема"}
        className="grid size-11 cursor-pointer place-items-center rounded-full border border-border bg-card text-foreground shadow-[var(--shadow-card)] transition-colors hover:text-accent"
      >
        {dark ? <Sun className="size-5" /> : <Moon className="size-5" />}
      </button>
    </div>
  );
}


