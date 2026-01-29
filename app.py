from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Groq API Configuration - Añade tu API key aquí
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")  # O pon tu key directamente: "gsk_..."
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# UI Text
UI_TEXT = {
    "title": {"en": "Cat Care Assistant", "es": "Asistente de Cuidado Felino"},
    "cat_name": {"en": "Cat name", "es": "Nombre del gato"},
    "age": {"en": "Age", "es": "Edad"},
    "years": {"en": "years", "es": "años"},
    "months": {"en": "months", "es": "meses"},
    "breed": {"en": "Breed", "es": "Raza"},
    "weight": {"en": "Weight (kg)", "es": "Peso (kg)"},
    "spayed_neutered": {"en": "Is your cat spayed/neutered?", "es": "¿Está esterilizado tu gato?"},
    "yes": {"en": "Yes", "es": "Sí"},
    "no": {"en": "No", "es": "No"},
    "calculate": {"en": "Calculate", "es": "Calcular"},
    "human_age": {"en": "Human age equivalent:", "es": "Edad humana equivalente:"},
    "personality": {"en": "Personality", "es": "Personalidad"},
    "health": {"en": "Health", "es": "Salud"},
    "vet": {"en": "Veterinarian", "es": "Veterinario"},
    "weight_status": {"en": "Weight Status", "es": "Estado del Peso"},
    "ideal_weight": {"en": "Ideal weight range:", "es": "Rango de peso ideal:"},
    "feeding": {"en": "Feeding Recommendations", "es": "Recomendaciones de Alimentación"},
    "feeding_frequency": {"en": "Feeding frequency:", "es": "Frecuencia de alimentación:"},
    "food_type": {"en": "Food type:", "es": "Tipo de comida:"},
    "daily_calories": {"en": "Daily calories:", "es": "Calorías diarias:"},
    "daily_grams": {"en": "Daily amount (grams):", "es": "Cantidad diaria (gramos):"},
    "vaccinations": {"en": "Vaccination Schedule", "es": "Calendario de Vacunación"},
    "deworming": {"en": "Deworming Schedule", "es": "Calendario de Desparasitación"},
    "warning_signs": {"en": "Warning Signs to Watch", "es": "Señales de Alerta"},
    "games": {"en": "Age-Appropriate Games & Activities", "es": "Juegos y Actividades Apropiados para su Edad"},
    "spay_neuter": {"en": "Spay/Neuter Information", "es": "Información sobre Esterilización"},
    "daily_tip": {"en": "Get Daily Tip", "es": "Obtener Consejo del Día"},
    "daily_tip_title": {"en": "💡 Personalized Tip for", "es": "💡 Consejo Personalizado para"},
    "generating": {"en": "Generating tip...", "es": "Generando consejo..."},
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
    "russian_blue": {
        "en": "Russian Blue", "es": "Azul Ruso", "weight": (3.0, 5.5),
        "description": {"en": "Quiet, gentle with silvery-blue coat. Loyal and reserved with strangers.", "es": "Tranquilos, gentiles con pelaje azul plateado. Leales y reservados con extraños."}
    },
    "birman": {
        "en": "Birman", "es": "Birmano", "weight": (3.5, 6.5),
        "description": {"en": "Gentle, affectionate with color-point coat and white paws. Very social.", "es": "Gentiles, cariñosos con pelaje color point y patas blancas. Muy sociables."}
    },
    "scottish_fold": {
        "en": "Scottish Fold", "es": "Scottish Fold", "weight": (3.0, 6.0),
        "description": {"en": "Sweet-natured with unique folded ears. Adaptable and affectionate.", "es": "De naturaleza dulce con orejas dobladas únicas. Adaptables y cariñosos."}
    },
    "american_shorthair": {
        "en": "American Shorthair", "es": "Americano de Pelo Corto", "weight": (3.5, 7.0),
        "description": {"en": "Easy-going, healthy, adaptable. Great family cats with hunting instincts.", "es": "Tranquilos, saludables, adaptables. Excelentes gatos familiares con instintos cazadores."}
    },
    "exotic_shorthair": {
        "en": "Exotic Shorthair", "es": "Exótico de Pelo Corto", "weight": (3.5, 6.0),
        "description": {"en": "Calm like Persians but with short coat. Playful and affectionate.", "es": "Tranquilos como los persas pero con pelo corto. Juguetones y cariñosos."}
    },
    "norwegian_forest_cat": {
        "en": "Norwegian Forest Cat", "es": "Gato del Bosque de Noruega", "weight": (4.5, 9.0),
        "description": {"en": "Large, sturdy with thick water-resistant coat. Friendly and patient.", "es": "Grandes, robustos con pelaje grueso resistente al agua. Amigables y pacientes."}
    },
    "siberian": {
        "en": "Siberian", "es": "Siberiano", "weight": (4.5, 9.0),
        "description": {"en": "Strong, agile with triple-layer coat. Hypoallergenic and dog-like personality.", "es": "Fuertes, ágiles con pelaje de triple capa. Hipoalergénicos con personalidad canina."}
    },
    "burmese": {
        "en": "Burmese", "es": "Burmés", "weight": (3.5, 6.0),
        "description": {"en": "Social, playful, dog-like loyalty. Muscular with silky coat.", "es": "Sociales, juguetones, lealtad tipo perro. Musculosos con pelaje sedoso."}
    },
    "oriental_shorthair": {
        "en": "Oriental Shorthair", "es": "Oriental de Pelo Corto", "weight": (3.0, 5.5),
        "description": {"en": "Elegant, intelligent, very vocal. Related to Siamese with many colors.", "es": "Elegantes, inteligentes, muy vocales. Relacionados con siameses con muchos colores."}
    },
    "tonkinese": {
        "en": "Tonkinese", "es": "Tonkinés", "weight": (3.0, 5.5),
        "description": {"en": "Active, social, affectionate. Cross between Siamese and Burmese.", "es": "Activos, sociales, cariñosos. Cruce entre siamés y burmés."}
    },
}

# Full Breed List for Dropdown (with Spanish translations and Unknown/Mixed at top)
ALL_BREEDS_EN = [
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
]

ALL_BREEDS_ES = [
    "Desconocido / Mestizo",
] + sorted([
    "Abisinio", "Egeo", "Americano de Pelo Corto", "Americano de Pelo Duro",
    "American Curl", "Angora Turco", "Azul Ruso", "Balinés", "Bambino",
    "Bengalí", "Birmano", "Bobtail Americano", "Bobtail de las Kuriles",
    "Bobtail Japonés", "Bombay", "Británico de Pelo Corto", "Británico de Pelo Largo",
    "Burmés", "Burmés Europeo", "Burmilla", "Chartreux", "Chausie",
    "Colorpoint de Pelo Corto", "Cornish Rex", "Cymric", "Devon Rex", "Donskoy",
    "Esfinge", "Exótico de Pelo Corto", "Gato del Bosque de Noruega",
    "Havana Brown", "Highlander", "Himalayo", "Javanés", "Khao Manee",
    "Korat", "LaPerm", "Levkoy Ucraniano", "Lykoi", "Maine Coon", "Manx",
    "Mau Egipcio", "Minskin", "Munchkin", "Nebelung", "Ocicat",
    "Oriental de Pelo Corto", "Oriental de Pelo Largo", "Persa", "Peterbald",
    "Pixiebob", "Ragamuffin", "Ragdoll", "Rex Alemán", "Savannah",
    "Scottish Fold", "Selkirk Rex", "Serengeti", "Siamés", "Siberiano",
    "Singapura", "Snowshoe", "Somalí", "Thai", "Tonkinés",
    "Toyger", "Van Turco", "York Chocolate"
])

ALL_BREEDS = {
    "en": ALL_BREEDS_EN,
    "es": ALL_BREEDS_ES
}

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
            "warning_signs": "⚠️ Letargo, no come, diarrea por más de 24h, dificultad para respirar, secreción ocular o nasal, no aumenta de peso"
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

# Feeding Recommendations (detailed with bullet points)
FEEDING_RECOMMENDATIONS = {
    "kitten": {
        "en": {
            "frequency": "3-4 times daily",
            "food_type": "High-protein kitten food (dry or wet)",
            "calories": "200-250 calories per day per kg of body weight",
            "grams": "50-75 grams per kg of body weight (varies by food brand)"
        },
        "es": {
            "frequency": "3-4 veces al día",
            "food_type": "Comida para gatitos alta en proteínas (seca o húmeda)",
            "calories": "200-250 calorías por día por kg de peso corporal",
            "grams": "50-75 gramos por kg de peso corporal (varía según la marca)"
        }
    },
    "adult": {
        "en": {
            "frequency": "2 times daily",
            "food_type": "Adult cat food with balanced nutrition",
            "calories": "200-300 calories total per day (adjust for activity level)",
            "grams": "40-60 grams per day (for average 4-5kg cat)"
        },
        "es": {
            "frequency": "2 veces al día",
            "food_type": "Comida para gatos adultos con nutrición balanceada",
            "calories": "200-300 calorías totales por día (ajustar según actividad)",
            "grams": "40-60 gramos por día (para gato promedio de 4-5kg)"
        }
    },
    "senior": {
        "en": {
            "frequency": "2-3 times daily (smaller portions)",
            "food_type": "Senior cat food (easier to digest, joint support)",
            "calories": "180-220 calories per day",
            "grams": "35-50 grams per day (for average senior cat)"
        },
        "es": {
            "frequency": "2-3 veces al día (porciones más pequeñas)",
            "food_type": "Comida para gatos mayores (más fácil de digerir, apoyo articular)",
            "calories": "180-220 calorías por día",
            "grams": "35-50 gramos por día (para gato mayor promedio)"
        }
    }
}

# Age-Appropriate Games and Activities
GAMES_ACTIVITIES = {
    "kitten": {
        "en": {
            "min_playtime": "60-90 minutes per day (in short 10-15 minute sessions)",
            "activities": [
                "🎾 Chasing toys (feather wands, balls)",
                "🧶 String and ribbon play (always supervised)",
                "📦 Exploring boxes and tunnels",
                "🎯 Laser pointer games (always end with catchable toy)",
                "🧩 Simple puzzle feeders",
                "👥 Socialization with people and other pets",
                "🪴 Safe climbing structures",
                "💤 Rest periods between play (kittens tire quickly)"
            ]
        },
        "es": {
            "min_playtime": "60-90 minutos por día (en sesiones cortas de 10-15 minutos)",
            "activities": [
                "🎾 Perseguir juguetes (varitas con plumas, pelotas)",
                "🧶 Jugar con cuerdas y cintas (siempre supervisado)",
                "📦 Explorar cajas y túneles",
                "🎯 Juegos con puntero láser (siempre terminar con juguete capturable)",
                "🧩 Comederos tipo puzzle simples",
                "👥 Socialización con personas y otras mascotas",
                "🪴 Estructuras seguras para trepar",
                "💤 Períodos de descanso entre juegos (los gatitos se cansan rápido)"
            ]
        }
    },
    "adult": {
        "en": {
            "min_playtime": "30-45 minutes per day (2-3 sessions)",
            "activities": [
                "🎣 Interactive fishing rod toys",
                "🏃 Chase games (10-15 min sessions)",
                "🧠 Puzzle feeders and treat-dispensing toys",
                "🎾 Ball and mouse toys",
                "📦 Cardboard boxes for hiding",
                "🌿 Cat grass and safe plants to explore",
                "🧗 Cat trees and vertical spaces",
                "🎯 Hunting simulation games",
                "🪟 Window perches for bird watching"
            ]
        },
        "es": {
            "min_playtime": "30-45 minutos por día (2-3 sesiones)",
            "activities": [
                "🎣 Juguetes interactivos tipo caña de pescar",
                "🏃 Juegos de persecución (sesiones de 10-15 min)",
                "🧠 Comederos tipo puzzle y juguetes dispensadores de premios",
                "🎾 Pelotas y ratones de juguete",
                "📦 Cajas de cartón para esconderse",
                "🌿 Hierba gatera y plantas seguras para explorar",
                "🧗 Árboles para gatos y espacios verticales",
                "🎯 Juegos de simulación de caza",
                "🪟 Perchas en ventanas para observar pájaros"
            ]
        }
    },
    "senior": {
        "en": {
            "min_playtime": "15-20 minutes per day (multiple short sessions)",
            "activities": [
                "🐢 Gentle play sessions (5-10 minutes each)",
                "🧸 Soft toys they can bat around",
                "🧠 Food puzzles (easier difficulty)",
                "🪟 Comfortable window perches",
                "🌞 Warm, accessible resting spots",
                "🤲 Gentle petting and grooming sessions",
                "📻 Calm background sounds",
                "🎾 Slow-moving toys",
                "⚠️ Avoid high jumps - provide ramps/steps"
            ]
        },
        "es": {
            "min_playtime": "15-20 minutos por día (múltiples sesiones cortas)",
            "activities": [
                "🐢 Sesiones de juego suaves (5-10 minutos cada una)",
                "🧸 Juguetes suaves que puedan golpear",
                "🧠 Rompecabezas de comida (dificultad más fácil)",
                "🪟 Perchas cómodas en ventanas",
                "🌞 Lugares cálidos y accesibles para descansar",
                "🤲 Sesiones suaves de caricias y aseo",
                "📻 Sonidos de fondo tranquilos",
                "🎾 Juguetes de movimiento lento",
                "⚠️ Evitar saltos altos - proporcionar rampas/escalones"
            ]
        }
    }
}

# Spay/Neuter Info
SPAY_NEUTER_INFO = {
    "en": {"timing": "Recommended between 4-6 months of age.", "benefits": "Prevents unwanted pregnancies, reduces cancer risk, decreases spraying.", "recovery": "Usually 7-10 days. Keep cat calm, monitor incision."},
    "es": {"timing": "Recomendado entre 4-6 meses de edad.", "benefits": "Previene embarazos no deseados, reduce riesgo de cáncer, disminuye marcaje.", "recovery": "Usualmente 7-10 días. Mantener tranquilo, monitorear incisión."}
}

# Helper Functions
def get_breed_specific_games(breed_key, stage, lang):
    """Get games tailored to breed characteristics"""
    breed_traits = {
        "bengal": {
            "en": "🏃‍♂️ EXTRA: High-energy breed - ADD 15-30 minutes of vigorous play daily!", 
            "es": "🏃‍♂️ EXTRA: Raza muy energética - ¡AÑADIR 15-30 minutos de juego vigoroso diario!"
        },
        "siamese": {
            "en": "🗣️ EXTRA: Very vocal and social - interactive toys and conversation time!", 
            "es": "🗣️ EXTRA: Muy vocal y social - ¡juguetes interactivos y tiempo de conversación!"
        },
        "persian": {
            "en": "😌 EXTRA: Calm breed - gentle play is enough, avoid overexertion", 
            "es": "😌 EXTRA: Raza tranquila - juego suave es suficiente, evitar exceso de ejercicio"
        },
        "maine_coon": {
            "en": "🦁 EXTRA: Large and playful - sturdy toys and water play recommended!", 
            "es": "🦁 EXTRA: Grande y juguetón - ¡juguetes resistentes y juegos con agua recomendados!"
        },
        "sphynx": {
            "en": "🌡️ EXTRA: Hairless - keep warm during play, loves human interaction", 
            "es": "🌡️ EXTRA: Sin pelo - mantener caliente durante el juego, ama la interacción humana"
        },
        "abyssinian": {
            "en": "🔍 EXTRA: Very curious - puzzle toys and exploring new things daily!", 
            "es": "🔍 EXTRA: Muy curioso - ¡juguetes tipo puzzle y explorar cosas nuevas diariamente!"
        },
    }
    
    base_games = GAMES_ACTIVITIES[stage][lang]
    breed_addition = breed_traits.get(breed_key, {}).get(lang, "")
    
    # Add breed-specific note to activities list if exists
    activities = base_games["activities"].copy()
    if breed_addition:
        activities.append(breed_addition)
    
    return {
        "min_playtime": base_games["min_playtime"],
        "activities": activities
    }

def normalize_breed_key(breed_name, lang="en"):
    """Convert breed display name to dictionary key"""
    normalized = breed_name.lower().replace(" / ", "_").replace("/", "_").replace(" ", "_").replace("-", "_")
    
    breed_map = {
        "unknown_mixed": "mixed",
        "desconocido_mestizo": "mixed",
        "maine_coon": "maine_coon",
        "british_shorthair": "british_shorthair",
        "británico_de_pelo_corto": "british_shorthair",
        "siamese": "siamese",
        "siamés": "siamese",
        "persian": "persian",
        "persa": "persian",
        "ragdoll": "ragdoll",
        "bengal": "bengal",
        "bengalí": "bengal",
        "abyssinian": "abyssinian",
        "abisinio": "abyssinian",
        "sphynx": "sphynx",
        "esfinge": "sphynx",
        "bombay": "bombay",
        "russian_blue": "russian_blue",
        "azul_ruso": "russian_blue",
        "birman": "birman",
        "birmano": "birman",
        "scottish_fold": "scottish_fold",
        "american_shorthair": "american_shorthair",
        "americano_de_pelo_corto": "american_shorthair",
        "exotic_shorthair": "exotic_shorthair",
        "exótico_de_pelo_corto": "exotic_shorthair",
        "norwegian_forest_cat": "norwegian_forest_cat",
        "gato_del_bosque_de_noruega": "norwegian_forest_cat",
        "siberian": "siberian",
        "siberiano": "siberian",
        "burmese": "burmese",
        "burmés": "burmese",
        "oriental_shorthair": "oriental_shorthair",
        "oriental_de_pelo_corto": "oriental_shorthair",
        "tonkinese": "tonkinese",
        "tonkinés": "tonkinese",
    }
    
    result = breed_map.get(normalized)
    
    if result and result in CAT_BREEDS:
        return result
    
    return "mixed"

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
    
    if weight < min_weight:
        return "underweight"
    elif weight > max_weight:
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
            breed = request.form.get("breed", ALL_BREEDS[lang][0])
            weight = float(request.form.get("weight", 0))
            is_spayed = request.form.get("spayed_neutered", "no") == "yes"
            
            breed_key = normalize_breed_key(breed, lang)
            
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
                "games": get_breed_specific_games(breed_key, stage, lang),
                "vaccination": get_vaccination_info(years, months, lang),
                "deworming": get_deworming_info(years, months, lang),
                "is_spayed": is_spayed,
                "spay_neuter": SPAY_NEUTER_INFO[lang] if not is_spayed else None,
                "stage": stage
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
        breeds=CAT_BREEDS,
        all_breeds=ALL_BREEDS[lang],
        groq_enabled=groq_client is not None
    )

@app.route("/daily-tip", methods=["POST"])
def daily_tip():
    """Generate a personalized daily tip using Groq AI"""
    if not groq_client:
        return jsonify({"error": "Groq API not configured", "success": False}), 500
    
    try:
        data = request.get_json()
        cat_name = data.get("name", "your cat")
        breed = data.get("breed", "Mixed")
        age_years = data.get("years", 0)
        age_months = data.get("months", 0)
        weight = data.get("weight", 0)
        weight_status = data.get("weight_status", "healthy")
        stage = data.get("stage", "adult")
        is_spayed = data.get("is_spayed", False)
        lang = data.get("lang", "en")
        
        # Build prompt
        if lang == "es":
            prompt = f"""Genera UN SOLO consejo práctico y personalizado para el cuidado de {cat_name}, un gato {breed} de {age_years} años y {age_months} meses que pesa {weight}kg (estado: {weight_status}).

Etapa de vida: {stage}
Esterilizado: {'Sí' if is_spayed else 'No'}

El consejo debe ser:
- Específico para esta raza y edad
- Práctico y fácil de implementar HOY
- Máximo 3-4 líneas
- Amigable y motivador
- Enfocado en UN solo tema (juego, nutrición, salud, o comportamiento)

No uses formato de lista, solo escribe el consejo directo."""
        else:
            prompt = f"""Generate ONE practical, personalized care tip for {cat_name}, a {breed} cat who is {age_years} years and {age_months} months old, weighing {weight}kg (status: {weight_status}).

Life stage: {stage}
Spayed/Neutered: {'Yes' if is_spayed else 'No'}

The tip should be:
- Specific to this breed and age
- Practical and actionable TODAY
- Maximum 3-4 lines
- Friendly and motivating
- Focused on ONE topic (play, nutrition, health, or behavior)

Don't use list format, just write the tip directly."""
        
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful cat care expert who gives concise, practical daily tips."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.8,
            max_tokens=200
        )
        
        tip = chat_completion.choices[0].message.content.strip()
        
        return jsonify({
            "tip": tip,
            "success": True
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)