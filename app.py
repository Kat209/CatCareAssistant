from flask import Flask, render_template, request

app = Flask(__name__)

# UI Text
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

# Cat Breeds
CAT_BREEDS = {
    "mixed": {
        "en": "Mixed/Unknown", "es": "Mestizo/Desconocido", "weight": (3.5, 5.5),
        "description": {"en": "Unique personality and appearance. Often healthy and adaptable.", "es": "Personalidad y apariencia únicas. A menudo saludables y adaptables."}
    },
    "siamese": {
        "en": "Siamese", "es": "Siamés", "weight": (2.5, 5.0),
        "description": {"en": "Vocal, social, and intelligent. Known for blue eyes and color-point coat.", "es": "Vocales, sociales e inteligentes. Conocidos por ojos azules y pelaje con puntas de color."}
    },
    "persian": {
        "en": "Persian", "es": "Persa", "weight": (3.5, 5.5),
        "description": {"en": "Calm, gentle, with long luxurious coat. Requires daily grooming.", "es": "Tranquilos, gentiles, con pelaje largo y lujoso. Requiere aseo diario."}
    },
    "maine_coon": {
        "en": "Maine Coon", "es": "Maine Coon", "weight": (5.5, 9.0),
        "description": {"en": "Gentle giants, sociable and playful. One of the largest domestic breeds.", "es": "Gigantes gentiles, sociables y juguetones. Una de las razas domésticas más grandes."}
    },
    "british_shorthair": {
        "en": "British Shorthair", "es": "Británico de Pelo Corto", "weight": (4.0, 7.0),
        "description": {"en": "Easy-going, calm, with round face and dense coat. Independent yet affectionate.", "es": "Tranquilos, con cara redonda y pelaje denso. Independientes pero cariñosos."}
    },
    "ragdoll": {
        "en": "Ragdoll", "es": "Ragdoll", "weight": (4.5, 9.0),
        "description": {"en": "Docile, gentle, and love to be held. Blue eyes and semi-long coat.", "es": "Dóciles, gentiles y les encanta que los carguen. Ojos azules y pelaje semi-largo."}
    },
    "bengal": {
        "en": "Bengal", "es": "Bengalí", "weight": (4.0, 7.0),
        "description": {"en": "Active, playful, with wild leopard-like appearance. Very energetic.", "es": "Activos, juguetones, con apariencia salvaje de leopardo. Muy energéticos."}
    },
    "abyssinian": {
        "en": "Abyssinian", "es": "Abisinio", "weight": (3.0, 5.0),
        "description": {"en": "Active, curious, and playful. Ticked coat gives unique appearance.", "es": "Activos, curiosos y juguetones. Pelaje moteado da apariencia única."}
    },
    "sphynx": {
        "en": "Sphynx", "es": "Esfinge", "weight": (3.0, 5.0),
        "description": {"en": "Hairless, warm to touch, very affectionate and social. Requires regular bathing.", "es": "Sin pelo, cálidos al tacto, muy cariñosos y sociales. Requiere baños regulares."}
    },
    "bombay": {
        "en": "Bombay", "es": "Bombay", "weight": (3.0, 5.0),
        "description": {"en": "Sleek black coat, copper eyes, panther-like. Affectionate and social.", "es": "Pelaje negro brillante, ojos cobrizos, como pantera. Cariñosos y sociales."}
    },
}

# Full Breed List for Dropdown (Alphabetical)
ALL_BREEDS = sorted([
    "Unknown / Mixed",
    "Abyssinian", "Aegean", "American Bobtail", "American Curl",
    "American Shorthair", "American Wirehair", "Balinese", "Bambino",
    "Bengal", "Birman", "Bombay", "British Longhair", "British Shorthair",
    "Burmese", "Burmilla", "Chartreux", "Chausie", "Colorpoint Shorthair",
    "Cornish Rex", "Cymric", "Devon Rex", "Donskoy", "Egyptian Mau",
    "European Burmese", "Exotic Shorthair", "German Rex", "Havana Brown",
    "Highlander", "Himalayan", "Japanese Bobtail", "Javanese", "Khao Manee",
    "Korat", "Kurilian Bobtail", "LaPerm", "Lykoi", "Maine Coon", "Manx",
    "Minskin", "Munchkin", "Nebelung", "Norwegian Forest Cat", "Ocicat",
    "Oriental Longhair", "Oriental Shorthair", "Persian", "Peterbald",
    "Pixiebob", "Ragamuffin", "Ragdoll", "Russian Blue", "Savannah",
    "Scottish Fold", "Selkirk Rex", "Serengeti", "Siamese", "Siberian",
    "Singapura", "Snowshoe", "Somali", "Sphynx", "Thai", "Tonkinese",
    "Toyger", "Turkish Angora", "Turkish Van", "Ukrainian Levkoy", "York Chocolate"
])

# Cat Info by Life Stage
CAT_INFO = {
    "kitten": {
        "en": {
            "personality": "Playful, curious, full of energy. Learning social skills and exploring their environment.",
            "health": "Watch for parasites, infections, and proper growth. Eyes, ears, and teeth need regular checking.",
            "vet": "Check-ups every 3–4 weeks during vaccination period. First visit at 6-8 weeks old.",
            "warning_signs": "⚠️ Lethargy, not eating, diarrhea for more than 24h, difficulty breathing, eye or nose discharge, not gaining weight"
        },
        "es": {
            "personality": "Juguetones, curiosos y llenos de energía. Aprendiendo habilidades sociales y explorando su entorno.",
            "health": "Vigilar parásitos, infecciones y desarrollo adecuado. Ojos, oídos y dientes necesitan revisión regular.",
            "vet": "Chequeos cada 3–4 semanas durante vacunación. Primera visita a las 6-8 semanas.",
            "warning_signs": "⚠️ Letargo, no come, diarrhea por más de 24h, dificultad para respirar, secreción ocular o nasal, no aumenta de peso"
        }
    },
    "adult": {
        "en": {
            "personality": "Calmer but active. Established routines and preferences. More independent.",
            "health": "Watch weight, dental health, and activity levels. Annual check-ups important.",
            "vet": "Annual check-up recommended. Dental cleaning as needed.",
            "warning_signs": "⚠️ Sudden weight changes, changes in eating/drinking habits, vomiting frequently, difficulty urinating, hiding more than usual"
        },
        "es": {
            "personality": "Más tranquilos pero activos. Rutinas y preferencias establecidas. Más independientes.",
            "health": "Controlar peso, salud dental y niveles de actividad. Chequeos anuales importantes.",
            "vet": "Chequeo anual recomendado. Limpieza dental según necesidad.",
            "warning_signs": "⚠️ Cambios súbitos de peso, cambios en hábitos de comida/bebida, vómitos frecuentes, dificultad al orinar, esconderse más de lo normal"
        }
    },
    "senior": {
        "en": {
            "personality": "Less active, may sleep more (up to 20h/day). May become more vocal or clingy.",
            "health": "Watch kidneys, teeth, mobility, and cognitive function. Common issues: arthritis, kidney disease, hyperthyroidism.",
            "vet": "Check-ups every 6 months recommended. Blood work annually to monitor organs.",
            "warning_signs": "⚠️ Confusion/disorientation, significant weight loss, excessive thirst, difficulty jumping, crying at night, not grooming"
        },
        "es": {
            "personality": "Menos activos, pueden dormir más (hasta 20h/día). Pueden volverse más vocales o apegados.",
            "health": "Vigilar riñones, dientes, movilidad y función cognitiva. Problemas comunes: artritis, enfermedad renal, hipertiroidismo.",
            "vet": "Chequeos cada 6 meses recomendados. Análisis de sangre anual para monitorear órganos.",
            "warning_signs": "⚠️ Confusión/desorientación, pérdida significativa de peso, sed excesiva, dificultad para saltar, llanto nocturno, no se acicala"
        }
    }
}

# Vaccination Schedule
VACCINATION_SCHEDULE = {
    "en": {"6-8 weeks": "First FVRCP", "10-12 weeks": "Second FVRCP booster", "14-16 weeks": "Third FVRCP booster + Rabies", "1 year": "FVRCP booster + Rabies booster", "Annual": "FVRCP every 1-3 years + Rabies per local laws"},
    "es": {"6-8 semanas": "Primera FVRCP", "10-12 semanas": "Segundo refuerzo FVRCP", "14-16 semanas": "Tercer refuerzo FVRCP + Rabia", "1 año": "Refuerzo FVRCP + Refuerzo rabia", "Anual": "FVRCP cada 1-3 años + Rabia según leyes locales"}
}

# Deworming Schedule
DEWORMING_SCHEDULE = {
    "en": {"kittens": "Every 2 weeks from 2-8 weeks old, then monthly until 6 months", "adults": "Every 3-6 months for outdoor cats, every 6-12 months for indoor cats", "seniors": "Every 3-6 months, adjusted based on lifestyle and health"},
    "es": {"gatitos": "Cada 2 semanas desde las 2-8 semanas, luego mensual hasta los 6 meses", "adultos": "Cada 3-6 meses para gatos de exterior, cada 6-12 meses para interiores", "mayores": "Cada 3-6 meses, ajustado según estilo de vida y salud"}
}

# Feeding Recommendations
FEEDING_RECOMMENDATIONS = {
    "kitten": {"en": "Feed 3-4 times daily. High-protein kitten food. Approximately 200-250 calories per day per kg of body weight.", "es": "Alimentar 3-4 veces al día. Comida para gatitos alta en proteínas. Aproximadamente 200-250 calorías por día por kg de peso corporal."},
    "adult": {"en": "Feed 2 times daily. Adult cat food with balanced nutrition. Approximately 200-300 calories total per day.", "es": "Alimentar 2 veces al día. Comida para gatos adultos con nutrición balanceada. Aproximadamente 200-300 calorías totales por día."},
    "senior": {"en": "Feed 2-3 times daily. Senior cat food (easier to digest, joint support). Approximately 180-220 calories per day.", "es": "Alimentar 2-3 veces al día. Comida para gatos mayores. Aproximadamente 180-220 calorías por día."}
}

# Spay/Neuter Info
SPAY_NEUTER_INFO = {
    "en": {"timing": "Recommended between 4-6 months of age.", "benefits": "Prevents unwanted pregnancies, reduces cancer risk, decreases spraying.", "recovery": "Usually 7-10 days. Keep cat calm, monitor incision."},
    "es": {"timing": "Recomendado entre 4-6 meses de edad.", "benefits": "Previene embarazos no deseados, reduce riesgo de cáncer, disminuye marcaje.", "recovery": "Usualmente 7-10 días. Mantener tranquilo, monitorear incisión."}
}

# Helper Functions
def normalize_breed_key(breed_name):
    """Convert breed display name to dictionary key"""
    breed_map = {
        "Unknown / Mixed": "mixed",
        "Maine Coon": "maine_coon",
        "British Shorthair": "british_shorthair",
        "Siamese": "siamese",
        "Persian": "persian",
        "Ragdoll": "ragdoll",
        "Bengal": "bengal",
        "Abyssinian": "abyssinian",
        "Sphynx": "sphynx",
        "Bombay": "bombay"
    }
    return breed_map.get(breed_name, "mixed")

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
        breed_key = "mixed"
    min_weight, max_weight = CAT_BREEDS[breed_key]["weight"]
    if weight < min_weight * 0.9:
        return "underweight"
    elif weight > max_weight * 1.1:
        return "overweight"
    else:
        return "healthy"

def get_vaccination_info(years, months, lang):
    total_months = years * 12 + months
    if lang == "en":
        if total_months < 5:
            return VACCINATION_SCHEDULE["en"]["6-8 weeks"]
        elif total_months < 11:
            return VACCINATION_SCHEDULE["en"]["10-12 weeks"]
        elif total_months < 17:
            return VACCINATION_SCHEDULE["en"]["14-16 weeks"]
        elif total_months < 18:
            return VACCINATION_SCHEDULE["en"]["1 year"]
        else:
            return VACCINATION_SCHEDULE["en"]["Annual"]
    else:
        if total_months < 5:
            return VACCINATION_SCHEDULE["es"]["6-8 semanas"]
        elif total_months < 11:
            return VACCINATION_SCHEDULE["es"]["10-12 semanas"]
        elif total_months < 17:
            return VACCINATION_SCHEDULE["es"]["14-16 semanas"]
        elif total_months < 18:
            return VACCINATION_SCHEDULE["es"]["1 año"]
        else:
            return VACCINATION_SCHEDULE["es"]["Anual"]

def get_deworming_info(years, months, lang):
    total_months = years * 12 + months
    if lang == "en":
        if total_months < 7:
            return DEWORMING_SCHEDULE["en"]["kittens"]
        elif total_months < 120:
            return DEWORMING_SCHEDULE["en"]["adults"]
        else:
            return DEWORMING_SCHEDULE["en"]["seniors"]
    else:
        if total_months < 7:
            return DEWORMING_SCHEDULE["es"]["gatitos"]
        elif total_months < 120:
            return DEWORMING_SCHEDULE["es"]["adultos"]
        else:
            return DEWORMING_SCHEDULE["es"]["mayores"]

# Main Route
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
            
            # Convert breed name to key for lookup
            breed_key = normalize_breed_key(breed)
            
            human_age = cat_to_human_age(years, months)
            stage = get_life_stage(years, months)
            info = CAT_INFO[stage][lang]
            
            weight_status = check_weight_status(weight, breed_key)
            min_w, max_w = CAT_BREEDS[breed_key]["weight"]
            
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
                "breed": CAT_BREEDS[breed_key][lang],
                "breed_description": CAT_BREEDS[breed_key]["description"][lang],
                "weight": weight,
                "weight_status": weight_status,
                "weight_message": weight_message[weight_status][lang],
                "ideal_weight": f"{min_w} - {max_w} kg",
                "info": info,
                "feeding": FEEDING_RECOMMENDATIONS[stage][lang],
                "vaccination": get_vaccination_info(years, months, lang),
                "deworming": get_deworming_info(years, months, lang),
                "spay_neuter": SPAY_NEUTER_INFO[lang]
            }
        except Exception as e:
            import traceback
            print(f"Error: {e}")
            print(traceback.format_exc())
            result = {"error": True, "error_message": str(e)}
    
    return render_template(
        "index.html",
        lang=lang,
        result=result,
        ui=UI_TEXT,
        breeds=CAT_BREEDS,        # for medical logic
        all_breeds=ALL_BREEDS     # for dropdown
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)