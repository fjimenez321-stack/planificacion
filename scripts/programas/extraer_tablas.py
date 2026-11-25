#!/usr/bin/env python3
"""Extrae OA e indicadores de las tablas de unidad de un Programa de Estudio (PDF Mineduc).
Uso: python scripts/programas/extraer_tablas.py programas/<nivel>/extraccion.json salida.json
Revisar siempre la salida contra el PDF (ver CLAUDE.md > Cargar un programa nuevo)."""
import pdfplumber, re, json, sys
from collections import defaultdict

def dehyph(lines):
    s=""
    for l in lines:
        l=l.strip()
        if not l: continue
        if s.endswith("-") and l[:1].islower():
            s=s[:-1]+l
        else:
            s=(s+" "+l) if s else l
    return re.sub(r"\s+"," ",s).strip()

def tabla(page, basico):
    words=page.extract_words(x_tolerance=1.5)
    hdr=None
    for w in words:
        if w['text'] in('Las','Los'):
            line=" ".join(x['text'] for x in sorted([x for x in words if abs(x['top']-w['top'])<2 and x['x0']>=w['x0']],key=lambda x:x['x0']))
            if 'alcanzado' in line: hdr=w;break
    xind=hdr['x0']-3
    act=[w for w in words if w['text'].startswith('Actividades')]
    xact=act[0]['x0']-5 if act and not basico else 10**6
    if basico: xact=page.width-20
    body=[w for w in words if w['top']>hdr['top']+8 and w['bottom']<page.height-20]
    bullets=[w for w in body if w['text'] in('ú','›') and xind-25<=w['x0'] and w['x1']<=xind+6]
    subs=[w for w in body if w['text'] in('>','>>') and xind-4<=w['x0']<=xind+20]
    body=[w for w in body if w not in bullets and w not in subs]
    # skip continuation header row 'jes esperados:' etc
    lines=defaultdict(list)
    for w in body: lines[round(w['top']/2.5)].append(w)
    rows=[]
    for k in sorted(lines):
        ws=sorted(lines[k],key=lambda x:x['x0'])
        lt=" ".join(w['text'] for w in ws)
        if re.search(r"(?i)programa de estudio|ciencias naturales\s*(\||unidad)",lt): continue
        t0=min(w['top'] for w in ws)
        bul=any(abs(b['top']-t0)<5 for b in bullets) and any(xind-2<=w['x0']<xact for w in ws)
        L=" ".join(w['text'] for w in ws if w['x1']<=xind+4)
        M=" ".join(w['text'] for w in ws if xind-2<=w['x0']<xact)
        R=" ".join(w['text'] for w in ws if w['x0']>=xact)
        sb=any(abs(b['top']-t0)<5 for b in subs)
        rows.append((t0,L,('>'+M) if sb else M,R,bul))
    return rows

def parse_unit(pdf, pages, basico):
    oas=[]; byc={}; curcode=None; ind=None; left=defaultdict(list)
    with pdfplumber.open(pdf) as P:
        for pn in pages:
            rows=tabla(P.pages[pn-1],basico)
            marks=[]
            for top,L,M,R,bul in rows:
                m=re.match(r"^OA\s?(\d+)\b\s*(.*)",L)
                if m: marks.append((top,f"OA{int(m.group(1))}"))
            def oa_at(t):
                c=curcode
                for mt,code in marks:
                    if mt<=t+6: c=code
                return c
            last_top=None
            for top,L,M,R,bul in rows:
                m=re.match(r"^OA\s?(\d+)\b\s*(.*)",L)
                if m:
                    if m.group(2): left[f"OA{int(m.group(1))}"].append(m.group(2))
                elif L:
                    c=oa_at(top)
                    if c: left[c].append(L)
                if not M: continue
                code=oa_at(top)
                if code is None: continue
                if code not in byc:
                    byc[code]={'oa':code,'indicadores':[]}; oas.append(byc[code])
                if code!=curcode: ind=None; curcode=code
                t=M.strip()
                sub = (not basico) and t.startswith('>')
                if basico:
                    newb = bul or t.startswith(('›','•')) or (last_top is not None and top-last_top>20)
                else:
                    numR = bool(R) and bool(re.match(r"^[\d ,y–-]+$",R))
                    prevtxt = " ".join(ind) if ind else ""
                    newb = (numR and not sub) or (not sub and not R and last_top is not None and top-last_top>20 and prevtxt.rstrip().endswith('.') and t[:1].isupper())
                if ind is None or newb:
                    ind=[]; byc[code]['indicadores'].append(ind)
                if sub: ind.append('• '+re.sub(r"^>+\s*","",t))
                else: ind.append(re.sub(r"^[›>•ú]+\s*","",t))
                last_top=top
            if marks: curcode=marks[-1][1] if not rows or True else curcode
    for o in oas:
        o['indicadores']=[dehyph(i) for i in o['indicadores'] if dehyph(i)]
        o['texto_tabla']=dehyph(left[o['oa']])
    return oas

def unit_name(pdf,page):
    with pdfplumber.open(pdf) as P:
        t=(P.pages[page-1].extract_text() or '').split('\n')
    for i,l in enumerate(t[:10]):
        if re.match(r"(?i)unidad\s*\d",l.strip()):
            n=t[i+1].strip()
            return n[:1].upper()+n[1:].lower() if n.islower() or n.isupper() else n[:1].upper()+n[1:]
    return None

cfg=json.load(open(sys.argv[1]))
res=[]
for u in cfg['unidades']:
    oas=parse_unit(cfg['pdf'],u['pages'],cfg['basico'])
    res.append(dict(eje=u.get('eje'),unidad=u['n'],nombre=u.get('nombre') or unit_name(cfg['pdf'],u['pages'][0]),oas=oas))
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=1)
for u in res:
    print(u['eje'],u['unidad'],u['nombre'],[ (o['oa'],len(o['indicadores'])) for o in u['oas']])
