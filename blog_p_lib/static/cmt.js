function modo_ed( id ) {
	if( activar(id) ) {
		alert( "ya hay un comentario en edición" );
		return 1;
	}
	$(`#cmt${id}`).children("p").replaceWith(
		"<textarea name='ctndo_post' cols=20 rows=10>" + 
		$(`#cmt${id}`).children("p").text() + 
		"</textarea>"
	);
	$(`#cmt${id}`).children("[type='submit']").attr(
		"value", "publicar cambios" );
	document.querySelector(
		`#cmt${id} > input[ type = "submit" ]` ).
		onclick = al_env;
//		`grecaptcha.execute();
//		actu( ${id} ); return false;` );
	$(`#cmt${id}`).children(`#dejar_cambios`).html(
	`<input type = "button" value = "dejar cambios"
	 onclick="volver( ${id} ); return false;">`);
}
function volver( id ) {
	/* cambiar la caja de edición de texto al
	contenido original del texto */
	$.getJSON( "/publ/cmt", {cmt_id: id},
	function( cmt_rstdo ) {
//		if( cmt_rstdo[ "cmt_null" ] ) {
//			alert( "el comentario no se encontró" );
//			location.reload();
//		}
		let elm_nvo = document.createElement("p");
		elm_nvo.innerText = cmt_rstdo[ "ctndo" ];
		elm_ant = document.querySelector(`#cmt${id} textarea`);
		document.querySelector(`#cmt${id}`).replaceChild(
			elm_nvo, elm_ant );
//		$(`#cmt${id}`).children("textarea").replaceWith(
//		"<p>" + cmt_rstdo[ "ctndo" ] + "</p>" );
	} );

	/* convertir el botón "enviar" en "escribe una
		revisión" y borrar el elemento "dejar cambios"
	 */
	console.log( "********", id );
	document.querySelector(
		`#cmt${id} > input[ type = "submit" ]` ).
		onclick = a_modo_ed.bind( undefined, id );
	$(`#cmt${id}`).children("[type='submit']").attr(
		"value", "revisar" );
	$(`#cmt${id}`).children(`#dejar_cambios`).empty();
	$("#activo").remove();
}
function actu( id, ficha = "" ) {
error_guardar = "¡error! no llevó al cabo la " +
	"solicitud. por favor copia y guarda el " +
	"comentario y pruebalo más tarde. "
	"si el error vuelve, por favor ponte en " +
	"contacto con el administrador del sitio";
	dat_post = {};
	/*
	 id == 0		añadir cmt nuevo
	 id >  0		actualizar
	 id <  0		borrar
	 */
	if( ! id ) {
		if( $("#activo").length != 0 )  {
			alert( "ya hay algo en edición" );
			return 1; }
		dat_post.id_publ = $("#publ").attr("name");
	}
	else if ( id > 0 ) {
		/* el caso de actualizar:
			no he podido sacar el valor del elemento "textarea"
			revisado sino por el método "serializeArray()", y
			es por eso la enredosa manera de sacar el texto
			del bucle siguente:
		 */
		for( ii of $( `#cmt${id}` ).serializeArray() )
			if( ii["name"] == "ctndo_post" ) {
				ctndo = ii[ "value" ];
				break;
			}
		if( ctndo == undefined )
			alert( error_guardar );
	
		dat_post[ "ctndo" ] = ctndo;
	}
	dat_post[ "id" ] = id;
	dat_post[ "ficha" ] = ficha;
	$.ajax( "/publ/cmt/post", {
		type: "POST",
		data: JSON.stringify( dat_post ),
		success: function( datos ) {
		if( id == 0 )
			cmt_nuevo( datos["id"], cnt = 1 );
		else if( id < 0 ) document.querySelector(
			`#cmt${-id}` ).remove();
		else volver( id );
		grecaptcha.reset();
		}.bind( id ),
		error: function() {
			mnsj_flash = document.createElement("p");
			mnsj_flash.innerText = error_guardar;
			document.querySelector("#blq_mnsj").
				appendChild( mnsj_flash );
			},
		contentType: "application/json"
	} );
}
