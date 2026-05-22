---
title: "Bash Scripting Best Practices"
description: "Essential patterns for writing reliable, maintainable shell scripts in production environments."
date: 2025-12-01
board: tech
url: https://aidev.fit/en/tech/bash-scripting-guide.html
---

# Bash Scripting Best Practices

Bash scripting remains one of the most critical skills for developers, DevOps engineers, and system administrators. Despite its age, Bash is everywhere -- from CI/CD pipelines to deployment scripts and system automation. Writing robust, maintainable shell scripts requires discipline and adherence to proven practices.

## Start with Strict Mode

Every production Bash script should begin with strict mode settings that catch errors early:

## !/usr/bin/env bash

set -euo pipefail

IFS=$'\n\t'

  * `set -e` causes the script to exit immediately when a command fails.

  * `set -u` treats unset variables as an error.

  * `set -o pipefail` makes pipeline failures propagate.

  * Setting `IFS` to newline and tab prevents word-splitting issues with filenames containing spaces.




A more advanced option is `set -o errexit` combined with custom error handling:

error_handler() {

local line=$1

echo "Error on line $line" >&2

exit 1

}

trap 'error_handler $LINENO' ERR

## Use Functions for Modularity

Avoid writing long linear scripts. Break logic into functions with clear names:

validate_input() { ... }

process_file() { ... }

send_notification() { ... }

Declare all functions at the top of the script, followed by argument parsing, followed by the main execution flow. This makes the script readable and testable.

## Prefer `[[ ]]` Over `[ ]`

The double-bracket `[[ ]]` construct is a Bash keyword with fewer surprises:

if [[ -f "$file" && "$name" == "prod" ]]; then

echo "Matched"

fi

Unlike single brackets, double brackets handle empty variables safely, support pattern matching, and avoid word-splitting.

## Quote Everything

Unquoted variables are one of the most common sources of bugs:

## Wrong

if [ -f $file ]; then # breaks if file has spaces

## Right

if [[ -f "$file" ]]; then

Quote all variable expansions: `"$var"`, `"${array[@]}"`, and command substitutions `"$(command)"`.

## Use `trap` for Cleanup

Always clean up temporary files and resources:

cleanup() {

rm -rf "$TEMP_DIR"

kill "$PID" 2>/dev/null || true

}

trap cleanup EXIT

The `EXIT` trap fires regardless of why the script exits -- success, failure, or signal. For signal-specific handling, add separate traps for `INT` and `TERM`.

## Argument Parsing with `getopts`

Use `getopts` for reliable argument parsing instead of manual position checks:

usage() { echo "Usage: $0 -f file -o output [-v]" >&2; exit 1; }

while getopts ":f:o:v" opt; do

case $opt in

f) INPUT_FILE="$OPTARG" ;;

o) OUTPUT_DIR="$OPTARG" ;;

v) VERBOSE=true ;;

*) usage ;;

esac

done

This handles short flags robustly, including missing argument errors.

## Use `readonly` and `declare -r`

Mark constants and configuration values as readonly:

readonly MAX_RETRIES=3

readonly CONFIG_PATH="/etc/myapp/config.yml"

This prevents accidental overwrites and documents intent.

## Prefer `printf` Over `echo`

The `echo` command behaves differently across shells and platforms. Use `printf` for portable, predictable output:

printf "Processing file: %s\n" "$filename"

## Logging with Timestamps

Implement a simple logging function for better observability:

log() {

local level="$1"

shift

printf "[%s] [%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$*" >&2

}

info() { log "INFO" "$@"; }

error() { log "ERROR" "$@"; }

Send logs to stderr so they don't interfere with stdout data output.

## Validating Dependencies

Check required commands before proceeding:

require() {

for cmd in "$@"; do

if ! command -v "$cmd" &>/dev/null; then

error "Required command not found: $cmd"

exit 1

fi

done

}

require jq curl openssl

## Avoid `eval` and Backtick Substitution

Never use `eval` unless absolutely necessary -- it is a security risk. Use `$()` instead of backticks for command substitution; `$()` nests cleanly and is visually distinct.

## Use Arrays for Lists

Modern Bash supports arrays, which handle spaces correctly:

files=()

while IFS= read -r -d '' file; do

files+=("$file")

done < <(find /var/log -name "*.log" -print0)

for file in "${files[@]}"; do

process_file "$file"

done

The `-print0` / `read -d ''` pattern handles filenames with any special characters.

## ShellCheck Integration

Run [ShellCheck](<https://www.shellcheck.net/>) as part of your CI pipeline. It catches hundreds of common pitfalls and enforces consistency. Integrate it with VS Code via the shellcheck extension for real-time feedback during editing.

## Testing Bash Scripts

Use `bats` (Bash Automated Testing System) for unit testing:

@test "validate_input rejects empty string" {

run validate_input ""

[[ "$status" -ne 0 ]]

}

Test your error handlers, edge cases with spaces, and exit codes.

## Summary

Bash scripting is not dead -- it is the glue that holds modern infrastructure together. By following these practices, you will write scripts that are robust, maintainable, and production-ready. Strict mode, proper quoting, function decomposition, traps, and ShellCheck validation will prevent the majority of common issues before they reach production.

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Microservices Communication Patterns](</en/tech/microservices-communication.html>).

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>)

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>)

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>)

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>)

**See also:** [Kubernetes Security Best Practices](</en/tech/kubernetes-services-security.html>), [Terraform Infrastructure as Code](</en/tech/terraform-infrastructure-code.html>), [Advanced GitHub Actions Workflows](</en/tech/github-actions-advanced.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)

**See also:** [Infrastructure Testing with Terratest and Other Tools](</en/tech/infrastructure-testing.html>), [Serverless Framework: From Zero to Production](</en/tech/serverless-framework.html>), [Service Discovery in Microservices](</en/tech/service-discovery.html>)
