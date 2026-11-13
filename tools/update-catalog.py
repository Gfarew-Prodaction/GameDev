"""Synchronize only UI records in the existing GameDev gallery."""
from pathlib import Path
import json
import re
from html import escape

root=Path(__file__).resolve().parents[1]
p=root/'index.html'
s=p.read_text()
items=json.loads((root/'UI/manifest.json').read_text())['items']
by_id={i['id']:i for i in items}
m=re.search(r'(<script type="application/json" id="catalog">)(.*?)(</script>)',s,re.S)
data=json.loads(m.group(2))
for item in items:
    row=data[item['id']]
    row.update(title=item['name'],priority=item['priority'],inScene=item['location'],integration=item['behavior'],
               file='UI/'+item['svg'],png='UI/'+item['png'],small='UI/'+item['preview'],handoff=item['handoff'])
    if 'dimensions' in item:
        row['dimensions']=item['dimensions']
s=s[:m.start(2)]+json.dumps(data,ensure_ascii=False)+s[m.end(2):]

def card(match):
    block=match.group(0)
    mid=re.search(r'data-open="(UI-\d{3})"',block)
    if not mid:return block
    item=by_id[mid[1]]
    block=re.sub(r'data-priority="[^"]*"',f'data-priority="{item["priority"]}"',block)
    block=re.sub(r'data-search="[^"]*"',f'data-search="{escape(item["id"]+" "+item["name"],quote=True)}"',block)
    block=re.sub(r'(<img )[^>]+>',lambda _:f'<img src="assets/previews/{item["id"]}.webp" alt="{escape(item["name"],quote=True)}" width="640" height="360" loading="lazy" decoding="async">',block)
    block=re.sub(r'(<h2>).*?(</h2>)',lambda m:m[1]+escape(item['name'])+m[2],block)
    block=re.sub(r'(<span>UI-\d{3}</span><span>)[^<]*(</span>)',lambda m:m[1]+item['priority']+m[2],block)
    block=re.sub(r'aria-label="Открыть UI-[^"]*"',f'aria-label="Открыть {item["id"]} {escape(item["name"],quote=True)}"',block)
    block=re.sub(r'<p class="card-dimensions">.*?</p>','',block,flags=re.S)
    if 'dimensions' in item:
        label='<p class="card-dimensions"><span>На экране · </span>'+escape(item['dimensions']['summary'])+'</p>'
        block=block.replace('</h2>','</h2>'+label,1)
    return block
s=re.sub(r'<article\b[^>]*data-kind="ui".*?</article>',card,s,flags=re.S)
s=s.replace('Скетчи кабинета и интерфейса','Модели кабинета и новый интерфейс')
s=s.replace('<title>Звезда‑57 · Скетчи</title>','<title>Звезда‑57 · Модели и интерфейс</title>')
if 'ui-catalog-link' not in s:
    s=s.replace('</div></header>','<p><a class="btn ui-catalog-link" href="UI/">Новый UI-каталог · 35 элементов →</a></p></div></header>',1)
    s=s.replace('</style>', '.ui-catalog-link{display:inline-block;margin-top:12px;text-decoration:none;border-color:var(--gold)}.ui-downloads{display:flex;flex-wrap:wrap;gap:14px}.ending-variants{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}.ending-variants button[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}.ending-variants[hidden],#ui-files[hidden]{display:none}.card[data-kind="ui"] .preview img{aspect-ratio:16/9}\n</style>',1)
    s=s.replace('<a class="download" id="download" download></a>','<a class="download" id="download" download></a><div class="ui-downloads" id="ui-files" hidden><a class="download" id="ui-png" download>PNG 1080p ↓</a><a class="download" id="ui-small" download>PNG 720p ↓</a><a class="download" href="UI/">Новый каталог →</a></div><div class="ending-variants" id="ending-variants" hidden></div>')
    s=s.replace('  if(!zoom.open)zoom.showModal();', '''  byId("ui-files").hidden=row.kind!=="ui";
  byId("ui-png").href=row.png||"";byId("ui-small").href=row.small||"";
  const variants=byId("ending-variants");variants.hidden=id!=="UI-030";variants.replaceChildren();
  if(id==="UI-030")for(const [key,label] of [["LAUNCH","Пуск"],["EMPTY_CITY","Пустой город"],["BLACKOUT","Авария"]]){
    const b=document.createElement("button");b.type="button";b.className="btn";b.textContent=label;
    b.setAttribute("aria-pressed",String(key==="LAUNCH"));
    b.addEventListener("click",()=>{art.src="UI/Previews/1080p/UI_030_ENDING_"+key+".png";download.href="UI/Source/Artboards/UI_030_ENDING_"+key+".svg";byId("ui-png").href=art.src;[...variants.children].forEach(el=>el.setAttribute("aria-pressed",String(el===b)));});variants.append(b);
  }
  if(!zoom.open)zoom.showModal();''')
    s=s.replace('zoom.addEventListener("click",e=>{if(e.target===zoom)zoom.close();});','zoom.addEventListener("click",e=>{if(e.target===zoom){const r=zoom.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)zoom.close();}});')
    s=s.replace('Источник — производственное ТЗ «Звезда‑57: Особый сектор», версия 2.1. Надписи в SVG остаются редактируемыми.', 'Модели — ТЗ «Звезда‑57: Особый сектор», версия 2.1. Новый UI — каталог 35 элементов от 13 ноября 2026. Надписи в SVG редактируются. <a href="UI/README.md">Передача UI в Unity</a>.')
if 'id="ui-dimensions"' not in s:
    s=s.replace('<h3>Связанные листы</h3>', '<section id="ui-dimensions" hidden><h3>Размеры по ТЗ</h3><p class="dimensions-base">База 1920 × 1080 px</p><dl><dt>На игровом экране</dt><dd id="ui-screen-size"></dd><dt>Расположение</dt><dd id="ui-screen-position"></dd><dt>Экспорт графики</dt><dd id="ui-export-size"></dd></dl></section><h3>Связанные листы</h3>',1)
    s=s.replace('</style>', '.caption .card-dimensions{margin:9px 0;color:var(--paper);font-size:.79rem;overflow-wrap:anywhere}.card-dimensions span{color:var(--muted)}#ui-dimensions[hidden]{display:none}#ui-dimensions dl{font-size:.86rem}#ui-dimensions dt{color:var(--gold);margin-top:14px}#ui-dimensions dd{margin:4px 0 0;color:var(--muted);overflow-wrap:anywhere}.dimensions-base{font-size:.8rem}\n</style>',1)
    s=s.replace('  byId("integration").hidden=!row.integration;', '''  byId("integration").hidden=!row.integration;
  byId("ui-dimensions").hidden=!row.dimensions;
  if(row.dimensions){
    byId("ui-screen-size").textContent=row.dimensions.screen;
    byId("ui-screen-position").textContent=row.dimensions.position;
    byId("ui-export-size").textContent=row.dimensions.export;
  }''',1)
p.write_text(s)
print('Updated all 35 UI records and previews. Preserved 50 model records and their relationships.')
