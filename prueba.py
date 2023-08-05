import requests
from bs4 import BeautifulSoup
import ssl
import urllib3

def get_element_path(url, element_id):
    try:
        #context = ssl.CERT_NONE
        #context = ssl._create_unverified_context()
        urllib3.disable_warnings
        # Obtener el código fuente de la página web
        response = requests.get(url, verify=False)
        #print(response.status_code)
        response.raise_for_status()

        # Analizar el código fuente utilizando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar el elemento específico utilizando su ID
        target_element = soup.find(id=element_id)

        # Generar la ruta de ancestros hasta llegar al elemento raíz (<html>)
        element_path = []
        current_element = target_element
        while current_element and current_element.name != 'html':
            element_info = {
                'tag': current_element.name,
                'attrs': {attr: current_element[attr] for attr in current_element.attrs},
            }
            element_path.append(element_info)
            current_element = current_element.parent

        # Revertir la lista para tener la ruta desde la raíz hasta el elemento
        element_path.reverse()

        return element_path

    except requests.exceptions.RequestException as e:
        print("Error al obtener la página:", e)
        return None
    except AttributeError as e:
        print("El elemento con ID especificado no fue encontrado:", e)
        return None

# URL de la página web que deseas analizar
url = "https://172.16.17.12/hp/device/InternalPages/Index?id=UsagePage"

# ID del elemento específico que deseas encontrar
element_id = "InternalPageContent"
#print(url + element_id)
# Obtener la ruta del elemento
element_path = get_element_path(url, element_id)
#print(element_path)
if element_path:
    print("Ruta del elemento:")
    for element_info in element_path:
        print(element_info)
else:
    print("No se pudo obtener la ruta del elemento.")
