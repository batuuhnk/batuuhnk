#!/usr/bin/env python3
"""Generates the animated SVG assets for the GitHub profile README."""
import math, os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

BG, PANEL, GRID, LINE = "#0A0F1C", "#0F172A", "#16213A", "#1E293B"
CYAN, GREEN, AMBER, TEXT, MUTED = "#22D3EE", "#34D399", "#F59E0B", "#E2E8F0", "#64748B"
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI','Inter',-apple-system,'Helvetica Neue',Arial,sans-serif"


def grid_defs(pid="g", size=24):
    return f'''<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">
  <path d="M {size} 0 L 0 0 0 {size}" fill="none" stroke="{GRID}" stroke-width="1"/></pattern>'''


def save(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote", name)


# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 380
    cx, cy, r = 960, 190, 118
    # roll scale ticks
    ticks = []
    for a in (-60, -45, -30, -20, -10, 0, 10, 20, 30, 45, 60):
        L = 14 if a % 30 == 0 else 8
        rad = math.radians(a - 90)
        x1, y1 = cx + (r + 6) * math.cos(rad), cy + (r + 6) * math.sin(rad)
        x2, y2 = cx + (r + 6 + L) * math.cos(rad), cy + (r + 6 + L) * math.sin(rad)
        ticks.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{TEXT}" stroke-width="2"/>')
    # pitch ladder
    ladder = []
    for p in (-20, -10, 10, 20):
        y = cy - p * 4
        w = 40 if abs(p) == 10 else 60
        ladder.append(f'<line x1="{cx-w/2}" y1="{y}" x2="{cx+w/2}" y2="{y}" stroke="#fff" stroke-width="2" opacity=".85"/>')
        ladder.append(f'<text x="{cx+w/2+6}" y="{y+4}" font-family="{MONO}" font-size="11" fill="#fff" opacity=".85">{abs(p)}</text>')
    for p in (-15, -5, 5, 15):
        y = cy - p * 4
        ladder.append(f'<line x1="{cx-12}" y1="{y}" x2="{cx+12}" y2="{y}" stroke="#fff" stroke-width="1.5" opacity=".6"/>')

    # PCB traces from text block towards instrument
    traces = [
        "M 600 96 H 700 L 730 126 H 820",
        "M 600 150 H 690 L 720 120 H 760 L 790 150 H 832",
        "M 600 230 H 700 L 730 260 H 830",
        "M 600 284 H 680 L 710 254 H 780 L 810 284 H 860",
        "M 600 190 H 828",
    ]
    tr_svg, pulse_svg = [], []
    for i, d in enumerate(traces):
        tr_svg.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2"/>')
        x0, y0 = d.split()[1], d.split()[2]
        tr_svg.append(f'<circle cx="{x0}" cy="{y0}" r="4" fill="{BG}" stroke="{LINE}" stroke-width="2"/>')
        col = CYAN if i % 2 == 0 else GREEN
        dur = 2.4 + i * 0.45
        pulse_svg.append(
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linecap="round" '
            f'stroke-dasharray="26 600" filter="url(#glow)">'
            f'<animate attributeName="stroke-dashoffset" from="26" to="-600" dur="{dur:.2f}s" begin="{i*0.35:.2f}s" repeatCount="indefinite"/></path>')

    tech = "STM32 · ARM CORTEX-M · FREERTOS · SENSOR FUSION · DO-178C"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Batuhan Kılıçlı — Embedded Software Engineer, Defense and Avionics">
<defs>
  {grid_defs()}
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="dial"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>
  <style>
    .in{{opacity:0;animation:in .8s ease-out forwards}}
    .d1{{animation-delay:.2s}} .d2{{animation-delay:.6s}} .d3{{animation-delay:1s}} .d4{{animation-delay:1.4s}} .d5{{animation-delay:1.8s}}
    @keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
    .cur{{animation:blink 1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
  </style>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)" opacity=".6"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="{LINE}" stroke-width="2"/>

<!-- corner registration marks -->
<g stroke="{MUTED}" stroke-width="2" opacity=".6">
  <path d="M 24 44 V 24 H 44"/><path d="M {W-44} 24 H {W-24} V 44"/>
  <path d="M 24 {H-44} V {H-24} H 44"/><path d="M {W-44} {H-24} H {W-24} V {H-44}"/>
</g>

{''.join(tr_svg)}
{''.join(pulse_svg)}

<!-- text block -->
<g transform="translate(0 24)">
<g font-family="{MONO}">
  <text class="in d1" x="64" y="98" font-size="15" fill="{CYAN}" letter-spacing="3">// EMBEDDED SOFTWARE ENGINEER</text>
</g>
<text class="in d2" x="60" y="166" font-family="{SANS}" font-size="62" font-weight="700" fill="{TEXT}">Batuhan Kılıçlı</text>
<text class="in d3" x="64" y="214" font-family="{MONO}" font-size="13" fill="{MUTED}" letter-spacing="0.6">{tech}</text>
<g class="in d4" font-family="{MONO}" font-size="15">
  <rect x="64" y="246" width="250" height="34" rx="6" fill="{PANEL}" stroke="{LINE}"/>
  <circle cx="84" cy="263" r="5" fill="{GREEN}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
  <text x="98" y="268" fill="{GREEN}">SYS OK</text>
  <text x="166" y="268" fill="{MUTED}">uptime 7y+</text>
  <rect class="cur" x="276" y="254" width="9" height="18" fill="{GREEN}"/>
</g>

</g>
<!-- attitude indicator -->
<circle cx="{cx}" cy="{cy}" r="{r+34}" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>
<g clip-path="url(#dial)">
  <g>
    <animateTransform attributeName="transform" type="rotate" values="-14 {cx} {cy};11 {cx} {cy};-6 {cx} {cy};16 {cx} {cy};-14 {cx} {cy}" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/>
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 -10;0 18;0 4;0 -16;0 -10" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1;.45 0 .55 1;.45 0 .55 1"/>
      <rect x="{cx-260}" y="{cy-260}" width="520" height="260" fill="#1E5A8A"/>
      <rect x="{cx-260}" y="{cy}" width="520" height="260" fill="#6B4423"/>
      <line x1="{cx-260}" y1="{cy}" x2="{cx+260}" y2="{cy}" stroke="#fff" stroke-width="2.5"/>
      {''.join(ladder)}
    </g>
  </g>
</g>
<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="3"/>
{''.join(ticks)}
<path d="M {cx} {cy-r-4} l -8 -14 h 16 z" fill="{AMBER}"/>
<!-- fixed aircraft symbol -->
<g stroke="{AMBER}" stroke-width="5" stroke-linecap="round" fill="none">
  <path d="M {cx-70} {cy} H {cx-28} L {cx-14} {cy+12}"/>
  <path d="M {cx+70} {cy} H {cx+28} L {cx+14} {cy+12}"/>
</g>
<circle cx="{cx}" cy="{cy}" r="4" fill="{AMBER}"/>
<text x="{cx}" y="{cy+r+30}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}" letter-spacing="2">AHRS · ATTITUDE</text>
</svg>'''


# ---------------------------------------------------------------- section titles
def section(num, title, sub):
    W, H = 1200, 72
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<style>
  .ln{{stroke-dasharray:1200;stroke-dashoffset:1200;animation:draw 1.6s ease-out .2s forwards}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
</style>
<text x="4" y="40" font-family="{MONO}" font-size="15" fill="{CYAN}" letter-spacing="2">{num}</text>
<text x="52" y="42" font-family="{SANS}" font-size="28" font-weight="700" fill="#8B98AE">{title}</text>
<text x="{W-4}" y="40" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}" letter-spacing="1.5">{sub}</text>
<line x1="4" y1="62" x2="{W-4}" y2="62" stroke="{LINE}" stroke-width="2"/>
<line class="ln" x1="4" y1="62" x2="{W-4}" y2="62" stroke="{CYAN}" stroke-width="2"/>
<circle cx="{W-4}" cy="62" r="3" fill="{CYAN}"><animate attributeName="opacity" values="0;0;1" keyTimes="0;.9;1" dur="1.8s" fill="freeze"/></circle>
</svg>'''


# ---------------------------------------------------------------- telemetry (what I build)
def telemetry():
    W, H = 1200, 330
    x0, x1 = 230, 1176
    span = x1 - x0
    rows = [
        ("CH1", "SENSOR FUSION", "IMU · AHRS · Kalman / complementary", CYAN, 60),
        ("CH2", "RTOS SCHEDULING", "FreeRTOS · DMA · deterministic timing", GREEN, 155),
        ("CH3", "BUS &amp; PROTOCOLS", "UART · SPI · I²C · RS-485 · MIL-STD-1553B", AMBER, 250),
    ]

    def sine(y, period, amp, noise=0.0):
        pts = []
        for x in range(0, span * 2 + period, 4):
            v = amp * math.sin(2 * math.pi * x / period) + noise * math.sin(2 * math.pi * x / 23.0) + noise * .6 * math.sin(2 * math.pi * x / 9.0)
            pts.append(f"{x0 + x:.0f},{y - v:.1f}")
        return "M " + " L ".join(pts)

    def rtos(y):
        # repeated pattern of task slices (period 240px)
        out = []
        pattern = [(0, 34, 1.0), (40, 70, .55), (116, 22, 1.0), (144, 46, .35), (196, 18, .75)]
        for k in range(0, span * 2 + 240, 240):
            for (o, w, op) in pattern:
                out.append(f'<rect x="{x0 + k + o}" y="{y-16}" width="{w}" height="32" rx="3" fill="{GREEN}" opacity="{op}"/>')
        return "".join(out)

    def digital(y):
        bits = "0110100111010010110011101001011010011010"
        pts, x = [f"{x0},{y+14}"], x0
        prev = "0"
        while x < x0 + span * 2 + 400:
            for b in bits:
                yy = y - 14 if b == "1" else y + 14
                if b != prev:
                    pts.append(f"{x},{yy}")
                x += 16
                pts.append(f"{x},{yy}")
                prev = b
        return "M " + " L ".join(pts)

    body = []
    for i, (ch, name, sub, col, y) in enumerate(rows):
        body.append(f'''<g font-family="{MONO}">
  <rect x="24" y="{y-34}" width="190" height="68" rx="8" fill="{PANEL}" stroke="{LINE}"/>
  <circle cx="44" cy="{y-14}" r="5" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="{1.2+i*.4}s" repeatCount="indefinite"/></circle>
  <text x="58" y="{y-9}" font-size="13" fill="{col}">{ch}</text>
  <text x="40" y="{y+16}" font-size="13" font-weight="700" fill="{TEXT}">{name}</text>
</g>
<text x="{x0+8}" y="{y-40}" font-family="{MONO}" font-size="11" fill="{MUTED}">{sub}</text>
<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE}" stroke-dasharray="4 6"/>''')
        if i == 0:
            wave = f'<path d="{sine(y, 240, 22, 3)}" fill="none" stroke="{col}" stroke-width="2.2" filter="url(#glow)"/>'
            shift = 240 * 3
        elif i == 1:
            wave = rtos(y)
            shift = 240 * 3
        else:
            wave = f'<path d="{digital(y)}" fill="none" stroke="{col}" stroke-width="2" filter="url(#glow)"/>'
            shift = 640
        body.append(f'''<g clip-path="url(#scope)"><g>
  <animateTransform attributeName="transform" type="translate" from="0 0" to="-{shift} 0" dur="{6+i*1.5}s" repeatCount="indefinite"/>
  {wave}
</g></g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Focus areas: sensor fusion, RTOS scheduling, bus protocols">
<defs>
  {grid_defs("g2", 20)}
  <clipPath id="scope"><rect x="{x0}" y="10" width="{span}" height="{H-20}"/></clipPath>
  <filter id="glow" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect x="{x0}" y="10" width="{span}" height="{H-20}" fill="url(#g2)" opacity=".7"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINE}" stroke-width="2"/>
{''.join(body)}
<line x1="{x0}" y1="10" x2="{x0}" y2="{H-10}" stroke="{LINE}" stroke-width="2"/>
</svg>'''


# ---------------------------------------------------------------- project cards
def card(title, desc1, desc2, tags, lang, lang_col, accent, status, placeholder=False):
    W, H = 580, 190
    tag_svg, tx = [], 24
    for t in tags:
        w = len(t) * 7.6 + 20
        tag_svg.append(f'<rect x="{tx}" y="132" width="{w:.0f}" height="26" rx="13" fill="{PANEL}" stroke="{LINE}"/>'
                       f'<text x="{tx + w/2:.0f}" y="149" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#94A3B8">{t}</text>')
        tx += w + 8
    border = f'stroke="{LINE}" stroke-dasharray="8 6"' if placeholder else f'stroke="{LINE}"'
    bar = "" if placeholder else f'''<rect x="0" y="0" width="6" height="{H}" rx="3" fill="{accent}"/>
<rect x="0" y="0" width="6" height="40" rx="3" fill="#fff" opacity=".55">
  <animate attributeName="y" values="0;{H-40};0" dur="4s" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></rect>'''
    lang_svg = "" if not lang else f'''<circle cx="{W-110}" cy="38" r="6" fill="{lang_col}"/>
<text x="{W-98}" y="43" font-family="{MONO}" font-size="13" fill="#94A3B8">{lang}</text>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BG}" {border} stroke-width="2"/>
{bar}
<text x="24" y="44" font-family="{MONO}" font-size="20" font-weight="700" fill="{TEXT if not placeholder else MUTED}">{title}</text>
{lang_svg}
<text x="24" y="82" font-family="{SANS}" font-size="15" fill="#94A3B8">{desc1}</text>
<text x="24" y="106" font-family="{SANS}" font-size="15" fill="#94A3B8">{desc2}</text>
{''.join(tag_svg)}
<text x="{W-24}" y="149" text-anchor="end" font-family="{MONO}" font-size="11" fill="{accent}" letter-spacing="1.5">{status}</text>
</svg>'''


# ---------------------------------------------------------------- timeline
def timeline():
    W, H = 1200, 250
    y0 = 2018 + 7 / 12  # Aug 2018
    yN = 2026 + 11 / 12
    X0, X1 = 60, 1140

    def X(year):
        return X0 + (year - y0) / (yN - y0) * (X1 - X0)

    segs = [
        ("INTERNSHIPS", "Anova R&amp;D · Kuasoft · Else Enerji", 2018 + 7/12, 2020 + 3/12, MUTED, 0),
        ("ANOVA R&amp;D TECHNOLOGIES", "Candidate → System → Embedded SW Engineer", 2020 + 3/12, 2025 + 3/12, CYAN, 1),
        ("HARPAX SYSTEM TECH.", "Embedded SW Engineer", 2025 + 3/12, 2026 + 9.5/12, GREEN, 2),
    ]
    out = []
    for name, sub, a, b, col, i in segs:
        xa, xb = X(a), X(b)
        w = xb - xa
        out.append(f'''<rect x="{xa:.1f}" y="118" width="{w-4:.1f}" height="14" rx="7" fill="{col}" opacity=".9" transform="scale(1 1)">
  <animate attributeName="width" from="0" to="{w-4:.1f}" dur=".8s" begin="{.3+i*.7:.1f}s" fill="freeze" calcMode="spline" keySplines=".2 0 .2 1"/>
  <set attributeName="width" to="0" begin="0s"/>
</rect>''')
        ly = 82 if i % 2 == 0 else 176
        anchor = "start"
        lx = xa
        if i == 2:
            anchor, lx = "end", xb + 10
        out.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".5s" begin="{.6+i*.7:.1f}s" fill="freeze"/>
  <line x1="{xa+2:.1f}" y1="{ly+12 if ly<118 else 136}" x2="{xa+2:.1f}" y2="{118 if ly<118 else ly-30}" stroke="{col}" stroke-width="1.5" opacity=".6"/>
  <text x="{lx:.1f}" y="{ly-14 if ly<118 else ly-6}" text-anchor="{anchor}" font-family="{MONO}" font-size="14" font-weight="700" fill="{TEXT}">{name}</text>
  <text x="{lx:.1f}" y="{ly+6 if ly<118 else ly+14}" text-anchor="{anchor}" font-family="{SANS}" font-size="13" fill="#94A3B8">{sub}</text>
</g>''')
    years = []
    for yr in range(2019, 2027):
        x = X(yr)
        years.append(f'<line x1="{x:.1f}" y1="112" x2="{x:.1f}" y2="138" stroke="{LINE}" stroke-width="1.5"/>'
                     f'<text x="{x:.1f}" y="{230}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">{yr}</text>')
    xn = X(2026 + 9.5 / 12)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career timeline 2018 to present">
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="15" fill="none" stroke="{LINE}" stroke-width="2"/>
<line x1="{X0}" y1="125" x2="{X1}" y2="125" stroke="{LINE}" stroke-width="2"/>
{''.join(years)}
{''.join(out)}
<circle cx="{xn:.1f}" cy="125" r="7" fill="{GREEN}"/>
<circle cx="{xn:.1f}" cy="125" r="7" fill="none" stroke="{GREEN}" stroke-width="2">
  <animate attributeName="r" values="7;20" dur="1.8s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/>
</circle>
<text x="{xn+16:.1f}" y="230" font-family="{MONO}" font-size="12" fill="{GREEN}">NOW</text>
</svg>'''


# ---------------------------------------------------------------- footer
def footer():
    W, H = 1200, 110
    pts = []
    for x in range(0, W + 1, 6):
        t = x / W
        env = math.sin(math.pi * t)
        v = env * 16 * math.sin(2 * math.pi * x / 90) * (0.6 + .4 * math.sin(2 * math.pi * x / 400))
        pts.append(f"{x},{40 - v:.1f}")
    d = "M " + " L ".join(pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Footer">
<style>
  .w{{stroke-dasharray:2600;stroke-dashoffset:2600;animation:d 3s ease-in-out forwards}}
  @keyframes d{{to{{stroke-dashoffset:0}}}}
</style>
<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2"/>
<path class="w" d="{d}" fill="none" stroke="{CYAN}" stroke-width="2"/>
<text x="{W/2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}" letter-spacing="2">while (1) {{ build(); measure(); verify(); }}</text>
</svg>'''


save("header.svg", header())
save("telemetry.svg", telemetry())
save("footer.svg", footer())

sections = [
    ("01", "About", "WHOAMI"),
    ("02", "What I build", "FOCUS AREAS"),
    ("03", "Tech stack", "TOOLCHAIN"),
    ("04", "Featured work", "PUBLIC REPOS"),
    ("05", "Currently", "IN PROGRESS"),
    ("06", "Get in touch", "CONTACT"),
]
for n, t, s in sections:
    save(f"section-{n}.svg", section(n, t, s))

save("card-px4.svg", card("px4-sitl-learning",
     "PX4 flight stack in SITL: uORB architecture, control loops,",
     "GPS-loss scenario and ULog flight-log analysis.",
     ["PX4", "SITL", "uORB", "ULog"], "Python", "#3572A5", GREEN, "ACTIVE"))
save("card-cpp.svg", card("cpp-temelleri",
     "C++ concepts used in PX4, each rebuilt side-by-side",
     "with its plain-C equivalent and memory-level notes.",
     ["C", "C++17", "OOP", "templates"], "C++", "#F34B7D", CYAN, "ACTIVE"))
save("card-handbook.svg", card("embedded-handbook",
     "Embedded C, RTOS, serial buses, MIL-STD-1553, sensor",
     "fusion, firmware architecture and DO-178C in 7 chapters.",
     ["C", "RTOS", "1553", "DO-178C"], "Markdown", "#083FA1", AMBER, "NEW"))
save("card-soon.svg", card("next project",
     "Next open-source embedded project is in the works:",
     "bare-metal drivers, RTOS architecture, test tooling.",
     ["STM32", "FreeRTOS"], "", "", MUTED, "COMING SOON", placeholder=True))
