"""Synthetic IT tickets with resolution text for recommendation."""

from __future__ import annotations
import random
from typing import List, Dict
import numpy as np
import pandas as pd

TICKET_KB: List[Dict] = [
    {
        "category": "Network",
        "titles": [
            "Cannot connect to VPN from home",
            "VPN connection times out after login",
            "Remote VPN fails for multiple users",
        ],
        "descriptions": [
            "VPN client times out after entering credentials. Affects remote workforce.",
            "Users report connection refused or timeout when connecting to corporate VPN.",
            "Intermittent VPN drops after a few minutes of use.",
        ],
        "resolutions": [
            "1. Reset user VPN profile. 2. Verify MFA token sync. 3. Check firewall rules for UDP 443. 4. Reinstall VPN client if needed.",
            "Updated VPN concentrator config; increased concurrent session limit. Advised users to update client to latest version.",
            "Identified MTU issue on home routers. Documented workaround: set MTU to 1400 on VPN adapter.",
        ],
    },
    {
        "category": "Access",
        "titles": [
            "New employee cannot access email",
            "AD account not provisioned for starter",
            "Password reset not working for contractor",
        ],
        "descriptions": [
            "New hire started today but cannot log into Outlook or Teams. AD account missing groups.",
            "Onboarding ticket: mailbox not created. Manager requesting urgent access.",
            "External contractor locked out; self-service password reset fails with account not found.",
        ],
        "resolutions": [
            "1. Created AD account from HR feed. 2. Added to standard distribution groups. 3. Provisioned Exchange mailbox. 4. Sent welcome credentials.",
            "Ran manual provisioning script. Verified license assignment in M365 admin. User confirmed access within 15 minutes.",
            "Account was disabled after contract end date. Re-enabled with manager approval and extended expiry by 90 days.",
        ],
    },
    {
        "category": "Software",
        "titles": [
            "CRM application returns 500 errors",
            "Order service throwing NullPointerException",
            "Batch job failed overnight",
        ],
        "descriptions": [
            "Users cannot create or update records in CRM. HTTP 500 on save actions.",
            "Checkout flow fails with NPE in OrderService when applying discounts.",
            "Nightly inventory sync job exited with code 1. Downstream reports stale.",
        ],
        "resolutions": [
            "Root cause: null customer ID from upstream. Deployed null-check patch and added validation. Monitored for 24h - stable.",
            "Fixed missing null guard on discount object. Added unit tests. Hotfixed to production.",
            "Job failed due to disk full on batch server. Cleared old logs, increased volume, re-ran job successfully.",
        ],
    },
    {
        "category": "Hardware",
        "titles": [
            "Laptop not powering on",
            "Printer offline on finance floor",
            "Server disk failure predicted",
        ],
        "descriptions": [
            "Executive laptop shows no LED when power button pressed. Urgent loaner requested.",
            "Network printer FIN-PRN-02 offline. Users cannot print invoices.",
            "Monitoring alert: disk failure predicted on DB-PROD-03. RAID degraded.",
        ],
        "resolutions": [
            "Replaced faulty power adapter and battery. Laptop recovered. Ordered spare dock for executive.",
            "Cleared paper jam, reset printer, updated firmware. Print queue drained successfully.",
            "Hot-swapped failed disk in RAID array. Rebuild completed overnight. No data loss.",
        ],
    },
    {
        "category": "Security",
        "titles": [
            "Suspicious login attempts detected",
            "Phishing email reported by user",
            "SSL certificate expiring soon",
        ],
        "descriptions": [
            "SIEM alert: multiple failed logins from unusual geolocations on privileged accounts.",
            "Employee clicked link in email claiming to be from CFO. Requested investigation.",
            "Public portal certificate expires in 5 days. Renewal stuck in approval.",
        ],
        "resolutions": [
            "Forced password reset on affected accounts. Enabled geo-blocking for high-risk regions. Confirmed no successful breach.",
            "URL blocked at gateway. User machine scanned - clean. Sent company-wide phishing awareness reminder.",
            "Expedited CA renewal. Installed new cert on load balancers. Verified HTTPS and set calendar reminder for next renewal.",
        ],
    },
    {
        "category": "Database",
        "titles": [
            "Production DB high CPU",
            "Replication lag on read replica",
            "Deadlock in order processing",
        ],
        "descriptions": [
            "CPU on ORDERS-DB above 90% for 2 hours. Application latency elevated.",
            "PostgreSQL replica lag exceeded 30 seconds. Reporting data stale.",
            "Frequent deadlocks between order and inventory tables. Transactions rolling back.",
        ],
        "resolutions": [
            "Identified missing index on high-traffic query. Added index during maintenance window. CPU returned to normal.",
            "Restarted replication after network blip. Tuned wal_sender timeout. Lag cleared within 10 minutes.",
            "Rewrote transaction order to acquire locks consistently. Reduced deadlock rate by 95%.",
        ],
    },
]


def generate_ticket_dataset(n_samples: int = 3000, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)
    records = []
    for i in range(n_samples):
        kb = random.choice(TICKET_KB)
        title = random.choice(kb["titles"])
        desc = random.choice(kb["descriptions"])
        resolution = random.choice(kb["resolutions"])
        if random.random() < 0.2:
            desc = desc + f" Ticket ref INC{random.randint(100000,999999)}."
        full = f"Title: {title}\nDescription: {desc}"
        records.append({
            "ticket_id": f"INC-{i+1:06d}",
            "title": title,
            "description": desc,
            "full_text": full,
            "category": kb["category"],
            "resolution": resolution,
            "status": "resolved",
        })
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_ticket_dataset(100)
    print(df["category"].value_counts())
    print(df.head(1)[["title", "resolution"]].to_string())
