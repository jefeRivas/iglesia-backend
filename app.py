from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # 🔥 habilita CORS en toda la app


AREAS = {
    "domingo": ["sonido", "textos", "transmision", "camara1", "camara2"],
    "martes": ["sonido", "textos", "transmision", "camara1", "camara2"],
    "jueves": ["sonido", "textos", "transmision", "camara1", "camara2"]
}

AREAS = {
    "domingo": ["sonido", "textos", "transmision", "camara1", "camara2"],
    "martes": ["sonido", "textos", "transmision", "camara1", "camara2"],
    "jueves": ["sonido", "textos", "transmision", "camara1", "camara2"]
}

def generar_programacion(miembros):
    conteo_servicio = {nombre: 0 for nombre in miembros.keys()}
    programacion = {}

    for dia, areas in AREAS.items():
        programacion[dia] = {}
        disponibles = {n: d for n, d in miembros.items() if dia in d["dias"]}

        for area in areas:
            # ⚡ si el área es camara1 o camara2, buscamos candidatos en "camara"
            area_busqueda = "camara" if area.startswith("camara") else area

            candidatos = [
                n for n, d in disponibles.items()
                if area_busqueda in d["areas"]
            ]

            if candidatos:
                min_servicios = min(conteo_servicio[n] for n in candidatos)
                elegibles = [n for n in candidatos if conteo_servicio[n] == min_servicios]
                elegido = random.choice(elegibles)

                programacion[dia][area] = [elegido]
                conteo_servicio[elegido] += 1
                disponibles.pop(elegido, None)  # evitar que repita en el mismo día
            else:
                programacion[dia][area] = ["SIN ASIGNAR"]

    return programacion



@app.route("/programar", methods=["POST"])
def programar():
    miembros = request.json  # recibe el JSON de React (sin el campo activo)
    resultado = generar_programacion(miembros)
    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
