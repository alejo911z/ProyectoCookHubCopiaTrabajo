from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db, EnumADiccionario, EnumANombre
from .receta import Dificultad, Receta
from .ingrediente import TipoIngrediente, UnidadMedida, Ingrediente


class RecetaSchema(SQLAlchemyAutoSchema):
    dificultad = EnumANombre(attribute='dificultad')

    class Meta:
        model = Receta
        include_relationships = True
        load_instance = True


class IngredienteSchema(SQLAlchemyAutoSchema):
    tipo = EnumADiccionario(attribute='tipo')
    unidad_medida = EnumADiccionario(attribute='unidad_medida')

    class Meta:
        model = Ingrediente
        include_relationships = True
        load_instance = True
