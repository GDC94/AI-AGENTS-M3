"""The three Areas that can resolve a Query, and what each one resolves.

AREA_DESCRIPTIONS is the single source for both the Router prompt and the
Specialist prompt. Ownership rule (ADR 0001): a topic belongs to the Area
whose staff act to resolve the request, not the Area the topic sounds like.
"""

from enum import StrEnum


class Area(StrEnum):
    HR = "hr"
    TECH = "tech"
    FINANCE = "finance"


AREA_DESCRIPTIONS: dict[Area, str] = {
    Area.HR: (
        "Resolves employment matters for Atalaya Staff: onboarding (background checks, "
        "the first month, when equipment is handed over), security clearances (levels, "
        "applications, renewals, what happens when one is lost or the person leaves), "
        "confidentiality and ethics, leave and absences, work modality (client offices, "
        "remote work, on-call duty, schedules), development (performance reviews, "
        "mandatory training, when salaries are reviewed or raised) and leaving the "
        "company (resignation, notice period). For Clients, it resolves questions "
        "about their assigned consultant: who it is, their clearance and how to "
        "request a replacement."
    ),
    Area.TECH: (
        "Resolves anything that requires acting on a system. For Clients: platform "
        "access (creating users, passwords, two-factor authentication, locked "
        "accounts), roles and permissions (including removing access for someone who "
        "left the organisation), data classification, connecting data sources, "
        "dashboards and exports, audit logs, deployment and maintenance windows, and "
        "reporting incidents and following support tickets. For Staff: internal "
        "security (VPN, phishing, security incidents, USB use) and equipment "
        "(laptop setup and faults, allowed software, peripherals)."
    ),
    Area.FINANCE: (
        "Resolves money matters. For Clients: contracting Atalaya (tenders, direct "
        "contracting, contract guarantees), purchase orders, invoices issued to "
        "their organisation (issuing, downloading, tax details, corrections), "
        "payments and collections, prices, licences and renewals (including the cost "
        "of adding users, price adjustments and credit notes). For Staff: expenses "
        "and travel allowances (receipts, limits, reimbursement), corporate cards, "
        "and salary payment (when the salary is paid, payslips, deductions, changing "
        "the bank account)."
    ),
}
