import csv
import os
import pdfkit
import ssl
import certifi
import re
import urllib.request as urlopen
from bs4 import BeautifulSoup
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
    #print("aqui es "+ x[0])

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


   
for pagina in datos:
    
    result= ping(pagina[0])
    #print(result)
    try:
        if result==True:
            
            url=(f'https://{pagina[0]}/hp/device/InternalPages/Index?id=UsagePage')
            
            #print(url)
            context=ssl._create_unverified_context(cafile=certifi.where())
            context.set_ciphers("DEFAULT")
            site=urlopen.urlopen(url, context=context)

            soup = BeautifulSoup(site, 'html.parser')
            #name = soup.find('id', attrs={'id': 'company__name'})
            link = soup.find("div", {"id": "InternalPageContent"}).encode()
            #print(link)
            
            #print(f'{pagina[1]}.html')
            f=open(f'{pagina[1]}.html', 'w')
            
            f.write(str(link))
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
            print(reader)
            cargaDatos = re.findall(r'Grand Total</td><td class="align-right" id="UsagePage.ScanCountsDestinationTable.GrandTotal.Value">(\d+[^a-zA-Z0-9_]\w+)', reader)
            print(cargaDatos)
            f.close()
            os.remove(f'{pagina[1]}.html')
        else:
            
            print("error 1")         
                
    except urllib.error.URLError:
        print("Error 2")
        
    except ConnectionResetError:
        print("Erro 3")
        
print('Finalizado con éxito')       