# Family Med Nanny - Architecture Diagram

## System Overview

This is a medication management SMS service built with FastAPI that allows users to manage their medications through text messages using Twilio.

```mermaid
graph TB
    %% External Services
    subgraph "External Services"
        TWILIO[Twilio SMS Service]
        USER[User Phone]
    end

    %% Infrastructure Layer
    subgraph "Infrastructure"
        ENV[Environment Variables<br/>.env file]
        LOG[Logging System]
    end

    %% Application Layer
    subgraph "FastAPI Application"
        WEBHOOK[Webhook Handler<br/>/webhook/sms]
        PARSER[Message Parser<br/>Natural Language Processing]
        MANAGER[MedicationManager<br/>Business Logic]
        API[API Endpoints<br/>/medications/phone<br/>/logs/phone]
    end

    %% Data Layer
    subgraph "Data Storage"
        MEMORY[In-Memory Storage<br/>medications: dict<br/>logs: list<br/>users: dict]
        DB[(Future: Database<br/>SQLAlchemy + PostgreSQL)]
    end

    %% User Interface
    subgraph "User Interface"
        SMS[SMS Commands<br/>ADD, TAKE, LIST, TODAY, HELP]
        NATURAL[Natural Language<br/>I took my aspirin]
    end

    %% Connections
    USER <-->|SMS Messages| TWILIO
    TWILIO -->|POST /webhook/sms| WEBHOOK
    WEBHOOK --> PARSER
    PARSER --> MANAGER
    MANAGER --> MEMORY
    API --> MEMORY

    %% Environment and Logging
    ENV --> WEBHOOK
    ENV --> MANAGER
    LOG --> WEBHOOK
    LOG --> MANAGER

    %% Future Database
    MEMORY -.->|Future Migration| DB

    %% Styling
    classDef external fill:#e1f5fe
    classDef app fill:#f3e5f5
    classDef data fill:#e8f5e8
    classDef infra fill:#fff3e0

    class TWILIO,USER external
    class WEBHOOK,PARSER,MANAGER,API app
    class MEMORY,DB data
    class ENV,LOG infra
```

## Detailed Component Architecture

```mermaid
graph LR
    %% Message Flow
    subgraph "Message Processing Flow"
        SMS_IN[Incoming SMS]
        PARSE[Parse Message]
        INTENT[Extract Intent]
        PROCESS[Process Action]
        RESPONSE[Generate Response]
        SMS_OUT[Outgoing SMS]
    end

    %% Intent Types
    subgraph "Supported Intents"
        ADD[ADD Medication]
        TAKE[TAKE Medication]
        LIST[List Medications]
        TODAY[Today's Logs]
        HELP[Help Message]
    end

    %% Business Logic
    subgraph "MedicationManager Class"
        ADD_MED[add_medication]
        LOG_MED[log_medication_taken]
        LIST_MED[list_medications]
        LIST_LOGS[list_today_logs]
        HELP_MSG[help_message]
    end

    %% Data Models
    subgraph "Data Structures"
        MED_DATA[Medication Data<br/>name, dosage, frequency, added_date]
        LOG_DATA[Log Entry<br/>phone_number, medication, dosage, taken_at]
        USER_DATA[User Data<br/>phone_number -> medications]
    end

    %% Flow Connections
    SMS_IN --> PARSE
    PARSE --> INTENT
    INTENT --> ADD
    INTENT --> TAKE
    INTENT --> LIST
    INTENT --> TODAY
    INTENT --> HELP

    ADD --> ADD_MED
    TAKE --> LOG_MED
    LIST --> LIST_MED
    TODAY --> LIST_LOGS
    HELP --> HELP_MSG

    ADD_MED --> MED_DATA
    LOG_MED --> LOG_DATA
    LIST_MED --> USER_DATA
    LIST_LOGS --> LOG_DATA

    PROCESS --> RESPONSE
    RESPONSE --> SMS_OUT

    %% Styling
    classDef flow fill:#e3f2fd
    classDef intent fill:#fce4ec
    classDef logic fill:#f1f8e9
    classDef data fill:#fff8e1

    class SMS_IN,PARSE,INTENT,PROCESS,RESPONSE,SMS_OUT flow
    class ADD,TAKE,LIST,TODAY,HELP intent
    class ADD_MED,LOG_MED,LIST_MED,LIST_LOGS,HELP_MSG logic
    class MED_DATA,LOG_DATA,USER_DATA data
```

## API Endpoints Architecture

```mermaid
graph TB
    %% FastAPI App
    subgraph "FastAPI Application"
        APP[FastAPI App<br/>title: Medication Management SMS API]

        subgraph "Endpoints"
            WEBHOOK_ENDPOINT[POST /webhook/sms<br/>Twilio Webhook Handler]
            HEALTH_ENDPOINT[GET /<br/>Health Check]
            MED_ENDPOINT[GET /medications/phone_number<br/>Debug: Get Medications]
            LOGS_ENDPOINT[GET /logs/phone_number<br/>Debug: Get Logs]
        end

        subgraph "Request/Response"
            TWIML_RESPONSE[TwiML Response<br/>XML Format]
            JSON_RESPONSE[JSON Response<br/>Debug Data]
            PLAIN_RESPONSE[Plain Text<br/>Health Status]
        end
    end

    %% External Dependencies
    subgraph "Dependencies"
        TWILIO_LIB[Twilio Library<br/>twilio.rest.Client]
        FASTAPI_LIB[FastAPI<br/>Web Framework]
        UVICORN[Uvicorn<br/>ASGI Server]
    end

    %% Connections
    TWILIO_LIB --> WEBHOOK_ENDPOINT
    FASTAPI_LIB --> APP
    UVICORN --> APP

    WEBHOOK_ENDPOINT --> TWIML_RESPONSE
    MED_ENDPOINT --> JSON_RESPONSE
    LOGS_ENDPOINT --> JSON_RESPONSE
    HEALTH_ENDPOINT --> PLAIN_RESPONSE

    %% Styling
    classDef app fill:#e8eaf6
    classDef endpoint fill:#c8e6c9
    classDef response fill:#fff3e0
    classDef dep fill:#fce4ec

    class APP app
    class WEBHOOK_ENDPOINT,MED_ENDPOINT,LOGS_ENDPOINT,HEALTH_ENDPOINT endpoint
    class TWIML_RESPONSE,JSON_RESPONSE,PLAIN_RESPONSE response
    class TWILIO_LIB,FASTAPI_LIB,UVICORN dep
```

## Deployment Architecture

```mermaid
graph TB
    %% Development Environment
    subgraph "Development"
        DEV_SERVER[Local FastAPI Server<br/>localhost:8000]
        NGROK[Ngrok Tunnel<br/>Public HTTPS URL]
        DEV_TWILIO[Twilio Webhook<br/>ngrok.io/webhook/sms]
    end

    %% Production Environment
    subgraph "Production"
        PROD_SERVER[Production Server<br/>Heroku/Railway]
        PROD_TWILIO[Twilio Webhook<br/>your-domain.com/webhook/sms]
        ENV_VARS[Environment Variables<br/>TWILIO_ACCOUNT_SID<br/>TWILIO_AUTH_TOKEN<br/>TWILIO_PHONE_NUMBER]
    end

    %% Database Options
    subgraph "Storage Options"
        CURRENT[Current: In-Memory<br/>Python dictionaries]
        FUTURE[Future: Database<br/>SQLAlchemy + PostgreSQL]
    end

    %% Connections
    DEV_SERVER --> NGROK
    NGROK --> DEV_TWILIO

    PROD_SERVER --> PROD_TWILIO
    ENV_VARS --> PROD_SERVER

    CURRENT --> DEV_SERVER
    CURRENT --> PROD_SERVER
    FUTURE -.->|Migration Path| PROD_SERVER

    %% Styling
    classDef dev fill:#e1f5fe
    classDef prod fill:#f3e5f5
    classDef storage fill:#e8f5e8

    class DEV_SERVER,NGROK,DEV_TWILIO dev
    class PROD_SERVER,PROD_TWILIO,ENV_VARS prod
    class CURRENT,FUTURE storage
```

## Key Features

- **SMS Integration**: Twilio webhook handles incoming/outgoing SMS
- **Natural Language Processing**: Understands both structured commands and natural language
- **In-Memory Storage**: Fast access to medication and log data
- **RESTful API**: Debug endpoints for data inspection
- **Async Processing**: FastAPI handles concurrent requests
- **Environment Configuration**: Secure credential management
- **Logging**: Comprehensive request and error logging

## Technology Stack

- **Backend**: FastAPI (Python)
- **SMS Service**: Twilio
- **Server**: Uvicorn (ASGI)
- **Storage**: In-memory (Python dictionaries)
- **Configuration**: python-dotenv
- **Future**: SQLAlchemy + PostgreSQL
