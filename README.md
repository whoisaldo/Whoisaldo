<div align="center">

<img src="./hero.svg" width="100%" alt="ALDO. Software engineer. Systems, iOS and web. Boston." />

<img src="https://readme-typing-svg.demolab.com?font=Fira%20Code&weight=700&size=16&duration=2600&pause=700&color=FCEE0A&center=true&vCenter=true&width=780&lines=SDE%20Co-op%20%40%20Philips%2C%20System%20Integration%3BLead%20Full%20Stack%20%40%20Pinnatec%20Auto%2C%20Virtual%20Link%3BBackend%20%40%20Pawtograder%2C%20Northeastern%27s%20autograder%3BCo-founder%20%40%20Sideband%2C%20studio%20in%20Boston%3Bex-SDE%20Intern%20%40%20AWS%20CloudFormation%2C%20Seattle%3BCS%20%2B%20Political%20Science%20%40%20Northeastern%20%2727" alt="Typing SVG" />

<br/>

[![Portfolio](https://img.shields.io/badge/PORTFOLIO-aliyounes.dev-FCEE0A?style=for-the-badge&labelColor=07070C)](https://aliyounes.dev) [![Resume](https://img.shields.io/badge/RESUME-read-00F0FF?style=for-the-badge&labelColor=07070C)](https://aliyounes.dev/resume) [![Sideband](https://img.shields.io/badge/STUDIO-sideband.studio-FF2E88?style=for-the-badge&labelColor=07070C)](https://sideband.studio) [![LinkedIn](https://img.shields.io/badge/LINKEDIN-connect-00F0FF?style=for-the-badge&labelColor=07070C)](https://www.linkedin.com/in/alialdoyounes/) [![Email](https://img.shields.io/badge/EMAIL-reach%20out-EAFEFF?style=for-the-badge&labelColor=07070C)](mailto:younes.al@northeastern.edu)

</div>

<div align="center"><img src="./divider_pink.svg" width="760" /></div>

## `> whoami`

```yaml
name:   "Ali Younes"
base:   "Boston, MA"
now:
  - { role: "SDE Co-op, part-time",     org: "Philips",       at: "Cambridge, MA" }
  - { role: "Lead Full Stack Engineer", org: "Pinnatec Auto", at: "Worcester, MA" }
  - { role: "Backend Engineer",         org: "Pawtograder",   at: "Boston, MA"    }
also:   "Co-founder at Sideband. Four of us. Our own products, no client work."
prev:   "SDE Intern on the AWS CloudFormation Registry. Seattle, summer 2026."
school: "Northeastern University, CS and Political Science, class of 2027"
```

I write systems software, iOS apps, and the web front-ends that sit on top of them. Most of what is
here exists because something I wanted did not do what I asked, or cost too much. I over-engineer,
and I keep the result intuitive. Whoever is using it should never have to know what is underneath.

<div align="center"><img src="./divider_cyan.svg" width="760" /></div>

## `> gh repo list whoisaldo --sort=stars`

<div align="center">

<img src="./stars.svg" width="820" alt="Stargazer counts by repository" />

</div>

<!-- STARS:START -->
```
SIGNAL // stargazers across whoisaldo   ·   synced 2026-09-19
──────────────────────────────────────────────────────────────────
EternalMonitor         ████████████████████████████  104  Rust
Eternal-Rich-Presence  ███████                        26  Python
codex-image-skill      ▏                               1  Python
Whoisaldo              ▏                               1  you are here
──────────────────────────────────────────────────────────────────
TOTAL                                                132
```
<!-- STARS:END -->

<div align="center"><img src="./divider_yellow.svg" width="760" /></div>

## `> ls ./projects`

**[Eternal Monitor](https://github.com/whoisaldo/EternalMonitor)** · [eternalmonitor.dev](https://eternalmonitor.dev) ![](https://img.shields.io/badge/IN_DEV-FF2E88?style=flat-square&labelColor=07070C) ![](https://img.shields.io/github/stars/whoisaldo/EternalMonitor?style=flat-square&labelColor=07070C&color=FCEE0A&logo=github&logoColor=FCEE0A&label=)
> I refused to pay $40 for an iPad-as-second-display app that lagged. So I wrote my own. A Rust host captures the Windows desktop through DXGI, encodes H.264 on whatever silicon is in the machine (NVENC, AMF, QSV, then libx264), and fragments every frame behind a 16-byte UDP header I wrote. The iPad decodes on VideoToolbox and draws through a Metal-backed `MTKView`. UDP instead of TCP was on purpose. A dropped frame should be a dropped frame, not head-of-line blocking.
>
> It mirrors the primary display today. No extended desktop, no input relay, and no latency number, because I have not measured one.
>
> `v0.1.2-mirror` · 5,900 lines of Rust, 3,700 of Swift · MIT

`Rust` `Swift` `DXGI` `H.264` `VideoToolbox` `Metal` `tokio`

---

**[Eternal Rich Presence](https://github.com/whoisaldo/Eternal-Rich-Presence)** · [eternalrichpresence.dev](https://eternalrichpresence.dev) ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C) ![](https://img.shields.io/github/stars/whoisaldo/Eternal-Rich-Presence?style=flat-square&labelColor=07070C&color=FCEE0A&logo=github&logoColor=FCEE0A&label=)
> Apple Music does not talk to Discord, and Discord's Listen Along is Spotify-only. This makes both work. pypresence is send-only, so Listen Along was impossible with it. I open Discord's IPC named pipes over ctypes, speak the frame protocol by hand, and subscribe to `ACTIVITY_JOIN`, which is how an Apple Music listener and a Spotify listener end up in sync.
>
> `v1.0.0-beta` · 74 tests across ~3.9k lines · SHA-256 published per release

`Python` `WinRT/SMTC` `COM` `Discord IPC` `pystray` `PyInstaller`

---

**[EternalExchange](https://github.com/whoisaldo/EternalExchange)** · [eternalexchangemod.com](https://eternalexchangemod.com) ![](https://img.shields.io/badge/PRE--RELEASE-FF2E88?style=flat-square&labelColor=07070C)
> ProjectE is the canonical equivalent-exchange mod for Minecraft and it is Forge-only, so I wrote the Fabric-native spin-off. At server start and after every `/reload` the solver walks the whole loaded recipe graph and propagates values outward from a seed set, in exact `BigFraction` arithmetic. Add another mod and its recipes get priced with no patch from me. Fabric does not have the primitives the original assumes, so it carries a 2,031-line compatibility layer and 9 Mixins.
>
> `v1.0.0` pre-release · 39,399 lines across 450 files · saves from the NeoForge original load

`Java 21` `Fabric` `Mixin` `Gradle · Loom` `Commons Math`

---

**[Exerly Fitness](https://github.com/whoisaldo/Exerly-Fitness)** · [exerlyfitness.com](https://exerlyfitness.com) ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C)
> Every commercial fitness app is paywalled, so this one is free and open source. One REST backend behind `apps/api`, `apps/web` and `apps/ios`, so the browser and the phone read the same account. The AI coach builds its prompt from your real profile, your age, weight, goals and logged progress, instead of answering in a vacuum.
>
> Web is live. The iOS client is written, 71 Swift files and roughly 9k lines, but it has not shipped to the App Store yet, so the site says coming soon and so do I.

`SwiftUI` `HealthKit` `React 19` `Express 5` `MongoDB` `Gemini 2.0 Flash-Lite`

---

**[Sideband](https://sideband.studio)** · co-founder ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C)
> An independent software studio in Boston, founded in 2025 as Eternal Reverse and renamed in 2026. Four founders. We ship our own products and take no client work, six so far and four live. I started it because I want somewhere younger engineers can get free mentoring as I get better at this.

`Next.js 14` `TypeScript` `Rust` `SwiftUI` `Node.js` `Framer Motion`

---

<details>
<summary><code>&gt; ls ./projects --archived</code></summary>

<br/>

| project | what it is | stack |
|---|---|---|
| [Moops Bookstore](https://moopsbooks.com) | Reading tracker for me and my friends. Goodreads is fine, but it is not ours. | `MERN` `JWT` |
| [Signature Cuts 413](https://signaturecutschicopee.com) | Barbershop site. Booking compiles into a WhatsApp deeplink, so there is no backend to keep alive. | `Next.js 14` `SSG` |
| [Real-Time Face Analytics](https://whoisaldo.github.io/real-time-face-analytics/) | Face, emotion and age detection with nothing leaving the machine. | `TF.js` `face-api.js` |
| [BetterAppleMusic](https://github.com/whoisaldo/BetterAppleMusic) | Windows desktop Apple Music client. | `Electron` `MusicKit JS` |
| [VirtualDyno](https://github.com/whoisaldo/VirtualDyno) | Estimates horsepower and torque without a dyno. | `Simulation` |
| [Lua-Roblox-Commands](https://github.com/whoisaldo/Lua-Roblox-Commands) | Where this started, though not the code from back then. | `Lua` `Roblox` |

</details>

<div align="center"><img src="./divider_pink.svg" width="760" /></div>

## `> git log --author=aldo --graph`

```
* Philips · SDE Co-op, System Integration         Jan 2026 to now · Cambridge, MA
│   About a thousand machines in FDA-regulated patient-monitoring infrastructure,
│   each one imaged by a technician with a USB stick, and UEFI Secure Boot had to
│   stay on the whole time. Many engineers had wanted this automated. Nobody had
│   shipped it. I pitched it, designed it and shipped it solo.
│   The first attempt needed a keypress per machine to enroll a custom signing key,
│   so I threw it out. The second used Microsoft's own signed Boot Manager as the
│   PXE boot program, trusted by every Secure Boot firmware shipped since 2012.
│   FOG on Ubuntu 24.04, a PowerShell orchestrator inside WinPE, a FastAPI service
│   handing each machine its MAC-keyed config. Presented to 50+ engineers.
│   Co-op January to June. Back on the same team part-time since August.
│
* Pinnatec Auto · Lead Full Stack Engineer        Sep 2026 to now · Worcester, MA
│   Code owner on Virtual Link: Expo and React Native app, WordPress and PHP
│   backend, ESP32 firmware, three-person team, part-time.
│   17 pull requests my first week, 12 merged. Neither repository had CI. Both now
│   refuse a merge until typecheck, lint, tests, the seven contracts the firmware
│   and the app share, and both firmware builds pass.
│   Removed 214,000+ lines of dead code from the 463-file monorepo.
│
* Pawtograder · Backend Engineer                  Aug 2026 to now · Boston, MA
│   Northeastern's open-source autograder, running in production against real
│   submissions. Eleven engineers, three of us own the grading server.
│   Every submission runs lint, build, the instructor's tests and optional pitest
│   mutation analysis in a GitHub Action in the student's own repository. The
│   results come back to Deno edge functions on Supabase and turn into a grade.
│
* Amazon · SDE Intern, AWS CloudFormation         Jun 2026 to Sep 2026 · Seattle, WA
│   Owned the team's tier-1 deliverable end to end: policy-based sharing of private
│   resource types across an AWS Organization. One type had been cloned into 8,000+
│   accounts across 8 regions. Now the management account publishes one ALLOW/DENY
│   policy and every permitted account references the type by bare name.
│   12 merged code reviews in production Java: 2 new public APIs, a DynamoDB table
│   and DAO, an IAM-style deny-by-default policy evaluator, org-aware resolution on
│   the read paths. Review caught the org lookup firing on ~90% of DescribeType
│   traffic, so the cheap tiers go first now and the expensive read waits for a miss.
│   On the side: a dual-model code reviewer for Kiro, GPT and Claude on the same
│   diff, presented to the whole org and featured on Kiro's LinkedIn. And a Slack
│   bot that hands a ticket to a Bedrock agent, sandboxed under a scoped IAM role
│   that AppSec signed off on.
│
* Top Choice Realty · Frontend Developer Intern   Apr 2024 to Aug 2024 · New York, NY
│   Twenty real estate agents, none of them technical, and 800+ client records they
│   had to ask someone else to look up. React, Python and SQL so they could do it
│   themselves. A lookup went from 5+ minutes to 45 seconds. IT tickets dropped 90%.
│
* Robert DeFalco Realty · Computer Technician     Jun 2023 to Sep 2023 · New York, NY
│   IT across three offices. 15+ machines on Windows, macOS and Linux, 95%+ uptime.
│   If it has screws in it I have probably had it open.
│
* Northeastern · CS + Political Science           2023 to 2027 · Boston, MA
    Combined-major B.S.
    Wrestling · Powerlifting Club · Arab Student Association
```

<div align="center"><img src="./divider_cyan.svg" width="760" /></div>

## `> cat ./stack.json`

<div align="center">

[![Languages](https://skillicons.dev/icons?i=rust,swift,ts,java,py,cs,cpp,go,php,bash&perline=10&theme=dark)](https://skillicons.dev)

[![Frameworks](https://skillicons.dev/icons?i=react,nextjs,nodejs,express,fastapi,dotnet,tailwind,vite,gradle,powershell&perline=10&theme=dark)](https://skillicons.dev)

[![Infra](https://skillicons.dev/icons?i=aws,docker,linux,postgres,mongodb,supabase,deno,githubactions,git,vim&perline=10&theme=dark)](https://skillicons.dev)

</div>

```
ai:      OpenAI SDK · Claude SDK · MCP · Ollama · AWS Bedrock
agents:  Kiro · Codex · Claude Code · OpenCode · Windsurf · T3 Code · Cursor Bugbot · CodeRabbit
```

<div align="center"><img src="./divider_yellow.svg" width="760" /></div>

## `> btop --user aldo`

<div align="center">

<img height="165" src="./cards/stats.svg" alt="stats" />
<img height="165" src="./cards/top-langs.svg" alt="top languages" />

<img src="./cards/streak.svg" alt="contribution streak" />

<br/><br/>

[![Followers](https://img.shields.io/github/followers/whoisaldo?style=for-the-badge&label=FOLLOWERS&labelColor=07070C&color=00F0FF&logo=github&logoColor=00F0FF)](https://github.com/whoisaldo?tab=followers) [![EternalMonitor release](https://img.shields.io/github/v/release/whoisaldo/EternalMonitor?include_prereleases&style=for-the-badge&label=ETERNALMONITOR&labelColor=07070C&color=FCEE0A)](https://github.com/whoisaldo/EternalMonitor/releases) [![ERP release](https://img.shields.io/github/v/release/whoisaldo/Eternal-Rich-Presence?include_prereleases&style=for-the-badge&label=ETERNALRICHPRESENCE&labelColor=07070C&color=FF2E88)](https://github.com/whoisaldo/Eternal-Rich-Presence/releases)

</div>

<div align="center"><img src="./divider_pink.svg" width="760" /></div>

## `> tail -f ./now.log`

```
[WORK]  Philips .................... SDE Co-op, part-time · System Integration
[WORK]  Pinnatec Auto .............. Lead Full Stack · Virtual Link · code owner
[WORK]  Pawtograder ................ Backend · grading server · in production
[STDO]  Sideband ................... four founders · six products · Boston
[DEV ]  Eternal Monitor ............ v0.1.2-mirror · Rust host, Swift client
[DEV ]  Exerly Fitness ............. web live · iOS built, not on the store yet
[EDU ]  Northeastern ............... CS + PoliSci · graduating May 2027
[LIVE]  Audi S4 B8.5 ............... 540 whp · tuned it myself
[WARN]  Sleep schedule ............. undefined....
```

<div align="center">

<br/>

[![Visitors](https://komarev.com/ghpvc/?username=whoisaldo&style=for-the-badge&color=FF2E88&labelColor=07070C&label=DATA_RUNNERS)](https://github.com/whoisaldo)

<img src="https://readme-typing-svg.demolab.com?font=Fira%20Code&weight=700&size=13&duration=4200&pause=1100&color=FCEE0A&center=true&vCenter=true&width=560&lines=let%27s%20build%20something%2C%20choom.%3Bthe%20good%20stuff%20is%20in%20the%20commit%20history.%3B_" alt="footer" />

</div>
