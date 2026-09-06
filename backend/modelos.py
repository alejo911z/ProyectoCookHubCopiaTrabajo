from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class Dificultad(enum.Enum):
    Fácil = 1
    Medio = 2
    Difícil = 3


class TipoIngrediente(enum.Enum):
    Proteína = 1
    Carbohidrato = 2
    Vegetal = 3
    Lácteo = 4
    Fruta = 5
    Condimento = 6


class UnidadMedida(enum.Enum):
    Gramos = 1
    Kilogramos = 2
    Unidades = 3
    Litros = 4
    Mililitros = 5
    Cucharadas = 6


class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    descripcion = db.Column(db.String(256))
    tiempo_preparacion = db.Column(db.Integer)
    dificultad = db.Column(db.Enum(Dificultad))
    porciones = db.Column(db.Integer)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    ingrediente_principal = db.relationship('Ingrediente', back_populates='recetas')


class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    tipo = db.Column(db.Enum(TipoIngrediente))
    unidad_medida = db.Column(db.Enum(UnidadMedida))
    disponible = db.Column(db.Boolean, default=True)
    recetas = db.relationship('Receta', back_populates='ingrediente_principal')


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        return {
            'llave': value.name,
            'valor': value.value
        }


class EnumANombre(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        return value.name


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
