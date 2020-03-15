var agnad_cmt_recap_id;
function activar( id ) {
	if( $("#activo").length != 0 ) return 1;
	$(`#cmt${id}`).prepend("<div id='activo'></div>");
	return 0;
}
function al_env( event )
{
	event.preventDefault();
	grecaptcha.execute();
}
function recapejec_rll( token )
{
	console.log( "*".repeat(20) + "ficha: " + token );
	actu( Number( document.querySelector("#activo").
		parentElement.id.slice(3)  ), ficha = token );
}
function a_modo_ed( id, event )
{
	event.preventDefault();
	modo_ed( id );
}
//function agnad_cmt()
//{
//	id = actu( 0 );
//}
function cmt_nuevo( idn = 0, cnt = 0 ) {
	if( !cnt ) actu( 0 );
	else {
	//	$("#agnad_cmt").before( cmt_nuevo( idn ) );
		$("#agnad_cmt").before(`<form id = "cmt${idn}">
		<textarea name="ctndo_post" cols=20 rows=10></textarea>
		<span id="dejar_cambios"></span>
		<input type="submit" value="publicar">
		<input type="button" value="borrar"
		onclick = "actu( -${idn} ); return false;">
		</form>` );
		document.querySelector(
			`#cmt${idn} > input[type = "submit"]` ).
			onclick = al_env;
		activar( idn );
	}
}
