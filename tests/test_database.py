import csv
import helpers
import config
import copy
import unittest
import database as db


class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        db.Clientes.lista=[
            db.Cliente('12J', 'Pepe', 'Lopez'),
            db.Cliente('68L', 'Pablo', 'Dominguez'),
            db.Cliente('98H', 'Enrique', 'Arias')

        ]

    def test_buscar_cliente(self):
        cliente_existente=db.Clientes.buscar('12J')
        cliente_inexistente=db.Clientes.buscar('99X')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        nuevo_cliente=db.Clientes.crear('56P', 'Nicol', 'Armijos')
        self.assertEqual(len(db.Clientes.lista),4)
        self.assertEqual(nuevo_cliente.dni,'56P')
        self.assertEqual(nuevo_cliente.nombre,'Nicol')
        self.assertEqual(nuevo_cliente.apellido,'Armijos')

    def test_modificar_cliente(self):
        cliente_a_modificar=copy.copy(db.Clientes.buscar('98H'))
        cliente_modificado=db.Clientes.modificar('98H', 'Pedro', 'Arias')
        self.assertEqual(cliente_a_modificar.nombre,'Enrique')
        self.assertEqual(cliente_modificado.nombre,'Pedro')

    def test_borrar_cliente(self):
        cliente_borrado=db.Clientes.borrar('68L')
        cliente_rebuscado=db.Clientes.buscar('68L')
        self.assertEqual(cliente_borrado.dni,'68L')
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('22229E',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('J98',db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('12J',db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('12J')
        db.Clientes.borrar('98H')
        db.Clientes.modificar('68L','Mariana','Garcia')

        dni,nombre,apellido=None,None,None

        with open(config.DATABASE_PATH,newline='\n')as fichero:
            reader = csv.reader(fichero,delimiter=';')
            dni,nombre,apellido=next(reader)

        self.assertEqual(dni,'68L')
        self.assertEqual(nombre,'Mariana')
        self.assertEqual(apellido,'Garcia')



