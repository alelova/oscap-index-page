#!/usr/bin/python3
import jinja2
import re
import statistics
from operator import itemgetter
from pathlib import Path
from datetime import date

title = 'Informe Global Cumplimiento - SCAP'
subtitle= 'Actualizado con informes en repositorio: '
outputfile = '/var/www/report/oscap/index.htm'
carpeta_informes = Path('/var/www/report/oscap/').rglob('*.html')
files = [x for x in carpeta_informes]
data2=[]
suma=0

for nombre_archivo in files:
  res=0
  fechareport='';
  #leemos los datos que nos interesan
  handler = open(nombre_archivo,'r')
  for linea in handler:
      if 'urn:xccdf:scoring:default' in linea: 
          resultado=(linea.split('progress-bar')[2])
          res=[float(s) for s in re.findall(r'-?\d+\.?\d*', resultado)]
          print(res)
      if 'Finished at' in linea:
          match=(re.search(r'\d{4}-\d{2}-\d{2}', linea))
          fechareport=format(match.group(0))
  servidor=str(nombre_archivo).split('/')[-1].replace(".html","")
  data2.append([servidor,round(res[0],2),fechareport])
  handler.close() 

for i in data2: 
    suma=suma+(i[1])
media=round(suma/len(data2),2)
#print (media)
data2=sorted(data2, key=itemgetter(0))
print(data2)

#construimos la pagina
subtitle=subtitle + str(date.today())+', '+str(len(data2))+ ' servidores.'
subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader('./')      
).get_template('template.html').render(title=title,subtitle=subtitle,mydata=data2,total=media)

# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)
