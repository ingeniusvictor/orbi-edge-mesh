# P0 — Node-01 Headless / Screen-Off Test

Device: POCO X7 Pro  
Status: NOT STARTED

## Objective

Validate that Node-01 can function as an AI/server node with the display off.

## Preconditions

- [ ] P0-B environment certified
- [ ] llama-server works with display on
- [ ] PC can reach Node-01 over LAN
- [ ] battery optimization settings documented
- [ ] Termux wake-lock behavior available/understood

## Procedure

1. Start Node-01 server using the headless launcher.
2. Confirm API response while display is on.
3. Lock the phone / turn display off.
4. From the PC, run a request every 5 minutes.
5. Continue for at least 30 minutes.
6. Record:
   - API availability
   - heartbeat availability
   - successful/failed requests
   - initial/final battery
   - initial/max/final temperature
   - whether Android killed or suspended Termux
7. Turn display back on.
8. Stop the server and release wake lock.

## Acceptance

PASS requires:

- [ ] display remained off
- [ ] API remained reachable
- [ ] at least 6 periodic checks completed
- [ ] at least one inference request completed after 20+ minutes
- [ ] no Android process kill
- [ ] no unsafe thermal behavior
- [ ] battery delta recorded

## Comparison test

Run two comparable 30-minute tests later:

```text
A — screen ON
B — screen OFF
```

Compare:

- battery percentage delta
- thermal behavior
- tokens/s
- API stability

This comparison will quantify the practical benefit on Node-01 rather than assuming a universal percentage saving.
