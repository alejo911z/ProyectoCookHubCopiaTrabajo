from flask import request
from flask_restful import Resource
from data.mock_data import recetas, ingredientes, reporte_ingredientes

class VistaRecetas(Resource):
    def get(self):
        recetas_con_ingrediente = []
        for receta in recetas:
            ingrediente = next((i for i in ingredientes if i["id"] == receta["ingrediente_id"]), None)
            receta_completa = receta.copy()
            receta_completa["ingrediente"] = ingrediente
            recetas_con_ingrediente.append(receta_completa)
        return recetas_con_ingrediente

    def post(self):
        try:
            nueva_receta = {
                "id": max([r["id"] for r in recetas]) + 1 if recetas else 1,
                "nombre": request.json["nombre"],
                "descripcion": request.json["descripcion"],
                "tiempo_preparacion": int(request.json["tiempo_preparacion"]),
                "dificultad": request.json["dificultad"],
                "porciones": int(request.json["porciones"]),
                "ingrediente_id": int(request.json["ingrediente_id"])
            }
            
            # Validar que el ingrediente existe
            if not any(i["id"] == nueva_receta["ingrediente_id"] for i in ingredientes):
                return {"mensaje": "El ingrediente seleccionado no existe"}, 400
            
            recetas.append(nueva_receta)
            return {"mensaje": "Receta creada exitosamente", "receta": nueva_receta}, 201
        except (KeyError, ValueError) as e:
            return {"mensaje": "Datos inválidos para crear la receta"}, 400

class VistaReceta(Resource):
    def get(self, id_receta):
        receta = next((r for r in recetas if r["id"] == id_receta), None)
        if not receta:
            return {"mensaje": "Receta no encontrada"}, 404
        
        ingrediente = next((i for i in ingredientes if i["id"] == receta["ingrediente_id"]), None)
        receta_completa = receta.copy()
        receta_completa["ingrediente"] = ingrediente
        return receta_completa

    def put(self, id_receta):
        try:
            receta = next((r for r in recetas if r["id"] == id_receta), None)
            if not receta:
                return {"mensaje": "Receta no encontrada"}, 404
            
            # Validar que el ingrediente existe
            if not any(i["id"] == int(request.json["ingrediente_id"]) for i in ingredientes):
                return {"mensaje": "El ingrediente seleccionado no existe"}, 400
            
            receta["nombre"] = request.json["nombre"]
            receta["descripcion"] = request.json["descripcion"]
            receta["tiempo_preparacion"] = int(request.json["tiempo_preparacion"])
            receta["dificultad"] = request.json["dificultad"]
            receta["porciones"] = int(request.json["porciones"])
            receta["ingrediente_id"] = int(request.json["ingrediente_id"])
            
            return {"mensaje": "Receta actualizada exitosamente", "receta": receta}
        except (KeyError, ValueError) as e:
            return {"mensaje": "Datos inválidos para actualizar la receta"}, 400

    def delete(self, id_receta):
        global recetas
        receta = next((r for r in recetas if r["id"] == id_receta), None)
        if not receta:
            return {"mensaje": "Receta no encontrada"}, 404
        
        recetas = [r for r in recetas if r["id"] != id_receta]
        return {"mensaje": "Receta eliminada exitosamente"}

class VistaIngredientes(Resource):
    def get(self):
        ingredientes_con_conteo = []
        for ingrediente in ingredientes:
            conteo_recetas = len([r for r in recetas if r["ingrediente_id"] == ingrediente["id"]])
            ingrediente_completo = ingrediente.copy()
            ingrediente_completo["cantidad_recetas"] = conteo_recetas
            ingredientes_con_conteo.append(ingrediente_completo)
        return ingredientes_con_conteo

    def post(self):
        try:
            nuevo_ingrediente = {
                "id": max([i["id"] for i in ingredientes]) + 1 if ingredientes else 1,
                "nombre": request.json["nombre"],
                "tipo": request.json["tipo"],
                "unidad_medida": request.json["unidad_medida"],
                "disponible": bool(request.json.get("disponible", True))
            }
            ingredientes.append(nuevo_ingrediente)
            return {"mensaje": "Ingrediente creado exitosamente", "ingrediente": nuevo_ingrediente}, 201
        except (KeyError, ValueError) as e:
            return {"mensaje": "Datos inválidos para crear el ingrediente"}, 400

class VistaIngrediente(Resource):
    def get(self, id_ingrediente):
        ingrediente = next((i for i in ingredientes if i["id"] == id_ingrediente), None)
        if not ingrediente:
            return {"mensaje": "Ingrediente no encontrado"}, 404
        return ingrediente

    def put(self, id_ingrediente):
        try:
            ingrediente = next((i for i in ingredientes if i["id"] == id_ingrediente), None)
            if not ingrediente:
                return {"mensaje": "Ingrediente no encontrado"}, 404
            
            ingrediente["nombre"] = request.json["nombre"]
            ingrediente["tipo"] = request.json["tipo"]
            ingrediente["unidad_medida"] = request.json["unidad_medida"]
            ingrediente["disponible"] = bool(request.json.get("disponible", True))
            
            return {"mensaje": "Ingrediente actualizado exitosamente", "ingrediente": ingrediente}
        except (KeyError, ValueError) as e:
            return {"mensaje": "Datos inválidos para actualizar el ingrediente"}, 400

    def delete(self, id_ingrediente):
        global ingredientes
        ingrediente = next((i for i in ingredientes if i["id"] == id_ingrediente), None)
        if not ingrediente:
            return {"mensaje": "Ingrediente no encontrado"}, 404
        
        # Verificar que no tenga recetas asociadas
        recetas_asociadas = [r for r in recetas if r["ingrediente_id"] == id_ingrediente]
        if recetas_asociadas:
            return {"mensaje": "No se puede eliminar el ingrediente porque tiene recetas asociadas"}, 400
        
        ingredientes = [i for i in ingredientes if i["id"] != id_ingrediente]
        return {"mensaje": "Ingrediente eliminado exitosamente"}

class VistaReporteIngredientes(Resource):
    def get(self):
        return reporte_ingredientes