#!/usr/bin/env python3
"""Per #10 audit suggestion: MEMORY.md is 191 lines of dense index. 491 primitives.
Not graph-navigable. This generates a static MEMORY.html that renders the primitive
cross-reference DAG for outside adopters.

Inputs: substrate/memory/*.md
Output: substrate/MEMORY.html (single file, no dependencies)

Run on push (CI step) or manually:
    python substrate/scripts/render_memory_graph.py
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MEM_DIR = Path(__file__).resolve().parent.parent / "memory"
OUT_PATH = Path(__file__).resolve().parent.parent / "MEMORY.html"

REF_RE = re.compile(r'\[([PFJURO])·([a-z0-9-]+)\]')
NAME_RE = re.compile(r'^name:\s*(.+)$', re.MULTILINE)
DESC_RE = re.compile(r'^description:\s*(.+?)(?:\n[a-z_]+:|---)', re.MULTILINE | re.DOTALL)
TYPE_RE = re.compile(r'^type:\s*(\w+)', re.MULTILINE)


def slug_from_filename(p: Path) -> str:
    stem = p.stem
    if '_' not in stem:
        return stem
    prefix, _, slug = stem.partition('_')
    return slug


def parse_file(p: Path) -> dict:
    try:
        text = p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {}
    nm = NAME_RE.search(text)
    ty = TYPE_RE.search(text)
    dm = DESC_RE.search(text)
    refs = sorted({m.group(2) for m in REF_RE.finditer(text)})
    return {
        'file': p.name,
        'slug': slug_from_filename(p),
        'name': nm.group(1).strip() if nm else p.stem,
        'type': ty.group(1).strip() if ty else 'unknown',
        'description': (dm.group(1).strip()[:280] + '…') if dm else '',
        'refs': refs,
    }


def build_graph():
    """Build node list. Skip MEMORY.md + MEMORY_INDEX_*.md + MEMORY_FORMAT_SPEC.md (indexes
    + format-spec, not primitives). Class-eliminates 'index-files-rendered-as-primitives'
    confusion in the graph view."""
    nodes = []
    for p in sorted(MEM_DIR.glob('*.md')):
        # Skip the navigation files; they're index-of-primitives, not primitives themselves
        if p.name.startswith('MEMORY'):
            continue
        info = parse_file(p)
        if info:
            nodes.append(info)
    return nodes


def html_escape(s: str) -> str:
    """Escape HTML-special chars to class-eliminate XSS via primitive bodies (e.g., a
    description containing `</script>` would otherwise break out of the JSON literal
    when rendered into the inline JS context)."""
    return (s
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;'))


def sanitize_nodes(nodes):
    """Escape all user-facing string fields before they hit the HTML/JS template."""
    out = []
    for n in nodes:
        out.append({
            'file': html_escape(n['file']),
            'slug': html_escape(n['slug']),
            'name': html_escape(n['name']),
            'type': html_escape(n['type']),
            'description': html_escape(n['description']),
            'refs': [html_escape(r) for r in n['refs']],
        })
    return out


HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JARVIS Memory Graph</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
          margin: 0; padding: 0; background: #111; color: #ddd; }}
  header {{ position: sticky; top: 0; background: #000; padding: 12px 20px; border-bottom: 1px solid #333; }}
  header h1 {{ font-size: 16px; margin: 0; color: #fff; }}
  header input {{ background: #222; color: #fff; border: 1px solid #555; padding: 6px 10px; font: inherit; width: 100%; max-width: 600px; box-sizing: border-box; margin-top: 8px; }}
  .summary {{ color: #888; font-size: 12px; }}
  .filters {{ margin-top: 8px; }}
  .filters button {{ background: #222; color: #ccc; border: 1px solid #444; padding: 4px 10px; margin-right: 6px; cursor: pointer; font: inherit; }}
  .filters button.active {{ background: #4af; color: #000; border-color: #4af; }}
  main {{ display: grid; grid-template-columns: 1fr; gap: 12px; padding: 20px; max-width: 1200px; margin: 0 auto; }}
  .card {{ background: #1a1a1a; border: 1px solid #2a2a2a; border-radius: 6px; padding: 12px 16px; }}
  .card h2 {{ font-size: 14px; margin: 0; color: #fff; }}
  .meta {{ font-size: 11px; color: #888; margin: 4px 0; }}
  .type-feedback {{ border-left: 3px solid #f80; }}
  .type-primitive {{ border-left: 3px solid #4af; }}
  .type-project {{ border-left: 3px solid #5c5; }}
  .type-reference {{ border-left: 3px solid #c5c; }}
  .type-protocol {{ border-left: 3px solid #cc4; }}
  .type-user {{ border-left: 3px solid #888; }}
  .desc {{ color: #ccc; font-size: 13px; }}
  .refs {{ font-size: 11px; color: #6cf; margin-top: 6px; }}
  .refs span {{ display: inline-block; padding: 2px 6px; margin: 2px 4px 0 0; background: #1a2a3a; border-radius: 3px; cursor: pointer; }}
  .refs span:hover {{ background: #2a3a5a; }}
  .hidden {{ display: none; }}
</style>
</head>
<body>
<header>
  <h1>JARVIS Memory Graph</h1>
  <div class="summary">{n_nodes} primitives · types: {type_summary}</div>
  <input id="q" type="search" placeholder="search by name, slug, description…">
  <div class="filters" id="filters"></div>
</header>
<main id="grid"></main>
<script>
const NODES = {nodes_json};
const TYPES = [...new Set(NODES.map(n => n.type))].sort();
const grid = document.getElementById('grid');
const filters = document.getElementById('filters');
const q = document.getElementById('q');
let activeType = null;

function render() {{
  const term = q.value.toLowerCase();
  grid.innerHTML = '';
  for (const n of NODES) {{
    if (activeType && n.type !== activeType) continue;
    if (term && !((n.name + ' ' + n.slug + ' ' + n.description).toLowerCase().includes(term))) continue;
    // Round-9 class-fix: build via createElement + textContent. Class-eliminates
    // HTML injection entirely without HTML-escape gymnastics. Server-side escape
    // (sanitize_nodes) becomes a belt-and-suspenders defense; this is the suspenders.
    const card = document.createElement('div');
    card.className = 'card type-' + n.type;
    const h2 = document.createElement('h2'); h2.textContent = n.name; card.appendChild(h2);
    const meta = document.createElement('div'); meta.className = 'meta';
    meta.textContent = n.type + ' · ' + n.slug + ' · ';
    const code = document.createElement('code'); code.textContent = n.file; meta.appendChild(code);
    card.appendChild(meta);
    const desc = document.createElement('div'); desc.className = 'desc';
    if (n.description) {{ desc.textContent = n.description; }} else {{ const i = document.createElement('i'); i.textContent = 'no description'; desc.appendChild(i); }}
    card.appendChild(desc);
    if (n.refs.length) {{
      const refsDiv = document.createElement('div'); refsDiv.className = 'refs';
      refsDiv.appendChild(document.createTextNode('refs: '));
      for (const r of n.refs) {{
        const span = document.createElement('span');
        span.dataset.slug = r;
        span.textContent = r;
        refsDiv.appendChild(span);
        refsDiv.appendChild(document.createTextNode(' '));
      }}
      card.appendChild(refsDiv);
    }}
    grid.appendChild(card);
  }}
}}

for (const t of TYPES) {{
  const btn = document.createElement('button');
  btn.textContent = t + ' (' + NODES.filter(n => n.type === t).length + ')';
  btn.onclick = () => {{ activeType = (activeType === t ? null : t); for (const b of filters.children) b.classList.toggle('active', b.textContent.startsWith(activeType || '\\0')); render(); }};
  filters.appendChild(btn);
}}

q.addEventListener('input', render);
grid.addEventListener('click', e => {{
  if (e.target.tagName === 'SPAN' && e.target.dataset.slug) {{
    q.value = e.target.dataset.slug;
    activeType = null;
    for (const b of filters.children) b.classList.remove('active');
    render();
    window.scrollTo({{top: 0, behavior: 'smooth'}});
  }}
}});

render();
</script>
</body>
</html>
'''


def main() -> int:
    if not MEM_DIR.exists():
        print(f"memory dir not found: {MEM_DIR}", file=sys.stderr)
        return 1
    nodes = build_graph()
    type_counts = defaultdict(int)
    for n in nodes:
        type_counts[n['type']] += 1
    type_summary = ', '.join(f"{t}={c}" for t, c in sorted(type_counts.items()))
    safe_nodes = sanitize_nodes(nodes)
    html = HTML_TEMPLATE.format(
        n_nodes=len(nodes),
        type_summary=html_escape(type_summary),
        nodes_json=json.dumps(safe_nodes, ensure_ascii=False),
    )
    OUT_PATH.write_text(html, encoding='utf-8')
    print(f"rendered {len(nodes)} nodes -> {OUT_PATH}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
