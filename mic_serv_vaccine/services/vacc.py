from flask import request, Response
from bson import json_util, ObjectId
from config.mongodb import mongo


"""Registro de vacunas"""


def create_vaccine_service():
    data = request.get_json()
    registro = data.get("registro", None)
    name = data.get("name")
    vacuna = data.get("vacuna", None)
    lote = data.get("lote", None)
    fecha = data.get("fecha", None)
    if registro:
        response = mongo.db.vaccines.insert_one(
            {
                "registro": registro,
                "name": name,
                "vacuna": vacuna,
                "lote": lote,
                "fecha": fecha,
                "status": False,
            }
        )
        result = {
            "id": str(response.inserted_id),
            "registro": registro,
            "name": name,
            "vacuna": vacuna,
            "lote": lote,
            "fecha": fecha,
            "status": False,
        }
        return result
    else:
        return "Invalid payload", 400


"""Obtiene las vacunas"""


def get_vaccines_service():
    data = mongo.db.vaccines.find()
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


"""Obtener una Vacuna"""


def get_vaccine_service(id):
    data = mongo.db.vaccines.find_one({"_id": ObjectId(id)})
    result = json_util.dumps(data)
    return Response(result, mimetype="application/json")


"""Actualizacion de vacuna"""


def update_vaccine_service(id):
    data = request.get_json()
    if len(data) == 0:
        return "No hay datos para actualizar", 400
    response = mongo.db.vaccines.update_one({"_id": ObjectId(id)}, {"$set": data})
    if response.modified_count >= 1:
        return "La vacuna ah sido actualizada correctamente", 200
    else:
        return "La vacuna no fue encontrada", 404


"""Eliminar una vacuna"""


def delete_vaccine_service(id):
    response = mongo.db.vaccines.delete_one({"_id": ObjectId(id)})
    if response.deleted_count >= 1:
        return "La vacuna ha sido eliminada correctamente", 200
    else:
        return "La vacuna no fue encontrada", 404


"""Generar Esquema"""


def create_schema_service():
    return {"message": "recived"}
