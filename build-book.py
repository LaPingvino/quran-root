#!/usr/bin/env python3
"""
Build beautifully typeset PDF books for each language in the quran-root project.
Usage: python3 build-book.py [lang]     — build one language (en, pt, nl, eo, id, fy)
       python3 build-book.py all        — build all languages
"""

import os, sys, re, html

BASE = os.path.dirname(os.path.abspath(__file__))

LANG_META = {
    'en': {
        'title': 'The Recitation',
        'subtitle': 'A Root-Recovery Translation of the Qur\u2019an',
        'author': 'Joop Kiefte',
        'lang': 'en',
        'preface_title': 'Preface',
        'appendix_title': 'Root Discoveries',
        'toc_title': 'Contents',
        'surah_label': 'Surah',
    },
    'pt': {
        'title': 'A Recita\u00e7\u00e3o',
        'subtitle': 'Tradu\u00e7\u00e3o do Alcor\u00e3o pela Recupera\u00e7\u00e3o das Ra\u00edzes',
        'author': 'Joop Kiefte',
        'lang': 'pt',
        'preface_title': 'Pref\u00e1cio',
        'appendix_title': 'Descobertas das Ra\u00edzes',
        'toc_title': '\u00cdndice',
        'surah_label': 'Surata',
    },
    'nl': {
        'title': 'De Voordracht',
        'subtitle': 'Stamherwinning van de Koran',
        'author': 'Joop Kiefte',
        'lang': 'nl',
        'preface_title': 'Voorwoord',
        'appendix_title': 'Stamontdekkingen',
        'toc_title': 'Inhoud',
        'surah_label': 'Soera',
    },
    'eo': {
        'title': 'La Recitado',
        'subtitle': 'Radik-Rekupera Traduko de la Korano',
        'author': 'Joop Kiefte',
        'lang': 'eo',
        'preface_title': 'Anta\u016dparolo',
        'appendix_title': 'Radikaj Malkovroj',
        'toc_title': 'Enhavo',
        'surah_label': 'Surao',
    },
    'id': {
        'title': 'Bacaan',
        'subtitle': 'Terjemahan Pemulihan-Akar Al-Qur\u2019an',
        'author': 'Joop Kiefte',
        'lang': 'id',
        'preface_title': 'Kata Pengantar',
        'appendix_title': 'Penemuan Akar',
        'toc_title': 'Daftar Isi',
        'surah_label': 'Surah',
    },
    'fy': {
        'title': 'De Foardracht',
        'subtitle': 'Stamherwinning fan de Koran',
        'author': 'Joop Kiefte',
        'lang': 'fy',
        'preface_title': 'Foarwurd',
        'appendix_title': 'Stamûntdekkingen',
        'toc_title': 'Ynhald',
        'surah_label': 'Soera',
    },
}

# Preface blurbs per language (key root-recovery explanation)
PREFACE = {
    'en': (
        '<p>This translation recovers meanings hidden in the Arabic roots of the Qur\u2019an '
        '\u2014 meanings that centuries of conventional translation have obscured.</p>'
        '<p>Key choices: <em>kafir</em> (k-f-r) becomes \u201cthose who conceal\u201d; '
        '<em>muslim</em> (s-l-m) becomes \u201cthe Devoted\u201d; '
        '<em>hur</em> (h-w-r) becomes \u201cthe Returners\u201d \u2014 the same root as '
        'Jesus\u2019s disciples; <em>al-Qur\u2019an</em> (q-r-\u2019) becomes '
        '\u201cthe Recitation.\u201d</p>'
        '<p>Footnotes mark where root analysis reveals hidden connections. '
        'The appendix catalogues all root discoveries.</p>'
    ),
    'pt': (
        '<p>Esta tradu\u00e7\u00e3o recupera significados ocultos nas ra\u00edzes \u00e1rabes '
        'do Alcor\u00e3o \u2014 significados que s\u00e9culos de tradu\u00e7\u00e3o convencional obscureceram.</p>'
        '<p>Escolhas-chave: <em>kafir</em> (k-f-r) torna-se \u201cos que ocultam\u201d; '
        '<em>muslim</em> (s-l-m) torna-se \u201cos Devotos\u201d; '
        '<em>hur</em> (h-w-r) torna-se \u201cos Retornantes\u201d; '
        '<em>al-Qur\u2019an</em> (q-r-\u2019) torna-se \u201ca Recita\u00e7\u00e3o.\u201d</p>'
    ),
    'nl': (
        '<p>Deze vertaling herwint betekenissen verborgen in de Arabische wortels '
        'van de Koran \u2014 betekenissen die eeuwen van gangbare vertaling hebben verduisterd.</p>'
        '<p>Kernkeuzes: <em>kafir</em> (k-f-r) wordt \u201cdie verhullen\u201d; '
        '<em>muslim</em> (s-l-m) wordt \u201cde Toegewijden\u201d; '
        '<em>hur</em> (h-w-r) wordt \u201cde Weromkearden\u201d; '
        '<em>al-Qur\u2019an</em> (q-r-\u2019) wordt \u201cde Voordracht.\u201d</p>'
    ),
    'eo': (
        '<p>\u0108i tiu traduko reakiras signifojn ka\u015ditajn en la arabaj radikoj '
        'de la Korano \u2014 signifojn, kiujn jarcentoj da konvencia tradukado ombris.</p>'
        '<p>\u015closilaj elektoj: <em>kafir</em> (k-f-r) fari\u011das \u201ctiuj kiuj ka\u015das\u201d; '
        '<em>muslim</em> (s-l-m) fari\u011das \u201cla Dedi\u0109itoj\u201d; '
        '<em>hur</em> (h-w-r) fari\u011das \u201cla Reveni\u011dantoj\u201d; '
        '<em>al-Qur\u2019an</em> (q-r-\u2019) fari\u011das \u201cla Recitado.\u201d</p>'
    ),
    'id': (
        '<p>Terjemahan ini memulihkan makna yang tersembunyi dalam akar kata Arab '
        'Al-Qur\u2019an \u2014 makna yang berabad-abad terjemahan konvensional telah kaburkan.</p>'
        '<p>Pilihan kunci: <em>kafir</em> (k-f-r) menjadi \u201cyang menyembunyikan\u201d; '
        '<em>muslim</em> (s-l-m) menjadi \u201cyang berserah\u201d; '
        '<em>hur</em> (h-w-r) menjadi \u201cpara Kembali\u201d; '
        '<em>al-Qur\u2019an</em> (q-r-\u2019) menjadi \u201cBacaan.\u201d</p>'
    ),
    'fy': (
        '<p>Dizze oersetting herwint betsjuttingen ferburgen yn de Arabyske woartels '
        'fan de Koran \u2014 betsjuttingen dy\u2019t iuwen fan g\u00e4ngbere oersetting ferdústere hawwe.</p>'
        '<p>Kaaseleksjes: <em>kafir</em> (k-f-r) wurdt \u201cdy\u2019t ferbergje\u201d; '
        '<em>muslim</em> (s-l-m) wurdt \u201cde Tawijden\u201d; '
        '<em>hur</em> (h-w-r) wurdt \u201cde Weromkearden\u201d; '
        '<em>al-Qur\u2019an</em> (q-r-\u2019) wurdt \u201cde Foardracht.\u201d</p>'
    ),
}


def escape(text):
    return html.escape(text, quote=False)


def parse_surah(filepath):
    """Parse a surah .md file into (arabic_name, trans_name, basmala, verses)."""
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    arabic_name = ''
    trans_name = ''
    basmala = None
    verses = []

    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('# ') and not arabic_name:
            arabic_name = line[2:].strip()
        elif line.startswith('## ') and not trans_name:
            trans_name = line[3:].strip()
        elif re.match(r'^\d+\.\s', line):
            # numbered verse
            m = re.match(r'^(\d+)\.\s+(.*)', line)
            if m:
                verses.append((int(m.group(1)), m.group(2)))
        elif not verses and not line.startswith('#') and line.strip():
            # non-numbered text before verses = basmala
            if 'Nome de Deus' in line or 'Name of God' in line or 'Naam van God' in line or \
               'Nomo de Dio' in line or 'Nama Allah' in line or 'Namme fan God' in line or \
               'Misericordioso' in line or 'Merciful' in line or 'Barmhartige' in line or \
               'Kompatema' in line or 'Pengasih' in line or 'Barmhertige' in line:
                basmala = line.strip()

    return arabic_name, trans_name, basmala, verses


def extract_key_footnotes(comment_path, max_notes=8):
    """Extract a limited set of key observations from a comment file."""
    if not os.path.exists(comment_path):
        return []

    with open(comment_path, encoding='utf-8') as f:
        text = f.read()

    notes = []
    # Extract verse-level observations and root findings
    # Look for ### headings with verse references, and take the first paragraph
    sections = re.split(r'###\s+', text)
    for section in sections[1:]:  # skip header
        lines = section.strip().split('\n')
        if not lines:
            continue
        heading = lines[0].strip()
        # Collect first substantive paragraph
        para = []
        for line in lines[1:]:
            line = line.strip()
            if not line and para:
                break
            if line and not line.startswith('#') and not line.startswith('---'):
                para.append(line)
        if para:
            note_text = ' '.join(para)
            # Clean markdown artifacts
            note_text = re.sub(r'\*\*(.+?)\*\*', r'\1', note_text)  # bold
            note_text = re.sub(r'\*(.+?)\*', r'\1', note_text)  # italic
            note_text = re.sub(r'`(.+?)`', r'\1', note_text)  # code
            # Truncate very long notes
            if len(note_text) > 300:
                note_text = note_text[:297] + '...'
            notes.append(note_text)
            if len(notes) >= max_notes:
                break

    return notes


def markdown_to_html_simple(md_text):
    """Very basic markdown to HTML for roots appendix."""
    lines = md_text.split('\n')
    out = []
    in_list = False

    for line in lines:
        if line.startswith('# '):
            continue  # skip top-level heading
        elif line.startswith('### '):
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append(f'<h3>{escape(line[4:])}</h3>')
        elif line.startswith('## '):
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append(f'<h2>{escape(line[3:])}</h2>')
        elif line.startswith('- '):
            if not in_list:
                out.append('<ul>')
                in_list = True
            content = line[2:]
            # Bold
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            # Italic
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            out.append(f'<li>{content}</li>')
        elif line.startswith('---'):
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append('<hr class="ornament">')
        elif line.strip() == '':
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append('')
        else:
            # Regular paragraph
            content = line
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
            out.append(f'<p>{content}</p>')

    if in_list:
        out.append('</ul>')
    return '\n'.join(out)


def build_html(lang):
    """Build complete HTML for a language."""
    meta = LANG_META[lang]
    lang_dir = os.path.join(BASE, lang)
    comments_dir = os.path.join(lang_dir, 'comments')

    parts = []

    # HTML header
    parts.append(f'''<!DOCTYPE html>
<html lang="{meta['lang']}">
<head>
<meta charset="utf-8">
<title>{escape(meta['title'])}</title>
<link rel="stylesheet" href="book-style.css">
</head>
<body>
''')

    # Title page
    parts.append(f'''<div class="title-page">
<span class="book-ornament">\u25c6 \u2726 \u25c6 \u2726 \u25c6</span>
<div class="book-title">{escape(meta['title'])}</div>
<div class="book-subtitle">{escape(meta['subtitle'])}</div>
<div class="book-author">{escape(meta['author'])}</div>
<span class="title-footer-ornament">\u25c6 \u2726 \u25c6</span>
</div>
''')

    # Preface
    parts.append(f'''<div class="front-matter">
<h1>{escape(meta['preface_title'])}</h1>
{PREFACE.get(lang, PREFACE['en'])}
</div>
''')

    # Table of contents
    parts.append(f'<div class="toc">\n<h1>{escape(meta["toc_title"])}</h1>\n<ol>\n')

    # Pre-scan surahs for TOC
    surah_data = []
    for snum in range(1, 115):
        path = os.path.join(lang_dir, f'{snum:03d}.md')
        if not os.path.exists(path):
            continue
        arabic_name, trans_name, basmala, verses = parse_surah(path)
        comment_path = os.path.join(comments_dir, f'{snum:03d}-comments.md')
        footnotes = extract_key_footnotes(comment_path, max_notes=6)
        surah_data.append((snum, arabic_name, trans_name, basmala, verses, footnotes))
        display = f'{meta["surah_label"]} {snum}: {arabic_name}'
        if trans_name:
            display += f' \u2014 {trans_name}'
        parts.append(f'<li><a href="#surah-{snum}">{escape(display)}</a></li>\n')

    parts.append('</ol>\n</div>\n')

    # Surahs — page counter resets via CSS @page on first surah
    footnote_counter = 0
    for snum, arabic_name, trans_name, basmala, verses, footnotes in surah_data:
        surah_id = f'surah-{snum}'
        first_class = ' first-surah' if snum == 1 else ''
        parts.append(f'<div class="surah{first_class}" id="{surah_id}">\n')
        parts.append('<div class="surah-header">\n')
        parts.append(f'<span class="surah-number">{meta["surah_label"]} {snum}</span>\n')
        title_text = arabic_name
        parts.append(f'<h1>{escape(title_text)}</h1>\n')
        if trans_name:
            parts.append(f'<h2>{escape(trans_name)}</h2>\n')
        parts.append('</div>\n')  # surah-header
        parts.append('<span class="chapter-opening-ornament">\u25c6 \u25c6 \u25c6</span>\n')

        if basmala:
            parts.append(f'<p class="basmala">{escape(basmala)}</p>\n')

        parts.append('<div class="surah-body">\n<ol>\n')
        for vnum, vtext in verses:
            # Check if this verse has a footnote
            fn_html = ''
            if footnotes and vnum <= len(footnotes):
                # Attach footnotes to specific verses (distribute evenly)
                fn_index = None
                if len(verses) > 0 and len(footnotes) > 0:
                    # Map footnotes to verse positions roughly
                    fn_spacing = max(1, len(verses) // len(footnotes))
                    for fi, fn in enumerate(footnotes):
                        target_verse = (fi * fn_spacing) + 1
                        if vnum == target_verse:
                            fn_index = fi
                            break

                if fn_index is not None:
                    footnote_counter += 1
                    fn_text = escape(footnotes[fn_index])
                    fn_html = f'<span class="footnote">{fn_text}</span>'

            parts.append(f'<li>{escape(vtext)}{fn_html}</li>\n')
        parts.append('</ol>\n</div>\n')  # surah-body
        parts.append('</div>\n')  # surah

    # Appendix: Root discoveries
    roots_path = os.path.join(lang_dir, 'roots.md')
    if os.path.exists(roots_path):
        with open(roots_path, encoding='utf-8') as f:
            roots_md = f.read()
        parts.append(f'<div class="backmatter">\n')
        parts.append(f'<h1>{escape(meta["appendix_title"])}</h1>\n')
        parts.append(markdown_to_html_simple(roots_md))
        parts.append('</div>\n')

    # Colophon
    parts.append(f'''<div class="colophon">
<span class="colophon-ornament">\u25c6 \u2726 \u25c6 \u2726 \u25c6</span>
<p>{escape(meta['title'])}</p>
<p>{escape(meta['subtitle'])}</p>
<p>{escape(meta['author'])}</p>
<p style="margin-top: 1em; font-size: 7.5pt; color: #888;">
A root-recovery translation project<br>
github.com/LaPingvino/quran-root
</p>
</div>
''')

    parts.append('</body></html>')
    return ''.join(parts)


def build_lang(lang):
    """Build HTML and PDF for one language."""
    if lang not in LANG_META:
        print(f"Unknown language: {lang}")
        print(f"Available: {', '.join(LANG_META.keys())}")
        return False

    meta = LANG_META[lang]
    print(f"Building {meta['title']} ({lang})...")

    html_content = build_html(lang)
    html_path = os.path.join(BASE, f'book-{lang}.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"  HTML: {html_path}")

    # Generate PDF with weasyprint
    pdf_name = f'{meta["title"]} - {meta["subtitle"]}.pdf'
    pdf_path = os.path.join(BASE, pdf_name)

    try:
        import subprocess
        result = subprocess.run(
            ['weasyprint', html_path, pdf_path],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            size = os.path.getsize(pdf_path)
            print(f"  PDF: {pdf_path} ({size // 1024}K)")
        else:
            print(f"  PDF error: {result.stderr[:200]}")
            return False
    except FileNotFoundError:
        print("  weasyprint not found! Install with: pip install weasyprint")
        return False

    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 build-book.py [lang|all]")
        print(f"Languages: {', '.join(LANG_META.keys())}")
        sys.exit(1)

    target = sys.argv[1]
    if target == 'all':
        for lang in LANG_META:
            build_lang(lang)
    else:
        build_lang(target)
