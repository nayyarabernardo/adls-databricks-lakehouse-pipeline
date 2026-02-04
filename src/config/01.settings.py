# Template: copie para src/config/settings.py antes de executar.

# Configurações do Azure Storage
STORAGE_ACCOUNT_NAME = "{STORAGE_ACCOUNT_NAME}"
CONTAINER_NAME = "{CONTAINER_NAME}"
PROJECT_NAME = "{PROJECT_NAME}"

# Base URL
BASE_URL = f"abfss://{CONTAINER_NAME}@{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"

# External Location
EXTERNAL_LOCATION = BASE_URL

# Layer Paths
BRONZE_PATH = f"{BASE_URL}/{PROJECT_NAME}/bronze/"
SILVER_PATH = f"{BASE_URL}/{PROJECT_NAME}/silver/"
GOLD_PATH = f"{BASE_URL}/{PROJECT_NAME}/gold/"

# Resource Paths
RESOURCE_PATH = f"{BASE_URL}/{PROJECT_NAME}/resource/origem/"
RESOURCE_VOLUME_PATH = f"/Volumes/{PROJECT_NAME}/logistics/{PROJECT_NAME}_resource/origem/"

# Layer Paths Dictionary
LAYER_PATHS = {
    "bronze": f"{BASE_URL}/{PROJECT_NAME}/bronze",
    "silver": f"{BASE_URL}/{PROJECT_NAME}/silver",
    "gold": f"{BASE_URL}/{PROJECT_NAME}/gold"
}

# Metadata Path
METADATA_BASE_PATH = f"{BASE_URL}/{PROJECT_NAME}/resource/metadata"
