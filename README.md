<div align="center">

<img src="./hero.svg" width="100%" alt="ALDO. Software engineer. Systems, iOS and web. Boston." />

<img src="https://readme-typing-svg.demolab.com?font=Fira%20Code&weight=700&size=16&duration=2600&pause=700&color=FCEE0A&center=true&vCenter=true&width=780&lines=SDE%20Co-op%20%40%20Philips%2C%20System%20Integration%3BLead%20Full%20Stack%20%40%20Pinnatec%20Auto%2C%20Virtual%20Link%3BBackend%20%40%20Pawtograder%2C%20Northeastern%27s%20autograder%3BCo-founder%20%40%20Sideband%2C%20studio%20in%20Boston%3Bex-SDE%20Intern%20%40%20AWS%20CloudFormation%2C%20Seattle%3BCS%20%2B%20Political%20Science%20%40%20Northeastern%20%2727" alt="Typing SVG" />

<br/>

[![Portfolio](https://img.shields.io/badge/PORTFOLIO-aliyounes.dev-FCEE0A?style=for-the-badge&labelColor=07070C)](https://aliyounes.dev) [![Resume](https://img.shields.io/badge/RESUME-read-00F0FF?style=for-the-badge&labelColor=07070C)](https://aliyounes.dev/resume) [![Sideband](https://img.shields.io/badge/STUDIO-sideband.studio-FF2E88?style=for-the-badge&labelColor=07070C)](https://sideband.studio) [![LinkedIn](https://img.shields.io/badge/LINKEDIN-connect-00F0FF?style=for-the-badge&labelColor=07070C)](https://www.linkedin.com/in/alialdoyounes/) [![Email](https://img.shields.io/badge/EMAIL-reach%20out-EAFEFF?style=for-the-badge&labelColor=07070C)](mailto:younes.al@northeastern.edu)

</div>

<div align="center"><img src="./divider_pink.svg" width="760" /></div>

## `> whoami`

```yaml
handle:   "whoisaldo"
name:     "Ali Younes"
base:     "Boston, MA"
now:
  - { role: "SDE Co-op, part-time",     org: "Philips",       at: "Cambridge, MA" }
  - { role: "Lead Full Stack Engineer", org: "Pinnatec Auto", at: "Worcester, MA" }
  - { role: "Backend Engineer",         org: "Pawtograder",   at: "Boston, MA"    }
also:     "Co-founder at Sideband. Four of us. Our own products, no client work."
prev:     "SDE Intern on the AWS CloudFormation Registry. Seattle, summer 2026."
school:   "Northeastern University, CS and Political Science, class of 2027"
writes:   ["Rust", "Swift", "TypeScript", "Java", "Python", "C++", "C#", "Go", "PHP"]
works_on: ["systems", "iOS", "web", "cloud control planes", "deployment infra"]
rule:     "if the number was not measured, do not quote it"
outside:  ["powerlifting", "wrestling", "a supercharged B8.5 S4 I tuned myself"]
```

I write systems software, iOS apps, and the web front-ends that sit on top of them.
Most of what is here exists because something I wanted did not do what I asked, or cost too much.

It started at 12. I scripted other people's Roblox games, got paid in Robux, and cashed it out
through DevEx for gaming PC parts my family could not have bought me. In 2020 I wrote a Python bot
to watch for GPU restocks so I could get one at MSRP, because I was 15 and wanted a better machine.
The pattern has not changed.

I over-engineer, and I keep the result intuitive. Whoever is using it should never have to know
what is underneath. The $40 iPad app I refused to buy became a Rust host with a hardware encoder
chain and my own UDP protocol, and the person using it just sees a second screen.

<div align="center"><img src="./divider_cyan.svg" width="760" /></div>

## `> gh repo list whoisaldo --sort=stars`

<div align="center">

[![EternalMonitor](https://img.shields.io/github/stars/whoisaldo/EternalMonitor?style=for-the-badge&label=ETERNALMONITOR&labelColor=07070C&color=FCEE0A&logo=github&logoColor=FCEE0A)](https://github.com/whoisaldo/EternalMonitor) [![EternalRichPresence](https://img.shields.io/github/stars/whoisaldo/Eternal-Rich-Presence?style=for-the-badge&label=ETERNALRICHPRESENCE&labelColor=07070C&color=FF2E88&logo=github&logoColor=FF2E88)](https://github.com/whoisaldo/Eternal-Rich-Presence)

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

## `> ls ./projects --all`

**[Eternal Monitor](https://github.com/whoisaldo/EternalMonitor)** · [eternalmonitor.dev](https://eternalmonitor.dev) ![](https://img.shields.io/badge/IN_DEV-FF2E88?style=flat-square&labelColor=07070C) ![](https://img.shields.io/github/stars/whoisaldo/EternalMonitor?style=flat-square&labelColor=07070C&color=FCEE0A&logo=github&logoColor=FCEE0A&label=)
> I refused to pay $40 for an iPad-as-second-display app that lagged. So I wrote my own. A Rust host captures the Windows desktop through DXGI Desktop Duplication, encodes H.264 on whatever silicon is in the machine (it probes NVENC, AMF and QSV, then falls back to libx264), and fragments every frame behind a 16-byte UDP header I wrote. The iPad client decodes on VideoToolbox and draws through a Metal-backed `MTKView`.
>
> UDP instead of TCP was on purpose. A dropped frame should be a dropped frame, not head-of-line blocking.
>
> It mirrors the primary display today. No extended desktop, no input relay. I have not instrumented glass-to-glass latency, so I do not quote a number for it.
>
> `v0.1.2-mirror` · 5,900 lines of Rust, 3,700 of Swift · MIT

`Rust` `Swift` `DXGI` `H.264` `VideoToolbox` `Metal` `FlatBuffers` `tokio` `mDNS`

---

**[Eternal Rich Presence](https://github.com/whoisaldo/Eternal-Rich-Presence)** · [eternalrichpresence.dev](https://eternalrichpresence.dev) ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C) ![](https://img.shields.io/github/stars/whoisaldo/Eternal-Rich-Presence?style=flat-square&labelColor=07070C&color=FCEE0A&logo=github&logoColor=FCEE0A&label=)
> Apple Music does not talk to Discord, and Discord's Listen Along is Spotify-only. This makes both work. It reads now playing from the iTunes COM interface and Windows SMTC, pushes it through pypresence, and uploads cover art down a litterbox, 0x0, catbox fallback chain so one host going down does not take the artwork with it.
>
> The part worth reading: pypresence is send-only, so Listen Along was impossible with it. I open Discord's IPC named pipes (`\\.\pipe\discord-ipc-0..9`) directly over ctypes and kernel32, speak the frame protocol by hand, and subscribe to `ACTIVITY_JOIN`. Registering `eternalrp://` in HKCU means a join link works without admin rights.
>
> `v1.0.0-beta` · 74 tests across ~3.9k lines · SHA-256 published per release

`Python` `WinRT/SMTC` `COM` `Discord IPC` `spotipy` `pystray` `PyInstaller`

---

**[EternalExchange](https://github.com/whoisaldo/EternalExchange)** · [eternalexchangemod.com](https://eternalexchangemod.com) ![](https://img.shields.io/badge/PRE--RELEASE-FF2E88?style=flat-square&labelColor=07070C)
> ProjectE is the canonical equivalent-exchange mod for Minecraft and it is Forge-only. Fabric had nothing comparable, so I wrote the Fabric-native spin-off. It is credited openly in the README and the LICENSE.
>
> The solver is the centre of it. At server start and after every `/reload` it walks the whole loaded recipe graph and propagates values outward from a seed set, in exact `BigFraction` arithmetic so fractional intermediates never drift into rounding errors. Add another mod and its recipes get priced with no patch from me.
>
> Fabric does not have the primitives the original assumes. No capabilities, no attachments, no item handlers, no event bus. So the mod carries a 2,031-line compatibility layer and 9 Mixins standing in for hooks Fabric never fires.
>
> `v1.0.0` pre-release · 39,399 lines across 450 files · saves from the NeoForge original load

`Java 21` `Fabric` `Mixin` `Gradle · Loom` `Commons Math`

---

**[Exerly Fitness](https://github.com/whoisaldo/Exerly-Fitness)** · [exerlyfitness.com](https://exerlyfitness.com) ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C)
> Every commercial fitness app is paywalled. I wanted a free one, so this is free and open source. An npm-workspaces monorepo (`apps/api`, `apps/web`, `apps/ios`) behind one REST backend, so the browser and the phone read the same account. The AI coach builds its prompt from your real profile, your age, weight, goals and logged progress, instead of answering in a vacuum.
>
> Web is live. The iOS client is written: 71 Swift files, roughly 9k lines, a 12-step onboarding that computes maintenance calories with Mifflin-St Jeor. It has not shipped to the App Store yet, so the site says coming soon and so do I.

`SwiftUI` `HealthKit` `React 19` `TypeScript` `Express 5` `MongoDB` `SQLite` `Gemini 2.0 Flash-Lite`

---

**[Sideband](https://sideband.studio)** · co-founder ![](https://img.shields.io/badge/LIVE-FCEE0A?style=flat-square&labelColor=07070C)
> An independent software studio in Boston. Founded in 2025 as Eternal Reverse, renamed Sideband in 2026. Two of us then, four founders now. We ship our own products and take no client work. Six so far, four live.
>
> I started it because I want somewhere younger engineers can get free mentoring as I get better at this. I write the Rust and Swift behind Eternal Monitor, the SwiftUI app and Node API behind Exerly, and most of the studio site.

`Next.js 14` `TypeScript` `Rust` `SwiftUI` `Node.js` `Tailwind` `Framer Motion`

---

<details>
<summary><code>&gt; ls ./projects --archived</code></summary>

<br/>

| project | what it is | stack |
|---|---|---|
| [Moops Bookstore](https://moopsbooks.com) | I was reading more and wanted somewhere to track it with my friends. Goodreads is fine, but it is not ours. Source private. | `MERN` `JWT` |
| [Signature Cuts 413](https://signaturecutschicopee.com) | A barbershop in Chicopee taking every booking by phone. The booking flow compiles into a WhatsApp deeplink, so there is no backend to keep alive. | `Next.js 14` `SSG` |
| [Real-Time Face Analytics](https://whoisaldo.github.io/real-time-face-analytics/) | Face, emotion, age and gender detection with nothing leaving the machine. | `TF.js` `face-api.js` |
| [BetterAppleMusic](https://github.com/whoisaldo/BetterAppleMusic) | Windows desktop Apple Music client. | `Electron` `MusicKit JS` |
| [VirtualDyno](https://github.com/whoisaldo/VirtualDyno) | Estimates horsepower and torque without a dyno. | `Simulation` |
| [Lua-Roblox-Commands](https://github.com/whoisaldo/Lua-Roblox-Commands) | Where this started, though not the code from back then. | `Lua` `Roblox` |

</details>

<div align="center"><img src="./divider_pink.svg" width="760" /></div>

## `> git log --author=aldo --graph --decorate`

```
* Philips · SDE Co-op, System Integration         Jan 2026 to now · Cambridge, MA
│   About a thousand machines in FDA-regulated patient-monitoring infrastructure,
│   each one imaged by a technician with a USB stick. UEFI Secure Boot had to stay
│   on the whole time, which kills every standard fleet-imaging shortcut. Many
│   engineers had wanted this automated. Nobody had shipped it. I pitched it,
│   designed it and shipped it solo.
│   The first attempt reached Windows PE on a custom-signed chain, then needed a
│   keypress per machine to enroll the key, so I threw it out. The second used
│   Microsoft's own signed Boot Manager as the PXE boot program, trusted by every
│   Secure Boot firmware shipped since 2012. Power on, and the machine provisions
│   itself.
│   FOG on Ubuntu 24.04 with dnsmasq proxyDHCP and tftpd-hpa, a PowerShell
│   orchestrator running inside WinPE, a FastAPI service handing each machine its
│   MAC-keyed config. Presented to 50+ engineers and stakeholders.
│   The co-op ran January to June. I have been back on the same team part-time
│   since August, alongside the degree.
│
* Pinnatec Auto · Lead Full Stack Engineer        Sep 2026 to now · Worcester, MA
│   Code owner on Virtual Link, an app-controlled lowering module: Expo and React
│   Native app, WordPress and PHP backend, ESP32 firmware, three-person team.
│   Part-time, alongside Philips and the degree.
│   17 pull requests in my first week, 12 merged. Neither repository had CI. Both
│   now refuse a pull request until typecheck, lint, tests, the seven contracts the
│   firmware and the app share, and both firmware builds pass.
│   Audited the 463-file monorepo and removed 214,000+ lines of dead code,
│   duplicated research trees and tracked build output, in five reviewed commits.
│   Zero compiler warnings before and after.
│
* Pawtograder · Backend Engineer                  Aug 2026 to now · Boston, MA
│   Northeastern's open-source autograder, running in production against real
│   submissions for the university's CS courses. Eleven engineers on the team,
│   three of us own the grading server.
│   The scoring algorithm is the complicated part. Every submission runs lint,
│   build, the instructor's tests and optional pitest mutation analysis inside a
│   GitHub Action in the student's own repository. The results come back to Deno
│   edge functions on Supabase and turn into a grade. Gradebook recalculation is
│   Postgres and PL/pgSQL.
│
* Amazon · SDE Intern, AWS CloudFormation         Jun 2026 to Sep 2026 · Seattle, WA
│   Owned the team's tier-1 deliverable end to end: policy-based sharing of private
│   resource types across an AWS Organization, on the CloudFormation Registry.
│   Before it, reusing a private type meant registering it again in every account.
│   One type had been cloned into 8,000+ accounts across 8 regions. Now the
│   management account publishes one ALLOW/DENY policy and every permitted account
│   references the type by bare name. A consumer's own type always wins, so turning
│   sharing on cannot break a workload that already runs.
│   Shipped in production Java over 12 merged code reviews: 2 new public APIs, a
│   DynamoDB table and DAO, an IAM-style deny-by-default policy evaluator, and
│   org-aware type resolution on the service's read paths.
│   Review caught the org lookup, a strongly consistent uncached read, firing on
│   ~90% of DescribeType traffic the cached tiers already answered. The cheap tiers
│   go first now, so the expensive read only fires on a true miss.
│   Two things I built on the side. A dual-model code reviewer for Kiro, where GPT
│   and Claude critique the same diff and what they agree on leads the report. I
│   presented it to the whole CloudFormation org, spoke about it at a Kiro launch
│   event, and Kiro put it on their LinkedIn. And a Slack bot that hands a ticket to
│   a Bedrock agent, sandboxed on the caller's own cloud desktop under a scoped IAM
│   role. Scoping that role was the hard part. AppSec approved it.
│
* Top Choice Realty · Frontend Developer Intern   Apr 2024 to Aug 2024 · New York, NY
│   Twenty real estate agents, none of them technical, and 800+ client records they
│   had to ask someone else to look up. I built them a client-management app in
│   React, Python and SQL so they could do it themselves. A lookup went from 5+
│   minutes to 45 seconds. Reworked the queries and added caching for 3x faster
│   retrieval. IT tickets dropped 90%.
│
* Robert DeFalco Realty · Computer Technician     Jun 2023 to Sep 2023 · New York, NY
│   IT across three offices. 15+ machines configured on Windows, macOS and Linux,
│   25+ issues resolved, 95%+ uptime. If it has screws in it I have probably had it
│   open, and this is where that started paying.
│
* Northeastern · CS + Political Science           2023 to 2027 · Boston, MA
    Combined-major B.S. Data structures and algorithms, object-oriented design,
    systems programming, databases, networks.
    Wrestling · Powerlifting Club · Arab Student Association
```

<div align="center"><img src="./divider_cyan.svg" width="760" /></div>

## `> cat ./stack.json`

<div align="center">

[![Languages](https://skillicons.dev/icons?i=rust,swift,ts,java,py,cs,cpp,go,php,bash&perline=10&theme=dark)](https://skillicons.dev)

[![Frameworks](https://skillicons.dev/icons?i=react,nextjs,nodejs,express,fastapi,dotnet,tailwind,vite,gradle,powershell&perline=10&theme=dark)](https://skillicons.dev)

[![Infra](https://skillicons.dev/icons?i=aws,docker,linux,postgres,mongodb,supabase,deno,githubactions,git,vim&perline=10&theme=dark)](https://skillicons.dev)

</div>

Most of my work has been automating something tedious. For years that meant deterministic code.
Frontier models handle the parts that never fit a fixed script, and that is the part I find amazing.
I spend my free time on whatever people are using right now, looking for the piece of my routine it
can take.

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
[SHIP]  Eternal Rich Presence ...... v1.0.0-beta · Apple Music to Discord
[DEV ]  Eternal Monitor ............ v0.1.2-mirror · Rust host, Swift client
[DEV ]  EternalExchange ............ v1.0.0 pre-release · 39K lines of Java
[DEV ]  Exerly Fitness ............. web live · iOS built, not on the store yet
[PAST]  AWS CloudFormation ......... summer 2026 · Registry control plane
[EDU ]  Northeastern ............... CS + PoliSci · graduating May 2027
[LIVE]  Wrestling + powerlifting ... 285 lb bench at 145 lbs
[LIVE]  Audi S4 B8.5 ............... 540 whp · tuned it myself
[WARN]  Sleep schedule ............. undefined....
```

<div align="center">

<br/>

[![Visitors](https://komarev.com/ghpvc/?username=whoisaldo&style=for-the-badge&color=FF2E88&labelColor=07070C&label=DATA_RUNNERS)](https://github.com/whoisaldo)

<img src="https://readme-typing-svg.demolab.com?font=Fira%20Code&weight=700&size=13&duration=4200&pause=1100&color=FCEE0A&center=true&vCenter=true&width=560&lines=let%27s%20build%20something%2C%20choom.%3Bthe%20good%20stuff%20is%20in%20the%20commit%20history.%3B_" alt="footer" />

</div>
