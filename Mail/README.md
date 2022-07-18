# Control-M Python Mail plugin
## Changes on this version

| Date | Who | What |
| - | - | - |
| 2022-07-18 | Mathieu Petit | First release |


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

- Deploy the integration AI Mail Python.ctmai using Application Integrator.
- Install imap_tools library: pip install imap_tools.
- Copy the script imap_d.py on the agent.

 
## Detailed description:

The script detects mail arrivals in a mailbox depending on criteria.
2 options:
-	Without loop, on Ended OK, it will start another job following conditions
-	With a loop and a job to trigger, it will wait and start itself a job.
 

## Control-M

* #### 1. Connection Profile 

![](./images/connprof.png)

* #### 2. Define a job

![](./images/job.png)

* #### 3. Output

![](./images/output.png)
