![](https://github.com/IgniteBinary/web-ihealth-api/workflows/Build/badge.svg)
# iHEALTH
Personal health software that presents various benefits in assisting health enterprises automate processes, increase productivity, and facilitate workflow management as well as help patients track their health history at a personal level. The software contains real-time, patient medical records that make information available instantly and securely to authorized users.
It also contains the medical and treatment histories of patients, the software will go beyond standard clinical data collected in a provider’s office and can be inclusive of a broader view of a patient’s care with great benefits to the medical institutions and patients. Contain a patient’s medical history, diagnoses, medications, treatment plans, immunization dates, allergies, radiology images, and laboratory and test results. Allows access to evidence-based tools that providers can use to make decisions about a patient’s care.
Automate and streamline medical providers workflow. Allows access to a pool of approved and registered doctors (serve as doctors
database) Allows on demand consulting

# INSTALLATION

1. clone repo
1. cd to root folder
1. create virtualenv
1. create test database and application database
1. `make init-app`

## to install requirements
```
make install
```

## to create new migrations
```
make migrate messsage="migration message"
```

## to update database
```
make update-db
```

## to run application
```
make run
```

## to run linter
```
make lint
```

## to run tests
```
make test
```