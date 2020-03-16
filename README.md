
## mi primera ap

tiene como base [la guía oficial de flask][ref1]
(en inglés)

nota: fue construido para el uso de *Linux*, exige
conocimiento técnico mínimo de *bash*
(línea de comando de *Linux*)

nota: Fijase que para el
uso de comentarios con *google recaptcha* hay
que meter un llave de *google api* en un archvio
nuevo *llaverecap* en el directorio raíz de la ap.
Se proporciona de manera gratuita por el *Google*.

### probar la ap:

- hacer clone con el comando conocido git

- crear en el directorio raíz de la ap un entorno
  virtual de python 3

- requisitos: los paquetes *flask* y *request* de *python3*

- `. venv/bin/activate`

- iniciar el base de datos:
  `FLASK_APP=blog_p_lib flask ini-bbdd`

- `echo SECRET_KEY = "llave123" > instance/config.py`
  (un llave temporal para la fase de desarrollo)

- ejecutar un servidor de pruebas:
  `FLASK_APP=blog_p_lib FLASK_ENV=development flask run`

- ¿como meter un artículo?

    - tenemos una publicación *tortas de aceite*
      bajo la categoría *gastronomía* > *recetas*

    - metemos el artículo en
      *instance/gastr/recet*

    - abrimos *instance/flast.sqlite* y
      hay que añadir las categorías a la tabla
      *ctg* y la publicación a la tabla *publ*

      nota: muy sencillo pero debo una explicación mejor,
      está para incluir un bbdd de ejemplo [15-2-20]

[ref1]: https://flask.palletsprojects.com/en/1.1.x/tutorial/
