from fastapi import APIRouter, Query
from typing import Optional, List
from datetime import datetime, timedelta
from .activity import router as activity_router
from .contact import router as contact_router
from .lead import router as lead_router
from .opportunity import router as opportunity_router
from .quotation import router as quotation_router
from .report import router as report_router
from .target import router as target_router

router = APIRouter()
router.include_router(activity_router, tags=["activities"])
router.include_router(contact_router, tags=["contacts"])
router.include_router(lead_router, tags=["leads"])
router.include_router(opportunity_router, tags=["opportunities"])
router.include_router(quotation_router, tags=["quotations"])
router.include_router(report_router, tags=["reports"])
router.include_router(target_router, tags=["targets"])

@router.get("/metrics")
def get_sales_metrics():
    """Get overall sales metrics for dashboard"""
    return {
        "totalRevenue": 2450000,
        "revenueChange": "+18% from last quarter",
        "totalCustomers": 342,
        "customerChange": "+45 this month",
        "conversionRate": 73,
        "conversionChange": "+8% improvement",
        "totalDeals": 89,
        "dealsChange": "15 closing this week",
        "avgDealSize": 27500,
        "avgDealChange": "+5% increase",
        "salesCycle": 32,
        "cycleChange": "-3 days faster"
    }


@router.get("/data")
def get_sales_data(period: str = Query("current", description="Time period for data")):
    """Get sales data for charts and visualizations"""
    if period == "current":
        return [
            {"month": "Jan", "sales": 205000, "target": 200000},
            {"month": "Feb", "sales": 187000, "target": 190000},
            {"month": "Mar", "sales": 234000, "target": 220000},
            {"month": "Apr", "sales": 298000, "target": 250000},
            {"month": "May", "sales": 276000, "target": 260000},
            {"month": "Jun", "sales": 312000, "target": 280000},
            {"month": "Jul", "sales": 289000, "target": 290000},
            {"month": "Aug", "sales": 334000, "target": 300000},
            {"month": "Sep", "sales": 298000, "target": 310000}
        ]
    return []


@router.get("/activities")
def get_sales_activities(
    limit: int = Query(10, description="Number of activities to return"),
    type: Optional[str] = Query(None, description="Filter by activity type")
):
    """Get recent sales activities"""
    activities = [
        {
            "id": "1",
            "type": "call",
            "title": "Follow-up call with Acme Corp",
            "description": "Discussed Q4 renewal and additional licenses",
            "salesRep": "John Williams",
            "customer": "Acme Corp",
            "timestamp": "2025-09-24T09:30:00Z",
            "status": "completed",
            "outcome": "Positive - moving to proposal stage",
            "value": 45000
        },
        {
            "id": "2",
            "type": "email",
            "title": "Proposal sent to TechStart",
            "description": "Custom package proposal for enterprise solution",
            "salesRep": "Sarah Mitchell",
            "customer": "TechStart Inc", 
            "timestamp": "2025-09-24T08:15:00Z",
            "status": "sent",
            "outcome": "Awaiting response",
            "value": 78000
        },
        {
            "id": "3",
            "type": "meeting",
            "title": "Demo presentation completed",
            "description": "Product demo for Innovate Inc leadership team",
            "salesRep": "Mike Chen",
            "customer": "Innovate Inc",
            "timestamp": "2025-09-23T16:00:00Z",
            "status": "completed",
            "outcome": "Very interested - scheduling follow-up",
            "value": 125000
        },
        {
            "id": "4",
            "type": "call",
            "title": "Discovery call with FutureTech",
            "description": "Initial needs assessment and qualification",
            "salesRep": "Emily Davis",
            "customer": "FutureTech Solutions",
            "timestamp": "2025-09-23T14:30:00Z",
            "status": "completed",
            "outcome": "Qualified lead - high potential",
            "value": 95000
        },
        {
            "id": "5",
            "type": "meeting",
            "title": "Contract negotiation",
            "description": "Final terms discussion with Nexus Solutions",
            "salesRep": "David Rodriguez",
            "customer": "Nexus Solutions",
            "timestamp": "2025-09-23T11:00:00Z",
            "status": "completed",
            "outcome": "Agreed on terms - preparing contract",
            "value": 156000
        }
    ]
    
    return {"activities": activities[:limit]}


@router.get("/customers")
def get_sales_customers(
    limit: int = Query(10, description="Number of customers to return"),
    sortBy: Optional[str] = Query("lastContact", description="Sort field"),
    sortOrder: Optional[str] = Query("desc", description="Sort order")
):
    """Get customer data for sales dashboard"""
    customers = [
        {
            "id": "1",
            "name": "John Smith",
            "email": "john.smith@acme.com",
            "company": "Acme Corp",
            "value": "$125,000",
            "lastContact": "2 days ago",
            "status": "active",
            "phone": "+1 (555) 123-4567"
        },
        {
            "id": "2", 
            "name": "Sarah Johnson",
            "email": "sarah.j@techstart.io",
            "company": "TechStart",
            "value": "$89,500",
            "lastContact": "1 week ago",
            "status": "prospect",
            "phone": "+1 (555) 234-5678"
        },
        {
            "id": "3",
            "name": "Mike Chen",
            "email": "mike@innovate.com",
            "company": "Innovate Inc",
            "value": "$156,000",
            "lastContact": "3 days ago",
            "status": "active",
            "phone": "+1 (555) 345-6789"
        },
        {
            "id": "4",
            "name": "Emily Davis",
            "email": "emily@futuretech.com",
            "company": "FutureTech",
            "value": "$203,000",
            "lastContact": "5 hours ago",
            "status": "active",
            "phone": "+1 (555) 456-7890"
        },
        {
            "id": "5",
            "name": "David Park",
            "email": "david.park@nexus.com",
            "company": "Nexus Solutions",
            "value": "$178,500",
            "lastContact": "1 day ago", 
            "status": "negotiation",
            "phone": "+1 (555) 567-8901"
        }
    ]
    
    return {"customers": customers[:limit]}


@router.get("/")
def get_sales_dashboard():
    return {
        "message": "Sales Dashboard",
        "modules": [
            "activities",
            "contacts",
            "leads",
            "opportunities",
            "quotations",
            "reports",
            "targets"
        ]
    }