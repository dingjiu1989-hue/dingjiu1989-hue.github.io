"""
Syndication risk control config.
All syndication scripts should import from here for consistent pacing.
"""
import json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Per-run limits ──────────────────────────────────────
ARTICLES_PER_RUN = 3          # Max articles per script execution
SLEEP_BETWEEN_ARTICLES = 120  # Seconds between posts (natural pacing)

# ── Daily global cap (across all platforms) ─────────────
DAILY_MAX = 30                # Total articles per day across all platforms
LOG_PATH = ROOT / "data" / "syndication-log.json"

def get_daily_count():
    """Return how many articles published today across all platforms."""
    today = time.strftime("%Y-%m-%d")
    try:
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
        return log.get("days", {}).get(today, {}).get("total", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def record_published(platform, count, success=True):
    """Record an article publication to the daily log."""
    today = time.strftime("%Y-%m-%d")
    now = time.strftime("%H:%M:%S")
    try:
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        log = {"days": {}}
    day = log["days"].setdefault(today, {"total": 0, "platforms": {}, "events": []})
    day["total"] += count
    day["platforms"].setdefault(platform, 0)
    day["platforms"][platform] += count
    day["events"].append({"t": now, "platform": platform, "count": count, "ok": success})
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
