# N6 Native Headless Parity Validation

## Research question

Can ORBI Edge Node reproduce the proven 30-minute Termux screen-off result using only the APK-owned runtime?

## Native mechanism

N6 introduces:

- Android foreground service;
- partial CPU wake lock;
- process-level ORBI runtime ownership;
- trusted-LAN API owned by the service;
- explicit start/stop controls;
- no Termux runtime dependency.

The service type is declared as Android `specialUse` for this sideloaded research build because local AI node operation does not map cleanly to the narrower standard foreground-service categories.

## Physical procedure

1. import and validate the reference GGUF;
2. load Qwen in the native runtime;
3. run one successful in-app inference;
4. start the headless node service;
5. verify `/health` from the Windows PC;
6. launch the existing 30-minute Windows headless probe against the APK API;
7. after check 1/7, turn the POCO display off;
8. do not reopen the app for the full test;
9. require a real inference after at least 20 minutes;
10. record battery and thermal observations.

## PASS

- 7/7 LAN checks pass;
- post-20-minute chat completion passes;
- foreground service remains alive;
- model remains loaded;
- display stays off;
- no Termux process provides inference or serving;
- no abnormal thermal behavior;
- no uncontrolled restart loop.

## Evidence

Record:
- APK version and SHA-256;
- Android version;
- start/end battery;
- Android thermal status when available;
- manual device feel;
- all probe timestamps;
- inference latency;
- any HyperOS battery/background warning;
- whether notification remained visible.

## Important

N6 is the parity gate.

Only after this PASS may Termux be considered optional for normal ORBI Edge Node operation. It remains valuable as a diagnostic/reference environment.
