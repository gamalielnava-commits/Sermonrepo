"""
Pure helpers for mapping a user-facing quality choice (best / 4k / 2k /
1080p / 720p / 480p) to the yt-dlp format selector string and the
ffmpeg CRF used on the clip cut.

Kept in its own module so tests can import it without pulling the whole
ML / video-processing stack (cv2, mediapipe, torch, yolo, etc.) that
main.py imports at module load.
"""


def quality_to_ydl_format(quality):
    """Map UI quality choice to a yt-dlp format selector.

    Note: YouTube only serves H.264 up to 1080p. 1440p/2160p are VP9/AV1
    only, so for "best" / "4k" / "2k" we must NOT force avc1 or even
    `ext=mp4`, or the download silently caps at 1080p (or falls back to
    a much lower resolution). The download container is merged as mkv;
    the clip cut step re-encodes to H.264/MP4 anyway, so final clips
    are always standard MP4.
    """
    q = (quality or "best").lower()
    if q in ("best", "max", "4k", "2160p"):
        # Any container, any codec. yt-dlp picks highest resolution
        # (honours format_sort on the YoutubeDL instance).
        return 'bestvideo+bestaudio/best'
    if q in ("2k", "1440p"):
        return 'bestvideo[height<=1440]+bestaudio/best[height<=1440]/best'
    if q == "1080p":
        # Prefer H.264/mp4 when available (YouTube offers it up to 1080p
        # and it avoids a re-encode during merge), fall back to anything.
        return ('bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best')
    if q == "720p":
        return ('bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height<=720]+bestaudio/best[height<=720]/best')
    if q == "480p":
        return ('bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height<=480]+bestaudio/best[height<=480]/best')
    return 'bestvideo+bestaudio/best'


def quality_to_crf(quality):
    """Map UI quality choice to an ffmpeg CRF value (lower = higher quality)."""
    q = (quality or "best").lower()
    return {
        "best": 15, "4k": 15, "2160p": 15,
        "2k": 16, "1440p": 16,
        "1080p": 18,
        "720p": 20,
        "480p": 23,
    }.get(q, 18)


# Ordered list of format_sort keys we pass to YoutubeDL so the format
# selector always prefers the highest resolution first, falling back to
# H.264/mp4 only as a tiebreaker.
FORMAT_SORT = ['res', 'fps', 'vcodec:h264', 'ext:mp4:m4a']

# yt-dlp player_client order: the `web` / `web_safari` clients are the
# only ones that expose >1080p streams; if `tv_embed` / `android` are
# listed first yt-dlp can silently settle on 1080p.
YOUTUBE_PLAYER_CLIENTS = ['web', 'web_safari', 'tv_embed', 'android', 'mweb']
