import sqlite3
import hashlib

DB_NAME = "terranexa.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Table UTILISATEUR
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UTILISATEUR (
            id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            telephone TEXT NOT NULL,
            mot_de_passe_hash TEXT NOT NULL,
            est_porteur BOOLEAN DEFAULT 1,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Table PORTEUR_DE_PROJET (KYS)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PORTEUR_DE_PROJET (
            id_porteur INTEGER PRIMARY KEY AUTOINCREMENT,
            id_utilisateur INTEGER NOT NULL UNIQUE,
            profil_kys TEXT NOT NULL,
            annees_experience INTEGER NOT NULL,
            resume_parcours TEXT,
            nom_structure TEXT NOT NULL,
            pays_implantation TEXT DEFAULT 'Bénin',
            ville_implantation TEXT NOT NULL,
            FOREIGN KEY (id_utilisateur) REFERENCES UTILISATEUR (id_utilisateur) ON DELETE CASCADE
        )
    """)

    # 3. Table PROJET
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PROJET (
            id_projet INTEGER PRIMARY KEY AUTOINCREMENT,
            id_porteur INTEGER NOT NULL,
            titre_projet TEXT NOT NULL,
            niveau_maturite TEXT NOT NULL,
            secteur_activite TEXT NOT NULL,
            resume_accroche TEXT NOT NULL,
            description_concept TEXT,
            experience_garantie TEXT,
            vision_transmission TEXT,
            impact_local TEXT,
            montant_recherche REAL NOT NULL,
            utilisation_fonds TEXT,
            statut_dossier TEXT DEFAULT 'En attente de paiement',
            date_soumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_porteur) REFERENCES PORTEUR_DE_PROJET (id_porteur) ON DELETE CASCADE
        )
    """)

    # 4. Table PAIEMENT_FRAIS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PAIEMENT_FRAIS (
            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
            id_projet INTEGER NOT NULL,
            montant_frais REAL DEFAULT 50.0,
            devise TEXT DEFAULT 'EUR',
            moyen_paiement TEXT NOT NULL,
            statut_paiement TEXT NOT NULL,
            date_paiement TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_projet) REFERENCES PROJET (id_projet) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()

# --- FONCTIONS CRUD & AUTHENTIFICATION ---

def inscrire_utilisateur(nom_prenom, email, telephone, mot_de_passe, est_porteur=True):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO UTILISATEUR (nom_prenom, email, telephone, mot_de_passe_hash, est_porteur)
            VALUES (?, ?, ?, ?, ?)
        """, (nom_prenom, email, telephone, hash_password(mot_de_passe), est_porteur))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id, "Compte créé avec succès !"
    except sqlite3.IntegrityError:
        conn.close()
        return False, None, "Cette adresse e-mail est déjà utilisée."

def authentifier_utilisateur(email, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UTILISATEUR WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and user["mot_de_passe_hash"] == hash_password(mot_de_passe):
        return True, dict(user)
    return False, None

def enregistrer_porteur_kys(id_utilisateur, data):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Vérifier s'il existe déjà un profil porteur
    cursor.execute("SELECT id_porteur FROM PORTEUR_DE_PROJET WHERE id_utilisateur = ?", (id_utilisateur,))
    row = cursor.fetchone()
    
    if row:
        id_porteur = row["id_porteur"]
        cursor.execute("""
            UPDATE PORTEUR_DE_PROJET
            SET profil_kys = ?, annees_experience = ?, resume_parcours = ?, 
                nom_structure = ?, pays_implantation = ?, ville_implantation = ?
            WHERE id_porteur = ?
        """, (
            data.get('profil_kys'), data.get('years_exp', 0), data.get('resume_parcours'),
            data.get('nom_structure'), data.get('pays', 'Bénin'), data.get('ville'),
            id_porteur
        ))
    else:
        cursor.execute("""
            INSERT INTO PORTEUR_DE_PROJET (
                id_utilisateur, profil_kys, annees_experience, resume_parcours,
                nom_structure, pays_implantation, ville_implantation
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id_utilisateur, data.get('profil_kys'), data.get('years_exp', 0), data.get('resume_parcours'),
            data.get('nom_structure'), data.get('pays', 'Bénin'), data.get('ville')
        ))
        id_porteur = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return id_porteur

def enregistrer_projet_et_paiement(id_porteur, form_data, moyen_paiement):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Insertion dans PROJET
    cursor.execute("""
        INSERT INTO PROJET (
            id_porteur, titre_projet, niveau_maturite, secteur_activite,
            resume_accroche, description_concept, experience_garantie,
            vision_transmission, impact_local, montant_recherche,
            utilisation_fonds, statut_dossier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_porteur,
        form_data.get('titre_projet'),
        form_data.get('maturite'),
        form_data.get('secteur'),
        form_data.get('resume_accroche'),
        form_data.get('desc_concept'),
        form_data.get('exp_garantie', ''),
        form_data.get('vision_transmission', ''),
        form_data.get('impact_local'),
        form_data.get('montant', 0.0),
        form_data.get('utilisation'),
        'Soumis'
    ))
    id_projet = cursor.lastrowid

    # Insertion dans PAIEMENT_FRAIS
    cursor.execute("""
        INSERT INTO PAIEMENT_FRAIS (
            id_projet, montant_frais, devise, moyen_paiement, statut_paiement
        ) VALUES (?, ?, ?, ?, ?)
    """, (id_projet, 50.0, 'EUR', moyen_paiement, 'Validé'))

    conn.commit()
    conn.close()
    return id_projet
