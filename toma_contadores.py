import csv
import os
import pdfkit
import requests
import ssl
import certifi
import urllib.request as request
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pathlib
import urllib.error
import time

#http://10.1.251.41/cgi-bin/dynamic/printer/login.html?login_type=password_only&accid=13&goto=%2Fcgi%2Dbin%2Fdynamic%2Fprinter%2Fconfig%2Freports%2Fdevicestatistics.html
f=open('Impresoras.csv')
reader= csv.reader(f, delimiter= ';')
next(reader, None)
datos=[x for x in reader]
f.close()
#for x in datos:
#    print("aqui es "+ x[0])

def ping(ip):
    response=os.popen(f'ping -n 1 {ip}').read()
    
    if "expirado" in response:
        result= False
    
    elif "expired" in response:
        result= False
        
    elif "agotado" in response:
        result = False
        
    elif "time out" in response:
        result= False
    
    elif "inaccesible" in response:
        result = False
        
    else:
        result = True
        
    return result

def contadorInicialyFinal(contadorI):
    if len(contadorI) == 4:
        contadorHojas = contadorI[1]
        contadorCopias = 0
        contadorCaras = contadorI[-1]
    elif len(contadorI) == 5:
        contadorHojas = contadorI[1]
        contadorCopias =  contadorI[3]
        contadorCaras = contadorI[-1]
    else:
        contadorHojas = contadorI[1]
        contadorCopias = contadorI[4]
        contadorCaras = contadorI[-1]
    
    return contadorHojas, contadorCaras, contadorCopias
#noFound=[]
#facturacion =[]
def porcentajeSuministros(match, reader):
    try:
        
        if match ==[]:
            porcentajeSuministros = re.findall("Nivel suministro</p></td><td><p>\s\s(\w+)", reader)
            porcentajeToner = porcentajeSuministros[0]
            porUnidadImagen = porcentajeSuministros[1]
            porKitMantenimiento = porcentajeSuministros[2]
        else:
            porcentajeSuministros = re.findall("Nivel suministro</p></td><td><p>\s\s(\w+)", reader)
            porcentajeToner = re.findall("Nivel de tóner</p></td><td><p>\s\s(\w+)", reader)
            porcentajeToner = porcentajeToner[0]
            porUnidadImagen = porcentajeSuministros[0]
            porKitMantenimiento = porcentajeSuministros[1]
    
    except IndexError:
        porUnidadImagen = "N/A"
        porKitMantenimiento = "N/A"
    
    return porcentajeToner,porUnidadImagen, porKitMantenimiento

def archivoNoFound(campo, nofound):
    if not pathlib.Path('noFound.csv').exists():        
        with open('noFound.csv', 'w', newline='') as file:                        
            writer = csv.DictWriter(file, fieldnames=campo, delimiter= ';', dialect='excel')
            writer.writeheader()
    with open('noFound.csv', 'a', newline='') as file:            
        writer = csv.DictWriter(file, fieldnames=campo, delimiter=';')
        writer.writerow(nofound)
    
#Proceso de Toma de contadores
   
for pagina in datos:
    
    result= ping(pagina[0])
    #print(result)
    try:
        if result==True:
            url=f'https://{pagina[0]}/hp/device/InternalPages/Index?id=UsagePage'
            #context = ssl._create_unverified_context(cafile=certifi.where())
            #site=request.urlopen(url, context=context)
            site = requests.get(url).text
            #print(site)
            f=open(f'{pagina[1]}.html', 'wb')
            #print(f)
            f.write(site.read())
            f.close
            now = time.strftime("%d/%m/%y")
            #print(now)
            option = {'header-right': f'{pagina[1]}', 'footer-right': f'{pagina[0]}    -      {now} '  , 
                      'enable-local-file-access': False}  
            #print(option)                  
            exe= 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=exe)
            #print(config)
            existe = True                                             
                        
            while existe:
                if not pathlib.Path(f'{pagina[1]}.html').exists():
                    time.sleep(1)                    
                else:
                    existe = False
                    
            #pdfkit.from_url(f'http://{pagina[0]}/cgi-bin/dynamic/printer/config/reports/devicestatistics.html', f'{pagina[1]}.pdf', options=option)
            pdfkit.from_file(f'{pagina[1]}.html', f'{pagina[1]}.pdf', options=option)
                    
            f = open(f'{pagina[1]}.html')
            reader = f.read()       
            cargaDatos = re.findall("Total general</p></td><td><p>(\d{1,2})", reader)
            print(cargaDatos)
            contaHoj, contaCar, contaCop = contadorInicialyFinal(cargaDatos)
            serial = re.findall("Número de serie</p></td><td><p>\s\s(\w+)", reader)
            serial = serial[-1]
            porTon = re.findall("Nivel de tóner</p></td><td><p>\s\s(\w+)", reader)
            modelo = re.findall("Nombre de modelo</p></td><td><p>\s\sLexmark\s(\w+)", reader)
            #print(pagina[1])
            '''porcentajeToner = porcentajeToner[0]
            porcentajeSuministros = re.findall("Nivel suministro</p></td><td><p>\s(\w+)", reader)
            porUnidadImagen = porcentajeSuministros[0]
            porKitMantenimiento = porcentajeSuministros[1]'''
            porcentajeToner, porUnidadImagen, porKitMantenimiento = porcentajeSuministros(porTon, reader)
            #facturacion.append([f'{pagina[1]}',f'{pagina[0]}',serial, contaHoj, contaCar])
            f.close()
            os.remove(f'{pagina[1]}.html')
            campos = ['Nombre Impresora', 'Modelo', 'IP', 'Serial', 'Hojas Impresas', 'Caras Impresas', 'Copias','Nivel de Toner', 'Nivel Unidad de Imagen', 'Nivel Kit de Mantenimiento']
            facturacion = {campos[0]: pagina[1], campos[1]:modelo[0],campos[2]:pagina[0], campos[3]: serial, campos[4]: contaHoj, campos[5]: contaCar, campos[6]: contaCop, campos[7]: porcentajeToner, campos[8]:porUnidadImagen, campos[9]: porKitMantenimiento}
            if not pathlib.Path('facturacion.csv').exists():
                with open('facturacion.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=campos, delimiter= ';', dialect='excel')
                    writer.writeheader()
            with open('facturacion.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=campos, delimiter= ';')
                writer.writerow(facturacion)
                                        
        else:
            campos = ['IP', 'Nombre Impresora', 'Estado']
            noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Sin Conexión'}
            archivoNoFound(campos, noFound)
            #print(pagina[1])         
                
    except urllib.error.URLError:
        campos = ['IP', 'Nombre Impresora', 'Estado']
        noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Error aqui'}
        archivoNoFound(campos, noFound)
        #print(pagina[1] + " error")
        '''if not pathlib.Path('noFound.csv').exists():
            with open('noFound.csv', 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=campos, delimiter= ';', dialect='excel')
                writer.writeheader()
        with open('noFound.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=campos, delimiter=';')
            writer.writerow(noFound)''' 
        
    except ConnectionResetError:
        campos = ['IP', 'Nombre Impresora', 'Estado']
        noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Error'}
        archivoNoFound(campos, noFound)
        #print(pagina[1] + " error")
        
print('Finalizado con éxito')       