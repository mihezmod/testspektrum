import { useEffect, useRef, useState } from "react";
import { createFileRoute, Link } from "@tanstack/react-router";
import {
  Truck,
  Globe2,
  Boxes,
  Construction,
  Warehouse,
  FileCheck2,
  Phone,
  MapPin,
  Clock,
  Mail,
  ShieldCheck,
  ChevronDown,
  Route as RouteIcon,
} from "lucide-react";
import { Header, Footer, FloatingActions, SectionHead } from "@/components/site/Chrome";
import heroImg from "@/assets/hero-warehouse.jpg";
import aboutImg from "@/assets/about-company.jpg";
import {
  ADVANTAGES,
  COMPANY,
  EMAIL,
  FAQ,
  LEGAL_ADDRESS,
  NAV,
  OFFICE_ADDRESS,
  PHONES,
  PHONE_DISPLAY,
  PHONE_TEL,
  ROUTES,
  POSTAL_ADDRESS,
  SERVICES,
  STEPS,
  WORK_HOURS,
} from "@/components/site/data";

const TITLE = "ООО «Униспектрум» — грузоперевозки по Беларуси и России";
const DESCRIPTION =
  "Перевозки грузов по Беларуси и в разные регионы России. Расчёт стоимости до 30 минут.";
const SITE_URL = "https://unispektrum.by/";

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "MovingCompany",
      "@id": `${SITE_URL}#organization`,
      name: "ООО «Униспектрум»",
      description:
        "Перевозки грузов по Беларуси и в разные регионы России. Расчёт стоимости до 30 минут.",
      url: SITE_URL,
      logo: `${SITE_URL}icon-192.png`,
      image: `${SITE_URL}icon-192.png`,
      telephone: PHONE_DISPLAY,
      email: EMAIL,
      priceRange: "$$",
      address: {
        "@type": "PostalAddress",
        streetAddress: "ул. Бабушкина, 54-415",
        addressLocality: "Минск",
        postalCode: "220024",
        addressCountry: "BY",
      },
      geo: { "@type": "GeoCoordinates", latitude: 53.9412, longitude: 27.6519 },
      openingHoursSpecification: [
        {
          "@type": "OpeningHoursSpecification",
          dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          opens: "09:00",
          closes: "18:00",
        },
      ],
      areaServed: ["Беларусь", "Россия"],
      foundingDate: "2001",
    },
    {
      "@type": "FAQPage",
      "@id": `${SITE_URL}#faq`,
      mainEntity: FAQ.map((f) => ({
        "@type": "Question",
        name: f.q,
        acceptedAnswer: { "@type": "Answer", text: f.a },
      })),
    },
  ],
};

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: TITLE },
      { name: "description", content: DESCRIPTION },
      { name: "google-site-verification", content: "BEc4msYHPzyG_koRHH0fMTPFbyY7syqt27Lt5ZB-vbw" },
      { name: "yandex-verification", content: "6a707cf82391ac60" },
      {
        name: "keywords",
        content:
          "униспектрум, униспектрум ооо, юниспектрум ооо, юниспектр ооо, ооо униспектрум, униспектрум минск, униспектрум беларусь, униспектрум унп 101347929, униспектрум 101347929, унп 101347929, компания униспектрум, фирма униспектрум, unispektrum, unispektrum.by, униспектрум бай, униспектрум сайт, юниспектрум бай, униспектрум сайт минск, unispektrum сайт, unispectrum , unispectrum.by, униспектрум, униспектр, юниспектр, unispektr, юниспектрум, униспектрум минск адрес, униспектрум минск контакты, униспектрум минск телефон, униспектрум рб, униспектрум Беларусь официальный сайт, униспектрум грузоперевозки, униспектрум международные перевозки, униспектрум логистика, униспектрум транспортная компания, униспектрум перевозка грузов, униспектрум доставка, unispektrum грузоперевозки, unispektrum логистика, униспектрум минск грузоперевозки, ооо униспектрум международные перевозки, униспектрум беларусь логистика, сайт униспектрум грузоперевозки, униспектрум унп 101347929 контакты, грузоперевозки униспектрум, грузоперевозки unispektrum, 3PL логистика, 3PL оператор Беларусь, автодоставка, автоперевозки Беларусь Россия, автоперевозки Брест, автоперевозки Витебск, автоперевозки Гомель, автоперевозки Гродно, автоперевозки Минск, автоперевозки Могилёв, автоперевозки по Беларуси, автоперевозки Россия Беларусь, автотракинг, автотранспортные услуги, Автотранспортные услуги РБ, аренда грузовика, аренда грузовика с водителем, аренда тентованной фуры, аренда фуры с водителем, аудит грузоперевозок, аутсорсинг логистики, биржа грузоперевозок, быстрая доставка грузов, водитель категории CE, водитель-экспедитор, выгодные грузоперевозки, грузовое такси, грузовое такси Брест, грузовое такси Витебск, грузовое такси Гомель, грузовое такси Гродно, грузовое такси Минск, грузовое такси Могилёв, грузовой транспорт, грузовые перевозки, Грузовые перевозки Минск, грузовые перевозки по РФ, грузоперевозки, грузоперевозки Барановичи, грузоперевозки без посредников, грузоперевозки Беларусь, грузоперевозки Беларусь Армения, грузоперевозки Беларусь Грузия, грузоперевозки Беларусь Казахстан, грузоперевозки Беларусь Кыргызстан, грузоперевозки Беларусь Россия, грузоперевозки Бобруйск, грузоперевозки Борисов, грузоперевозки Брест, грузоперевозки Брест Россия, грузоперевозки в РФ, грузоперевозки Витебск, грузоперевозки Витебск Россия, грузоперевозки Минск Москва СПб Тула, грузоперевозки Минск Турция, грузоперевозки Минск Узбекистан, грузоперевозки Могилёв, грузоперевозки Могилёв Россия, грузоперевозки Мозырь, грузоперевозки Молодечно, грузоперевозки недорого, грузоперевозки Новополоцк, грузоперевозки онлайн заказ, грузоперевозки Орша, грузоперевозки от поставщика, грузоперевозки от производителя, грузоперевозки от склада, грузоперевозки Пинск, грузоперевозки по России и Беларуси, грузоперевозки Полоцк, грузоперевозки попутным транспортом, грузоперевозки РБ, грузоперевозки Речица, грузоперевозки Россия, грузоперевозки Россия Беларусь, грузоперевозки с гарантией, грузоперевозки Слуцк, грузоперевозки СНГ, грузоперевозки Солигорск, грузоперевозки Таможенный союз, грузоперевозки тентованным транспортом, грузоперевозки фурой, грузоперевозки цена, дешёвые грузоперевозки, диспетчер грузоперевозок, догруз, догрузка фуры, доставка в распределительный центр, доставка в торговую сеть, доставка генеральных грузов, доставка груза точно в срок, доставка грузов, доставка грузов Брест, доставка грузов Витебск, доставка грузов Гомель, доставка грузов Гродно, доставка грузов из Беларуси в Россию, доставка грузов Минск, доставка грузов Минск Россия, доставка грузов Могилёв, Доставка грузов по РБ, доставка грузов по России, доставка на склад, доставка на стройплощадку, доставка сборных грузов, доставка сборных грузов из Беларуси, загрузка 10 тонн, загрузка 20 тонн, загрузка 5 тонн, загрузка 25 тонн, заказать грузоперевозку, заказать грузоперевозку Минск Россия, заказать фуру из Минска, заявка на грузоперевозку, калькулятор грузоперевозки, контрактная логистика, контроль перевозок, корпоративные грузоперевозки, крупнотоннажные перевозки, логист грузоперевозок, логистическая компания Беларусь, логистическая компания Брест, логистическая компания Витебск, логистическая компания Гомель, логистическая компания Гродно, логистическая компания Минск Россия, логистическая компания Могилёв, логистические услуги, Логистические услуги Беларусь, логистический консалтинг, логистический оператор Беларусь, лучшая транспортная компания Беларусь, малотоннажные перевозки, маркировка грузов, машины для перевозки грузов, международная доставка грузов, международная транспортная накладная, международные грузоперевозки, международные грузоперевозки Брест, международные грузоперевозки Витебск, международные грузоперевозки Гомель, международные грузоперевозки Гродно, международные грузоперевозки Могилёв, международный водитель, надёжный перевозчик, наём грузового транспорта, найти догруз, найти машину для перевозки груза, найти обратную загрузку, найти попутный груз, негабарит Брест, негабарит Витебск, негабарит Гомель, негабарит Гродно, негабарит Могилёв, негабаритные грузоперевозки, негабаритные перевозки Минск Россия, недорогие грузоперевозки, ночные грузоперевозки, обратная загрузка, оперативная доставка грузов., оптимизация логистики, оптимизация перевозок, оставить заявку на перевозку груза, ответственность экспедитора, отзывы о грузоперевозках, отслеживание груза, паллетирование грузов, перевезти груз из Беларуси в Россию, перевозка бытовой техники, перевозка бытовой техники Брест, перевозка бытовой техники Витебск, перевозка бытовой техники Гомель, перевозка бытовой техники Гродно, перевозка бытовой техники Могилёв, перевозка бытовой химии, перевозка бытовок, перевозка генеральных грузов, перевозка грузов Беларусь, перевозка грузов Брест, перевозка грузов в Питер, перевозка грузов Витебск, перевозка грузов Гомель, перевозка грузов Гродно, перевозка грузов из Беларуси в Россию, перевозка грузов Могилёв, перевозка грузов на объект, перевозка длинномерных грузов, перевозка запчастей, перевозка зерна, перевозка коммерческих грузов, перевозка коробов, перевозка крупногабаритных грузов, перевозка мебели, перевозка мебели Брест, перевозка мебели Витебск, перевозка мебели Гомель, перевозка мебели Гродно, перевозка мебели Могилёв, перевозка медикаментов, перевозка медицинского оборудования, перевозка металлоконструкций, перевозка негабарита по Беларуси, перевозка негабарита по России, перевозка негабаритных грузов, перевозка оборудования, перевозка оборудования для производств, перевозка одежды, перевозка паллет, перевозка поддонов, перевозка продуктов питания, перевозка промышленных грузов, перевозка сборных грузов, перевозка станков, перевозка стройматериалов, перевозка стройматериалов Брест, перевозка стройматериалов Витебск, перевозка стройматериалов Гомель, перевозка стройматериалов Гродно, перевозка стройматериалов Могилёв, перевозка торговых грузов, перевозка труб, перевозка тяжеловесных грузов, перевозка электроники, перевозки по СНГ, перевозки тент, перевозчик Беларусь, перевозчик Минск, персональный менеджер по грузоперевозкам, площадка для негабарита, полная загрузка фуры, попутные грузоперевозки, прайс на грузоперевозки, проверенный перевозчик, пропуск на перевозку, прямые грузоперевозки, разовые грузоперевозки, распределительный склад, рассчитать грузоперевозку, рассчитать стоимость доставки груза, регулярные грузоперевозки, рейтинг грузоперевозчиков Беларусь, сборные грузы Брест, сборные грузы Витебск, сборные грузы Гомель, сборные грузы Гродно, сборные грузы Могилёв, сезонные грузоперевозки, складская логистика, СМР перевозки, сопровождение негабарита, среднетоннажные перевозки, срочные грузоперевозки, стоимость грузоперевозки, страхование грузов, страхование грузоперевозок, страхование ответственности перевозчика, таможенное декларирование, таможенное оформление грузов, таможенный брокер Беларусь, тарифы на грузоперевозки, тендер на грузоперевозки, тендерная логистика, товарно-транспортная накладная, транспорт для перевозки грузов, Транспорт для перевозки грузов Минск, транспорт для перевозки грузов по Беларуси, транспорт для перевозки грузов по России, транспортировка грузов, Транспортировка грузов по Беларуси, транспортная компания Бобруйск, транспортная компания Борисов, транспортная компания Брест, транспортная компания Витебск, транспортная компания Гомель, транспортная компания Гродно, транспортная компания Минск, транспортная компания Минск Россия, транспортная компания Могилёв, транспортная компания Мозырь, транспортная компания Пинск, транспортная компания Солигорск, транспортная логистика Беларусь Россия, транспортно-экспедиционное обслуживание, транспортно-экспедиционные услуги, транспортные услуги Брест, транспортные услуги Витебск, транспортные услуги Гомель, транспортные услуги Гродно, транспортные услуги Минск, транспортные услуги Могилёв, ТТН Беларусь, тяжеловесные перевозки Минск Россия, фрахт грузов, фрахтование транспорта, фулфилмент, фуры для грузоперевозок, цепочка поставок Беларусь Россия, частичная загрузка, экспедирование грузов, экспедитор Беларусь, экспедиторские услуги, экспресс доставка грузов, электронная транспортная накладная, электронные перевозочные документы, ЭТрН, ADR перевозки, CMR накладная, FTL перевозки, LTL перевозки, TIR перевозки, грузоперевозки Гомель, грузоперевозки выходного дня, грузоперевозки Гомель Россия, грузоперевозки Гродно, грузоперевозки Гродно Россия, грузоперевозки день в день, грузоперевозки для ИП, грузоперевозки для юридических лиц, грузоперевозки Жлобин, грузоперевозки Жодино, грузоперевозки за 24 часа, грузоперевозки из Бреста, грузоперевозки из Витебска, грузоперевозки из Гомеля, грузоперевозки из Гродно, грузоперевозки из Минска, грузоперевозки из Могилёва, грузоперевозки из РБ, грузоперевозки из РБ в РФ, грузоперевозки Лида, грузоперевозки Минск, грузоперевозки Минск Армения, грузоперевозки Минск Россия, грузоперевозки Минск Китай, грузоперевозки Минск Грузия, грузоперевозки Минск Казахстан",
      },
      { property: "og:title", content: TITLE },
      { property: "og:description", content: DESCRIPTION },
      { property: "og:type", content: "website" },
      { property: "og:url", content: SITE_URL },
      { property: "og:image", content: `${SITE_URL}og-image.png` },
      { property: "og:image:width", content: "1200" },
      { property: "og:image:height", content: "630" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: TITLE },
      { name: "twitter:description", content: DESCRIPTION },
      { name: "twitter:image", content: `${SITE_URL}og-image.png` },
    ],
    links: [{ rel: "canonical", href: SITE_URL }],
    scripts: [{ type: "application/ld+json", children: JSON.stringify(jsonLd) }],
  }),
  component: Landing,
});

const SERVICE_ICONS: Record<string, typeof Truck> = {
  truck: Truck,
  globe: Globe2,
  boxes: Boxes,
  crane: Construction,
  warehouse: Warehouse,
  file: FileCheck2,
};

const ROUTE_LINKS: Record<string, string | undefined> = {
  "Минск-Москва": "/minsk-moscow",
  "Минск-Санкт-Петербург": "/minsk-spb",
  "Минск-Тула": "/minsk-tula",
};


function Hero() {
  return (
    <section id="hero" className="relative isolate flex min-h-[46rem] items-center pt-16 lg:min-h-[44rem]">
      <img
        src={heroImg}
        alt="Грузовики едущие по дороге"
        width={1920}
        height={1088}
        className="absolute inset-0 -z-20 size-full object-cover"
      />
      <div className="hero-overlay absolute inset-0 -z-10" />
      <div className="container-page py-16">
        <div className="text-ink-foreground">
          <span className="eyebrow">Логистика Беларусь ⇄ Россия</span>
          <h1 className="mt-4 text-4xl leading-[1.08] sm:text-5xl lg:text-[3.4rem]">
            Грузоперевозки по Беларуси и России — быстро, надёжно, с полным сопровождением
          </h1>
          <p className="mt-5 max-w-xl text-lg text-ink-muted">
            ООО «Униспектрум» – перевозки грузов по Беларуси и в разные регионы России. Расчёт стоимости до 30 минут.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a href="#contacts" className="btn-base btn-cta hover:btn-cta-hover">
              Связаться с нами
            </a>
            <a href={`tel:${PHONE_TEL}`} className="btn-base btn-outline-light hover:bg-white/10">
              <Phone className="size-4" /> {PHONE_DISPLAY}
            </a>
          </div>
          <dl className="mt-10 grid max-w-lg grid-cols-2 gap-6 border-t border-white/15 pt-6">
            {[
              ["с 2001", "на рынке логистики"],
              ["11", "тентованных фур"],
            ].map(([v, l]) => (
              <div key={l}>
                <dt className="font-display text-2xl text-accent">{v}</dt>
                <dd className="mt-1 text-xs text-ink-muted">{l}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </section>
  );
}

function Services() {
  return (
    <section id="services" className="section-y">
      <div className="container-page">
        <SectionHead
          eyebrow="Услуги"
          title="Грузовые перевозки в тентованных полуприцепах"
          text="Предлагаем услуги автопарка, укомплектованного только тентованными фурами (еврофурами) грузоподъемностью до 25 тонн. Наш профиль – доставка любых сухих (не требующих температурного режима) грузов."
        />
        <div className="mt-10 flex flex-wrap justify-center gap-5">
          {SERVICES.map((s) => {
            const Icon = SERVICE_ICONS[s.icon] ?? Truck;
            return (
              <article key={s.title} className="card-surface group w-full p-6 sm:w-[calc((100%-1.25rem)/2)] lg:w-[calc((100%-2.5rem)/3)]">
                <span className="grid size-11 place-items-center rounded-md bg-secondary text-primary">
                  <Icon className="size-5" />
                </span>
                <h3 className="mt-4 text-lg">{s.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{s.text}</p>
                <a href="#contacts" className="mt-4 inline-flex text-sm font-semibold text-primary hover:text-accent">
                  Связаться →
                </a>
              </article>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function Geography() {
  return (
    <section id="geography" className="section-y bg-surface">
      <div className="container-page">
        <SectionHead
          eyebrow="География"
          title="Популярные направления"
          text="Рейсы из Минска, Бреста, Гомеля, Витебска, Гродно и Могилёва в Москву, Санкт-Петербург, Смоленск, Тулу и другие города России (ориентировочные сроки доставки указаны с момента загрузки)."
        />
        <div className="mt-10">
          <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {ROUTES.map((r) => {
              const href = ROUTE_LINKS[`${r.from}-${r.to}`];
              const content = (
                <>
                  <span className="flex items-center gap-2 text-sm font-semibold">
                    <RouteIcon className="size-4 text-accent" />
                    {r.from} → {r.to}
                  </span>
                  <span className="shrink-0 whitespace-nowrap text-xs text-muted-foreground">{r.time}</span>
                </>
              );
              const className =
                "card-surface flex select-none items-center justify-between gap-3 p-4 transition-[background-color,border-color,color,box-shadow,transform] duration-150 hover:border-accent/40 hover:shadow-[var(--shadow-lift)] hover:bg-secondary hover:text-accent";
              return (
                <li key={`${r.from}-${r.to}`} className="contents">
                  {href ? (
                    <Link
                      to={href}
                      draggable={false}
                      onDragStart={(e) => e.preventDefault()}
                      className={`${className} cursor-pointer active:scale-[0.98] active:border-accent active:bg-secondary active:text-accent active:shadow-[var(--shadow-lift)] focus-visible:border-accent focus-visible:outline-none`}
                    >

                      {content}
                    </Link>

                  ) : (
                    <div className={className}>{content}</div>
                  )}
                </li>
              );
            })}
          </ul>
        </div>

      </div>
    </section>
  );
}

function About() {

  return (
    <section id="about" className="section-y">
      <div className="container-page grid items-center gap-10 lg:grid-cols-2">
        <div>
          <SectionHead
            eyebrow="О компании"
            title="Униспектрум – ваш надёжный партнёр"
            text="Наша компания прошла путь от пары машин до компании с парком из 11 фур. Имеем многолетний опыт перевозки грузов по Европе, Казахстану и России. У нас есть собственная ремонтная база для обслуживания рабочего транспорта, где мы сами контролируем его состояние, и не зависим от сторонних сервисов. За нашими плечами десятки тысяч успешных доставок и множество довольных клиентов."
          />
        </div>
        <img
          src={aboutImg}
          alt="Автопарк грузовых фур Униспектрум"
          width={1600}
          height={680}
          className="w-full rounded-xl object-cover shadow-[var(--shadow-card)]"
        />
      </div>
    </section>
  );
}

function Advantages() {
  return (
    <section id="advantages" className="section-y bg-ink text-ink-foreground">
      <div className="container-page">
        <SectionHead
          eyebrow="Преимущества"
          title="Почему клиенты остаются с нами"
          text="Прозрачные условия, качество работы и команда, на которую можно положиться."
          textClassName="text-ink-muted"
        />
        <div className="mt-10 grid gap-px overflow-hidden rounded-xl bg-white/10 sm:grid-cols-2 lg:grid-cols-3">
          {ADVANTAGES.map((a) => (
            <div key={a.title} className="bg-ink p-6 transition-colors hover:bg-white/5">
              <ShieldCheck className="size-6 text-accent" />
              <h3 className="mt-4 text-base">{a.title}</h3>
              <p className="mt-2 text-sm text-ink-muted">{a.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

function Process() {
  return (
    <section id="process" className="section-y">
      <div className="container-page">
        <SectionHead eyebrow="Как мы работаем" title="Пять шагов от заявки до выгрузки" />
        <ol className="mt-10 flex flex-wrap justify-center gap-5">
          {STEPS.map((s, i) => (
            <li key={s.title} className="card-surface relative w-full p-6 md:w-[calc((100%-2.5rem)/3)] lg:w-[calc((100%-5rem)/5)]">
              <span className="font-display text-4xl text-accent/40">0{i + 1}</span>
              <h3 className="mt-2 text-base">{s.title}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{s.text}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}


function Faq() {
  return (
    <section id="faq" className="section-y bg-surface">
      <div className="container-page grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">
        <SectionHead eyebrow="FAQ" title="Вопросы и ответы" text="Не нашли ответ на интересующий вас вопрос? Позвоните нам — подскажем за минуту!" />
        <div className="divide-y divide-border rounded-xl border border-border bg-card">
          {FAQ.map((f) => (
            <details key={f.q} className="group">
              <summary className="flex w-full cursor-pointer list-none items-center justify-between gap-4 p-5 text-sm font-semibold">
                {f.q}
                <ChevronDown className="size-4 shrink-0 text-accent transition-transform group-open:rotate-180" />
              </summary>
              <p className="px-5 pb-5 text-sm text-muted-foreground">{f.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}

function Contacts() {
  return (
    <section id="contacts" className="section-y">
      <div className="container-page">
        <SectionHead eyebrow="Контакты" title="Свяжитесь с нами" />
        <div className="mt-10 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <div className="card-surface space-y-5 p-6">
            <p className="flex gap-3 text-sm">
              <Clock className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Режим работы</strong>
                {WORK_HOURS}
              </span>
            </p>
            <p className="flex gap-3 text-sm">
              <Phone className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Телефоны</strong>
                <span className="flex flex-col gap-1">
                  {PHONES.map((p) => (
                    <a key={p.tel} href={`tel:${p.tel}`} className="hover:text-accent">
                      {p.display} — {p.note}
                    </a>
                  ))}
                </span>
              </span>
            </p>
            <p className="flex gap-3 text-sm">
              <Mail className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Электронная почта</strong>
                <a href={`mailto:${EMAIL}`} className="hover:text-accent">
                  {EMAIL}
                </a>
              </span>
            </p>
            <p className="flex gap-3 text-sm">
              <MapPin className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Местонахождение офиса</strong>
                {OFFICE_ADDRESS}
              </span>
            </p>
            <p className="flex gap-3 text-sm">
              <MapPin className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Юридический адрес</strong>
                {LEGAL_ADDRESS}
              </span>
            </p>
            <p className="flex gap-3 text-sm">
              <MapPin className="size-5 shrink-0 text-accent" />
              <span>
                <strong className="block">Почтовый адрес</strong>
                {POSTAL_ADDRESS}
              </span>
            </p>
          </div>
          <MapCard />
        </div>
      </div>
    </section>
  );
}

function MapCard() {
  const [active, setActive] = useState(false);
  const touchStart = useRef<{ x: number; y: number } | null>(null);

  // Пока карта активна — любой скролл страницы снова блокирует жесты карты
  useEffect(() => {
    if (!active) return;
    const onScroll = () => setActive(false);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [active]);

  return (
    <div className="relative overflow-hidden rounded-xl border border-border">
      <iframe
        title="Карта: офис Униспектрум, Зелёная улица 1А, офис 8А, деревня Большой Тростенец, Минский район"
        src="https://yandex.by/map-widget/v1/?ll=27.706568%2C53.848925&z=17&pt=27.706568,53.848925,pm2rdm"
        className="h-[380px] w-full lg:h-full"
      />
      {!active && (
        <button
          type="button"
          onClick={() => setActive(true)}
          onTouchStart={(e) => {
            if (e.touches.length >= 2) {
              touchStart.current = null;
              setActive(true);
              return;
            }
            const t = e.touches[0];
            touchStart.current = t ? { x: t.clientX, y: t.clientY } : null;
          }}
          onTouchMove={(e) => {
            // Жест двумя пальцами сразу включает карту без отдельного нажатия
            if (e.touches.length >= 2) {
              touchStart.current = null;
              setActive(true);
            }
          }}
          onTouchEnd={(e) => {
            const start = touchStart.current;
            const t = e.changedTouches[0];
            touchStart.current = null;
            if (!start || !t) return;
            // активируем только по настоящему тапу, а не по свайпу
            if (Math.hypot(t.clientX - start.x, t.clientY - start.y) < 10) setActive(true);
          }}
          aria-label="Включить взаимодействие с картой"
          className="group absolute inset-0 grid touch-pan-y place-items-center bg-transparent transition-colors hover:bg-ink/20 focus-visible:bg-ink/20 [@media(pointer:coarse)]:bg-ink/20"
        >
          <span className="max-w-[calc(100%-2rem)] rounded-md bg-ink/75 px-4 py-2 text-center text-sm font-semibold text-ink-foreground opacity-0 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100 [@media(pointer:coarse)]:opacity-100">
            Нажмите, чтобы работать с картой
          </span>
        </button>
      )}

    </div>
  );
}

function Landing() {
  return (
    <div className="min-h-screen">
      <Header />
      <main>
        <Hero />
        <Services />
        <Geography />
        <About />
        <Advantages />
        <Process />
        <Faq />
        <Contacts />
      </main>
      <Footer />
      <FloatingActions />
    </div>
  );
}
