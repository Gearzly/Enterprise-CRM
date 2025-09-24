# SaaS CRM Backend - API Quick Reference

## Base URL
```
http://localhost:8001
```

## Authentication
All protected endpoints require OAuth 2.0 with PKCE authentication.
- **Auth Endpoint**: `/auth/login`
- **Token Refresh**: `/auth/refresh`
- **Token Revoke**: `/auth/logout`

## Core Endpoints

### System Health
```
GET /health              # System health check
GET /                    # API root with module information
GET /search?q={query}    # Global search across all modules
```

### Sales Module (`/sales`)
```
GET    /sales/                     # Sales dashboard
GET    /sales/metrics              # Sales metrics
GET    /sales/data                 # Sales data for charts
GET    /sales/activities           # Recent activities
GET    /sales/customers            # Customer data

# Activities
GET    /sales/activities/
POST   /sales/activities/
GET    /sales/activities/{id}
PUT    /sales/activities/{id}
DELETE /sales/activities/{id}

# Contacts
GET    /sales/contacts/
POST   /sales/contacts/
GET    /sales/contacts/{id}
PUT    /sales/contacts/{id}
DELETE /sales/contacts/{id}

# Leads
GET    /sales/leads/
POST   /sales/leads/
GET    /sales/leads/{id}
PUT    /sales/leads/{id}
DELETE /sales/leads/{id}
GET    /sales/leads/status/{status}
GET    /sales/leads/config/statuses
GET    /sales/leads/config/sources

# Opportunities
GET    /sales/opportunities/
POST   /sales/opportunities/
GET    /sales/opportunities/{id}
PUT    /sales/opportunities/{id}
DELETE /sales/opportunities/{id}
GET    /sales/opportunities/stage/{stage}
GET    /sales/opportunities/config/stages

# Quotations
GET    /sales/quotations/
POST   /sales/quotations/
GET    /sales/quotations/{id}
PUT    /sales/quotations/{id}
DELETE /sales/quotations/{id}
GET    /sales/quotations/status/{status}
GET    /sales/quotations/config/statuses

# Reports
GET    /sales/reports/sales
GET    /sales/reports/sales/metrics

# Targets
GET    /sales/targets/
POST   /sales/targets/
GET    /sales/targets/{id}
PUT    /sales/targets/{id}
DELETE /sales/targets/{id}
GET    /sales/forecasts/
GET    /sales/forecasts/current
```

### Marketing Module (`/marketing`)
```
GET    /marketing/                 # Marketing dashboard

# Campaigns
GET    /marketing/campaigns/
POST   /marketing/campaigns/
GET    /marketing/campaigns/{id}
PUT    /marketing/campaigns/{id}
DELETE /marketing/campaigns/{id}

# Leads
GET    /marketing/leads/
POST   /marketing/leads/
GET    /marketing/leads/{id}
PUT    /marketing/leads/{id}
DELETE /marketing/leads/{id}

# Email
GET    /marketing/email/
POST   /marketing/email/
GET    /marketing/email/{id}
PUT    /marketing/email/{id}
DELETE /marketing/email/{id}

# Social Media
GET    /marketing/social-media/
POST   /marketing/social-media/
GET    /marketing/social-media/{id}
PUT    /marketing/social-media/{id}
DELETE /marketing/social-media/{id}

# Content
GET    /marketing/content/
POST   /marketing/content/
GET    /marketing/content/{id}
PUT    /marketing/content/{id}
DELETE /marketing/content/{id}

# Analytics
GET    /marketing/analytics/
GET    /marketing/analytics/{id}

# Automation
GET    /marketing/automation/
POST   /marketing/automation/
GET    /marketing/automation/{id}
PUT    /marketing/automation/{id}
DELETE /marketing/automation/{id}

# Segmentation
GET    /marketing/segmentation/
POST   /marketing/segmentation/
GET    /marketing/segmentation/{id}
PUT    /marketing/segmentation/{id}
DELETE /marketing/segmentation/{id}

# Events
GET    /marketing/events/
POST   /marketing/events/
GET    /marketing/events/{id}
PUT    /marketing/events/{id}
DELETE /marketing/events/{id}

# Partners
GET    /marketing/partners/
POST   /marketing/partners/
GET    /marketing/partners/{id}
PUT    /marketing/partners/{id}
DELETE /marketing/partners/{id}

# Resources
GET    /marketing/resources/
POST   /marketing/resources/
GET    /marketing/resources/{id}
PUT    /marketing/resources/{id}
DELETE /marketing/resources/{id}

# CDP
GET    /marketing/cdp/
GET    /marketing/cdp/{id}
```

### Support Module (`/support`)
```
GET    /support/                   # Support dashboard
GET    /support/metrics            # Support metrics
GET    /support/tickets            # Support tickets

# Tickets
GET    /support/tickets/
POST   /support/tickets/
GET    /support/tickets/{id}
PUT    /support/tickets/{id}
DELETE /support/tickets/{id}

# Knowledge Base
GET    /support/knowledge-base/
POST   /support/knowledge-base/
GET    /support/knowledge-base/{id}
PUT    /support/knowledge-base/{id}
DELETE /support/knowledge-base/{id}

# Interactions
GET    /support/interactions/
POST   /support/interactions/
GET    /support/interactions/{id}
PUT    /support/interactions/{id}
DELETE /support/interactions/{id}

# Live Chat
GET    /support/live-chat/
POST   /support/live-chat/
GET    /support/live-chat/{id}

# Call Center
GET    /support/call-center/
POST   /support/call-center/
GET    /support/call-center/{id}

# Social Support
GET    /support/social-support/
POST   /support/social-support/
GET    /support/social-support/{id}

# Feedback
GET    /support/feedback/
POST   /support/feedback/
GET    /support/feedback/{id}
PUT    /support/feedback/{id}
DELETE /support/feedback/{id}

# SLA
GET    /support/sla/
POST   /support/sla/
GET    /support/sla/{id}
PUT    /support/sla/{id}
DELETE /support/sla/{id}

# Asset
GET    /support/asset/
POST   /support/asset/
GET    /support/asset/{id}
PUT    /support/asset/{id}
DELETE /support/asset/{id}

# Remote
GET    /support/remote/
POST   /support/remote/
GET    /support/remote/{id}

# Community
GET    /support/community/
POST   /support/community/
GET    /support/community/{id}

# Reporting
GET    /support/reporting/
GET    /support/reporting/{id}

# Automation
GET    /support/automation/
POST   /support/automation/
GET    /support/automation/{id}
PUT    /support/automation/{id}
DELETE /support/automation/{id}

# Mobile
GET    /support/mobile/
GET    /support/mobile/{id}

# Integration
GET    /support/integration/
POST   /support/integration/
GET    /support/integration/{id}
PUT    /support/integration/{id}
DELETE /support/integration/{id}

# Language
GET    /support/language/
GET    /support/language/{id}
```

### Super Admin Panel (`/api/superadmin`)
```
GET    /api/superadmin/            # Super Admin dashboard

# Organizations
GET    /api/superadmin/organizations/
POST   /api/superadmin/organizations/
GET    /api/superadmin/organizations/{id}
PUT    /api/superadmin/organizations/{id}
DELETE /api/superadmin/organizations/{id}
POST   /api/superadmin/organizations/{id}/suspend
POST   /api/superadmin/organizations/{id}/activate

# Security - Roles
GET    /api/superadmin/security/roles/
POST   /api/superadmin/security/roles/
GET    /api/superadmin/security/roles/{id}
PUT    /api/superadmin/security/roles/{id}
DELETE /api/superadmin/security/roles/{id}

# Security - Permissions
GET    /api/superadmin/security/permissions/
POST   /api/superadmin/security/permissions/
GET    /api/superadmin/security/permissions/{id}
PUT    /api/superadmin/security/permissions/{id}
DELETE /api/superadmin/security/permissions/{id}

# Security - Policies
GET    /api/superadmin/security/policies/
POST   /api/superadmin/security/policies/
GET    /api/superadmin/security/policies/{id}
PUT    /api/superadmin/security/policies/{id}
DELETE /api/superadmin/security/policies/{id}

# Security - Users
GET    /api/superadmin/security/users/
POST   /api/superadmin/security/users/
GET    /api/superadmin/security/users/{id}
PUT    /api/superadmin/security/users/{id}
DELETE /api/superadmin/security/users/{id}

# Settings
GET    /api/superadmin/settings/
POST   /api/superadmin/settings/
GET    /api/superadmin/settings/{id}
PUT    /api/superadmin/settings/{id}
DELETE /api/superadmin/settings/{id}
GET    /api/superadmin/settings/categories
GET    /api/superadmin/settings/search/

# Modules
GET    /api/superadmin/modules/
POST   /api/superadmin/modules/
GET    /api/superadmin/modules/{id}
PUT    /api/superadmin/modules/{id}
DELETE /api/superadmin/modules/{id}

# Module Assignments
GET    /api/superadmin/modules/assignments/
POST   /api/superadmin/modules/assignments/
GET    /api/superadmin/modules/assignments/{id}
PUT    /api/superadmin/modules/assignments/{id}
DELETE /api/superadmin/modules/assignments/{id}
POST   /api/superadmin/modules/assignments/{id}/enable
POST   /api/superadmin/modules/assignments/{id}/disable

# Sales Configuration
GET    /api/superadmin/sales-config/
POST   /api/superadmin/sales-config/
GET    /api/superadmin/sales-config/{id}
PUT    /api/superadmin/sales-config/{id}
DELETE /api/superadmin/sales-config/{id}
GET    /api/superadmin/sales-config/key/{key}
GET    /api/superadmin/sales-config/categories

# Marketing Configuration
GET    /api/superadmin/marketing-config/
POST   /api/superadmin/marketing-config/
GET    /api/superadmin/marketing-config/{id}
PUT    /api/superadmin/marketing-config/{id}
DELETE /api/superadmin/marketing-config/{id}

# Support Configuration
GET    /api/superadmin/support-config/
POST   /api/superadmin/support-config/
GET    /api/superadmin/support-config/{id}
PUT    /api/superadmin/support-config/{id}
DELETE /api/superadmin/support-config/{id}
```

### Compliance & Security Endpoints (`/api`)
```
# Compliance
GET    /api/compliance/retention/
POST   /api/compliance/retention/
GET    /api/compliance/retention/{id}
PUT    /api/compliance/retention/{id}
DELETE /api/compliance/retention/{id}

GET    /api/compliance/deletion/
POST   /api/compliance/deletion/
GET    /api/compliance/deletion/{id}
PUT    /api/compliance/deletion/{id}
DELETE /api/compliance/deletion/{id}

GET    /api/compliance/consent/
POST   /api/compliance/consent/
GET    /api/compliance/consent/{id}
PUT    /api/compliance/consent/{id}
DELETE /api/compliance/consent/{id}

# Security
GET    /api/security/
GET    /api/security/{id}

# Audit Logging
GET    /api/audit/
GET    /api/audit/{id}

# Data Classification
GET    /api/data/
GET    /api/data/{id}
```

## Common Response Formats

### Success Response
```json
{
  "data": {...},
  "meta": {
    "timestamp": "2025-09-24T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "meta": {
    "timestamp": "2025-09-24T10:30:00Z",
    "version": "1.0.0"
  }
}
```

## Rate Limiting
- **Default Limit**: 1000 requests per hour
- **Authenticated Limit**: 5000 requests per hour
- **Admin Limit**: 10000 requests per hour

## Documentation
- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`