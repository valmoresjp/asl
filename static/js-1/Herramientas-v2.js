
//var $TABLE = $('#table');
var $CLON = $('#TablaClon');
var $BTN = $('#export-btn');
var $EXPORT = $('#datos');
var $TABLE = null;

$('.table-add').click(function () {
  var $clone = $CLON.find('tr.hide').clone(true).removeClass('hide table-line');;
  var idTABLE = '#'+$(this).attr("id").substring(1) + " tbody tr";
  $TABLE = $('#'+$(this).attr("id").substring(1));
    $TABLE.append($clone);
    var a=1;
    $(idTABLE).each( function(a){
      a=a+1;
      $(this).find("td").eq(1).text(a);
    });
});

$('.table-remove').click(function () {
  var idTABLE = '#'+ $(this).closest("table").attr("id")+" tr";
  $(this).parents('tr').detach();
    var a = 0;
    $(idTABLE).each( function(a){
    $(this).find("td").eq(1).text(a);
    a=a+1;
  });
});

// $('.table-up').click(function () {
//   var $row = $(this).parents('tr');
//   if ($row.index() === 1) return; // Don't go above the header
//   $row.prev().before($row.get(0));
// });

// $('.table-down').click(function () {
//   var $row = $(this).parents('tr');
//   $row.next().after($row.get(0));
// });

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

$BTN.click(function () {

  if($TABLE ===null ){
    alert("No existen datos para guardar");
  }else{
    var $rows = $TABLE.find('tr:not(:hidden)');
     var headers = [];
  var data = [];
  var ID;

  // nueva version
  $('table:not(:hidden)').each(function(){
     //console.log($(this).attr('id'));
     ID=$(this).attr('id').toLowerCase();

     $rows = $(this).find('tr:not(:hidden)');
    // Get the headers (add special header logic here)
    $($rows.shift()).find('th:not(:empty)').each(function (i) {
     // console.log(i + " " + ID);
        if ( i == 0){
          headers.push("tipo");
        }else{
          headers.push($(this).text().toLowerCase());
        }
       // console.log(headers);
     // headers.push($(this).text().toLowerCase());
    });
      // Turn all existing rows into a loopable array
    $rows.each(function () {
    var $td = $(this).find('td');
    var h = {};
    
    // Use the headers from earlier to name our hash keys
    headers.forEach(function (header, i) {
      if ( header == "tipo" ){
        h[header] = ID;  
      }else{
        h[header] = $td.eq(i).text();
        }         
    });

    data.push(h);
  });

    $EXPORT.val(JSON.stringify(data));
    headers = [];
    //data = [];

  });

  // se ejecuta el codigo para la ventana emergente y enviar los datos para ser almacenados.
  //$("#datos").val("prueba");
   $("#myBtn3").click();

  } 
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







