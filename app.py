import re
import streamlit as st
import os
from database import (
    init_db,
    inscrire_utilisateur,
    authentifier_utilisateur,
    enregistrer_porteur_kys,
    enregistrer_projet_et_paiement
)

# Initialisation de la base de données
init_db()

# Configuration globale de la page
st.set_page_config(
    page_title="Terranexa",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# DICTIONNAIRE DE TRADUCTION (DICTIONARY)
# ==========================================
TRANSLATIONS = {
    'fr': {
        'page_title': "Terranexa - Financez l'économie réelle",
        'welcome_title': "Bienvenue sur la plateforme terranexa",
        'hero_title': "Financez l'économie réelle, l'expérience et les projets d'avenir.",
        'hero_desc': "Que vous soyez un jeune fondateur Tech, un entrepreneur chevronné, ou un futur retraité prêt à concrétiser la ferme ou le commerce de vos rêves: Terranexa valorise votre parcours et connecte votre projet au capital d'investisseurs engagés.",
        'btn_deposit': "📌 Déposer un Projet",
        'btn_discover': "🔍 Découvrir les Projets",
        'profile_title': "Diversité des Porteurs de Projet",
        'senior_desc': "👵👴 <b>Sénior / Retraité :</b> Valorisation du savoir-faire dans sa ferme ou sa boutique.",
        'artisan_desc': "🛠️ <b>Artisan & Commerçant :</b> Consolidation et extension d'activités locales.",
        'tech_desc': "💡 <b>Ingénieur / Young Tech :</b> Projets d'innovation et AgriTech.",
        'partners_title': "En partenariat avec des institutions financières, banques et microfinances de confiance",
        'nav_home': "🏠 Accueil",
        'auth_title': "Espace Porteur de Projet",
        'auth_sub': "Pour déposer votre projet et suivre son avancement, veuillez vous identifier.",
        'btn_register': "📝 S'inscrire",
        'has_account': "Avez-vous déjà un compte ?",
        'btn_login': "🔑 Se connecter",
        'step1_reg_title': "Étape 1 sur 7 : Inscription de votre compte",
        'step1_login_title': "Étape 1 sur 7 : Connexion à votre compte",
        'label_nom': "Nom *",
        'label_prenom': "Prénom(s) *",
        'label_email': "Adresse E-mail *",
        'label_phone': "Numéro de téléphone (+229) *",
        'label_pwd': "Mot de passe *",
        'label_porteur_check': "Je suis un Porteur de Projet / Entrepreneur",
        'label_cgu': "J'accepte les Conditions Générales d'Utilisation (CGU) *",
        'btn_back': "⬅️ Retour",
        'btn_continue_reg': "S'inscrire et Continuer ➡️",
        'btn_continue_login': "Se connecter et Continuer ➡️",
        'err_missing_fields': "Veuillez remplir tous les champs obligatoires et accepter les CGU.",
        'err_email': "Format d'adresse e-mail invalide.",
        'err_phone': "Le numéro de téléphone doit contenir uniquement des chiffres.",
        'err_login': "E-mail ou mot de passe incorrect.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    },
    'en': {
        'page_title': "Terranexa - Finance the real economy",
        'welcome_title': "Welcome to the Terranexa platform",
        'hero_title': "Finance the real economy, expertise, and future projects.",
        'hero_desc': "Whether you are a young Tech founder, a seasoned entrepreneur, or a future retiree ready to start the farm or business of your dreams: Terranexa values your background and connects your project to committed investors.",
        'btn_deposit': "📌 Submit a Project",
        'btn_discover': "🔍 Discover Projects",
        'profile_title': "Diversity of Project Owners",
        'senior_desc': "👵👴 <b>Senior / Retiree:</b> Highlighting expertise in farming or local shops.",
        'artisan_desc': "🛠️ <b>Artisan & Trader:</b> Consolidation and expansion of local activities.",
        'tech_desc': "💡 <b>Engineer / Young Tech:</b> Innovation projects and AgriTech.",
        'partners_title': "In partnership with trusted financial institutions, banks, and microfinance networks",
        'nav_home': "🏠 Home",
        'auth_title': "Project Owner Space",
        'auth_sub': "To submit your project and track its progress, please log in or register.",
        'btn_register': "📝 Register",
        'has_account': "Already have an account?",
        'btn_login': "🔑 Log In",
        'step1_reg_title': "Step 1 of 7: Account Registration",
        'step1_login_title': "Step 1 of 7: Account Login",
        'label_nom': "Last Name *",
        'label_prenom': "First Name(s) *",
        'label_email': "Email Address *",
        'label_phone': "Phone Number (+229) *",
        'label_pwd': "Password *",
        'label_porteur_check': "I am a Project Owner / Entrepreneur",
        'label_cgu': "I accept the Terms and Conditions (TCU) *",
        'btn_back': "⬅️ Back",
        'btn_continue_reg': "Register and Continue ➡️",
        'btn_continue_login': "Log In and Continue ➡️",
        'err_missing_fields': "Please fill in all required fields and accept the Terms.",
        'err_email': "Invalid email address format.",
        'err_phone': "Phone number must contain digits only.",
        'err_login': "Incorrect email or password.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    },
    'es': {
        'page_title': "Terranexa - Financiar la economía real",
        'welcome_title': "Bienvenido a la plataforma Terranexa",
        'hero_title': "Financie la economía real, la experiencia y los proyectos del futuro.",
        'hero_desc': "Ya sea un joven fundador Tech, un empresario experimentado o un futuro jubilado listo para hacer realidad la granja o el negocio de sus sueños: Terranexa valora su trayectoria y conecta su proyecto con inversores comprometidos.",
        'btn_deposit': "📌 Publicar un Proyecto",
        'btn_discover': "🔍 Descubrir Proyectos",
        'profile_title': "Diversidad de Promotores de Proyectos",
        'senior_desc': "👵👴 <b>Sénior / Jubilado:</b> Valoración de la experiencia en su granja o tienda.",
        'artisan_desc': "🛠️ <b>Artesano y Comerciante:</b> Consolidación y expansión de actividades locales.",
        'tech_desc': "💡 <b>Ingeniero / Young Tech:</b> Proyectos de innovación y AgriTech.",
        'partners_title': "En asociación con instituciones financieras, bancos y microfinanzas de confianza",
        'nav_home': "🏠 Inicio",
        'auth_title': "Espacio del Promotor",
        'auth_sub': "Para enviar su proyecto y seguir su estado, inicie sesión o regístrese.",
        'btn_register': "📝 Registrarse",
        'has_account': "¿Ya tiene una cuenta?",
        'btn_login': "🔑 Iniciar sesión",
        'step1_reg_title': "Paso 1 de 7: Registro de cuenta",
        'step1_login_title': "Paso 1 de 7: Inicio de sesión",
        'label_nom': "Apellido *",
        'label_prenom': "Nombre(s) *",
        'label_email': "Correo electrónico *",
        'label_phone': "Número de teléfono (+229) *",
        'label_pwd': "Contraseña *",
        'label_porteur_check': "Soy un Promotor de Proyecto / Emprendedor",
        'label_cgu': "Acepto los Términos y Condiciones *",
        'btn_back': "⬅️ Volver",
        'btn_continue_reg': "Registrarse y Continuar ➡️",
        'btn_continue_login': "Iniciar sesión y Continuar ➡️",
        'err_missing_fields': "Por favor complete todos los campos obligatorios y acepte los términos.",
        'err_email': "Formato de correo electrónico no válido.",
        'err_phone': "El teléfono debe contener solo dígitos.",
        'err_login': "Correo electrónico o contraseña incorrectos.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    }
}

# --- INITIALISATION DE LA LANGUE DANS SESSION STATE ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'fr'

# --- MENU DE SÉLECTION DE LA LANGUE DANS LA SIDEBAR ---
with st.sidebar:
    lang_choice = st.selectbox(
        TRANSLATIONS[st.session_state['lang']]['lang_selector'],
        options=['fr', 'en', 'es'],
        format_func=lambda x: {'fr': '🇫🇷 Français', 'en': '🇬🇧 English', 'es': '🇪🇸 Español'}[x]
    )
    if lang_choice != st.session_state['lang']:
        st.session_state['lang'] = lang_choice
        st.rerun()

# Raccourci pour récupérer les textes traduits
t = TRANSLATIONS[st.session_state['lang']]

# --- CSS Personnalisé ---
LOGO_URL = "https://raw.githubusercontent.com/Sylvalaine-agblonon/terranexa/main/logo.jpg"

custom_css = f"""
<style>
.stApp {{ background-color: #E0F2FE; }}
.stApp::before {{
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url('{LOGO_URL}');
    background-repeat: no-repeat; background-position: center; background-size: 1500px;
    opacity: 0.10; pointer-events: none; z-index: 0;
    animation: floatLogo 8s ease-in-out infinite;
}}
@keyframes floatLogo {{
    0% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
    50% {{ transform: translateY(-20px) scale(1.05) rotate(2deg); }}
    100% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
}}
.home-header-banner {{
    background-color: #0C192C; padding: 40px 20px; border-radius: 12px;
    text-align: center; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(12, 25, 44, 0.3);
}}
.home-header-title {{
    color: #FFFFFF !important; font-size: 3rem !important;
    font-weight: 900 !important; text-transform: uppercase; margin: 0 !important;
}}
.auth-wrapper {{ display: flex; justify-content: center; align-items: center; min-height: 60vh; }}
.centered-choice-card {{
    background-color: #FFFFFF; padding: 40px 30px; border-radius: 16px;
    box-shadow: 0 10px 25px rgba(12, 25, 44, 0.15); text-align: center;
    border: 1px solid #CBD5E1; width: 100%; max-width: 500px;
}}
.main-title {{ color: #142B52; font-size: 2.2rem; font-weight: 800; }}
.hero-card {{ background-color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; }}
.stButton>button {{ background-color: #142B52; color: white; border-radius: 8px; font-weight: 600; }}
.stButton>button:hover {{ background-color: #0A9E60; color: white; }}
.partner-section {{
    background-color: #F8FAFC; padding: 20px; border-radius: 12px;
    border: 1px solid #E2E8F0; text-align: center; margin-top: 20px;
}}
.partner-logo-box {{
    background-color: #ffffff; border: 1px solid #CBD5E1; border-radius: 8px;
    padding: 12px; text-align: center; font-weight: 700; color: #142B52;
}}
.footer-container {{
    background-color: #142B52; color: #ffffff; padding: 20px;
    margin-top: 40px; border-radius: 8px; text-align: center; font-size: 0.85rem;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Initialisation du Session State
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'step' not in st.session_state:
    st.session_state['step'] = 'choix_auth'

def check_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# ==========================================
# 1. PAGE D'ACCUEIL TRADUITE
# ==========================================
if st.session_state['page'] == 'home':
    st.markdown(f"""
        <div class='home-header-banner'>
            <h1 class='home-header-title'>{t['welcome_title']}</h1>
        </div>
    """, unsafe_allow_html=True)

    col_hero_left, col_hero_right = st.columns([3, 2], gap="large")
    
    with col_hero_left:
        st.markdown(f"<h2 class='main-title'>{t['hero_title']}</h2>", unsafe_allow_html=True)
        st.write(t['hero_desc'])
        
        col_cta1, col_cta2 = st.columns(2)
        with col_cta1:
            if st.button(t['btn_deposit'], use_container_width=True):
                st.session_state['page'] = 'parcours'
                st.session_state['step'] = 'choix_auth'
                st.rerun()
        with col_cta2:
            st.button(t['btn_discover'], use_container_width=True)

    with col_hero_right:
        st.markdown(f"""
            <div class='hero-card'>
                <h4 style='color: #142B52; margin-top:0;'>{t['profile_title']}</h4>
                <p style='color: #475569; font-size: 0.9rem;'>
                    {t['senior_desc']}<br>
                    {t['artisan_desc']}<br>
                    {t['tech_desc']}
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"""
        <div class='partner-section'>
            <p style='color: #142B52; font-weight: 700; font-size: 1.05rem; margin-bottom: 15px;'>
                {t['partners_title']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1: st.markdown("<div class='partner-logo-box'>🏦 ECOBANK</div>", unsafe_allow_html=True)
    with col_b2: st.markdown("<div class='partner-logo-box'>🏦 BOA</div>", unsafe_allow_html=True)
    with col_b3: st.markdown("<div class='partner-logo-box'>🏛️ FECECAM-BÉNIN</div>", unsafe_allow_html=True)
    with col_b4: st.markdown("<div class='partner-logo-box'>💼 SGB</div>", unsafe_allow_html=True)

# ==========================================
# 2. PARCOURS (DÉPÔT / ACCÈS TRADUIT)
# ==========================================
elif st.session_state['page'] == 'parcours':

    if st.session_state['step'] == 'choix_auth':
        _, col_center, _ = st.columns([1, 2, 1])
        
        with col_center:
            st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='centered-choice-card'>
                    <h2 style='color: #142B52; margin-bottom: 10px;'>{t['auth_title']}</h2>
                    <p style='color: #64748B; font-size: 1rem; margin-bottom: 25px;'>{t['auth_sub']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(t['btn_register'], use_container_width=True):
                st.session_state['step'] = 'page_inscription'
                st.rerun()
            
            st.write("")
            st.markdown(f"<p style='text-align: center; font-weight: 600; color: #142B52; margin-top: 15px;'>{t['has_account']}</p>", unsafe_allow_html=True)
            
            if st.button(t['btn_login'], use_container_width=True):
                st.session_state['step'] = 'page_connexion'
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state['step'] == 'page_inscription':
        st.subheader(t['step1_reg_title'])
        st.progress(1 / 7)

        with st.form("form_register"):
            col_name1, col_name2 = st.columns(2)
            with col_name1: nom = st.text_input(t['label_nom']).strip()
            with col_name2: prenom = st.text_input(t['label_prenom']).strip()

            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input(t['label_email']).strip().lower()
                phone_digits = st.text_input(t['label_phone'], max_chars=10)
            with col2:
                pwd = st.text_input(t['label_pwd'], type="password")

            is_porteur = st.checkbox(t['label_porteur_check'], value=True)
            cgu = st.checkbox(t['label_cgu'])

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button(t['btn_back']):
                    st.session_state['step'] = 'choix_auth'
                    st.rerun()
            with col_btn2:
                if st.form_submit_button(t['btn_continue_reg']):
                    if not nom or not prenom or not email or not phone_digits or not pwd or not cgu:
                        st.error(t['err_missing_fields'])
                    elif not check_email(email):
                        st.error(t['err_email'])
                    elif not phone_digits.isdigit():
                        st.error(t['err_phone'])
                    else:
                        phone_full = f"+229{phone_digits}"
                        success, user_id, msg = inscrire_utilisateur(nom, prenom, email, phone_full, pwd, is_porteur)
                        if success:
                            st.session_state['user'] = {'id_utilisateur': user_id, 'nom': nom, 'prenom': prenom, 'email': email}
                            st.session_state['step'] = 'etape_2'
                            st.rerun()
                        else:
                            st.error(msg)

    elif st.session_state['step'] == 'page_connexion':
        st.subheader(t['step1_login_title'])
        st.progress(1 / 7)

        with st.form("form_login"):
            login_email = st.text_input(t['label_email']).strip().lower()
            login_pwd = st.text_input(t['label_pwd'], type="password")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button(t['btn_back']):
                    st.session_state['step'] = 'choix_auth'
                    st.rerun()
            with col_btn2:
                if st.form_submit_button(t['btn_continue_login']):
                    success, user_data = authentifier_utilisateur(login_email, login_pwd)
                    if success:
                        st.session_state['user'] = user_data
                        st.session_state['step'] = 'etape_2'
                        st.rerun()
                    else:
                        st.error(t['err_login'])

# --- FOOTER SOBRE ---
st.markdown("""
    <div class='footer-container'>
        <p style='margin-bottom: 5px; font-weight: 600;'>TERRANEXA © 2026 - Platform</p>
    </div>
""", unsafe_allow_html=True)
