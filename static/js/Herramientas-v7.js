
//var $TABLE = $('#table');
var $CLON = $('#TablaClon');
var $GUARDAR = $('#export-btn');
var $EXPORT = $('#datos');
var $TABLE = null;
var c_tmp=1;
var SELE="tomato", DSEL="white", ADV="yellow";
var ObjDatos=[];//{'accion':"", "id":-1, "datos":[-1]}
var ID_TBL_ACT=null;  // almacena el id de la tabla activa, es decir en uso
var TBL_LISTA = null;      // almacena el id de la tabla para listar
var DIV_LISTA = null;      // almacena el id del div que contiene TBL_LISTA
var VALOR_TMP = null;
var DATOS = {'cant':-1, 'cumedida':-1, 'total':-1}
var TOTAL = null; // almacena el id de la celda que muestra el total
var SUBTOTAL = null //almacena el id de la celda que mantiene el subtotal
var SBTOTALS = [];
var count_esc = 0;
var REF =[]; // almacena las celdas de referencia para calculo que sean expresados en porcentaje
var REGS=[]; // almacena todos los objetos que se agregan
var Conf = [];
var Conf_datos = {
	div 		: null,
	ref 		: null,
	tbl 		: null,
	destino		: null,
	id_tbl_act  : null,
	tbl_lista	: null,
	div_lista	: null,
	cld_lista	: null,
	cld_ref 	: {'cantidad':-1, 'cumedida':-1, 'total':-1, 'cld_listar': -1,'referencia':-1},
	total   : null,
	subtotal 	: null,
	subtotales	: [],
	limpiar:function(){
					this.div 		= null;
					this.ref 		= null;
					this.tbl 		= null;
					this.destino		= null;
					this.id_tbl_act  = null;
					this.tbl_lista	= null;
					this.div_lista	= null;
					this.cld_lista	= null;
					this.cld_ref 	= {'cantidad':-1, 'cumedida':-1, 'total':-1, 'cld_listar': -1,'referencia':-1};
					this.total   = null;
					this.subtotal 	= null;
					this.subtotales	= [];
	}
};

var registros = {
		idbd: -1,
		$idreg :"",
		$idtotal:"",
		$idcant:"",
		cantidad:"1",
		tipo:"",
		accion:"",
		tabla:"",
		$idcumedida :"",
		asignar_cantidad: function(){
							this.$idcant.text(((parseFloat(this.cantidad)).toFixed(2)).toString().replace(".",",") );
							this.total();
							//~ console.log("Cantidad: " +  this.cantidad);
						},
		total : function(){
					var total= 0.0;
					//~ console.log(this.$idcumedida.html());
					total = parseFloat(this.cantidad)*parseFloat(this.$idcumedida.html().replace(",","."));
					//~ total = total + 0.5;
					this.$idtotal.text((total.toFixed(2)).toString().replace(".",","));
					//~ console.log(this.cantidad + "  "+ $(this.$idcumedida).text() + " = " + total);
				},
		limpiar:function(){
					this.$idreg ="";
					this.$idtotal="";
					this.$idcant="";
					this.cantidad="1";
					this.tipo="";
					this.$idcumedida;
				}
};

document.body.addEventListener("keydown", function(event) {
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
  if (event.code === 'Escape' || event.keyCode === 27) {
    // Aqui la lógica para el caso de Escape ...
    if ( count_esc == 0 ){
		//~ console.log("escapando  " + '#'+tbl_act.div_lista);
		$('#'+tbl_act.div_lista).css("display","none");		
		$("#Blistar").parent().removeClass("modificando_lista");
		$("#Blistar").remove();
	}

  }
});

function Existentes(id_reg){
	//~ Verifica la existencia del registro que se quiere agregar
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	var existe = -1;
	//~ console.log("Registro: " + id_reg + "  " + '#'+tbl_act.tbl);
	$('#'+tbl_act.tbl + " > tbody > tr").each(function(i, elemento){
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
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	
  filter = patron.toUpperCase(); //input.value.toUpperCase();
  table = document.getElementById(tbl_act.tbl_lista);
  tr = table.getElementsByTagName("tr");
  // Filtra la tabla de acuerdo al patron ingresado
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[tbl_act.cld_ref['cld_listar']-1];
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
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });

	pos.ancho = $(id).width();
	pos.alto  = $(id).height();
	pos.x     = window.scrollY + id.getBoundingClientRect().top  + pos.alto + 10;
	pos.y     = window.scrollX + id.getBoundingClientRect().left;
	$('#'+tbl_act.div_lista).offset({top:pos.x,left:pos.y});	
	FiltrarInsumos($(id).val());
	$('#'+tbl_act.div_lista).show();
}

function ModificarCantidad(id){
    
    //~ var pos = {};
	var rect = $(id).position();
	var input = "<input id='MCantidad' type='text' name='MCantidad'  style='width:100%;' text-align:right; placeholder='Ingrese la cantidad..'>";
	var VALOR_TMP = $(id).html();
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	var idtd=$(id);
	var idtr=$(id).parent();
	
	if ( !$(id).hasClass("modificando_cant") ) {

		$(id).addClass("modificando_cant");
		$(id).text("");	
		$(id).append(input);
		$("#MCantidad").val(VALOR_TMP);
		
		$("#MCantidad").keyup(function(e){
			//~ console.log(e.which);

			if (e.which == 13){
				var a = REGS.find(function(element){ return element.$idreg.attr("id") == $(".modificando_cant").parent().attr("id") });

				if ( !a ){
					//~  el registro no existe y es almacenado para calculos
					// quiere decir que este ya existe en la BD
					
					registros.$idreg   = $($(".modificando_cant").parent())
					registros.idbd     = parseInt(registros.$idreg.find("td").eq(0).html());
					registros.$idtotal = registros.$idreg.find("td").eq(5);
					registros.$idcant  = registros.$idreg.find("td").eq(4);
					registros.tipo     = registros.$idreg.find("td").eq(4) != "%" ? "UMED" : "%" ;
					registros.$idcumedida = registros.$idreg.find("td").eq(3);
					
					registros.cantidad = parseFloat($(this).val().replace(",","."));
					registros.asignar_cantidad();
					registros.accion   = registros.accion == "nuevo" ? 'nuevo' : 'actualizar'
					registros.tabla=tbl_act.destino;
					
					REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
					registros.limpiar();
				}else{
					//~ console.log("Registro existe");
					// el registro no existe en la BD y se esta agregando nuevo
					a.idbd  = parseInt(idtr.find("td").eq(0).html());
					a.cantidad      = parseFloat($(this).val().replace(",","."));
					a.asignar_cantidad();
				}
		
				CalculoTotal();
				
				$("#MCantidad").remove();
				$(id).removeClass("modificando_cant") ;
			}
			if (e.which == 27){
				$(id).text(VALOR_TMP);
				$("#MCantidad").val("");
				$(id).removeClass("modificando_cant");
				$("#MCantidad").remove();
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
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	
	$(idreg).find("td").each(function(i,e){
		campo.push($(e).html());
	});
	//~ console.log(campo);
	//~ console.log("Entro:"+'#'+tbl_act.tbl);
	if (Existentes(campo[tbl_act.cld_ref['cld_listar']-1]) == -1){
			
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(0).text(campo[0]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(1).text(campo[1]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(2).text(campo[2]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(3).text(campo[3]);		
			//~ var a = REGS.find(function(element){ return element.$idreg.attr("id") == $('#'+tbl_act.tbl+ ' tbody tr:last').attr("id") });
			
		if ( tbl_act.tbl == "Insumos_dat" ){

			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			id = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(4);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl + ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.$idcumedida =  $('#'+tbl_act.tbl +' tbody tr:last-child').find("td").eq(3) ;
		}
		if ( tbl_act.tbl == "Materiales_dat" ){
			
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5).text(campo[4]);
			id = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl + ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.$idcumedida =  $('#'+tbl_act.tbl +' tbody tr:last-child').find("td").eq(3) ;
		}
		if ( tbl_act.tbl == "CostosAdicionales_dat" ){
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl + ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = campo[4];
			registros.$idcumedida =  $('#'+tbl_act.tbl +' tbody tr:last-child').find("td").eq(3) ;
				
			id = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
		}
		if ( tbl_act.tbl == "Partidas_dat" ){
			$( '#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			$( '#'+tbl_act.tbl+ ' tbody tr:last-child').find("td").eq(5).text(campo[3]);
			id = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl+ ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl+ ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl+ ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.$idcumedida =  $('#'+tbl_act.tbl +' tbody tr:last-child').find("td").eq(3) ;
			
		}
		if ( tbl_act.tbl == "Utilidades_dat" ){
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			id = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl + ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = campo[4];
			registros.$idcumedida =  $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(3);
		}
		$("#Blistar").parent().removeClass("modificando_lista");
		$("#Blistar").remove();
		$( $('#'+tbl_act.div_lista) ).hide();
		registros.tabla=tbl_act.destino;
		registros.accion="nuevo";
		registros.total();
		REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
		registros.limpiar();
		
		CalculoTotal();
		SeleccionarRegistro($(".seleccionado"));
		
	}else{
			$("#linsumos").hide();
			alert("El registro que desea agregar ya existe...");
	}
}

function CalculoTotal(){
	var total = 0.0;
	var sbtotal = new Object();
	var idtbl ="";
	var tipo="";
	var valor = 0.0;
	var total = 0.0;
	var ref=null;
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	TABLAS = ['Insumos_prd', 'Materiales_prd', 'Otros-costos_prd']
	sbtotal={};
	$("p[id$='_tot']").each(function(i,elemento){
		$(elemento).html("0.0");
	});
	
	$('.datos  > tbody > tr').each(function(i,elemento){

			idtbl = $(elemento).parent().parent().attr("id")
			idtbl = idtbl.substr(0,idtbl.length - 4);
			
			valor  = parseFloat( $(elemento).find("td").eq(5).text().replace(",","."));
			sbtotal[idtbl] = sbtotal[idtbl] == undefined ? 0 : sbtotal[idtbl]
			sbtotal[idtbl] = sbtotal[idtbl] +  valor;
			$( "#" + idtbl + "_tot" ).html(sbtotal[idtbl].toFixed(2).replace(".",","));
	});

	total =0.0;
	sbtotal.Utilidades = 0.0;
	for ( i in sbtotal){
		total = total + sbtotal[i];
	}
	sbtotal.total = total;
	//~ sbtotal.total = total;
	
	$('#Utilidades_dat  > tbody > tr').each(function(i,elemento){
		//~ console.log($(elemento).find('td').eq(1).html());
		if( $(elemento).find('td').eq(1).html().toUpperCase() == "UTILIDADES" ){
			porcentaje = parseFloat( $(elemento).find('td').eq(4).html().replace(",",".") );
			sbtotal.Utilidades = (porcentaje*sbtotal.total)/100;
			//~ console.log(porcentaje + "   " + sbtotal.total);
		}
	});
	sbtotal.total = (sbtotal.total + sbtotal.Utilidades).toFixed(2);
	sbtotal.Utilidades = sbtotal.Utilidades.toFixed(2);
	//~ console.log(sbtotal);
	//~ Utilidades_tot
	//~ console.log(sbtotal.total);
	$( "#costo_total" ).text(sbtotal.total.replace(".",","));
	$('#Utilidades_dat  > tbody > tr').find("td").eq(5).html(sbtotal.Utilidades.toString().replace(".",","));
	$( "#Utilidades_tot" ).text(sbtotal.Utilidades.toString().replace(".",","));
	
}

$("#Materiales").change( function(){
	//recalcula cuando se elimina una fila de la tabla
	CalculoTotal();
});
 
$("#patron").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
    $("#Listado-body tr").filter(function() {
    //~ console.log( "#" + tbl_act.tbl_filtrar );
    //~ $("#" +tbl_act.tbl_filtrar).filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

function CerrarLista(id){
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	$(tbl_act.div_lista).css("display","none");
}

function AgregarRegistro(id){
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');
	  
	idreg = tbl_act.tbl.substr(0,3) +"-"+$('#'+tbl_act.tbl + '> tbody > tr').length;
	$clone.attr("class","table-remove");
	$clone.attr("id",idreg);
	$('#'+tbl_act.tbl).append($clone);
	//~ console.log(tbl_act.tbl);
	if ( tbl_act.tbl === "Materiales_dat" ){
		
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese el nombre...'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
		});
	}
	if ( tbl_act.tbl === "Insumos_dat" ){
	
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( tbl_act.tbl === "CostosAdicionales_dat" ){
	
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
		});
	}
	if ( tbl_act.tbl === "Partidas_dat" ){
		//~ console.log("Ingrediente_partida: " + ID_TBL_ACT);
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( tbl_act.tbl === "Utilidades_dat" ){
		//~ console.log("Ingrediente_partida: " + ID_TBL_ACT);
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
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
	
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	
	r = $(".seleccionado").find("td").eq(0).text() == "" ? -1 : parseInt($(".seleccionado").find("td").eq(0).text());
	var a = REGS.find(function(element){ return element.$idreg.attr("id") == $(".seleccionado").attr("id") });

	if (a){
		if (a.accion === "nuevo"){
			a.accion="NOGUARDAR";
			a.$idreg = null;
			for ( i=0;i<REGS.length;i++ ){
				if (REGS[i].$idreg == null ){
					REGS.splice(i,1);
				}
			}
		}else{
			a.id = r;
			a.accion="eliminar";
		}
	}else{
		registros.$idreg   = $(".seleccionado");
		registros.idbd     = parseInt(registros.$idreg.attr("id").substr(5,4) );
		//~ registros.idbd     = registros.$idreg.find("td").eq(0);
		registros.$idtotal = registros.$idreg.find("td").eq(5);
		registros.$idcant  = registros.$idreg.find("td").eq(4);
		registros.tipo     = registros.$idreg.find("td").eq(2) != "%" ? "UMED" : "%" ;
		registros.$idcumedida = registros.$idreg.find("td").eq(3);
		registros.cantidad = parseFloat(registros.$idcant.val().replace(",","."));
		registros.asignar_cantidad();
		registros.accion   = "eliminar";
		registros.tabla=tbl_act.destino;
					
		REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
		registros.limpiar();		
	}
	$(".seleccionado").remove();
	CalculoTotal();
	//~ $idTABLE.trigger("change");
}

function SeleccionarTabla(id){
	//~ tbl = '#' + $(id).attr("name");
		
	tbl = $(id).attr("id").substr(0,$(id).attr("id").length - 4);
	//~ console.log("TABLA SELECCIONADA: " + tbl);
	var a = Conf.find(function(element){ return element.ref === tbl });
	if ( !a ){
		Conf_datos.ref = tbl
		Conf_datos.div = tbl + "_div";
		Conf_datos.tbl = tbl + "_dat";
		Conf_datos.destino = tbl;
		Conf_datos.div_lista = tbl + "_lis";
		Conf_datos.tbl_lista = tbl + "_agr";
		//~ Conf_datos.tbl_filtrar = tbl + "_filtrar";
		Conf_datos.total = tbl + "_tot"; 
		Conf_datos.cld_ref={'cantidad':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		Conf.push($.extend( {}, Conf_datos ));
		Conf_datos.limpiar();
	}
	ID_TBL_ACT = tbl;
	
}

$("tr[name=regn]").click(function (e) {
	SeleccionarRegistro(this);
});

function SeleccionarRegistro(id){
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	//~ var idTABLE = '#'+ $(id).closest("table").attr("id")+" tr";
	
	$('#'+tbl_act.tbl + " > tbody > tr").each(function(i,e){
		if( id != e ){
			if ( $(e).hasClass("seleccionado") ){
				$(e).css("background-color",DSEL);
				$(e).removeClass("seleccionado");
				//~ $(e).removeClass("modificando_lista");
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

	if ( REGS.length == 0 ){
			alert("No hay Datos para almacenar");
	}else{
		for (i=0; i<REGS.length; i++){
			//~ console.log(REGS[i]);
			//~ console.log(REGS[i].accion);
			if (REGS[i].accion === "nuevo" || REGS[i].accion === "actualizar" || REGS[i].accion === "eliminar"){
				ObjDatos.push({ "destino" :REGS[i].tabla,
								 "accion" :REGS[i].accion,
								  "id"    :REGS[i].idbd,
								   "datos":REGS[i].cantidad
 							});
			}
		}
		ObjDatos.push({ "destino":"TOTALIZAR","accion":"actualizar", "id":-1, "datos":$( '#costo_total' ).html().replace(",",".")});
		
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






