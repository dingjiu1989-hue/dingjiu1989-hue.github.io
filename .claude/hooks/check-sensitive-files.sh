#!/bin/bash
# UserPromptSubmit hook — detect risky requests involving sensitive files
# Runs before every user prompt to flag potential security issues

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt',''))" 2>/dev/null || echo "")

# Check if user prompt mentions pushing or committing sensitive info
if echo "$PROMPT" | grep -qiE '(push|commit|deploy).*(key|secret|token|password|credential)'; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Security reminder: this prompt mentions push/deploy + sensitive info."
  echo "Make sure no API keys, tokens, or credentials are exposed."
  echo "Refer to CLAUDE.md: scan before every push."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

exit 0
