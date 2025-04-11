
### In Fabric:
1. Create Data Ingestion and Ingestion Logs workspaces
2. Create Fabric lakehouse Bronze
3. Create IngestionLogs KQL DB
4. Give SPN Contributor access to workspaces
5. Give SPN admin rights to DB:
.add database 'IngestionLogs' admins ('aadapp=<application_id of SPN>')