import unittest
from flask import jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import app, agregar_producto

class TestAPIAgregar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        self.productos = {
            1: {"nombre": "Producto A", "cantidad": 10},
            2: {"nombre": "Esferas de vidrio", "cantidad": 12},
        }

    def test_agregar_producto(self):
        self.assertEqual(agregar_producto(1, 5), "Producto Producto A actualizado. Nueva cantidad: 15.")
        self.assertEqual(agregar_producto(3, -5), "Error: La cantidad debe ser un número entero positivo.")
        
        response = self.client.post('/producto', json={'nombre': 'Producto C', 'cantidad': 30})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['nombre'], 'Producto C')

        response = self.client.post('/producto', json={'nombre': 'Producto D'})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
