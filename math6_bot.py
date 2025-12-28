import telebot
from sympy import (
    symbols, sympify, solve, diff, integrate,
    limit, simplify
)

# 🔑 TOKEN
TOKEN = "8502618334:AAH4NQJT6psrlnrSBzI3_AdL2QObdKRjcF8"
bot = telebot.TeleBot(TOKEN)

x = symbols('x')

# ======================
# PRÉSENTATION
# ======================
PRESENTATION = (
    "🤖 BOT SOLVEUR MATH – MODE LYCÉE AVANCÉ\n\n"
    "Je résous et j’explique les mathématiques\n"
    "**ligne par ligne**, comme un professeur.\n\n"
    "📘 Niveau : Lycée\n"
    "👨‍💻 Développé par **Beya Mutungilay Light**\n"
)

# ======================
# CALCULS SIMPLES (TRÈS DÉTAILLÉ)
# ======================
def calcul_simple(expr):
    etapes = []
    etapes.append(f"📘 Expression donnée : {expr}")
    etapes.append("📐 Étape 1 : On applique les priorités opératoires")
    etapes.append("   - Parenthèses")
    etapes.append("   - Multiplication et division")
    etapes.append("   - Addition et soustraction")
    resultat = simplify(sympify(expr))
    etapes.append(f"📐 Étape 2 : Calcul du résultat")
    etapes.append(f"✅ Résultat final : {resultat}")
    return "\n".join(etapes)

# ======================
# ÉQUATIONS (TRÈS DÉTAILLÉ)
# ======================
def resoudre_equation(texte):
    etapes = []
    gauche, droite = texte.replace(" ", "").split("=")

    etapes.append(f"📘 Équation donnée : {gauche} = {droite}")
    etapes.append("📐 Ligne 1 : On ramène tout du même côté")
    expr = sympify(gauche) - sympify(droite)
    etapes.append(f"➡️ {expr} = 0")

    degre = expr.as_poly(x).degree()
    etapes.append(f"📐 Ligne 2 : Le degré de l’équation est {degre}")

    if degre == 1:
        etapes.append("📐 Ligne 3 : Équation du premier degré")
        sol = solve(expr, x)[0]
        etapes.append("📐 Ligne 4 : On isole x")
        etapes.append(f"✅ Solution : x = {sol}")

    elif degre == 2:
        etapes.append("📐 Ligne 3 : Équation du second degré")
        a, b, c = expr.as_poly(x).all_coeffs()
        etapes.append(f"📐 Ligne 4 : a={a}, b={b}, c={c}")
        delta = b**2 - 4*a*c
        etapes.append(f"📐 Ligne 5 : Δ = b² - 4ac = {delta}")

        if delta > 0:
            etapes.append("📐 Ligne 6 : Δ > 0 donc deux solutions")
        elif delta == 0:
            etapes.append("📐 Ligne 6 : Δ = 0 donc une solution")
        else:
            etapes.append("📐 Ligne 6 : Δ < 0 donc aucune solution réelle")

        sols = solve(expr, x)
        etapes.append(f"✅ Solutions : {sols}")

    return "\n".join(etapes)

# ======================
# TRIGONOMÉTRIE
# ======================
def trigonometrie(expr):
    etapes = []
    etapes.append(f"📘 Expression trigonométrique : {expr}")
    etapes.append("📐 Rappels lycée : sin(x), cos(x), tan(x)")
    resultat = simplify(sympify(expr))
    etapes.append(f"✅ Résultat : {resultat}")
    return "\n".join(etapes)

# ======================
# DÉRIVÉE
# ======================
def derivation(expr):
    etapes = []
    etapes.append(f"📘 Fonction : f(x) = {expr}")
    etapes.append("📐 Ligne 1 : On applique la règle de dérivation")
    etapes.append("(xⁿ)' = n·xⁿ⁻¹")
    resultat = diff(sympify(expr), x)
    etapes.append(f"📐 Ligne 2 : Calcul")
    etapes.append(f"✅ f'(x) = {resultat}")
    return "\n".join(etapes)

# ======================
# INTÉGRALE
# ======================
def integration(expr):
    etapes = []
    etapes.append(f"📘 Fonction : {expr}")
    etapes.append("📐 Ligne 1 : Une intégrale est une primitive")
    etapes.append("∫xⁿ dx = xⁿ⁺¹ / (n+1)")
    resultat = integrate(sympify(expr), x)
    etapes.append(f"📐 Ligne 2 : Calcul")
    etapes.append(f"✅ Primitive : {resultat} + C")
    return "\n".join(etapes)

# ======================
# LIMITE
# ======================
def calcul_limite(expr, val):
    etapes = []
    etapes.append(f"📘 Limite de {expr} quand x → {val}")
    etapes.append("📐 Ligne 1 : On remplace x par la valeur")
    resultat = limit(sympify(expr), x, sympify(val))
    etapes.append(f"✅ Limite = {resultat}")
    return "\n".join(etapes)

# ======================
# TELEGRAM
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        PRESENTATION +
        "\n📌 Commandes :\n"
        "➕ Calcul : 2+3*4\n"
        "📐 Équation : x**2-5*x+6=0\n"
        "📉 Dérivée : deriv x**2\n"
        "📈 Intégrale : integ x**2\n"
        "📊 Limite : lim 1/x 0\n"
        "📐 Trigo : trig sin(x)**2\n"
    )

@bot.message_handler(func=lambda message: True)
def handle(message):
    try:
        txt = message.text.lower()

        if txt.startswith("deriv"):
            rep = derivation(txt.replace("deriv", ""))

        elif txt.startswith("integ"):
            rep = integration(txt.replace("integ", ""))

        elif txt.startswith("lim"):
            _, expr, val = txt.split()
            rep = calcul_limite(expr, val)

        elif txt.startswith("trig"):
            rep = trigonometrie(txt.replace("trig", ""))

        elif "=" in txt:
            rep = resoudre_equation(txt)

        else:
            rep = calcul_simple(txt)

        bot.reply_to(message, rep)

    except:
        bot.reply_to(
            message,
            "❌ Erreur de format.\n"
            "Exemples :\n"
            "x**2-5*x+6=0\n"
            "deriv x**2\n"
            "integ x**2\n"
            "lim 1/x 0\n"
            "trig sin(x)"
        )

bot.infinity_polling()
