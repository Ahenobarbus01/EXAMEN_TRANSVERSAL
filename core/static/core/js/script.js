$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  if ($('#tabla-principal').length > 0) {

    var table = new DataTable('#tabla-principal', {
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/es-ES.json',
        },
    });

  }

});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()

document.getElementById("editar-rut").addEventListener("click", function() {
var rutSpan = document.getElementById("rut");
var rutInput = document.createElement("input");
rutInput.type = "text";
rutInput.value = rutSpan.innerText;
rutSpan.parentElement.replaceChild(rutInput, rutSpan);

var guardarBtn = document.createElement("button");
guardarBtn.type = "button";
guardarBtn.className = "btn btn-primary";
guardarBtn.innerText = "Guardar";
rutInput.parentElement.appendChild(guardarBtn);

guardarBtn.addEventListener("click", function() {
  rutSpan.innerText = rutInput.value;
  rutInput.parentElement.replaceChild(rutSpan, rutInput);
  this.parentElement.removeChild(this);
});
});

document.getElementById("editar-rut").addEventListener("click", function() {
var rutSpan = document.getElementById("rut");
var rutInput = document.createElement("input");
rutInput.type = "text";
rutInput.value = rutSpan.innerText;
rutSpan.parentElement.replaceChild(rutInput, rutSpan);

var guardarBtn = document.createElement("button");
guardarBtn.type = "button";
guardarBtn.className = "btn btn-primary";
guardarBtn.innerText = "Guardar";
rutInput.parentElement.appendChild(guardarBtn);

guardarBtn.addEventListener("click", function() {
  rutSpan.innerText = rutInput.value;
  rutInput.parentElement.replaceChild(rutSpan, rutInput);
  this.parentElement.removeChild(this);
});
});

