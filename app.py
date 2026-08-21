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

# Configuration globale
st.set_page_config(
    page_title="Terranexa - Financez l'économie réelle",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# DICTIONNAIRE DE TRADUCTION
# ==========================================
TRANSLATIONS = {
    'fr': {
        'hero_title': "Financez l'économie réelle, l'expérience et les projets d'avenir.",
        'hero_desc': "Que vous soyez un jeune fondateur Tech, un entrepreneur chevronné, ou un futur retraité prêt à concrétiser la ferme ou le commerce de vos rêves : Terranexa valorise votre parcours et connecte votre projet au capital d'investisseurs engagés.",
        'btn_deposit': "Déposer un Projet",
        'btn_invest': "Investir dans l'Impact",
        'secteurs_tag': "CE QUE NOUS FINANÇONS",
        'secteurs_title': "De la ferme familiale à la startup, tous les secteurs de l'économie réelle.",
        'secteurs_sub': "Chaque projet déposé sur Terranexa est classé par secteur pour orienter les investisseurs vers les impacts qui comptent pour eux.",
        'stat_1_val': "+120",
        'stat_1_lbl': "Projets accompagnés",
        'stat_2_val': "€18M",
        'stat_2_lbl': "Capital orienté vers les porteurs",
        'stat_3_val': "1 sur 3",
        'stat_3_lbl': "Porteurs séniors ou en reconversion",
        'stat_4_val': "9 pays",
        'stat_4_lbl': "Zones d'implantation couvertes",
        'steps_tag': "COMMENT ÇA MARCHE",
        'steps_title': "Un parcours simple en 4 étapes",
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
        'hero_title': "Finance the real economy, expertise, and future projects.",
        'hero_desc': "Whether you are a young Tech founder, a seasoned entrepreneur, or a future retiree ready to start the farm or business of your dreams: Terranexa values your background and connects your project to committed investors.",
        'btn_deposit': "Submit a Project",
        'btn_invest': "Invest in Impact",
        'secteurs_tag': "WHAT WE FINANCE",
        'secteurs_title': "From family farms to startups, all sectors of the real economy.",
        'secteurs_sub': "Each project submitted on Terranexa is classified by sector to guide investors towards the impacts that matter to them.",
        'stat_1_val': "+120",
        'stat_1_lbl': "Supported projects",
        'stat_2_val': "€18M",
        'stat_2_lbl': "Capital raised for entrepreneurs",
        'stat_3_val': "1 in 3",
        'stat_3_lbl': "Senior or career change founders",
        'stat_4_val': "9 countries",
        'stat_4_lbl': "Covered regions",
        'steps_tag': "HOW IT WORKS",
        'steps_title': "A simple 4-step process",
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
    }
}

# --- INITIALISATION DE LA LANGUE DANS SESSION STATE ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'fr'

with st.sidebar:
    lang_choice = st.selectbox(
        TRANSLATIONS[st.session_state['lang']]['lang_selector'],
        options=['fr', 'en'],
        format_func=lambda x: {'fr': '🇫🇷 Français', 'en': '🇬🇧 English'}[x]
    )
    if lang_choice != st.session_state['lang']:
        st.session_state['lang'] = lang_choice
        st.rerun()

t = TRANSLATIONS[st.session_state['lang']]

# ==========================================
# CSS SUR MESURE - CHARTE GRAPHIQUE TERRANEXA
# ==========================================
custom_css = """
<style>
/* Import de la police Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #F8FAFC;
}

.stApp {
    background-color: #060D18;
}

/* Header & Navbar */
.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 30px;
    background-color: #0A192F;
    border-bottom: 1px solid #1E293B;
    margin-bottom: 30px;
}
.brand-logo {
    font-size: 1.5rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 1px;
}
.brand-logo span {
    color: #10B981;
}

/* Sections Hero & Dark */
.hero-section {
    background-color: #0A192F;
    padding: 50px 40px;
    border-radius: 16px;
    border: 1px solid #1E293B;
    margin-bottom: 30px;
}
.hero-title {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
    line-height: 1.2 !important;
    margin-bottom: 20px !important;
}
.hero-desc {
    font-size: 1.1rem;
    color: #94A3B8;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* Section Fond Clair */
.light-section {
    background-color: #F8FAFC;
    color: #0F172A;
    padding: 50px 40px;
    border-radius: 16px;
    margin-bottom: 30px;
}
.light-section h2 {
    color: #0A192F !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}
.tag-green {
    color: #10B981;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* Cartes Profils sur Fond Clair */
.profile-card {
    background: #FFFFFF;
    border-right: 1px solid #E2E8F0;
    padding: 25px;
    height: 100%;
}
.profile-card h3 {
    color: #0A192F !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-top: 15px !important;
}
.profile-card p {
    color: #64748B;
    font-size: 0.95rem;
    line-height: 1.5;
}

/* Cartes Étapes (01, 02...) */
.step-card {
    background: #0A192F;
    border: 1px solid #1E293B;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.step-number {
    display: inline-block;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    border: 2px solid #10B981;
    color: #10B981;
    text-align: center;
    line-height: 41px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 15px;
}
.step-title {
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.step-desc {
    color: #94A3B8;
    font-size: 0.9rem;
    line-height: 1.4;
}

/* Grille de Statistiques */
.stat-box {
    text-align: center;
    padding: 30px 15px;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
}
.stat-value {
    font-size: 2.8rem;
    font-weight: 800;
    color: #0A192F;
}
.stat-value.green {
    color: #10B981;
}
.stat-label {
    color: #64748B;
    font-size: 0.95rem;
    margin-top: 5px;
}

/* Boutons personnalisés */
.stButton>button {
    background-color: #10B981 !important;
    color: #FFFFFF !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #059669 !important;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* Footer Dark */
.footer-dark {
    background-color: #0A192F;
    padding: 40px 20px;
    border-top: 1px solid #1E293B;
    margin-top: 50px;
}
.footer-col-title {
    color: #94A3B8;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 15px;
}
.footer-link {
    color: #CBD5E1;
    font-size: 0.9rem;
    margin-bottom: 8px;
    display: block;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Helper pour vérifier l'email
def check_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# Initialisation du Session State
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'step' not in st.session_state:
    st.session_state['step'] = 'choix_auth'

# ==========================================
# BARRE DE NAVIGATION FIXE
# ==========================================
col_nav_brand, col_nav_btn = st.columns([3, 1])
with col_nav_brand:
    st.markdown("<div class='brand-logo'>🟡 TERRANEXA<span></span></div>", unsafe_allow_html=True)
with col_nav_btn:
    if st.button(t['btn_invest'], use_container_width=True):
        st.session_state['page'] = 'home'
        st.rerun()

# ==========================================
# 1. PAGE D'ACCUEIL
# ==========================================
if st.session_state['page'] == 'home':

    # --- HERO SECTION ---
    st.markdown(f"""
        <div class='hero-section'>
            <h1 class='hero-title'>{t['hero_title']}</h1>
            <p class='hero-desc'>{t['hero_desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button(t['btn_deposit']):
        st.session_state['page'] = 'parcours'
        st.session_state['step'] = 'choix_auth'
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- SECTION CE QUE NOUS FINANÇONS (FOND CLAIR) ---
    st.markdown(f"""
        <div class='light-section'>
            <p class='tag-green'>{t['secteurs_tag']}</p>
            <h2>{t['secteurs_title']}</h2>
            <p style='color: #64748B; font-size: 1.05rem;'>{t['secteurs_sub']}</p>
        </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
            <div class='profile-card'>
                <div style='font-size: 2rem;'>👵👴</div>
                <h3>Sénior / Retraité</h3>
                <p>Un parcours d'accompagnement dédié pour valoriser des décennies d'expérience dans un nouveau projet.</p>
            </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
            <div class='profile-card'>
                <div style='font-size: 2rem;'>🏪</div>
                <h3>Commerçant / Artisan</h3>
                <p>Pour les entreprises déjà existantes — boulangerie, atelier, boutique — en recherche d'expansion.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- SECTION STATISTIQUES (FOND CLAIR & GRILLE) ---
    st.markdown("<p class='tag-green' style='text-align: center;'>IMPACT EN CHIFFRES</p>", unsafe_allow_html=True)
    
    st_col1, st_col2 = st.columns(2)
    with st_col1:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-value green'>{t['stat_1_val']}</div>
                <div class='stat-label'>{t['stat_1_lbl']}</div>
            </div>
        """, unsafe_allow_html=True)
    with st_col2:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-value green'>{t['stat_2_val']}</div>
                <div class='stat-label'>{t['stat_2_lbl']}</div>
            </div>
        """, unsafe_allow_html=True)

    st_col3, st_col4 = st.columns(2)
    with st_col3:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-value green'>{t['stat_3_val']}</div>
                <div class='stat-label'>{t['stat_3_lbl']}</div>
            </div>
        """, unsafe_allow_html=True)
    with st_col4:
        st.markdown(f"""
            <div class='stat-box'>
                <div class='stat-value green'>{t['stat_4_val']}</div>
                <div class='stat-label'>{t['stat_4_lbl']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- SECTION ÉTAPES PARCOURS (FOND SOMBRE) ---
    st.markdown(f"""
        <p class='tag-green'>{t['steps_tag']}</p>
        <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 800; margin-bottom: 30px;'>{t['steps_title']}</h2>
    """, unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("""
            <div class='step-card'>
                <div class='step-number'>01</div>
                <div class='step-title'>Inscription</div>
                <div class='step-desc'>Créez votre compte en quelques minutes : nom, e-mail, téléphone / WhatsApp.</div>
            </div>
        """, unsafe_allow_html=True)
    with col_e2:
        st.markdown("""
            <div class='step-card'>
                <div class='step-number'>02</div>
                <div class='step-title'>Profil & expérience</div>
                <div class='step-desc'>Sénior, artisan, reconversion ou startup : indiquez votre profil et valorisez votre parcours.</div>
            </div>
        """, unsafe_allow_html=True)

    col_e3, col_e4 = st.columns(2)
    with col_e3:
        st.markdown("""
            <div class='step-card'>
                <div class='step-number'>03</div>
                <div class='step-title'>Formulaire adaptatif</div>
                <div class='step-desc'>Présentez votre concept, l'impact de votre activité et vos besoins financiers.</div>
            </div>
        """, unsafe_allow_html=True)
    with col_e4:
        st.markdown("""
            <div class='step-card'>
                <div class='step-number'>04</div>
                <div class='step-title'>Validation</div>
                <div class='step-desc'>Réglez les frais d'instruction et soumettez votre dossier au comité d'experts.</div>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. PARCOURS (INSCRIPTION / CONNEXION)
# ==========================================
elif st.session_state['page'] == 'parcours':

    if st.session_state['step'] == 'choix_auth':
        st.markdown(f"""
            <div class='hero-section' style='text-align: center;'>
                <h2 style='color: #FFFFFF; font-size: 2rem; font-weight: 800;'>{t['auth_title']}</h2>
                <p style='color: #94A3B8;'>{t['auth_sub']}</p>
            </div>
        """, unsafe_allow_html=True)

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            if st.button(t['btn_register'], use_container_width=True):
                st.session_state['step'] = 'page_inscription'
                st.rerun()
        with col_a2:
            if st.button(t['btn_login'], use_container_width=True):
                st.session_state['step'] = 'page_connexion'
                st.rerun()

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

# ==========================================
# FOOTER NOIR / BLEU NUIT (CONFORME À LA CAPTURE)
# ==========================================
st.markdown("""
    <div class='footer-dark'>
        <div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>
            <div style='max-width: 300px;'>
                <div class='brand-logo' style='margin-bottom: 15px;'>🟡 TERRANEXA</div>
                <p style='color: #94A3B8; font-size: 0.85rem; line-height: 1.5;'>
                    Plateforme de financement participatif qui valorise tous les parcours — jeunes fondateurs, artisans, séniors et retraités — au service de l'économie réelle.
                </p>
            </div>
            <div>
                <div class='footer-col-title'>PLATEFORME</div>
                <span class='footer-link'>Déposer un projet</span>
                <span class='footer-link'>Investir</span>
                <span class='footer-link'>Profils</span>
                <span class='footer-link'>Secteurs</span>
            </div>
            <div>
                <div class='footer-col-title'>RESSOURCES</div>
                <span class='footer-link'>Centre d'aide</span>
                <span class='footer-link'>Comité d'experts</span>
                <span class='footer-link'>Frais d'instruction</span>
            </div>
            <div>
                <div class='footer-col-title'>SOCIÉTÉ</div>
                <span class='footer-link'>À propos</span>
                <span class='footer-link'>Contact</span>
                <span class='footer-link'>Presse</span>
            </div>
        </div>
        <div style='border-top: 1px solid #1E293B; margin-top: 30px; padding-top: 20px; text-align: center; color: #64748B; font-size: 0.8rem;'>
            © 2026 Terranexa. Tous droits réservés. · Mentions légales · CGU · Confidentialité
        </div>
    </div>
""", unsafe_allow_html=True)
