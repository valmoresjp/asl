
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
var $CLD_LISTAR = null;     // almacena el id de la celda donde se requiere listar TBL_LISTA
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
	div 		: null;
	tbl 		: null;
	destino		: null;
	id_tbl_act  : null;
	tbl_lista	: null;
	div_lista	: null;
	cld_lista	: null;
	ref_cld 	: {'cantidad':-1, 'cumedida':-1, 'total':-1, 'cld_listar': -1,'referencia':-1};
	cld_total   : null;
	subtotal 	: null;
	subtotales	: [];
	limpiar:function(){
					div 		: null;
					tbl 		: null;
					destino		: null;
					id_tbl_act  : null;
					tbl_lista	: null;
					div_lista	: null;
					cld_lista	: null;
					ref_cld 	: {'cantidad':-1, 'cumedida':-1, 'total':-1, 'cld_listar': -1,'referencia':-1};
					cld_total   : null;
					subtotal 	: null;
					subtotales	: [];
		
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
		idcumedida :[],
		asignar_cantidad: function(){
							this.$idcant.text(((parseFloat(this.cantidad)).toFixed(2)).toString().replace(".",",") );
							this.total();
							//~ console.log("Cantidad: " +  this.cantidad);
						},
		total : function(){
					var total= 0.0;
					var r = this.idcumedida.entries();
					for ( i=0;i<this.idcumedida.length;i++){
						total = total + parseFloat(this.cantidad)*parseFloat($(this.idcumedida[i]).text().replace(",","."));
						//~ console.log("Total: " + total +  "   " + this.cantidad + "    " + parseFloat($(this.idcumedida[i]).text().replace(",",".")));
					}
					total = total + 0.5;
					total = (this.tipo == 'UMED'? total : total/100);
					this.$idtotal.text((total.toFixed(2)).toString().replace(".",","));
				},
		limpiar:function(){
					this.$idreg ="";
					this.$idtotal="";
					this.$idcant="";
					this.cantidad="1";
					this.tipo="";
					this.idcumedida=[];
				}
};

document.body.addEventListener("keydown", function(event) {
  if (event.code === 'Escape' || event.keyCode === 27) {
    // Aqui la lógica para el caso de Escape ...
    if ( count_esc == 0 ){
		$(DIV_LISTA).css("display","none");		
		$("#Blistar").removeClass("modificando_lista");
		$("#Blistar").remove();
		
		//~ EliminarRegistro($('.seleccionado').attr("id"));
		cotn_esc = 0;
	}

  }
});

function Existentes(id_reg){
	//~ Verifica la existencia del registro que se quiere agregar
	var existe = -1;
	//~ console.log("Registro: " + id_reg+ "  " + ID_TBL_ACT);
	$(ID_TBL_ACT + " > tbody > tr").each(function(i, elemento){
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
				//~ $(".modificando_cant").text($(this).val());
				var a = REGS.find(function(element){ return element.$idreg.attr("id") == $(".modificando_cant").parent().attr("id") });
				if ( !a ){
					//~  el registro no existe y es almacenado para calculos
					// quiere decir que este ya existe en la BD
					
					registros.$idreg   = $($(".modificando_cant").parent())
					registros.idbd     = parseInt(registros.$idreg.find("td").eq(0).html());
					//~ registros.idbd     = registros.$idreg.find("td").eq(0);
					registros.$idtotal = registros.$idreg.find("td").eq(5);
					registros.$idcant  = registros.$idreg.find("td").eq(4);
					registros.tipo     = registros.$idreg.find("td").eq(4) != "%" ? "UMED" : "%" ;
					registros.idcumedida.push( registros.$idreg.find("td").eq(3) );
					registros.cantidad = parseFloat($(this).val().replace(",","."));
					registros.asignar_cantidad();
					registros.accion   = registros.accion == "nuevo" ? 'nuevo' : 'actualizar'
					registros.tabla=DESTINO;
					
					REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
					registros.limpiar();
				}else{
					// el registro no existe en la BD y se esta agregando nuevo
					a.idbd  = parseInt(a.$idreg.find("td").eq(0).html());
					a.cantidad      = parseFloat($(this).val().replace(",","."));
					a.asignar_cantidad();
				}
		
				CalculoTotal();
				$(this).val("");
				$(".modificando_cant").removeClass("modificando_cant");
				$("#MCantidad").hide();
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
	
	if (Existentes(campo[DATOS['cld_listar']-1]) == -1){
		if ( ID_TBL_ACT == "#Insumos_prd" ){
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(1).text(campo[1]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(2).text(campo[2]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(3).text(campo[3]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(4).text(1);
			id = $( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(4);
			registros.idbd = campo[0];
			registros.$idreg   = $(ID_TBL_ACT + ' tbody tr:last')
			registros.$idtotal = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.idcumedida.push( $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(3) );
		}
		if ( ID_TBL_ACT == "#Materiales_prd" ){
			$( $(ID_TBL_ACT + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(4).text(1);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(5).text(campo[4]);
			id = $( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(4);
			registros.idbd = campo[0];
			registros.$idreg   = $(ID_TBL_ACT + ' tbody tr:last')
			registros.$idtotal = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.idcumedida.push( $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(3) );
		}
		if ( ID_TBL_ACT == "#Otros-costos_prd" ){
			$( $(ID_TBL_ACT + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(4).text(1);
			registros.idbd = campo[0];
			registros.$idreg   = $(ID_TBL_ACT + ' tbody tr:last')
			registros.$idtotal = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = campo[4];
	
				if ( registros.tipo  === 'UMED' ){
					registros.idcumedida.push( $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(3) );
				}
				if ( registros.tipo === 'TINS' ){
					registros.idcumedida.push('#total_insumo_prd');
				}
				if ( registros.tipo === 'TMAT' ){
					registros.idcumedida.push('#total_materiales_prd');
				}
				if ( registros.tipo === 'TIMA' ){
					registros.idcumedida.push('#total_insumo_prd');
					registros.idcumedida.push('#total_materiales_prd');
				}
				
			id = $( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(4);
		}
		if ( ID_TBL_ACT == "#Ingrediente_partida" ){
			//~ console.log("----------");
			$( $(ID_TBL_ACT + ' tbody tr:last') ).find("td").eq(0).text(campo[0]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(1).text(campo[1]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(2).text(campo[2]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(3).text(campo[3]);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(4).text(1);
			$( $(ID_TBL_ACT + ' tbody tr:last-child') ).find("td").eq(5).text(1);
			id = $( $(ID_TBL_ACT + ' tbody tr:last-child')).find("td").eq(5);
			registros.idbd = campo[0];
			registros.$idreg   = $(ID_TBL_ACT + ' tbody tr:last')
			registros.$idtotal = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(5);
			registros.$idcant  = $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(4);
			registros.tipo = 'UMED';
			registros.idcumedida.push( $(ID_TBL_ACT + ' tbody tr:last-child').find("td").eq(3) );
			
		}
		$("#Blistar").removeClass("modificando_lista");
		$("#Blistar").remove();
		$( $(DIV_LISTA) ).hide();
		registros.tabla=DESTINO;
		registros.accion="nuevo";
		registros.total();
		REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
		registros.limpiar();
		
		//~ CalculoTotalRegistro(id);
		CalculoTotal();
		SeleccionarRegistro($(".seleccionado"));
		
		//~ console.log("SALIENDO: Seleccionando datos de la lista...");
	}else{
			$("#linsumos").hide();
			alert("El registro que desea agregar ya existe...");
			
	}
}

function CalculoTotal(){
	var total = 0.0;
	var sbtotal = new Object();
	var idtbl ="";
	var valor = 0.0;
	var total = 0.0;
	var ref=null;
	//~ console.log("Calculo del Total");
	TABLAS = ['Insumos_prd', 'Materiales_prd', 'Otros-costos_prd']
	 
	$('.datos  > tbody > tr').each(function(i,elemento){
		if (TABLAS.find(element => element == $(elemento).parent().parent().attr("id") ) ){
			idtbl = $(elemento).parent().parent().attr("id");
			
			//~ sbtotal[idtbl] = sbtotal[idtbl] == undefined ? 0 : sbtotal[idtbl];
			valor  = parseFloat( $(elemento).find("td").eq(DATOS['total']).text().replace(",","."));
			
			console.log($(elemento).find("td:last").text().replace(",","."));
			ref = $(elemento).find("td:last").text().replace(",",".");
			               
			sbtotal[idtbl] = sbtotal[idtbl] == undefined ? 0 : sbtotal[idtbl]
			if ( ref === "UMED" ){
				sbtotal[idtbl] = sbtotal[idtbl] +  valor + 0.5;
			}
			if ( ref === "TINS" ){
				total = total + sbtotal[idtbl]*DATOS['cant']/100;
			}
			if ( ref === "TMAT" ){
				total = total + sbtotal[idtbl];
			}
			if ( ref === "TIMA" ){
				total = total + sbtotal[idtbl];
			}
			$( "#total_" + idtbl ).html(sbtotal[idtbl].toFixed(2).replace(".",","));
			total = total + sbtotal[idtbl];
		}
	});
	sbtotal.total = total.toFixed(2);
	console.log(sbtotal);

	total_prod = total.toFixed(2).replace(".",",");
	$( TOTAL ).html(total_prod);
	
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

$(".datos > tbody > tr").change(function(){
 console.log("Se modifico una celda");
});

function CerrarLista(id){
	$(DIV_LISTA).css("display","none");
}

function AgregarRegistro(id){
	//~ console.log("Agregando registro");

	var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');
	  
	$TABLE = $(ID_TBL_ACT);
	//~ console.log(ID_TBL_ACT);
	//~ console.log("idTABLE: " + idTABLE + " TABLE: " + '#'+$(this).attr("name"));
	
	$clone.attr("class","table-remove");
	$clone.attr("id","reg-"+$(ID_TBL_ACT + '> tbody > tr').length);
	$TABLE.append($clone); 
	//~ RecalcularFormularios("AGREGAR", '#' + $(this).attr("name") );
	
	if ( ID_TBL_ACT === "#Materiales_prd" ){
		
		$(ID_TBL_ACT + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese el nombre...'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					//~ console.log("VALOR: ingresando");
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TBL_ACT === "#Insumos_prd" ){
	
		$(ID_TBL_ACT + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TBL_ACT === "#Otros-costos_prd" ){
		//~ console.log("fffff: " + ID_TBL_ACT);
		$(ID_TBL_ACT + " > tbody > tr > td:nth-child(2)").on("click", function(){
				var input = "<input id='Blistar' type='text' name='Blistar'  onkeyup='Listar(this)' style='width:100%;' placeholder='Ingrese nombre..'>";
				if ( !$(this).hasClass("modificando_lista") ) {
					$(this).addClass("modificando_lista");				
					$(this).append(input);
				}
				$("#Blistar").focus();
					
		});
	}
	if ( ID_TBL_ACT === "#Ingrediente_partida" ){
		//~ console.log("Ingrediente_partida: " + ID_TBL_ACT);
		$(ID_TBL_ACT + " > tbody > tr > td:nth-child(2)").on("click", function(){
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
	var a = REGS.find(function(element){ return element.$idreg.attr("id") == $(".seleccionado").attr("id") });
	console.log(a);
	if (a){
		if (a.accion === "nuevo"){
			a.accion="NOGUARDAR";
		}else{
			a.id = r;
			a.accion="eliminar";
		}
	}else{
		registros.$idreg   = $(".seleccionado");
		registros.idbd     = parseInt(registros.$idreg.attr("id").substr(5,2) );
		//~ registros.idbd     = registros.$idreg.find("td").eq(0);
		registros.$idtotal = registros.$idreg.find("td").eq(5);
		registros.$idcant  = registros.$idreg.find("td").eq(4);
		registros.tipo     = registros.$idreg.find("td").eq(2) != "%" ? "UMED" : "%" ;
		registros.idcumedida.push( registros.$idreg.find("td").eq(3) );
		registros.cantidad = parseFloat(registros.$idcant.val().replace(",","."));
		registros.asignar_cantidad();
		registros.accion   = "eliminar";
		registros.tabla=DESTINO;
					
		REGS.push($.extend( {}, registros ));// copia el objeto dentro de REGS
		registros.limpiar();		
	}
	$(".seleccionado").remove();
	CalculoTotal();
	//~ $idTABLE.trigger("change");
}

function SeleccionarTabla(id){
	//~ tbl = '#' + $(id).attr("name");
	
	//~ console.log("Seleccionando Tabla: " + tbl);
	
	//~ ######################
	
	tbl = $(id).attr("id").subtr(0,tbl.length - 4);
	var a = Conf.find(function(element){ return element.ref === tbl });
	if ( !a ){
		Conf_datos.ref = tbl
		Conf_datos.div = tbl + "_div";
		Conf_datos.tbl = tbl + "_dat";
		Conf_datos.destino = tbl;
		Conf_datos.div_lista = tbl + "_lis";
		Conf_datos.tbl_lista = tbl + "_agr";
		//~ Conf_datos.cld_lista = 
		Conf_datos.cld_ref={'cantidad':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		Conf.push($.extend( {}, Conf_datos ));
		Conf_datos.limpiar();
	}
	ID_TBL_ACT = tbl;
	
	//~ ##############
	
	
	if ( tbl === "#Insumos_prd"){
		
		DESTINO = "INSUMOS";
		ID_TBL_ACT = '#Insumos_prd';
		TBL_LISTA       = 'TablaPartidas';
		DIV_LISTA       = '#lpartidas';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_Insumos_prd';
		SBTOTALS = [ '#total_Insumos_prd', '#total_Materiales_prd', '#total_Otros-costos_prd'];			
	
	}

	
	if ( tbl === "#Materiales_prd" ){
		DESTINO  ="MAQYHERR";
		ID_TBL_ACT = '#Materiales_prd';
		TBL_LISTA       = 'TablaInsumos';
		DIV_LISTA       = '#linsumos';
		$CLD_LISTAR      = $("#Insumos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_Materiales_prd';
		SBTOTALS = [ '#total_Insumos_prd', '#total_Materiales_prd', '#total_Otros-costos_prd'];		
	}
	
	if ( tbl === "#OtrosCostos_prd" ){
		DESTINO  ="CSTSADNLS";
		ID_TBL_ACT = '#Otros-costos_prd';
		TBL_LISTA       = 'TablaCstsAdnls';
		DIV_LISTA       = '#CstsAdnls';
		$CLD_LISTAR      = $("#Otros-costos_prd > tbody > tr > td:nth-child(2)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_producto';
		SUBTOTAL = '#total_Otros-costos_prd';
		SBTOTALS = [ '#total_Insumos_prd', '#total_Materiales_prd', '#total_Otros-costos_prd'];				
	}
	
	if ( tbl === "#Ingrediente_partida" ){
		DESTINO  ="PARTDETLLS";
		ID_TBL_ACT = '#Ingrediente_partida';
		TBL_LISTA       = 'TablaInsumos';
		DIV_LISTA       = '#linsumos';
		$CLD_LISTAR      = $("#Ingrediente_partida > tbody > tr > td:nth-child(3)");
		DATOS = {'cant':4, 'cumedida':3, 'total':5, 'cld_listar': 2};
		TOTAL = '#costo_partida';
		//~ SUBTOTAL = '#total_ingrediente_partida';
		//~ SBTOTALS = [ '#total_ingrediente_partida'];			
	}
}

$("tr[name=regn]").click(function (e) {
	SeleccionarRegistro(this);
});

function SeleccionarRegistro(id){
	var idTABLE = '#'+ $(id).closest("table").attr("id")+" tr";
	
	$(ID_TBL_ACT + " > tbody > tr").each(function(i,e){
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






