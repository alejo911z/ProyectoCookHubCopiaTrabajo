from data.mock_data import recetas, ingredientes, reporte_ingredientes
from modelos import db, Receta, RecetaSchema

recetas_schema = RecetaSchema()


class Coleccion:
    def darReceta(self):
        recetas_con_ingrediente = []
        for receta in Receta.query.all():
            ingrediente = next((i for i in ingredientes if i["id"] == receta.ingrediente_id), None)
            receta_completa = recetas_schema.dump(receta)
            receta_completa["ingrediente"] = ingrediente
            recetas_con_ingrediente.append(receta_completa)
        return recetas_con_ingrediente

    def darRecetaPorId(self, id_receta):
        receta = next((r for r in recetas if r["id"] == id_receta), None)
        if not receta:
            return None

        ingrediente = next((i for i in ingredientes if i["id"] == receta["ingrediente_id"]), None)
        receta_completa = receta.copy()
        receta_completa["ingrediente"] = ingrediente
        return receta_completa

    def agregarReceta(self, nombre, descripcion, tiempo_preparacion, dificultad, porciones, ingrediente_id):
        nueva_receta = Receta(
            nombre=nombre,
            descripcion=descripcion,
            tiempo_preparacion=tiempo_preparacion,
            dificultad=dificultad,
            porciones=porciones,
            ingrediente_id=ingrediente_id
        )

        if not any(i["id"] == nueva_receta.ingrediente_id for i in ingredientes):
            return None

        db.session.add(nueva_receta)
        db.session.commit()

        return nueva_receta

    def editarReceta(self, id_receta, nombre, descripcion, tiempo_preparacion, dificultad, porciones, ingrediente_id):
        receta = next((r for r in recetas if r["id"] == id_receta), None)
        if not receta:
            return None

        if not any(i["id"] == ingrediente_id for i in ingredientes):
            return False

        receta["nombre"] = nombre
        receta["descripcion"] = descripcion
        receta["tiempo_preparacion"] = tiempo_preparacion
        receta["dificultad"] = dificultad
        receta["porciones"] = porciones
        receta["ingrediente_id"] = ingrediente_id

        return receta

    def eliminarReceta(self, id_receta):
        global recetas
        receta = next((r for r in recetas if r["id"] == id_receta), None)
        if not receta:
            return False

        recetas = [r for r in recetas if r["id"] != id_receta]
        return True

    def darIngrediente(self):
        ingredientes_con_conteo = []
        for ingrediente in ingredientes:
            conteo_recetas = len([r for r in recetas if r["ingrediente_id"] == ingrediente["id"]])
            ingrediente_completo = ingrediente.copy()
            ingrediente_completo["cantidad_recetas"] = conteo_recetas
            ingredientes_con_conteo.append(ingrediente_completo)
        return ingredientes_con_conteo

    def darIngredientePorId(self, id_ingrediente):
        return next((i for i in ingredientes if i["id"] == id_ingrediente), None)

    def agregarIngrediente(self, nombre, tipo, unidad_medida, disponible=True):
        nuevo_ingrediente = {
            "id": max([i["id"] for i in ingredientes]) + 1 if ingredientes else 1,
            "nombre": nombre,
            "tipo": tipo,
            "unidad_medida": unidad_medida,
            "disponible": bool(disponible)
        }
        ingredientes.append(nuevo_ingrediente)
        return nuevo_ingrediente

    def editarIngrediente(self, id_ingrediente, nombre, tipo, unidad_medida, disponible=True):
        ingrediente = next((i for i in ingredientes if i["id"] == id_ingrediente), None)
        if not ingrediente:
            return None

        ingrediente["nombre"] = nombre
        ingrediente["tipo"] = tipo
        ingrediente["unidad_medida"] = unidad_medida
        ingrediente["disponible"] = bool(disponible)

        return ingrediente

    def eliminarIngrediente(self, id_ingrediente):
        global ingredientes
        ingrediente = next((i for i in ingredientes if i["id"] == id_ingrediente), None)
        if not ingrediente:
            return None

        recetas_asociadas = [r for r in recetas if r["ingrediente_id"] == id_ingrediente]
        if recetas_asociadas:
            return False

        ingredientes = [i for i in ingredientes if i["id"] != id_ingrediente]
        return True

    def darReporteIngredientes(self):
        return reporte_ingredientes
