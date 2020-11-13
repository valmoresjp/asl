
//var $TABLE = $('#table');
var $CLON = $('#TablaClon');
var $GUARDAR = $('#export-btn');
var $EXPORT = $('#datos');
var $TABLE = null;
var c_tmp=1;
var SELE="tomato", DSEL="white", ADV="yellow";
var ObjDatos=[];//{'accion':"", "id":-1, "datos":[-1]}
var ID_TBL_ACT=null;  // almacena el id de la tabla activa, es decir en uso
var VALOR_TMP = null;
var DATOS_TMP = null;
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
	//~ putilidad	: null,
	//~ utilidad	: null,
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
					//~ this.putilidad	= null;
					//~ this.utilidad	= null;
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
		//~ utilidades: [],
		asignar_cantidad: function(){
							this.$idcant.text(((parseFloat(this.cantidad)).toFixed(2)).toString().replace(".",",") );
							this.total();
							//~ console.log("Cantidad: " +  this.cantidad);
						},
		total : function(){
					var total= 0.0;
					var porcentaje = 0.0;
					var utilidad   = 0.0;
					//~ console.log(this.$idcumedida.html());
					total = parseFloat(this.cantidad)*parseFloat(this.$idcumedida.html().replace(",","."));
					//~ porcentaje = (parseFloat(this.$idputil.val()))/100;
					//~ utilidad   = porcentaje*total;
					//~ total = total + 0.5;
					this.$idtotal.text((total.toFixed(2)).toString().replace(".",","));
					//~ this.$idutilidad.text((utilidad.toFixed(2)).toString().replace(".",","));
					//~ console.log(this.cantidad + "  "+ $(this.$idcumedida).text() + " = " + total);
				},
		limpiar:function(){
					this.$idreg ="";
					this.$idtotal="";
					this.$idcant="";
					//~ this.$idputil="";
					//~ this.$idutilidad="";
					this.cantidad="1";
					this.tipo="";
					this.$idcumedida=null;
					//~ this.utilidades=	[];

				}
};

$("#vender_1").click(function(evento){
	
	var estado = true;
	var mensaje=""
	var cantidad     = parseFloat($("#id_cant").val());
	var costo_unidad = parseFloat($("#id_costo").val());
	var costo_total  = cantidad*costo_unidad;
	var fhentr       = $("#id_fhentr").val();
	var direcc       = $("#id_direc").val();
	var cdirec       = $("#id_centr").val();
	var cliente      = $("#id_idclie").val();
	
	//~ $("#id_estado").val("en proceso");
	
	if ( cliente == 0 ){
		mensaje = mensaje + "Debe seleccionar un cliente.. \n";
		$("#id_idclie").addClass("borde_error");
		estado = false;
	}
	if ( fhentr == "" ){
		mensaje = mensaje + "Debe agregar la fecha y hora de entrega.. \n";
		$("#id_fhentr").addClass("borde_error");
		estado = false;
	}else{
		var actual = new Date();
		//~ 01-11-2020 10:00
		var ayo = parseInt(fhentr.substr(6,9));
		var mes = parseInt(fhentr.substr(3,4))-1;
		var dia = parseInt(fhentr.substr(0,2));
		var hora= parseInt(fhentr.substr(11,12));
		var min = parseInt(fhentr.substr(14,15));
		var entrega = new Date(ayo,mes,dia,hora,min);
		console.log(actual, "    ", entrega)
		console.log(Date.parse(actual), "    ", Date.parse(entrega))
		if ( Date.parse(actual) >= Date.parse(entrega) ){
			mensaje = mensaje + "La fecha y hora de entrega debe ser mayor a la fecha actual... \n";
			$("#id_fhentr").addClass("borde_error");
			estado = false;
		}else{
			console.log(fhentr)
			var a  =  fhentr.replace("T","-").split("-");
			console.log(a)
			$("#id_fhentr").removeClass("borde_error");
			fhentr  = a[2]+"-"+ a[1]+"-"+a[0] +" "+a[3]; 
		}
	}
	if (estado){
		$("#cantidad").html(cantidad);
		$("#costo_total").html(costo_total);
		$('#direccion_entrega').html($('#id_direc').val());
		$('#fecha_entrega').html(fhentr);
		$('#costo_entrega').html($('#id_centr').val());
	}else{
		alert("Revise los campos marcados, pues tienen los siguientes errores: \n\n" + mensaje);
		evento.stopPropagation();
	}
});
$("#vender_3").click(function(){
	
		$('#vender_2').click();
});

$(document).ready(function() {
	
	if ( $("div[name='Detallar_prd']").length == 1 ){
		CalculoTotal();
	}
	if ( $("div[name='Inicio']").length == 1 ){
		$('#entregas > tr').each(function(){ 
			if ( parseInt($(this).find('td').eq(4).html()) <= 5 ){
				$(this).addClass("marca");
			}
			
		});
	}
});

document.body.addEventListener("keydown", function(event) {
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
  if (event.code === 'Escape' || event.keyCode === 27) {
    // Aqui la lógica para el caso de Escape ...
    if ( count_esc == 0 ){
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

function Registrar(id){
	
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
							
		var tmp = [];
		$("td[id$='_por']").each(function(){
			 tmp[$(this).attr("id")]=$(this).html();
		});
		tmp=null;
		registros.utilidades.push(tmp);
							
		registros.cantidad = parseFloat($(this).val().replace(",","."));
		registros.asignar_cantidad();
		registros.accion   = registros.accion == "nuevo" ? 'nuevo' : 'actualizar'
		registros.tabla=tbl_act.destino;
							
		REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
		registros.limpiar();
	}else{
							// el registro no existe en la BD y se esta agregando nuevo
		a.idbd  = parseInt(idtr.find("td").eq(0).html());
		a.cantidad      = parseFloat($(this).val().replace(",","."));
		a.asignar_cantidad();
	}	
	
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

			if (e.which == 13){
				
				if (ID_TBL_ACT === "Utilidades" ){
					$(this).parent().html($(this).val().replace(".",","));
					CalculoTotal();
					if(REGS.length == 0){
						registros.accion="TOTALIZAR";
						REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
						registros.limpiar();
					}
				}else{
					var a = REGS.find(function(element){ return element.$idreg.attr("id") == $(".modificando_cant").parent().attr("id") });
					if ( !a ){

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
						a.idbd  = parseInt(idtr.find("td").eq(0).html());
						a.cantidad      = parseFloat($(this).val().replace(",","."));
						a.asignar_cantidad();
					}
					//~ Registrar($(".modificando_cant"));
					CalculoTotal();
				
					
				}
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
	var campo = [];
	var id;
	var tbl_act = Conf.find(function(element){ return element.ref === ID_TBL_ACT });
	
	$(idreg).find("td").each(function(i,e){
		campo.push($(e).html());
	});
	if (Existentes(campo[tbl_act.cld_ref['cld_listar']-1]) == -1){
			
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(0).text(campo[0]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(1).text(campo[1]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(2).text(campo[2]);
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(3).text(campo[3]);		
			
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
		if ( tbl_act.tbl == "Servicios_dat" ){
			$('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4).text(1);
			registros.idbd = campo[0];
			registros.$idreg   = $('#'+tbl_act.tbl + ' tbody tr:last')
			registros.$idtotal = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = campo[4];
			registros.$idcumedida =  $('#'+tbl_act.tbl +' tbody tr:last-child').find("td").eq(3) ;
				
			id = $('#'+tbl_act.tbl + ' tbody tr:last-child').find("td").eq(4);
		}
		if ( tbl_act.tbl == "Personal_dat" ){
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
	sbtotal={};
	$("p[id$='_tot']").each(function(i,elemento){
		$(elemento).html("0,0");
	});
	
	$('.datos  > tbody > tr').each(function(i,elemento){

			idtbl = $(elemento).parent().parent().attr("id")
			idtbl = idtbl.substr(0,idtbl.length - 4);
			
			valor  = parseFloat( $(elemento).find("td").eq(5).text().replace(",","."));
			sbtotal[idtbl] = sbtotal[idtbl] == undefined ? 0 : sbtotal[idtbl]
			sbtotal[idtbl] = sbtotal[idtbl] +  valor;
			$( "#" + idtbl + "_tot" ).html(sbtotal[idtbl].toFixed(2).replace(".",","));
	});
	Utilidad();
	total =0.0;
	$("p[id$='_tot']").each(function(i,elemento){
		total = total + parseFloat( $(elemento).html().replace(",",".") );
	});
	$( "#costo_total" ).text(total.toFixed(2).toString().replace(".",","));

}

$("#Materiales").change( function(){
	//recalcula cuando se elimina una fila de la tabla
	CalculoTotal();
});
 
$("#patron").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#Listado-body tr").filter(function() {
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
	if ( tbl_act.tbl === "Servicios_dat" ){
	
		$('#' + tbl_act.tbl + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
		});
	}
	if ( tbl_act.tbl === "Personal_dat" ){
	
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

function Utilidad(){
	var total=0.0;
	$(".total").each(function(){
		var st = parseFloat( $(this).html().replace(",","."));
		var por = parseFloat( $("#"+$(this).attr("name") +"_por").text().replace(",","."));
		var utilidad = (st*por)/100;
		
		$("#"+$(this).attr("name") +"_util").html(utilidad.toFixed(2).toString().replace(".",","));
		total = total + utilidad;
	});
		$("#Utilidades_tot").html(total.toFixed(2).toString().replace(".",","));
	
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
}

function SeleccionarTabla(id){
		
	tbl = $(id).attr("id").substr(0,$(id).attr("id").length - 4);
	var a = Conf.find(function(element){ return element.ref === tbl });
	if ( !a ){
		Conf_datos.ref = tbl
		Conf_datos.div = tbl + "_div";
		Conf_datos.tbl = tbl + "_dat";
		Conf_datos.destino = tbl;
		Conf_datos.div_lista = tbl + "_lis";
		Conf_datos.tbl_lista = tbl + "_agr";
		Conf_datos.putilidad = tbl + "_por";
		Conf_datos.utilidad = tbl + "_uti";
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
	
	$('#'+tbl_act.tbl + " > tbody > tr").each(function(i,e){
		if( id != e ){
			if ( $(e).hasClass("seleccionado") ){
				$(e).css("background-color",DSEL);
				$(e).removeClass("seleccionado");
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
			if (REGS[i].accion === "nuevo" || REGS[i].accion === "actualizar" || REGS[i].accion === "eliminar"){
				ObjDatos.push({ "destino" :REGS[i].tabla,
								 "accion" :REGS[i].accion,
								     "id" :REGS[i].idbd,
								   "datos":REGS[i].cantidad
 							});
			}
		}

		total = { 
			'costo' :$('#costo_total').length  == 0 ? -1 : $('#costo_total' ).html().replace(",","."),
			'insm'  :$('#Insumos_tot').length  == 0 ? -1 : $('#Insumos_tot' ).html().replace(",","."),
			'part'  :$('#Partidas_tot').length == 0 ? -1 : $('#Partidas_tot' ).html().replace(",","."),
			'pers'  :$('#Personal_tot').length == 0 ? -1 : $('#Personal_tot' ).html().replace(",","."),
			'mate'  :$('#Materiales_tot').length == 0? -1: $('#Materiales_tot' ).html().replace(",","."),
			'serv'  :$('#Servicios_tot').length == 0? -1: $('#Servicios_tot' ).html().replace(",","."),
			'utlds' :$('#Utilidades_tot').length == 0? -1: $('#Utilidades_tot' ).html().replace(",","."),
			'pinsm' :$('#Insumos_por').length == 0? -1:$('#Insumos_por').html().replace(",","."),
			'pmate' :$('#Materiales_por').length == 0? -1:$('#Materiales_por').html().replace(",","."),
			'ppers':$('#Personal_por').length == 0? -1: $('#Personal_por').html().replace(",","."),
			'pserv' :$('#Servicios_por').length == 0? -1: $('#Servicios_por').html().replace(",","."),
			//~ 'ptran' :$('#Servicios_por').length == 0? -1: $('#Transporte_por').html().replace(",","."),
			//~ 'pimpr' :$('#Servicios_por').length == 0? -1: $('#IMprevisto_por').html().replace(",",".")
		}
		ObjDatos.push({ "destino":"TOTALIZAR","accion":"actualizar", "id":-1, "datos":total });
		
		$("#ObjDatos").val(JSON.stringify(ObjDatos));
			
		var winSize = {
		  wheight : $(window).height(),
		  wwidth : $(window).width()
		};
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

