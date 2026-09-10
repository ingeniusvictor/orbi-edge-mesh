# ORBI Edge Mesh — Secure Node Pairing & Trust v0.1

## Goal

Prevent arbitrary devices on the same LAN from registering as trusted ORBI nodes or issuing control-plane commands.

## Threat model

A local network may contain other phones, TVs, IoT devices, guests or compromised devices.

Being on the same Wi-Fi must not imply trust.

## Pairing model

Phase 0 uses explicit local pairing. A node must be approved before privileged control actions are accepted.

No cloud account is required.

## Trust states

- unpaired
- trusted
- revoked

Revoked nodes must not receive privileged control actions.

## Request authenticity

Privileged control messages must carry verifiable authenticity and replay protection.

Phase 0 will use a local shared-secret approach with per-request authentication metadata.

## Scope

Phase 0 protects the ORBI control plane first. The inference plane may require separate protection depending on runtime exposure.

## Security rules

- same Wi-Fi does not imply trust
- pairing must be explicit
- revocation must be possible
- production secrets must never be committed to Git
- local trust state must remain local by default
- replayed privileged requests must be rejected
