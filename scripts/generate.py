#!/usr/bin/env python3
"""AI HOT Daily Report Generator - fetches data from aihot.virxact.com and generates static HTML."""

import json
import os
import shutil
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

API_BASE = "https://aihot.virxact.com/api/public"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": UA}
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
ARCHIVE_KEEP_DAYS = 90


def fetch_daily(date_str=None):
    """Fetch daily report from API. Returns dict or None."""
    url = f"{API_BASE}/daily"
    if date_str:
        url = f"{API_BASE}/daily/{date_str}"
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(5)
    return None


def render_template(env, template_name, **kwargs):
    """Render a Jinja2 template."""
    template = env.get_template(template_name)
    return template.render(**kwargs)


def write_file(path, content):
    """Write content to file, creating dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  Written: {path}")


def cleanup_old_archives(archive_dir, keep_days=ARCHIVE_KEEP_DAYS):
    """Remove archive files older than keep_days."""
    if not archive_dir.exists():
        return
    cutoff = datetime.now(timezone.utc) - timedelta(days=keep_days)
    for f in archive_dir.glob("*.html"):
        try:
            date_str = f.stem  # "2026-05-10"
            file_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if file_date < cutoff:
                f.unlink()
                print(f"  Cleaned up old archive: {f.name}")
        except ValueError:
            pass


def main():
    print("=== AI HOT Daily Report Generator ===")

    # Ensure output dir exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    archive_dir = OUTPUT_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Copy static files
    if STATIC_DIR.exists():
        for f in STATIC_DIR.iterdir():
            if f.is_file():
                shutil.copy2(f, OUTPUT_DIR / f.name)
                print(f"  Copied static: {f.name}")

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), autoescape=True)

    # Fetch latest daily
    print("Fetching latest daily report...")
    data = fetch_daily()
    if not data:
        print("ERROR: Could not fetch daily report")
        sys.exit(1)

    date_str = data.get("date", "unknown")
    print(f"Got report for {date_str}")

    # Get archive list for sidebar
    print("Fetching archive list...")
    # For archive dates, we generate from existing files
    archive_dates = []
    if archive_dir.exists():
        for f in sorted(archive_dir.glob("*.html"), reverse=True):
            archive_dates.append(f.stem)

    # Render daily page
    html = render_template(env, "daily.html", report=data, archive_dates=archive_dates, is_index=True)

    # Write index.html
    write_file(OUTPUT_DIR / "index.html", html)

    # Write archive page
    write_file(archive_dir / f"{date_str}.html", html)

    # Add to archive list if not already there
    if date_str not in archive_dates:
        archive_dates.insert(0, date_str)

    # Re-render index with updated archive list
    html = render_template(env, "daily.html", report=data, archive_dates=archive_dates, is_index=True)
    write_file(OUTPUT_DIR / "index.html", html)

    # Cleanup old archives
    cleanup_old_archives(archive_dir)

    print(f"=== Done! Report for {date_str} generated. ===")


if __name__ == "__main__":
    main()
