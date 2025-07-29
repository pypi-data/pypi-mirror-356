#!/usr/bin/env python

config = {
    "summary":
        {"widths": [],
         "heading": ["Description", "Count"],
         "vaults": {"text": "Number of scanned vaults", "value": 0},
         "vaults_error": {"text": "Number of failed vaults", "value": 0},
         "records_active": {"text": "Total number of active records", "value": 0},
         "records_disabled": {"text": "Total number of disabled records", "value": 0},
         "records": {"text": "Total number of records (including disabled)", "value": 0},
         "expired": {"text": "Active records already expired", "value": 0},
         "missing": {"text": "Active records missing Expiration Date", "value": 0},
         "this_year": {"text": "Active records updated in the last year", "value": 0},
         "one_year": {"text": "Active records NOT updated in the last year", "value": 0},
         "two_years": {"text": "Active records NOT updated for the last 2 years", "value": 0},
         "three_years": {"text": "Active records NOT updated for the last 3 years", "value": 0}
         },
    "report":
        {"widths": [],
         "heading": ["Record Name", "Record Type", "Vault Name", "Last Updated", "Expiration",
                     "Comment"]
         },
    "known_errors": {"Not authorized": "Forbidden By Firewall",
                     "List permission": "List Access Denied",
                     "Failed to establish a new connection": "Unknown Key Vault",
                     "Invalid issuer": "Invalid Key Vault"
                     }
}
