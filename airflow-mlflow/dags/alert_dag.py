from airflow import DAG
from airflow.providers.microsoft.azure.sensors.wasb import WasbPrefixSensor
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from azure.storage.blob import ContainerClient


BLOB_CONTAINER_NAME = "quickdrawjdvpgn"
STORAGE_CONN_ID = "azure_blob_connection"
CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=jdvpgniacloudproject;AccountKey=2edSn5N29xK38a8tXgp+XKoQw3/KqfPVe1hL5jCHHWTRpa4a2RBaRAvLoQc1wMltLtwfh6MJUlrS+AStH7RzkQ==;EndpointSuffix=core.windows.net"

# 📌 Configuration du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "quickdraw_pipeline",
    default_args=default_args,
    schedule_interval=timedelta(seconds=30),  # ✅ Exécution automatique toutes les 30s
    catchup=False,
)

# 📌 1️⃣ Détection d'un NOUVEAU fichier avec `WasbPrefixSensor`
check_new_file = WasbPrefixSensor(
    task_id="check_for_new_file",
    container_name=BLOB_CONTAINER_NAME,
    prefix="",  # Détecte tous les fichiers du conteneur
    wasb_conn_id=STORAGE_CONN_ID,
    timeout=600,
    poke_interval=60,  # Vérifie toutes les 60 secondes
    mode="poke",  # Polling actif (changer en "reschedule" si besoin)
    dag=dag,
)

# 📌 2️⃣ Vérification et comptage des fichiers (sans écriture locale)
def check_file_count():
    """ Vérifie le nombre de fichiers et déclenche une alerte tous les 10 fichiers """
    container_client = ContainerClient.from_connection_string(CONNECT_STR, BLOB_CONTAINER_NAME)
    blob_list = list(container_client.list_blobs())

    file_count = len(blob_list)
    print(f"📊 Nombre total de fichiers traités : {file_count}")

    # Déclencher une alerte si le nombre total est un multiple de 10
    if file_count % 10 == 0 and file_count > 0:
        return "send_alert"
    return "skip_alert"

task_check_files = BranchPythonOperator(
    task_id="check_file_count",
    python_callable=check_file_count,
    dag=dag,
)

# 📌 3️⃣ Tâche d'alerte si 10 nouveaux fichiers détectés
def send_alert():
    print("🚨 ALERTE: 10 nouveaux fichiers traités !")

task_alert = PythonOperator(
    task_id="send_alert",
    python_callable=send_alert,
    dag=dag,
)

# 📌 Dummy task pour ignorer l’alerte si ce n’est pas un multiple de 10
skip_alert = EmptyOperator(
    task_id="skip_alert",
    dag=dag,
)

# 📌 4️⃣ Debug : Lister les fichiers détectés
def debug_blob_list():
    container_client = ContainerClient.from_connection_string(CONNECT_STR, BLOB_CONTAINER_NAME)
    blob_list = list(container_client.list_blobs())

    print("📂 Liste des fichiers détectés :", [blob.name for blob in blob_list])

task_debug_blob = PythonOperator(
    task_id="debug_blob_list",
    python_callable=debug_blob_list,
    dag=dag,
)

# 📌 Dépendances des tâches
check_new_file >> task_debug_blob >> task_check_files
task_check_files >> [task_alert, skip_alert]  # Choix dynamique (alerte ou non)