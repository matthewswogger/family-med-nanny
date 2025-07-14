# Family Med Nanny Service Architecture

## System Overview

This document describes the architecture of the Family Med Nanny service, a comprehensive platform for managing family medical needs and nanny services.


## High-Level Architecture

```mermaid
architecture-beta

    service slack(logos:slack-icon)[Slack MedNannyAI]%% in frontend
    service whatsapp(logos:whatsapp)%% in twilio_whatsapp
    service twilio(logos:twilio)%% in twilio_whatsapp
    service fastapi(logos:fastapi-icon)[API]%% in backend
    service core(logos:python)[Core]%% in backend
    %%service auth(logos:auth0-icon)[Authentication] in backend


service one("<img src='https://avatars.githubusercontent.com/u/110818415'>")[one]
service two("<img src='/Users/msmay/Documents/repos/family-med-nanny/pydantic_ai_dark.png'>")[two]
service two2("<img src='/Users/msmay/Documents/repos/family-med-nanny/pydantic_ai_dark.png' width=500 height=50 style='vertical-align:middle;margin:0px 0px'>")[two2]
service three("<img src='https://raw.githubusercontent.com/mingrammer/diagrams/master/assets/img/diagrams.png'>")[three]


    %%service ai(logos:medusa-icon)[AI Assistant]%% in backend
    %%service ai("<img src='https://ai.pydantic.dev/img/pydantic-ai-light.svg'>")[Assistant]%% in backend
service ai("<img src='/Users/msmay/Documents/repos/family-med-nanny/pydantic_ai_dark.png'>")[Assistant]%% in backend
    %%service ai("<img src='https://avatars.githubusercontent.com/u/110818415' style='background-color: grey; border: 10px solid black;'>")[Assistant]%% in backend




    service db(logos:sqlite)%% in data

    junction frontendcenter
    junction frontendleft
    junction frontendright

    whatsapp:L <-- R:twilio
    frontendleft:T -- B:slack
    frontendright:T -- B:twilio
    frontendleft:R -- L:frontendcenter
    frontendcenter:R -- L:frontendright
    fastapi:B --> T:core
    core:L --> R:ai
    frontendcenter:B -- T:fastapi
    core:B --> T:db



    %%group frontend(cloud)[MedNannyAI Frontend]
    %%group twilio_whatsapp(logos:whatsapp-icon)[WhatsApp MedNannyAI] in frontend
    %%group backend(logos:fastapi-icon)[MedNannyAI API Backend]
    %%frontendCenter:B -- T:fastapi{group}
    %%slack{group}:B -- T:fastapi{group}
    %%whatsapp{group}:B -- T:fastapi{group}
    %%group data(logos:aws-lambda)[Data Persistance]
```


## Service Components

### Frontend Layer
- **Slack Integration**: Real-time messaging interface for families and nannies
- **WhatsApp Integration**: Mobile messaging interface for families and nannies

### Backend Services
- **Authentication Service**: User authentication and authorization
- **User Management**: User profiles and account management
- **Medical Records**: Secure storage and management of medical information
- **Nanny Services**: Nanny profiles, scheduling, and service management
- **AI Assistant**: Intelligent assistance for medical queries and recommendations

### Data Layer
- **Database**: PostgreSQL for structured data storage
- **Cache**: Redis for session management and performance optimization
- **File Storage**: Secure storage for documents and medical records


## Data Flow

<!-- ---
config:
    theme: redux-dark-color
--- -->


```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant S as Backend Service
    participant D as Database
    participant E as External Service

    U->>F: User Action
    F->>S: API Request
    S->>S: Authenticate & Authorize
    S->>D: Query/Update Data
    D-->>S: Response
    S->>E: External Service Call (if needed)
    E-->>S: External Response
    S-->>F: API Response
    F-->>U: Update UI
```

## Security Architecture

<div style="display: flex; justify-content: space-between;">
<div style="flex: 1; margin-right: 20px;">

### Security Layers

```mermaid
graph LR
    subgraph "Security Layers"
        Auth[Authentication]
        Authz[Authorization]
        Encrypt[Encryption]
        Audit[Audit Logging]
    end

    Auth --> Authz
    Authz --> Encrypt
    Encrypt --> Audit
```

</div>
<div style="flex: 1;">

### Data Protection

```mermaid
graph LR
    subgraph "Data Protection"
        PII[PII Protection]
        HIPAA[HIPAA Compliance]
        GDPR[GDPR Compliance]
    end

    PII --> HIPAA
    HIPAA --> GDPR
```

</div>
</div>

## Deployment Architecture

```mermaid
graph TB
    subgraph "Application Tier"
        App[Application Instance]
    end

    subgraph "Database Tier"
        DB[(Database)]
    end

    subgraph "Cache Tier"
        Cache[(Cache)]
    end

    App --> DB
    App --> Cache
```

## Technology Stack

### Frontend
- Slack API Integration
- WhatsApp Business API

### Backend
- FastAPI (Python)
- PostgreSQL
- Redis
- Celery (for background tasks)

### Infrastructure
- Docker
- Single server deployment

### Monitoring
- Prometheus
- Grafana
- ELK Stack

## Next Steps

This architecture will be iteratively refined based on:
1. Specific requirements gathering
2. Performance requirements
3. Security requirements
4. Integration requirements
