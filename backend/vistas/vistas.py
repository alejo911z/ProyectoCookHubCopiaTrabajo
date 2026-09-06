from flask import request
from flask_restful import Resource

from modelos import RecetaSchema
from logica import Coleccion

recetas_schema = RecetaSchema()
coleccion = Coleccion()


class VistaRecetas(Resource):
    def get(self):
        return coleccion.darReceta()

    def post(self):
        try:
            nombre = request.json["nombre"]
            descripcion = request.json["descripcion"]
            tiempo_preparacion = int(request.json["tiempo_preparacion"])
            dificultad = request.json["dificultad"]
            porciones = int(request.json["porciones"])
            ingrediente_id = int(request.json["ingrediente_id"])
        except (KeyError, ValueError):
            return {"mensaje": "Datos inválidos para crear la receta"}, 400

        nueva_receta = coleccion.agregarReceta(
            nombre, descripcion, tiempo_preparacion, dificultad, porciones, ingrediente_id
        )
        if nueva_receta is None:
            return {"mensaje": "El ingrediente seleccionado no existe"}, 400

        return {"mensaje": "Receta creada exitosamente", "receta": recetas_schema.dump(nueva_receta)}, 201


class VistaReceta(Resource):
    def get(self, id_receta):
        receta = coleccion.darRecetaPorId(id_receta)
        if not receta:
            return {"mensaje": "Receta no encontrada"}, 404
        return receta

    def put(self, id_receta):
        try:
            nombre = request.json["nombre"]
            descripcion = request.json["descripcion"]
            tiempo_preparacion = int(request.json["tiempo_preparacion"])
            dificultad = request.json["dificultad"]
            porciones = int(request.json["porciones"])
            ingrediente_id = int(request.json["ingrediente_id"])
        except (KeyError, ValueError):
            return {"mensaje": "Datos inválidos para actualizar la receta"}, 400

        receta = coleccion.editarReceta(
            id_receta, nombre, descripcion, tiempo_preparacion, dificultad, porciones, ingrediente_id
        )
        if receta is None:
            return {"mensaje": "Receta no encontrada"}, 404
        if receta is False:
            return {"mensaje": "El ingrediente seleccionado no existe"}, 400

        return {"mensaje": "Receta actualizada exitosamente", "receta": receta}

    def delete(self, id_receta):
        eliminado = coleccion.eliminarReceta(id_receta)
        if not eliminado:
            return {"mensaje": "Receta no encontrada"}, 404
        return {"mensaje": "Receta eliminada exitosamente"}


class VistaIngredientes(Resource):
    def get(self):
        return coleccion.darIngrediente()

    def post(self):
        try:
            nombre = request.json["nombre"]
            tipo = request.json["tipo"]
            unidad_medida = request.json["unidad_medida"]
            disponible = bool(request.json.get("disponible", True))
        except (KeyError, ValueError):
            return {"mensaje": "Datos inválidos para crear el ingrediente"}, 400

        nuevo_ingrediente = coleccion.agregarIngrediente(nombre, tipo, unidad_medida, disponible)
        return {"mensaje": "Ingrediente creado exitosamente", "ingrediente": nuevo_ingrediente}, 201


class VistaIngrediente(Resource):
    def get(self, id_ingrediente):
        ingrediente = coleccion.darIngredientePorId(id_ingrediente)
        if not ingrediente:
            return {"mensaje": "Ingrediente no encontrado"}, 404
        return ingrediente

    def put(self, id_ingrediente):
        try:
            nombre = request.json["nombre"]
            tipo = request.json["tipo"]
            unidad_medida = request.json["unidad_medida"]
            disponible = bool(request.json.get("disponible", True))
        except (KeyError, ValueError):
            return {"mensaje": "Datos inválidos para actualizar el ingrediente"}, 400

        ingrediente = coleccion.editarIngrediente(id_ingrediente, nombre, tipo, unidad_medida, disponible)
        if not ingrediente:
            return {"mensaje": "Ingrediente no encontrado"}, 404

        return {"mensaje": "Ingrediente actualizado exitosamente", "ingrediente": ingrediente}

    def delete(self, id_ingrediente):
        resultado = coleccion.eliminarIngrediente(id_ingrediente)
        if resultado is None:
            return {"mensaje": "Ingrediente no encontrado"}, 404
        if resultado is False:
            return {"mensaje": "No se puede eliminar el ingrediente porque tiene recetas asociadas"}, 400
        return {"mensaje": "Ingrediente eliminado exitosamente"}


class VistaReporteIngredientes(Resource):
    def get(self):
        return coleccion.darReporteIngredientes()
