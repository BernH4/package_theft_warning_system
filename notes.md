1. Create resource group:
az group create --name package_theft --location northeurope

2. https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-portal
Storage Account -> Data Storage -> Containers -> Create Container: packagetheftcontainerbst




CHANGES:
Upload to Blob storage directly from pi, use azure function to generate url and send to user



# Maybe use queue for video processing and then azure function for telegram api 
Or instead of queue trigger azure function after video upload


Grafana managed or docker deploy? -> Managed to expensive, free version does not allow plugins to get data from influxdb or similar


Log events on time series database
web applicaton that react to this events

log the events!



TODO:
- Extract the Telegram API as Azure Function (Just send mqtt with the link) so other services like whatsapp or webapp could be added
