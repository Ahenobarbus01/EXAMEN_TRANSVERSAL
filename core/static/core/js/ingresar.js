$(document).ready(function() {

  $('#form').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'password': {
          required: true,
        },
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'password': {
          required: 'Debe ingresar una contraseña',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); 
        error.addClass('error-message'); 
      },
  });

  $('#user-select').change(function() {
    var username = $(this).val();
    var password = 'Duoc@123';
    if ('cevans eolsen tholland sjohansson cpratt mruffalo super'.includes(username)) {
      password = '123';
    };
    $('#id_username').val(username);
    $('#id_password').val(password);
  });

});
