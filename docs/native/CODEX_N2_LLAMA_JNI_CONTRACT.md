# Codex Contract — N2 llama.cpp JNI

Status: PREPARED — DO NOT IMPLEMENT UNTIL N1 PASS

## Goal

Integrate a pinned llama.cpp revision into the Android app as an arm64 native dependency.

## Dependency policy

- pin an exact upstream revision;
- record upstream license and revision;
- keep third-party source separable from ORBI-owned JNI glue;
- never silently track upstream HEAD in a reproducible build.

## JNI policy

Kotlin must not mirror the complete llama.cpp C API.

N2 exposes only a minimal ORBI-owned bridge sufficient to prove:
- library load;
- runtime version/build query;
- initialization/teardown boundary.

Model loading belongs to N3.
Inference belongs to N4.

## Ownership

Kotlin:
- Android lifecycle
- state machine
- error presentation
- orchestration

C++:
- llama backend initialization
- llama resource ownership
- deterministic cleanup
- native error translation

## Acceptance

- arm64 build PASS;
- app launch PASS;
- llama runtime metadata visible;
- create/destroy smoke cycle PASS;
- no model required;
- no Termux dependency;
- no network dependency at runtime.

## Failure rule

Any native exception/error path must be translated into a bounded result visible to Kotlin; do not allow ordinary initialization failures to terminate the process.
