# azure-key-vault-report  
  
## Description  

----
**NOTE:** This package will be refactored to use [ops-py-reports](https://github.com/equinor/ops-py-reports)
to generate the various report formats
----

Generates reports from the output of `az keyvault` commands.
    
The column names/header/key values for the reports are defined in the `config.py` file.    
- The input if a list of the output from a `az keyvault` command
    
### The summary
A summary (stats about the records) of the outputs of the `az keyvault` commands.
 
- **Total number of vaults**
- **Total number of records**
- **Records already expired**
- **Records missing Expiration Date**
- **Records updated in the last year**
- **Records NOT updated in the last year**
- **Records NOT updated for the last 2 years**
- **Records NOT updated for the last 3 years**

**NOTE:** Defined in the `config.py` file.

**Available as:**
- JSON (dict)
- Plain text Markdown

### The rows 
The processed and enriched outputs of the `az keyvault` commands.  
Defined in the `config.py` file:

- **Record Name**
- **Record Type**
- **Vault Name**
- **Last Updated**
- **Expiration**
- **Comment** May include info about:  
   - Days to when the secret will expire  
   - Days since the secret expired  
   - Info if the secret has no expiration date set  
   - Days since the Secret was last updated  

**Available as:**
  - JSON (dict)
  - Plain text Markdown

**NOTE:** Will include *all* rows if `include_all` is set to `True`.    
If not, only the rows not filterer out by any of the parameters will be added.

### The summary and the rows combined

**Available as:**
  - JSON (dict) 
  - Plain text Markdown
 
**Full report**          
A dict version of the full report were all the rows are included (unfiltered) and a dict of the summary is ALWAYS created. 

**Available as:**
  - JSON (dict)  
 
### MS Teams payload with facts and a HTML table 
A payload ready to be posted to a MS Teams webhook.

Consists of a title, facts (the summary) and a html table of the rows.

The MS Team payload will use the following base template:     
```  
{  
 "@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "0076D7", "summary": "-", "sections": [ { "activityTitle": "<TITLE>", "activitySubtitle": "", "activityImage": "", "facts": [], "markdown": true }, { "startGroup": true, "text": "<TEXT>" } ]}  
```  
- `activityTitle` will contain the value of the provided `title` - `facts` will contain the rows from the summary table     
- `text` may contain additional data. Defaults to a html table  
  
### Slack items
Items to be posted to Slack.  

**Slack Markdown items**  
These posts are only generated if the records is filtered by the `critical_threshold` parameter.  

**Slack Workflow items**  
List of tuple pairs ("title" and "text") to be posted to a Slack Workflow.  
The text is made up of the summary and the rows as a plain text Markdown table.  

**Slack App items**  
List of dicts to be converted to json and posted to a Slack App.  
The key name of the json is "text". The value is a formatted message made up of a title and the rows as a plain text Markdown table.  


## parameters (add_report)
The reports are generated based on the following `add_report` method parameters  
`expire_threshold`  
`critical_threshold`   
`ignore_no_expiration`    
`include_all`  
`teams_json`  

  
## Installation  
`pip install ops-py-azure-key-vault-report`  

  
## Usage  
The `azure_key_vault_report` object must be initialized with the json output of one more `az keyvault` list commands.    
Please refer to the code documentation provided in the `az_cmd.py` file.      
  
Example code which will process the records of type `secret`and `certificate`from a Key Vault named `kv-test` in the subscription:  
**NOTE:** `az login` and `az account set --subscription ...` must have been executed prior to running this code.  

### Initial code
```   
import az_cmd  
import azure_key_vault_report  
  
vaults = ["kv-test"]  
az_results = []  
for vault in vaults:  
    az_results += az_cmd.az_cmd(vault, ["secret", "certificate"])  
  
kv_report = azure_key_vault_report.AzureKeyVaultReport(az_results)  
kv_report.parse_results()  
kv_report.add_summary()  
```

### Only records with Expiration date set
Process the records, but filter out records not having a **Expiration** date set:  
```
kv_report.add_report()
```

### Get various results
**The summary only**  
As plaintext Markdown table:  
```
out = kv_report.get_summary_markdown()  
print(out)
```
As dict:  
```
out = kv_report.get_summary()  
print(out)
```

**The report only**  
As plaintext Markdown table:  
```
out = kv_report.get_report_markdown()  
print(out)
```
As list of dicts:  
```
out = kv_report.get_report()  
print(out)
```

**Combined summary and report as plaintext Markdown table**  
```
out = kv_report.get_report_summary_markdown()  
print(out)
```

**Full report - combined summary and report - as dict**  
This will include all the processed records, even the ones not having an **Expiration** date set.  
It will always include all the processed records, regardless of the add_report parameters.  

```
out = kv_report.get_report_full()  
print(out)
```

**Full report - combined summary and report - as plaintext Markdown table**  
To include all and output as plaintext Markdown the `include_all` parameter has to be set to `True`  
```
kv_report.add_report(include_all=True)  
out = kv_report.get_report_summary_markdown()  
print(out)
```

**Only expired and soon expiring records - combined summary and report**  
Soon expiring records are defined by the `expire_threshold` parameter.  
E.g. to only list records that will expire within the next 30 days (expired are automatically included):  

```
kv_report.add_report(expire_threshold=30) 
```

As plaintext Markdown table:  
```
out = kv_report.get_report_summary_markdown()  
print(out)
```

As plaintext Markdown table in a Slack App post:  
```
out = kv_report.get_slack_payloads("My Key Vault report")  
print(out)
```

As plaintext Markdown table in a Slack Workflow post:  
```
out = kv_report.get_slack_payloads("My Key Vault report", app=False)  
print(out)
```

As MS Team payload with html_table:  
```
kv_report.add_report(expire_threshold=30, teams_json=True) 
out = kv_report.get_teams_payload("My Key Vault report")  
print(out)
```

**Critical records as Slack post messages**  
Slack Markdown JSON will be generated from a row if it contains a record which is within the `critical_threshold`parameter.  

E.g. if the `critical_threshold` is set to `7`, a Slack Markdown JSON of the row is generated    
if the row contains a record which is **expiring within the next 7 days** OR   
if the record has **already expired, but only for 7 or fewer days**.  

```
kv_report.add_report(critical_threshold=7)
out = kv_report.get_slack_payloads("title", md=True)  
print(out)
```