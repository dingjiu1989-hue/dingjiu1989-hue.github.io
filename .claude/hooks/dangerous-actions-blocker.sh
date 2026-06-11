#!/bin/bash
# PreToolUse hook — block/warn on dangerous shell commands
# Matched: Bash tool calls only

INPUT=$(cat)
COMMAND="$INPUT"

# Pattern matching for destructive commands
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# BLOCK: rm -rf on project root or home
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+(/(\*|$)|~/(\*|$)|.*/gh-pages-demo(\*|$))'; then
  echo -e "${RED}━━━ BLOCKED ━━━${NC}"
  echo "Command matches destructive pattern: rm -rf on critical path"
  echo ""
  echo "If you really need to delete this, reply with:"
  echo "  \"I approve the rm -rf — <reason>\""
  exit 1
fi

# BLOCK: git push --force to main
if echo "$COMMAND" | grep -qE 'git\s+push\s+.*(--force|-f).*\b(main|master)\b'; then
  echo -e "${RED}━━━ BLOCKED ━━━${NC}"
  echo "Force push to main/master is blocked."
  echo "Use a feature branch instead, or reply with explicit approval."
  exit 1
fi

# WARN: git reset --hard
if echo "$COMMAND" | grep -qE 'git\s+reset\s+--hard'; then
  echo -e "${YELLOW}━━━ WARNING ━━━${NC}"
  echo "git reset --hard will discard uncommitted changes."
  echo "Uncommitted work will be lost. Proceed with caution."
  echo ""
fi

# WARN: deleting more than 10 files
if echo "$COMMAND" | grep -qE 'rm\s+-rf\s+\S+'; then
  FILE_COUNT=$(echo "$COMMAND" | grep -oE 'rm\s+-rf\s+\S+' | wc -l)
  echo -e "${YELLOW}━━━ WARNING ━━━${NC}"
  echo "This will delete files/directories. Double-check the paths."
  echo ""
fi

exit 0
