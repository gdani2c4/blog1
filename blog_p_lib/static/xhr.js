function enviar_mensaje( mnsj )
{
	console.log( "hasta aquí todobién" );
	if( window.XMLHttpRequest )
		pet_http = new XMLHttpRequest();
	else if( window.ActiveXObject )
		pet_http = new ActiveXObject( "Microsoft.XMLHTTP" );
	pet_http.overrideMimeType( "application/json" );
//	pet_http.onreadystatechange = env_mnsj_rll;
	pet_http.onload = env_mnsj_rll;
	pet_http.open( "GET", "env_ficha", true );
	pet_http.send();
	return 0;
}
function env_mnsj_rll()
{
//	if( pet_http.readyState == 4 )
	console.log( "¡respuesta recibida!" );
	var rsp = JSON.parse( pet_http.responseText );
	if( rsp == 0 ) {
		var mnsj_div = document.createElement("div");
		mnsj_div.setAttribute( "class", "flash" );
		var mnsj = document.createTextNode(
			"** se mandó el enlace de verificación " +
			"por correo electrónico **" );
		mnsj_div.appendChild(mnsj);
		var header = document.querySelector("header");
		header.insertAdjacentElement( "afterend", mnsj_div );
	}
	return 0;
}
