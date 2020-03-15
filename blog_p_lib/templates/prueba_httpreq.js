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
	pet_http.open( "GET", "xhr", true );
	pet_http.send();
	return 0;
}
function env_mnsj_rll()
{
//	if( pet_http.readyState == 4 )
	console.log( "¡respuesta recibida!" );
	console.log( JSON.parse( pet_http.responseText ) );
	return 0;
}
