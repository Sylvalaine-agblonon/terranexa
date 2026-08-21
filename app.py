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

# Initialisation des tables SQLite
init_db()

# Configuration globale unique de la page
st.set_page_config(
    page_title="Terranexa - Financez l'économie réelle",
    page_icon="🌱",
    layout="wide"
)

# --- CSS Personnalisé ---
LOGO_URL = "https://raw.githubusercontent.com/Sylvalaine-agblonon/terranexa/main/logo.jpg"

custom_css = f"""
<style>
/* Fond bleu ciel sur toute l'application */
.stApp {{
    background-color: #E0F2FE;
}}

/* Logo en arrière-plan avec animation de flottaison */
.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: url('{LOGO_URL}');
    background-repeat: no-repeat;
    background-position: center;
    background-size: 1500px;
    opacity: 0.10;
    pointer-events: none;
    z-index: 0;
    animation: floatLogo 8s ease-in-out infinite;
}}

@keyframes floatLogo {{
    0% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
    50% {{ transform: translateY(-20px) scale(1.05) rotate(2deg); }}
    100% {{ transform: translateY(0px) scale(1) rotate(0deg); }}
}}

@keyframes spinLogo {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}

.header-rotating-logo img {{
    border-radius: 50%;
    animation: spinLogo 12s linear infinite;
    transition: transform 0.3s ease;
}}

.header-rotating-logo img:hover {{
    animation-play-state: paused;
}}

/* En-tête Bleu Nuit (Page d'accueil) */
.home-header-banner {{
    background-color: #0C192C;
    padding: 40px 20px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 4px 12px rgba(12, 25, 44, 0.3);
}}

.home-header-title {{
    color: #FFFFFF !important;
    font-size: 3rem !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 0 !important;
    line-height: 1.2;
}}

/* Carte centrée pour le choix Inscription/Connexion */
.centered-choice-card {{
    background-color: #FFFFFF;
    padding: 40px 30px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(12, 25, 44, 0.15);
    text-align: center;
    border: 1px solid #CBD5E1;
    margin-top: 50px;
}}

/* Palette générale */
.main-title {{ color: #142B52; font-size: 2.2rem; font-weight: 800; line-height: 1.3; }}
.hero-card {{ background-color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #E2E8F0; }}
.stButton>button {{ background-color: #142B52; color: white; border-radius: 8px; font-weight: 600; }}
.stButton>button:hover {{ background-color: #0A9E60; color: white; }}

.partner-section {{
    background-color: #F8FAFC;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    text-align: center;
    margin-top: 20px;
}}

.partner-logo-box {{
    background-color: #ffffff;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    font-weight: 700;
    color: #142B52;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

.footer-container {{
    background-color: #142B52;
    color: #ffffff;
    padding: 20px;
    margin-top: 40px;
    border-radius: 8px;
    text-align: center;
    font-size: 0.85rem;
}}

.stMarkdown, .stButton, div[data-testid="stVerticalBlock"] {{
    position: relative;
    z-index: 1;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialisation du Session State
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'step' not in st.session_state:
    st.session_state['step'] = 'choix_auth'
if 'form_data' not in st.session_state:
    st.session_state['form_data'] = {}
if 'user' not in st.session_state:
    st.session_state['user'] = None
if 'id_porteur' not in st.session_state:
    st.session_state['id_porteur'] = None

LOGO_PATH = "logo.jpg"

def check_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)

# --- HEADER GLOBAL POUR LE PARCOURS DE DÉPÔT ---
if st.session_state['page'] == 'parcours':
    col_logo, col_nav = st.columns([3, 1])
    with col_logo:
        if os.path.exists(LOGO_PATH):
            st.markdown("<div class='header-rotating-logo'>", unsafe_allow_html=True)
            st.image(LOGO_PATH, width=120)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color: #142B52; margin:0;'>TERRA<span style='color: #0A9E60;'>NEXA</span></h2>", unsafe_allow_html=True)
    with col_nav:
        if st.button("🏠 Accueil"):
            st.session_state['page'] = 'home'
            st.rerun()
    st.divider()

# ==========================================
# 1. PAGE D'ACCUEIL
# ==========================================
if st.session_state['page'] == 'home':
    st.markdown("""
        <div class='home-header-banner'>
            <h1 class='home-header-title'>Bienvenue sur la plateforme terranexa</h1>
        </div>
    """, unsafe_allow_html=True)

    col_hero_left, col_hero_right = st.columns([3, 2], gap="large")
    
    with col_hero_left:
        st.markdown("<h2 class='main-title'>Financez l'économie réelle, l'expérience et les projets d'avenir.</h2>", unsafe_allow_html=True)
        st.write("Que vous soyez un jeune fondateur Tech, un entrepreneur chevronné, ou un futur retraité prêt à concrétiser la ferme ou le commerce de vos rêves: Terranexa valorise votre parcours et connecte votre projet au capital d'investisseurs engagés.")
        
        col_cta1, col_cta2 = st.columns(2)
        with col_cta1:
            if st.button("📌 Déposer un Projet", use_container_width=True):
                st.session_state['page'] = 'parcours'
                st.session_state['step'] = 'choix_auth'
                st.rerun()
        with col_cta2:
            st.button("🔍 Découvrir les Projets", use_container_width=True)

    with col_hero_right:
        st.markdown("""
            <div class='hero-card'>
                <h4 style='color: #142B52; margin-top:0;'>Diversité des Porteurs de Projet</h4>
                <p style='color: #475569; font-size: 0.9rem;'>
                    👵👴 <b>Sénior / Retraité :</b> Valorisation du savoir-faire dans sa ferme ou sa boutique.<br>
                    🛠️ <b>Artisan & Commerçant :</b> Consolidation et extension d'activités locales.<br>
                    💡 <b>Ingénieur / Young Tech :</b> Projets d'innovation et AgriTech.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
        <div class='partner-section'>
            <p style='color: #142B52; font-weight: 700; font-size: 1.05rem; margin-bottom: 15px;'>
                En partenariat avec des institutions financières, banques et microfinances de confiance
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        st.markdown("<div class='partner-logo-box'>🏦 ECOBANK</div>", unsafe_allow_html=True)
    with col_b2:
        st.markdown("<div class='partner-logo-box'>🏦 BOA (Bank of Africa)</div>", unsafe_allow_html=True)
    with col_b3:
        st.markdown("<div class='partner-logo-box'>🏛️ FECECAM-BÉNIN</div>", unsafe_allow_html=True)
    with col_b4:
        st.markdown("<div class='partner-logo-box'>💼 SGB (Société Générale)</div>", unsafe_allow_html=True)

# ==========================================
# 2. PARCOURS PAS-À-PAS EN 7 ÉTAPES
# ==========================================
elif st.session_state['page'] == 'parcours':

    # ------------------------------------------
    # ÉTAPE 1.A : CHOIX ACCÈS (CENTRÉ AU MILIEU)
    # ------------------------------------------
    if st.session_state['step'] == 'choix_auth':
        _, col_center, _ = st.columns([1, 2, 1])
        
        with col_center:
            st.markdown("""
                <div class='centered-choice-card'>
                    <h2 style='color: #142B52; margin-bottom: 10px;'>Espace Porteur de Projet</h2>
                    <p style='color: #64748B; font-size: 1rem; margin-bottom: 30px;'>
                        Pour déposer votre projet et suivre son avancement, veuillez vous identifier.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            if st.button("📝 S'inscrire", use_container_width=True):
                st.session_state['step'] = 'page_inscription'
                st.rerun()
            
            st.write("")
            st.write("")
            st.markdown("<p style='text-align: center; font-weight: 600; color: #142B52;'>Avez-vous déjà un compte ?</p>", unsafe_allow_html=True)
            if st.button("🔑 Se connecter", use_container_width=True):
                st.session_state['step'] = 'page_connexion'
                st.rerun()

    # ------------------------------------------
    # ÉTAPE 1.B : PAGE DÉDIÉE À L'INSCRIPTION
    # ------------------------------------------
    elif st.session_state['step'] == 'page_inscription':
        st.subheader("Étape 1 sur 7 : Inscription de votre compte")
        st.progress(1 / 7)

        with st.form("form_register"):
            col_name1, col_name2 = st.columns(2)
            with col_name1:
                nom = st.text_input("Nom *").strip()
            with col_name2:
                prenom = st.text_input("Prénom(s) *").strip()

            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Adresse E-mail *").strip().lower()
                phone_digits = st.text_input("Numéro de téléphone (+229) *", max_chars=10)
            with col2:
                pwd = st.text_input("Mot de passe *", type="password")

            is_porteur = st.checkbox("Je suis un Porteur de Projet / Entrepreneur", value=True)
            cgu = st.checkbox("J'accepte les Conditions Générales d'Utilisation (CGU) *")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'choix_auth'
                    st.rerun()
            with col_btn2:
                if st.form_submit_button("S'inscrire et Continuer ➡️"):
                    if not nom or not prenom or not email or not phone_digits or not pwd or not cgu:
                        st.error("Veuillez remplir tous les champs obligatoires (Nom, Prénom, E-mail, Téléphone, Mot de passe) et accepter les CGU.")
                    elif not check_email(email):
                        st.error("Format d'adresse e-mail invalide.")
                    elif not phone_digits.isdigit():
                        st.error("Le numéro de téléphone doit contenir uniquement des chiffres.")
                    else:
                        phone_full = f"+229{phone_digits}"
                        success, user_id, msg = inscrire_utilisateur(nom, prenom, email, phone_full, pwd, is_porteur)
                        if success:
                            st.session_state['user'] = {
                                'id_utilisateur': user_id,
                                'nom': nom,
                                'prenom': prenom,
                                'nom_prenom': f"{nom} {prenom}",
                                'email': email,
                                'telephone': phone_full
                            }
                            st.session_state['step'] = 'etape_2'
                            st.rerun()
                        else:
                            st.error(msg)

    # ------------------------------------------
    # ÉTAPE 1.C : PAGE DÉDIÉE À LA CONNEXION
    # ------------------------------------------
    elif st.session_state['step'] == 'page_connexion':
        st.subheader("Étape 1 sur 7 : Connexion à votre compte")
        st.progress(1 / 7)

        with st.form("form_login"):
            login_email = st.text_input("Adresse E-mail *").strip().lower()
            login_pwd = st.text_input("Mot de passe *", type="password")

            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'choix_auth'
                    st.rerun()
            with col_btn2:
                if st.form_submit_button("Se connecter et Continuer ➡️"):
                    success, user_data = authentifier_utilisateur(login_email, login_pwd)
                    if success:
                        st.session_state['user'] = user_data
                        st.success(f"Bienvenue, {user_data.get('prenom', user_data.get('nom', ''))} !")
                        st.session_state['step'] = 'etape_2'
                        st.rerun()
                    else:
                        st.error("E-mail ou mot de passe incorrect.")

    # ------------------------------------------
    # ÉTAPE 2 : PROFIL & KYS
    # ------------------------------------------
    elif st.session_state['step'] == 'etape_2':
        st.subheader("Étape 2 sur 7 : Profil & Valorisation du Parcours (KYS)")
        st.progress(2 / 7)

        with st.form("form_step_2"):
            profil_kys = st.selectbox(
                "Profil du porteur de projet *",
                [
                    "Sénior / Retraité ou Proche Retraite",
                    "Entreprise déjà existante / Commerçant / Artisan",
                    "Particulier / Reconversion professionnelle",
                    "Startup / Projet d'Innovation"
                ]
            )
            years_exp = st.number_input("Années d'expérience professionnelle dans le secteur *", min_value=0, max_value=60)
            resume_parcours = st.text_area("Résumé du parcours / Expertise accumulée *")

            col_id1, col_id2 = st.columns(2)
            with col_id1:
                nom_structure = st.text_input("Nom légal ou Nom du projet *")
                pays = st.text_input("Pays d'implantation *", value="Bénin")
            with col_id2:
                ville = st.text_input("Ville d'implantation *")
                identity_doc = st.file_uploader("Pièce d'identité (CNI/Passeport)", type=["pdf", "jpg", "png"])

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'choix_auth'
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Étape Suivante ➡️"):
                    if not nom_structure or not ville or not resume_parcours:
                        st.error("Veuillez remplir les champs obligatoires.")
                    else:
                        st.session_state['form_data'].update({
                            'profil_kys': profil_kys,
                            'years_exp': years_exp,
                            'resume_parcours': resume_parcours,
                            'nom_structure': nom_structure,
                            'pays': pays,
                            'ville': ville
                        })
                        id_porteur = enregistrer_porteur_kys(
                            st.session_state['user']['id_utilisateur'],
                            st.session_state['form_data']
                        )
                        st.session_state['id_porteur'] = id_porteur
                        st.session_state['step'] = 'onglet_a'
                        st.rerun()

    # ------------------------------------------
    # ÉTAPE 3 : PRÉSENTATION & MATURITÉ
    # ------------------------------------------
    elif st.session_state['step'] == 'onglet_a':
        st.subheader("Étape 3 sur 7 : Présentation Générale & Maturité")
        st.progress(3 / 7)

        with st.form("form_onglet_a"):
            titre_projet = st.text_input("Titre du projet *")
            maturite = st.radio(
                "Niveau de maturité du projet *",
                [
                    "Étape 1: Idée / Conception",
                    "Étape 2: Lancement / Amorçage",
                    "Étape 3: Déjà en cours d'exploitation"
                ]
            )
            secteur = st.selectbox(
                "Secteur d'activité *",
                [
                    "Élevage & Agriculture Classique",
                    "Commerce & Restauration",
                    "Artisanat & Services de proximité",
                    "AgriTech, GreenTech & IA engagée"
                ]
            )
            resume_accroche = st.text_area("Résumé court (Accroche - 280 caractères max) *", max_chars=280)

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'etape_2'
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Étape Suivante ➡️"):
                    if not titre_projet or not resume_accroche:
                        st.error("Veuillez renseigner le titre et l'accroche.")
                    else:
                        st.session_state['form_data'].update({
                            'titre_projet': titre_projet,
                            'maturite': maturite,
                            'secteur': secteur,
                            'resume_accroche': resume_accroche
                        })
                        st.session_state['step'] = 'onglet_b'
                        st.rerun()

    # ------------------------------------------
    # ÉTAPE 4 : CONCEPT, EXPÉRIENCE & IMPACT
    # ------------------------------------------
    elif st.session_state['step'] == 'onglet_b':
        st.subheader("Étape 4 sur 7 : Concept, Expérience & Impact")
        st.progress(4 / 7)

        with st.form("form_onglet_b"):
            desc_concept = st.text_area("Description détaillée du concept *")

            exp_garantie = ""
            vision_transmission = ""
            if "Sénior / Retraité" in st.session_state['form_data'].get('profil_kys', ''):
                st.info("🌾 Section Dédiée Séniors / Retraités - La Valeur de l'Expérience")
                exp_garantie = st.text_area("Comment votre expérience garantit-elle la réussite du projet ? *")
                vision_transmission = st.text_area("Quelle est votre vision pour la transmission du savoir-faire ? *")

            impact_local = st.text_area("Impact local & Création de valeur (Emplois, développement...) *")

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'onglet_a'
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Étape Suivante ➡️"):
                    st.session_state['form_data'].update({
                        'desc_concept': desc_concept,
                        'exp_garantie': exp_garantie,
                        'vision_transmission': vision_transmission,
                        'impact_local': impact_local
                    })
                    st.session_state['step'] = 'onglet_c'
                    st.rerun()

    # ------------------------------------------
    # ÉTAPE 5 : BESOINS FINANCIERS
    # ------------------------------------------
    elif st.session_state['step'] == 'onglet_c':
        st.subheader("Étape 5 sur 7 : Besoins Financiers & Utilisation des Fonds")
        st.progress(5 / 7)

        with st.form("form_onglet_c"):
            montant = st.number_input("Montant recherché (En FCFA ou Euros €) *", min_value=1000)
            utilisation = st.text_area("Utilisation prévue des fonds *")
            preuve_doc = st.file_uploader("Preuve de viabilité (Relevés/bilans ou devis)", type=["pdf", "png", "jpg"])

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'onglet_b'
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Étape Suivante ➡️"):
                    st.session_state['form_data'].update({
                        'montant': montant,
                        'utilisation': utilisation
                    })
                    st.session_state['step'] = 'onglet_d'
                    st.rerun()

    # ------------------------------------------
    # ÉTAPE 6 : DATA ROOM
    # ------------------------------------------
    elif st.session_state['step'] == 'onglet_d':
        st.subheader("Étape 6 sur 7 : La Data Room (Documents Joints)")
        st.progress(6 / 7)

        with st.form("form_onglet_d"):
            st.file_uploader("Plan d'affaires / Business Plan (PDF)", type=["pdf"])
            st.file_uploader("Devis équipements / Photos terrain", type=["pdf", "jpg", "png"], accept_multiple_files=True)

            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.form_submit_button("⬅️ Retour"):
                    st.session_state['step'] = 'onglet_c'
                    st.rerun()
            with col_b2:
                if st.form_submit_button("Étape Finaliser ➡️"):
                    st.session_state['step'] = 'etape_4'
                    st.rerun()

    # ------------------------------------------
    # ÉTAPE 7 : PAIEMENT & SOUMISSION
    # ------------------------------------------
    elif st.session_state['step'] == 'etape_4':
        st.subheader("Étape 7 sur 7 : Règlement des Frais d'Instruction & Soumission")
        st.progress(7 / 7)

        st.info("🔒 Vos données sont sécurisées et prêtes à être analysées.")
        st.markdown("### Règlement des frais d'instruction")
        st.write("Frais d'instruction : **50 € (environ 32 800 FCFA)**")

        pay_method = st.radio("Moyen de paiement", ["Mobile Money (MTN / Moov)", "Carte Bancaire"])

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("⬅️ Retour aux documents"):
                st.session_state['step'] = 'onglet_d'
                st.rerun()
        with col_b2:
            if st.button("💳 Payer et Soumettre mon dossier", use_container_width=True):
                id_porteur = st.session_state.get('id_porteur')
                if id_porteur:
                    id_projet = enregistrer_projet_et_paiement(
                        id_porteur,
                        st.session_state['form_data'],
                        pay_method
                    )
                    st.success(f"✅ Dossier N° {id_projet} enregistré avec succès en base de données et transmis aux analystes !")
                    st.balloons()
                else:
                    st.error("Erreur d'identification du porteur de projet. Veuillez réessayer l'Étape 2.")

# --- FOOTER SOBRE ---
st.markdown("""
    <div class='footer-container'>
        <p style='margin-bottom: 5px; font-weight: 600;'>TERRANEXA © 2026 - Plateforme d'Investissement & Économie Réelle</p>
        <p style='font-size: 0.75rem; color: #CBD5E1;'>En partenariat avec des institutions financières agréées : Ecobank | BOA | FECECAM | SGB</p>
    </div>
""", unsafe_allow_html=True)
