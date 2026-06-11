#!/bin/bash
# PostToolUse hook — remind to regenerate when source files change
# Matched: Edit|Write on any file

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null || echo "")

# Source files that require site regeneration
case "$FILE_PATH" in
  *articles.json|*gen_cn_site.py|*gen_en_site.py|*gen_ai_friendly.py)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Source file changed: $(basename "$FILE_PATH")"
    echo ""
    echo "Regenerate the site with:"
    echo "  PYTHONPATH=. python3 scripts/gen_cn_site.py"
    echo "  PYTHONPATH=. python3 scripts/gen_ai_friendly.py"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;
  *md/zh/*.md|*md/en/*.md)
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Markdown source changed: $(basename "$FILE_PATH")"
    echo "Run site generators to update the HTML."
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ;;
esac

exit 0
