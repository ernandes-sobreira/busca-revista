#!/usr/bin/env python3
"""Títulos de publicação do Anexo I do contrato CAPES–ACM 56/2025."""
import io,json,re,urllib.request
from pathlib import Path
from datetime import datetime,timezone
import pdfplumber
PDF="https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/contratos-capes/04122025_SEI_2729393_Contrato_56.pdf/@@display-file/file"
OUTPUT=Path("data");OUTPUT.mkdir(exist_ok=True)
ISSN=r"\d{4}-[\dXx]{4}"
rx=re.compile(r"^\s*(\d{1,2})\s+(?:(?:"+ISSN+r")\s+){1,2}.+")
def main():
 req=urllib.request.Request(PDF,headers={"User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=90) as r:raw=r.read()
 records={}
 section=False
 with pdfplumber.open(io.BytesIO(raw)) as pdf:
  for pg in range(10,min(13,len(pdf.pages))):
   for line in (pdf.pages[pg].extract_text(x_tolerance=2,y_tolerance=3) or "").splitlines():
    t=line.strip()
    if "PERIÓDICOS PARA PUBLICAÇÃO" in t or "PERIODICOS PARA PUBLICACAO" in t:section=True;continue
    if "ANEXO II" in t:section=False;break
    if not section:continue
    m=re.match(r"^(\d{1,2})\s+(.+)$",t)
    if not m:continue
    num=int(m.group(1))
    if not 1<=num<=73:continue
    tail=m.group(2)
    ids=re.findall(ISSN,tail)
    if not ids:continue
    rest=re.sub(r"^(?:"+ISSN+r"\s+){1,2}","",tail).strip()
    if len(rest)<4:continue
    records[num]={"titulo":rest,"issn":ids[0],"eissn":ids[-1],"area":"Computação","editora":"ACM","status":"Periódico no acordo CAPES–ACM","fonte":PDF,"origem":"Contrato CAPES–ACM 56/2025, Anexo I, seção periódicos para publicação","atualizado":datetime.now(timezone.utc).date().isoformat(),"url":"https://dl.acm.org/"}
 meta={"quantidade":len(records),"faltando":[i for i in range(1,74) if i not in records],"amostra":list(records.values())[:4],"fonte":PDF}
 (OUTPUT/"acm-diagnostico.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
 if len(records)!=73:raise RuntimeError(f"ACM: apenas {len(records)} dos 73 títulos extraídos")
 (OUTPUT/"acm.json").write_text(json.dumps([records[i] for i in sorted(records)],ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 print("ACM: 73 periódicos confirmados para publicação")
if __name__=="__main__":main()
