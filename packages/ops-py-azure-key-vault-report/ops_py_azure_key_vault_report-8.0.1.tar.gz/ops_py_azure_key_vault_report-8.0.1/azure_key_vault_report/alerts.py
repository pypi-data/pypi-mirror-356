#!/usr/bin/env python


def slack_card(heading, row):
    """Creates a Slack alert payload of the row.

    Returns
    -------
    A dict of the Slack item.
    """

    if not row:
        return

    item = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{row[0]}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{row[-1]}*"
                }
            },
            {
                "type": "section",
                "fields": []
            }
        ]
    }

    blocks = item.get("blocks")
    for i in range(1, len(row) - 1):
        x = {"type": "mrkdwn",
             "text": f"*{heading[i]}:*\n{row[i]}"
             }
        blocks[-1]["fields"].append(x)
    blocks.append({"type": "divider"})
    return item


def teams_card(heading, row):
    """Creates an MS Teams alert payload of the row.

    Returns
    -------
    MS Teams payload.
    """
    if not row:
        return

    item = {"type": "message",
            "attachments": [{"contentType": "application/vnd.microsoft.card.adaptive",
                             "content": {
                                 "type": "AdaptiveCard",
                                 "body": [
                                     {
                                         "type": "TextBlock",
                                         "size": "large",
                                         "weight": "Bolder",
                                         "text": row[0]
                                     },
                                     {
                                         "type": "TextBlock",
                                         "size": "medium",
                                         "weight": "Bolder",
                                         "text": row[-1]
                                     },
                                     {
                                         "type": "TextBlock",
                                         "text": ""
                                     }
                                 ]
                             }
                             }
                            ]
            }

    for i in range(1, len(row) - 1):
        item['attachments'][0]['content']['body'][-1][
            "text"] += f"**{heading[i]}:** {row[i]}\n\n"

    return item
