"""
Configuration File for Auto-Reel Creator
Edit this file with your API keys before running
"""

# ========== API KEYS ==========
# Get these from:
# - ElevenLabs: elevenlabs.io (Creator plan, $22/month)
# - Pexels: pexels.com/api (FREE)

ELEVENLABS_API_KEY = "sk_your_elevenlabs_api_key_here"
PEXELS_API_KEY = "your_pexels_api_key_here"

# ========== VOICE SETTINGS ==========
# Voice selection per category
VOICES = {
    'True Crime': 'Marcus',  # Deep, authoritative
    'Historical': 'Rachel',  # Warm, engaging
    'Unexplained': 'Antoni',  # Mysterious
    'Survival': 'Marcus',
    'What If': 'Rachel',
    'Fascinating Person': 'Rachel'
}

# Voice settings (adjust for your preference)
VOICE_STABILITY = 0.75  # 0-1, higher = more consistent
VOICE_CLARITY = 0.75    # 0-1, higher = clearer
VOICE_STYLE = 0         # 0-1, 0 = neutral

# ========== BRAND COLORS ==========
COLORS = {
    'black': '#0A0A0A',
    'dark_blue': '#1A1A2E',
    'red': '#E94560',
    'gold': '#FFD700',
    'white': '#FFFFFF'
}

# ========== VIDEO SETTINGS ==========
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
VIDEO_BITRATE = '6000k'  # Higher = better quality
VIDEO_PRESET = 'medium'   # slow/medium/fast (slow = best quality)

# ========== FILE PATHS ==========
# Input: CSV with story data
STORIES_CSV = "templates/week_stories.csv"

# Output: Where to save created reels
OUTPUT_FOLDER = "exports"

# Temporary files (auto-deleted)
TEMP_FOLDER = "temp"

# ========== TEMPLATE SETTINGS ==========
# Which templates to use (leave all True for max variety)
TEMPLATES_ENABLED = {
    'cinematic_mystery': True,
    'case_file_documentary': True,
    'historical_timeline': True,
    'suspense_build': True,
    'revelation_style': True
}

# Text settings
HOOK_FONT_SIZE = 80  # Size of hook text
HOOK_DURATION = 5     # How long hook appears (seconds)

# ========== PEXELS SEARCH ==========
# Fallback search terms if story-specific not found
CATEGORY_FOOTAGE = {
    'True Crime': 'dark corridor crime scene investigation',
    'Historical': 'vintage historical sepia old documentary',
    'Unexplained': 'mysterious fog dark unknown paranormal',
    'Survival': 'ocean storm wilderness extreme nature',
    'What If': 'abstract space cosmic futuristic concept',
    'Fascinating Person': 'vintage portrait historical person sepia'
}

# ========== AUTOMATION SETTINGS ==========
# Delay between creating reels (to avoid rate limits)
DELAY_BETWEEN_REELS = 2  # seconds

# Maximum number of retries if download/creation fails
MAX_RETRIES = 3

# Verbose logging (True = more details in console)
VERBOSE_LOGGING = True

# ========== ADVANCED SETTINGS ==========
# Only change if you know what you're doing

# MoviePy settings
THREADS = 4  # CPU threads to use (higher = faster but more CPU)

# Color grading intensity (0-1)
COLOR_GRADE_INTENSITY = 0.85  # Lower = darker/more dramatic

# Zoom effect speed (for cinematic template)
ZOOM_SPEED = 0.15  # Higher = zoom faster

# Text animation speed
TEXT_FADE_IN = 0.3  # seconds
TEXT_FADE_OUT = 0.2  # seconds

print("✓ Config loaded successfully!")
print(f"✓ ElevenLabs API: {'Configured' if 'your' not in ELEVENLABS_API_KEY else 'NOT SET'}")
print(f"✓ Pexels API: {'Configured' if 'your' not in PEXELS_API_KEY else 'NOT SET'}")
