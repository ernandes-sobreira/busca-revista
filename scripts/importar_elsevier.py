#!/usr/bin/env python3
"""Importa tabela Freedom Collection (read versus read & publish) do contrato CAPES 57/2025."""
import io,json,re,urllib.request
from datetime import datetime,timezone
from pathlib import Path
import pdfplumber
PDF="https://www.gov.br/capes/pt-br/centrais-de-conteudo/documentos/contratos-capes/04122025_Contrato_572025_SEI_2729395.pdf/@@display-file/file"
SOURCE="https://www.elsevier.com/open-access/agreements/capes"
OUT=Path("data")
OUT.mkdir(exist_ok=True)
CODE=re.compile(r"^\s*(\d{1,4})\s+(.+?)\s+(\d{4}-[\dXx]{4})\s+(.+?)\s+(Read\s*&\s*Publish|Read)\s*$",re.I)
def main():
 req=urllib.request.Request(PDF,headers={"User-Agent":"Mozilla/5.0"})
 with urllib.request.urlopen(req,timeout=120) as rsp: raw=rsp.read()
 if len(raw)<100000:raise RuntimeError("PDF do contrato não foi baixado por completo")
 found={}
 examples=[]
 with pdfplumber.open(io.BytesIO(raw)) as pdf:
  # Páginas 7 a 27 do contrato: tabela completa da Freedom Collection.
  for pg in range(6,min(27,len(pdf.pages))):
   txt=pdf.pages[pg].extract_text(x_tolerance=2,y_tolerance=3) or ""
   lines=txt.splitlines()
   pending=""
   for line in lines:
    line=line.strip()
    if "ANEXO II - LISTA DE INSTITUIÇÕES" in line: break
    if not line:continue
    m=CODE.match(line)
    if not m and pending:m=CODE.match(pending+" "+line)
    if m:
     num=int(m.group(1))
     if not 1<=num<=1693:continue
     title=re.sub(r"\s+"," ",m.group(2)).strip()
     issn=m.group(3).upper()
     is_pub="Publish" in m.group(5)
     found[num]={"titulo":title,"issn":issn,"eissn":issn,"area":"","editora":"Elsevier","status":"Read & Publish" if is_pub else "Apenas leitura","cobertura_apc":"elegivel_titulo" if is_pub else "nao_coberto","fonte":PDF,"origem":"Contrato CAPES Elsevier 57/2025, anexo I Freedom Collection","atualizado":datetime.now(timezone.utc).date().isoformat(),"url":SOURCE}
     pending=""
    elif re.match(r"^\d{1,4}\s+",line):
     pending=line
    elif pending and len(pending)<300:
     pending+=" "+line
    if 1<=len(examples)<3:pass
   if pg==6:examples=lines[:20]
 # Quatro linhas cuja diagramação do PDF quebra o extrator (verificação manual no Anexo I).
 overrides={
 644:("Nuclear Instruments and Methods in Physics Research Section B: Beam Interactions with Materials and Atoms","0168-583X"),
 665:("Nuclear Instruments and Methods in Physics Research Section A: Accelerators, Spectrometers, Detectors and Associated Equipment","0168-9002"),
 1298:("Photonics and Nanostructures - Fundamentals and Applications","1569-4410"),
 1451:("Radiología (English Edition)","2173-5107"),
 }
 for num,(title,issn) in overrides.items():
  if num not in found:
   found[num]={"titulo":title,"issn":issn,"eissn":issn,"area":"","editora":"Elsevier","status":"Read & Publish","cobertura_apc":"elegivel_titulo","fonte":PDF,"origem":"Contrato CAPES Elsevier 57/2025, Anexo I; linha fragmentada na extração, conferida no texto oficial","atualizado":datetime.now(timezone.utc).date().isoformat(),"url":SOURCE}
 full=list(found.values())
 eligible=[x for x in full if x["cobertura_apc"]=="elegivel_titulo"]
 meta={"total":len(full),"publicacao":len(eligible),"apenas_leitura":len(full)-len(eligible),"faltando":[i for i in range(1,1694) if i not in found][:50],"origem":PDF,"amostra":full[:3],"coletado_em":datetime.now(timezone.utc).isoformat(),"amostra_texto":examples}
 (OUT/"elsevier-diagnostico.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
 # A tabela contratual é explícita: 1.693 títulos, 1.619 com Read & Publish.
 # Falha fechada para não colocar assinaturas de leitura como APC grátis.
 if len(full)!=1693 or len(eligible)!=1619:raise RuntimeError("Contagens não conferem com contrato: "+str(meta["total"])+"/"+str(meta["publicacao"]))
 (OUT/"elsevier.json").write_text(json.dumps(sorted(full,key=lambda x:x["titulo"].casefold()),ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 print("Elsevier importada: 1693 títulos, 1619 elegíveis para publicação, 74 apenas leitura")
if __name__=="__main__":main()
