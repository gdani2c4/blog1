from flask import (
Blueprint, jsonify
)

sqm_prueba = Blueprint( "prueba", __name__, url_prefix = "/prueba" )

@sqm_prueba.route( "/xhr" )
def xhr():
    return jsonify( ("es lo que me dijo pero no"
        " se lo quise decir hasta ahora") )

@sqm_prueba.route( "/" )
def prueba():
#    return json.dumps( current_app.config[ "CNTA_STA" ] )
#    return current_app.prueba1
#    return g.prueba1
    achvo_nom = "blog_p_lib/templates/prueba_httpreq.html"
    with open(achvo_nom) as achvo:
        achvo_cda = achvo.read()
    return achvo_cda
#    return "ruta de prueba"

@sqm_prueba.route( "/guion" )
def guion():
    achvo_nom = "blog_p_lib/templates/prueba_httpreq.js"
    with open( achvo_nom ) as achvo:
        achvo_cda = achvo.read()
    return achvo_cda
