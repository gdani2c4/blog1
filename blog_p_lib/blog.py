#import os, requests, json
import os, json

from flask import (
Blueprint, g, render_template, request,
url_for, jsonify, abort, flash, current_app )
from blog_p_lib.bbdd import obt_bbdd, de_arb_ctg
from blog_p_lib.autr import ini_ses_obl
from blog_p_lib.util import desinfectar

sqm1 = Blueprint( "publ", __name__, url_prefix = "/publ" )

#1 obt_cmt
@sqm1.route( "/cmt" )
def obt_cmt():
    bbdd1 = obt_bbdd()      
    
    id_cmt = request.args.get( "cmt_id" )   
    rstdo = bbdd1.execute(  
    "SELECT ctndo FROM cmt " \
"WHERE id = ?", ( id_cmt, )     
    ).fetchone()    
    if rstdo == None: return jsonify( { "cmt_null" : 1 } )
    #end if
    return jsonify({ "ctndo": rstdo[ "ctndo" ] })   
#end def obt_cmt

#2 modificar - peticiones de modificar un comentario
@sqm1.route( "/cmt/post", methods = [ "POST" ] )
@ini_ses_obl
def modificar():
    bbdd1 = obt_bbdd()
    dat_post = request.json
    #    print( "****datos****", request.json)
    # valor de "id":
    # -x, x > 0         borrar x
    # 0                 inicializar un cmt nuevo
    # x, x > 0          actualizar cmt x
    #3 modificar - caso: id == 0 - cmt nuevo
    #   devuelve: el número id. del cmt nuevo
    if not dat_post[ "id" ]:
        # fallo: si el navigador del cliente cambia el valor de
        # 'id_publ', no aparecerá en la publicación destinada
        bbdd1.execute(
        "INSERT INTO cmt (id_usr, id_publ, ctndo) "\
"VALUES( ?, ?, ? );", (g.usr["id"], dat_post[ "id_publ" ], '') )
        bbdd1.commit()
        rstdo = bbdd1.execute("SELECT * FROM cmt " \
"WHERE id_usr = ? ORDER BY creado DESC LIMIT 1; ", \
        (g.usr["id"], )  ).fetchone()
        return jsonify( {"id": rstdo[ "id" ]} )
    #end if
    #4 modificar - id < 0: borrar cmt
    # id > 0: actualizar cmt
    # devolver: 0
    if dat_post[ "id" ] < 0:
        borrar = 1
        dat_post[ "id" ] *= -1
    else: borrar = 0
    #end if
    duegno = bbdd1.execute(
    "SELECT id_usr FROM cmt "\
"WHERE id = ?", (dat_post["id"],) ).fetchone()["id_usr"]
    if duegno != g.usr[ "id" ]:
        flash( "permiso de edición inválido" )
        abort( 403, "permiso de edición inválido" )
    #end if
    if not borrar:
        if google_rsp( dat_post[ "ficha" ] ):
            bbdd1.execute(
                "UPDATE cmt SET ctndo = ? WHERE id = ?", (
                desinfectar( dat_post["ctndo"] ),
                dat_post[ "id" ] )
            )
        else: abort( 400, "no se pudo cumplir la solicitud" )
    else:
        bbdd1.execute(
        "DELETE FROM cmt WHERE id = ?", ( dat_post[ "id" ], ) )
    #end if
    bbdd1.commit()
    return jsonify( {"id": 0} )
#end def modificar

@sqm1.route( "/<id_publ>", methods = ( "GET", ) )
def ver_publ( id_publ ):
    bbdd1 = obt_bbdd()
    #5 ver_publ paso 1: construir el camino del archivo
    #   de la publicación
    rstdo = bbdd1.execute(
    "SELECT publ.achvo, ctg.pdr, ctg.id " \
"FROM publ INNER JOIN ctg " \
"WHERE publ.id_ctg = ctg.id " \
"AND publ.id = ?", ( id_publ, )
    ).fetchone()
    
#    print( '**** rstdo["id"]', rstdo["id"] )
    # hay que extraer el camino de la ctg
    achvo_publ = os.path.join(
    "instance",
    *de_arb_ctg( rstdo["id"], "camino" ),
    rstdo[ "achvo" ] )
    
    #6 ver_publ: paso 2: obtener cmtos y archivo
    rstdo = bbdd1.execute(
    "SELECT id, ctndo, id_usr FROM cmt " \
"WHERE id_publ = ? ", ( id_publ, )
    ).fetchall()
    
    with open( achvo_publ ) as achvo1:
        publ1 = achvo1.read()
    #end with
    
    return render_template(
    "publ.html", publ = publ1, id_publ = id_publ, cmtos = rstdo )
#        recap_url = current_app.config[ "URL_GOOGLE_RECAP" ] )
#end def
@sqm1.route("/")
def index():
    bbdd1 = obt_bbdd()
    publes = bbdd1.execute(
    "SELECT id, id_ctg, creado, titulo FROM publ " \
                "ORDER BY creado DESC" ).fetchall()
    nomes = { ii[ "id" ] : de_arb_ctg( ii["id_ctg"], "nom" ) for ii in publes }
#    for ii in nomes: print(nomes[ii])
#    #end for
    return render_template( "index.html", publes = publes, nomes = nomes )
#end def index
def google_rsp( ficha ):
        with open("llaverecap") as aa:
            param = {
                "secret": aa.read(),
                "response": ficha
            }
        google_rsp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            param )
        google_rsp = json.loads( google_rsp.text )
        return jsonify( google_rsp[ "success" ] )
