# Mesure du mode atelier — le critère de la feuille de route (annexe)
# Usage : python mesure_atelier.py <URL du bilan_economique.html>
# Critère : code de sortie 0 (aucun texte < 12 px, aucun bouton < 56 px, aucune erreur JS).
# Exclusions assumées : les éléments à font-size 0 (volontairement masqués —
# ex. le 🔒 du bandeau verrouillé, dont le visuel vit dans son ::after).
# pip install playwright && playwright install chromium
import asyncio, json, sys
from playwright.async_api import async_playwright
URL = sys.argv[1]
JS = """()=>{
  const out={tiny:0,nText:0,tinyList:[],btnSmall:[]};
  const vis=e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);
    return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
  for(const e of document.body.querySelectorAll('*')){
    if(!vis(e)) continue;
    const fs=parseFloat(getComputedStyle(e).fontSize);
    if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){
      out.nText++;
      if(fs<12&&fs>1){ out.tiny++;
        out.tinyList.push(fs+'px '+e.tagName+'.'+String(e.className).split(' ')[0]); }
    }
    if(e.tagName==='BUTTON' && e.getBoundingClientRect().height<56)
      out.btnSmall.push((e.className||e.id||e.textContent.trim().slice(0,18)));
  }
  return out;}"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await (await b.new_context(viewport={'width':1180,'height':820},
                                         has_touch=True)).new_page()
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        await pg.goto(URL); await pg.wait_for_timeout(2500)
        await pg.evaluate("window._spkSetMode('atelier')")
        await pg.wait_for_timeout(800)
        r = await pg.evaluate(JS); r['errors']=errs
        r['mode']=await pg.evaluate("document.documentElement.getAttribute('data-mode')")
        print(json.dumps(r, indent=1, ensure_ascii=False))
        ok = r['tiny']==0 and not r['btnSmall'] and not errs and r['mode']=='atelier'
        await b.close(); sys.exit(0 if ok else 1)
asyncio.run(main())
