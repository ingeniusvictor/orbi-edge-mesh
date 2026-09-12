# N11 Zero-Config LAN Discovery

## Goal

Allow ORBI Edge Node to advertise itself on the local network so normal operation does not depend on a remembered IPv4 address.

## Android mechanism

N11 uses Android Network Service Discovery (NSD / DNS-SD).

Service type:

`_orbi-edge._tcp.`

The advertisement is tied to the ORBI local API lifecycle.

When the API starts, ORBI attempts to advertise:

- service name derived from the node ID;
- local API port;
- protocol version;
- node ID;
- app build version;
- authentication requirement.

No pairing secret or model content is advertised.

## Lifecycle

```text
ORBI local API starts
        ↓
NSD registration requested
        ↓
service advertised on LAN
        ↓
API stops
        ↓
NSD unregister requested
```

Discovery failure is non-fatal. The local API and inference runtime must remain usable through manual host configuration.

## Physical PASS

N11 is physically certified only after a second device or PC discovers the real Node-01 advertisement and resolves the usable local service endpoint.

Until then, the current known IPv4/manual configuration remains the fallback.
