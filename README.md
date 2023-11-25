# Proyecto_Grupo22
Proyecto Grupo 22 - DSA - MIAD

[![UML](figs/dsa_banner.png)](figs/dsa_banner.png)

[![Tests](https://github.com/JECaballeroR/Proyecto_Grupo22/actions/workflows/tests.yml/badge.svg)](https://github.com/JECaballeroR/Proyecto_Grupo22/actions/workflows/tests.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/badge/python-3.9-blue.svg)
![](https://img.shields.io/badge/status-prod-green.svg)
![](https://img.shields.io/badge/version-1.0.1-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)


# Deployment

## API:
1. Crear una instancia de una máquina virtual.
1. Clonar el repositorio.
```
 git clone https://github.com/JECaballeroR/Proyecto_Grupo22.git
```

1. Ir a la carpeta en que se clonó
```
$ cd ruta/a/la/carpeta
```


## Dashboard:
1. Clonar el repositorio
1. Crear una cuenta en https://share.streamlit.io/
1. Dale permisos a Streamlit share sobre tus repos de github
1. Desde el workspace, click en "New App" en la esquina superior izquierda:

[![UML](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-empty-new-app.png
)](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-empty-new-app.png
)
3. Elige el nombre del repo, branch y el archivo. Puedes usar también "Paste GitHub URL" 
   y pegar el link al archivo .py con la app de streamlit.
   
1. Streamlit genera una URL con un Random Hash. Cambia la URL de la app

[![UML](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-an-app.png
)](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-an-app.png
)   
5. Da clic en opciones avanzadas. Especifica que la app corra en python 3.9 y 
   agrega un el secreto URL_API='IP de la API', donde 'IP de la API' es la IP del endpoint predict de tu API
   (p.e., http://123.456.0.1/predict)
   
1. Observa a la app lanzarse.

[![UML](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-an-app-provisioning.png
)](https://docs.streamlit.io/images/streamlit-community-cloud/deploy-an-app-provisioning.png
)   

7. Para actualizar tu app, **Haz un push a la rama del proyecto que elegiste en tu deployment**.
Streamlit monitorea y actualiza la app al hacer un push.