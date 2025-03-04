FROM continuumio/miniconda3

# Définir le répertoire de travail
WORKDIR /root/airflow

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier les dossiers et fichiers nécessaires
COPY dags/ dags/
COPY plugins/ plugins/
COPY airflow.db .

# Définir les variables d'environnement à partir des arguments
ENV AWS_ACCESS_KEY_ID=AKIAQ3EGWSOML5RMTDO2
ENV AWS_SECRET_ACCESS_KEY=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


ENV PYTHONASYNCIODEBUG=1
# Commande pour démarrer Airflow
CMD airflow standalone

