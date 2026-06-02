#!/bin/bash
# Moa Mart — Full project file setup
# Written by Littlebird via Hermes bridge
cd ~/moa-mart
set -e
mkdir -p components
echo "🍜 Writing Moa Mart files..."

cat > app/globals.css << 'MOAEOF'
@import "tailwindcss";

@theme {
  --color-moa-red:     #E8003D;
  --color-moa-bg:      #07070F;
  --color-moa-surface: #0F0F1C;
  --color-moa-card:    #14142A;
  --color-moa-muted:   #6E6E9A;
  --color-moa-text:    #EEEEF8;

  --font-syne:  var(--font-syne-var), sans-serif;
  --font-inter: var(--font-inter-var), sans-serif;

  --animate-marquee: marquee 22s linear infinite;

  @keyframes marquee {
    from { transform: translateX(0); }
    to   { transform: translateX(-50%); }
  }
}

html { scroll-behavior: smooth; }
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
MOAEOF

cat > app/layout.tsx << 'MOAEOF'
import type { Metadata } from 'next'
import { Syne, Inter } from 'next/font/google'
import './globals.css'

const syne = Syne({
  subsets: ['latin'],
  weight: ['400', '600', '700', '800'],
  variable: '--font-syne-var',
})

const inter = Inter({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600'],
  variable: '--font-inter-var',
})

export const metadata: Metadata = {
  title: 'MOA MART — Korean Grocery, Sunnybank QLD',
  description: "Brisbane's favourite Korean grocery store.",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${syne.variable} ${inter.variable}`}>
      <body className="bg-moa-bg text-moa-text font-inter antialiased overflow-x-hidden">
        {children}
      </body>
    </html>
  )
}
MOAEOF

cat > app/page.tsx << 'MOAEOF'
import Navbar           from '@/components/Navbar'
import Hero             from '@/components/Hero'
import MarqueeBanner    from '@/components/MarqueeBanner'
import Categories       from '@/components/Categories'
import FeaturedProducts from '@/components/FeaturedProducts'
import About            from '@/components/About'
import DeliveryCTA      from '@/components/DeliveryCTA'
import Footer           from '@/components/Footer'

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <MarqueeBanner />
      <Categories />
      <FeaturedProducts />
      <About />
      <DeliveryCTA />
      <Footer />
    </main>
  )
}
MOAEOF

cat > components/Navbar.tsx << 'MOAEOF'
'use client'

import { useState, useEffect } from 'react'

const navLinks = ['Shop', 'Categories', 'About', 'Contact']

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-14 py-5 transition-all duration-300 ${
      scrolled ? 'bg-moa-bg/90 backdrop-blur-2xl border-b border-white/[0.07]' : 'bg-transparent'
    }`}>
      <div className="font-syne text-xl font-extrabold tracking-tight text-white select-none">
        모아마트&nbsp;·&nbsp;MOA<span className="text-moa-red">MART</span>
      </div>
      <ul className="hidden md:flex gap-9 list-none m-0 p-0">
        {navLinks.map((item) => (
          <li key={item}>
            <a href={`#${item.toLowerCase()}`}
              className="text-moa-muted hover:text-white text-[11px] font-medium tracking-[0.1em] uppercase transition-colors duration-200 no-underline">
              {item}
            </a>
          </li>
        ))}
      </ul>
      <a href="https://www.doordash.com/en/store/moa-mart-sunnybank-31537431/"
        target="_blank" rel="noopener noreferrer"
        className="bg-moa-red text-white px-6 py-2.5 rounded-full text-xs font-semibold tracking-wide shadow-[0_0_20px_rgba(232,0,61,0.3)] hover:opacity-[0.85] hover:-translate-y-px transition-all duration-200 no-underline">
        Order on DoorDash →
      </a>
    </nav>
  )
}
MOAEOF

cat > components/Hero.tsx << 'MOAEOF'
type HeroCard = { emoji: string; name: string; desc: string; badge: string }

const heroCards: HeroCard[] = [
  { emoji: '🍜', name: 'Samyang Buldak Dumplings', desc: 'Carbonara · 700g',     badge: '🔥 Hot Pick' },
  { emoji: '🥛', name: 'Binggrae Banana Milk',     desc: '6 Pack · $17.99',      badge: 'Fan Fave'   },
  { emoji: '🌶️', name: 'Dooki Teokbokki',         desc: 'Spicy & Sweet · 560g', badge: '$15.50'     },
  { emoji: '🌿', name: 'Wang Seaweed',             desc: 'Seasoned · 16 pack',   badge: '$16.30'     },
]

const stats = [
  { num: '200+',    label: 'Products'       },
  { num: '⭐ 4.8', label: 'Customer Rating' },
  { num: 'Weekly',  label: 'New Arrivals'   },
]

export default function Hero() {
  return (
    <section className="relative min-h-screen overflow-hidden grid grid-cols-1 lg:grid-cols-[1fr_440px] gap-10 items-center px-14 pt-32 pb-20">
      <div className="pointer-events-none absolute -top-40 -right-40 h-[700px] w-[700px] rounded-full bg-[radial-gradient(circle,rgba(232,0,61,0.28),transparent_65%)]" />
      <div className="pointer-events-none absolute -bottom-20 left-[15%] h-[450px] w-[450px] rounded-full bg-[radial-gradient(circle,rgba(80,0,220,0.1),transparent_65%)]" />
      <div className="relative z-10">
        <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-moa-red/[0.28] bg-moa-red/10 px-4 py-1.5 text-[11px] font-bold uppercase tracking-[0.1em] text-moa-red">
          📍 Robertson · Sunnybank QLD 4109
        </div>
        <h1 className="mb-8 font-syne text-[clamp(52px,7.5vw,100px)] font-extrabold leading-[0.92] tracking-[-3px] text-white">
          Taste<br /><span className="text-moa-red">Korea,</span><br />in Brisbane.
        </h1>
        <p className="mb-11 max-w-[480px] font-light text-lg leading-[1.75] text-moa-muted">
          Brisbane&apos;s favourite Korean grocery — new collections landing weekly, straight from Korea. From fire ramen to K-Beauty, all in one place.
        </p>
        <div className="mb-16 flex items-center gap-5">
          <a href="#shop" className="inline-block rounded-full bg-moa-red px-10 py-4 text-base font-semibold text-white shadow-[0_0_40px_rgba(232,0,61,0.28)] transition-all duration-200 hover:-translate-y-0.5 hover:shadow-[0_12px_55px_rgba(232,0,61,0.35)] no-underline">Shop Now</a>
          <a href="#categories" className="flex items-center gap-1.5 text-sm font-medium text-white/60 hover:text-white transition-colors duration-200 no-underline">Browse Categories →</a>
        </div>
        <div className="flex gap-10 border-t border-white/[0.07] pt-11">
          {stats.map((s) => (
            <div key={s.label}>
              <div className="mb-1.5 font-syne text-[34px] font-extrabold leading-none text-white">{s.num}</div>
              <div className="text-[11px] uppercase tracking-[0.1em] text-moa-muted">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
      <div className="relative z-10 hidden lg:grid grid-cols-2 gap-3.5 pt-8">
        {heroCards.map((card, i) => (
          <div key={card.name}
            style={{ marginTop: i === 1 ? '28px' : i === 3 ? '-28px' : undefined }}
            className="rounded-2xl border border-white/[0.07] bg-moa-card p-6 text-center cursor-pointer transition-all duration-300 hover:-translate-y-1.5 hover:border-moa-red/35 hover:shadow-[0_20px_50px_rgba(0,0,0,0.4)]">
            <div className="mb-3 text-5xl leading-none">{card.emoji}</div>
            <div className="mb-1 font-syne text-[13px] font-bold leading-tight text-white">{card.name}</div>
            <div className="mb-2.5 text-xs text-moa-muted">{card.desc}</div>
            <span className="inline-block rounded-full bg-moa-red px-2.5 py-1 text-[10px] font-bold uppercase tracking-wide text-white">{card.badge}</span>
          </div>
        ))}
      </div>
    </section>
  )
}
MOAEOF

cat > components/MarqueeBanner.tsx << 'MOAEOF'
const items = [
  'Ramen','Kimchi','Teokbokki','Banana Milk','Seaweed',
  'Dumplings','K-Beauty','Frozen Meals','Sauces','Rice Cakes','Pouch Drinks',
]

export default function MarqueeBanner() {
  const doubled = [...items, ...items]
  return (
    <div className="overflow-hidden bg-moa-red py-3.5">
      <div className="flex w-max animate-marquee">
        {doubled.map((item, i) => (
          <span key={i}
            className="whitespace-nowrap px-8 font-syne text-xs font-bold uppercase tracking-[0.15em] text-white/90 before:content-['★__']">
            {item}
          </span>
        ))}
      </div>
    </div>
  )
}
MOAEOF

cat > components/Categories.tsx << 'MOAEOF'
type Category = { icon: string; title: string; desc: string; count: string }

const categories: Category[] = [
  { icon: '🍜', title: 'Ramen & Noodles',    desc: 'Samyang, Nongshim, Ottogi and more. From mild to absolutely nuclear.',   count: '20+ items' },
  { icon: '🥟', title: 'Dumplings & Snacks', desc: 'Frozen, fried, steamed — all your Korean classics in one freezer.',       count: '15+ items' },
  { icon: '🥤', title: 'Drinks & Pouches',   desc: 'Banana milk, barley tea, yogurt drinks, and sparkling soju mixes.',       count: '30+ items' },
  { icon: '💄', title: 'K-Beauty',           desc: 'Sheet masks, serums, cleansers — curated fresh from Korea monthly.',      count: '12+ items' },
  { icon: '🍱', title: 'Ready Meals',        desc: 'Heat and eat Korean classics. Bibimbap, jjigae, sundubu — all here.',     count: '25+ items' },
  { icon: '🌿', title: 'Seaweed & Kimchi',   desc: 'Fresh kimchi, seasoned seaweed, and banchan sides to complete any meal.', count: '18+ items' },
  { icon: '🍚', title: 'Rice & Grains',      desc: 'Ottogi cooked rice packs, short-grain varieties, and mixed grains.',      count: '10+ items' },
  { icon: '🧃', title: 'Sauces & Pantry',    desc: 'Gochujang, doenjang, sesame oil, soy sauce — all the essentials.',       count: '22+ items' },
]

export default function Categories() {
  return (
    <section className="px-14 py-24" id="categories">
      <p className="mb-4 text-[11px] font-bold uppercase tracking-[0.15em] text-moa-red">What We Carry</p>
      <h2 className="mb-14 font-syne text-[clamp(34px,4vw,54px)] font-extrabold leading-[1.05] tracking-[-1.5px] text-white">
        Everything Korean.<br />Nothing Else.
      </h2>
      <div className="grid grid-cols-2 gap-3.5 md:grid-cols-4">
        {categories.map((cat) => (
          <a key={cat.title} href="#shop"
            className="group relative overflow-hidden rounded-2xl border border-white/[0.07] bg-moa-card px-6 py-8 text-moa-text no-underline transition-all duration-300 hover:-translate-y-1 hover:border-moa-red/35">
            <div className="pointer-events-none absolute inset-0 rounded-2xl bg-gradient-to-br from-moa-red/[0.07] to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
            <span className="absolute right-5 top-5 text-[11px] font-bold tracking-wide text-moa-red">{cat.count}</span>
            <span className="mb-5 block text-[42px] leading-none">{cat.icon}</span>
            <div className="relative z-10 mb-2 font-syne text-[18px] font-bold text-white">{cat.title}</div>
            <div className="relative z-10 text-[13px] leading-relaxed text-moa-muted">{cat.desc}</div>
          </a>
        ))}
      </div>
    </section>
  )
}
MOAEOF

cat > components/FeaturedProducts.tsx << 'MOAEOF'
type MiniProduct = { emoji: string; brand: string; name: string; price: string }

const miniProducts: MiniProduct[] = [
  { emoji: '🥛', brand: 'Binggrae', name: 'Banana Flavored Milk 6pk',     price: 'A$17.99' },
  { emoji: '🌿', brand: 'Wang',     name: 'Seasoned Seaweed 16pk',        price: 'A$16.30' },
  { emoji: '🌶️', brand: 'Dooki',   name: 'Spicy & Sweet Teokbokki 560g', price: 'A$15.50' },
  { emoji: '🍚', brand: 'Ottogi',   name: 'Cooked White Rice 4ea',        price: 'A$16.30' },
]

export default function FeaturedProducts() {
  return (
    <section className="px-14 pb-24" id="shop">
      <p className="mb-4 text-[11px] font-bold uppercase tracking-[0.15em] text-moa-red">Most Loved</p>
      <h2 className="mb-14 font-syne text-[clamp(34px,4vw,54px)] font-extrabold leading-[1.05] tracking-[-1.5px] text-white">Fan Favourites</h2>
      <div className="grid grid-cols-1 gap-3.5 lg:grid-cols-[1.35fr_1fr_1fr] lg:grid-rows-[auto_auto]">
        <div className="relative flex flex-col justify-end overflow-hidden rounded-3xl border border-moa-red/[0.22] bg-gradient-to-br from-[#180010] via-[#280018] to-[#12000C] p-12 lg:row-span-2">
          <div className="pointer-events-none absolute -right-20 -top-20 h-[360px] w-[360px] rounded-full bg-[radial-gradient(circle,rgba(232,0,61,0.22),transparent_65%)]" />
          <span className="relative z-10 mb-9 block text-[110px] leading-none drop-shadow-[0_16px_40px_rgba(232,0,61,0.5)]">🍜</span>
          <p className="relative z-10 mb-2.5 text-[11px] font-bold uppercase tracking-[0.15em] text-moa-red">🔥 #1 Best Seller</p>
          <h3 className="relative z-10 mb-2.5 font-syne text-2xl font-extrabold leading-[1.15] text-white">Samyang Buldak<br />Carbonara Dumplings</h3>
          <p className="relative z-10 mb-7 text-sm leading-[1.65] text-moa-muted">Spicy chicken carbonara meets the dumpling. 700g of pure beautiful chaos.</p>
          <div className="relative z-10 mb-5 font-syne text-3xl font-extrabold text-white">A$18.80{' '}<span className="ml-1.5 font-inter text-sm font-normal text-moa-muted">per pack</span></div>
          <button className="relative z-10 flex w-fit cursor-pointer items-center gap-2 rounded-full border-none bg-moa-red px-7 py-3.5 text-sm font-semibold text-white transition-all duration-200 hover:opacity-[0.85] hover:-translate-y-0.5">+ Add to Cart</button>
        </div>
        {miniProducts.map((prod) => (
          <div key={prod.name} className="flex cursor-pointer flex-col rounded-2xl border border-white/[0.07] bg-moa-card p-6 transition-all duration-200 hover:-translate-y-0.5 hover:border-moa-red/30">
            <div className="mb-3.5 text-[52px] leading-none">{prod.emoji}</div>
            <div className="mb-1.5 text-[11px] font-bold uppercase tracking-wide text-moa-red">{prod.brand}</div>
            <div className="flex-1 font-syne text-[16px] font-bold leading-snug text-white">{prod.name}</div>
            <div className="mt-5 flex items-center justify-between">
              <div className="font-syne text-xl font-extrabold text-white">{prod.price}</div>
              <button className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-full border-none bg-moa-red text-2xl leading-none text-white transition-transform duration-200 hover:scale-110">+</button>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
MOAEOF

cat > components/About.tsx << 'MOAEOF'
const features = [
  'New collections imported from Korea weekly',
  'Available on DoorDash for same-day delivery',
  'K-Beauty, food, drinks, pantry staples all in one',
  'Friendly local staff who genuinely know the products',
]

type InfoCard = { icon: string; title: string; desc: string }

const infoCards: InfoCard[] = [
  { icon: '📍', title: 'Find Us',            desc: '4 Zamia Street\nSunnybank QLD 4109'       },
  { icon: '🚗', title: 'Delivery',           desc: 'Available on DoorDash.\nFast and reliable.' },
  { icon: '🕐', title: 'Open Daily',         desc: '10:30 AM — 8:40 PM\n7 days a week'         },
  { icon: '🇰🇷', title: 'Direct from Korea', desc: 'Fresh stock arrivals\nevery week'           },
]

export default function About() {
  return (
    <div className="grid grid-cols-1 items-center gap-20 border-y border-white/[0.07] bg-moa-surface px-14 py-24 lg:grid-cols-2" id="about">
      <div>
        <h2 className="mb-6 font-syne text-[clamp(32px,3.5vw,48px)] font-extrabold leading-[1.08] tracking-[-1.5px] text-white">Your Korean corner store,<br />right in Robertson.</h2>
        <p className="mb-3.5 text-base leading-[1.8] text-moa-muted">Moa Mart is a locally-loved Korean grocery right in the heart of Sunnybank. We bring fresh collections directly from Korea every single week — your shelf always has something new.</p>
        <p className="text-base leading-[1.8] text-moa-muted">From K-Beauty to K-Snacks to full pantry essentials, we have it all in one tight-knit little shop. And yes — DoorDash delivers us straight to your door.</p>
        <ul className="mt-8 flex list-none flex-col gap-3 p-0">
          {features.map((f) => (
            <li key={f} className="flex items-center gap-3.5 text-[15px] text-moa-text">
              <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full border border-moa-red/25 bg-moa-red/[0.12] text-xs font-bold text-moa-red">✓</div>
              {f}
            </li>
          ))}
        </ul>
      </div>
      <div className="grid grid-cols-2 gap-3.5">
        {infoCards.map((card) => (
          <div key={card.title} className="rounded-2xl border border-white/[0.07] bg-moa-card p-8 text-center">
            <div className="mb-3.5 text-[34px]">{card.icon}</div>
            <div className="mb-1.5 font-syne text-[17px] font-bold text-white">{card.title}</div>
            <div className="whitespace-pre-line text-[13px] leading-[1.5] text-moa-muted">{card.desc}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
MOAEOF

cat > components/DeliveryCTA.tsx << 'MOAEOF'
export default function DeliveryCTA() {
  return (
    <div className="relative mx-14 my-24 flex flex-col items-center justify-between gap-10 overflow-hidden rounded-3xl border border-moa-red/[0.22] bg-gradient-to-br from-[#1A0010] to-[#240018] px-14 py-16 lg:flex-row" id="contact">
      <div className="pointer-events-none absolute -right-28 -top-28 h-[400px] w-[400px] rounded-full bg-[radial-gradient(circle,rgba(232,0,61,0.18),transparent_65%)]" />
      <div className="relative z-10">
        <p className="mb-4 text-[11px] font-bold uppercase tracking-[0.15em] text-moa-red">🚀 Ready when you are</p>
        <h2 className="mb-4 font-syne text-[clamp(28px,3vw,44px)] font-extrabold leading-[1.1] tracking-[-1.5px] text-white">Get Korean groceries<br />delivered today.</h2>
        <p className="max-w-[440px] text-base leading-[1.7] text-moa-muted">Too far to walk? We&apos;ll come to you. Order on DoorDash and get Moa Mart delivered to your door in under an hour.</p>
      </div>
      <div className="relative z-10 flex shrink-0 flex-col gap-3.5">
        <a href="https://www.doordash.com/en/store/moa-mart-sunnybank-31537431/" target="_blank" rel="noopener noreferrer"
          className="rounded-full bg-moa-red px-10 py-[18px] text-center text-[17px] font-bold text-white no-underline shadow-[0_0_40px_rgba(232,0,61,0.28)] transition-all duration-200 hover:-translate-y-0.5 hover:opacity-[0.88]">🛵 Order on DoorDash</a>
        <a href="https://maps.google.com/?q=4+Zamia+Street+Sunnybank+QLD+4109" target="_blank" rel="noopener noreferrer"
          className="rounded-full border border-white/[0.07] px-10 py-[14px] text-center text-sm font-medium text-moa-muted no-underline transition-all duration-200 hover:border-white/20 hover:text-white">📍 Get Directions</a>
      </div>
    </div>
  )
}
MOAEOF

cat > components/Footer.tsx << 'MOAEOF'
const links = [
  { label: 'Instagram', href: '#' },
  { label: 'Facebook',  href: 'https://www.facebook.com/moamartbrisbane/' },
  { label: 'DoorDash',  href: 'https://www.doordash.com/en/store/moa-mart-sunnybank-31537431/' },
]

export default function Footer() {
  return (
    <footer className="flex flex-col items-center justify-between gap-6 border-t border-white/[0.07] px-14 py-12 md:flex-row">
      <div className="font-syne text-[19px] font-extrabold text-white">
        모아마트&nbsp;·&nbsp;MOA<span className="text-moa-red">MART</span>
      </div>
      <div className="text-center text-[13px] leading-[1.7] text-moa-muted">
        <strong className="mb-1 block text-sm text-moa-text">📍 4 Zamia Street, Sunnybank QLD 4109</strong>
        Proudly serving Brisbane&apos;s Korean community since day one · © 2026 Moa Mart
      </div>
      <div className="flex gap-5">
        {links.map((link) => (
          <a key={link.label} href={link.href}
            target={link.href !== '#' ? '_blank' : undefined}
            rel="noopener noreferrer"
            className="text-[13px] font-medium text-moa-muted no-underline transition-colors duration-200 hover:text-moa-red">
            {link.label}
          </a>
        ))}
      </div>
    </footer>
  )
}
MOAEOF

echo ""
echo "✅ All 13 files written!"
echo "🚀 Opening Cursor..."
cursor .
