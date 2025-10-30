# HR Analytics Cloud Platform 
## Projektöversikt
En automatiserad plattform för analys av jobbannonser med ETL-pipeline och interaktiv dashboard, deployad i Azure Cloud.

## Syfte
Plattformen löser följande problem:

- Snabb marknadsanalys - Spåra trender inom IT-rekrytering i realtid
- Data-drivna beslut - Hjälp HR-specialister och kandidater med aktuell marknadsdata
- Automatisering - Eliminera manuell datainsamling och analys


## Arkitektur
```
Arbetsförmedlingen API → Python ETL → DuckDB → dbt → Streamlit Dashboard
   
              ↓
         Dagster (orkestrering)
              ↓
         Azure Container Instances
```

### Komponenter:

- **Data Ingestion** - Hämtar jobbannonser 
- **ETL Pipeline** - Transformerar och laddar data till DuckDB
- **Data Warehouse** - DuckDB-databas i Azure File Share
- **Orchestration** - Dagster för pipeline-hantering
- **Dashboard** - Streamlit för visualisering och analys

---

## Teknisk Stack

### Backend:
- **Python 3.11** - Huvudprogrammeringsspråk
- **DuckDB** - OLAP-databas för analytiska queries
- **dbt (data build tool)** - Data transformations
- **Dagster** - Workflow orchestration

### Frontend:
- **Streamlit** - Interaktiv dashboard

### Cloud Infrastructure:
- **Azure Container Registry (ACR)** - Docker image storage
- **Azure Container Instances (ACI)** - Container hosting
- **Azure Storage Account** - File Share för DuckDB
- **Terraform** - Infrastructure as Code (IaC)

---

## Projektstruktur
```
hr-analytics-cloud-deployment/
├── terraform/                 # Infrastructure as Code
│   ├── main.tf               # Azure resources definition
│   ├── variables.tf          # Terraform variables
│   └── outputs.tf            # Output values
│
├── orchestration/            # Dagster orchestration
│   └── definitions.py        # Pipeline definitions
│
├── dashboard/                # Streamlit dashboard
│   ├── dashboard.py          # Main dashboard app
│   └── conn_warehouse.py     # DuckDB connection
│
├── dbt/                      # Data transformations
│   └── models/               # dbt models
│
├── dockerfile.dwh            # DWH Pipeline container
├── dockerfile.dashboard      # Dashboard container
├── requirements.txt          # Python dependencies
└── main.py                   # ETL entry point
```

## Installation och Deployment
Förutsättningar:

- Azure CLI - installerad och konfigurerad
- Terraform - version ~> 1.12
- Docker - för att bygga images
- Python 3.11 - för lokal utveckling

1. Klona projektet:
- git clone <repository-url>
- cd hr-analytics-cloud-deployment

2. Konfigurera Azure:
az login

3. Sätt subscription:
az account set --subscription "subscription id"

4. Deploy Infrastructure:
cd terraform

5. Initiera Terraform:
terraform init

6. Granska planen:
terraform plan

7. Applicera (skapar ACR + Storage): terraform apply

8. Bygg och pusha Docker Images
- cd ..

- Logga in på ACR: az acr login --name craihrnalyticsdevterr

- Bygg images:
  
  docker build -f dockerfile.dwh -t craihrnalyticsdevterr.azurecr.io/hr-pipeline:latest .
  
  docker build -f dockerfile.dashboard -t craihrnalyticsdevterr.azurecr.io/dashboard:latest .

- Pusha till ACR:

  docker push craihrnalyticsdevterr.azurecr.io/hr-pipeline:latest

  docker push craihrnalyticsdevterr.azurecr.io/dashboard:latest

9. Deploy Containers
- cd terraform
- Avkommentera container blocks i main.tf
- Applicera igen för att skapa containers
- terraform apply

---

## Åtkomst till Tjänster

### Dagster UI (ETL Pipeline):

http://dwh-pipeline-dev.swedencentral.azurecontainer.io:3000


**Användning:**
1. Öppna Dagster UI
2. Navigera till Assets/Jobs
3. Klicka "Materialize" för att köra ETL
4. Övervaka körningen i realtid

### Streamlit Dashboard:

http://dashboard-dev.swedencentral.azurecontainer.io:8501


## Underhåll
### Uppdatera kod:
bash# Bygg nya images
docker build -f dockerfile.dwh -t craihrnalyticsdevterr.azurecr.io/hr-pipeline:latest .
docker build -f dockerfile.dashboard -t craihrnalyticsdevterr.azurecr.io/dashboard:latest .

### Pusha
docker push craihrnalyticsdevterr.azurecr.io/hr-pipeline:latest
docker push craihrnalyticsdevterr.azurecr.io/dashboard:latest

### Starta om containers
az container restart \
  --resource-group rg-ai-hr-analytics-dev-terr \
  --name dwh-pipeline-ci

az container restart \
  --resource-group rg-ai-hr-analytics-dev-terr \
  --name dashboard-ci
Skala resurser:
Redigera terraform/main.tf:
terraformcpu    = "4"      # Öka CPU
memory = "8"      # Öka minne
Applicera:
terraform apply


## Best Practices för Produktion:

- Använd Azure Key Vault för secrets
- Aktivera Private Endpoints för ACR och Storage
- Implementera RBAC för åtkomstkontroll
- Aktivera Azure Monitor för logging
- Backup strategy för DuckDB-databasen

## Dokumentation

- Dagster Docs: https://docs.dagster.io
- dbt Docs: https://docs.getdbt.com
- DuckDB Docs: https://duckdb.org/docs
- Streamlit Docs: https://docs.streamlit.io
- Azure Docs: https://docs.microsoft.com/azure
- Terraform Azure Provider: https://registry.terraform.io/providers/hashicorp/azurerm


Skapad: Oktober 2025
