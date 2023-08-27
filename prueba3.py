import csv
import os
import pdfkit
import ssl
import certifi
import re
import urllib.request as urlopen
import requests
from bs4 import BeautifulSoup
import pathlib
import urllib.error
import time
import json
from googletrans import Translator
#http://10.1.251.41/cgi-bin/dynamic/printer/login.html?login_type=password_only&accid=13&goto=%2Fcgi%2Dbin%2Fdynamic%2Fprinter%2Fconfig%2Freports%2Fdevicestatistics.html
f=open('Impresoras.csv')
reader= csv.reader(f, delimiter= ';')
next(reader, None)
datos=[x for x in reader]
f.close()
cont = 1
totalDatos = (len(datos)+1)
#for x in datos:
    #print("aqui es "+ x[0])
#print(str(cont)+"/"+str(totalDatos))

#cont = cont + 1

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
def archivoNoFound(campo, nofound):
    if not pathlib.Path('noFound.csv').exists():        
        with open('noFound.csv', 'w', newline='') as file:                        
            writer = csv.DictWriter(file, fieldnames=campo, delimiter= ';', dialect='excel')
            writer.writeheader()
    with open('noFound.csv', 'a', newline='') as file:            
        writer = csv.DictWriter(file, fieldnames=campo, delimiter=';')
        writer.writerow(nofound)

   
for pagina in datos:
    #print(str(cont)+"/"+str(totalDatos))

    cont = cont + 1
    result= ping(pagina[0])
    #print(result)
    try:
        if result==True:
            
            url=(f'https://{pagina[0]}/hp/device/InternalPages/Index?id=UsagePage')
            
            #print(url)
            context=ssl._create_unverified_context(cafile=certifi.where())
            context.set_ciphers("DEFAULT")
            site=urlopen.urlopen(url, context=context).read()
            #site= requests.get(url, headers=Hostreferer,verify=False)
            #sinBy =(site.decode('utf-8'))
            #print(sinBy)
            soup = BeautifulSoup(site, 'html.parser')
            #name = soup.find('id', attrs={'id': 'company__name'})
            link = soup.find("div", {"id": "InternalPageContent"})
            #print(link)
            #json_string = json.dumps({'message': link.decode('utf-8')})
            #translator = Translator()
            #traduccion = translator.translate(link, src='en', dest='es')
            #print(traduccion.text)
            #print(f'{pagina[1]}.html')
            f=open(f'{pagina[1]}.html', 'w', encoding='utf-8')
            
            f.write(str(link))
            #f.write((traduccion.text))
            f.close
            now = time.strftime("%d-%m-%y")
            nomCarp = 'PDFs_'+now
            #print(now)
            option = {'page-size': 'Letter','header-right': f'{pagina[1]}', 'footer-right': f'{pagina[0]}    -      {now} '  , 
                      'enable-local-file-access': False, "load-error-handling": "ignore"}                
            exe= 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
            config=pdfkit.configuration(wkhtmltopdf=exe)
            #print(config)
            existe = True
            esta = True                                             
                        
            while existe:
                if not pathlib.Path(f'{pagina[1]}.html').exists():
                    time.sleep(1)                    
                else:
                    existe = False
            #print(existe)
            
            while esta:
                if os.path.exists(nomCarp):
                    esta = False
                else:
                    #print('')
                    os.mkdir(nomCarp)
            #print(f'{pagina[1]}.html')
            try:
                pdfkit.from_file(f'{pagina[1]}.html', os.path.join(nomCarp, f'{pagina[1]}.pdf'), configuration=config, options=option)
            except Exception as e:
                #print('')
                print('Error for ' + str(e) + ',Page :' + f'{pagina[1]}.pdf')
            
            #print('paso')
            f = open(f'{pagina[1]}.html')
            reader = f.read()       
            #print(reader)
            modelo = re.findall('Product Name:</span><strong id="UsagePage.DeviceInformation.ProductName">HP\s(\w+)', reader)
            #print(modelo)
            if modelo[0] == 'Color':
                cargaDatos = re.findall('Grand Total</td><td class="align-right" id="UsagePage.ScanCountsDestinationTable.GrandTotal.Value">(\d+[^a-zA-Z0-9_]\w+)', reader)
                serial = re.findall('Product Serial Number:</span><strong id="UsagePage.DeviceInformation.DeviceSerialNumber">(\w+)', reader)
                modelo = re.findall('Product Name:</span><strong id="UsagePage.DeviceInformation.ProductName">(\w+\s\w+\s\w+\s\w+\s\w+)', reader)
            else:
                cargaDatos = re.findall('Print</td><td class="align-right" id="UsagePage.EquivalentImpressionsTable.Print.Total">(\d+[^a-zA-Z0-9_]\w+)', reader)
                serial = re.findall('Product Serial Number:</span><strong id="UsagePage.DeviceInformation.DeviceSerialNumber">(\w+)', reader)
                modelo = re.findall('Product Name:</span><strong id="UsagePage.DeviceInformation.ProductName">(\w+\s\w+\s\w+\s\w+)', reader)
            #print(cargaDatos)
            #print(serial)
            #print(modelo)
            f.close()
            os.remove(f'{pagina[1]}.html')
            campos = ['Nombre Impresora', 'Modelo', 'IP', 'Serial', 'Contador']
            facturacion = {campos[0]: pagina[1], campos[1]:modelo[0],campos[2]:pagina[0], campos[3]: serial[0], campos[4]: cargaDatos[0]}
            if not pathlib.Path('facturacion.csv').exists():
                with open('facturacion.csv', 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=campos, delimiter= ';', dialect='excel')
                    writer.writeheader()
            with open('facturacion.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=campos, delimiter= ';')
                writer.writerow(facturacion)
        else:
            campos = ['IP', 'Nombre Impresora', 'Estado']
            noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Sin Conexion'}
            archivoNoFound(campos, noFound)         
                
    except urllib.error.URLError:
        campos = ['IP', 'Nombre Impresora', 'Estado']
        noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Sin Conexion'}
        archivoNoFound(campos, noFound)
        
    except ConnectionResetError:
        campos = ['IP', 'Nombre Impresora', 'Estado']
        noFound = {campos[0]: pagina[0], campos[1]: pagina[1], campos[2]: 'Error'}
        archivoNoFound(campos, noFound)
        
print('Finalizado con éxito')       