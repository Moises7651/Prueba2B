import unittest
from flask import jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import app, consultar_producto

class TestAPIConsultar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        # Crear una copia de la base de datos antes de cada prueba
        self.productos = {
            1: {"nombre": "Producto A", "cantidad": 10},
            2: {"nombre": "Esferas de vidrio", "cantidad": 12},
        }

    def test_consultar_producto(self):
        self.assertEqual(consultar_producto(1), {"nombre": "Producto A", "cantidad": 10})
        self.assertEqual(consultar_producto(999), "Error: Producto no encontrado.")
        self.assertEqual(consultar_producto(-1), "Error: El ID del producto debe ser un número entero positivo.")
        
        response = self.client.get('/producto/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('nombre', response.json)

        response = self.client.get('/producto/999')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
