#!/usr/bin/env python3
"""
Gera o protótipo estático em ./ a partir de ../base-criacao/*.html (export UX Pilot / Next).
"""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "base-criacao"

END_TAIL = re.compile(r"\s*(width|height|title|class|style|frameborder|/>|>)")


def extract_srcdoc(raw: str) -> str | None:
    m = re.search(r"srcdoc\s*=\s*'", raw)
    if not m:
        return None
    start = m.end()
    i = start
    while True:
        pos = raw.find("'", i)
        if pos == -1:
            return None
        tail = raw[pos + 1 : pos + 80]
        if END_TAIL.match(tail):
            return html_lib.unescape(raw[start:pos])
        i = pos + 1


def extract_main_fragment(full: str) -> str:
    m = re.search(r"<main\b[^>]*>", full, re.I)
    if not m:
        raise ValueError("no <main> found")
    start = m.start()
    end = full.rindex("</main>") + len("</main>")
    return full[start:end]


def extract_title(full: str) -> str:
    m = re.search(r"<title>([^<]*)</title>", full, re.I)
    return m.group(1).strip() if m else "Grupo Conpav"


def blog_rename_tabs(fragment: str) -> str:
    return fragment.replace("switchTab(", "switchBlogTab(")


def make_head(*, title: str, plotly: bool) -> str:
    plotly_line = ""
    if plotly:
        plotly_line = (
            '    <script src="https://cdn.plot.ly/plotly-3.1.1.min.js"></script>\n'
        )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_lib.escape(title)}</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        window.FontAwesomeConfig = {{ autoReplaceSvg: "nest" }};
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="js/tailwind-config.js"></script>
{plotly_line}    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js" crossorigin="anonymous" referrerpolicy="no-referrer" defer></script>
</head>
"""


def nav_link(href: str, pid: str, label: str, active: str) -> str:
    if pid == active:
        cls = "text-sm font-semibold text-brand-accent border-b-2 border-brand-accent pb-1"
    else:
        cls = "text-sm font-medium text-brand-gray-600 hover:text-brand-navy transition-colors"
    return f'                <a href="{href}" class="{cls}">{label}</a>'


def make_header(active: str) -> str:
    items = [
        ("index.html", "index", "Início"),
        ("galeria.html", "galeria", "Galeria"),
        ("blog.html", "blog", "Blog"),
        ("sobre.html", "sobre", "Sobre"),
        ("contato.html", "contato", "Contato"),
        ("orcamento.html", "orcamento", "Orçamento"),
    ]
    nav_html = "\n".join(nav_link(h, p, l, active) for h, p, l in items)
    mobile_rows = "\n".join(
        f'            <a href="{h}" class="py-3 px-2 border-b border-brand-gray-100 text-brand-navy font-medium">{l}</a>'
        for h, p, l in items
    )
    extra_mobile = """
            <p class="text-xs font-bold text-brand-gray-400 uppercase tracking-wider mt-4 mb-2">Ferramentas</p>
            <a href="calculadora-concreto.html" class="py-2 px-2 text-brand-gray-600">Calculadora de concreto</a>
            <a href="calculadora-solar.html" class="py-2 px-2 text-brand-gray-600">Calculadora solar (UNISOLAR)</a>
            <a href="sorteio.html" class="py-2 px-2 text-brand-gray-600">Sorteios</a>
"""
    return f"""
    <header id="header" class="fixed top-0 w-full z-50 glass-card border-b border-brand-gray-200 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-6 lg:px-12 h-20 flex items-center justify-between">
            <a href="index.html" class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-brand-navy text-white flex items-center justify-center font-bold text-lg shadow-lg shadow-brand-navy/20">GC</div>
                <span class="font-bold text-xl tracking-tight text-brand-navy">Grupo Conpav</span>
            </a>

            <nav class="hidden md:flex items-center gap-8" aria-label="Principal">
{nav_html}
            </nav>

            <div class="flex items-center gap-4">
                <a href="orcamento.html" class="hidden lg:inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-brand-navy text-white text-sm font-semibold hover:bg-brand-navy/90 transition-all shadow-md shadow-brand-navy/10">
                    <i class="fa-solid fa-calculator" aria-hidden="true"></i>
                    Solicitar orçamento
                </a>
                <button type="button" id="nav-toggle" class="md:hidden text-brand-navy p-2 rounded-lg border border-brand-gray-200" aria-expanded="false" aria-controls="mobile-nav" aria-label="Abrir menu">
                    <i class="fa-solid fa-bars text-xl" aria-hidden="true"></i>
                </button>
            </div>
        </div>
    </header>

    <div id="mobile-nav" class="hidden fixed inset-x-0 top-20 z-40 md:hidden glass-card border-b border-brand-gray-200 shadow-lg max-h-[calc(100vh-5rem)] overflow-y-auto" role="dialog" aria-label="Menu">
        <nav class="flex flex-col px-6 py-4">
{mobile_rows}
{extra_mobile}
        </nav>
    </div>

    <a href="https://wa.me/5511300000000" target="_blank" rel="noopener noreferrer" class="fixed bottom-8 right-8 z-50 w-16 h-16 bg-[#25D366] rounded-full flex items-center justify-center text-white shadow-xl shadow-[#25D366]/30 hover:scale-110 transition-transform duration-300" aria-label="WhatsApp">
        <i class="fa-brands fa-whatsapp text-3xl" aria-hidden="true"></i>
        <span class="absolute top-0 right-0 w-4 h-4 bg-brand-accent rounded-full border-2 border-white animate-pulse" aria-hidden="true"></span>
    </a>
"""


PAGES: list[tuple[str, str, str, str, bool, list[str]]] = [
    # source_name, out_name, active_id, title_override (empty = from source), plotly, extra_js
    ("home.html", "index.html", "index", "Grupo Conpav — Início", False, []),
    ("sobre.html", "sobre.html", "sobre", "Grupo Conpav — Sobre o grupo", False, []),
    ("blog.html", "blog.html", "blog", "Grupo Conpav — Blog e notícias", False, ["js/blog.js"]),
    ("contato.html", "contato.html", "contato", "Grupo Conpav — Contato", False, ["js/contato.js"]),
    ("galeria.html", "galeria.html", "galeria", "Grupo Conpav — Galeria de obras", False, []),
    ("orcamento.html", "orcamento.html", "orcamento", "Grupo Conpav — Central de orçamentos", False, ["js/orcamento.js"]),
    (
        "calculadora-concreto.html",
        "calculadora-concreto.html",
        "concreto",
        "Grupo Conpav — Calculadora de concreto",
        False,
        [],
    ),
    (
        "calculadora-solar.html",
        "calculadora-solar.html",
        "solar",
        "Grupo Conpav — Calculadora solar UNISOLAR",
        True,
        ["js/calculadora-solar.js", "js/plotly-resize.js"],
    ),
    ("sorteio.html", "sorteio.html", "sorteio", "Grupo Conpav — Sorteios", False, []),
]


def aggregate_css() -> str:
    seen: set[str] = set()
    parts: list[str] = []
    for src_name, *_ in PAGES:
        raw = (BASE / src_name).read_text(encoding="utf-8", errors="replace")
        inner = extract_srcdoc(raw)
        if not inner:
            continue
        for m in re.finditer(r"<style>([\s\S]*?)</style>", inner, re.I):
            block = m.group(1).strip()
            key = re.sub(r"\s+", " ", block)
            if key in seen:
                continue
            seen.add(key)
            parts.append(f"/* source: {src_name} */\n{block}")
    return "\n\n".join(parts)


def main() -> None:
    (ROOT / "css").mkdir(parents=True, exist_ok=True)
    (ROOT / "js").mkdir(parents=True, exist_ok=True)

    (ROOT / "css" / "main.css").write_text(aggregate_css(), encoding="utf-8")
    print("wrote", (ROOT / "css" / "main.css").relative_to(ROOT.parent))

    for src_name, out_name, active, title_ov, plotly, extra_js in PAGES:
        src = BASE / src_name
        raw = src.read_text(encoding="utf-8", errors="replace")
        inner = extract_srcdoc(raw)
        if not inner:
            raise SystemExit(f"sem srcdoc: {src}")
        title = title_ov or extract_title(inner)
        main_frag = extract_main_fragment(inner)
        if src_name == "blog.html":
            main_frag = blog_rename_tabs(main_frag)

        body = f"""<body class="text-brand-navy font-sans flex flex-col m-0 p-0">
{make_header(active)}
{main_frag}
    <script src="js/main.js" defer></script>
"""
        for js in extra_js:
            body += f'    <script src="{js}" defer></script>\n'
        body += "</body>\n</html>\n"

        out_path = ROOT / out_name
        out_path.write_text(make_head(title=title, plotly=plotly) + body, encoding="utf-8")
        print("wrote", out_path.relative_to(ROOT.parent))


if __name__ == "__main__":
    main()
