// objeto.metodo(json)

$(document).ready(function () {

    $("#productos").validate({
        rules: {
            id: {
                required: true,
            },
            nombres: {
                required: true,
            },
            detalle: {
                required: true,
            },
            precio: {
                required: true,
            },
            descuento: {
                required: true,
            },
            descuentos: {
                required: true,
            },
        },
        messages: {
            id: {
                required: "La ID es un campo obligatorio",
            },
            nombres: {
                required: "El nombre es un campo requerido",
            },
            detalle: {
                required: "La descripción es un campo requerido",
            },
            precio: {
                required: "El precio es un campo obligatorio",
            },
            descuento: {
                required: "El descuento es un campo obligatorio",
            },
            descuentos: {
                required: "El descuento es un campo obligatorio",
            },
        },
    });
});
  