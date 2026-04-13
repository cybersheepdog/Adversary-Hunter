# Adversary Hunter
[![Build Status](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-blue.svg)](https://shields.io)
![Maintenance](https://img.shields.io/maintenance/yes/2026.svg?style=flat-square)
![Github last commit](https://img.shields.io/github/last-commit/cybersheepdog/Adversary-Hunter.svg?style=flat-square)

Adversary Hunter is a free-to-use-community-driven IOC feed that uses [Shodan](https://www.shodan.io/) and [Censys](https://search.censys.io/) (hopefully coming soon) searches to collect IP addresses of known malware/botnet/C2 infrastructure.

## Honorable Mentions

This is based on [C2-Tracker](https://github.com/montysecurity/C2-Tracker) by [@montysecurity](https://github.com/montysecurity). C2-Tracker has been archived and is no longer being updated.  The last weekly update was April 6, 2026. I am currently going through and validating the existing signatures in there and will then update with new signatures.  Stay tuned for the weekly update cadence.

## Usage

The most recent collection will be stored in `data/`. The IPs are seperated by the name of the tool and there is an `all.txt` that contains all of the IPs. As it currently stands this feed updates `weekly` on Monday.

The queries for Censys and Shodan are in the code in the respective function and you can see them there.  I am also including a feature to define custom queries in a text file that will be imported into the program and added to the pre-defined queries.  This gives intel and research teams the ability to define queries they may not want to be publically available.

### Investigations/Historical Analysis

- The repo, by its nature, has version control. This means you can search the history of the repo for when an IP was present in the results. 
- I have created a python script to ingest this data into OpenCTI [here](https://github.com/cybersheepdog/opencti-c2-tracker)

## What do I track?

- C2's
    - [Brute Ratel](https://bruteratel.com)
    - [Caldera](https://caldera.mitre.org)
    - [Cobalt Strike](https://cobaltstrike.com)
    - [Covenant](https://github.com/cobbr/Covenant)
    - [Deimos](https://github.com/DeimosC2/DeimosC2)
    - [Havoc](https://github.com/HavocFreamework/havoc)
    - [Mythic](https://github.com/its-a-feature/Mythic)
    - [NimPlant](https://github.com/chvancooten/NimPlant)
    - Panda
    - Poseidon
    - [POSH](https://github.com/nettitude/PoshC2/tree/517903431ab43e6d714b24b0752ba111f5d4c2f1)
    - [RedWarden](https://github.com/mgeeky/RedWarden)
    - [Sliver](https://github.com/BishopFox/sliver)
- Malware
    - AcidRain Stealer
    - Collector Stealer
    - Meduza Stealer
    - Misha Staler (AKA Grand Misha)
    - Mystic Stealer
    - Patriot Stealer
    - RAXNET Bitcoin Stealer
    - Titan Stealer
    - Vidar Stealer
- Tools
    - [DayBreak](https://github.com/tophant-ai/DayBreak) / [DayBreak](https://daybreak.tophant.com/home)
    - [GoPhish](https://getgophish.com)
    - [XMRig Monero Cryptominter](https://xmrig.com)
- Botnets
    - TBD

## Running Locally

If you want to host a private version, put your Shodan API key in an environment variable called `SHODAN_API_KEY`, and setup your Censys credentials in `CENSYS_API_ID` & `CENSYS_API_SECRET`

```bash
python3 -m pip install -r requirements.txt
python3 hunter.py
```

## Contributing

I encourage opening an issue/PR if you know of any additional Shodan/Censys searches for identifying adversary infrastructure. I will not set any hard guidelines around what can be submitted, just know, **fidelity is paramount** (high true/false positive ratio is the focus).

