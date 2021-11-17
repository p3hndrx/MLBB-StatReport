import os
from os.path import exists
from wand.image import Image
from wand.color import Color

src = "/var/www/html/summary-reports"
dst = "/var/www/html/summary-reports-png"


for file in os.listdir(src):
    filein = f"{src}/{file}"
    fileout = f"{dst}/{file}.png"
    if exists(fileout):
        print(f"{fileout} exists")
    else:
        print(f"{fileout}-- MISSING")
        print(f"Converting...")
        print(f"{filein} >> {fileout}")
        
        with Image(filename=f"{filein}[0]", resolution=150) as img:
            format = "PNG"
            img.save(filename=fileout)
