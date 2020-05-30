
//var $TABLE = $('#table');
var $CLON = $('#TablaClon');
var $GUARDAR = $('#export-btn');
var $EXPORT = $('#datos');
var $TABLE = null;
var c_tmp=1;
var SELE="tomato", DSEL="white", ADV="yellow";
var ObjDatos=[];//{'accion':"", "id":-1, "datos":[-1]}
var ID_TABLA_ACTIVA=null;  // almacena el id de la tabla activa, es decir en uso
var TBL_LISTA = null;      // almacena el id de la tabla para listar
var DIV_LISTA = null;      // almacena el id del div que contiene TBL_LISTA
var $CLD_LISTAR = null;     // almacena el id de la celda donde se requiere listar TBL_LISTA
var VALOR_TMP = null;
var DATOS = {'cant':-1, 'cumedida':-1, 'total':-1}
var TOTAL = null; // almacena el id de la celda que muestra el total
var SUBTOTAL = null //almacena el id de la celda que mantiene el subtotal
var SBTOTALS = [];
var count_esc = 0;


document.body.addEventListener("keydown", function(event) {
  console.log(event.code, event.keyCode);
  if (event.code === 'Escape' || event.keyCode === 27) {
    // Aqui la lógica para el caso de Escape ...
    if ( count_esc == 0 ){
		$(DIV_LISTA).css("display","none");		
		$("#Blistar").removeClass("modificando_lista");
		$("#Blistar").remove();
		EliminarRegistro($('.seleccionado').attr("id"));
		cotn_esc = 0;
	}

  }
});

function Cambios(datos){
	var enc =-1;
	
	if ( datos.id != -1 ){
		for (i=0; i<ObjDatos.length; i++){
				if (datos.id == ObjDatos[i].id){
					enc = i
					break;				
				}
		}
		if(enc!=-1){
			ObjDatos[enc].datos = datos.datos;
			ObjDatos[enc].accion = datos.accion;
			console.log("Encontrado: ");
			console.log(ObjDatos);
		}else{
			if ( datos.id != NaN ){
				ObjDatos.push(datos);
				console.log("No Encontrado: ");
				console.log(ObjDatos);
			}
		}
	}else{
		console.log("ID es Nan");
	}

}

function Existentes(id_reg){
	//~ Verifica la existencia del registro que se quiere agregar
	var existe = -1;
	//~ console.log("Registro: " + id_reg+ "  " + ID_TABLA_ACTIVA);
	$(ID_TABLA_ACTIVA + " > tbody > tr").each(function(i, elemento){
		
		console.log( $(elemento).find("td").eq(1).text() + " === " + id_reg);
		
		if ( $(elemento).find("td").eq(1).text() === id_reg ){
			existe = $(elemento).attr("id");
			return false;
		}
	});
	return (existe);
}

function FiltrarInsumos(patron="") {
	//~ Filtra la tabla activa 
	var input, filter, table, tr, td, i, txtValue;
	
  filter = patron.toUpperCase(); //input.value.toUpperCase();
  table = document.getElementById(TBL_LISTA);
  tr = table.getElementsByTagName("tr");
  // Filtra la tabla de acuerdo al patron ingresado
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[DATOS['cld_listar']-1];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function Listar(id){
	// Captura la modificacion de la celda, en este caso la segunda celda de la fila
	// es la que interesa
	
	//~ console.log("Keypress...filtrando productos");	
    var pos = {};
	var rect = $(id).position();

	pos.ancho = $(id).width();
	pos.alto  = $(id).height();
	pos.x     = window.scrollY + id.getBoundingClientRect().top  + pos.alto + 10;
	pos.y     = window.scrollX + id.getBoundingClientRect().left;
	$(DIV_LISTA).offset({top:pos.x,left:pos.y});	
	FiltrarInsumos($(id).val());
	$(DIV_LISTA).show();
}

function ModificarCantidad(id){
    
    console.log("MODIFICAR CANTIDAD");
    
    var pos = {};
	var rect = $(id).position();
	var input = "<input id='MCantidad' type='text' name='MCantidad'  style='width:100%;' text-align:right; placeholder='Ingrese la cantidad..'>";
	var VALOR_TMP = $(id).html();

	if ( !$(id).hasClass("modificando_cant") ) {

		$(id).addClass("modificando_cant");
		$(id).text("");	
		$(id).append(input);
		$("#MCantidad").val(VALOR_TMP);
		
		$("#MCantidad").keyup(function(e){
			//~ var valor = 
			if (e.which == 13){
				$(".modificando_cant").text($(this).val());
				
				//~ console.log($(".modificando_cant").attr("i"));
				CalculoTotalRegistro(".modificando_cant");
				$(this).val("");
				$(".modificando_cant").removeClass("modificando_cant");
				$("#MCantidad").hide();
				//~ Cambios({"accion": "actualizar", "id": parseInt(id), "datos":parseFloat($(this).val())})
			}
			if (e.which == 27){
				$(".modificando_cant").text(VALOR_TMP);
				$(this).val("");
				$(".modificando_cant").removeClass("modificando_cant");
				$("#MCantidad").hide();
				VALOR_TMP = null;
			}
			
			});
	}
	$("#MCantidad").focus();
	
}

function SelTblListar(idreg){	
	//~ console.log("Seleccionando datos de la lista...");
	
	var campo = [];
	var id;
	$(idreg).find("td").each(function(i,e){
		campo.push($(e).html());
	});
	
	//~ console.log("DATOS:");
	//~ console.log(campo[DATOS['cld_listar']]);		
	
	if (Existentes(campo[DATOS['cld_listar']-1]) == -1){
		if ( ID_TABLA_ACTIVA == "#Insumos_prd" ){
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(0).text(campo[0]);
			//~ $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(1).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(1).text(campo[1]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(2).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(3).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(4).text(1);
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(4);
		}
		if ( ID_TABLA_ACTIVA == "#Materiales_prd" ){
			//~ console.log("----------");
			//~ console.log(campo);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(4).text(1);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(5).text(campo[4]);
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(4);
		}
		if ( ID_TABLA_ACTIVA == "#Otros-costos_prd" ){
			//~ console.log("----------");
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(4).text(1);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(5).text("2");
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(4);
		}
		if ( ID_TABLA_ACTIVA == "#Ingrediente_partida" ){
			//~ console.log("----------");
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(4).text(campo[4]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(5).text(1);
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(5);
		}
		$("#Blistar").removeClass("modificando_lista");
		$("#Blistar").remove();
		$( $(DIV_LISTA) ).hide();
		
		CalculoTotalRegistro(id);
		CalculoTotal();
		SeleccionarRegistro($(".seleccionado"));
		
		//~ console.log("SALIENDO: Seleccionando datos de la lista...");
	}else{
			$("#linsumos").hide();
			alert("El registro que desea agregar ya existe...");
			
	}
}

function CalculoTotalRegistro(id){	
	
	var cant, cmax, total_u; //, total;

	cant = parseFloat( $(id).text().replace(",",".") );
	
	cumedida = parseFloat($(id).parent().find("td").eq(DATOS['cumedida']).text().replace(",",".")); //costo maximo por unidad de medida	
	total_u = (cant*cumedida).toFixed(2);
	//~ console.log(cant + "  "+ cumedida + "   "+ total_u);
	$(id).parent().find("td").eq(DATOS['total']).text(total_u.replace(".",",") );
	CalculoTotal()
	datos ={ "destino":DESTINO, "accion":"actualizar", "id":parseInt($(id).parent().find("td").eq(0).text()), "datos":cant};
	Cambios(datos);
}

function CalculoTotal(){
	var total = 0.0;
	var sbtotal = 0.0;
	console.log("Calculo del Total");
	if ( $(ID_TABLA_ACTIVA + " tbody" ).length > 0 ){
		$(ID_TABLA_ACTIVA + " > tbody > tr" ).each(function(i, elemento){
			sbtotal = sbtotal + parseFloat($(elemento).find("td").eq(DATOS['total']).text().replace(",",".")); 	
			//~ console.log(sbtotal);
		});
	}
	$( SUBTOTAL ).text( (sbtotal.toFixed(2)).replace(".",","));
	for (i=0;i<SBTOTALS.length;i++){
		total = total + parseFloat($( SBTOTALS[i] ).html().replace(",","."));
		//~ console.log(parseFloat($( SBTOTALS[i] ).html()) + "  " + total );
	}
	total_prod = total.toFixed(2).replace(".",",");
	//~ datos ={ "total_prod":total_prod, "accion":"actualizar", "id":parseInt($(id).parent().find("td").eq(0).text()), "datos":cant};
	$( TOTAL ).html(total_prod);
	
}

$("#Materiales").change( function(){
	//recalcula cuando se elimina una fila de la tabla
	CalculoTotal();
});

function CerrarLista(id){
	$(DIV_LISTA).css("display","none");
}

function AgregarRegistro(id){
	console.log("Agregando registro");

	var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');
	  
	$TABLE = $(ID_TABLA_ACTIVA);
	console.log(ID_TABLA_ACTIVA);
	//~ console.log("idTABLE: " + idTABLE + " TABLE: " + '#'+$(this).attr("name"));
	
	$clone.attr("class","table-remove");
	$TABLE.append($clone); 
	//~ RecalcularFormularios("AGREGAR", '#' + $(this).attr("name") );
	
	if ( ID_TABLA_ACTIVA === "#Materiales_prd" ){
		
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese el nombre...'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					//~ console.log("VALOR: ingresando");
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TABLA_ACTIVA === "#Insumos_prd" ){
	
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TABLA_ACTIVA === "#Otros-costos_prd" ){
		//~ console.log("fffff: " + ID_TABLA_ACTIVA);
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TABLA_ACTIVA === "#Ingrediente_partida" ){
		//~ console.log("Ingrediente_partida: " + ID_TABLA_ACTIVA);
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	
}

function EliminarRegistro(id){
	
	var $idTABLE = $(".seleccionado").parent();
	var DIR = $($idTABLE.parent()).attr("id");
	
	r = $(".seleccionado").find("td").eq(0).text() == "" ? -1 : parseInt($(".seleccionado").find("td").eq(0).text());
	Cambios({"destino":DESTINO, "accion": "eliminar", "id": r, "datos":-1} );
	
	$(".seleccionado").remove();
	CalculoTotal();
	//~ $idTABLE.trigger("change");
}

function SeleccionarTabla(id){
	tbl = '#' + $(id).attr("name");
	//~ console.log("Seleccionando Tabla: " + tbl);
	
	if ( tbl === "#Insumos_prd"){
		DESTINO = "INSUMOS";
		ID_TABLA_ACTIVA = '#Insumos_prd';
		TBL_LISTA       = 'TablaPartidas';
		DIV_LISTA       = '#lpartidas';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_insumo_prd';
		SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];		
	
	}
	
	if ( tbl === "#Materiales_prd" ){
		DESTINO  ="MAQYHERR";
		ID_TABLA_ACTIVA = '#Materiales_prd';
		TBL_LISTA       = 'TablaInsumos';
		DIV_LISTA       = '#linsumos';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_materiales_prd';
		SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];		
	}
	
	if ( tbl === "#OtrosCostos_prd" ){
		DESTINO  ="CSTSADNLS";
		ID_TABLA_ACTIVA = '#Otros-costos_prd';
		TBL_LISTA       = 'TablaCstsAdnls';
		DIV_LISTA       = '#CstsAdnls';
		$CLD_LISTAR      = $("#Otros-costos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		//~ TOTAL = '#costo_producto';
		SUBTOTAL = '#total_otros-costos_prd';
		SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];			
	}
	
	if ( tbl === "#Ingrediente_partida" ){
		DESTINO  ="PARTDETLLS";
		ID_TABLA_ACTIVA = '#Ingrediente_partida';
		TBL_LISTA       = 'TablaInsumos';
		DIV_LISTA       = '#linsumos';
		$CLD_LISTAR      = $("#Ingrediente_partida > tbody > tr > td:nth-child(3)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_partida';
		SUBTOTAL = '#total_ingrediente_partida';
		SBTOTALS = [ '#total_ingrediente_partida'];			
	}
}

$("tr[name=regn]").click(function (e) {
	SeleccionarRegistro(this);
});

function SeleccionarRegistro(id){
	var idTABLE = '#'+ $(id).closest("table").attr("id")+" tr";
	
	$(ID_TABLA_ACTIVA + " > tbody > tr").each(function(i,e){
		if( id != e ){
			if ( $(e).hasClass("seleccionado") ){
				$(e).css("background-color",DSEL);
				$(e).removeClass("seleccionado");
				$(e).removeClass("modificando_lista");
			}
		}
	});
	
	if ( $(id).hasClass("seleccionado") ) {
		$(id).css("background-color",DSEL);
		$(id).removeClass("seleccionado");
	}else {
		$(id).css("background-color",SELE);
		$(id).addClass("seleccionado");
	}	
}

$GUARDAR.click(function () {

	if ( ObjDatos.length == 0 ){
			alert("No hay Datos para almacenar");
	}else{
		
		ObjDatos.push({ "destino":"TOTALIZAR","accion":"actualizar", "id":-1, "datos":$( TOTAL ).html().replace(",",".")});
		$("#ObjDatos").val(JSON.stringify(ObjDatos));
			
		var winSize = {
		  wheight : $(window).height(),
		  wwidth : $(window).width()
		};
		//~ console.log(winSize);
		var modSize = {
		  mheight : $('#myModal3').height(winSize.wheight),
		  mwidth : $('#myModal3').width(winSize.wwidth)
		};
	  $('#myModal3').css({
		'background-color' : '#fff',
		'opacity': '0.9',
		'padding-top' :  ((winSize.wheight - (modSize.mheight/2))/2),
		'padding-left': '10px',

	  });
	  $('#dialogo').css({
		'background-color' : '#fff',
		'top' :  '15%',
		'left': '0%',
	  });
		$("#myModal3").modal({backdrop: "static"});
	}
		
});

function AbrirVentana(){
  var cg = document.getElementById("id_archivo1");
  cg.style.backgroundColor = "red";
  cg.click();
}

function agregar_archivos(){
  var patron = document.getElementById("patron");
  var nuevo = patron.cloneNode(true);
  var bpatron = document.getElementById("bpatron");
  var p = document.getElementById("principal");
  var cuerpo= document.getElementById("cuerpo");
  //var elem = nuevo.children


  if ( bpatron == null){
    console.log("eroor, no existe el objeto");
  }
  //bpatron.style.backgroundColor = "red";
  bpatron.setAttribute("class","oculto");  
  //bpatron.id = "b" + p.rows.length;
  nuevo.id = p.rows.length;  

  nuevo.style.display = "";
  cuerpo.appendChild(nuevo);
  console.log("entro");
}

function enviar_archivos(){

 // var arch = document.getElementByTagName("button");
  var arch = document.getElementsByClassName("oculto");

  console.log("Numero de Registros a guardar: " + arch.length);
  for ( var i=0; i<arch.length;i++){
    //alert('Llamado a la funcion ENVIAR: ' + i);
    //if (i.id == "b" + i){
      console.log("Enviando archivo numero: "+ i );  
      arch[i].click();
   // }
    
    //console.log('Taking a break...');
   
    //setTimeout(console.log.bind(null, 'Two second later'), 2000);
   
  }

}

function bs_input_file() {
  $(".input-file").before(
    function() {
      if ( ! $(this).prev().hasClass('input-ghost') ) {
        var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
        element.attr("name",$(this).attr("name"));
        element.change(function(){
          element.next(element).find('input').val((element.val()).split('\\').pop());
          console.log("se selecciono un archivo");

          //se añade un elemento mas para seguir agregando archivos
          var div_principal = document.getElementById("agregar_planos");

          var div = document.createElement("div");
          var span_agr = document.createElement("span");
          var button_agr = document.createElement("button");
          var input = document.createElement("input");
          var span_lim = document.createElement("span");
          var button_lim = document.createElement("button");
          
          div.setAttribute("class","input-group input-file");
          div.setAttribute("id","f2");
          div.setAttribute("name","Fichier2");
          span_agr.setAttribute("class","input-group-btn");
          span_lim.setAttribute("class","input-group-btn");
          
          button_agr.setAttribute("class","btn btn-default btn-primary");
          button_agr.setAttribute("type","button");
          //button_agr.setAttribute("onclick","bs_input_file()");
          button_agr.addEventListener("click", bs_input_file)
          button_agr.appendChild(document.createTextNode("Agregar"));

          button_lim.setAttribute("class", "btn btn-default btn-choose");
          button_lim.setAttribute("type","button");
          button_lim.appendChild(document.createTextNode("Limpiar"));

          input.setAttribute("class","form-control");
          //input.setAttribute("name", "lista")
          input.setAttribute("type","text");
          input.setAttribute("placeholder","Seleccionar archivo...");
          input.style.cursor = "pointer";

          //se construye el elemento completo que permite agregar archivos
          span_agr.appendChild(button_agr);
          span_lim.appendChild(button_lim);

          div.appendChild(span_agr);
          div.appendChild(input);
          div.appendChild(span_lim);

          div_principal.appendChild(div); 

          button_agr.click();
        });

        $(this).find("button.btn-primary").click(function(){
          element.click();
          console.log("Se realiza busqueda de archivo");

        });
        $(this).find("button.btn-choose").click(function(){
          element.val(null);
          $(this).parents(".input-file").find('input').val('');
        });
        $(this).find('input').css("cursor","pointer");
        $(this).find('input').mousedown(function() {
          $(this).parents('.input-file').prev().click();
          return false;
        });
        return element;
      }
    }
  );
}

$(function() {
  //bs_input_file();
  // enviar_archivos();
});

function enviar(){

  var lista = document.getElementByTagName("input");
  console.log("Ingreso al envio");
  for (var i = 0; i < lista.length; i++) {
    console.log(lista[i].value);
  }

/*
  if (inputFile.files.length > 0) {
        let formData = new FormData();
        formData.append("archivo", inputFile.files[0]); // En la posición 0; es decir, el primer elemento
        fetch("guardar.php", {
            method: 'POST',
            body: formData,
        })
            .then(respuesta => respuesta.text())
            .then(decodificado => {
                console.log(decodificado);
            });
    } else {
        // El usuario no ha seleccionado archivos
        alert("Selecciona un archivo");
    }
    */
}

function actualizarLista(){
        var inpute = document.getElementById("boton-file");
        var lista = inpute.files;
        var cad = "Total archivos:" +lista.length + "<br />";
        for (var i=0; i<lista.length; i++){
            if (cad != "") cad += "------------------<br />";
            cad += "Nombre: " + lista[i].name + "<br />" +
                   "Tipo: " + lista[i].type + "<br />" +
                   "Tamaño: " + lista[i].size + " bytes<br />" +
                   "RUTA: " + lista[i].value + " bytes<br />" +
                   "Fecha: " + lista[i].lastModifiedDate + "<br />";
                   
        }
        document.getElementById("lista-archivos").innerHTML = cad;
    }

function handleFileSelect(evt) {
  var files = evt.target.files; // FileList object

  // files is a FileList of File objects. List some properties.
  var output = [];
  for (var i = 0, f; f = files[i]; i++) {
      console.log(f.name);
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                f.size, ' bytes, last modified: ',
                f.lastModifiedDate.toLocaleDateString(), '</li>');
  }
  document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

function ExtraerTabla($id_tabla) {

	var clave = new Array();
	var tmp = {};
	var tmpp = {};
	var json = "";
	// se obtiene la cabecera de la tabla
	$($id_tabla + " thead > tr th").each(function(){
		clave.push($(this).text().toLowerCase());
	});
	
	$($id_tabla + " tbody > tr").each(function(idr, er){
		$(er).find("td").each(function(idc, ec){
			tmp[clave[idc] ] = $(ec).text();
		});
		json = json + JSON.stringify(tmp)+","  ;
		tmpp[idr] = tmp;
	});
	
	json = "["+ json.slice(0,-1) + "]";
return json	; 
}

