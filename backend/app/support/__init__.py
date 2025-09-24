from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, timedelta
from .tickets import router as tickets_router
from .knowledge_base import router as knowledge_base_router
from .interactions import router as interactions_router
from .live_chat import router as live_chat_router
from .call_center import router as call_center_router
from .social_support import router as social_support_router
from .feedback import router as feedback_router
from .sla import router as sla_router
from .asset import router as asset_router
from .remote import router as remote_router
from .community import router as community_router
from .reporting import router as reporting_router
from .automation import router as automation_router
from .mobile import router as mobile_router
from .integration import router as integration_router
from .language import router as language_router

router = APIRouter()
router.include_router(tickets_router, tags=["tickets"])
router.include_router(knowledge_base_router, tags=["knowledge-base"])
router.include_router(interactions_router, tags=["interactions"])
router.include_router(live_chat_router, tags=["live-chat"])
router.include_router(call_center_router, tags=["call-center"])
router.include_router(social_support_router, tags=["social-support"])
router.include_router(feedback_router, tags=["feedback"])
router.include_router(sla_router, tags=["sla"])
router.include_router(asset_router, tags=["asset"])
router.include_router(remote_router, tags=["remote"])
router.include_router(community_router, tags=["community"])
router.include_router(reporting_router, tags=["reporting"])
router.include_router(automation_router, tags=["automation"])
router.include_router(mobile_router, prefix="/mobile", tags=["mobile"])
router.include_router(integration_router, tags=["integration"])
router.include_router(language_router, prefix="/language", tags=["language"])

@router.get("/metrics")
def get_support_metrics(
    start: Optional[str] = Query(None, description="Start date for metrics"),
    end: Optional[str] = Query(None, description="End date for metrics")
):
    """Get support metrics for dashboard"""
    return {
        "totalTickets": 1284,
        "openTickets": 89,
        "resolvedToday": 23,
        "resolvedTodayChange": "+12% from yesterday",
        "avgFirstResponse": "2.3 hrs",
        "firstResponseTrend": "↓ 15% improvement",
        "avgResolutionTime": "14.7 hrs",
        "resolutionTimeTrend": "↓ 8% faster",
        "customerSatisfaction": "94.2%",
        "satisfactionTrend": "↑ 3% increase",
        "activeAgents": 12,
        "escalatedTickets": 4,
        "slaCompliance": "97.8%"
    }


@router.get("/tickets")
def get_support_tickets(
    limit: int = Query(10, description="Number of tickets to return"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority")
):
    """Get support tickets data"""
    tickets = [
        {
            "id": "T-001",
            "number": "T-001",
            "subject": "Login issues with mobile app",
            "description": "User unable to login using Touch ID on iOS app",
            "customerName": "John Smith",
            "customerEmail": "john.smith@acmecorp.com",
            "priority": "high",
            "status": "open",
            "assignedTo": "Sarah Johnson",
            "category": "Technical",
            "type": "incident",
            "createdAt": "2025-09-24T08:00:00Z",
            "updatedAt": "2025-09-24T10:30:00Z",
            "tags": ["mobile", "authentication"],
            "attachments": [],
            "comments": [],
            "slaDetails": {
                "responseTime": {"target": 240, "elapsed": 45, "status": "met"},
                "resolutionTime": {"target": 1440, "elapsed": 180, "status": "on_track"}
            }
        },
        {
            "id": "T-002",
            "number": "T-002",
            "subject": "Billing question about invoice",
            "description": "Customer asking about charges on recent invoice #12345",
            "customerName": "Lisa Chen",
            "customerEmail": "lisa.chen@innovateco.com",
            "priority": "medium",
            "status": "in-progress", 
            "assignedTo": "Mike Wilson",
            "category": "Billing",
            "type": "question",
            "createdAt": "2025-09-24T07:15:00Z",
            "updatedAt": "2025-09-24T09:45:00Z",
            "tags": ["billing", "invoice"],
            "attachments": [],
            "comments": [],
            "slaDetails": {
                "responseTime": {"target": 480, "elapsed": 120, "status": "met"},
                "resolutionTime": {"target": 2880, "elapsed": 390, "status": "on_track"}
            }
        },
        {
            "id": "T-003",
            "number": "T-003",
            "subject": "Feature request: Dark mode",
            "description": "Customer requesting dark mode theme option in dashboard",
            "customerName": "David Park",
            "customerEmail": "david.park@techstart.com",
            "priority": "low",
            "status": "resolved",
            "assignedTo": "Emma Thompson",
            "category": "Feature Request",
            "type": "request",
            "createdAt": "2025-09-23T14:00:00Z",
            "updatedAt": "2025-09-24T09:00:00Z",
            "tags": ["feature", "ui"],
            "attachments": [],
            "comments": [],
            "slaDetails": {
                "responseTime": {"target": 720, "elapsed": 60, "status": "met"},
                "resolutionTime": {"target": 5760, "elapsed": 1140, "status": "met"}
            }
        }
    ]
    
    return {"tickets": tickets[:limit]}


@router.get("/knowledge/articles")
def get_knowledge_articles(
    limit: int = Query(10, description="Number of articles to return"),
    status: Optional[str] = Query("published", description="Filter by status"),
    sortBy: Optional[str] = Query("views", description="Sort field"),
    sortOrder: Optional[str] = Query("desc", description="Sort order")
):
    """Get knowledge base articles"""
    articles = [
        {
            "id": "KB-001",
            "title": "Getting Started with Your Account",
            "slug": "getting-started-account",
            "content": "This article covers the basics of setting up your account...",
            "category": "Getting Started",
            "status": "published",
            "author": "Sarah Johnson",
            "createdAt": "2025-09-20T10:00:00Z",
            "updatedAt": "2025-09-23T14:30:00Z",
            "views": 1524,
            "likes": 89,
            "helpful": 95,
            "tags": ["setup", "account", "basics"]
        },
        {
            "id": "KB-002",
            "title": "Two-Factor Authentication Setup",
            "slug": "two-factor-authentication",
            "content": "Learn how to enable and configure 2FA for your account...",
            "category": "Security",
            "status": "published",
            "author": "Mike Chen",
            "createdAt": "2025-09-18T09:15:00Z",
            "updatedAt": "2025-09-22T16:20:00Z",
            "views": 892,
            "likes": 67,
            "helpful": 88,
            "tags": ["security", "2fa", "authentication"]
        },
        {
            "id": "KB-003",
            "title": "Troubleshooting Login Issues",
            "slug": "troubleshooting-login",
            "content": "Common solutions for login problems and authentication issues...",
            "category": "Troubleshooting",
            "status": "published",
            "author": "Emma Thompson",
            "createdAt": "2025-09-15T11:30:00Z",
            "updatedAt": "2025-09-24T08:45:00Z",
            "views": 2103,
            "likes": 156,
            "helpful": 92,
            "tags": ["login", "troubleshooting", "authentication"]
        }
    ]
    
    return {"articles": articles[:limit]}


@router.get("/")
def get_support_dashboard():
    return {"message": "Support Dashboard"}