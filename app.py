import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="City Gems Explorer",
    page_icon="💎",
    layout="wide"
)

# ==========================================
# 🧠 ZONE D'INTELLIGENCE (TES GEMS)
# ==========================================

# GEM 1 : GLOBAL FOOD SCOUT
PROMPT_FOOD = """
### 🎯 ROLE & OBJECTIF
Tu es le "Global Food Scout". Ta mission est de trouver 5 pépites culinaires ("Hidden Gems") et de les présenter.

### 🌐 PROTOCOLE DE LANGUE
1. Ville en FRANCE 🇫🇷 : Réponds en FRANÇAIS.
2. Ville MONDE 🌍 : Réponds en ANGLAIS.
3. Instruction spécifique utilisateur : Prioritaire.

### 🛡️ ALGORITHME DE SÉLECTION
1. QUALITÉ : Note Google strictement >= 4.5/5.
2. CONFIDENTIALITÉ : Moins de 1000 avis (Tolérance 2000 pour grandes capitales).
3. UNICITÉ : Pas de chaînes.
4. OUVERTURE : Vérifie que le lieu est "Ouvert".

### 📝 FORMAT DE SORTIE TEXTE
Affiche cette liste simple :

[Si Français] :
"Voici 5 pépites vérifiées à **[Ville]**."

**1. [Nom Exact en GRAS]** (Quartier)
* 🥘 **Concept :** [Spécialité en quelques mots].
* ✨ **Pourquoi c'est une pépite :** [Ton avis d'expert].
* 💰 **Prix :** [€ / €€ / €€€]

[Si Anglais] :
"Here are 5 verified hidden gems in **[City]**."

**1. [Exact Name in BOLD]** (Neighborhood)
"""

# GEM 2 : SOCIAL MEDIA EXPERT
PROMPT_SOCIAL = """
Tu es un expert en création de contenu social media et un dénicheur de faits historiques insolites.
Ton objectif est de générer 3 informations insolites sur une ville.

### 🌍 RÈGLE DE LANGUE
1. Ville francophone → FRANÇAIS.
2. Ville NON-francophone → ANGLAIS.

### 🔎 RÈGLE DE SOURCING
Tu ne dois inventer aucune statistique. Trouve une source fiable et inclus l'URL directe.

### 📝 FORMAT DE RÉPONSE
Pour chaque ville, propose exactement 3 idées distinctes :

[Emoji] Idée [Numéro] : [Nom de l'idée]
[Phrase d'intro]

**Le titre du post :** [Titre Clickbait intelligent]
**La stat/L'info :** [Le fait précis]
**La source :** [Nom] - [URL]
**Texte :** [Corps du post engageant]
👇 [Question d'engagement]
[Hashtags]
"""

# ==========================================
# 🖥️ INTERFACE UTILISATEUR (FRONTEND)
# ==========================================

# Titre et Sous-titre
st.title("💎 City Gems Explorer")
st.markdown("Ton dénicheur personnel de restos cachés et d'anecdotes historiques.")
st.divider()

# Barre latérale pour les réglages
with st.sidebar:
    st.header("⚙️ Réglages")
    
    # Champ pour la clé API (pour sécuriser ton accès)
    api_key = st.text_input("Ta Clé API Google (Gemini)", type="password", help="Récupère ta clé sur aistudio.google.com")
    
    st.divider()
    
    # Le choix du mode (Resto ou Social)
    mode = st.radio(
        "Que cherches-tu aujourd'hui ?",
        ["🥘 Pépites Restos (Food Scout)", "🤓 Fun Facts (Social Media)"],
        captions=["5 restos cachés et bien notés", "3 idées de contenus viraux"]
    )

# Zone principale
col1, col2 = st.columns([3, 1])

with col1:
    ville = st.text_input("📍 Quelle ville veux-tu explorer ?", placeholder="ex: Paris, Tokyo, Barcelone...")

with col2:
    # Espace vide pour aligner le bouton
    st.write("") 
    st.write("")
    bouton_lancer = st.button("Lancer la recherche 🚀", use_container_width=True, type="primary")

# ==========================================
# 🚀 LOGIQUE D'EXÉCUTION
# ==========================================

if bouton_lancer:
    if not api_key:
        st.error("⚠️ Oups ! Il manque ta Clé API dans la barre latérale.")
        st.info("Va sur https://aistudio.google.com/app/apikey pour en créer une gratuite.")
    
    elif not ville:
        st.warning("⚠️ Merci d'écrire le nom d'une ville.")
        
    else:
        try:
            # 1. Configuration de Gemini
            genai.configure(api_key=api_key)
            
            # 2. Sélection du bon "Cerveau" (Prompt)
            if "Restos" in mode:
                system_instruction = PROMPT_FOOD
                user_message = f"Trouve des pépites à {ville}"
            else:
                system_instruction = PROMPT_SOCIAL
                user_message = f"Trouve des fun facts sur {ville}"
            
            # 3. Appel à l'IA (avec animation de chargement)
            with st.spinner(f"🕵️‍♂️ L'IA analyse {ville} en profondeur..."):
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
                response = model.generate_content(user_message)
            
            # 4. Affichage du résultat
            st.success("Analyse terminée !")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
