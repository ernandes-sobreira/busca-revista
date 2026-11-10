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
assert "data/springer.json" in html
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
print("Auditoria da plataforma concluída.")
