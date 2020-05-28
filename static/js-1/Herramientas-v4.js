
//var $TABLE = $('#table');
var $CLON = $('#TablaClon');
var $BTN = $('#export-btn');
var $EXPORT = $('#datos');
var $TABLE = null;
var c_tmp=1;
var SELE="tomato", DSEL="white";

function FiltrarInsumos(patron="") {

  var input, filter, table, tr, td, i, txtValue;

  filter = patron.toUpperCase(); //input.value.toUpperCase();
  table = document.getElementById("TablaInsumos");
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

$('tr:even td:eq(2)').keyup(function(){
	// Captura la modificacion de la celda, en este caso la segunda celda de la fila
	// es la que interesa
    var pos = {};
	var rect = $(this).position();
	
	pos.ancho = $(this).width();
	pos.alto  = $(this).height();
	pos.x     = window.scrollY + this.getBoundingClientRect().top  + pos.alto + 10;
	pos.y     = window.scrollX + this.getBoundingClientRect().left;
	$("#linsumos").offset({top:pos.x,left:pos.y});	
	FiltrarInsumos($(this).text());
	$("#linsumos").show();

    //~ console.log(pos);
    //~ console.log(rect);
});

$('#TablaInsumos tbody tr').click(function(){
	
	id        = $(this).find("td").eq(0).text();
	codigo    = $(this).find("td").eq(1).text();
	desc      = $(this).find("td").eq(2).text();
	umedida   = $(this).find("td").eq(3).text(); //uniadd de medida
	cant      = $(this).find("td").eq(4).text().replace(",",".")	; //cantidad
	cmedida   = $(this).find("td").eq(5).text().replace(",",".");//costo maximo	por unidad de medida
	cmin      = $(this).find("td").eq(6).text(); //costo minimo
	cprom     = $(this).find("td").eq(7).text(); //costo promedio
	cmax      = $(this).find("td").eq(8).text(); //costo maximo		
	
	ctotal = (cant*cmedida).toFixed(2).replace(".",",");
	$('#Materiales tbody tr:last-child').find("td").eq(0).text(id);
	$('#Materiales tbody tr:last-child').find("td").eq(1).text(codigo);
	$('#Materiales tbody tr:last-child').find("td").eq(2).text(desc);
	$('#Materiales tbody tr:last-child').find("td").eq(2).attr("contenteditable", false	);
	$('#Materiales tbody tr:last-child').find("td").eq(3).text(umedida);
	$('#Materiales tbody tr:last-child').find("td").eq(4).text(cant.replace(".",","));
	$('#Materiales tbody tr:last-child').find("td").eq(5).text(cmedida.replace(".",","));
	$('#Materiales tbody tr:last-child').find("td").eq(6).text(ctotal);
	$("#linsumos").hide();
	CalculoPartida()
	SeleccionarRegistro($(".seleccionado"));
});

$("tr:even td:eq(4)").keypress(function(e){
	var cant, cmax, total_u; //, total;
	
	console.log("Keypress...modificando cantidad");	
	if(e.which == 13) {
		e.preventDefault();
		cant = parseFloat($(this).text().replace(",","."));
		cmedida = parseFloat($(this).parent().find("td").eq(5).text().replace(",",".")); //costo maximo por unidad de medida	
		total_u = (cant*cmedida).toFixed(2);
		$(this).parent().find("td").eq(6).text(total_u.replace(".",",") );
		CalculoPartida()

		this.blur();
    }

});

function CalculoPartida(){
	var total=0.0;
	
	if ( $("#Materiales tbody").length > 0 ){
		$("#Materiales > tbody > tr").each(function(i, elemento){
			total = total + parseFloat($(elemento).find("td").eq(6).text().replace(",",".")); 	
			console.log(total);
		});
	}

	$("#total_partida").text((total.toFixed(2)).replace(".",","));
}

$("#Materiales").change( function(){
	//recalcula cuando se elimina una fila de la tabla
	CalculoPartida();
});


$("#btnAgregar").click(function () {
	var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');
	var idTABLE = '#'+$(this).attr("name") + " tbody tr";
	  
	$TABLE = $('#'+$(this).attr("name"));
	//~ console.log("idTABLE: " + idTABLE + " TABLE: " + '#'+$(this).attr("name"));
	
	$clone.attr("class","table-remove");

	$TABLE.append($clone); 
    //~ var a=1;
    //~ $(idTABLE).each( function(a){
      //~ a=a+1;
      //~ $(this).find("td").eq(1).text(a);
    //~ });

    $("#Materiales > tbody > tr > td:nth-child(3)").attr("contenteditable", true);
    $("#Materiales > tbody > tr > td:nth-child(5)").attr("contenteditable", true);
});

$("#btnEliminar").click(function(){
	var $idTABLE = $(".seleccionado").parent();
	
	
	$(".seleccionado").remove();
	$idTABLE.trigger("change");
	var a = 0;
	//~ $idTABLE.find("tr").each( function(a){
		//~ $(this).find("td").eq(1).text(++a);
		//~ a=a+1;
	//~ });
});

$("tr[name=regn]").click(function (e) {
	SeleccionarRegistro(this);
});

function SeleccionarRegistro(id){
	var idTABLE = '#'+ $(id).closest("table").attr("id")+" tr";
	
	console.log("Selecionar");
	if ( $(id).hasClass("seleccionado") ) {
		$(id).css("background-color",DSEL);
		$(id).removeClass("seleccionado");
	}else {
		$(id).css("background-color",SELE);
		$(id).addClass("seleccionado");
	}	
}

$BTN.click(function () {
// etraen los datos de todas las tablas existentes  en la pagina
// deberia ser    $("#registros").val(ExtraerTabla("#Materiales") + ExtraerTabla("#otra tablas"));
	//~ $("#registros").val(ExtraerTabla("#Materiales"));
	
 
    var data = JSON.parse(ExtraerTabla("#Materiales"));
	var codp = $('#codp').text()
	for(i=0; i<data.length; i++){
		idcodp = 'id_form-'+ i.toString() + '-codp';
		console.log(idcodp);
		$('#id_form-'+ i.toString() + '-codp').val(codp);
		$('#id_form-'+ i.toString() + '-codi').val(data[i]['id']);
		$('#id_form-'+ i.toString() + '-cant').val(parseFloat(data[i]['cantidad'].replace(",",".")));
	}
	console.log(data[0]);
    
  
	$("#EnviarDatos").click();
});

  $("#myBtn3").click(function(){
    var winSize = {
      wheight : $(window).height(),
      wwidth : $(window).width()
    };
   // console.log(winSize);

    var modSize = {
      mheight : $('#myModal3').height(winSize.wheight),
      mwidth : $('#myModal3').width(winSize.wwidth)
    };
  $('#myModal3').css({
    'background-color' : '#fff',
    'opacity': '0.8',
    'padding-top' :  ((winSize.wheight - (modSize.mheight/2))/2),
    'padding-left': '10px',

  });
  $('#dialogo').css({
    'background-color' : '#fff',
    'top' :  '15%',
    'left': '0%',
  });


    $("#myModal3").modal({backdrop: "static"});
  });
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


