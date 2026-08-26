# OKX Testnet — création des clés API et insertion dans config.json

Ce document explique pas à pas comment créer des clés API sur OKX Testnet, quelles permissions donner, et où les insérer exactement dans user_data/config.json sur le VPS.

1) Accéder à OKX Testnet
- Rendez-vous sur le site OKX Testnet (recherchez "OKX Testnet" ou utilisez l'URL officielle de testnet d'OKX depuis la documentation). Créez un compte testnet si nécessaire.

2) Créer une clé API Testnet
- Dans le tableau de bord, allez dans "API Management" (ou API keys).
- Choisissez "Create API Key" (ou équivalent). Choisissez un nom identifiable (ex: freqtrade-vps-test).
- Permissions recommandées : ENABLE "Trade" (exécution d'ordres). Désactivez "Withdrawals".
- Si l'option existe, restreignez l'accès par IP en indiquant l'IP publique de votre VPS.
- Enregistrez : vous obtiendrez 3 éléments importants : API Key, Secret, Passphrase (si OKX utilise une passphrase). Sauvegardez-les immédiatement (le secret est affiché une seule fois dans de nombreux panels).

3) Exemple JSON (où placer les clés)

Ouvrez le fichier user_data/config.json sur le VPS :

nano ~/FreqTrade-Deploy/user_data/config.json

Recherchez la section "exchange" et remplissez les valeurs EXACTEMENT comme ci-dessous :

"exchange": {
  "name": "okx",
  "key": "VOTRE_API_KEY_ICI",
  "secret": "VOTRE_API_SECRET_ICI",
  "password": "VOTRE_API_PASSPHRASE_ICI",
  "ccxt_config": {},
  "ccxt_async_config": {}
},

- Remplacez VOTRE_API_KEY_ICI, VOTRE_API_SECRET_ICI et VOTRE_API_PASSPHRASE_ICI par les valeurs que vous avez récupérées depuis le site OKX Testnet.
- Sauvegardez et fermez (Ctrl+O, Enter, Ctrl+X dans nano).

4) Vérification et tests (dry_run)
- Assurez-vous que "dry_run": true dans le JSON pour éviter d'envoyer de vraies ordres sur les markets réels.
- Lancez un test de connexion via Freqtrade (commande):

# depuis le répertoire du dépôt
docker compose run --rm freqtrade --config user_data/config.json list-markets

ou essayez d'exécuter un backtest ou trade en --dry-run pour vérifier la connexion.

5) Bonnes pratiques
- NE JAMAIS stocker ces clés dans un dépôt public.
- Sauvegarder les clés dans un coffre-fort numérique (1Password, Bitwarden), ou dans un fichier chiffré, pas en clair.
- Utiliser un sous-compte OKX avec droits limités si possible.
- Surveiller les logs et alerter en cas d'activité anormale.

---

Si vous souhaitez que je crée les PDFs techniquement (conversion) et que vous voulez que je les pousse dans le repo, dites-le — je ne peux pas générer les PDFs côté serveur ici, mais j'ai ajouté le script scripts/generate_pdfs.sh pour que vous (ou le VPS) puissiez le faire en 1 commande.