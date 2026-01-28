from flask import Flask, render_template, request

app = Flask(__name__)

# -----------------------
# UI Text
# -----------------------
UI_TEXT = {
    "title": {"en": "Cat Care Assistant", "es": "Asistente de Cuidado Felino"},
    "cat_name": {"en": "Cat name", "es": "Nombre del gato"},
    "age": {"en": "Age", "es": "Edad"},
    "years": {"en": "years", "es": "años"},
    "months": {"en": "months", "es": "meses"},
    "breed": {"en": "Breed", "es": "Raza"},
    "weight": {"en": "Weight (kg)", "es": "Peso (kg)"},
    "calculate": {"en": "Calculate", "es": "Calcular"},
    "human_age": {"en": "Human age equivalent:", "es": "Edad humana equivalente:"},
    "personality": {"en": "Personality", "es": "Personalidad"},
    "health": {"en": "Health", "es": "Salud"},
    "vet": {"en": "Veterinarian", "es": "Veterinario"},
    "weight_status": {"en": "Weight Status", "es": "Estado del Peso"},
    "ideal_weight": {"en": "Ideal weight range:", "es": "Rango de peso ideal:"},
    "feeding": {"en": "Feeding Recommendations", "es": "Recomendaciones de Alimentación"},
    "vaccinations": {"en": "Vaccination Schedule", "es": "Calendario de Vacunación"},
    "deworming": {"en": "Deworming Schedule", "es": "Calendario de Desparasitación"},
    "warning_signs": {"en": "Warning Signs to Watch", "es": "Señales de Alerta"},
    "spay_neuter": {"en": "Spay/Neuter Information", "es": "Información sobre Esterilización"},
    "disclaimer": {
        "en": "This info is for educational purposes and not a substitute for a veterinarian.",
        "es": "Esta información es educativa y no sustituye al veterinario."
    }
}

# -----------------------
# Cat Breeds
# -----------------------
CAT_BREEDS = {
    "Unknown / Mixed": {"en": "Mixed/Unknown", "es": "Mestizo/Desconocido", "weight": (3.5, 5.5),
                        "description": {"en": "Unique personality and appearance. Often healthy and adaptable.",
                                        "es": "Personalidad y apariencia únicas. A menudo saludables y adaptables."}},
    "Abyssinian": {"en": "Abyssinian", "es": "Abisinio", "weight": (3.0, 5.0),
                   "description": {"en": "Active, curious, and playful. Ticked coat gives unique appearance.",
                                   "es": "Activos, curiosos y juguetones. Pelaje moteado da apariencia única."}},
    "Bengal": {"en": "Bengal", "es": "Bengalí", "weight": (4.0, 7.0),
               "description": {"en": "Active, playful, with wild leopard-like appearance. Very energetic.",
                               "es": "Activos, juguetones, con apariencia salvaje de leopardo. Muy energéticos."}},
    "Bombay": {"en": "Bombay", "es": "Bombay", "weight": (3.0, 5.0),
               "description": {"en": "Sleek black coat, copper eyes, panther-like. Affectionate and social.",
                               "es": "Pelaje negro brillante, ojos cobrizos, como pantera. Cariñosos y sociales."}},
    "British Shorthair": {"en": "British Shorthair", "es": "Británico de Pelo Corto", "weight": (4.0, 7.0),
                          "description": {"en": "Easy-going, calm, with round face and dense coat. Independent yet affectionate.",
                                          "es": "Tranquilos, con cara redonda y pelaje denso. Independientes pero cariñosos."}},
    "Maine Coon": {"en": "Maine Coon", "es": "Maine Coon", "weight": (5.5, 9.0),
                   "description": {"en": "Gentle giants, sociable and playful. One of the largest domestic breeds.",
                                   "es": "Gigantes gentiles, sociables y juguetones. Una de las razas domésticas más grandes."}},
    "Persian": {"en": "Persian", "es": "Persa", "weight": (3.5, 5.5),
                "description": {"en": "Calm, gentle, with long luxurious coat. Requires daily grooming.",
                                "es": "Tranquilos, gentiles, con pelaje largo y lujoso. Requiere aseo diario."}},
    "Ragdoll": {"en": "Ragdoll", "es": "Ragdoll", "weight": (4.5, 9.0),
                "description": {"en": "Docile, gentle, and love to be held. Blue eyes and semi-long coat.",
                                "es": "Dóciles, gentiles y les encanta que los carguen. Ojos azules y pelaje semi-largo."}},
    "Siamese": {"en": "Siamese", "es": "Siamés", "weight": (2.5, 5.0),
                "description": {"en": "Vocal, social, and intelligent. Known for blue eyes and color-point coat.",
                                "es": "Vocales, sociales e inteligentes. Conocidos por ojos azules y pelaje con puntas de color."}},
    "Sphynx": {"en": "Sphynx", "es": "Esfinge", "weight": (3.0, 5.0),
               "description": {"en": "Hairless, warm to touch, very affectionate and social. Requires regular bathing.",
                               "es": "Sin pelo, cálidos al tacto, muy cariñosos y sociales. Requiere baños regulares."}}
}

# Sorted breed list for dropdown, unknown/mixed first
ALL_BREEDS = sorted([b for b in CAT_BREEDS.keys() if b != "Unknown / Mixed"])
ALL_BREEDS.insert(0, "Unknown / Mixed")

# -----------------------
# Helper Functions
# -----------------------
def cat_to_human_age(years, months=0):
    total_months = years * 12 + months
    if total_months <= 1:
        return 1
    elif total_months <= 12:
        return int(total_months * 1.25)
    elif total_months <= 24:
        return 15 + int((total_months - 12) * 0.75)
    else:
        return 24 + int((total_months - 24) / 3)

def get_life_stage(years, months=0):
    total_months = years * 12 + months
    if total_months < 12:
        return "kitten"
    elif total_months < 120:
        return "adult"
    else:
        return "senior"

def check_weight_status(weight, breed_key):
    if breed_key not in CAT_BREEDS:
        breed_key = "Unknown / Mixed"
    min_w, max_w = CAT_BREEDS[breed_key]["weight"]
    if weight < min_w * 0.9:
        return "underweight"
    elif weight > max_w * 1.1:
        return "overweight"
    else:
        return "healthy"

# -----------------------
# Main Route
# -----------------------
@app.route("/", methods=["GET", "POST"])
def home():
    lang = request.args.get("lang", "en")
    if lang not in ["en", "es"]:
        lang = "en"

    result = None
    if request.method == "POST":
        try:
            name = request.form["name"]
            years = int(request.form.get("years", 0))
            months = int(request.form.get("months", 0))
            breed = request.form.get("breed", "Unknown / Mixed")
            weight = float(request.form.get("weight", 0))

            human_age = cat_to_human_age(years, months)
            stage = get_life_stage(years, months)

            weight_status = check_weight_status(weight, breed)
            min_w, max_w = CAT_BREEDS[breed]["weight"]
            weight_message = {
                "underweight": {"en": "⚠️ Below ideal range. Consult vet.", "es": "⚠️ Por debajo del rango ideal. Consultar veterinario."},
                "healthy": {"en": "✅ Healthy weight!", "es": "✅ ¡Peso saludable!"},
                "overweight": {"en": "⚠️ Above ideal range. Consider diet adjustment.", "es": "⚠️ Por encima del rango ideal. Considerar ajuste de dieta."}
            }

            result = {
                "name": name,
                "human_age": human_age,
                "years": years,
                "months": months,
                "breed": CAT_BREEDS[breed][lang],
                "breed_description": CAT_BREEDS[breed]["description"][lang],
                "weight": weight,
                "weight_status": weight_status,
                "weight_message": weight_message[weight_status][lang],
                "ideal_weight": f"{min_w} - {max_w} kg"
            }
        except Exception as e:
            result = {"error": True, "error_message": str(e)}

    return render_template(
    "index.html",
    lang=lang,
    result=result,
    ui=UI_TEXT,
    breeds=CAT_BREEDS,   # <- pass the full dict for the template
    all_breeds=ALL_BREEDS  # <- optional, can use for Choices.js ordering
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)