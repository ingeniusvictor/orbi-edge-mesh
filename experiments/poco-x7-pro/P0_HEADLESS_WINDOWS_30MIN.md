# P0 Headless — Windows 30-Minute Validation

Status: READY TO RUN

## Target

- Node: Node-01
- Device: POCO X7 Pro 5G
- Endpoint: `http://192.168.1.7:8080`
- Model: Qwen3 1.7B Q4_K_M

## Procedure

1. Keep llama-server running.
2. Start the Windows headless probe.
3. After first PASS, turn the POCO display off.
4. Keep screen off for the full 30-minute window.
5. At ~20 minutes, the probe performs a real chat completion.
6. Record final PASS/FAIL and battery delta.

## PASS

- 7/7 reachability checks pass.
- post-20-minute inference passes.
- screen remains off.
- process survives.
- no abnormal thermal behavior.

## Manual evidence

- Start battery:
- End battery:
- Start temperature/feel:
- End temperature/feel:
- Android warning shown: YES / NO
- Termux killed: YES / NO
- llama-server killed: YES / NO

## Result

- PASS / PASS WITH LIMITATIONS / FAIL
