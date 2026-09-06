import os

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from modelos import db
from vistas import (
    VistaRecetas,
    VistaReceta,
    VistaIngredientes,
    VistaIngrediente,
    VistaReporteIngredientes,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "cookhub-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "COOKHUB_DATABASE_URL", "sqlite:///cookhub.db"
)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)

# Rutas para recetas
api.add_resource(VistaRecetas, "/api/recetas")
api.add_resource(VistaReceta, "/api/recetas/<int:id_receta>")

# Rutas para ingredientes
api.add_resource(VistaIngredientes, "/api/ingredientes")
api.add_resource(VistaIngrediente, "/api/ingredientes/<int:id_ingrediente>")

# Ruta para reportes
api.add_resource(VistaReporteIngredientes, "/api/reportes/ingredientes")

if __name__ == "__main__":
    print("👨‍🍳 CookHub Backend iniciado en http://localhost:5001")
    print("📊 Endpoints disponibles:")
    print("   GET/POST /api/recetas")
    print("   GET/PUT/DELETE /api/recetas/<id>")
    print("   GET/POST /api/ingredientes")
    print("   GET/PUT/DELETE /api/ingredientes/<id>")
    print("   GET /api/reportes/ingredientes")
    app.run(debug=True, port=5001)
