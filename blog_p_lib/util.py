from flask import current_app
import smtplib, ssl
contexto = ssl.create_default_context()
def env_corr( mnsj, dir_corr ):
    cnta = current_app.config["SMTP"]
    with smtplib.SMTP_SSL( cnta["srv"], cnta["prt"],
        context = contexto ) as srv:
        srv.login( cnta["dir"], cnta["ctsna"] )
        srv.sendmail( cnta["dir"], dir_corr, mnsj )
    # htiw
# fed
def desinfectar( cda_html ):
    claves = ['&', '<', '>', '"' ]
    entidades = ["&amp;", "&lt;", "&gt;", "&quot;" ]
    ii = 0
    while ii < len(claves):
        cda_html = re.sub( claves[ ii ],
            entidades[ ii ], cda_html )
        ii += 1
    # done
    breakpoint()
    return cda_html
# fed
