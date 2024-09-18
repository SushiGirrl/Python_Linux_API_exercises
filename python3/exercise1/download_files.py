""""
Løsning på øvelse 1, Python modules
https://itakea.github.io/e24_swa/py_intro_3.html#ov-1-download-filer

Løsningen er absolut minimal.
Der er ikke nogen fejlhåndtering.
Den kan gøre meget mere dynamisk ved at benytte functions og moduler.
Men den følger KISS princippet.
"""

import os
import requests
import subprocess

# Opretter en mappe på din computer
os.makedirs('downloaded_site', exist_ok=True)

#  cd ind i mappen
os.chdir('downloaded_site')

# Læs denne fil
res = requests.get('https://itakea.github.io/e24_swa/py_intro_3.html')

# gem html i variabel 
html = res.text

start = 0
i = 1

# Loop igennem html variablen så lang tid der er stylesheets tilbage
while True:
    
    # led efter path til stylesheets i hele dokumentet
    link_start = html.find('<link rel="stylesheet"', start) # find index på <link
    
    # hvis der ikke er flere link tags i html dokumentet (stop loop)
    if link_start == -1:   
        break

    # find index på href
    href_start = html.find('href="', link_start)
    
    # find index på slut " 
    href_end = html.find('"', href_start + len('href="')) 
    
    # find substring mellem " og "
    css = html[ href_start + len('href="'):href_end ] 

    # læs css online
    res_css = requests.get(f'https://itakea.github.io/e24_swa/{css}')

    # skriv css filerne til hd
    with open(f'style{i}.css', 'w', encoding='utf-8') as f:
        f.write(res_css.text)


    # opdater html variable med nyt css navn    
    html = html.replace(css, f'style{i}.css')

    i += 1  # del  af stylesheet navn

    # opdater startposition for at læse links til style sheet
    start = link_start + len('<link')


# skriv html variabel til fil og gem på HD
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

file_path = os.path.abspath('index.html')

try:
    subprocess.run(['start', file_path], shell=True)
    print("Attempted to open file with default application.")
except Exception as e:
    print(f"Failed to open file with subprocess: {e}")

# skift mappe fra downloads og tilbage til parrent (reset)
os.chdir('..')