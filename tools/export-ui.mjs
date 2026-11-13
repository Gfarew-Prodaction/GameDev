import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const packageRequire = process.env.NTO_NODE_MODULES
  ? createRequire(path.join(process.env.NTO_NODE_MODULES, 'package.json')) : require;
const sharp = packageRequire('sharp');
const previewPng={palette:true,quality:90,colours:256,dither:0.5,effort:7};
const catalog = JSON.parse(await fs.readFile(path.join(root, 'UI/manifest.json'), 'utf8'));
for (const item of catalog.items) {
  const source = await fs.readFile(path.join(root, 'UI', item.svg));
  await sharp(source).png(previewPng).toFile(path.join(root, 'UI', item.png));
  await sharp(source).resize(1280, 720).png(previewPng).toFile(path.join(root, 'UI', item.preview));
  await sharp(source).resize(640,360).webp({quality:83}).toFile(path.join(root,'assets/previews',`${item.id}.webp`));
  console.log(`${item.id}: ${item.name}`);
}
for (const file of await fs.readdir(path.join(root, 'UI/Source/Artboards'))) {
  if (!file.endsWith('.svg')) continue;
  await sharp(await fs.readFile(path.join(root, 'UI/Source/Artboards', file)))
    .png(previewPng).toFile(path.join(root, 'UI/Previews/1080p', file.replace('.svg', '.png')));
}
for (const file of await fs.readdir(path.join(root, 'UI/Source/Components'))) {
  if (!file.endsWith('.svg')) continue;
  await sharp(await fs.readFile(path.join(root, 'UI/Source/Components', file)))
    .png().toFile(path.join(root, 'UI/Sprites', file.replace('.svg', '.png')));
}
// A complete contact sheet allows checking coverage without opening 35 files.
const thumbW=384, thumbH=250;
const composites=[];
for (let i=0;i<catalog.items.length;i++) {
  const item=catalog.items[i];
  const thumb=await sharp(path.join(root,'UI',item.png)).resize(384,216).png().toBuffer();
  const label=Buffer.from(`<svg width="384" height="34"><rect width="384" height="34" fill="#172C3A"/><text x="10" y="23" fill="#F5EFE0" font-family="Arial" font-size="15">${item.id} · ${item.name.replaceAll('&','&amp;').replaceAll('<','&lt;')}</text></svg>`);
  composites.push({input:thumb,left:(i%5)*thumbW,top:Math.floor(i/5)*thumbH});
  composites.push({input:label,left:(i%5)*thumbW,top:Math.floor(i/5)*thumbH+216});
}
await sharp({create:{width:1920,height:1750,channels:4,background:'#172C3A'}})
  .composite(composites).png().toFile(path.join(root,'UI/Previews/overview.png'));
console.log('Exported all 35 artboards at 1080p and 720p, ending variants, transparent sprites and contact sheet.');
