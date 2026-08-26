# Guide d'installation et d'utilisation de Freqtrade sur un VPS (Ubuntu 22.04)

Ce guide détaille, pas à pas et de façon précise, toutes les commandes à exécuter depuis votre téléphone (via SSH) pour préparer un VPS, cloner le dépôt, configurer Freqtrade, démarrer les conteneurs Docker et accéder à l'interface web (FreqUI) en tunnel SSH.

Important — sécurité :
- NE JAMAIS mettre vos clés API en clair dans un dépôt.
- user_data/config.json est listé dans .gitignore du dépôt FreqTrade-Deploy ; conservez ce fichier uniquement sur le VPS.
- Commencez toujours avec dry_run=true et sur le testnet OKX.

Pré-requis :
- VPS Ubuntu 22.04 (1 vCPU, 1–2GB RAM suffisent pour tests).
- Accès SSH (utilisateur ubuntu ou root) depuis votre téléphone (Termius, JuiceSSH, Termux).
- Clé SSH publique de votre VPS ajoutée à votre compte GitHub (recommandé) pour cloner le repo privé.

Structure du guide :
1) Première connexion et préparation du VPS
2) Installation Docker, docker-compose, git
3) Clonage du repo et préparation des fichiers
4) Configuration (édition de user_data/config.json)
5) Démarrage des containers et lancement du bot en paper
6) Accès sécurisé à l'interface web (tunnel SSH)
7) Commandes de gestion (logs, arrêt, update)
8) Checklist de sécurité

---

1) Première connexion et sécurité SSH

Sur votre téléphone, ouvrez votre client SSH (Termius recommandé). Connectez‑vous au VPS :

ssh ubuntu@VPS_IP

Si c'est la première connexion, acceptez l'empreinte. Vérifiez ensuite votre identité :

whoami
lsb_release -a

Créer un utilisateur non-root si vous utilisez root (optionnel mais recommandé) :

# sur le VPS en root
adduser deploy
usermod -aG sudo deploy

Ensuite, configurez l'authentification par clé SSH :

# Sur votre machine locale (ou sur le VPS) :
ssh-keygen -t ed25519 -C "deploy@vps"   # puis copiez la clé publique
cat ~/.ssh/id_ed25519.pub

Collez la clé publique dans GitHub → Settings → SSH and GPG keys → New SSH key.

---

2) Installer Docker, docker-compose, git et outils de base

Exécutez ces commandes sur le VPS (copier/coller) :

sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git nano curl ufw
sudo systemctl enable --now docker

# Optionnel : permettre l'utilisation de docker sans sudo (relogin nécessaire)
sudo usermod -aG docker $USER

Note : si vous utilisez la commande usermod pour ajouter $USER au groupe docker, déconnectez puis reconnectez votre session SSH pour prendre effet.

---

3) Cloner le dépôt FreqTrade-Deploy et préparer user_data

Si vous avez ajouté la clé SSH du VPS à GitHub, clonez le dépôt privé :

cd ~
# Clone du repo d'assets
git clone git@github.com:oscardemalter/FreqTrade-Deploy.git
cd FreqTrade-Deploy

Créer le dossier user_data/strategies et copier le sample en config.json :

mkdir -p user_data/strategies
cp user_data/config.sample.json user_data/config.json

Éditez user_data/config.json avec nano :

nano user_data/config.json

Remplacez les placeholders YOUR_API_KEY, YOUR_API_SECRET, YOUR_API_PASSPHRASE par vos clés OKX testnet (instructions pour créer ces clés dans le document OKX_Testnet_Keys.md fourni dans ce repo).
Assurez-vous que "dry_run": true.

---

4) Commandes Docker : construire et démarrer

Construire (pull) et démarrer les conteneurs :

docker compose pull
docker compose up -d

overifier l'état :

docker compose ps

Si un conteneur n'est pas démarré ou crash, consultez les logs (voir section 6).

---

5) Lancer la stratégie d'exemple en mode paper (dry-run)

Pour exécuter une session de trading en paper pour tester la stratégie SampleStrategy.py fournie :

# commande exécutée depuis le répertoire FreqTrade-Deploy
docker compose run --rm freqtrade trade --config user_data/config.json --strategy SampleStrategy --dry-run

Cette commande démarre un conteneur temporaire qui exécute le bot. Pour un fonctionnement permanent, vous pouvez configurer le service dans docker-compose.yml pour exécuter le process de trading au démarrage.

Logs en temps réel :

docker compose logs -f

Arrêter les services :

docker compose down

---

6) Accès sécurisé à l'interface web (FreqUI) via tunnel SSH

Le docker-compose fourni lie FreqUI sur 127.0.0.1:8080 (sécurisé localement). Pour y accéder depuis votre téléphone :

Option A - Termius (interface graphique) :
- Ouvrez la connexion SSH vers votre VPS dans Termius
- Éditez la connexion -> Port Forwarding -> Local 8080 -> Remote localhost:8080
- Connectez, puis ouvrez http://localhost:8080 dans le navigateur de votre téléphone

Option B - Tunnel SSH via Termux / OpenSSH (ligne de commande) :

ssh -L 8080:localhost:8080 ubuntu@VPS_IP

Puis, en gardant la session SSH ouverte, ouvrez votre navigateur mobile à l'adresse : http://localhost:8080

---

7) Mise à jour, sauvegardes et bonnes pratiques

Mettre à jour Freqtrade (depuis le dossier freqtrade cloné) :

# si vous avez cloné le dépôt upstream freqtrade
cd ~/freqtrade
git fetch --all
git checkout stable
git pull origin stable

Si vous utilisez l'image Docker officielle (recommandé), vous pouvez simplement :

docker compose pull
docker compose up -d --force-recreate

Sauvegarder votre configuration (sur VPS local, hors repo) :

cp user_data/config.json ~/backups/config.json.$(date +"%Y%m%d_%H%M%S")

---

8) Checklist de sécurité rapide

- Toujours dry_run=true lors des tests
- Ne jamais activer l'option de retrait sur vos API keys
- Restreindre IP si possible lors de la création de l'API key
- Garder user_data/config.json dans .gitignore
- Installer ufw et autoriser uniquement SSH :

sudo ufw allow OpenSSH
sudo ufw enable

---

Annexe : commandes utiles résumé

# update & docker
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io docker-compose git nano
sudo systemctl enable --now docker

# clone repo
cd ~
git clone git@github.com:oscardemalter/FreqTrade-Deploy.git
cd FreqTrade-Deploy

# prepare config
mkdir -p user_data/strategies
cp user_data/config.sample.json user_data/config.json
nano user_data/config.json

# start
docker compose pull
docker compose up -d

docker compose run --rm freqtrade trade --config user_data/config.json --strategy SampleStrategy --dry-run

docker compose logs -f

docker compose down

---

Fin du guide. Vous pouvez générer le PDF de ce guide avec le script scripts/generate_pdfs.sh que j'ai ajouté au dépôt (commande : bash scripts/generate_pdfs.sh).