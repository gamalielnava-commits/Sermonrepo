"""
Offline tests for the yt-dlp quality selectors.

These tests don't hit YouTube. They verify:
  1. The format-string helpers return sensible, well-formed values for
     each quality choice.
  2. A YouTubeDL instance built with our common opts + format selector
     picks the right format given a fabricated list of available
     formats (the same shape yt-dlp builds internally from a real
     extraction).

Run with:  python tests/test_quality_selectors.py
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quality import (
    quality_to_ydl_format,
    quality_to_crf,
    FORMAT_SORT,
)


# Fabricated list of formats that mirrors what YouTube returns for a
# video available in 2160p. Real yt-dlp extraction produces dicts with
# these keys; format_selector consumes them.
def _fmt(format_id, ext, vcodec, acodec, width=None, height=None, fps=None, tbr=None, abr=None):
    return {
        'format_id': format_id,
        'ext': ext,
        'vcodec': vcodec,
        'acodec': acodec,
        'width': width,
        'height': height,
        'fps': fps,
        'tbr': tbr,
        'abr': abr,
        'url': f'https://example.invalid/{format_id}',
        'protocol': 'https',
        'filesize': None,
    }


FAKE_YOUTUBE_FORMATS = [
    _fmt('160', 'mp4', 'avc1.42c00b', 'none', 256, 144, 24, 100),
    _fmt('133', 'mp4', 'avc1.4d4015', 'none', 426, 240, 24, 200),
    _fmt('134', 'mp4', 'avc1.4d401e', 'none', 640, 360, 24, 400),
    _fmt('135', 'mp4', 'avc1.4d401f', 'none', 854, 480, 24, 800),
    _fmt('136', 'mp4', 'avc1.4d401f', 'none', 1280, 720, 24, 1500),
    _fmt('137', 'mp4', 'avc1.640028', 'none', 1920, 1080, 24, 3000),
    # VP9 up to 4K (typical YouTube offering >1080p)
    _fmt('271', 'webm', 'vp9', 'none', 2560, 1440, 24, 6000),
    _fmt('313', 'webm', 'vp9', 'none', 3840, 2160, 24, 12000),
    # Audio-only
    _fmt('140', 'm4a', 'none', 'mp4a.40.2', abr=128),
    _fmt('251', 'webm', 'none', 'opus', abr=160),
]


def _pick(selector, sort=None):
    """Run yt-dlp's format selector over the fake formats and return the pick."""
    import yt_dlp

    opts = {'format': selector, 'quiet': True, 'no_warnings': True}
    if sort is not None:
        opts['format_sort'] = sort

    ydl = yt_dlp.YoutubeDL(opts)
    selector_fn = ydl.build_format_selector(selector)

    ctx = {'formats': list(FAKE_YOUTUBE_FORMATS), 'incomplete_formats': False}
    return list(selector_fn(ctx))


def _max_video_height(result):
    if result.get('requested_formats'):
        heights = [f.get('height') or 0 for f in result['requested_formats']
                   if f.get('vcodec') and f.get('vcodec') != 'none']
        return max(heights) if heights else 0
    return result.get('height') or 0


class QualityStringTests(unittest.TestCase):

    def test_best_does_not_force_mp4_or_avc1(self):
        sel = quality_to_ydl_format('best')
        self.assertNotIn('ext=mp4', sel)
        self.assertNotIn('avc1', sel)

    def test_4k_does_not_force_mp4_or_avc1(self):
        sel = quality_to_ydl_format('4k')
        self.assertNotIn('ext=mp4', sel)
        self.assertNotIn('avc1', sel)

    def test_2k_does_not_force_mp4(self):
        sel = quality_to_ydl_format('2k')
        self.assertNotIn('ext=mp4', sel)

    def test_1080p_still_prefers_mp4(self):
        sel = quality_to_ydl_format('1080p')
        self.assertIn('ext=mp4', sel)
        self.assertIn('height<=1080', sel)

    def test_720p_caps_height(self):
        self.assertIn('height<=720', quality_to_ydl_format('720p'))

    def test_480p_caps_height(self):
        self.assertIn('height<=480', quality_to_ydl_format('480p'))

    def test_crf_monotonic_by_quality(self):
        self.assertLess(quality_to_crf('best'), quality_to_crf('1080p'))
        self.assertLess(quality_to_crf('1080p'), quality_to_crf('720p'))
        self.assertLess(quality_to_crf('720p'), quality_to_crf('480p'))


class FormatSelectionTests(unittest.TestCase):
    """Run the real yt-dlp format selector against fabricated formats."""

    def test_best_picks_2160p(self):
        picked = _pick(quality_to_ydl_format('best'), sort=FORMAT_SORT)
        self.assertTrue(picked)
        h = _max_video_height(picked[-1])
        self.assertEqual(h, 2160, f"best should pick 2160p, got {h}")

    def test_4k_picks_2160p(self):
        picked = _pick(quality_to_ydl_format('4k'), sort=FORMAT_SORT)
        self.assertEqual(_max_video_height(picked[-1]), 2160)

    def test_2k_caps_at_1440p(self):
        picked = _pick(quality_to_ydl_format('2k'), sort=FORMAT_SORT)
        h = _max_video_height(picked[-1])
        self.assertLessEqual(h, 1440)
        self.assertGreaterEqual(h, 1080)

    def test_1080p_caps_at_1080p(self):
        picked = _pick(quality_to_ydl_format('1080p'), sort=FORMAT_SORT)
        h = _max_video_height(picked[-1])
        self.assertLessEqual(h, 1080)
        self.assertGreaterEqual(h, 720)

    def test_720p_caps_at_720p(self):
        picked = _pick(quality_to_ydl_format('720p'), sort=FORMAT_SORT)
        self.assertLessEqual(_max_video_height(picked[-1]), 720)

    def test_480p_caps_at_480p(self):
        picked = _pick(quality_to_ydl_format('480p'), sort=FORMAT_SORT)
        self.assertLessEqual(_max_video_height(picked[-1]), 480)


if __name__ == '__main__':
    unittest.main(verbosity=2)
