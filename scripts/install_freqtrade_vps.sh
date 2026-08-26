#!/usr/bin/env bash
set -euo pipefail

# install_freqtrade_vps.sh
# Script d'installation automatique pour un VPS Ubuntu 22.04
# - Installe Docker, docker-compose (plugin), git
# - Clone le dépôt FreqTrade-Deploy (utilise clé SSH déjà configurée)
# - Prépare user_data et copie le config.sample.json vers config.json
# - Démarre les conteneurs Docker

# Usage :
# 1) Copier ce script sur le VPS : curl -O https://raw.githubusercontent.com/oscardemalter/FreqTrade-Deploy/main/scripts/install_freqtrade_vps.sh
# 2) Rendre exécutable : chmod +x install_freqtrade_vps.sh
# 3) Exécuter : sudo ./install_freqtrade_vps.sh

if [ "$(id -u)" -ne 0 ]; then
  echo "Ce script doit être exécuté en tant que root ou via sudo. Ré-exécutez avec sudo." >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive

echo "Mise à jour du système..."
apt update && apt upgrade -y

echo "Installation des paquets nécessaires..."
apt install -y docker.io docker-compose git nano curl ufw

echo "Activation du service docker..."
systemctl enable --now docker

# Créer un utilisateur deploy si non existant
if id "deploy" &>/dev/null; then
  echo "L'utilisateur 'deploy' existe déjà."
else
  echo "Création de l'utilisateur 'deploy'..."
  adduser --disabled-password --gecos "" deploy
  usermod -aG sudo,ssh deploy || true
fi

# Autoriser docker pour l'utilisateur deploy
usermod -aG docker deploy || true

# Basculer en home de deploy
DEPLOY_HOME="/home/deploy"
mkdir -p "$DEPLOY_HOME"
chown deploy:deploy "$DEPLOY_HOME"

# Cloner le repo FreqTrade-Deploy (utilise SSH key ajoutée à GitHub)
su - deploy -c "bash -lc 'cd ~ && git clone git@github.com:oscardemalter/FreqTrade-Deploy.git || (cd FreqTrade-Deploy && git pull)'"

# Copier config.sample.json vers config.json si absent
if [ -f "$DEPLOY_HOME/FreqTrade-Deploy/user_data/config.sample.json" ]; then
  su - deploy -c "bash -lc 'cd ~/FreqTrade-Deploy && mkdir -p user_data/strategies && cp -n user_data/config.sample.json user_data/config.json || true'"
  echo "Fichier user_data/config.json créé à partir du sample (si absent). Éditez-le pour ajouter vos clés OKX testnet." 
else
  echo "Erreur : config.sample.json non trouvé dans le repo. Vérifiez le clonage." >&2
fi

# Démarrer docker compose
su - deploy -c "bash -lc 'cd ~/FreqTrade-Deploy && docker compose pull && docker compose up -d'"

# UFW basique
ufw allow OpenSSH
ufw --force enable

echo "Installation et démarrage terminés. Connectez-vous en tant que deploy et éditez user_data/config.json pour ajouter vos clés OKX testnet (dry_run=true)."

echo "Pour accéder à FreqUI via tunnel SSH depuis votre téléphone: utilisez un port forward local 8080 -> remote localhost:8080."

exit 0
