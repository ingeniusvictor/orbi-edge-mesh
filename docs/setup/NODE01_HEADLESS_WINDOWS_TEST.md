# Node-01 — 30-Minute Screen-Off Test (Windows)

## Goal

Prove that the POCO X7 Pro can behave as a local AI server with the display off.

## Preconditions

- llama-server is already running on Node-01;
- PC and POCO are on the same trusted Wi-Fi;
- Node-01 IPv4 is known;
- `/v1/models` and chat completion already pass from the PC.

## Step 1 — Keep llama-server running

Do not close the original Termux session running:

`listening on http://0.0.0.0:8080`

## Step 2 — Optional but recommended: acquire Termux wake lock

In a second Termux session:

```bash
termux-wake-lock
```

If the command is unavailable, do not improvise. Record that fact and continue with the first supervised test.

## Step 3 — Start Windows probe

From a PowerShell window in the repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\pc\headless_probe_windows.ps1 `
  -HostIp 192.168.1.7 `
  -Port 8080
```

Default behavior:

- 7 checks;
- one check every 5 minutes;
- approximately 30 minutes total;
- an inference test at check 5, around the 20-minute mark;
- local JSON evidence written at the end.

## Step 4 — Turn the POCO display off

Immediately after the first PASS appears on the PC, turn off the POCO screen.

Do not reopen Termux during the test unless the probe fails.

## PASS criteria

- all periodic `/v1/models` checks pass;
- the post-20-minute inference passes;
- llama-server is still alive at the end;
- the screen remained off for the full test;
- no abnormal heat is observed.

## Evidence

Default Windows evidence file:

`node01-headless-probe.json`

Also record manually:

- battery percentage before;
- battery percentage after;
- approximate device temperature/feel;
- whether Android displayed any battery/background warnings;
- whether Termux was killed or suspended.

## Important

This first test is supervised.

Do not yet enable unattended recovery or assume HyperOS background behavior is permanently solved.
