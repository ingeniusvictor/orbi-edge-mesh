# ORBI Edge Mesh — Phase 0 Exit Checklist

## Software baseline

- [x] architecture documented
- [x] node capability contract
- [x] heartbeat / registry
- [x] fallback planning
- [x] thermal/power policy
- [x] model locality
- [x] request execution
- [x] observability
- [x] adaptive scheduling
- [x] workload profiles
- [x] headless requirement
- [x] bounded watchdog
- [x] policy-gated recovery
- [x] idle power-state model
- [x] model placement planning
- [x] explicit trust primitives
- [x] unified Phase 0 manager entrypoint

## Node-01 real hardware

- [ ] Android/HyperOS version recorded
- [ ] physical RAM confirmed
- [ ] storage free space recorded
- [ ] memory extension state recorded
- [ ] Termux baseline captured
- [ ] llama.cpp exact commit recorded
- [ ] llama.cpp build passes
- [ ] first GGUF model recorded
- [ ] CLI inference passes offline
- [ ] llama-server starts
- [ ] PC LAN request passes
- [ ] screen-off 30-minute test passes
- [ ] post-20-minute inference passes
- [ ] battery delta recorded
- [ ] thermal sensors identified
- [ ] watchdog recovery passes
- [ ] observability event captured

## Merge gate

Draft PR #1 remains DRAFT until the real Node-01 evidence above is materially complete.
