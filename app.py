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

# Initialisation de la BDD
init_db()

# Configuration globale de la page
st.set_page_config(
    page_title="Terranexa - Financez l'économie réelle",
    page_icon="🌱",
    layout="wide"
)

# ==========================================
# DICTIONNAIRE DE TRADUCTION
# ==========================================
TRANSLATIONS = {
    'fr': {
        'welcome_title': "TERRANEXA",
        'hero_title': "Financez l'économie réelle, l'expérience et les projets d'avenir.",
        'hero_desc': "Terranexa valorise votre parcours et connecte votre projet au capital d'investisseurs engagés.",
        'btn_deposit': "📌 Déposer un Projet",
        'btn_discover': "🔍 Découvrir les Projets",
        'btn_dashboard': "📊 Mon Tableau de Bord",
        'stat_1_val': "+120", 'stat_1_lbl': "Projets accompagnés",
        'stat_2_val': "€18M", 'stat_2_lbl': "Capital orienté vers les porteurs",
        'stat_3_val': "1 sur 3", 'stat_3_lbl': "Porteurs séniors ou en reconversion",
        'stat_4_val': "9 pays", 'stat_4_lbl': "Zones d'implantation couvertes",
        'sec_title': "CE QUE NOUS FINANÇONS",
        'sec_subtitle': "De la ferme familiale à la startup, tous les secteurs de l'économie réelle.",
        'sec_desc': "Chaque projet déposé est classé par secteur pour orienter les investisseurs.",
        'profile_title': "PARCOURS & PROFILS",
        'profile_senior_title': "Sénior / Retraité",
        'profile_senior_desc': "Accompagnement dédié pour valoriser des décennies d'expérience.",
        'profile_artisan_title': "Commerçant / Artisan",
        'profile_artisan_desc': "Pour les entreprises existantes en recherche d'expansion.",
        'profile_tech_title': "Ingénieur / Young Tech",
        'profile_tech_desc': "Projets d'innovation, AgriTech et solutions locales.",
        'auth_title': "Espace Porteur de Projet",
        'auth_sub': "Pour déposer votre projet et suivre son avancement, veuillez vous identifier.",
        'btn_register': "📝 S'inscrire",
        'has_account': "Avez-vous déjà un compte ?",
        'btn_login': "🔑 Se connecter",
        'label_nom': "Nom *", 'label_prenom': "Prénom(s) *",
        'label_email': "Adresse E-mail *", 'label_phone': "Numéro WhatsApp (+229) *",
        'label_pwd': "Mot de passe *", 'label_porteur_check': "Je suis un Porteur de Projet / Entrepreneur",
        'label_cgu': "J'accepte les Conditions Générales d'Utilisation (CGU) *",
        'btn_back': "⬅️ Retour", 'btn_continue_reg': "S'inscrire et Continuer ➡️",
        'btn_continue_login': "Se connecter et Continuer ➡️",
        'err_missing_fields': "Veuillez remplir tous les champs obligatoires et accepter les CGU.",
        'err_email': "Format d'adresse e-mail invalide.",
        'err_phone': "Le numéro de téléphone doit contenir uniquement des chiffres.",
        'err_login': "E-mail ou mot de passe incorrect.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    },
    'en': {
        'welcome_title': "TERRANEXA",
        'hero_title': "Finance the real economy, expertise, and future projects.",
        'hero_desc': "Terranexa values your background and connects your project to committed investors.",
        'btn_deposit': "📌 Submit a Project",
        'btn_discover': "🔍 Discover Projects",
        'btn_dashboard': "📊 My Dashboard",
        'stat_1_val': "+120", 'stat_1_lbl': "Supported projects",
        'stat_2_val': "€18M", 'stat_2_lbl': "Capital directed to entrepreneurs",
        'stat_3_val': "1 in 3", 'stat_3_lbl': "Senior or career-change founders",
        'stat_4_val': "9 countries", 'stat_4_lbl': "Coverage areas",
        'sec_title': "WHAT WE FINANCE",
        'sec_subtitle': "From family farms to tech startups, across all real economy sectors.",
        'sec_desc': "Every submitted project is categorized to guide investors.",
        'profile_title': "TRACKS & PROFILES",
        'profile_senior_title': "Senior / Retiree",
        'profile_senior_desc': "Dedicated support to leverage decades of experience.",
        'profile_artisan_title': "Trader / Artisan",
        'profile_artisan_desc': "For existing businesses seeking expansion.",
        'profile_tech_title': "Engineer / Young Tech",
        'profile_tech_desc': "Innovation, AgriTech, and high-impact tech solutions.",
        'auth_title': "Project Owner Space",
        'auth_sub': "Please log in or register to track your submission.",
        'btn_register': "📝 Register", 'has_account': "Already have an account?",
        'btn_login': "🔑 Log In",
        'label_nom': "Last Name *", 'label_prenom': "First Name(s) *",
        'label_email': "Email Address *", 'label_phone': "WhatsApp Phone (+229) *",
        'label_pwd': "Password *", 'label_porteur_check': "I am a Project Owner / Entrepreneur",
        'label_cgu': "I accept Terms and Conditions *",
        'btn_back': "⬅️ Back", 'btn_continue_reg': "Register and Continue ➡️",
        'btn_continue_login': "Log In and Continue ➡️",
        'err_missing_fields': "Please fill all required fields and accept Terms.",
        'err_email': "Invalid email address format.",
        'err_phone': "Phone number must contain digits only.",
        'err_login': "Incorrect email or password.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    },
    'es': {
        'welcome_title': "TERRANEXA",
        'hero_title': "Financie la economía real, la experiencia y los proyectos del futuro.",
        'hero_desc': "Terranexa valora su trayectoria y conecta su proyecto con inversores comprometidos.",
        'btn_deposit': "📌 Publicar un Proyecto",
        'btn_discover': "🔍 Descubrir Proyectos",
        'btn_dashboard': "📊 Mi Panel",
        'stat_1_val': "+120", 'stat_1_lbl': "Proyectos acompañados",
        'stat_2_val': "€18M", 'stat_2_lbl': "Capital orientado a emprendedores",
        'stat_3_val': "1 de cada 3", 'stat_3_lbl': "Promotores séniores o en reconversión",
        'stat_4_val': "9 países", 'stat_4_lbl': "Zonas de cobertura",
        'sec_title': "LO QUE FINANCIAMOS",
        'sec_subtitle': "Desde la granja familiar hasta la startup, todos los sectores.",
        'sec_desc': "Cada proyecto se clasifica para guiar a los inversores.",
        'profile_title': "RUTAS Y PERFILES",
        'profile_senior_title': "Sénior / Jubilado",
        'profile_senior_desc': "Acompañamiento dedicado para valorizar su experiencia.",
        'profile_artisan_title': "Comerciante / Artesano",
        'profile_artisan_desc': "Para empresas existentes que buscan expansión.",
        'profile_tech_title': "Ingeniero / Young Tech",
        'profile_tech_desc': "Innovación, AgriTech y soluciones tecnológicas.",
        'auth_title': "Espacio del Promotor",
        'auth_sub': "Inicie sesión o regístrese para seguir su proyecto.",
        'btn_register': "📝 Registrarse", 'has_account': "¿Ya tiene una cuenta?",
        'btn_login': "🔑 Iniciar sesión",
        'label_nom': "Apellido *", 'label_prenom': "Nombre(s) *",
        'label_email': "Correo electrónico *", 'label_phone': "Teléfono WhatsApp (+229) *",
        'label_pwd': "Contraseña *", 'label_porteur_check': "Soy un Promotor de Proyecto",
        'label_cgu': "Acepto los Términos y Condiciones *",
        'btn_back': "⬅️ Volver", 'btn_continue_reg': "Registrarse y Continuar ➡️",
        'btn_continue_login': "Iniciar sesión y Continuar ➡️",
        'err_missing_fields': "Por favor complete los campos obligatorios.",
        'err_email': "Formato de correo no válido.",
        'err_phone': "El teléfono debe contener solo dígitos.",
        'err_login': "Correo electrónico o contraseña incorrectos.",
        'lang_selector': "🌐 Langue / Language / Idioma"
    }
}

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'fr'

with st.sidebar:
    lang_choice = st.selectbox(
        TRANSLATIONS[st.session_state['lang']]['lang_selector'],
        options=['fr', 'en', 'es'],
        format_func=lambda x: {'fr': '🇫🇷 Français', 'en': '🇬🇧 English', 'es': '🇪🇸 Español'}[x]
    )
    if lang_choice != st.session_state['lang']:
        st.session_state['lang'] = lang_choice
        st.rerun()

t = TRANSLATIONS[st.session_state['lang']]

# --- CSS PERSONNALISÉ ---
LOGO_URL = "https://raw.githubusercontent.com/Sylvalaine-agblonon/terranexa/main/logo.jpg"

custom_css = f"""
<style>
.stApp {{ background-color: #E0F2FE; }}
.stApp::before {{
    content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url('{LOGO_URL}'); background-repeat: no-repeat;
    background-position: center; background-size: 1500px; opacity: 0.10;
    pointer-events: none; z-index: 0; animation: floatLogo 8s ease-in-out infinite;
}}
@keyframes floatLogo {{
    0% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
    50% {{ transform: translateY(-20px) scale(1.05) rotate(2deg); }}
    100% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
}}
.dark-header-banner {{
    background-color: #0A192F; padding: 25px 20px; border-radius: 12px;
    margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1E293B;
}}
.dark-header-title {{ color: #FFFFFF !important; font-size: 2.2rem !important; font-weight: 800 !important; margin: 0 !important; }}
.dark-header-title span {{ color: #10B981; }}
.hero-dark-card {{
    background-color: #0A192F; color: #FFFFFF; padding: 35px; border-radius: 12px;
    border: 1px solid #1E293B; box-shadow: 0 8px 20px rgba(10, 25, 47, 0.25); margin-bottom: 25px;
}}
.hero-dark-card h1 {{ color: #FFFFFF !important; font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 15px; }}
.hero-dark-card p {{ color: #94A3B8; font-size: 1.05rem; line-height: 1.6; }}
.stat-card {{
    background-color: #FFFFFF; padding: 25px; border-radius: 10px; border: 1px solid #E2E8F0; text-align: left;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); height: 100%;
}}
.stat-val {{ font-size: 2.2rem; font-weight: 800; color: #10B981; margin-bottom: 5px; }}
.stat-lbl {{ font-size: 0.9rem; color: #475569; font-weight: 500; }}
.light-content-card {{
    background-color: #FFFFFF; padding: 30px; border-radius: 12px; border: 1px solid #E2E8F0;
    margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}}
.section-tag {{ color: #10B981; font-weight: 700; font-size: 0.85rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; }}
.section-title {{ color: #0F172A; font-size: 1.8rem; font-weight: 800; margin-bottom: 12px; }}
.profile-card {{ background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; height: 100%; }}
.profile-icon {{ font-size: 1.8rem; margin-bottom: 10px; }}
.profile-title {{ color: #0F172A; font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }}
.profile-desc {{ color: #64748B; font-size: 0.88rem; line-height: 1.5; }}
.badge-tag {{
    display: inline-block; background-color: #ECFDF5; color: #059669; padding: 4px 12px;
    border-radius: 20px; font-size: 0.8rem; font-weight: 700; border: 1px solid #A7F3D0; margin-right: 8px;
}}
.auth-wrapper {{ display: flex; justify-content: center; align-items: center; min-height: 60vh; }}
.centered-choice-card {{
    background-color: #FFFFFF; padding: 40px 30px; border-radius: 16px;
    box-shadow: 0 10px 25px rgba(12, 25, 44, 0.15); text-align: center; border: 1px solid #CBD5E1; width: 100%; max-width: 500px;
}}
.stButton>button {{
    background-color: #10B981 !important; color: white !important; border-radius: 6px !important;
    font-weight: 600 !important; border: none !important; padding: 0.5rem 1rem !important;
}}
.stButton>button:hover {{ background-color: #059669 !important; color: white !important; }}
.footer-dark {{
    background-color: #0A192F; color: #94A3B8; padding: 40px 20px 20px 20px;
    border-radius: 12px; margin-top: 40px; border: 1px solid #1E293B;
}}
.footer-col-title {{ color: #FFFFFF; font-weight: 700; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 15px; }}
.footer-link {{ color: #94A3B8; font-size: 0.88rem; margin-bottom: 8px; display: block; }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'step' not in st.session_state:
    st.session_state['step'] = 'choix_auth'

def check_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# ==========================================
# 1. PAGE D'ACCUEIL
# ==========================================
if st.session_state['page'] == 'home':
    st.markdown("""
        <div class='dark-header-banner'>
            <div class='dark-header-title'>🌱 TERRA<span>NEXA</span></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class='hero-dark-card'>
            <h1>{t['hero_title']}</h1>
            <p>{t['hero_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn1:
        if st.button(t['btn_deposit'], use_container_width=True):
            st.session_state['page'] = 'parcours'
            st.session_state['step'] = 'choix_auth'
            st.rerun()
    with col_btn2:
        if st.button(t['btn_discover'], use_container_width=True):
            st.session_state['page'] = 'projets'
            st.rerun()
    with col_btn3:
        if 'user' in st.session_state:
            if st.button(t['btn_dashboard'], use_container_width=True):
                st.session_state['page'] = 'dashboard'
                st.rerun()

    st.write("")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{t['stat_1_val']}</div><div class='stat-lbl'>{t['stat_1_lbl']}</div></div>", unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{t['stat_2_val']}</div><div class='stat-lbl'>{t['stat_2_lbl']}</div></div>", unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{t['stat_3_val']}</div><div class='stat-lbl'>{t['stat_3_lbl']}</div></div>", unsafe_allow_html=True)
    with col_s4:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{t['stat_4_val']}</div><div class='stat-lbl'>{t['stat_4_lbl']}</div></div>", unsafe_allow_html=True)

    st.write("")

    st.markdown(f"""
        <div class='light-content-card'>
            <div class='section-tag'>{t['sec_title']}</div>
            <div class='section-title'>{t['sec_subtitle']}</div>
            <p style='color: #64748B; font-size: 0.95rem; margin-bottom: 0;'>{t['sec_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='section-tag'>{t['profile_title']}</div>", unsafe_allow_html=True)
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown(f"<div class='profile-card'><div class='profile-icon'>👵👴</div><div class='profile-title'>{t['profile_senior_title']}</div><div class='profile-desc'>{t['profile_senior_desc']}</div></div>", unsafe_allow_html=True)
    with col_p2:
        st.markdown(f"<div class='profile-card'><div class='profile-icon'>🏪</div><div class='profile-title'>{t['profile_artisan_title']}</div><div class='profile-desc'>{t['profile_artisan_desc']}</div></div>", unsafe_allow_html=True)
    with col_p3:
        st.markdown(f"<div class='profile-card'><div class='profile-icon'>💡</div><div class='profile-title'>{t['profile_tech_title']}</div><div class='profile-desc'>{t['profile_tech_desc']}</div></div>", unsafe_allow_html=True)

# ==========================================
# 2. EXPLORATION DES PROJETS & MENTORING
# ==========================================
elif st.session_state['page'] == 'projets':
    st.markdown("<h2 style='color: #0A192F;'>🔍 Projets en Recherche de Financement</h2>", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        secteur_filter = st.selectbox("Filtrer par secteur", ["Tous", "AgriTech", "Artisanat / Commerce", "Énergie Renouvelable"])
    with col_f2:
        profil_filter = st.selectbox("Filtrer par type de porteur", ["Tous", "Jeune Tech", "Sénior / Retraité", "Artisan"])

    st.divider()

    projets_demo = [
        {"titre": "Ferme Avicole Biologique", "secteur": "AgriTech", "porteur": "Sénior / Retraité", "besoin": "15 000 000 FCFA", "score": 88, "badge": "Soutenu par FECECAM"},
        {"titre": "Plateforme Digitale Logistique", "secteur": "AgriTech", "porteur": "Jeune Tech", "besoin": "8 000 000 FCFA", "score": 92, "badge": "Inclusion Tech"},
        {"titre": "Extension Boulangerie Artisanale", "secteur": "Artisanat / Commerce", "porteur": "Artisan", "besoin": "5 000 000 FCFA", "score": 81, "badge": "Projet Vérifié"}
    ]

    for p in projets_demo:
        if (secteur_filter == "Tous" or secteur_filter == p["secteur"]) and (profil_filter == "Tous" or profil_filter == p["porteur"]):
            st.markdown(f"""
                <div class='light-content-card'>
                    <span class='badge-tag'>{p['badge']}</span>
                    <span class='badge-tag' style='background-color:#E0F2FE; color:#0284C7; border-color:#BAE6FD;'>Score ESG: {p['score']}/100</span>
                    <h3 style='color: #0A192F; margin-top: 10px;'>{p['titre']}</h3>
                    <p style='color: #64748B; margin-bottom: 5px;'>Secteur : <b>{p['secteur']}</b> | Porteur : <b>{p['porteur']}</b></p>
                    <p style='color: #10B981; font-weight: 700; font-size: 1.1rem;'>Besoin de financement : {p['besoin']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Financer / Parrainer {p['titre']}", key=p['titre']):
                st.success("Merci pour votre intérêt ! Un conseiller Terranexa prendra contact avec vous.")

    if st.button("⬅️ Retour à l'accueil"):
        st.session_state['page'] = 'home'
        st.rerun()

# ==========================================
# 3. DASHBOARD PORTEUR DE PROJET
# ==========================================
elif st.session_state['page'] == 'dashboard':
    st.markdown("<h2 style='color: #0A192F;'>📊 Votre Tableau de Bord Terranexa</h2>", unsafe_allow_html=True)
    user_name = st.session_state.get('user', {}).get('prenom', 'Porteur')
    st.write(f"Ravi de vous revoir, **{user_name}** !")

    st.markdown("""
        <div class='light-content-card'>
            <div class='section-tag'>STATUT DU DOSSIER</div>
            <h3 style='color: #0A192F;'>Projet : Ferme Solaire Locale</h3>
            <p style='color: #64748B;'>Avancement de la soumission :</p>
    """, unsafe_allow_html=True)
    st.progress(0.85)
    st.caption("Profil complété à 85% — KYC vérifié — En attente du règlement des frais d'instruction")
    st.markdown("</div>", unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("""
            <div class='light-content-card'>
                <div class='section-tag'>GÉNÉRATEUR EXPRESS</div>
                <h4>📄 Synthese Business Plan</h4>
                <p style='color: #64748B; font-size: 0.9rem;'>Téléchargez le récapitulatif structuré de votre dossier pour votre banque ou partenaire.</p>
            </div>
        """, unsafe_allow_html=True)
        pdf_data = f"TERRANEXA - BUSINESS PLAN EXPRESS\nPorteur: {user_name}\nProjet: Ferme Solaire Locale\nStatut: En validation"
        st.download_button("📥 Télécharger le dossier (PDF)", data=pdf_data, file_name="Business_Plan_Terranexa.txt", mime="text/plain")

    with col_d2:
        st.markdown("""
            <div class='light-content-card'>
                <div class='section-tag'>RÈGLEMENT SÉCURISÉ</div>
                <h4>💳 Frais d'instruction</h4>
                <p style='color: #64748B; font-size: 0.9rem;'>Réglez vos frais d'analyse de dossier via Mobile Money ou carte.</p>
            </div>
        """, unsafe_allow_html=True)
        moyen_payement = st.selectbox("Choisir l'opérateur", ["MTN Mobile Money", "Moov Money", "KKiaPay / Carte Bancaire"])
        if st.button("Payer 10 000 FCFA"):
            st.success(f"Paiement initialisé via {moyen_payement}. Veuillez valider le sous-menu sur votre téléphone.")

    if st.button("⬅️ Retour à l'accueil"):
        st.session_state['page'] = 'home'
        st.rerun()

# ==========================================
# 4. PARCOURS (DÉPÔT / FORMULAIRE & KYC)
# ==========================================
elif st.session_state['page'] == 'parcours':

    if st.session_state['step'] == 'choix_auth':
        _, col_center, _ = st.columns([1, 2, 1])
        with col_center:
            st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class='centered-choice-card'>
                    <h2 style='color: #0A192F; margin-bottom: 10px;'>{t['auth_title']}</h2>
                    <p style='color: #64748B; font-size: 0.95rem; margin-bottom: 25px;'>{t['auth_sub']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(t['btn_register'], use_container_width=True):
                st.session_state['step'] = 'page_inscription'
                st.rerun()
            
            st.write("")
            st.markdown(f"<p style='text-align: center; font-weight: 600; color: #0A192F;'>{t['has_account']}</p>", unsafe_allow_html=True)
            
            if st.button(t['btn_login'], use_container_width=True):
                st.session_state['step'] = 'page_connexion'
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state['step'] == 'page_inscription':
        st.subheader("Étape 1 sur 3 : Inscription du compte")
        st.progress(1 / 3)

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
                            st.session_state['step'] = 'etape_kyc'
                            st.rerun()
                        else:
                            st.error(msg)

    elif st.session_state['step'] == 'page_connexion':
        st.subheader("Connexion")
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
                        st.session_state['step'] = 'etape_kyc'
                        st.rerun()
                    else:
                        st.error(t['err_login'])

    elif st.session_state['step'] == 'etape_kyc':
        st.subheader("Étape 2 sur 3 : Vérification KYC & Impact ESG")
        st.progress(2 / 3)

        st.markdown("##### 📁 Pièces justificatives")
        c1, c2 = st.columns(2)
        with c1:
            st.file_uploader("Pièce d'identité (CNI / Passeport / CIP)", type=['pdf', 'png', 'jpg'])
        with c2:
            st.file_uploader("Document d'entreprise (IFU / RCCM / Optionnel)", type=['pdf', 'png', 'jpg'])

        st.markdown("##### 🌱 Évaluation de l'Impact ESG")
        jobs = st.slider("Nombre d'emplois locaux créés prévus", 1, 50, 5)
        eco = st.selectbox("Utilisation d'énergies propres ou pratiques durables ?", ["Oui", "Partiellement", "Non"])

        score_esg = min(100, (jobs * 2) + (30 if eco == "Oui" else 15))
        st.info(f"Score d'Impact ESG estimé : **{score_esg}/100**")

        if st.button("Valider et Passer au Tableau de Bord ➡️"):
            st.session_state['page'] = 'dashboard'
            st.rerun()

# ==========================================
# FOOTER COMPLET
# ==========================================
st.markdown("""
    <div class='footer-dark'>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 30px; margin-bottom: 30px;'>
            <div>
                <div style='color: #FFFFFF; font-size: 1.3rem; font-weight: 800; margin-bottom: 12px;'>🌱 TERRA<span style='color: #10B981;'>NEXA</span></div>
                <p style='font-size: 0.85rem; line-height: 1.5;'>Plateforme de financement participatif qui valorise tous les parcours — jeunes fondateurs, artisans, séniors et retraités — au service de l'économie réelle.</p>
            </div>
            <div>
                <div class='footer-col-title'>PLATEFORME</div>
                <div class='footer-link'>Déposer un projet</div>
                <div class='footer-link'>Investir</div>
                <div class='footer-link'>Profils & Secteurs</div>
            </div>
            <div>
                <div class='footer-col-title'>RESSOURCES</div>
                <div class='footer-link'>Centre d'aide</div>
                <div class='footer-link'>Comité d'experts</div>
                <div class='footer-link'>Frais d'instruction</div>
            </div>
            <div>
                <div class='footer-col-title'>PARTENAIRES</div>
                <div class='footer-link'>Ecobank</div>
                <div class='footer-link'>BOA Group</div>
                <div class='footer-link'>Banque Atlantique</div>
                <div class='footer-link'>FECECAM-BÉNIN</div>
            </div>
        </div>
        <hr style='border-color: #1E293B; margin-bottom: 20px;'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; font-size: 0.8rem; color: #64748B;'>
            <div>© 2026 Terranexa. Tous droits réservés.</div>
            <div>Mentions légales | CGU | Confidentialité</div>
        </div>
    </div>
""", unsafe_allow_html=True)
