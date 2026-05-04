#!/usr/bin/env python3
"""
Gera o protótipo estático em ../docs/ (GitHub Pages: branch main, pasta /docs)
a partir de ../base-criacao/*.html (export UX Pilot / Next).
"""
from __future__ import annotations

import html as html_lib
import re
import shutil
from pathlib import Path
from urllib.parse import quote

REPO = Path(__file__).resolve().parent.parent
SITE = Path(__file__).resolve().parent
ROOT = REPO / "docs"
BASE = REPO / "base-criacao"
STATIC_JS = SITE / "js"
CONCRETO_UI_CSS = SITE / "css" / "calculadora-concreto-ui.css"
HEADER_NAV_CSS = SITE / "css" / "header-nav.css"
CALC_MODAL_CSS = SITE / "css" / "calc-modal.css"

ORCAMENTO_SUB_ACTIVE = frozenset({"orcamento", "concreto", "solar"})

# WhatsApp: número informado "017 991744642" → internacional 55 + DDD 17 + 991744642
WHATSAPP_PHONE_E164 = "5517991744642"
_WHATSAPP_PREFILL = (
    "Olá! Estou entrando em contato pelo site do Grupo Conpav."
)
WHATSAPP_URL = (
    f"https://wa.me/{WHATSAPP_PHONE_E164}?text={quote(_WHATSAPP_PREFILL, safe='')}"
)

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


def augment_calculator_html(main_frag: str, src_name: str) -> str:
    """Injeta ids estáveis para os scripts das calculadoras (conteúdo do srcdoc)."""
    if src_name == "calculadora-concreto.html":
        h = main_frag
        h = h.replace(
            '<span class="text-5xl font-extrabold text-white leading-none">7.88</span>',
            '<span id="cc-out-volume" class="text-5xl font-extrabold text-white leading-none">7.88</span>',
            1,
        )
        h = h.replace(
            '<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-brand-accent/20 text-brand-accent text-xs font-semibold mt-2">\n'
            "                                <i class=\"fa-solid fa-circle-plus\"></i>\n"
            "                                Inclui 5% de perda\n"
            "                            </div>",
            '<div id="cc-out-loss-badge" class="inline-flex items-center gap-1.5 px-3 py-1 rounded bg-brand-accent/20 text-brand-accent text-xs font-semibold mt-2">\n'
            "                                <i class=\"fa-solid fa-circle-plus\"></i>\n"
            '                                <span id="cc-out-loss-text">Inclui 5% de perda</span>\n'
            "                            </div>",
            1,
        )
        h = h.replace(
            '<div class="text-2xl font-bold text-brand-gray-900">1 Caminhão</div>',
            '<div id="cc-out-trucks" class="text-2xl font-bold text-brand-gray-900">1 Caminhão</div>',
            1,
        )
        h = h.replace(
            '<div class="text-sm text-brand-gray-500">Betoneira padrão</div>',
            '<div id="cc-out-truck-hint" class="text-sm text-brand-gray-500">Betoneira padrão</div>',
            1,
        )
        h = h.replace(
            '<span class="text-brand-gray-500">Aplicação</span>\n'
            '                                    <span class="font-semibold text-brand-gray-900">',
            '<span class="text-brand-gray-500">Aplicação</span>\n'
            '                                    <span id="cc-out-app" class="font-semibold text-brand-gray-900">',
            1,
        )
        h = h.replace(
            '<span class="text-brand-gray-500">Resistência</span>\n'
            '                                    <span class="font-semibold text-brand-gray-900">',
            '<span class="text-brand-gray-500">Resistência</span>\n'
            '                                    <span id="cc-out-fck" class="font-semibold text-brand-gray-900">',
            1,
        )
        h = h.replace(
            '<span class="text-brand-gray-500">Bombeamento</span>\n'
            '                                    <span class="font-semibold text-brand-navy bg-brand-navy/5 px-2 py-0.5 rounded">',
            '<span class="text-brand-gray-500">Bombeamento</span>\n'
            '                                    <span id="cc-out-pump" class="font-semibold text-brand-navy bg-brand-navy/5 px-2 py-0.5 rounded">',
            1,
        )
        h = h.replace(
            '<span class="text-brand-gray-500">CEP</span>\n'
            '                                    <span class="font-semibold text-brand-gray-900">',
            '<span class="text-brand-gray-500">CEP</span>\n'
            '                                    <span id="cc-out-cep" class="font-semibold text-brand-gray-900">',
            1,
        )
        h = h.replace(
            'Comprimento (metros)</label>\n'
            '                                    <div class="relative">\n'
            '                                        <input type="number"',
            'Comprimento (metros)</label>\n'
            '                                    <div class="relative">\n'
            '                                        <input id="cc-in-length" type="number"',
            1,
        )
        h = h.replace(
            'Largura (metros)</label>\n'
            '                                    <div class="relative">\n'
            '                                        <input type="number"',
            'Largura (metros)</label>\n'
            '                                    <div class="relative">\n'
            '                                        <input id="cc-in-width" type="number"',
            1,
        )
        h = h.replace(
            "Espessura/Altura (centímetros)</label>\n"
            '                                    <div class="relative">\n'
            '                                        <input type="number"',
            "Espessura/Altura (centímetros)</label>\n"
            '                                    <div class="relative">\n'
            '                                        <input id="cc-in-thick" type="number"',
            1,
        )
        h = h.replace(
            '<input type="range" min="0" max="15" value="5" class="w-full">',
            '<input id="cc-in-loss" type="range" min="0" max="15" value="5" class="w-full">',
            1,
        )
        h = h.replace(
            '<label class="custom-label mb-0">Fator de Perda (Desperdício)</label>\n'
            '                                        <span class="text-sm font-bold text-brand-navy">5%</span>',
            '<label class="custom-label mb-0">Fator de Perda (Desperdício)</label>\n'
            '                                        <span id="cc-in-loss-label" class="text-sm font-bold text-brand-navy">5%</span>',
            1,
        )
        h = re.sub(
            r'(Classe de Resistência \(Fck\)</label>\s*<select)( class="custom-input)',
            r'\1 id="cc-in-fck"\2',
            h,
            count=1,
        )
        h = h.replace(
            '<input type="checkbox" class="w-5 h-5 rounded border-brand-gray-300 text-brand-navy focus:ring-brand-navy" checked>',
            '<input id="cc-in-pump" type="checkbox" class="w-5 h-5 rounded border-brand-gray-300 text-brand-navy focus:ring-brand-navy" checked>',
            1,
        )
        h = h.replace(
            '<label class="custom-label">CEP da Obra</label>\n'
            '                                <div class="flex gap-2">\n'
            '                                    <input type="text" class="custom-input" placeholder="00000-000">',
            '<label class="custom-label">CEP da Obra</label>\n'
            '                                <div class="flex gap-2">\n'
            '                                    <input id="cc-in-cep" type="text" class="custom-input" placeholder="00000-000">',
            1,
        )
        h = h.replace(
            "                        </div>\n"
            "                    </div>\n\n"
            "                    <!-- Step 2: Dimensions & Details -->",
            "                        </div>\n\n"
            '                        <div id="cc-seg-wrap" class="mt-8 pt-6 border-t border-brand-gray-100">\n'
            '                            <h3 class="text-sm font-semibold text-brand-gray-700 uppercase tracking-wider mb-4 text-center">Distribuição por segmento</h3>\n'
            '                            <div class="flex justify-center">\n'
            '                                <div class="flex flex-col items-center w-full max-w-[180px] mx-auto">\n'
            '                                    <div class="relative w-14 sm:w-16 h-44 bg-brand-gray-100 rounded-lg overflow-hidden border border-brand-gray-200">\n'
            '                                        <div id="cc-seg-fill" class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-brand-navy to-brand-navy/85 rounded-b-md transition-all duration-300" style="height: 100%;"></div>\n'
            "                                    </div>\n"
            '                                    <p id="cc-seg-caption" class="mt-3 text-xs font-bold text-brand-navy text-center leading-tight px-1">Laje / Piso</p>\n'
            '                                    <p class="text-[10px] text-brand-gray-500 text-center mt-1 leading-snug">Volume do tipo selecionado (barra única)</p>\n'
            "                                </div>\n"
            "                            </div>\n"
            "                        </div>\n\n"
            "                    </div>\n\n"
            "                    <!-- Step 2: Dimensions & Details -->",
            1,
        )
        return h

    if src_name == "calculadora-solar.html":
        h = main_frag
        h = h.replace(
            '<label class="custom-label mb-0">Valor Médio da Conta de Luz (Mensal)</label>',
            '<label id="cs-label-main" class="custom-label mb-0">Valor Médio da Conta de Luz (Mensal)</label>',
            1,
        )
        h = re.sub(
            r'<span class="text-lg font-bold text-brand-navy">R\$ [\d.,]+</span>',
            '<span id="cs-disp-main" class="text-lg font-bold text-brand-navy">R$ 850,00</span>',
            h,
            count=1,
        )
        h = h.replace(
            '<input type="range" min="100" max="5000" step="50" value="850" class="w-full">',
            '<input id="cs-main-range" type="range" min="100" max="5000" step="50" value="850" class="w-full">',
            1,
        )
        h = h.replace(
            '<div class="text-2xl font-bold text-white">6.4 <span class="text-sm text-brand-gray-400 font-normal">kWp</span></div>',
            '<div class="text-2xl font-bold text-white"><span id="cs-out-kwp">6.4</span> <span class="text-sm text-brand-gray-400 font-normal">kWp</span></div>',
            1,
        )
        h = h.replace(
            '<div class="text-2xl font-bold text-white">820 <span class="text-sm text-brand-gray-400 font-normal">kWh</span></div>',
            '<div class="text-2xl font-bold text-white"><span id="cs-out-gen">820</span> <span class="text-sm text-brand-gray-400 font-normal">kWh</span></div>',
            1,
        )
        h = h.replace(
            '<div class="text-2xl font-bold text-white">32 <span class="text-sm text-brand-gray-400 font-normal">m²</span></div>',
            '<div class="text-2xl font-bold text-white"><span id="cs-out-area">32</span> <span class="text-sm text-brand-gray-400 font-normal">m²</span></div>',
            1,
        )
        h = h.replace(
            '<div class="text-2xl font-bold text-white">12 <span class="text-sm text-brand-gray-400 font-normal">und</span></div>',
            '<div class="text-2xl font-bold text-white"><span id="cs-out-mod">12</span> <span class="text-sm text-brand-gray-400 font-normal">und</span></div>',
            1,
        )
        h = h.replace(
            '<div class="text-xl font-bold text-[#10B981]">R$ 9.690,00</div>',
            '<div class="text-xl font-bold text-[#10B981]"><span id="cs-out-saving">R$ 9.690,00</span></div>',
            1,
        )
        h = h.replace(
            '<div class="text-lg font-bold text-white">R$ 85,00</div>',
            '<div class="text-lg font-bold text-white"><span id="cs-out-newbill">R$ 85,00</span></div>',
            1,
        )
        h = h.replace(
            '<span class="text-sm font-bold text-brand-accent">3.5 a 4 anos</span>',
            '<span id="cs-out-payback" class="text-sm font-bold text-brand-accent">3.5 a 4 anos</span>',
            1,
        )
        h = h.replace(
            '<div class="bg-brand-accent h-2 rounded-full" style="width: 25%"></div>',
            '<div id="cs-out-payback-bar" class="bg-brand-accent h-2 rounded-full" style="width: 25%"></div>',
            1,
        )
        h = h.replace(
            '<div class="text-sm font-bold text-white">120 Árvores salvas</div>',
            '<div class="text-sm font-bold text-white"><span id="cs-out-trees">120</span> Árvores salvas</div>',
            1,
        )
        h = h.replace(
            '<div class="text-3xl font-bold text-brand-gray-900 mb-1">820 <span class="text-sm font-normal text-brand-gray-500">kWh/mês</span></div>',
            '<div class="text-3xl font-bold text-brand-gray-900 mb-1"><span id="cs-side-monthly">820</span> <span class="text-sm font-normal text-brand-gray-500">kWh/mês</span></div>',
            1,
        )
        return h

    return main_frag


def augment_orcamento_html(main_frag: str) -> str:
    """Destaca as calculadoras interativas como parte do fluxo de orçamento."""
    needle = "        <!-- Calculators Content Area -->"
    if needle not in main_frag:
        return main_frag
    insert = """        <section class="max-w-7xl mx-auto px-6 lg:px-12 py-6 relative z-10">
            <div class="rounded-2xl border border-brand-navy/15 bg-brand-navy/5 px-6 py-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <p class="text-sm text-brand-gray-700 max-w-xl">
                    <span class="font-semibold text-brand-navy">Calculadoras</span>
                    — estimativas interativas para apoiar seu pedido de orçamento na central abaixo.
                </p>
                <div class="flex flex-wrap gap-3 shrink-0">
                    <a href="calculadora-concreto.html" data-modal-title="Calculadora de concreto" class="js-calc-modal inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-white border border-brand-gray-200 text-sm font-semibold text-brand-navy hover:border-brand-navy/40 transition-colors">
                        <i class="fa-solid fa-cube" aria-hidden="true"></i>
                        Concreto
                    </a>
                    <a href="calculadora-solar.html" data-modal-title="Calculadora solar (UNISOLAR)" class="js-calc-modal inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-brand-navy text-white text-sm font-semibold hover:bg-brand-navy/90 transition-colors">
                        <i class="fa-solid fa-solar-panel" aria-hidden="true"></i>
                        Solar (UNISOLAR)
                    </a>
                </div>
            </div>
        </section>

"""
    return main_frag.replace(needle, insert + needle, 1)


def augment_calculator_parent_strip(main_frag: str) -> str:
    """Vincula visualmente as calculadoras à central de orçamentos."""
    needle = '<main class="flex-grow pt-24 pb-20 grid-bg">\n        \n        <!-- Calculator Hero Section -->'
    if needle not in main_frag:
        return main_frag
    strip = """        <div class="max-w-7xl mx-auto px-6 lg:px-12 pt-4">
            <nav aria-label="Navegação secundária" class="text-sm">
                <a href="orcamento.html" class="inline-flex items-center gap-2 text-brand-gray-600 hover:text-brand-navy font-medium transition-colors">
                    <i class="fa-solid fa-arrow-left-long text-xs opacity-70" aria-hidden="true"></i>
                    Central de orçamentos
                </a>
            </nav>
        </div>

"""
    return main_frag.replace(needle, '<main class="flex-grow pt-24 pb-20 grid-bg">\n' + strip + "\n        <!-- Calculator Hero Section -->", 1)


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


def _orcamento_sub_link_desktop(
    href: str, pid: str, label: str, active: str, *, calc_modal: bool = False
) -> str:
    if pid == active:
        acl = "block px-4 py-2.5 text-sm rounded-lg mx-1 font-semibold text-brand-accent bg-brand-navy/5"
    else:
        acl = "block px-4 py-2.5 text-sm rounded-lg mx-1 text-brand-gray-700 hover:bg-brand-gray-50 hover:text-brand-navy"
    if calc_modal:
        acl += " js-calc-modal"
    extra = f' data-modal-title="{html_lib.escape(label)}"' if calc_modal else ""
    return f'                            <a href="{href}" role="menuitem" class="{acl}"{extra}>{label}</a>'


def _orcamento_sub_link_mobile(
    href: str, pid: str, label: str, active: str, *, calc_modal: bool = False
) -> str:
    if pid == active:
        acl = "block py-2.5 px-2 rounded-lg text-sm font-semibold text-brand-accent bg-brand-navy/5"
    else:
        acl = "block py-2.5 px-2 rounded-lg text-sm text-brand-gray-700 hover:bg-brand-gray-50"
    if calc_modal:
        acl += " js-calc-modal"
    extra = f' data-modal-title="{html_lib.escape(label)}"' if calc_modal else ""
    return f'            <a href="{href}" class="{acl}"{extra}>{label}</a>'


def _orcamento_dropdown_desktop(active: str) -> str:
    orc_active = active in ORCAMENTO_SUB_ACTIVE
    sum_cls = (
        "list-none cursor-pointer inline-flex items-center gap-1.5 text-sm font-semibold text-brand-accent border-b-2 border-brand-accent pb-1"
        if orc_active
        else "list-none cursor-pointer inline-flex items-center gap-1.5 text-sm font-medium text-brand-gray-600 hover:text-brand-navy border-b-2 border-transparent pb-1 transition-colors"
    )
    subs = "\n".join(
        [
            _orcamento_sub_link_desktop("orcamento.html", "orcamento", "Central de orçamentos", active),
            _orcamento_sub_link_desktop(
                "calculadora-concreto.html",
                "concreto",
                "Calculadora de concreto",
                active,
                calc_modal=True,
            ),
            _orcamento_sub_link_desktop(
                "calculadora-solar.html",
                "solar",
                "Calculadora solar (UNISOLAR)",
                active,
                calc_modal=True,
            ),
        ]
    )
    return f"""                <details class="relative group nav-orcamento-wrap">
                    <summary class="{sum_cls}">
                        Orçamento
                        <i class="fa-solid fa-chevron-down text-xs opacity-70 nav-orcamento-chevron transition-transform duration-200" aria-hidden="true"></i>
                    </summary>
                    <div class="absolute left-0 top-full pt-2 z-50 w-64 min-w-[14rem]" role="group" aria-label="Orçamento e calculadoras">
                        <div class="rounded-xl border border-brand-gray-200 bg-white shadow-lg py-2">
{subs}
                        </div>
                    </div>
                </details>"""


def make_header(active: str) -> str:
    items_main = [
        ("index.html", "index", "Início"),
        ("galeria.html", "galeria", "Galeria"),
        ("blog.html", "blog", "Blog"),
        ("sobre.html", "sobre", "Sobre"),
        ("contato.html", "contato", "Contato"),
    ]
    nav_html = "\n".join(nav_link(h, p, l, active) for h, p, l in items_main)
    nav_html += "\n" + _orcamento_dropdown_desktop(active)
    mobile_rows = "\n".join(
        f'            <a href="{h}" class="py-3 px-2 border-b border-brand-gray-100 text-brand-navy font-medium">{l}</a>'
        for h, p, l in items_main
    )
    extra_mobile = (
        """
            <div class="mt-4 pt-2 border-t border-brand-gray-100">
            <p class="text-xs font-bold text-brand-gray-400 uppercase tracking-wider mb-2">Orçamento</p>
"""
        + "\n".join(
            [
                _orcamento_sub_link_mobile("orcamento.html", "orcamento", "Central de orçamentos", active),
                _orcamento_sub_link_mobile(
                    "calculadora-concreto.html",
                    "concreto",
                    "Calculadora de concreto",
                    active,
                    calc_modal=True,
                ),
                _orcamento_sub_link_mobile(
                    "calculadora-solar.html",
                    "solar",
                    "Calculadora solar (UNISOLAR)",
                    active,
                    calc_modal=True,
                ),
            ]
        )
        + """
            </div>
            <p class="text-xs font-bold text-brand-gray-400 uppercase tracking-wider mt-4 mb-2">Outros</p>
"""
        + _orcamento_sub_link_mobile("sorteio.html", "sorteio", "Sorteios", active)
        + "\n"
    )
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

    <div id="calc-modal" class="hidden fixed inset-0 z-[100] flex flex-col justify-center p-0 sm:p-4 md:p-6" aria-hidden="true" aria-labelledby="calc-modal-title">
        <div id="calc-modal-backdrop" class="absolute inset-0 bg-brand-navy/55 backdrop-blur-[2px]"></div>
        <div class="relative z-10 flex min-h-0 flex-1 flex-col w-full max-w-6xl mx-auto sm:max-h-[min(92vh,900px)] sm:rounded-2xl sm:shadow-2xl sm:border sm:border-brand-gray-200 bg-white overflow-hidden">
            <div class="flex shrink-0 items-center justify-between gap-3 border-b border-brand-gray-100 bg-white px-4 py-3">
                <span id="calc-modal-title" class="truncate text-base font-semibold text-brand-navy">Calculadora</span>
                <button type="button" id="calc-modal-close" class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-brand-gray-200 text-brand-gray-600 hover:bg-brand-gray-50 hover:text-brand-navy" aria-label="Fechar calculadora">
                    <i class="fa-solid fa-xmark text-lg" aria-hidden="true"></i>
                </button>
            </div>
            <iframe id="calc-modal-frame" class="min-h-0 flex-1 w-full border-0 bg-white" title="Calculadora"></iframe>
        </div>
    </div>

    <a href="{WHATSAPP_URL}" target="_blank" rel="noopener noreferrer" class="fixed bottom-8 right-8 z-50 w-16 h-16 bg-[#25D366] rounded-full flex items-center justify-center text-white shadow-xl shadow-[#25D366]/30 hover:scale-110 transition-transform duration-300" aria-label="WhatsApp">
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
        ["js/calculadora-concreto.js"],
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


def copy_static_js() -> None:
    if not STATIC_JS.is_dir():
        raise SystemExit(f"pasta JS de origem inexistente: {STATIC_JS}")
    dest = ROOT / "js"
    dest.mkdir(parents=True, exist_ok=True)
    for f in STATIC_JS.glob("*.js"):
        shutil.copy2(f, dest / f.name)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "css").mkdir(parents=True, exist_ok=True)
    (ROOT / "js").mkdir(parents=True, exist_ok=True)

    copy_static_js()
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    css_bundle = aggregate_css()
    if CONCRETO_UI_CSS.is_file():
        css_bundle += "\n\n" + CONCRETO_UI_CSS.read_text(encoding="utf-8")
    if HEADER_NAV_CSS.is_file():
        css_bundle += "\n\n" + HEADER_NAV_CSS.read_text(encoding="utf-8")
    if CALC_MODAL_CSS.is_file():
        css_bundle += "\n\n" + CALC_MODAL_CSS.read_text(encoding="utf-8")
    (ROOT / "css" / "main.css").write_text(css_bundle, encoding="utf-8")
    print("wrote", (ROOT / "css" / "main.css").relative_to(REPO))

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
        if src_name in ("calculadora-concreto.html", "calculadora-solar.html"):
            main_frag = augment_calculator_html(main_frag, src_name)
            main_frag = augment_calculator_parent_strip(main_frag)
        if src_name == "orcamento.html":
            main_frag = augment_orcamento_html(main_frag)

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
        print("wrote", out_path.relative_to(REPO))


if __name__ == "__main__":
    main()
