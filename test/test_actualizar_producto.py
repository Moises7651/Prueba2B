import unittest
from flask import jsonify
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app import app, actualizar_stock

class TestAPIActualizar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def setUp(self):
        self.productos = {
            1: {"nombre": "Producto A", "cantidad": 10},
            2: {"nombre": "Esferas de vidrio", "cantidad": 12},
        }

    def test_actualizar_producto(self):
        self.assertEqual(actualizar_stock(1, 50), "Producto Producto A actualizado. Nueva cantidad: 50.")
        self.assertRaises(AssertionError, actualizar_stock, 1, -5)
        
        response = self.client.put('/producto/1', json={'cantidad': 50})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['cantidad'], 50)

        response = self.client.put('/producto/1', json={'cantidad': -5})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
