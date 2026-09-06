import os
import unittest
from unittest.mock import patch

# Debe fijarse ANTES de importar `app`: usa un archivo sqlite propio para
# pruebas, distinto del que usa el backend en desarrollo, para no leer ni
# borrar datos reales al correr los tests.
os.environ.setdefault("COOKHUB_DATABASE_URL", "sqlite:///test_cookhub.db")

from app import app
from modelos import db, Receta
from logica.coleccion import Coleccion

INGREDIENTES_PRUEBA = [
    {"id": 1, "nombre": "Pollo", "tipo": "Proteína", "unidad_medida": "gramos", "disponible": True},
    {"id": 2, "nombre": "Arroz", "tipo": "Carbohidrato", "unidad_medida": "gramos", "disponible": True},
]

class TestColeccionRecetas(unittest.TestCase):


    def setUp(self):
        self.coleccion = Coleccion()
        self.app_context = app.app_context()
        self.app_context.push()
        Receta.query.delete()
        db.session.commit()

    def tearDown(self):
        """Borra las recetas creadas durante la prueba"""
        Receta.query.delete()
        db.session.commit()
        self.app_context.pop()

    @patch("logica.coleccion.ingredientes", INGREDIENTES_PRUEBA)
    def test_agregar_receta(self):
        receta = self.coleccion.agregarReceta(
            nombre="Sopa de prueba",
            descripcion="Sopa creada para la prueba",
            tiempo_preparacion=15,
            dificultad="Fácil",
            porciones=2,
            ingrediente_id=1
        )
        self.assertIsInstance(receta, Receta)
        self.assertEqual(receta.nombre, "Sopa de prueba")
        self.assertEqual(Receta.query.count(), 1)

    @patch("logica.coleccion.ingredientes", INGREDIENTES_PRUEBA)
    def test_agregar_receta_con_ingrediente_inexistente(self):
        """Prueba que no se cree la receta si el ingrediente no existe"""
        receta = self.coleccion.agregarReceta(
            nombre="Receta inválida",
            descripcion="No debería crearse",
            tiempo_preparacion=10,
            dificultad="Fácil",
            porciones=1,
            ingrediente_id=999
        )
        self.assertIsNone(receta)
        self.assertEqual(Receta.query.count(), 0)

    @patch("logica.coleccion.ingredientes", INGREDIENTES_PRUEBA)
    def test_listar_recetas(self):
        """Prueba que darReceta() devuelva las recetas ya creadas"""
        self.coleccion.agregarReceta("Receta A", "desc", 10, "Fácil", 2, 1)
        self.coleccion.agregarReceta("Receta B", "desc", 20, "Medio", 4, 2)

        recetas = self.coleccion.darReceta()

        self.assertIsInstance(recetas, list)
        nombres = [r["nombre"] for r in recetas]
        self.assertIn("Receta A", nombres)
        self.assertIn("Receta B", nombres)

    @patch("logica.coleccion.ingredientes", INGREDIENTES_PRUEBA)
    def test_listar_recetas_adjunta_su_ingrediente(self):
        """Prueba que cada receta listada traiga los datos de su ingrediente"""
        self.coleccion.agregarReceta("Receta C", "desc", 5, "Fácil", 1, 2)

        recetas = self.coleccion.darReceta()
        receta_c = next(r for r in recetas if r["nombre"] == "Receta C")

        self.assertIsNotNone(receta_c["ingrediente"])
        self.assertEqual(receta_c["ingrediente"]["nombre"], "Arroz")


class TestColeccionIngredientes(unittest.TestCase):
    def setUp(self):
        """Crea una colección para hacer las pruebas"""
        self.coleccion = Coleccion()

    @patch("logica.coleccion.recetas", [])
    @patch("logica.coleccion.ingredientes", list(INGREDIENTES_PRUEBA))
    def test_listar_ingredientes(self):
        """Prueba que darIngrediente() devuelva los ingredientes disponibles"""
        ingredientes = self.coleccion.darIngrediente()

        self.assertIsInstance(ingredientes, list)
        self.assertEqual(len(ingredientes), 2)
        nombres = [i["nombre"] for i in ingredientes]
        self.assertIn("Pollo", nombres)
        self.assertIn("Arroz", nombres)


