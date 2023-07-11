from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Categoria, Producto, Boleta, Carrito, DetalleBoleta,Bodega, Perfil
from .forms import ProductoForm, BodegaForm, RegistroClienteForm, IngresarForm
from .zpoblar import poblar_bd
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.contrib import messages
from .tools import eliminar_registro, verificar_eliminar_registro
from core.templatetags.custom_filters import formatear_dinero, formatear_numero



def inicio(request):

    if request.method == 'POST':
        buscar = request.POST.get('buscar')
        registros = Producto.objects.filter(nombre__icontains=buscar).order_by('nombre')
    else:
        registros = Producto.objects.all().order_by('nombre')

    productos = []
    for registro in registros:
        productos.append(obtener_info_producto(registro.id))

    datos = { 'productos': productos }
    return render(request, 'core/incio.html', datos)


def registrarme(request):

    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/registrarme.html", {'form': form})


def nosotros(request):
    return render(request, 'core/nosotros.html')

def ropa(request):
    return render(request, 'core/ropa.html')


def administrar(request):
    return render(request, 'core/administrar.html')

def mantenedor_de_usuarios(request):
    return render(request, 'core/mantenedor_de_usuarios.html')

def detalle_de_boleta(request):
    return render(request, 'core/detalle_de_boleta.html')


def mantenedor_de_bodega(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        for cantidad in range(1, cantidad + 1):
            Bodega.objects.create(producto=producto)
        if cantidad == 1:
            messages.success(request, f'Se ha agregado 1 nuevo "{producto.nombre}" a la bodega')
        else:
            messages.success(request, f'Se han agregado {cantidad} productos de "{producto.nombre}" a la bodega')

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    return render(request, 'core/mantenedor_de_bodega.html', {
        'form': BodegaForm(),
        'productos': lista,
    })


def obtener_productos(request):
    categoria_id = request.GET.get('categoria_id')
    productos = Producto.objects.filter(categoria_id=categoria_id)
    data = [
        {
            'id': producto.id, 
            'nombre': producto.nombre, 
            'imagen': producto.imagen.url
        } for producto in productos
    ]
    return JsonResponse(data, safe=False)


def eliminar_producto_en_bodega(request, bodega_id):
    
    nombre_producto = Bodega.objects.get(id=bodega_id).producto.nombre
    eliminado, error = verificar_eliminar_registro(Bodega, bodega_id, True)
    
    if eliminado:
        messages.success(request, f'Se ha eliminado el ID {bodega_id} ({nombre_producto}) de la bodega')
    else:
        messages.error(request, error)

    return redirect()


def ventas(request):
    boletas = Boleta.objects.all()
    historial =[]
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'nom_cliente': f'{boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}',
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'subscrito': 'Sí' if boleta.cliente.subscrito else 'No',
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/ventas.html', { 
        'historial': historial 
    })


def boleta(request, nro_boleta):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    detalle_boleta = DetalleBoleta.objects.filter(boleta=boleta)
    datos = { 
        'boleta': boleta, 
        'detalle_boleta': detalle_boleta 
    }
    return render(request, 'core/boleta.html', datos)


def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Despachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(ventas)


def ingresar(request):

    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(inicio)
            messages.error(request, 'La cuenta o la password no son correctos')
    
    return render(request, "core/ingresar.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
    })


def misdatos(request):
    return render(request, 'core/misdatos.html')


def miscompras(request):

    usuario = User.objects.get(username='eolsen')
    perfil = Perfil.objects.get(usuario=usuario)

    boletas = Boleta.objects.filter(cliente=perfil)
    historial =[]
    for boleta in boletas:
        boleta_historial = {
            'nro_boleta': boleta.nro_boleta,
            'fecha_venta': boleta.fecha_venta,
            'fecha_despacho': boleta.fecha_despacho,
            'fecha_entrega': boleta.fecha_entrega,
            'total_a_pagar': boleta.total_a_pagar,
            'estado': boleta.estado,
        }
        historial.append(boleta_historial)
    return render(request, 'core/miscompras.html', { 
        'historial': historial 
    })


def salir(request):
    logout(request)
    return redirect(inicio)


def carrito(request):

    detalle_carrito = Carrito.objects.filter(cliente=request.user.perfil)

    total_a_pagar = 0
    for item in detalle_carrito:
        total_a_pagar += item.precio_a_pagar
    monto_sin_iva = int(round(total_a_pagar / 1.19))
    iva = total_a_pagar - monto_sin_iva

    return render(request, 'core/carrito.html', {
        'detalle_carrito': detalle_carrito,
        'monto_sin_iva': monto_sin_iva,
        'iva': iva,
        'total_a_pagar': total_a_pagar,
    })


def eliminar_producto_en_carrito(request, carrito_id):

    Carrito.objects.get(id=carrito_id).delete()

    return redirect(carrito)


def agregar_producto_al_carrito(request, producto_id):

    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)

    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)

    precio = producto.precio
    descuento_subscriptor = producto.descuento_subscriptor if perfil.subscrito else 0
    descuento_total=producto.descuento_subscriptor + producto.descuento_oferta if perfil.subscrito else producto.descuento_oferta
    precio_a_pagar = precio_subscr if perfil.subscrito else precio_oferta
    descuentos = precio - precio_subscr if perfil.subscrito else precio - precio_oferta

    Carrito.objects.create(
        cliente=perfil,
        producto=producto,
        precio=precio,
        descuento_subscriptor=descuento_subscriptor,
        descuento_oferta=producto.descuento_oferta,
        descuento_total=descuento_total,
        descuentos=descuentos,
        precio_a_pagar=precio_a_pagar
    )

    return redirect(ficha, producto_id)


def ficha(request, producto_id):

    context = obtener_info_producto(producto_id)
    return render(request, 'core/ficha.html', context)


def obtener_info_producto(producto_id):

    producto = Producto.objects.get(id=producto_id)
    stock = Bodega.objects.filter(producto_id=producto_id).exclude(detalleboleta__isnull=False).count()
    
    # Preparar texto para mostrar estado: en oferta, sin oferta y agotado
    con_oferta = f'<span class="text-primary"> EN OFERTA {producto.descuento_oferta}% DE DESCUENTO </span>'
    sin_oferta = '<span class="text-success"> DISPONIBLE EN BODEGA </span>'
    agotado = '<span class="text-danger"> AGOTADO </span>'

    if stock == 0:
        estado = agotado
    else:
        estado = sin_oferta if producto.descuento_oferta == 0 else con_oferta

    # Preparar texto para indicar cantidad de productos en stock
    en_stock = f'En stock: {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"}'
   
    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen': producto.imagen,
        'html_estado': estado,
        'html_precio': obtener_html_precios_producto(producto),
        'html_stock': en_stock,
    }


def calcular_precios_producto(producto):
    precio_normal = producto.precio
    precio_oferta = producto.precio * (100 - producto.descuento_oferta) / 100
    precio_subscr = producto.precio * (100 - (producto.descuento_oferta + producto.descuento_subscriptor)) / 100
    hay_desc_oferta = producto.descuento_oferta > 0
    hay_desc_subscr = producto.descuento_subscriptor > 0
    return precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr


def obtener_html_precios_producto(producto):
    
    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)
    
    normal = f'Normal: {formatear_dinero(precio_normal)}'
    tachar = f'Normal: <span class="text-decoration-line-through"> {formatear_dinero(precio_normal)} </span>'
    oferta = f'Oferta: <span class="text-success"> {formatear_dinero(precio_oferta)} </span>'
    subscr = f'Subscrito: <span class="text-danger"> {formatear_dinero(precio_subscr)} </span>'

    if hay_desc_oferta > 0:
        texto_precio = f'{tachar}<br>{oferta}'
    else:
        texto_precio = normal

    if hay_desc_subscr > 0:
        texto_precio += f'<br>{subscr}'

    return texto_precio
    

def admin_productos(request, accion, id):
    data = {
        'mensaje': '', 
        'formulario': ProductoForm, 
        'accion': accion, 
        'id': id, 
    }

    if accion == 'ins':
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, request.FILES)
            if formulario.is_valid():
                try:
                    formulario.save()
                    data['mensaje'] = '¡El producto fue creado correctamente!'
                except:
                    data['mensaje'] = '¡No se puede crear dos productos con el mismo ID!'

    elif accion == 'upd':
        producto = Producto.objects.get(id=id)
        if request.method == 'POST':
            formulario = ProductoForm(data=request.POST, files=request.FILES, instance=producto)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = '¡El producto fue actualizado correctamente!'
        data['formulario'] = ProductoForm(instance=producto)

    elif accion == 'del':
        try:
            Producto.objects.get(id=id).delete()
            data['mensaje'] = '¡El producto fue eliminado correctamente!'
            return redirect(admin_productos, accion='ins', id = '-1')
        except:
            data['mensaje'] = '¡El producto ya estaba eliminado!'

    data['productos'] = Producto.objects.all().order_by('id')
    return render(request, 'core/admin_productos.html', data)

def premio(request):
    return render(request, 'core/premio.html')


def poblar(request):
    poblar_bd()
    return redirect(inicio)
