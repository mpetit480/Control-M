# Control-M Python Mail plugin
## Changes on this version

| Date | Who | What |
| - | - | - |
| 2022-07-18 | Mathieu Petit | First release |
| 2025-05-16 | Mathieu Petit | Python is now embedded in job type |


## Contributions

| Date | Who | What |
| - | - | - |


## Short description:
Control-M Integration plugin for MAPI mailbox

## Prerequisites

- Control-M Version 9.20.000,
- Control-M Application pack 9.20
- Python 3


## Installation

- Deploy the integration AIMAILPYTH.ctmai using Application Integrator.
- Install imap_tools library: pip install imap_tools.

 
## Detailed description:

The script detects mail arrivals in a mailbox depending on criteria.
Options:
-	Break: it stops if a mail is found
-	Save attachments to folder
-	Trigger a Control-M Folder/job
 

## Control-M

* #### 1. Connection Profile 

![](./images/connprof.png)

* #### 2. Define a job

![](./images/job.png)

* #### 3. Output

![](./images/output.png)
