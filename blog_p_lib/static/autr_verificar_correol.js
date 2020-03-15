function enl_boton()
{
	document.querySelector( "input" ).onclick = function() {
		event.preventDefault();
		console.log( "aqí en enlazar boton" );
		enviar_mensaje( "nada" );
	};
}
