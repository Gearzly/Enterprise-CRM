# Enterprise CRM System

A comprehensive, modular CRM solution built with Python FastAPI, designed for enterprise-level customer relationship management across Sales, Marketing, and Support operations.

## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Modules](#modules)
  - [Sales Module](#sales-module)
  - [Marketing Module](#marketing-module)
  - [Support Module](#support-module)
  - [Super Admin Panel](#super-admin-panel)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

This Enterprise CRM system provides a complete solution for managing customer relationships across all business functions. Built with a modular architecture, it allows organizations to customize and extend functionality based on their specific needs while maintaining a consistent API and data model.

The system features dynamic configuration management, role-based access control, organization-specific settings, and comprehensive reporting capabilities.

## Key Features

- **Modular Architecture**: Separate modules for Sales, Marketing, Support, and Administration
- **Dynamic Configuration**: Runtime configuration management via Super Admin panel
- **Multi-tenancy**: Organization-specific data and configurations
- **Role-Based Access Control**: Comprehensive permission system with Attribute-Based Access Control (ABAC)
- **RESTful API**: Clean, well-documented API endpoints
- **Comprehensive Error Handling**: Robust error handling with meaningful messages
- **Type Safety**: Pydantic models for data validation
- **Extensible Design**: Easy to extend with new modules and features

## Architecture

The CRM system follows a microservices-inspired architecture with a central FastAPI backend:

```
┌─────────────────────────────────────────────────────────────┐
│                    Enterprise CRM System                    │
├─────────────────────────────────────────────────────────────┤
│                        ┌─────────────┐                      │
│                        │   Client    │                      │
│                        └─────────────┘                      │
│                              │                              │
│                        ┌─────────────┐                      │
│                        │   FastAPI   │                      │
│                        │   Backend   │                      │
│                        └─────────────┘                      │
│                              │                              │
├──────────────────────────────┼──────────────────────────────┤
│         Business Modules     │      Management Modules      │
├──────────────────────────────┼──────────────────────────────┤
│  ┌─────────┐ ┌────────────┐ │ ┌──────────────────────────┐ │
│  │  Sales  │ │ Marketing  │ │ │      Super Admin         │ │
│  └─────────┘ └────────────┘ │ │  ┌─────────────────────┐ │ │
│  ┌─────────┐ ┌────────────┐ │ │  │   Organizations     │ │ │
│  │ Support │ │  ...       │ │ │  ├─────────────────────┤ │ │
│  └─────────┘ └────────────┘ │ │  │      Security       │ │ │
│                              │  ├─────────────────────┤ │ │
│                              │  │      Settings       │ │ │
│                              │  ├─────────────────────┤ │ │
│                              │  │      Modules        │ │ │
│                              │  └─────────────────────┘ │ │
└──────────────────────────────┴──────────────────────────┘ │
│                        ┌─────────────┐                      │
│                        │    Data     │                      │
│                        │  Storage    │                      │
│                        └─────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## Modules

### Sales Module

Comprehensive sales management with lead tracking, opportunity management, and performance reporting.

**Features:**
- Activity management
- Contact management
- Lead lifecycle tracking
- Opportunity pipeline management
- Quotation handling
- Sales forecasting and target management
- Detailed reporting and analytics

**API Endpoints:**
- Activities: Create, read, update, delete activities
- Contacts: Manage customer contacts
- Leads: Track leads through the sales funnel
- Opportunities: Manage sales opportunities through stages
- Quotations: Create and manage sales quotations
- Reports: Generate sales performance reports
- Targets: Set and track sales targets with forecasting

### Marketing Module

Full-featured marketing automation platform with campaign management, lead nurturing, and analytics.

**Features:**
- Campaign management with templates
- Lead management and scoring
- Email marketing automation
- Social media integration
- Content management system
- Customer data platform (CDP)
- Event management
- Partner relationship management
- Resource and budget management
- Customer segmentation
- Marketing automation workflows
- Analytics and reporting

**Submodules:**
- Campaigns: Create and manage marketing campaigns
- Leads: Advanced lead management and nurturing
- Email: Email marketing and automation
- Social Media: Social platform integration
- Content: Content creation and management
- Analytics: Marketing performance analytics
- Automation: Workflow automation
- Segmentation: Customer segmentation
- Events: Event management
- Partners: Partner relationship management
- Resources: Budget and resource management
- CDP: Customer data platform

### Support Module

Customer support ticketing system with knowledge base and interaction tracking.

**Features:**
- Ticket management system
- Knowledge base
- Customer interaction tracking
- Support analytics

### Super Admin Panel

Centralized administration for the entire CRM system with multi-tenant support.

**Features:**
- Organization management
- Role-based access control with ABAC
- System settings management
- Module management for organizations
- Sales and marketing configuration management
- Security policy management

**Submodules:**
- Organizations: Multi-tenant organization management
- Security: RBAC and ABAC security system
- Settings: System-wide configuration
- Modules: Module management and assignment
- Sales Config: Sales module configuration
- Marketing Config: Marketing module configuration

## Technology Stack

- **Backend**: Python FastAPI
- **Data Validation**: Pydantic
- **HTTP Client**: httpx
- **Database**: (Currently using in-memory storage for demo)
- **API Documentation**: Swagger UI, ReDoc
- **Authentication**: (Implementation pending)
- **Deployment**: (Implementation pending)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gearzly/Enterprise-CRM.git
   cd Enterprise-CRM
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install the dependencies:
   ```bash
   cd backend
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

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the following documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive API documentation and testing capabilities.

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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.