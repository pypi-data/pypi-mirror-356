$(document).ready(function(){

	//$("input[name*='-descripcion']").attr("readonly","true");
	$("input[name*='-precio_unitario']").attr("readonly","true");
	$("input[name*='-precio_total']").attr("readonly","true");

});

$("select[name*='-tipo']").on("change",function(){
// debugger	
	var id_c=this.name;
	var uno_id=id_c.replace("detallecotizacion_set-", "");
	var res_id=uno_id.replace("-tipo", "");
	var namecant="detallecotizacion_set-"+res_id+"-cantidad";
	var nameancho="detallecotizacion_set-"+res_id+"-ancho";
	var namealto="detallecotizacion_set-"+res_id+"-altura";
	var nameempaque="detallecotizacion_set-"+res_id+"-empaque";
	var namecepillo="detallecotizacion_set-"+res_id+"-cepillo";
	var nameempaque_costo="detallecotizacion_set-"+res_id+"-empaque_costo";
	var namecepillo_costo="detallecotizacion_set-"+res_id+"-cepillo_costo";
	var namecepillo_costo="detallecotizacion_set-"+res_id+"-cepillo_costo";
	var nametipo="detallecotizacion_set-"+res_id+"-tipo";
	var namega="detallecotizacion_set-"+res_id+"-ga";
	debugger

	var tipo=this.value;
	var tiposs= $(this).find('option:selected').text();
	if (tiposs=='RC') 
	{
		 $("input[name="+namecant+"]").val('1');
		$("input[name="+nameancho+"]").val('1');
		$("input[name="+namealto+"]").val('1');
		$("input[name="+namega+"]").val('0');
	}
	
	if (tiposs=='MT') 
	{		 $("input[name="+namecant+"]").val('1');
		$("input[name="+nameancho+"]").val('1');
		$("input[name="+namealto+"]").val('1');
		$("input[name="+namega+"]").val('0');
	}
	
	if (tiposs=='MTG') 
	{		 $("input[name="+namecant+"]").val('1');
		$("input[name="+nameancho+"]").val('1');
		$("input[name="+namealto+"]").val('1');
		$("input[name="+namega+"]").val('0');
	}
	
	var cantidad = $("input[name="+namecant+"]").val();
	var ancho = $("input[name="+nameancho+"]").val();
	var altura = $("input[name="+namealto+"]").val();
	var empaque = $("input[name="+nameempaque+"]").val();
	var cepillo = $("input[name="+namecepillo+"]").val();
	var empaque_costo=$("input[name="+nameempaque_costo+"]").val();
	var cepillo_costo=$("input[name="+namecepillo_costo+"]").val();

	get_calcular(cantidad,ancho,altura,tipo,res_id,empaque,cepillo,empaque_costo,cepillo_costo)

});
function totales()
{			// debugger
			var precio=0;
			$( "[name*='precio_total']" ).each(function() {
			
				precio=precio+parseFloat($(this).val());

				console.log(precio)
				//$("#totalgeneral").val(precio);

			});
			$( "[name*='cepillo_costo']" ).each(function() {
			
				precio=precio+parseFloat($(this).val());

				console.log(precio)
				//$("#totalgeneral").val(precio);

			});
			$( "[name*='empaque_costo']" ).each(function() {
			
				precio=precio+parseFloat($(this).val());

				console.log(precio)
				//$("#totalgeneral").val(precio);

			});
				document.getElementById("totalgeneral").value = precio;
}
function get_calcular(cantidad,ancho,altura,tipo,id,empaque,cepillo,empaque_costo,cepillo_costo){

		$.ajax({
	 	   	url:'/djmicrosip_cotizacion_puertas/calculo/',
	 	   	type : 'get',
	 	   	data : {
	 	   		'cantidad':cantidad,
	 	   		'ancho':ancho,
	 	   		'altura':altura,
	 	   		'tipo':tipo,
	 	   		'empaque':empaque,
	 	   		'cepillo':cepillo,
	 	   		'empaque_costo':empaque_costo,
	 	   		'cepillo_costo':cepillo_costo,
	 	   	},
	 	   	success: function(data){
	 	   		var namedesc="detallecotizacion_set-"+id+"-descripcion";
	 	   		$("input[name="+namedesc+"]").val(data.descripcion);
	 	   		var namedesc="detallecotizacion_set-"+id+"-precio_unitario";
	 	   		$("input[name="+namedesc+"]").val(data.unitario);
	 	   		var namedesc="detallecotizacion_set-"+id+"-precio_total";
	 	   		$("input[name="+namedesc+"]").val(data.total);
	 	   		var namedesc="detallecotizacion_set-"+id+"-empaque_costo";
	 	   		$("input[name="+namedesc+"]").val(data.empaque_costo);
	 	   		var namedesc="detallecotizacion_set-"+id+"-cepillo_costo";
				$("input[name="+namedesc+"]").val(data.cepillo_costo);
	 	   		totales()
			},
		});
}


