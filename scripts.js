let idProducto = 1;  
let nuevaCantidad = 50; 

// Realizando la solicitud PUT a la API
fetch(`http://127.0.0.1:5000/producto/${idProducto}`, {
    method: 'PUT',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        cantidad: nuevaCantidad  // El cuerpo de la solicitud con la nueva cantidad
    })
})
.then(response => response.json())  // Procesa la respuesta como JSON
.then(data => {
    console.log('Respuesta del servidor:', data);
})
.catch(error => {
    console.error('Error al actualizar el producto:', error);
});


/////Nuevo producto
fetch('http://127.0.0.1:5000/producto', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        nombre: 'Nuevo Producto',
        cantidad: 50
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
