
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
var DATOS = {'cant':-1, 'cmedida':-1, 'total':-1}
var TOTAL = null; // almacena el id de la celda que muestra el total
var SUBTOTAL = null //almacena el id de la celda que mantiene el subtotal
var SBTOTALS = [];


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
		//~ console.log(ObjDatos);
	}

	//~ console.log("Cambios");
	
}

function Existentes(id_reg){
	//~ Verifica la existencia del registro que se quiere agregar
	var existe = -1;
	//~ console.log("Registro: " + id_reg+ "  " + ID_TABLA_ACTIVA);
	$(ID_TABLA_ACTIVA + " > tbody > tr").each(function(i, elemento){
		//~ console.log(i);
		if ( parseInt($(elemento).find("td").eq(0).text()) == id_reg ){
			existe = $(elemento).attr("id");
			return false;
		}
	});
	return (existe);
}

function FiltrarInsumos(patron="") {
	//~ Filtra la tabla activa 
  var input, filter, table, tr, td, i, txtValue;

console.log(patron);
  filter = patron.toUpperCase(); //input.value.toUpperCase();
  table = document.getElementById(TBL_LISTA);
  tr = table.getElementsByTagName("tr");
  // Filtra la tabla de acuerdo al patron ingresado
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
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
			console.log("Modificando Cantidad");
			if (e.which == 13){
				$(".modificando_cant").text($(this).val());
				
				console.log($(".modificando_cant").attr("i"));
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

function Listar(id){
	// Captura la modificacion de la celda, en este caso la segunda celda de la fila
	// es la que interesa
	
	console.log("Keypress...filtrando productos");	
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

//~ $('#TablaInsumos tbody tr').click(function(){
function SelTblListar(idreg){	
	console.log("Seleccionando datos de la lista...");
	
	var campo = [];
	var id;
	$(idreg).find("td").each(function(i,e){
		campo.push($(e).html());
	});
	
	console.log(campo);
	//~ id        = $(idreg).find("td").eq(0).text();
	//~ codigo    = $(idreg).find("td").eq(1).text();
	//~ desc      = $(idreg).find("td").eq(2).text();
	//~ umedida   = $(idreg).find("td").eq(3).text(); //uniadd de medida
	//~ cant      = $(idreg).find("td").eq(4).text().replace(",",".")	; //cantidad
	//~ cmedida   = $(idreg).find("td").eq(5).text().replace(",",".");//costo maximo	por unidad de medida
	//~ cmin      = $(idreg).find("td").eq(6).text(); //costo minimo
	//~ cprom     = $(idreg).find("td").eq(7).text(); //costo promedio
	//~ cmax      = $(idreg).find("td").eq(8).text(); //costo maximo		
	
	if (Existentes(parseInt(campo[0])) == -1){
		if ( ID_TABLA_ACTIVA == "#Insumos_prd" ){
			//~ console.log(ID_TABLA_ACTIVA);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(1).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(2).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(3).text(1);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(4).text(campo[4]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(5).text(campo[4]);
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(3);
		}
		if ( ID_TABLA_ACTIVA == "#Materiales_prd" ){
			console.log("----------");
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(1).text(campo[2]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(2).text(campo[3]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(3).text(1);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(4).text(campo[4]);
			$( $(ID_TABLA_ACTIVA + ' tbody tr:last-child') ).find("td").eq(5).text(campo[4]);
			id = $( $(ID_TABLA_ACTIVA + ' tbody tr:last-child')).find("td").eq(3);
		}
		$("#Blistar").removeClass("modificando_lista");
		$("#Blistar").remove();
		$( $(DIV_LISTA) ).hide();
		
		//~ Cambios({"accion": "agregar", "id": parseInt(campo[0]), "datos":parseFloat(cant)})
		//~ ctotal = (cant*cmedida).toFixed(2).replace(".",",");
		//~ $('#Materiales tbody tr:last-child').find("td").eq(0).text(id);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(1).text(codigo);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(2).text(desc);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(3).text(umedida);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(2).attr("contenteditable", false	);

		//~ $('#Materiales tbody tr:last-child').find("td").eq(4).text(cant.replace(".",","));
		//~ $('#Materiales tbody tr:last-child').find("td").eq(5).text(cmedida.replace(".",","));
		//~ $('#Materiales tbody tr:last-child').find("td").eq(6).text(ctotal);
		//~ $("#linsumos").hide();
		
		CalculoTotalRegistro(id);
		CalculoTotal();
		SeleccionarRegistro($(".seleccionado"));
		
		//~ console.log("SALIENDO: Seleccionando datos de la lista...");
	}else{
			$("#linsumos").hide();
			alert("El registro que desea agregar ya existe...");
			
	}
	
	//~ if (Existentes(parseInt(id)) == -1){
		//~ Cambios({"accion": "agregar", "id": parseInt(id), "datos":parseFloat(cant)})
		//~ ctotal = (cant*cmedida).toFixed(2).replace(".",",");
		//~ $('#Materiales tbody tr:last-child').find("td").eq(0).text(id);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(1).text(codigo);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(2).text(desc);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(3).text(umedida);
		//~ $('#Materiales tbody tr:last-child').find("td").eq(2).attr("contenteditable", false	);

		//~ $('#Materiales tbody tr:last-child').find("td").eq(4).text(cant.replace(".",","));
		//~ $('#Materiales tbody tr:last-child').find("td").eq(5).text(cmedida.replace(".",","));
		//~ $('#Materiales tbody tr:last-child').find("td").eq(6).text(ctotal);
		//~ $("#linsumos").hide();
		//~ CalculoPartida()
		//~ SeleccionarRegistro($(".seleccionado"));
		//~ console.log("SALIENDO: Seleccionando datos de la lista...");
	//~ }else{
			//~ $("#linsumos").hide();
			//~ alert("El registro que desea agregar ya existe...");
			
	//~ }
}
//~ });

function CalculoTotalRegistro(id){	
	
	var cant, cmax, total_u; //, total;

	cant = parseFloat( $(id).text().replace(",",".") );
	cmedida = parseFloat($(id).parent().find("td").eq(DATOS['cmedida']).text().replace(",",".")); //costo maximo por unidad de medida	
	total_u = (cant*cmedida).toFixed(2);
	
	$(id).parent().find("td").eq(DATOS['total']).text(total_u.replace(".",",") );
	CalculoTotal()
	datos ={ "destino":DESTINO, "accion":"actualizar", "id":parseInt($(id).parent().find("td").eq(0).text()), "datos":cant};
	Cambios(datos);
}

function CalculoTotal(){
	var total = 0.0;
	var sbtotal = 0.0;
	//~ console.log("Calculo del Total");
	if ( $(ID_TABLA_ACTIVA + " tbody" ).length > 0 ){
		$(ID_TABLA_ACTIVA + " > tbody > tr" ).each(function(i, elemento){
			sbtotal = sbtotal + parseFloat($(elemento).find("td").eq(DATOS['total']).text().replace(",",".")); 	
			console.log(sbtotal);
		});
	}
	$( SUBTOTAL ).text( (sbtotal.toFixed(2)).replace(".",","));
	for (i=0;i<SBTOTALS.length;i++){
		total = total + parseFloat($( SBTOTALS[i] ).html().replace(",","."));
		//~ console.log(parseFloat($( SBTOTALS[i] ).html()) + "  " + total );
	}
	$( TOTAL ).html(total.toFixed(2).replace(".",","));
	
}

$("#Materiales").change( function(){
	//recalcula cuando se elimina una fila de la tabla
	CalculoTotal();
});

function RecalcularFormularios(ACCION, DIR){
	//*******   Recalcula el numero de formularios	
	
	//~ console.log(ACCION + ": RECALCULANDO FORMULARIOS: " + DIR);
	//~ total = $(DIR + " tbody tr").length;
	//~ console.log("TOTAL DE FILAS: " + total);
	if (ACCION == "ELIMINAR"){
		var i = 0;
		var expreg = /\d{1,2}/g;

		$(DIR + " tbody").find("tr").each(function(){
			$(this).find(":input").each(function(){
				var name = $(this).attr("name").replace(expreg, i);
				var id = $(this).attr("id").replace(expreg, i);
				//~ console.log("NAME: "+ $(this).attr("name")+ " -->" + name + "  ID :" + $(this).attr("id") + " --> " + id ) ;
				$(this).attr("name",name);
				$(this).attr("id",id);
			});
			i++;
		});
	}
	if (ACCION == "AGREGAR") {
		var expreg = /NUM/g;
		var i = $("#id_form-TOTAL_FORMS").val();
		var i = $(DIR + " tbody tr").length-1;
		//~ console.log(i)
		$(DIR + " tbody tr:last").find(":input").each(function(){
			var name = $(this).attr("name").replace(expreg, i);
			var id = $(this).attr("id").replace(expreg, i);
			//~ console.log("NAME: "+ $(this).attr("name")+ " -->" + name + "  ID :" + $(this).attr("id") + " --> " + id ) ;
			$(this).attr("name",name);
			$(this).attr("id",id);	
		});
	}
	$("#id_form-TOTAL_FORMS").val($(DIR + " tbody tr").length);
	
	//~ console.log("Total: " + $("#id_form-TOTAL_FORMS").val());
	//*******************************************
	
}

//~ $("#btnAgregar").click(function () {
function AgregarRegistro(id){
	//~ console.log("Agregando registro");

	var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');
	  
	$TABLE = $(ID_TABLA_ACTIVA);
	//~ console.log("idTABLE: " + idTABLE + " TABLE: " + '#'+$(this).attr("name"));
	
	$clone.attr("class","table-remove");
	$TABLE.append($clone); 
	//~ RecalcularFormularios("AGREGAR", '#' + $(this).attr("name") );
	
	if ( ID_TABLA_ACTIVA === "#Materiales_prd" ){
		//~ console.log("TABLA: " + ID_TABLA_ACTIVA);
		//~ console.log("CELDA: " + ID_TABLA_ACTIVA + " > tr > td.col-sm-4 ");
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
			//~ console.log("Ingrso");
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese el nombre...'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					//~ console.log("VALOR: ingresando");
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
		//~ $("#Materiales > tbody > tr > td:nth-child(3)").attr("contenteditable", true);
		//~ $("#Materiales > tbody > tr > td:nth-child(5)").attr("contenteditable", true);
	}
	if ( ID_TABLA_ACTIVA === "#Insumos_prd" ){
	
		$(ID_TABLA_ACTIVA + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					//~ console.log("VALOR: ingresando");
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TABLA_ACTIVA === "#Otros_costos_prd" ){
		console.log("fffff");

	}
}
//~ });

//~ $("#btnEliminar").click(function(){
function EliminarRegistro(id){
	
	var $idTABLE = $(".seleccionado").parent();
	var DIR = $($idTABLE.parent()).attr("id");
	
	r = $(".seleccionado").find("td").eq(0).text() == "" ? -1 : parseInt($(".seleccionado").find("td").eq(0).text());
	Cambios({"destino":DESTINO, "accion": "eliminar", "id": r, "datos":-1} );
	
	$(".seleccionado").remove();
	$idTABLE.trigger("change");
}
//~ });

//~ $("#Materiales").click(function(){
	//~ console.log("Se realizo accion sobre la tabla Materiales");
	//~ ID_TABLA_ACTIVA = '#Materiales';
//~ });

//~ $("#Insumos_prd").click(function(){

	//~ ID_TABLA_ACTIVA = '#Insumos_prd';
	//~ TBL_LISTA       = 'TablaPartidas';
	//~ DIV_LISTA       = '#lpartidas';
	//~ $CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
	//~ DATOS = {'cant':3, 'cmedida':4, 'total':5};
	//~ TOTAL = '#costo_producto';
	//~ SUBTOTAL = '#total_insumo_prd';
	//~ SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];
	
	
	//~ console.log("Se realizo accion sobre la tabla " + ID_TABLA_ACTIVA);
//~ });

//~ $("#Materiales_prd").click(function(){
	//~ console.log("Se realizo accion sobre la tabla Materiales");
	//~ ID_TABLA_ACTIVA = '#Materiales_prd';
	//~ TBL_LISTA       = 'TablaInsumos';
	//~ DIV_LISTA       = '#linsumos';
	//~ $CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
	//~ DATOS = {'cant':3, 'cmedida':4, 'total':5};
	//~ TOTAL = '#costo_producto';
	//~ SUBTOTAL = '#total_insumo_prd';
	//~ SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];
	
	//~ console.log("Se realizo accion sobre la tabla " + ID_TABLA_ACTIVA);
//~ });

function SeleccionarTabla(id){
	tbl = '#' + $(id).attr("name");
	console.log("Seleccionando Tabla: " + tbl);
	console.log("Configurando : " + tbl);
	
	if ( tbl === "#Insumos_prd"){
		DESTINO = "INSUMOS";
		ID_TABLA_ACTIVA = '#Insumos_prd';
		TBL_LISTA       = 'TablaPartidas';
		DIV_LISTA       = '#lpartidas';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':3, 'cmedida':4, 'total':5, 'cld_listar': 2};
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
		DATOS = {'cant':3, 'cmedida':4, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_materiales_prd';
		SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];		
	}
	
	if ( tbl === "#Otros_costos_prd" ){
		ID_TABLA_ACTIVA = '#Otros-costos_prd';
		TBL_LISTA       = 'TablaInsumos';
		DIV_LISTA       = '#linsumos';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':3, 'cmedida':4, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_materiales_prd';
		SBTOTALS = [ '#total_insumo_prd', '#total_materiales_prd', '#total_otros-costos_prd'];			
	}
}


$("tr[name=regn]").click(function (e) {
	SeleccionarRegistro(this);
});

function SeleccionarRegistro(id){
	var idTABLE = '#'+ $(id).closest("table").attr("id")+" tr";
	
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

  //~ $("#myBtn3").click(function(){
    //~ var winSize = {
      //~ wheight : $(window).height(),
      //~ wwidth : $(window).width()
    //~ };
    //~ console.log(winSize);

    //~ var modSize = {
      //~ mheight : $('#myModal3').height(winSize.wheight),
      //~ mwidth : $('#myModal3').width(winSize.wwidth)
    //~ };
  //~ $('#myModal3').css({
    //~ 'background-color' : '#fff',
    //~ 'opacity': '0.8',
    //~ 'padding-top' :  ((winSize.wheight - (modSize.mheight/2))/2),
    //~ 'padding-left': '10px',

  //~ });
  //~ $('#dialogo').css({
    //~ 'background-color' : '#fff',
    //~ 'top' :  '15%',
    //~ 'left': '0%',
  //~ });


    //~ $("#myModal3").modal({backdrop: "static"});
  //~ });
//});

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

// codigo usado por plano-1.html
/*
var form = document.getElementById("fenviar");
form.addEventListener('submit', function(ev) {
  var xhrObject = new XMLHttpRequest(); 
  var data = new FormData();
  var url = window.location.pathname;
  console.log("Ingreso al submit");
  //prevenimos la acción por defecto del navegador
  ev.preventDefault();
  //creamos un objeto FormData de HTML5 y le pasamos el formulario
  archivos = document.getElementsByClassName("input-ghost");
  console.log(archivos.length);
  narch = archivos.length;

  for (var i = 0; i < narch-1; i++){
    console.log(archivos[i].files[0].name);
    nombre = archivos[i].files[0].name; //"lastModified", "size","type",
    if ( nombre != ""){
      data.append(nombre, archivos[i].files[0]);  
    }
  } 

    xhrObject.open("POST",url,true); 
    xhrObject.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhrObject.setRequestHeader("X-CSRFToken",document.getElementById('csrf_token').value);
    xhrObject.send(data); 
  });
  */
//*********************************
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

