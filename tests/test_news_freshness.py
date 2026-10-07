"""Offline regression checks for the latest-news publication window."""

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime


with patch.dict(sys.modules, {"feedparser": SimpleNamespace(parse=None)}):
    spec = importlib.util.spec_from_file_location(
        "news_updater", Path(__file__).parents[1] / "scripts" / "update_news_v2.py"
    )
    updater = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(updater)


class NewsFreshnessTests(unittest.TestCase):
    now = datetime(2026, 10, 7, 1, 0, tzinfo=timezone.utc)

    def entry(self, title, date):
        return {"title": title, "published": date, "link": "https://example.org/news"}

    def fetch(self, entries):
        with patch.object(updater, "RSS_FEEDS", [{"url": "fixture", "category": "行业动态", "priority": 1}]), patch.object(
            updater.feedparser, "parse", return_value=SimpleNamespace(entries=entries)
        ):
            return updater.fetch_news(now=self.now)

    def test_missing_and_invalid_dates_are_unknown(self):
        for value in (None, "", "invalid date"):
            self.assertIsNone(updater.parse_date(value))

    def test_naive_source_date_is_normalized_to_utc(self):
        self.assertEqual(updater.parse_date("07 Oct 2026 01:00:00"), self.now)

    def test_fresh_story_keeps_original_publication_time(self):
        published = self.now - timedelta(hours=2)
        news = self.fetch([self.entry("A genuinely recent AI headline", format_datetime(published))])
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]["date"], published)

    def test_seven_day_cutoff_includes_boundary_not_older(self):
        boundary = self.now - timedelta(days=7)
        news = self.fetch([
            self.entry("AI story exactly on boundary", format_datetime(boundary)),
            self.entry("AI story just outside window", format_datetime(boundary - timedelta(seconds=1))),
        ])
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]["date"], boundary)

    def test_future_and_undated_stories_are_not_latest_news(self):
        news = self.fetch([
            self.entry("An undated AI headline item", ""),
            self.entry("An invalid AI headline item", "invalid"),
            self.entry("A future AI headline item", format_datetime(self.now + timedelta(seconds=1))),
        ])
        self.assertEqual(news, [])

    def test_stale_duplicate_does_not_hide_recent_story(self):
        title = "An identical AI headline item"
        news = self.fetch([
            self.entry(title, format_datetime(self.now - timedelta(days=90))),
            self.entry(title, format_datetime(self.now - timedelta(hours=1))),
        ])
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]["date"], self.now - timedelta(hours=1))


if __name__ == "__main__":
    unittest.main()
