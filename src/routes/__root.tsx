import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
// Шрифты предзагружаем: иначе браузер находит их только после разбора CSS,
// и текст успевает мигнуть системным шрифтом.
import manropeCyrillic from "@fontsource-variable/manrope/files/manrope-cyrillic-wght-normal.woff2?url";
import manropeLatin from "@fontsource-variable/manrope/files/manrope-latin-wght-normal.woff2?url";
import oswaldCyrillic from "@fontsource/oswald/files/oswald-cyrillic-600-normal.woff2?url";
import oswaldLatin from "@fontsource/oswald/files/oswald-latin-600-normal.woff2?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { applyTheme, resolveTheme } from "@/lib/theme";

function NotFoundComponent() {
  useEffect(() => {
    document.title = "Страница не найдена — ООО «Униспектрум»";
    const meta = document.createElement("meta");
    meta.name = "robots";
    meta.content = "noindex";
    document.head.appendChild(meta);
    return () => {
      meta.remove();
    };
  }, []);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-7xl font-bold text-foreground">404</h1>
        <h2 className="mt-4 text-xl font-semibold text-foreground">Страница не найдена</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Похоже, такой страницы не существует или она была перемещена.
        </p>
        <div className="mt-6">
          <Link
            to="/"
            className="inline-flex cursor-pointer items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            На главную
          </Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportLovableError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">
          Страница не загрузилась
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Произошла ошибка на нашей стороне. Попробуйте обновить страницу или вернуться на главную.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <button
            onClick={() => {
              router.invalidate();
              reset();
            }}
            className="inline-flex cursor-pointer items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Попробовать снова
          </button>
          <a
            href="/"
            className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            На главную
          </a>
        </div>
      </div>
    </div>
  );
}


export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      // Сообщаем браузеру, что сайт сам управляет светлой/тёмной темой,
      // иначе Chrome применяет принудительный auto-dark и перекрашивает цвета.
      { name: "color-scheme", content: "light dark" },
      { title: "ООО «Униспектрум»" },
      {
        name: "description",
        content:
          "Перевозки грузов по Беларуси и в разные регионы России. Расчёт стоимости до 30 минут.",
      },
      { name: "author", content: "ООО «Униспектрум»" },
      {
        property: "og:title",
        content: "ООО «Униспектрум» — грузоперевозки по Беларуси и России",
      },
      {
        property: "og:description",
        content:
          "Перевозки грузов по Беларуси и в разные регионы России. Расчёт стоимости до 30 минут.",
      },
      { property: "og:site_name", content: "ООО «Униспектрум»" },
      { property: "og:locale", content: "ru_RU" },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [
      {
        rel: "stylesheet",
        href: appCss,
      },
      ...[manropeCyrillic, manropeLatin, oswaldCyrillic, oswaldLatin].map((href) => ({
        rel: "preload",
        as: "font",
        type: "font/woff2",
        href,
        crossOrigin: "anonymous" as const,
      })),
      { rel: "icon", href: "/favicon.ico", sizes: "any" },
      { rel: "icon", href: "/icon-192.png", type: "image/png", sizes: "192x192" },
      { rel: "apple-touch-icon", href: "/apple-touch-icon.png", sizes: "180x180" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

const themeInit = `(function(){try{var s=localStorage.getItem("theme");var d=s?s==="dark":window.matchMedia("(prefers-color-scheme: dark)").matches;var e=document.documentElement;e.classList.toggle("dark",d);e.style.colorScheme=d?"dark only":"light only";}catch(e){}})();`;

// Если пользователь начал скроллить до гидратации, восстановление позиции
// роутером отбрасывало страницу назад. Гасим только эти ранние программные
// прокрутки, само восстановление при обновлении страницы продолжает работать.
const scrollGuard = `(function(){try{
var moved=false;
var hydrated=false;
var releaseTimer;
var mark=function(){moved=true;};
["wheel","touchmove","keydown"].forEach(function(t){window.addEventListener(t,mark,{passive:true});});
var origWin=window.scrollTo.bind(window);
var origEl=Element.prototype.scrollTo;
var blocked=function(){return moved;};
window.scrollTo=function(){if(blocked())return;return origWin.apply(null,arguments);};
Element.prototype.scrollTo=function(){if(blocked()&&(this===document.body||this===document.documentElement))return;return origEl.apply(this,arguments);};
var release=function(){
  if(!hydrated)return;
  window.scrollTo=origWin;
  Element.prototype.scrollTo=origEl;
  ["wheel","touchmove","keydown"].forEach(function(t){window.removeEventListener(t,mark);});
};
window.addEventListener("lovable:hydrated",function(){
  hydrated=true;
  clearTimeout(releaseTimer);
  releaseTimer=setTimeout(release,2500);
},{once:true});
setTimeout(function(){hydrated=true;release();},10000);
}catch(e){}})();`;

function RootShell({ children }: { children: ReactNode }) {
  const router = useRouter();

  // React может стереть класс на <html> при гидратации — сразу возвращаем его,
  // иначе тема "моргает" и кажется несохранённой.
  useEffect(() => {
    applyTheme(resolveTheme());
    window.dispatchEvent(new Event("lovable:hydrated"));
  }, []);

  // Переход к разделу на текущей странице прокручиваем сами, не добавляя якорь в адрес:
  // иначе кнопка «Назад» возвращает к старому разделу, а не туда, где пользователь остановился.
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const target = e.target as HTMLElement | null;
      const link = target?.closest?.("a");
      if (!link || link.target === "_blank") return;
      const url = new URL(link.href, window.location.href);
      if (url.origin !== window.location.origin) return;
      if (!url.hash || url.pathname !== window.location.pathname) return;
      const el = document.getElementById(url.hash.slice(1));
      if (!el) return;
      e.preventDefault();
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  // При переходе с другой страницы якорь нужен для прокрутки, но в адресе он не нужен:
  // после прокрутки убираем его, не создавая новую запись в истории. Обрабатываем
  // также якорь, который пользователь добавил в адрес уже после загрузки страницы.
  useEffect(() => {
    let timer: ReturnType<typeof setTimeout>;
    const handleHash = () => {
      const hash = window.location.hash;
      if (!hash || hash.length < 2) return;

      clearTimeout(timer);
      let attempts = 0;

      const stripHash = () => {
        if (window.location.hash !== hash) return;
        const y = window.scrollY;
        const x = window.scrollX;
        const root = document.documentElement;
        const previousScrollBehavior = root.style.scrollBehavior;

        // Удаление хэша может отменить ещё не завершившуюся плавную прокрутку
        // браузера и отправить страницу к началу. На время смены адреса делаем
        // прокрутку мгновенной и удерживаем достигнутую позицию несколько кадров.
        root.style.scrollBehavior = "auto";
        // Меняем адрес через роутер: если сделать это напрямую, роутер
        // продолжит считать текущим адрес с якорем и при возврате «Назад»
        // не найдёт сохранённую позицию прокрутки.
        router.history.replace(
          window.location.pathname + window.location.search,
          window.history.state,
        );


        const holdPosition = () => {
          if (Math.abs(window.scrollY - y) > 1 || Math.abs(window.scrollX - x) > 1) {
            window.scrollTo(x, y);
          }
        };

        holdPosition();
        requestAnimationFrame(() => {
          holdPosition();
          requestAnimationFrame(() => {
            holdPosition();
            root.style.scrollBehavior = previousScrollBehavior;
          });
        });
      };

      // Ждём, пока прокрутка к разделу завершится, и только потом чистим адрес.
      const stripWhenSettled = () => {
        let last = window.scrollY;
        let stable = 0;
        const check = () => {
          const y = window.scrollY;
          stable = Math.abs(y - last) < 1 ? stable + 1 : 0;
          last = y;
          if (stable >= 3) {
            stripHash();
            return;
          }
          timer = setTimeout(check, 60);
        };
        timer = setTimeout(check, 60);
      };

      const tick = () => {
        const el = document.getElementById(hash.slice(1));
        if (el) {
          el.scrollIntoView({ block: "start" });
          stripWhenSettled();
          return;
        }
        // Раздел может появиться позже — ждём, но адрес всё равно чистим.
        if (++attempts > 20) {
          stripHash();
          return;
        }
        timer = setTimeout(tick, 100);
      };


      timer = setTimeout(tick, 120);
    };

    handleHash();
    window.addEventListener("hashchange", handleHash);
    return () => {
      clearTimeout(timer);
      window.removeEventListener("hashchange", handleHash);
    };
  }, [router]);



  return (
    <html lang="ru" suppressHydrationWarning>
      <head suppressHydrationWarning>
        <HeadContent />
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        <script dangerouslySetInnerHTML={{ __html: scrollGuard }} />
      </head>
      <body suppressHydrationWarning>
        {children}
        <Scripts />
      </body>
    </html>
  );
}


function RootComponent() {
  const { queryClient } = Route.useRouteContext();

  return (
    <QueryClientProvider client={queryClient}>
      {/* Required: nested routes render here. Removing <Outlet /> breaks all child routes. */}
      <Outlet />
    </QueryClientProvider>
  );
}
