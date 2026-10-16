"""Offline regression checks for the latest-news publication window."""

import importlib.util
from pathlib import Path
import re
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


class FeedRegistryTests(unittest.TestCase):
    active_urls = [
        "https://www.qbitai.com/feed",
        "https://36kr.com/feed",
        "https://www.zhidx.com/feed",
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
    ]

    def test_registry_preserves_other_five_sources(self):
        self.assertEqual([feed["url"] for feed in updater.RSS_FEEDS], self.active_urls)

    def test_fetch_queries_active_sources_not_retired_html_page(self):
        with patch.object(updater.feedparser, "parse", return_value=SimpleNamespace(entries=[])) as parse:
            self.assertEqual(updater.fetch_news(now=NewsFreshnessTests.now), [])
        self.assertEqual([call.args[0] for call in parse.call_args_list], self.active_urls)

    def test_template_and_homepage_source_counts_match_registry(self):
        root = Path(__file__).parents[1]
        pattern = r'<div class="hero-stat-num">(\d+)</div>\s*<div class="hero-stat-label">RSS信源</div>'
        for name in ("index_template.html", "index.html"):
            with self.subTest(file=name):
                matches = re.findall(pattern, (root / name).read_text(encoding="utf-8"))
                self.assertEqual(matches, [str(len(updater.RSS_FEEDS))])


if __name__ == "__main__":
    unittest.main()
