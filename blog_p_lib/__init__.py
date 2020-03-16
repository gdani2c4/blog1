import os

from flask import Flask, render_template

def create_app( pruebas_cfg = None ):
    ap_x = Flask( __name__, instance_relative_config = True )
    ap_x.config.from_mapping(
#    SECRET_KEY = "des",
#    PRUEBA1 = "prueba 123 config var",
    DATABASE = os.path.join( ap_x.instance_path,
    "flask.sqlite" )
    )
    ap_x.CNTA_PND = 2
    ap_x.CNTA_VER = 1
    ap_x.CNTA_NOD = 0
    ap_x.ficha_lon = 20
# el siguiente no se ha pudido acceder desde blog.py:
#    g.prueba1 = "prueba - definir llaves en el objeto g"
#    ap_x.test1 = "test 123 config var"
    if pruebas_cfg == None:
        ap_x.config.from_pyfile( "config.py", silent = True )
    else:
        ap_x.config.from_mapping( pruebas_cfg )
    #end if
    # -- context_processor agrega parámetros a toda plantilla
    #    jinja. consulta https://stackoverflow.com/questions/ ...
    #    ... 31750655/pass-variables-to-all-jinja2-templates-with-flask
    @ap_x.context_processor
    def plantillas_contexto():
        return { "recap_url":
            ap_x.config[ "URL_GOOGLE_RECAP" ]
        }
    # fed
    
    try:
        os.makedirs( ap_x.instance_path )
    except OSError:
        pass
    #end try
    
    @ap_x.route( "/prueba1" )
    def prueba1():
        return "prueba 1234"
    #end def prueba1
    
    from . import bbdd
    bbdd.ini_ap( ap_x )
    
    from . import mod_prueba
    ap_x.register_blueprint( mod_prueba.sqm_prueba )

    from . import autr
    ap_x.register_blueprint( autr.sqm1 )
    
    from . import blog
    ap_x.register_blueprint( blog.sqm1 )

    @ap_x.route("/")
    def index():
        return blog.index()
#        with open( "instance/ctg1/publ_p1" ) as achvo0:
#            publ1 = achvo0.read()
#        #end with
#        return render_template( "publ.html", publ = publ1 )
#        bbdd1 = obt_bbdd()
#        publes = bbdd1.execute(
#        "SELECT id, creado, titulo FROM publ " \
#                "ORDER BY creado DESC" ).fetchall()
#        return render_template( "index.html", publes = publes )
    #end def index
    
    return ap_x
    
#end def create_app
