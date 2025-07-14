# Family Med Nanny Service Architecture

## System Overview

This document describes the architecture of the Family Med Nanny service, a comprehensive platform for managing family medical needs and nanny services.




## High-Level Architecture
![High-Level Arcchitecture](mermaid_png_files/high_level_arch.png)

<details>

<summary>This hides a single Mermaid code block that github has issues rendering correctly. The above PNG is the correct representation of the diagram as it should render. Including a PNG of the diagram is an efficient solution. If you want to see the error, take a look.</summary>

```mermaid
architecture-beta

    service slack(logos:slack-icon)[Slack MedNannyAI]
    service whatsapp(logos:whatsapp)
    service twilio(logos:twilio)
    service fastapi(logos:fastapi-icon)[API]
    service core(logos:python)[Core]
    service auth(logos:auth0-icon)[Authn Authz]

    %%service ai(logos:medusa-icon)[MedNannyAI Assistant]
    service ai("<img src='https://avatars.githubusercontent.com/u/110818415' style='background-color:black;vertical-align:middle;margin:0px 0px'>")[MedNannyAI Assistant]

    service llm(logos:anthropic-icon)[LLM Provider]
    service db(logos:sqlite)

    junction frontendcenter
    junction frontendleft
    junction frontendright

    whatsapp:L <-- R:twilio
    frontendleft:T -- B:slack
    frontendright:T -- B:twilio
    frontendleft:R -- L:frontendcenter
    frontendcenter:R -- L:frontendright
    fastapi:B --> T:core
    fastapi:R --> L:auth
    core:L --> R:ai
    ai:L --> R:llm
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
</details>

## Service Components

### Frontend Layer
- **Slack Integration**: Real-time messaging interface on mobile/desktop/web
- **WhatsApp Integration**: Mobile messaging interface

### Backend Services
- **Authentication Service**: User authentication and authorization
- **User Management**: User profiles and account management
- **Medical Records**: Secure storage and management of medical information
- **Nanny Services**: Nanny profiles, scheduling, and service management
- **AI Assistant**: Intelligent assistance for medical queries and recommendations

### Data Layer
- **Database**: PostgreSQL for structured data storage
- **Cache**: Redis for session management and performance optimization

<<<<<<< HEAD

=======
>>>>>>> feature/fastapi-module
## Data Flow
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

```mermaid
flowchart TB
    subgraph "Data Protection"
        PII[PII Protection]
        HIPAA[HIPAA Compliance]
        GDPR[GDPR Compliance]
        direction TB
        PII-->HIPAA
        HIPAA-->GDPR
    end

    subgraph "Security Layers"
        Auth[Authentication]
        Authz[Authorization]
        Encrypt[Encryption]
        Audit[Audit Logging]
        direction TB
        Auth-->Authz
        Authz-->Encrypt
        Encrypt-->Audit
    end
```

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
- FastAPI
- sqlite
- Pydantic AI
- Anthropic and/or OpenAI
- Redis (maybe, probably in memory caching or just go with sql db caching...it's fast enough)

### Infrastructure
- Docker
- [Railway](https://railway.com/) for deployment and monitoring
- [Twilio](https://www.twilio.com/) for communication using mobile phone numbers
- Single server deployment

### Monitoring
- [Railway](https://railway.com/) should give me what I need for something of this scope out of the box.


## Next Steps

This architecture will be iteratively refined based on:
1. Specific requirements gathering
2. Performance requirements
3. Security requirements
4. Integration requirements
