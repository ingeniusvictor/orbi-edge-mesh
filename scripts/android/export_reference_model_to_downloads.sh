#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODEL="${HOME}/models/Qwen3-1.7B-Q4_K_M.gguf"
EXPECTED_SHA="d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5"
DOWNLOADS="${HOME}/storage/downloads"
DEST="${DOWNLOADS}/Qwen3-1.7B-Q4_K_M.gguf"

echo "=== ORBI Edge Node - Export Reference GGUF ==="

if [[ ! -f "${MODEL}" ]]; then
  echo "ERROR: reference model not found: ${MODEL}" >&2
  exit 1
fi

SOURCE_SHA="$(sha256sum "${MODEL}" | awk '{print $1}')"
if [[ "${SOURCE_SHA}" != "${EXPECTED_SHA}" ]]; then
  echo "ERROR: source model SHA-256 mismatch." >&2
  echo "Expected: ${EXPECTED_SHA}" >&2
  echo "Actual:   ${SOURCE_SHA}" >&2
  exit 1
fi

if [[ ! -d "${DOWNLOADS}" ]]; then
  echo "Shared storage is not prepared yet."
  echo "Run: termux-setup-storage"
  echo "Approve Android shared-storage access, then run this script again."
  exit 2
fi

FREE_KB="$(df -Pk "${DOWNLOADS}" | awk 'NR==2 {print $4}')"
MODEL_KB="$(du -Pk "${MODEL}" | awk '{print $1}')"

if [[ -n "${FREE_KB}" && -n "${MODEL_KB}" ]] && (( FREE_KB < MODEL_KB + 1048576 )); then
  echo "ERROR: not enough free shared storage with 1 GiB safety margin." >&2
  exit 1
fi

if [[ -f "${DEST}" ]]; then
  DEST_SHA="$(sha256sum "${DEST}" | awk '{print $1}')"
  if [[ "${DEST_SHA}" == "${EXPECTED_SHA}" ]]; then
    echo "PASS: valid Downloads copy already exists."
    echo "Path: ${DEST}"
    echo "SHA-256: ${DEST_SHA}"
    exit 0
  fi

  echo "Existing Downloads file has a different hash; replacing it."
  rm -f "${DEST}"
fi

TMP="${DEST}.part"
rm -f "${TMP}"

echo "Copying reference model to shared Downloads..."
cp "${MODEL}" "${TMP}"

DEST_SHA="$(sha256sum "${TMP}" | awk '{print $1}')"
if [[ "${DEST_SHA}" != "${EXPECTED_SHA}" ]]; then
  rm -f "${TMP}"
  echo "ERROR: copied file SHA-256 mismatch." >&2
  exit 1
fi

mv "${TMP}" "${DEST}"

echo "PASS: shared Android-picker copy ready."
echo "Path: ${DEST}"
echo "SHA-256: ${DEST_SHA}"
echo "The original Termux reference model was left untouched."
