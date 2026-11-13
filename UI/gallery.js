const $ = s => document.querySelector(s);
const {items} = await fetch('manifest.json?v=dimensions-20261113').then(r => {
  if (!r.ok) throw new Error('Не удалось загрузить каталог');
  return r.json();
});
const groups = [
  ['all','Все элементы',1,35],['navigation','Навигация',1,8],['documents','Документы',9,14],
  ['phone','Связь',15,18],['map','Карта и службы',19,25],['shift','Смены и резервы',26,30],['system','Система',31,35]
];
let group='all', visible=items, current=0, activeVariant=null;
const viewer=$('#viewer');
for(const [id,label] of groups){
  const b=document.createElement('button');b.type='button';b.textContent=label;b.dataset.group=id;
  b.setAttribute('aria-pressed',String(id===group));
  b.addEventListener('click',()=>{group=id;document.querySelectorAll('[data-group]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.group===id)));render()});
  $('#groups').append(b);
}
function render(){
  const q=$('#search').value.toLocaleLowerCase('ru').trim();
  const priority=$('#priority').value;
  const [, ,lo,hi]=groups.find(g=>g[0]===group);
  visible=items.filter(i=>i.number>=lo&&i.number<=hi&&(priority==='all'||i.priority===priority)&&(!q||`${i.id} ${i.name}`.toLocaleLowerCase('ru').includes(q)));
  $('#catalog').replaceChildren();$('#count').textContent=visible.length;$('#empty').hidden=visible.length!==0;
  for(const item of visible){
    const b=document.createElement('button');b.className='ui-card';b.type='button';b.setAttribute('aria-label',`Открыть ${item.id}: ${item.name}`);
    const thumb=document.createElement('div');thumb.className='thumb';
    const img=new Image();img.src=`../assets/previews/${item.id}.webp`;img.alt=item.name;img.width=640;img.height=360;img.loading='lazy';thumb.append(img);
    const meta=document.createElement('div');meta.className='card-meta';
    const id=document.createElement('span');id.textContent=item.id;
    const kind=document.createElement('span');kind.textContent='SVG + PNG';
    const p=document.createElement('span');p.className='p';p.textContent=item.priority;meta.append(id,kind,p);
    const title=document.createElement('h2');title.textContent=item.name;
    const size=document.createElement('p');size.className='card-dimensions';
    const sizeLabel=document.createElement('span');sizeLabel.textContent='На экране · ';
    size.append(sizeLabel,document.createTextNode(item.dimensions.summary));
    b.append(thumb,meta,title,size);b.addEventListener('click',()=>open(item));$('#catalog').append(b);
  }
}
function setVariant(key,button){
  activeVariant=key;
  const item=items[current];
  const suffix=key?`UI_030_ENDING_${key}`:item.png.split('/').pop().replace('.png','');
  $('#full').src=`Previews/1080p/${suffix}.png`;
  $('#svg-link').href=key?`Source/Artboards/${suffix}.svg`:item.svg;
  $('#png-link').href=`Previews/1080p/${suffix}.png`;
  $('#small-link').hidden=Boolean(key);$('#small-link').href=item.preview;
  $('#variants').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
}
function open(item){
  current=items.indexOf(item);$('#viewer-id').textContent=`${item.id} / ${item.priority}`;
  $('#viewer-title').textContent=item.name;$('#full').alt=item.name;
  $('#location').textContent=item.location;$('#behavior').textContent=item.behavior;$('#handoff').textContent=item.handoff;
  $('#screen-size').textContent=item.dimensions.screen;
  $('#screen-position').textContent=item.dimensions.position;
  $('#export-size').textContent=item.dimensions.export;
  $('#position').textContent=`${String(current+1).padStart(2,'0')} / 35`;
  $('#variants').replaceChildren();$('#variants').hidden=item.number!==30;
  if(item.number===30){
    for(const [key,label] of [['LAUNCH','Пуск состоялся'],['EMPTY_CITY','Пустой город'],['BLACKOUT','Аварийная тьма']]){
      const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',()=>setVariant(key,b));$('#variants').append(b);
    }
    const first=$('#variants button');setVariant('LAUNCH',first);
  }else setVariant(null,null);
  if(!viewer.open)viewer.showModal();viewer.scrollTop=0;
}
$('#search').addEventListener('input',render);$('#priority').addEventListener('change',render);
$('#close').addEventListener('click',()=>viewer.close());
$('#prev').addEventListener('click',()=>open(items[(current+34)%35]));
$('#next').addEventListener('click',()=>open(items[(current+1)%35]));
viewer.addEventListener('click',e=>{if(e.target===viewer){const b=viewer.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)viewer.close()}});
document.addEventListener('keydown',e=>{if(!viewer.open)return;if(e.key==='ArrowLeft'){e.preventDefault();open(items[(current+34)%35])}if(e.key==='ArrowRight'){e.preventDefault();open(items[(current+1)%35])}});
render();
