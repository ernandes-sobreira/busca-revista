#!/usr/bin/env python3
"""Teste de integridade de catálogos e layout do Busca Revista UNEMAT."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.duplicated=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if "id" in d:
   if d["id"] in self.ids:self.duplicated.append(d["id"])
   self.ids.add(d["id"])
root=Path(__file__).resolve().parents[1]
html=(root/"plataforma.html").read_text(encoding="utf-8")
parser=Audit();parser.feed(html)
assert not parser.duplicated, f"IDs duplicados: {parser.duplicated}"
for x in ('id="term"','id="coverage"','id="results"','journalfinder.elsevier.com','Idealizado por Ernandes Sobreira','Identifique a revista'):
 assert x in html,x
assert "./data/" in html and all(n in html for n in ("springer.json","wiley.json","elsevier.json","acm.json","royal-society.json"))
def check(name,minimum):
 path=root/"data"/f"{name}.json"
 if not path.exists():
  print(f"{name}: arquivo ainda não disponível; importador separado")
  return
 data=json.loads(path.read_text(encoding="utf-8"))
 assert len(data)>=minimum,(name,len(data))
 assert all(d.get("titulo") and not d["titulo"].startswith(("http://","https://")) for d in data)
 assert all(d.get("fonte") for d in data)
 print(f"{name}: {len(data)} registros válidos")
 return data
springer=check("springer",1700)
wiley=check("wiley",1200)
royal=check("royal-society",10)
elsevier=check("elsevier",1693)
if elsevier:
 assert sum(d.get("cobertura_apc")=="elegivel_titulo" for d in elsevier)==1619
 assert sum(d.get("cobertura_apc")=="nao_coberto" for d in elsevier)==74
acm=check("acm",73)
# Avisos de qualidade (não interrompem a publicação): dígito verificador do ISSN e ISSN repetido na mesma lista.
def issn_valido(valor):
 c=re.sub(r"[^0-9Xx]","",valor or "").upper()
 if len(c)!=8:return False
 total=sum(int(ch)*(8-i) for i,ch in enumerate(c[:7]))
 dv=(11-total%11)%11
 return ("X" if dv==10 else str(dv))==c[7]
avisos=0
for nome,lista in (("springer",springer),("wiley",wiley),("elsevier",elsevier),("acm",acm),("royal-society",royal)):
 if not lista:continue
 vistos={}
 for d in lista:
  for campo in ("issn","eissn"):
   if d.get(campo) and not issn_valido(d[campo]):
    avisos+=1;print(f"AVISO {nome}: ISSN inválido na fonte ({d[campo]}) em {d['titulo']}")
  chave=re.sub(r"[^0-9X]","",(d.get("issn") or d.get("eissn") or "").upper())
  if chave:vistos.setdefault(chave,[]).append(d["titulo"])
 sem=sum(not(d.get("issn") or d.get("eissn")) for d in lista)
 if sem:avisos+=1;print(f"AVISO {nome}: {sem} título(s) sem ISSN")
 for chave,titulos in vistos.items():
  if len(titulos)>1:avisos+=1;print(f"AVISO {nome}: ISSN {chave} repetido em {titulos}")
print(f"Avisos de qualidade: {avisos}")
for x in ('Content-Security-Policy','hintPop','Resolução 076/2022'):
 assert x in html,x
assert "api_key" not in html.lower() and "apikey" not in html.lower(), "chave de API não pode ficar no HTML público"
print("Auditoria da plataforma concluída.")
