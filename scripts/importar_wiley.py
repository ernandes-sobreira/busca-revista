#!/usr/bin/env python3
"""Importação validada de catálogo Wiley-CAPES a partir do XLSX oficial."""
import io,json,re,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from openpyxl import load_workbook
SOURCE="https://authors.wiley.com/asset/2026-Peri%C3%B3dicos-elegiveis-CAPES-Wiley.xlsx"
LANDING="https://authors.wiley.com/author-resources/Journal-Authors/open-access/affiliation-policies-payments/capes-agreement.html"
def norm(x):return re.sub(r"[^a-z0-9]","",str(x or "").lower())
def pick(headers,candidates):
 for cand in candidates:
  for i,h in enumerate(headers):
   if norm(h)==norm(cand):return i
 for cand in candidates:
  for i,h in enumerate(headers):
   if norm(cand) in norm(h):return i
 return None
def main():
 req=urllib.request.Request(SOURCE,headers={"User-Agent":"Mozilla/5.0","Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,*/*"})
 with urllib.request.urlopen(req,timeout=90) as r: content=r.read()
 if len(content)<5000:raise ValueError("Download não parece ser planilha válida")
 wb=load_workbook(io.BytesIO(content),read_only=True,data_only=True)
 found=[]
 diagnostics=[]
 for sh in wb:
  rows=sh.iter_rows(values_only=True); pre=[]
  for i,row in enumerate(rows):
   if i<30:pre.append((i,list(row)))
   else:break
  diagnostics.append({'aba':sh.title,'linhas_iniciais':[[str(v or '')[:150] for v in row[:12]] for _,row in pre[:6]]})
  options=[]
  for i,header in pre:
   h=[str(v or "").strip() for v in header]
   title=pick(h,["Journal title","Journal Name","Journal","Title","Periódico","Título do periódico"])
   if title is not None: options.append((sum(k is not None for k in [pick(h,["ISSN"]),pick(h,["eISSN"]),pick(h,["Subject"])]),i,h,title))
  if not options:continue
  _,idx,header,title=max(options)
  isbn=pick(header,["Print ISSN","ISSN","ISSN (Print)"])
  eisbn=pick(header,["Online ISSN","eISSN","ISSN (Online)"])
  area=pick(header,["Subject Area","Subject","Discipline","Category"])
  url=pick(header,["URL","Journal URL","Journal Link"])
  # worksheet reopened to retain rows discarded by lookahead
  for j,row in enumerate(sh.iter_rows(values_only=True)):
   if j<=idx:continue
   def value(k):return re.sub(r"\s+"," ",str(row[k] or "").strip()) if k is not None and len(row)>k else ""
   name=value(title)
   if len(name)<4 or norm(name) in ("journal","journaltitle","title","journalname"):continue
   found.append({"titulo":name,"issn":value(isbn),"eissn":value(eisbn),"area":value(area),"editora":"Wiley","status":"Listado no acordo CAPES–Wiley 2026","fonte":LANDING,"origem":SOURCE,"atualizado":datetime.now(timezone.utc).date().isoformat(),"url":value(url)})
 Path('data').mkdir(exist_ok=True)
 Path('data/wiley-schema.json').write_text(json.dumps(diagnostics,ensure_ascii=False,indent=2),encoding='utf-8')
 dedup={}
 for item in found:
  k=norm(item["issn"] or item["eissn"] or item["titulo"])
  dedup[k]=item
 results=sorted(dedup.values(),key=lambda d:d["titulo"].casefold())
 if len(results)<900 or sum(str(x["titulo"]).startswith("http") for x in results)>10 or sum(bool(x["issn"] or x["eissn"]) for x in results)<600:raise ValueError(f"Apenas {len(results)} títulos encontrados; abortando para evitar sobrescrever arquivo com importação incompleta.")
 out=Path("data");out.mkdir(exist_ok=True)
 (out/"wiley.json").write_text(json.dumps(results,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 (out/"wiley-proveniencia.json").write_text(json.dumps({"fonte":SOURCE,"pagina":LANDING,"registros":len(results),"coletado_em":datetime.now(timezone.utc).isoformat(),"cobertura":"Periódicos híbridos listados; não prova aprovação de APC de cada artigo"},ensure_ascii=False,indent=2),encoding="utf-8")
 print(f"Wiley: {len(results)} títulos")
if __name__=="__main__":main()
