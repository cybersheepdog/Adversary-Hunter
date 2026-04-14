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
    - [Ares](https://github.com/sweetsoftware/Ares)
    - [Brute Ratel](https://bruteratel.com)
    - [Caldera](https://caldera.mitre.org)
    - [Cobalt Strike](https://cobaltstrike.com)
    - [Covenant](https://github.com/cobbr/Covenant)
    - [Deimos](https://github.com/DeimosC2/DeimosC2)
    - [Empire](https://github.com/EmpireProject/Empire)
    - [Hak5 Cloud C2](https://shop.hak5.org/products/c2)
    - [Havoc](https://github.com/HavocFreamework/havoc)
    - [Mythic](https://github.com/its-a-feature/Mythic)
    - [NimPlant](https://github.com/chvancooten/NimPlant)
    - Oyster
    - Panda
    - [Pantegana](https://github.com/cassanof/pantegana)
    - Poseidon
    - [POSH](https://github.com/nettitude/PoshC2/tree/517903431ab43e6d714b24b0752ba111f5d4c2f1)
    - [RedGuard](https://github.com/wikiZ/RedGuard/tree/main)
    - [RedWarden](https://github.com/mgeeky/RedWarden)
    - [Sliver](https://github.com/BishopFox/sliver)
    - [Supershell](https://github.com/tdragon6/Supershell/tree/main)
    - [Villain](https://github.com/t3l3machus/Villain)
    - [Vshell](https://github.com/veo/vshell)
- Malware
    - AcidRain Stealer
    - Async Rat
    - Atlandida Stealer
    - Bandit Stealer
    - BitRAT
    - Collector Stealer
    - DarkCommet Trojan
    - DarkTrack RAT Trojan
    - DcRAT
    - Gh0st RAT Trojan
    - Hookbot Trojan
    - Meduza Stealer
    - Misha Staler (AKA Grand Misha)
    - Mystic Stealer
    - NanoCore RAT Trojan
    - NetBus Trojan
    - njRAT Trojan
    - Orcus RAT Trojan
    - Patriot Stealer
    - Poison Ivy Trojan
    - Pyrsmax Stealer
    - Quasar Rat
    - RAXNET Bitcoin Stealer
    - Remcos RAT
    - [RisePro Stealer](https://github.com/noke6262/RisePro-Stealer)
    - Sectop RAT
    - ShadowPad
    - Spectre Stealer
    - [SpiceRAT](https://hunt.io/blog/the-secret-ingredient-unearthing-suspected-spicerat-infrastructure-via-html-response)
    - [SpyAgent](https://www.deepinstinct.com/blog/the-russian-spyagent-a-decade-later-and-rat-tools-remain-at-risk)
    - Titan Stealer
    - [Unam Web Panel](https://github.com/UnamSanctam/UnamWebPanel)/SilentCryptoMiner
    - Vidar Stealer
    - Viper RAT
    - XtremeRAT Trojan
    - ZeroAccess Trojan
- Tools
    - [BurpSuite](https://portswigger.net/burp)
    - [DayBreak](https://github.com/tophant-ai/DayBreak) / [DayBreak](https://daybreak.tophant.com/home)
    - [GoPhish](https://getgophish.com)
    - [Hashcat](https://hashcat.net/hashcat/)
    - [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF)
    - [XMRig Monero Cryptominter](https://xmrig.com)
- Botnets
    - [7777](https://gi7w0rm.medium.com/the-curious-caseof-the-7777-botnet-86e3464c3ffd)
    - [BlackNET](https://github.com/suriya73/BlackNET)
    - Doxerina
    - Mozi
    - Scarab

## Running Locally

If you want to host a private version, put your Shodan API key in an environment variable called `SHODAN_API_KEY`, and setup your Censys credentials in `CENSYS_API_ID` & `CENSYS_API_SECRET`

```bash
python3 -m pip install -r requirements.txt
python3 hunter.py
```

## Contributing

I encourage opening an issue/PR if you know of any additional Shodan/Censys searches for identifying adversary infrastructure. I will not set any hard guidelines around what can be submitted, just know, **fidelity is paramount** (high true/false positive ratio is the focus).

