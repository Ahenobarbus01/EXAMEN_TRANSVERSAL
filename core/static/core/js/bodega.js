// objeto.metodo(json)

$(document).ready(function () {

    $("#bodega").validate({
        rules: {
            cantidad: {
                required: true,
            },
            nombres: {
                required: true,
            },
        },
        messages: {
            cantidad: {
                required: "La ID es un campo obligatorio",
            },
            nombres: {
                required: "El nombre es un campo requerido",
            },
        },
    });
});
  