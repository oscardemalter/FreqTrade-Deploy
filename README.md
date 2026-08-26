# FreqTrade Deploy

Ce dépôt contient un template prêt à l'emploi pour déployer Freqtrade sur un VPS Ubuntu avec Docker.

Contenu:
- docker-compose.yml : lance l'image officielle Freqtrade et monte ./user_data
- user_data/config.sample.json : fichier de configuration à remplir (NE PAS y mettre de vraies clés dans le repo)
- user_data/strategies/SampleStrategy.py : stratégie d'exemple (RSI)
- README.md : instructions d'installation et d'utilisation
- .gitignore : ignore user_data/config.json

Important: NE COMMITEZ JAMAIS vos vraies clés API. Utilisez user_data/config.json localement et ajoutez-le à .gitignore.
