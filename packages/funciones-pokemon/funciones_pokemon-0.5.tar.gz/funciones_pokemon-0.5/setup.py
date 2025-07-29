from distutils.core import setup

setup(
      # Se especifica el nombre de la librería
      name = 'funciones_pokemon',
      # Se especifica el nombre del paquete
      packages = ['funciones_pokemon'],
      # Se especifica la versión, que va aumentando con cada actualización
      version = '0.5',
      # Se especifica la licencia escogida
      license='MIT',
    # Breve descripción de la librería
    description = 'Libreria de pokemon',
    # Nombre del autor
    author = 'Cristian Lorca Brenes',
    # Email del autor
    author_email = 'cristian@gmail.com',
    # Enlace al repositorio de git de la librería
    url = 'https://github.com/',
    # Enlace de descarga de la librería
    download_url = 'https://github.com/',
    # Palabras claves de la librería
    keywords = ['pokemon', 'csv', 'pandas'],

    # Librerías externas que requieren la librería
    install_requires=[
        "pandas"
    ],
    classifiers=[
      # Se escoge entre "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
      # según el estado de consolidación del paquete
      'Development Status :: 3 - Alpha',
      # Se define el público de la librería
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      # Se indica de nuevo la licencia
      'License :: OSI Approved :: MIT License',
      #Se definen las versiones de python compatibles con la librería
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
    ]
)
