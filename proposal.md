# Package theft warning system
#### Student Name: *Bernhard Steidl*   Student ID: *20114472*

The goal of this project is to implement a package theft warning system. When no one is at home, packages are usually left on the welcome mat. This system will use piezo sensors to monitor if a package is placed on the mat and send a notification via Blynk to the homeowner.

Additionally, a Raspberry Pi Camera will continuously monitor the welcome mat. If the package is removed (indicated by a change in piezo sensor values), the system will capture and upload video footage of the moments before and after the event to Azure Cloud. The homeowner will receive a notification with a link to the recorded footage via Blynk.

## Tools, Technologies and Equipment

### RaspberryPI with Camera
- Implement logic to differentiate between people and packages.

  - A package is identified if the piezo sensor values remain above a certain threshold for a specific duration without 
    significant fluctuation.

  - A person is identified by continuous changes in the piezo sensor values due to movement.

### Azure functions
- Receive sensor data from the Raspberry Pi via Event Hub.
- Store data in a database
- Notify the user via Blynk when an event occurs.

### Azure Databases
    Use a time-series database to store piezo sensor data.
    Use Azure Blob Storage to store recorded video footage.

### Blynk
- Notify the user in case of package theft and provide a link to the recorded video.

### Miscellaneous
The project will primarily use Python for both the Raspberry Pi logic and Azure Functions.


## Project Repository
https://github.com/BernH4/package_theft_warning_system


## Open Questions:
- Should the logic to differentiate persons and packages be handled on the pi or in an azure function? It probably makes more sense to do it on the pi, because azure functions are stateless and we need  historic data for differentiation.
- Is the Azure Function really needed? Data ingestion to the database and sending messages via blynk could be done on the pi directly
