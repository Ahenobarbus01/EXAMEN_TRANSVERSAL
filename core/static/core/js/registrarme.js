$(document).ready(function() {

  // Agregar método de validación para RUT chileno
  $.validator.addMethod("rutChileno", function(value, element) {
    // Eliminar puntos y guión del RUT
    value = value.replace(/[.-]/g, "");

    // Validar que el RUT tenga 8 o 9 dígitos
    if (value.length < 8 || value.length > 9) {
      return false;
    }

    // Validar que el último dígito sea un número o una 'K'
    var validChars = "0123456789K";
    var lastChar = value.charAt(value.length - 1).toUpperCase();
    if (validChars.indexOf(lastChar) == -1) {
      return false;
    }

    // Calcular el dígito verificador
    var rut = parseInt(value.slice(0, -1), 10);
    var factor = 2;
    var sum = 0;
    var digit;
    while (rut > 0) {
      digit = rut % 10;
      sum += digit * factor;
      rut = Math.floor(rut / 10);
      factor = factor === 7 ? 2 : factor + 1;
    }
    var dv = 11 - (sum % 11);
    dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();

    // Validar que el dígito verificador sea correcto
    return dv === lastChar;
  }, "Por favor ingrese un RUT válido."); 

  $.validator.setDefaults({
      messages: {
        required: 'Este campo es obligatorio',
      },
  });

  $('#form').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'first_name': {
          required: true,
        },
        'first_name': {
          required: true,
        },
        'last_name': {
          required: true,
        },
        'email': {
          required: true,
          email: true,
        },
        'rut': {
          required: true,
          rutChileno: true,
        },
        'direccion': {
          required: true,
        },
        'password1': {
          required: true,
          minlength: 8,
        },
        'password2': {
          required: true,
          equalTo: '#id_password1'
        }
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'first_name': {
          required: 'Debe ingresar su nombre',
        },
        'last_name': {
          required: 'Debe ingresar sus apellidos',
        },
        'email': {
          required: 'Debe ingresar su correo',
          email: 'El formato del correo no es válido',
        },
        'rut': {
          required: 'Debe ingresar su RUT',
          rutChileno: 'El formato del RUT no es válido',
        },
        'direccion': {
          required: 'Debe ingresar su dirección',
        },
        'password1': {
          required: 'Debe ingresar una contraseña',
          minlength: 'La contraseña debe tener al menos 8 caracteres',
        },
        'password2': {
          required: 'Debe ingresar una contraseña',
          equalTo: 'Debe repetir la contraseña anterior'
        }
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
        //element.after('<br>'); 
      },
  });

  $('#id_imagen').change(function() {
    var input = this;
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#registrarme-imagen').attr('src', e.target.result).show();
      };
      reader.readAsDataURL(input.files[0]);
    }
  });

  $('#crear_usuario_prueba').click(function(event) {
    event.preventDefault();
    $.get('https://randomuser.me/api/?results=1', // API para obtener datos de usuario al azar
      function(data){
        $.each(data.results, function(i, item) { // Recorrer las filas devueltas por la API
          $('#id_username').val(item.login.username);
          $('#id_first_name').val(item.name.first);
          $('#id_last_name').val(item.name.last);
          $('#id_email').val(item.email);
          $('#id_rut').val('11.111.111-1');
          $('#id_direccion').val(`${item.location.street.number} ${item.location.street.name}\n${item.location.city}\n${item.location.country}`);
          $('#id_subscrito').val(true);
          $('#id_imagen').val('');
          $('#id_password1').val('Duoc@123');
          $('#id_password2').val('Duoc@123');
        });
      });
  });

});