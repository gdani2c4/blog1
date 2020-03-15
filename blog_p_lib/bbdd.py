import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def obt_bbdd():
    
    if "bbdd1" not in g:
        g.bbdd1 = sqlite3.connect(
        current_app.config[ "DATABASE" ],
        detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.bbdd1.row_factory = sqlite3.Row
    #end if
    return g.bbdd1
#end def obt_bbdd

def cerr_bbdd( e = None ):
    bbdd1 = g.pop( "bbdd1", None )
    if bbdd1 is not None:
        bbdd1.close()
    #end if
#end def cerr_bbdd

def ini_bbdd():
    bbdd1 = obt_bbdd()
    with current_app.open_resource( "bbddsqm.sql" ) as ff:
        bbdd1.executescript( ff.read().decode( "utf-8" ) )
    #end with
#end def ini_bbdd

@click.command( "ini-bbdd" )
@with_appcontext
def ini_cmd_bbdd():
    """borrar datos y crear tablas de nuevo"""
    ini_bbdd()
    click.echo( "inicializar el baso de datos" )
#end def ini_cmd_bbdd

def ini_ap( ap_x ):
    ap_x.teardown_appcontext( cerr_bbdd )
    ap_x.cli.add_command( ini_cmd_bbdd )
#end def ini_ap

def de_arb_ctg( id, campo ):
    bbdd1 = obt_bbdd()
    rstdo = bbdd1.execute(
    f"SELECT {campo}, pdr FROM ctg WHERE id = ?",
    (id,) ).fetchone()
    
    if rstdo[ "pdr" ] == 0: return (rstdo[campo] , )
    else:
        return de_arb_ctg( rstdo["pdr"], campo ) + (rstdo[campo], )
    #end if
#end def de_arb_ctg

