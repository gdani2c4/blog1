import functools
from flask import ( jsonify,
Blueprint, flash, g, redirect, render_template,
request, session, url_for, current_app )
from werkzeug.security import check_password_hash, \
generate_password_hash
from blog_p_lib.bbdd import obt_bbdd
from secrets import token_urlsafe
import blog_p_lib.util as util

sqm1 = Blueprint( "autr", __name__, url_prefix = "/autr" )

@sqm1.route( "/reg", methods = ( "GET", "POST" ) )
def reg():
    if request.method == "POST":
        nom_usr = request.form[ "nom_usr" ]
        ctsna = request.form[ "ctsna" ]
        correol = request.form[ "correol" ]
        bbdd1 = obt_bbdd()
        error = None
        if not nom_usr:
            error = "falta nombre de usuario"
        elif not ctsna:
            error = "falta una contraseña"
        elif not correol:
            error = "falta la dirección de correo electrónico"
        elif bbdd1.execute(
            ( "SELECT id FROM usr WHERE "
              "nom_usr = ? OR correol = ?" ),
              ( nom_usr, correol )
            ).fetchone() is not None:
                error = ( "se encontró el nombre %s o la "
                    "dirección %s en otra perfil, por favor "
                    "elegir otro" )
       
        if error is None:
            bbdd1.execute(
            ( "INSERT INTO usr "
              "(nom_usr, ctsna, correol, tt) "
              "VALUES (?, ?, ?, ? )" ),
            ( nom_usr, generate_password_hash( ctsna ),
                correol, current_app.CNTA_PND )
            )
            bbdd1.commit()
            return redirect( url_for( "autr.ini_ses" ) )
        # fi
        flash( error )
    # fi
   
    return render_template( "autr/registrar.html" )
# fed
@sqm1.route( "/iniciar_sesion", methods = ( "GET", "POST" ) )
def ini_ses():
    if request.method == "POST":
        form_nom_usr = request.form[ "nom_usr" ]
        form_ctsna = request.form[ "ctsna" ]
        bbdd1 = obt_bbdd()
        error = None
        usr = bbdd1.execute(
        "SELECT * FROM usr WHERE nom_usr = ?",
        ( form_nom_usr, )
        ).fetchone()

        if usr is None:   
            error = "nombre de usuario equivocado"
        elif not check_password_hash(
        usr[ "ctsna" ], form_ctsna ):
            error = "contraseña incorrecta [¡]"
       
        if error is None:
            session.clear()
            session[ "usr_id" ] = usr[ "id" ]
            session[ "tt" ] = usr[ "tt" ]
            if usr["tt"] == current_app.CNTA_PND:
                return redirect( url_for( "autr.veri_corr" ) )
            return redirect( url_for( "index" ) )
       
        flash( error )
   
    return render_template( "autr/iniciar_sesion.html" )
# }

@sqm1.before_app_request
def cargar_usr_ensesion():
    usr_id = session.get( "usr_id" )
    # caso: la petición no pertenece a una sesión:
    if usr_id is None:
        g.usr = None
    else:
        # S id, tt, nom_usr F usr W id = usr_id L 1
        g.usr = obt_bbdd().execute(
        "SELECT id, tt, nom_usr FROM usr WHERE id = ?",
        ( usr_id , )  ).fetchone()
        if ( g.usr != None
            and g.usr["tt"] == current_app.CNTA_PND
            and request.endpoint.split('.')[0] != "autr"
            and request.path.split('/')[1] != "static"
        ):
            return redirect( url_for( "autr.veri_corr" ) )
# fed
@sqm1.route( "/salir" )
def salir():
    session.clear()
    return redirect( url_for( "index" ) )
# }

def ini_ses_obl( vista ):
    @functools.wraps( vista )
    def vista_envuelta( **args1 ):
        if g.usr is None:
            return redirect( url_for( "autr.ini_ses" ) )
       
        if g.usr["tt"] == current_app.CNTA_PND:
            return redirect( url_for( "autr.veri_corr" ) )
        if g.usr["tt"] == current_app.CNTA_VER:
            return vista( **args1 )
   
    return vista_envuelta
# }
@sqm1.route( "/verificar_correol" )
def veri_corr():
    usr = {
        "nom_usr": g.usr["nom_usr"],
        "correol": obt_bbdd().execute(
            "SELECT correol FROM usr WHERE id = ?",
            ( g.usr["id"], )
        ).fetchone()[0]
    }
    return render_template( "autr/verificar_correol.html",
        usr = usr
    )
# fed
@sqm1.route( "/env_ficha" )
def env_ficha():
    mnsj =    ("Subject: danigil.com verificar cuenta\n\n"
             "por favor entre al enlace siguiente "
             "para verificar su cuenta: "
            )
    bbdd1 = obt_bbdd()
    if g.usr["tt"] == current_app.CNTA_PND:
        val = bbdd1.execute(
            ("SELECT val FROM usr_tmp "
             "WHERE id_usr = ?"), (g.usr["id"], )  ).fetchone()
        ficha = val["val"] if ( val != None ) else \
            token_urlsafe( current_app.ficha_lon )
        mnsj += "\n%s%s?ficha=%s" % ( request.url_root, url_for(
            "autr.verif_ficha")[1:], ficha )
        bbdd1.execute(
            ("INSERT INTO usr_tmp ( val, id_usr ) "
             "VALUES ( ?, ? );"), ( ficha, g.usr["id"] )
        )
        bbdd1.commit()
        util.env_corr( mnsj,
            bbdd1.execute(
                "SELECT correol FROM usr WHERE id = ?",
                ( g.usr["id"], )  ).fetchone()[0]
        )
        return jsonify( 0 )
    # fi
    return jsonify( "la cuenta no está pend. de verif[¡]" )
# devuelve 0 - se actualizó, 1 - error
@sqm1.route( "/verif_ficha" )
def verif_ficha():
    ficha_solic = request.args.get( "ficha" )
    bbdd1 = obt_bbdd()
    ficha_reg = bbdd1.execute(
        "SELECT val FROM usr_tmp WHERE id_usr = ?",
        ( g.usr["id"], )  ).fetchone()
    if ficha_reg != None and ficha_solic == ficha_reg[0]:
        bbdd1.execute(
            "UPDATE usr SET tt = ? WHERE id = ?",
            ( current_app.CNTA_VER, g.usr["id"] )  )
        bbdd1.commit()
        bbdd1.execute(
            "DELETE FROM usr_tmp WHERE id_usr = ?",
            ( g.usr["id"], )  )
        bbdd1.commit()
        flash( "¡se actualizó el estado de la cuenta!" )
        return redirect( url_for( "index" )  )
	# fi
    flash( "no se ha podido actualizar el estado de la cuenta" )
    return redirect( url_for( "autr.veri_corr" )  )
# fed
