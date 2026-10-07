#!/usr/bin/env bash
# Materialize addons from addons.manifest.yml by copying (never symlink).
#
# Standalone (Linux/Windows):
#   odoo/src/sync-addons.sh
#   Fills odoo/src/public-addons and odoo/src/gml-addons from the manifest.
#   enterprise, paid-addons, and private-addons are already real trees.
#
# Container / Docker:
#   odoo/src/sync-addons.sh --dest /odoo/addons
#   Copies manifest modules plus enterprise, paid-addons, and private-addons
#   into a single destination folder.
#
# Run after clone, submodule update, or manifest changes.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: sync-addons.sh [--dest DIR]

  (no args)   Copy manifest modules into public-addons/ and gml-addons/
  --dest DIR  Copy manifest modules plus enterprise, paid-addons, and
              private-addons into DIR (flattened)

Paths in addons.manifest.yml are relative to odoo/src.
EOF
}

DEST=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --dest)
      if [[ $# -lt 2 ]]; then
        echo "error: --dest requires a directory argument" >&2
        exit 1
      fi
      DEST="$2"
      shift 2
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SRC_DIR}/addons.manifest.yml"
ALWAYS_TREES=(enterprise paid-addons private-addons)

if [[ ! -f "${MANIFEST}" ]]; then
  echo "error: manifest not found: ${MANIFEST}" >&2
  exit 1
fi

# Read a simple YAML mapping of list values:
#   farm:
#     - relative/path/to/module
yaml_list() {
  local farm="$1"
  local in_section=0
  local line key item
  while IFS= read -r line || [[ -n "${line}" ]]; do
    line="${line%$'\r'}"
    [[ "${line}" =~ ^[[:space:]]*# ]] && continue
    [[ "${line}" =~ ^[[:space:]]*$ ]] && continue
    if [[ "${line}" =~ ^([A-Za-z0-9_]+):[[:space:]]*$ ]]; then
      key="${BASH_REMATCH[1]}"
      if [[ "${key}" == "${farm}" ]]; then
        in_section=1
      else
        in_section=0
      fi
      continue
    fi
    if [[ "${in_section}" -eq 1 && "${line}" =~ ^[[:space:]]*-[[:space:]]+(.+)$ ]]; then
      item="${BASH_REMATCH[1]}"
      item="${item%\"}"
      item="${item#\"}"
      item="${item%\'}"
      item="${item#\'}"
      printf '%s\n' "${item}"
    fi
  done < "${MANIFEST}"
}

yaml_farms() {
  local line
  while IFS= read -r line || [[ -n "${line}" ]]; do
    line="${line%$'\r'}"
    [[ "${line}" =~ ^[[:space:]]*# ]] && continue
    if [[ "${line}" =~ ^([A-Za-z0-9_]+):[[:space:]]*$ ]]; then
      printf '%s\n' "${BASH_REMATCH[1]}"
    fi
  done < "${MANIFEST}"
}

is_addon_dir() {
  local path="$1"
  [[ -f "${path}/__manifest__.py" || -f "${path}/__openerp__.py" ]]
}

assert_not_git_checkout() {
  local path="$1"
  if [[ -e "${path}/.git" ]]; then
    echo "error: refusing to replace ${path} because it looks like a git checkout" >&2
    exit 1
  fi
}

copy_addon() {
  local src="$1"
  local dest="$2"
  if [[ ! -d "${src}" ]]; then
    echo "error: source not found: ${src}" >&2
    exit 1
  fi
  if ! is_addon_dir "${src}"; then
    echo "error: not an Odoo addon (missing __manifest__.py): ${src}" >&2
    exit 1
  fi
  rm -rf "${dest}"
  mkdir -p "$(dirname "${dest}")"
  cp -a "${src}" "${dest}"
  echo "  $(basename "${src}") <- ${src#"${SRC_DIR}"/}"
}

copy_tree_addons() {
  local from="$1"
  local to="$2"
  local child
  if [[ ! -d "${from}" ]]; then
    echo "warning: always-included tree missing, skipping: ${from}" >&2
    return 0
  fi
  echo "Copying $(basename "${from}") -> ${to}"
  shopt -s nullglob
  for child in "${from}"/*/; do
    child="${child%/}"
    if is_addon_dir "${child}"; then
      copy_addon "${child}" "${to}/$(basename "${child}")"
    fi
  done
  shopt -u nullglob
}

reset_farm() {
  local farm_dir="$1"
  assert_not_git_checkout "${farm_dir}"
  rm -rf "${farm_dir}"
  mkdir -p "${farm_dir}"
}

copy_farm_modules() {
  local farm="$1"
  local dest_dir="$2"
  local rel src name
  local count=0
  while IFS= read -r rel || [[ -n "${rel}" ]]; do
    [[ -z "${rel}" ]] && continue
    src="${SRC_DIR}/${rel}"
    name="$(basename "${rel}")"
    copy_addon "${src}" "${dest_dir}/${name}"
    count=$((count + 1))
  done < <(yaml_list "${farm}")
  if [[ "${count}" -eq 0 ]]; then
    echo "  (none)"
  fi
}

if [[ -n "${DEST}" ]]; then
  mkdir -p "${DEST}"
  echo "Syncing addons into ${DEST}"
  for farm in $(yaml_farms); do
    echo "Manifest farm: ${farm}"
    copy_farm_modules "${farm}" "${DEST}"
  done
  for tree in "${ALWAYS_TREES[@]}"; do
    copy_tree_addons "${SRC_DIR}/${tree}" "${DEST}"
  done
  echo "Done."
  exit 0
fi

echo "Syncing standalone addon farms under ${SRC_DIR}"
for farm in $(yaml_farms); do
  farm_dir="${SRC_DIR}/${farm}-addons"
  echo "Farm ${farm} -> ${farm_dir#"${SRC_DIR}"/}"
  reset_farm "${farm_dir}"
  copy_farm_modules "${farm}" "${farm_dir}"
done
echo "Done. Point addons_path at enterprise, paid-addons, private-addons,"
echo "public-addons, and gml-addons (plus odoo/odoo/addons)."
