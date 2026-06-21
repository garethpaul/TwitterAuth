#!/usr/bin/env sh
set -eu
PATH=/usr/bin:/bin
export PATH
ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && /bin/pwd -P)
TEMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/twitterauth-make-authority-XXXXXX")
trap 'rm -rf "$TEMP_ROOT"' EXIT HUP INT TERM
unset MAKEFILES MAKEFILE_LIST MAKEFLAGS MFLAGS MAKEOVERRIDES PYTHON ROOT SHELL UNITY
CONTROL_DIR="$TEMP_ROOT/control"; CHECKOUT="$TEMP_ROOT/twitterauth app's [gate] \"quoted\" \`touch TWITTERAUTH_ROOT_MARKER\`"; ATTACKER_ROOT="$TEMP_ROOT/attacker"; AUTHORITY_PATH="$TEMP_ROOT/no-platform-tools"; LOG="$TEMP_ROOT/commands.log"; SHELL_LOG="$TEMP_ROOT/shell.log"
mkdir -p "$CONTROL_DIR" "$CHECKOUT/scripts" "$ATTACKER_ROOT" "$AUTHORITY_PATH"; CONTROL_DIR=$(CDPATH= cd -- "$CONTROL_DIR" && /bin/pwd -P); CHECKOUT=$(CDPATH= cd -- "$CHECKOUT" && /bin/pwd -P); MAKEFILE="$CHECKOUT/Makefile"; cp "$ROOT_DIR/Makefile" "$MAKEFILE"
FAKE_PYTHON="$TEMP_ROOT/trusted python's \"quoted\" \`touch TWITTERAUTH_PYTHON_MARKER\` \$literal"; cat >"$FAKE_PYTHON" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$TWITTERAUTH_COMMAND_LOG"
EOF
chmod +x "$FAKE_PYTHON"
for script in test-makefile-root.sh check_unity_contracts.py test_generated_cache_contract.py test_oauth_callback_preflight_contract.py test_oauth_hardening_contract.py; do cp "$FAKE_PYTHON" "$CHECKOUT/scripts/$script"; done
cp "$ROOT_DIR/scripts/run-python.sh" "$CHECKOUT/scripts/run-python.sh"; chmod +x "$CHECKOUT/scripts/run-python.sh"
FAKE_UNITY="$TEMP_ROOT/trusted unity"; cat >"$FAKE_UNITY" <<'EOF'
#!/bin/sh
printf '%s|%s|%s\n' "$PWD" "$0" "$*" >> "$TWITTERAUTH_COMMAND_LOG"
EOF
chmod +x "$FAKE_UNITY"
FAKE_SHELL="$TEMP_ROOT/fake-shell"; printf '#!/bin/sh\nprintf invoked >> %s\nexec /bin/sh "$@"\n' "'$SHELL_LOG'" >"$FAKE_SHELL"; chmod +x "$FAKE_SHELL"
run_case() { target=$1; mode=$2; rm -f "$LOG" "$SHELL_LOG"; set +e; case "$mode" in default) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" "$target") >/dev/null 2>&1;; command-root) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" ROOT="$ATTACKER_ROOT" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" "$target") >/dev/null 2>&1;; environment-root) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" ROOT="$ATTACKER_ROOT" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" "$target") >/dev/null 2>&1;; command-shell) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" SHELL="$FAKE_SHELL" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" "$target") >/dev/null 2>&1;; environment-shell) (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" SHELL="$FAKE_SHELL" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" "$target") >/dev/null 2>&1;; esac; status=$?; set -e; [ "$status" -eq 0 ]; [ ! -e "$SHELL_LOG" ]; grep -Fq "$CHECKOUT" "$LOG"; }
executed=0; for target in build check lint root-test test verify; do for mode in default command-root environment-root command-shell environment-shell; do run_case "$target" "$mode"; executed=$((executed+1)); done; done; [ "$executed" -eq 30 ]
rm -f "$LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY" check) >/dev/null 2>&1; grep -Fq "$FAKE_PYTHON" "$LOG"; grep -Fq "$FAKE_UNITY" "$LOG"; [ ! -e "$CONTROL_DIR/TWITTERAUTH_ROOT_MARKER" ]; [ ! -e "$CONTROL_DIR/TWITTERAUTH_PYTHON_MARKER" ]
MARK="$TEMP_ROOT/python-syntax"; BAD="\$(shell /usr/bin/touch '$MARK')"; if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" "PYTHON=$BAD" lint) >"$TEMP_ROOT/python.out" 2>&1; then exit 1; fi; [ ! -e "$MARK" ]
ENV_MARK="$TEMP_ROOT/python-environment-syntax"; ENV_BAD="\$(shell /usr/bin/touch '$ENV_MARK')"; if (cd "$CONTROL_DIR"&&PYTHON="$ENV_BAD" /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" lint) >"$TEMP_ROOT/python-environment.out" 2>&1; then exit 1; fi; [ ! -e "$ENV_MARK" ]
if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFILE_LIST=/tmp/untrusted check) >"$TEMP_ROOT/list" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILE_LIST must not be overridden' "$TEMP_ROOT/list"
if (cd "$CONTROL_DIR"&&MAKEFILE_LIST=/tmp/untrusted /usr/bin/make --environment-overrides --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/list-environment" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILE_LIST must not be overridden' "$TEMP_ROOT/list-environment"
PRE="$TEMP_ROOT/pre.mk"; PRE_MARKER="$TEMP_ROOT/pre-ran"; printf '%s\n' "\$(shell /usr/bin/touch '$PRE_MARKER')" >"$PRE"; if (cd "$CONTROL_DIR"&&MAKEFILES="$PRE" /usr/bin/make --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/pre" 2>&1; then exit 1; fi; grep -Fq 'MAKEFILES must be empty' "$TEMP_ROOT/pre"; [ -e "$PRE_MARKER" ]
EARLY="$TEMP_ROOT/early.mk"; EARLY_MARKER="$TEMP_ROOT/early-ran"; printf '%s\n' "\$(shell /usr/bin/touch '$EARLY_MARKER')" >"$EARLY"; if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$EARLY" -f "$MAKEFILE" check) >"$TEMP_ROOT/early" 2>&1; then exit 1; fi; [ -s "$TEMP_ROOT/early" ]; [ -e "$EARLY_MARKER" ]
LATER="$TEMP_ROOT/later.mk"; LATER_MARKER="$TEMP_ROOT/later-ran"; cat >"$LATER" <<'EOF'
build check lint root-test test verify: MAKEFILE_LIST := Makefile
build check lint root-test test verify:
	@/usr/bin/touch "$$TWITTERAUTH_LATER_MARKER"
EOF
for target in build check lint root-test test verify; do rm -f "$LATER_MARKER"; if (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_LATER_MARKER="$LATER_MARKER" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER" "$target" "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY") >"$TEMP_ROOT/later-$target" 2>&1; then exit 1; fi; grep -Fq 'has both : and :: entries' "$TEMP_ROOT/later-$target"; [ ! -e "$LATER_MARKER" ]; done
mkdir -p "$ATTACKER_ROOT/scripts"
for script in test-makefile-root.sh check_unity_contracts.py test_generated_cache_contract.py test_oauth_callback_preflight_contract.py test_oauth_hardening_contract.py; do cp "$FAKE_PYTHON" "$ATTACKER_ROOT/scripts/$script"; done
TARGET_PYTHON="$TEMP_ROOT/target-python"; TARGET_UNITY="$TEMP_ROOT/target-unity"; cp "$FAKE_PYTHON" "$TARGET_PYTHON"; cp "$FAKE_UNITY" "$TARGET_UNITY"
LATER_VARS="$TEMP_ROOT/later-vars.mk"; cat >"$LATER_VARS" <<EOF
build check lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check lint root-test test verify: ROOT := $ATTACKER_ROOT
build check lint root-test test verify: PYTHON := $TARGET_PYTHON
build check lint root-test test verify: UNITY := $TARGET_UNITY
EOF
rm -f "$LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" PYTHON="$FAKE_PYTHON" UNITY="$FAKE_UNITY" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_VARS" check) >"$TEMP_ROOT/later-vars" 2>&1; grep -Fq "$CHECKOUT" "$LOG"; grep -Fq "$FAKE_PYTHON" "$LOG"; grep -Fq "$FAKE_UNITY" "$LOG"; if grep -Fq "$ATTACKER_ROOT" "$LOG" || grep -Fq "$TARGET_PYTHON" "$LOG" || grep -Fq "$TARGET_UNITY" "$LOG"; then exit 1; fi
LATER_OVERRIDE_VARS="$TEMP_ROOT/later-override-vars.mk"; cat >"$LATER_OVERRIDE_VARS" <<EOF
build check lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check lint root-test test verify: override ROOT := $ATTACKER_ROOT
build check lint root-test test verify: override PYTHON := $TARGET_PYTHON
build check lint root-test test verify: override UNITY := $TARGET_UNITY
EOF
rm -f "$LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" PYTHON="$FAKE_PYTHON" UNITY="$FAKE_UNITY" TWITTERAUTH_COMMAND_LOG="$LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_OVERRIDE_VARS" check) >"$TEMP_ROOT/later-override-vars" 2>&1; grep -Fq "$CHECKOUT" "$LOG"; grep -Fq "$FAKE_PYTHON" "$LOG"; grep -Fq "$FAKE_UNITY" "$LOG"; if grep -Fq "$ATTACKER_ROOT" "$LOG" || grep -Fq "$TARGET_PYTHON" "$LOG" || grep -Fq "$TARGET_UNITY" "$LOG"; then exit 1; fi
LATER_SHELL="$TEMP_ROOT/later-shell.mk"; LATER_SHELL_LOG="$TEMP_ROOT/later-shell.log"; LATER_FAKE_SHELL="$TEMP_ROOT/later-fake-shell"; cat >"$LATER_FAKE_SHELL" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$TWITTERAUTH_LATER_SHELL_LOG"
printf '%s\n' ok
exit 0
EOF
chmod +x "$LATER_FAKE_SHELL"
cat >"$LATER_SHELL" <<EOF
build check lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check lint root-test test verify: SHELL := $LATER_FAKE_SHELL
build check lint root-test test verify: .SHELLFLAGS := -c
EOF
rm -f "$LOG" "$LATER_SHELL_LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_COMMAND_LOG="$LOG" TWITTERAUTH_LATER_SHELL_LOG="$LATER_SHELL_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_SHELL" check "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY") >"$TEMP_ROOT/later-shell" 2>&1; grep -Fq "$CHECKOUT" "$LOG"; [ ! -e "$LATER_SHELL_LOG" ]
LATER_OVERRIDE="$TEMP_ROOT/later-override.mk"; cat >"$LATER_OVERRIDE" <<EOF
build check lint root-test test verify: MAKEFILE_LIST := $MAKEFILE
build check lint root-test test verify: override SHELL := $LATER_FAKE_SHELL
build check lint root-test test verify: override .SHELLFLAGS := -c
EOF
rm -f "$LATER_SHELL_LOG"; (cd "$CONTROL_DIR"&&PATH="$AUTHORITY_PATH" TWITTERAUTH_LATER_SHELL_LOG="$LATER_SHELL_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" -f "$LATER_OVERRIDE" check "PYTHON=$FAKE_PYTHON" "UNITY=$FAKE_UNITY") >"$TEMP_ROOT/later-override" 2>&1; [ -s "$LATER_SHELL_LOG" ]
PATH_PYTHON="$TEMP_ROOT/python3"; PATH_UNITY="$TEMP_ROOT/unity"; PATH_LOG="$TEMP_ROOT/path.log"; cp "$FAKE_PYTHON" "$PATH_PYTHON"; cp "$FAKE_UNITY" "$PATH_UNITY"; rm -f "$PATH_LOG"; if (cd "$CONTROL_DIR"&&PATH="$TEMP_ROOT:/usr/bin:/bin" TWITTERAUTH_COMMAND_LOG="$PATH_LOG" /usr/bin/make --no-print-directory -f "$MAKEFILE" lint) >"$TEMP_ROOT/path-tools" 2>&1; then exit 1; fi; [ ! -e "$PATH_LOG" ]
SITE_DIR="$TEMP_ROOT/site"; SITE_MARKER="$TEMP_ROOT/sitecustomize-ran"; mkdir -p "$SITE_DIR"; printf '%s\n' "import os; open('$SITE_MARKER', 'w').close(); os._exit(0)" >"$SITE_DIR/sitecustomize.py"; (cd "$ROOT_DIR"&&PYTHONPATH="$SITE_DIR" /usr/bin/make --no-print-directory lint PYTHON=/usr/bin/python3) >"$TEMP_ROOT/sitecustomize" 2>&1; [ ! -e "$SITE_MARKER" ]
if (cd "$CONTROL_DIR"&&/usr/bin/make --no-print-directory -f "$MAKEFILE" MAKEFLAGS=-n check) >"$TEMP_ROOT/flags" 2>&1; then exit 1; fi; grep -Fq 'MAKEFLAGS must not be overridden' "$TEMP_ROOT/flags"
for flag in -n --just-print --dry-run --recon -t --touch -q --question -i --ignore-errors; do if (cd "$CONTROL_DIR"&&/usr/bin/make "$flag" --no-print-directory -f "$MAKEFILE" check) >"$TEMP_ROOT/flag" 2>&1; then exit 1; fi; grep -Fq 'non-executing or error-ignoring MAKEFLAGS are not supported' "$TEMP_ROOT/flag"; done
printf '%s\n' 'Make authority tests passed: 30 target/authority cases, 6 later recipe-replacement rejections, later root/Python/Unity and non-override shell protection, override/startup boundary controls, PATH tool rejection, isolated Python startup, 2 raw Make-syntax rejections, 2 MAKEFILE_LIST rejections, caller MAKEFLAGS rejection, and 10 mode rejections'
