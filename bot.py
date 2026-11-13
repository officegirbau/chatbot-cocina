import random
import re
import uuid


RECETAS = {
    "tortilla de patatas": {
        "ingredientes": ["4 huevos", "3 patatas medianas", "1 cebolla", "aceite de oliva", "sal"],
        "pasos": [
            "Pela y corta las patatas en láminas finas.",
            "Fríelas a fuego medio con la cebolla picada hasta que estén tiernas.",
            "Bate los huevos con sal y mezcla con las patatas escurridas.",
            "Cuaja la tortilla en una sartén con poco aceite, 2-3 minutos por lado.",
        ],
        "tiempo_minutos": 30,
        "dificultad": "fácil",
    },
    "paella valenciana": {
        "ingredientes": [
            "400 g de arroz bomba",
            "500 g de pollo troceado",
            "300 g de conejo troceado",
            "judía verde plana",
            "garrofón",
            "tomate rallado",
            "azafrán",
            "pimentón dulce",
            "aceite de oliva",
        ],
        "pasos": [
            "Sofríe el pollo y el conejo en la paella con aceite.",
            "Añade la judía verde y el garrofón y sofríe unos minutos.",
            "Incorpora el tomate y el pimentón, remueve rápido.",
            "Vierte el agua (el triple que el arroz) y añade el azafrán.",
            "Cuando hierva 10 minutos, añade el arroz y cocina 18 minutos sin remover.",
            "Deja reposar 5 minutos antes de servir.",
        ],
        "tiempo_minutos": 70,
        "dificultad": "media",
    },
    "pasta carbonara": {
        "ingredientes": [
            "400 g de espaguetis",
            "150 g de guanciale o panceta",
            "4 yemas de huevo",
            "50 g de queso pecorino rallado",
            "pimienta negra",
        ],
        "pasos": [
            "Corta el guanciale en tiras y dóralo en sartén sin aceite.",
            "Cuece la pasta al dente según el paquete.",
            "Mezcla las yemas con el pecorino y mucha pimienta.",
            "Mezcla la pasta con el guanciale fuera del fuego, añade la salsa y un poco de agua de cocción.",
        ],
        "tiempo_minutos": 25,
        "dificultad": "fácil",
    },
    "gazpacho": {
        "ingredientes": [
            "1 kg de tomates maduros",
            "1 pepino pequeño",
            "1 pimiento verde",
            "1 diente de ajo",
            "40 ml de aceite de oliva",
            "vinagre",
            "sal",
        ],
        "pasos": [
            "Trocea y tritura todos los ingredientes hasta que quede fino.",
            "Añade el aceite en hilo mientras trituraste.",
            "Rectifica de sal y vinagre y enfría en la nevera 2 horas.",
        ],
        "tiempo_minutos": 15,
        "dificultad": "fácil",
    },
    "lentejas estofadas": {
        "ingredientes": [
            "400 g de lentejas",
            "1 cebolla",
            "2 zanahorias",
            "1 pimiento verde",
            "2 dientes de ajo",
            "1 cucharadita de pimentón",
            "laurel",
            "aceite de oliva",
        ],
        "pasos": [
            "Sofríe la cebolla, el pimiento y las zanahorias picadas.",
            "Añade el ajo y el pimentón, remueve rápido para que no se queme.",
            "Incorpora las lentejas y cúbrelas con agua fría (dos dedos por encima).",
            "Añade el laurel y cocina a fuego suave 40-50 minutos.",
        ],
        "tiempo_minutos": 60,
        "dificultad": "fácil",
    },
}

SUSTITUCIONES = {
    "huevo": "por cada huevo: 1 cucharada de linaza molida con 3 de agua, o 50 g de puré de manzana en repostería",
    "leche": "bebida de avena, soja o almendra en la misma cantidad",
    "mantequilla": "aceite de oliva (usa un 20% menos) o margarina vegetal",
    "nata": "crema de anacardos o yogur griego para salsas frías",
    "harina de trigo": "harina de arroz + almidón (50/50) sin gluten, o harina de avena",
    "azúcar": "miel (usa un 25% menos), dátiles triturados o stevia según el envase",
    "queso": "levadura nutricional para un sabor similar en salsas veganas",
    "vino blanco": "caldo de verduras con un chorrito de limón",
    "limón": "vinagre de manzana o lima en la misma cantidad",
    "ajo": "ajo en polvo (1/4 de cucharadita por diente) o cebollino",
}

CONSEJOS = [
    "Saca la mantequilla y los huevos de la nevera 30 minutos antes de hornear: se integran mejor.",
    "Prueba la comida mientras cocinas y ajusta la sal al final, nunca solo al principio.",
    "La sartén debe estar caliente antes de añadir el alimento, así no se pega.",
    "Deja reposar la carne 5-10 minutos tras cocinarla para que los jugos se repartan.",
    "Guarda el agua de cocción de la pasta: es oro líquido para ligar salsas.",
    "Afila los cuchillos: un cuchillo bien afilado es más seguro que uno romo.",
    "Añade el pimentón fuera del fuego para que no se queme y amargue.",
]

SALUDOS = ["hola", "buenas", "hey", "buenos días", "buenas tardes", "buenas noches"]
DESPEDIDAS = ["adiós", "adios", "hasta luego", "chao", "nos vemos", "bye"]
GRACIAS = ["gracias", "genial", "perfecto", "muchas gracias"]


def _normalizar(texto: str) -> str:
    return re.sub(r"\s+", " ", texto.lower().strip())


def _buscar_receta(texto: str):
    for nombre in RECETAS:
        if nombre in texto:
            return nombre
    for palabra, nombre in [
        ("tortilla", "tortilla de patatas"),
        ("paella", "paella valenciana"),
        ("carbonara", "pasta carbonara"),
        ("espaguetis", "pasta carbonara"),
        ("gazpacho", "gazpacho"),
        ("lenteja", "lentejas estofadas"),
    ]:
        if palabra in texto:
            return nombre
    return None


def responder(mensaje: str) -> str:
    texto = _normalizar(mensaje)

    if any(s in texto for s in SALUDOS) and len(texto) < 40:
        return (
            "¡Hola! Soy tu chef bot 👨‍🍳. Puedo darte recetas (prueba con «receta de tortilla»), "
            "ingredientes, tiempos de cocción, sustituciones («¿con qué sustituyo la nata?») o consejos de cocina."
        )

    if any(s in texto for s in DESPEDIDAS):
        return "¡Hasta pronto! Que aproveche 🍽️"

    if any(s in texto for s in GRACIAS) and len(texto) < 30:
        return "¡Un placer! Aquí estoy si necesitas otra receta."

    if "consejo" in texto or "truco" in texto or "tip" in texto:
        return f"Consejo del chef: {random.choice(CONSEJOS)}"

    receta = _buscar_receta(texto)
    if receta:
        datos = RECETAS[receta]
        if "ingrediente" in texto and "receta" not in texto:
            lista = ", ".join(datos["ingredientes"])
            return f"Para {receta} necesitas: {lista}."
        if "tiempo" in texto or "cuánto" in texto or "cuanto" in texto or "minutos" in texto or "tarda" in texto:
            return f"{receta.capitalize()} tarda unos {datos['tiempo_minutos']} minutos (dificultad: {datos['dificultad']})."
        if "dificultad" in texto or "complicado" in texto or "difícil" in texto or "dificil" in texto:
            return f"{receta.capitalize()} es de dificultad {datos['dificultad']}."
        if any(p in texto for p in ["paso", "cómo", "como", "preparar", "hacer", "receta"]):
            pasos = " ".join(f"{i}. {p}" for i, p in enumerate(datos["pasos"], 1))
            return (
                f"{receta.capitalize()} ({datos['tiempo_minutos']} min, {datos['dificultad']}).\n"
                f"Ingredientes: {', '.join(datos['ingredientes'])}.\n"
                f"Preparación: {pasos}"
            )
        return (
            f"Sobre {receta}: {datos['tiempo_minutos']} min, dificultad {datos['dificultad']}. "
            "Pídeme los ingredientes, los pasos o el tiempo."
        )

    for ingrediente, sustituto in SUSTITUCIONES.items():
        if ingrediente in texto and any(
            p in texto for p in ["sustituyo", "sustituir", "sustituto", "reemplazo", "reemplazar", "en vez de", "sin"]
        ):
            return f"Puedes sustituir {ingrediente} {sustituto}."

    if any(p in texto for p in ["receta", "qué cocino", "que cocino", "idea", "sugerencia", "cena", "comida"]):
        nombre = random.choice(list(RECETAS))
        datos = RECETAS[nombre]
        return (
            f"Te propongo: {nombre} ({datos['tiempo_minutos']} min, {datos['dificultad']}). "
            f"Ingredientes: {', '.join(datos['ingredientes'])}. ¿Quieres los pasos?"
        )

    if any(p in texto for p in ["ingrediente", "necesito"]):
        return "Dime de qué receta (tortilla, paella, carbonara, gazpacho o lentejas) y te doy sus ingredientes."

    return (
        "No estoy seguro de haberlo entendido 🤔. Puedo ayudarte con:\n"
        "• Recetas: «receta de paella»\n"
        "• Ingredientes: «ingredientes del gazpacho»\n"
        "• Tiempos: «cuánto tardan las lentejas»\n"
        "• Sustituciones: «¿con qué sustituyo el huevo?»\n"
        "• Consejos: «dame un consejo de cocina»"
    )


def sugerencias() -> list[str]:
    return [
        "Receta de tortilla de patatas",
        "¿Con qué sustituyo la nata?",
        "¿Cuánto tarda la paella?",
        "Dame un consejo de cocina",
    ]


def nueva_sesion() -> str:
    return uuid.uuid4().hex[:12]
