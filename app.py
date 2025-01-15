from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

# Simulación de base de datos de productos
productos = {
    1: {"nombre": "Producto A", "cantidad": 10},
    2: {"nombre": "Esferas de vidrio", "cantidad": 12},
}

# Parte 1: Programación Defensiva

# Función para consultar un producto
def consultar_producto(id_producto):
    if not isinstance(id_producto, int) or id_producto <= 0:
        return "Error: El ID del producto debe ser un número entero positivo."
    
    if id_producto not in productos:
        return "Error: Producto no encontrado."
    
    producto = productos[id_producto]
    return producto

# Función para agregar producto
def agregar_producto(id_producto, cantidad):
    if not isinstance(id_producto, int) or id_producto <= 0:
        return "Error: El ID del producto debe ser un número entero positivo."
    
    if not isinstance(cantidad, int) or cantidad <= 0:
        return "Error: La cantidad debe ser un número entero positivo."
    
    if id_producto in productos:
        productos[id_producto]["cantidad"] += cantidad
        return f"Producto {productos[id_producto]['nombre']} actualizado. Nueva cantidad: {productos[id_producto]['cantidad']}."
    else:
        return "Error: Producto no encontrado."

# Parte 2: Programación por Contrato y Aserciones

# Función para actualizar el stock de un producto
def actualizar_stock(id_producto, nueva_cantidad):
    # Contrato: id_producto debe ser un entero positivo
    assert isinstance(id_producto, int) and id_producto > 0, "Error: El ID del producto debe ser un número entero positivo."
    # Contrato: nueva_cantidad debe ser un entero no negativo
    assert isinstance(nueva_cantidad, int) and nueva_cantidad >= 0, "Error: La nueva cantidad debe ser un número entero no negativo."
    
    if id_producto not in productos:
        return "Error: Producto no encontrado."
    
    productos[id_producto]["cantidad"] = nueva_cantidad
    return f"Producto {productos[id_producto]['nombre']} actualizado. Nueva cantidad: {nueva_cantidad}."

# Parte 3: API con Flask

@app.route('/')
def home():
    return "API de Inventario - Bienvenido"

@app.route('/producto/<int:id_producto>', methods=['GET'])
def consultar_producto_api(id_producto):
    producto = consultar_producto(id_producto)
    if isinstance(producto, dict):
        return jsonify(producto)
    return jsonify({"error": producto}), 400

@app.route('/producto', methods=['POST'])
def agregar_producto_api():
    data = request.get_json()
    if 'nombre' not in data or 'cantidad' not in data:
        return jsonify({"error": "Datos incompletos, se requiere 'nombre' y 'cantidad'."}), 400
    
    try:
        nombre = data['nombre']
        cantidad = int(data['cantidad'])
        if cantidad <= 0:
            return jsonify({"error": "La cantidad debe ser un número entero positivo."}), 400
    except ValueError:
        return jsonify({"error": "La cantidad debe ser un número entero."}), 400
    
    # Simulando el agregar producto a la base de datos
    nuevo_id = max(productos.keys()) + 1
    productos[nuevo_id] = {"nombre": nombre, "cantidad": cantidad}
    return jsonify({"id_producto": nuevo_id, "nombre": nombre, "cantidad": cantidad}), 201

@app.route('/producto/<int:id_producto>', methods=['PUT'])
def actualizar_producto_api(id_producto):
    if id_producto not in productos:
        return jsonify({"error": "Producto no encontrado"}), 404

    data = request.get_json()
    if 'cantidad' not in data:
        return jsonify({"error": "Datos incompletos, se requiere 'cantidad'."}), 400
    
    try:
        nueva_cantidad = int(data['cantidad'])
        if nueva_cantidad < 0:
            return jsonify({"error": "La nueva cantidad debe ser un número entero no negativo."}), 400
    except ValueError:
        return jsonify({"error": "La cantidad debe ser un número entero."}), 400
    
    # Actualización con función por contrato
    try:
        actualizar_stock(id_producto, nueva_cantidad)
    except AssertionError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify(productos[id_producto])

if __name__ == '__main__':
    app.run(debug=True)
