#!/usr/bin/env python

import logging
import datetime
from .set_timestamp import set_timestamp, now
from .alerts import *
from .config import *


########################################################################################################################


class AzureKeyVaultReport(object):
    """Generates reports i various formats from the results of 'az keyvault' commands.

    The values of 'updated', 'created' and 'expires' are converted to date object
    and the age (in days) is calculated.

    Attributes
    ----------

    results : list
        The list of results from the 'az keyvault' commands, enriched with 'vault_name' and 'record_type'
    items : list
        The list of items.
        Items are enriched with more data, e.g. age of each date element, vault_name, record_type, record_name
    vaults : list
         The unique list of vaults processed
    vaults_failed : list
        The unique list of vaults failed to process
    total_scanned_records_count : int
        A counter of all scanned records. Not including failed records.
    report : list
        The list of filtered row items as dict
    report_csv : list
        The list of csv rows
    summary : dict
        The summary of the report as dict
    slack_alert_cards : list
        A list of Slack alert messages formatted as Slack Markdown
    teams_alert_cards : list
        A list of Teams alerts (dicts) to be posted to MS Teams.
    summary_values : dict
        The config for the summary report. Read from config.py
    report_values : dict
        The config for the report. Read from config.py
    report_full : dict
        The full report, including the summary, as dict


    Methods
    -------
    parse_results()
        Parse through the provided 'results' from the azure cli keyvault cmd outputs.
        For each result in the results new item is created and added to the items list.
        Each item contains the following data:
        - Date objects, created from the 'updated', 'created' and 'expires' values and stored as values
          in new X_ts keys.
        - The age (in days) is calculated from each of the date objects and stored as values in new X_age keys.
        - 'vault_name' and 'record_type

    add_report(expire_threshold=None, alert_threshold=None, ignore_no_expiration=True, include_all=False,
               teams_alerts=False)
        Creates detailed 'column and rows' reports with comment according to the parameters passed.

        The column names are defined in the 'config.py' file.

        The values for the "Comment" column is generated according to the age of 'updated', 'created' and 'expires'.
        If missing 'expires' then a comment concerning that is added.

        When a row is completed it is added to the report(s), according to input arguments.
        A json object of a completed row is ALWAYS created.

    add_summary()
        Creates a summary as a dict ('summary') and as a plain text Markdown table ('summary_md').

        The heading / keys are defined in the config.py file.

        The 'summary' dict is also added to the 'report_full' dict.

    sort_items():
         expired_days=7, will_expire_days=14
        Returns a sorted list of all the records

    create_kv_rows(rows)
        Creates key/value pairs of the items in the provided report rows

    get_report_full()
        Returns the dict version of the full report were all the rows are included and a dict of the summary.

    get_report()
        Returns a list of dict versions of the filtered rows.

    get_summary()
        Returns the dict version of the summary.

    error_record_handle(message)
        Checks if the error az cli cmd error output contains a known error.
        Known errors are defined in the config file.

    get_teams_alerts()
        Returns the list of Teams alert cards payloads

    get_slack_alerts()
        Returns the list of Slack alert cards messages
    """

    def __init__(self, results):
        """
        Parameters
        ----------
        results : list
            The list of results from the 'az keyvault' commands, enriched with 'vault_name' and 'record_type'
        """

        self.results = results
        self.items = []
        self.vaults = []
        self.vaults_failed = []
        self.total_scanned_records_count = 0
        self.report = []
        self.report_csv = []
        self.summary = {}
        self.slack_alert_cards = []
        self.teams_alert_cards = []
        self.summary_values = config.get("summary")
        self.report_values = config.get("report")
        self.report_full = {
            "created_at": datetime.datetime.utcnow().isoformat(),
            "summary": {},
            "report": {}
        }

    def sort_items(self, expired_days=7, will_expire_days=14):
        """Sort the list of dict items by days to expiration

        If no parameters provided, this method will return a sorted list of all the records.
        The list will be sorted from top and down, by the oldest 'Expiration' date and then followed
        by the oldest 'Last Updated' date and then returns the sorted list.

        If any of the parameters provided, it will first create and sort
        an 'error' list
        and then an 'expired' list
        and then a 'will_expire' list
        and the finally a list with the other records.

        Each list will be sorted from top and down, by the oldest 'Expiration' date and then followed
        by the oldest 'Last Updated' date and then returns a combined list.

        Parameters
        ----------
        expired_days : int
            If provided, the record will be added to a separate list (expired),
            if the expires_age (days since expiration) of the record
            is between 0 the days provided in the expired_days argument.

        will_expire_days : int
            If provided, the record will be added to a separate list (will_expire),
            if the expires_age (days to expiration) of the record
            is between 0 the days provided in the will_expire_days argument,
            and the record is not already added to the expired list.
        """

        if not isinstance(expired_days, int):
            return sorted(self.items, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)

        errors = []
        expired = []
        will_expire = []
        others = []
        for item in self.items:
            if item.get("error"):
                errors.append(item)
                continue

            expires_age = item.get("expires_age")
            if isinstance(expires_age, int) and expires_age <= 0 and abs(expires_age) <= expired_days:
                expired.append(item)
                continue

            if isinstance(expires_age, int) and 0 <= expires_age <= will_expire_days:
                will_expire.append(item)
                continue

            others.append(item)

        sorted_list = errors
        sorted_list += sorted(expired, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)
        sorted_list += sorted(will_expire, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)
        sorted_list += sorted(others, key=lambda x: (str(x.get('expires')), x.get('updated', ' ')), reverse=False)

        return sorted_list

    def error_record_handle(self, message):
        """Checks if the error az cli cmd error output contains a known error - as defined in the config file"""

        # Get the known error from config file
        known_errors = config.get("known_errors")

        # Returns if no error message provided or known errors not found in the config file
        if not message or not known_errors:
            return

        vault_name = "-"
        record_type = "-"
        error_msg = "-"

        # Parse through the know error keys in config to check if the same error is present in the message
        # The Vault Name and Record Type is fetched from the executed 'az keyvault' cmd
        # which may be present in the provided message
        for key, value in known_errors.items():
            if key.lower() in str(message).lower():
                for line in message.splitlines():

                    # List permission error
                    if line.startswith("ERROR:"):
                        if "list permission" in line.lower():
                            for item in line.split(";"):
                                if key.lower() in item:
                                    vault_name = item.split("'")[-1]
                                    record_type = item.split(key.lower())[0].split()[-1]
                                    error_msg = value
                                    if error_msg and vault_name and record_type:
                                        break

                        # Firewall not authorized error and establish error
                        else:
                            error_msg = value

                    # Firewall not authorized error
                    if error_msg and line.startswith("Vault: "):
                        vault_name = line.split(";")[0].split()[-1]
                        record_type = "-"

                    # Get vault_name and record_type from executed 'az keyvault' command (if command logged)
                    if line.startswith("az keyvault"):
                        cmd_elements = line.split()
                        vault_name = cmd_elements[-1]
                        record_type = cmd_elements[-4]
                        error_msg = value

        self.items.append(
            {
                "error": error_msg,
                "vault_name": vault_name,
                "record_type": record_type
            }
        )
        if vault_name not in self.vaults_failed:
            self.vaults_failed.append(vault_name)

    def parse_results(self):
        """Parse through the result from the azure cli keyvault cmd output and build new enriched items."""

        if not isinstance(self.results, list):
            logging.error(f"The provided results must be a list.")
            return

        for result in self.results:
            vault_name = ""
            record_type = ""

            if not isinstance(result, list):
                logging.error(f"The az output result is not a list. Will check if known error..")
                self.error_record_handle(result)
                continue

            for r in result:
                if not isinstance(r, dict):
                    logging.error(f"The az output is not in expected format.")
                    continue

                if not vault_name and not record_type:
                    kv_id = r.get("id", "")
                    if not kv_id:
                        kv_id = r.get("kid", "")

                    items = kv_id.split("/")
                    if len(items) == 5:
                        vault_name = items[2].split(".")[0]
                        record_type = items[3].rstrip("s")

                if not vault_name and not record_type:
                    continue

                if vault_name not in self.vaults:
                    self.vaults.append(vault_name)

                item = {
                    "vault_name": vault_name,
                    "record_type": record_type,
                    "record_name": r.get("name"),
                    "enabled": False,
                }

                a = r.get("attributes")
                if isinstance(a, dict):
                    for k, v in a.items():
                        if "enabled" in k:
                            item["enabled"] = v

                    if not item.get("enabled"):
                        self.summary_values["records_disabled"]["value"] += 1

                    else:
                        self.summary_values["records_active"]["value"] += 1

                    for k, v in a.items():
                        if ("updated" in k or "created" in k or "expires" in k) and v:
                            value = str(v).split("T")[0]
                            item[k] = value
                            ts = set_timestamp(value)
                            item[f"{k}_ts"] = ts
                            age = (now() - ts).days
                            item[f"{k}_age"] = age

                            # Update the update age counters:
                            # If already expired
                            if "expires" in k and item.get("enabled") and age > 0:
                                self.summary_values["expired"]["value"] += 1

                            # One year and older, but less than two years
                            if "updated" in k and item.get("enabled") and age < 365:
                                self.summary_values["this_year"]["value"] += 1

                            # One year and older, but less than two years
                            if "updated" in k and item.get("enabled") and (365 <= age < 365 * 2):
                                self.summary_values["one_year"]["value"] += 1

                            # Two year and older, but less than three years
                            elif "updated" in k and item.get("enabled") and (365 * 2 <= age < 365 * 3):
                                self.summary_values["two_years"]["value"] += 1

                            # Three years and older
                            elif "updated" in k and item.get("enabled") and age >= 365 * 3:
                                self.summary_values["three_years"]["value"] += 1

                        if "expires" in k and item.get("enabled") and not v:
                            self.summary_values["missing"]["value"] += 1

                self.items.append(item)
                self.total_scanned_records_count += 1

    def add_summary(self):
        """Creates a summary with stats of the parsed result. Also added to the full version of the report."""

        self.summary = {}
        self.summary_values["vaults"]["value"] = len(self.vaults)
        self.summary_values["vaults_error"]["value"] = len(self.vaults_failed)
        self.summary_values["records"]["value"] = self.total_scanned_records_count

        rows = []
        for k, v in self.summary_values.items():
            if "heading" in k:
                rows.append(v)
            elif isinstance(v, dict):
                value = v.get("value")
                if value:
                    text = v.get("text")
                    rows.append([text, value])
                    self.summary[text] = value

        self.report_full["summary"]["rows"] = [self.summary]

    def add_report(self, expire_threshold=None, alert_threshold=None, ignore_no_expiration=True,
                   include_all=False, teams_alerts=False):
        """Creates a detailed 'column and rows' reports with comment.

        The column names are defined in the 'config.py' file.

        The values for the "Comment" column is generated according to the age of 'updated', 'created' and 'expires'.
        If missing 'expires' then a comment concerning that is added.

        When a row is completed it is added to the report(s), according to input arguments.
        A json object of a completed row is ALWAYS created.

        Parameters
        ----------
        expire_threshold : int
            Ignore to report the record if days till the secret will expire are more than this 'expire_threshold' value
            NOTE: Secrets expiring today or already expired will always be reported.
        alert_threshold : int
            If specified, a Slack Markdown post of the row will be created, IF the row contains a record which days to
            expiring/expired (+/-) are within the value of 'alert_threshold' value.
            The markdown post will then be added to a 'slack_alert_rows' list.
        ignore_no_expiration : bool
            Reports all records if set to False. If set to True only secrets with Expiration Date set will be reported.
        include_all : bool
            If set to True all records are included in the output.
        teams_alerts : bool
            If set to True then the alert cards (if any) will be MS Teams formatted, if not the cards will be in
            Slack Markdown format.
        """
        if not isinstance(self.results, list):
            return

        heading = self.report_values.get("heading")

        # Add header to CSV report
        self.report_csv.append(heading)

        # Ensure only heading and no data rows
        rows = [heading]
        rows_all = [heading]

        # Sort the items from top and down
        # First sort by the oldest 'Expiration' date
        # Then sort by the oldest 'Last Updated' date
        items = self.sort_items()

        for item in items:

            # If no Vault Name, we skip to next item in the list
            vault_name = item.get("vault_name", "")
            if not vault_name:
                continue

            error = item.get("error")
            if error:
                record_type = item.get("record_type", "-")
                vault_name = item.get("vault_name", "-")
                error = item.get("error", "")
                record_name = "ERROR"
                updated = ""
                expires = ""
                comment = "Unknown error"
                if error:
                    comment = f"Error: {error.replace('a new ', '')}"

                row = [record_name, record_type, vault_name, updated, expires, comment]
                rows_all.append(row)
                rows.append(row)
                continue

            # Get the record name
            record_name = item.get("record_name", "ERROR")

            # Get the record type
            record_type = item.get("record_type", "")

            # Get the expires, update and enabled values
            expires = item.get("expires", "")
            expires_age = item.get("expires_age")
            updated = item.get("updated")
            updated_age = item.get("updated_age")
            enabled = item.get("enabled")

            # Add to row: the values of: 'record_name', 'record_type', 'vault_name' and 'updated'
            row = [record_name, record_type, vault_name, updated]

            # Add to row: the value of: 'expires' (if any)
            if expires:
                row.append(expires)
            else:
                row.append(" ")

            # Create 'comment' variable
            # The value of 'Comment' is dependent of the info from the 'expires' and 'update' values
            comment = ""
            if not enabled:
                comment += "Disabled. "

            if isinstance(expires_age, int):
                if expires_age <= 0:
                    comment += f"Will expire in {abs(expires_age)} days. "
                if expires_age > 0:
                    comment += f"Expired {expires_age} days ago. "

            if not expires:
                comment += f"Has no expiration date. "

            if isinstance(updated_age, int):
                comment += f"Updated {updated_age} days ago. "

            # A little cosmetic touch to avoid plural where it should not be used
            comment = comment.replace(" 1 days", " 1 day")

            # Add the comment to the row
            row.append(comment)

            # The row is now complete
            # Add the row to the rows_all (The ones that will be stored in db, but not necessarily will be alerted on)
            rows_all.append(row)

            # Add the row to CSV report
            self.report_csv.append(row)

            # Only include disabled entries if set to include_all
            if not include_all and not enabled:
                continue

            # Skip records with no Expiration Date set, only if 'ignore_no_expiration' and not 'include_all'
            if not expires:
                if ignore_no_expiration and not include_all:
                    continue

            # If the record has Expiration Date set, check if it should be alerted and/or reported on
            if isinstance(expires_age, int):
                # Check if soon expiring OR expired recently (the alert_threshold range)
                # If so, a Slack Markdown Payload of current row will be created
                # and added to the list of Slack Markdown payloads,
                if isinstance(alert_threshold, int):
                    alert = False

                    # The record has not expired, but is within the alert_threshold range
                    if 0 >= expires_age >= -alert_threshold:
                        logging.info(f"{record_name} - expiring in {abs(expires_age)} days.")
                        alert = True

                    # The record has expired and is within the alert_threshold range
                    if 0 < expires_age <= alert_threshold:
                        logging.info(f"{record_name} - expired {expires_age} days ago.")
                        alert = True

                    if alert:
                        logging.info(f"{record_name} - alert_threshold is set to '{alert_threshold}'.")

                        if teams_alerts:
                            card = teams_card(heading, row)
                            if card:
                                logging.info(f"{record_name} - MS Teams alert payload created.")
                                self.teams_alert_cards.append(card)

                        else:
                            logging.info(f"{record_name} - will be alerted to Slack.")
                            card = slack_card(heading, row)
                            if card:
                                logging.info(f"{record_name} - Slack alert payload created.")
                                self.slack_alert_cards.append(card)

                if expires_age < 0:
                    # The record has not expired yet
                    logging.info(f"{record_name} - has not expired yet. "
                                 f"It will expire in {abs(expires_age)} days ({expires}).")

                    # Handle those within the valid 'expire_threshold' range
                    # Those record will not be included in the standard report.
                    # They will only be included in the full report or if 'include_all' is set to True
                    if isinstance(expire_threshold, int) and expire_threshold < abs(expires_age):
                        logging.info(
                            f"{record_name} - Expiration Date is within the valid specified threshold of "
                            f"{expire_threshold} days. This record will start to be "
                            f"reported in {abs(expires_age) - expire_threshold} days.")

                        # This record is within the valid 'expire_threshold' range so the loop will
                        # not proceed with adding the row the list of rows
                        # unless if 'include_all' is set to True, then the row will be added.
                        if not include_all:
                            continue

                else:
                    # The record has expired or is expiring today
                    logging.info(f"{record_name} - expired {expires_age} days ago.")

            # Then finally add the row to the rows which will be reported on
            rows.append(row)

        # All the rows are now processed. Only the wanted rows are kept and will be used to create the reports

        # A json object of all rows are always created.
        self.report_full["report"]["rows"] = self.create_kv_rows(rows_all)

        # If 'include_all' argument is set to True, then 'all_rows' are used instead of the ones not filtered out.
        if include_all:
            rows = rows_all

        if not rows:
            logging.error("No report generated.")
            return

        # Create the reports
        if len(rows) > 1:
            # Create json of the report
            self.report = self.create_kv_rows(rows)

            logging.info("report generated.")

    def create_kv_rows(self, rows):
        """Creates key/value pairs of the items in the rows.

        Returns
        -------
        A list of row items as dicts.
        """

        kv_rows = []
        for i, r in enumerate(rows):
            if i > 0:
                j = {}
                for n, v in enumerate(self.report_values.get("heading")):
                    j[v] = r[n]
                kv_rows.append(j)
        return kv_rows

    def get_report_full(self):
        """Returns the dict version of the full report were all the rows are included and a dict of the summary."""
        return self.report_full

    def get_report(self):
        """Returns a list of dict versions of the filtered rows."""
        return self.report

    def get_summary(self):
        """Returns the dict version of the summary."""
        return self.summary

    def get_teams_alerts(self):
        """Returns the list of Teams alert cards payloads."""
        return self.teams_alert_cards

    def get_slack_alerts(self):
        """Returns the list of Slack alert cards messages."""
        return self.slack_alert_cards
