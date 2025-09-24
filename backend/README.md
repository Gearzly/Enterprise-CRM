# SaaS CRM Backend

This is the backend API for the SaaS CRM system, built with FastAPI.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Sales Module](#sales-module)
  - [Marketing Module](#marketing-module)
  - [Support Module](#support-module)
  - [Super Admin Panel](#super-admin-panel)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [API Documentation](#api-documentation)

## Overview

The backend provides RESTful APIs for a comprehensive CRM system with modules for Sales, Marketing, Support operations, and a Super Admin Panel for system management.

## Project Structure

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── sales/               # Sales module
│   │   ├── __init__.py      # Sales router
│   │   ├── activity.py      # Activity management
│   │   ├── contact.py       # Contact management
│   │   ├── lead.py          # Lead management
│   │   ├── opportunity.py   # Opportunity management
│   │   ├── quotation.py     # Quotation management
│   │   ├── report.py        # Sales reporting
│   │   ├── target.py        # Sales targets and forecasting
│   │   ├── config.py        # Sales configuration utilities
│   ├── marketing/           # Marketing module
│   ├── support/             # Support module
│   └── superadmin/          # Super Admin Panel
│       ├── __init__.py      # Super Admin router
│       ├── models.py        # Shared data models
│       ├── organizations/   # Organization management
│       │   ├── __init__.py  # Organizations router
│       │   └── organization.py
│       ├── security/        # Security management
│       │   ├── __init__.py  # Security router
│       │   └── security.py
│       ├── settings/        # System settings
│       │   ├── __init__.py  # Settings router
│       │   └── settings.py
│       ├── modules/         # Module management
│       │   ├── __init__.py  # Modules router
│       │   └── modules.py
│       └── sales_config/    # Sales configuration
│           ├── __init__.py  # Sales Config router
│           └── sales_config.py
├── requirements.txt         # Python dependencies
├── start_server.py         # Startup script
├── test_endpoints.py       # Endpoint testing script
├── test_superadmin.py      # Super Admin module testing script
└── README.md               # This file
```

## API Endpoints

### Sales Module

All sales endpoints are prefixed with `/sales`.

#### Activities
- `GET /activities` - List all activities
- `GET /activities/{id}` - Get a specific activity
- `POST /activities` - Create a new activity
- `PUT /activities/{id}` - Update an activity
- `DELETE /activities/{id}` - Delete an activity

#### Contacts
- `GET /contacts` - List all contacts
- `GET /contacts/{id}` - Get a specific contact
- `POST /contacts` - Create a new contact
- `PUT /contacts/{id}` - Update a contact
- `DELETE /contacts/{id}` - Delete a contact

#### Leads
- `GET /leads` - List all leads
- `GET /leads/{id}` - Get a specific lead
- `POST /leads` - Create a new lead
- `PUT /leads/{id}` - Update a lead
- `DELETE /leads/{id}` - Delete a lead
- `GET /leads/status/{status}` - Get leads by status
- `GET /leads/config/statuses` - Get available lead statuses
- `GET /leads/config/sources` - Get available lead sources

#### Opportunities
- `GET /opportunities` - List all opportunities
- `GET /opportunities/{id}` - Get a specific opportunity
- `POST /opportunities` - Create a new opportunity
- `PUT /opportunities/{id}` - Update an opportunity
- `DELETE /opportunities/{id}` - Delete an opportunity
- `GET /opportunities/stage/{stage}` - Get opportunities by stage
- `GET /opportunities/config/stages` - Get available opportunity stages

#### Quotations
- `GET /quotations` - List all quotations
- `GET /quotations/{id}` - Get a specific quotation
- `POST /quotations` - Create a new quotation
- `PUT /quotations/{id}` - Update a quotation
- `DELETE /quotations/{id}` - Delete a quotation
- `GET /quotations/status/{status}` - Get quotations by status
- `GET /quotations/config/statuses` - Get available quotation statuses

#### Reports
- `GET /reports/sales` - Get comprehensive sales report
- `GET /reports/sales/metrics` - Get sales metrics

#### Targets
- `GET /targets` - List all sales targets
- `GET /targets/{id}` - Get a specific sales target
- `POST /targets` - Create a new sales target
- `PUT /targets/{id}` - Update a sales target
- `DELETE /targets/{id}` - Delete a sales target
- `GET /forecasts` - List all sales forecasts
- `GET /forecasts/current` - Get current forecast

### Marketing Module

All marketing endpoints are prefixed with `/marketing`.

### Support Module

All support endpoints are prefixed with `/support`.

### Super Admin Panel

All super admin endpoints are prefixed with `/api/superadmin`.

#### Organizations
- `GET /organizations/` - List all organizations
- `GET /organizations/{id}` - Get a specific organization
- `POST /organizations/` - Create a new organization
- `PUT /organizations/{id}` - Update an organization
- `DELETE /organizations/{id}` - Delete an organization
- `POST /organizations/{id}/suspend` - Suspend an organization
- `POST /organizations/{id}/activate` - Activate an organization

#### Security Management
##### Roles
- `GET /security/roles` - List all roles
- `GET /security/roles/{id}` - Get a specific role
- `POST /security/roles` - Create a new role
- `PUT /security/roles/{id}` - Update a role
- `DELETE /security/roles/{id}` - Delete a role

##### Permissions
- `GET /security/permissions` - List all permissions
- `GET /security/permissions/{id}` - Get a specific permission
- `POST /security/permissions` - Create a new permission
- `PUT /security/permissions/{id}` - Update a permission
- `DELETE /security/permissions/{id}` - Delete a permission

##### Policies (ABAC)
- `GET /security/policies` - List all policies
- `GET /security/policies/{id}` - Get a specific policy
- `POST /security/policies` - Create a new policy
- `PUT /security/policies/{id}` - Update a policy
- `DELETE /security/policies/{id}` - Delete a policy

##### Users
- `GET /security/users` - List all users
- `GET /security/users/{id}` - Get a specific user
- `POST /security/users` - Create a new user
- `PUT /security/users/{id}` - Update a user
- `DELETE /security/users/{id}` - Delete a user

#### System Settings
- `GET /settings/` - List all system settings
- `GET /settings/{id}` - Get a specific setting
- `POST /settings/` - Create a new setting
- `PUT /settings/{id}` - Update a setting
- `DELETE /settings/{id}` - Delete a setting
- `GET /settings/categories` - List all setting categories
- `GET /settings/search/` - Search settings by key

#### Module Management
##### Modules
- `GET /modules/` - List all modules
- `GET /modules/{id}` - Get a specific module
- `POST /modules/` - Create a new module
- `PUT /modules/{id}` - Update a module
- `DELETE /modules/{id}` - Delete a module

##### Module Assignments
- `GET /modules/assignments/` - List all module assignments
- `GET /modules/assignments/{id}` - Get a specific module assignment
- `POST /modules/assignments/` - Assign a module to an organization
- `PUT /modules/assignments/{id}` - Update a module assignment
- `DELETE /modules/assignments/{id}` - Remove a module assignment
- `POST /modules/assignments/{id}/enable` - Enable a module assignment
- `POST /modules/assignments/{id}/disable` - Disable a module assignment

#### Sales Configuration
- `GET /sales-config/` - List all sales configurations
- `GET /sales-config/{id}` - Get a specific sales configuration
- `POST /sales-config/` - Create a new sales configuration
- `PUT /sales-config/{id}` - Update a sales configuration
- `DELETE /sales-config/{id}` - Delete a sales configuration
- `GET /sales-config/key/{key}` - Get configuration by key
- `GET /sales-config/categories` - List all configuration categories

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Method 1: Using the startup script (Recommended)
```bash
python start_server.py
```

### Method 2: Using uvicorn directly
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8001`.

## Testing

To test all endpoints, run the test script:
```bash
python test_endpoints.py
```

To test Super Admin module imports:
```bash
python test_superadmin.py
```

This will test all available endpoints and report which ones are working correctly.

## API Documentation

Once the application is running, you can access the following documentation:

- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

These provide interactive API documentation and testing capabilities.