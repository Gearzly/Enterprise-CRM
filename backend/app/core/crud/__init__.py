from .lead import lead
from .contact import contact
from .opportunity import opportunity
from .quotation import quotation
from .activity import activity
from .target import target
from .report import report
from .sla import sla, sla_breach, sla_notification

__all__ = [
    "lead",
    "contact",
    "opportunity",
    "quotation",
    "activity",
    "target",
    "report",
    "sla",
    "sla_breach", 
    "sla_notification",
]