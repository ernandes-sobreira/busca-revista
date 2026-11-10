#!/usr/bin/env python3
"""Importa exclusivamente listas oficiais CAPES/Springer, sem inferir elegibilidade individual de autor."""
import csv, io, json, os, re, urllib.request
from datetime import datetime, timezone
from pathlib import Path
from openpyxl import load_workbook

SPRINGER_XLSX="https://cms-resources.apps.public.k8s.springernature.io/springer-cms/rest/v1/content/27829124/data/v5"
SOURCE_PAGE="https://www.springernature.com/br/open-science/oa-agreements/brazil/capes"
OUT=Path("data")
OUT.mkdir(exist_ok=True)
def clean(x):
    return re.sub(r"\\s+"," ",str(x if x is not None else "").strip())
def norm(x):return re.sub("[^a-z0-9]","",clean(x).lower())
def pick(headers,options):
    for opt in options:
        for i,h in enumerate(headers):
            if norm(h)==norm(opt):return i
    for opt in options:
        for i,h in enumerate(headers):
            if norm(opt) in norm(h):return i
    return None
def parse_sheet(sheet):
    rows=list(sheet.values)
    best=(0,None,[],None)
    for n,row in enumerate(rows[:25]):
        vals=[clean(v) for v in row]
        ix=pick(vals,["Journal title","Journal Name","Title","Journal","Publication title"])
        if ix is not None:
            score=sum(x is not None for x in [pick(vals,["ISSN","Print ISSN","ISSN (Print)"]),pick(vals,["eISSN","Electronic ISSN","Online ISSN"]),pick(vals,["Subject","Subject Area","Discipline"])])
            if best[1] is None or score>best[0]: best=(score,ix,vals,n)
    if best[1] is None:return []
    _,ti,headers,start=best
    pi=pick(headers,["Print ISSN","ISSN Print","pISSN","ISSN"])
    ei=pick(headers,["Online ISSN","Electronic ISSN","eISSN","e-ISSN"])
    ar=pick(headers,["Subject Area","Subject","Discipline","Category"])
    uri=pick(headers,["Journal URL","Link","Website","URL"])
    rec=[]
    for row in rows[start+1:]:
        title=clean(row[ti] if len(row)>ti else "")
        if not title or norm(title) in ("journaltitle","journalname") or len(title)<4:continue
        def at(i):return clean(row[i]) if i is not None and len(row)>i else ""
        record={"titulo":title,"issn":at(pi),"eissn":at(ei),"area":at(ar),"editora":"Springer Nature — Springer","status":"Periódico no catálogo oficial Springer","fonte":SOURCE_PAGE,"origem":"acordo oficial CAPES–Springer 2026–2028","atualizado":datetime.now(timezone.utc).date().isoformat(),"url":at(uri)}
        rec.append(record)
    return rec
def main():
    req=urllib.request.Request(SPRINGER_XLSX,headers={"User-Agent":"Mozilla/5.0 BuscaRevistaUnemat/1.0","Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*"})
    with urllib.request.urlopen(req,timeout=45) as response:
        content=response.read()
    book=load_workbook(io.BytesIO(content),read_only=True,data_only=True)
    entries=[]
    for sheet in book:
        entries.extend(parse_sheet(sheet))
    distinct={}
    for r in entries:
        key=norm(r["titulo"])+"/"+norm(r["issn"])
        distinct[key]=r
    result=sorted(distinct.values(),key=lambda x:x["titulo"].casefold())
    if len(result)<800:raise RuntimeError(f"Importação interrompida: apenas {len(result)} títulos, esperado catálogo extenso; revisar cabeçalhos. Não sobrescrever base pública.")
    (OUT/"springer.json").write_text(json.dumps(result,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    (OUT/"proveniencia.json").write_text(json.dumps({"fonte":SOURCE_PAGE,"arquivo":SPRINGER_XLSX,"coletado_em":datetime.now(timezone.utc).isoformat(),"registros":len(result),"escopo":"Periódicos Springer / Academic Journals divulgados pela editora; cobertura final depende do autor, artigo, instituição e confirmação da CAPES","nature_unemat_elegivel":False},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Registros Springer importados: {len(result)}")
if __name__=="__main__":main()
