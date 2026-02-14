"""
Auto-Reel Creator for Storytelling Channel
Creates high-quality, engaging reels automatically

Usage:
    python auto_reel_creator.py

Requirements:
    - API keys configured in config.py
    - CSV file with stories (templates/week_stories.csv)
    - Dependencies installed (pip install -r requirements.txt)

Output:
    - 21 finished reels in exports/week_X/ folder
"""

import os
import sys
from datetime import datetime

print("\n" + "="*70)
print("  AUTO-REEL CREATOR - Storytelling Channel")
print("  High-Quality, Engaging Content Automation")
print("="*70 + "\n")

# Check Python version
if sys.version_info < (3, 7):
    print("❌ ERROR: Python 3.7 or higher required")
    print(f"   Your version: {sys.version}")
    sys.exit(1)

print("✓ Python version OK")

# Import dependencies
try:
    from moviepy.editor import *
    from elevenlabs import generate, set_api_key
    import requests
    import pandas as pd
    from PIL import Image, ImageDraw, ImageFont
    import time
    print("✓ All dependencies loaded\n")
except ImportError as e:
    print(f"❌ ERROR: Missing dependency: {e}")
    print("\n💡 Fix: Run this command:")
    print("   pip install -r requirements.txt\n")
    sys.exit(1)

# Load configuration
try:
    from config import *
    print("✓ Configuration loaded")
except ImportError:
    print("❌ ERROR: config.py not found")
    print("\n💡 Fix: Ensure config.py is in the scripts folder\n")
    sys.exit(1)

# Validate API keys
if "your" in ELEVENLABS_API_KEY.lower():
    print("\n❌ ERROR: ElevenLabs API key not configured")
    print("💡 Fix: Edit config.py and add your API key from elevenlabs.io\n")
    sys.exit(1)

if "your" in PEXELS_API_KEY.lower():
    print("\n❌ ERROR: Pexels API key not configured")
    print("💡 Fix: Edit config.py and add your API key from pexels.com/api\n")
    sys.exit(1)

print("✓ API keys configured\n")

# Initialize ElevenLabs
set_api_key(ELEVENLABS_API_KEY)


# ========== CORE FUNCTIONS ==========

def download_stock_video(search_query, output_path):
    """Download video from Pexels"""
    print(f"  → Downloading footage: {search_query}")
    
    url = "https://api.pexels.com/videos/search"
    params = {
        'query': search_query,
        'per_page': 1,
        'orientation': 'portrait'
    }
    headers = {"Authorization": PEXELS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if not data.get('videos'):
            print(f"    ⚠️ No video found, using fallback...")
            params['query'] = "dark mystery cinematic"
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
        
        # Find best quality vertical video
        video_files = data['videos'][0]['video_files']
        video_url = None
        
        for vf in video_files:
            if vf.get('width') == 1080 and vf.get('height') >= 1920:
                video_url = vf['link']
                break
        
        if not video_url:
            video_url = video_files[0]['link']
        
        # Download
        video_data = requests.get(video_url)
        with open(output_path, 'wb') as f:
            f.write(video_data.content)
        
        print(f"    ✓ Downloaded")
        return output_path
        
    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        raise


def generate_voiceover(script, output_path, voice="Marcus"):
    """Generate AI voiceover"""
    print(f"  → Generating voiceover ({len(script)} chars)")
    
    try:
        audio = generate(
            text=script,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        
        with open(output_path, 'wb') as f:
            f.write(audio)
        
        print(f"    ✓ Voiceover created")
        return output_path
        
    except Exception as e:
        print(f"    ❌ ERROR: {e}")
        raise


def create_text_overlay(text, output_path, size=(1080, 300)):
    """Create text overlay image"""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Use default font (better compatibility)
    try:
        font = ImageFont.truetype("impact.ttf", 70)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position (center)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw black outline
    for adj in range(-3, 4):
        for adj_y in range(-3, 4):
            draw.text((x+adj, y+adj_y), text, font=font, fill='black')
    
    # Draw white text
    draw.text((x, y), text, font=font, fill='white')
    
    img.save(output_path)
    return output_path


def create_reel(story_data, output_path, story_index):
    """Create complete reel from story data"""
    
    print(f"\n🎬 Creating reel #{story_index + 1}: {story_data['title']}")
    
    # Create temp folder
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    
    temp_video = os.path.join(TEMP_FOLDER, f"temp_video_{story_index}.mp4")
    temp_audio = os.path.join(TEMP_FOLDER, f"temp_audio_{story_index}.mp3")
    temp_text = os.path.join(TEMP_FOLDER, f"temp_text_{story_index}.png")
    
    try:
        # 1. Download stock footage
        search_term = CATEGORY_FOOTAGE.get(story_data['category'], 'dark mystery')
        download_stock_video(search_term, temp_video)
        
        # 2. Generate voiceover
        voice = VOICES.get(story_data['category'], 'Marcus')
        generate_voiceover(story_data['script'], temp_audio, voice)
        
        # 3. Load clips
        print(f"  → Assembling video...")
        video_clip = VideoFileClip(temp_video)
        audio_clip = AudioFileClip(temp_audio)
        
        # 4. Match duration
        video_duration = min(audio_clip.duration, 60)
        if video_clip.duration < video_duration:
            video_clip = video_clip.loop(duration=video_duration)
        else:
            video_clip = video_clip.subclip(0, video_duration)
        
        # 5. Resize to 9:16
        video_clip = video_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))
        
        # 6. Add audio
        video_clip = video_clip.set_audio(audio_clip)
        
        # 7. Create text overlay
        create_text_overlay(story_data['hook'], temp_text)
        text_clip = ImageClip(temp_text).set_duration(HOOK_DURATION).set_position(('center', 100))
        
        # 8. Composite
        final = CompositeVideoClip([video_clip, text_clip.set_start(0)])
        
        # 9. Color grading (darker, more dramatic)
        final = final.fx(vfx.colorx, COLOR_GRADE_INTENSITY)
        
        # 10. Export
        print(f"  → Exporting (this takes 1-2 minutes)...")
        final.write_videofile(
            output_path,
            fps=VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            bitrate=VIDEO_BITRATE,
            preset=VIDEO_PRESET,
            threads=THREADS,
            logger=None  # Suppress moviepy logs
        )
        
        print(f"  ✅ SUCCESS: {os.path.basename(output_path)}")
        
    except Exception as e:
        print(f"  ❌ FAILED: {e}")
        raise
        
    finally:
        # Cleanup temp files
        for temp_file in [temp_video, temp_audio, temp_text]:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def batch_create_reels(csv_path, output_folder):
    """Create all reels from CSV"""
    
    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"\n❌ ERROR: CSV file not found: {csv_path}")
        print("\n💡 Fix: Create your stories CSV file")
        print(f"   Template: templates/week_stories_template.csv")
        print(f"   Expected: {csv_path}\n")
        return
    
    # Load stories
    try:
        stories = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(stories)} stories from CSV\n")
    except Exception as e:
        print(f"\n❌ ERROR reading CSV: {e}\n")
        return
    
    # Validate CSV format
    required_columns = ['Title', 'Hook', 'Script', 'Category']
    missing = [col for col in required_columns if col not in stories.columns]
    if missing:
        print(f"\n❌ ERROR: CSV missing columns: {missing}")
        print("💡 Required columns: Title, Hook, Script, Category, CTA\n")
        return
    
    # Create output folder with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    full_output_path = os.path.join(output_folder, f"batch_{timestamp}")
    os.makedirs(full_output_path, exist_ok=True)
    
    print("="*70)
    print(f"🚀 BATCH CREATION STARTED")
    print(f"   Stories: {len(stories)}")
    print(f"   Output: {full_output_path}")
    print("="*70 + "\n")
    
    start_time = time.time()
    success_count = 0
    
    # Process each story
    for index, row in stories.iterrows():
        story_data = {
            'title': row['Title'],
            'hook': row['Hook'],
            'script': row['Script'],
            'category': row.get('Category', 'Mystery'),
            'cta': row.get('CTA', '')
        }
        
        # Safe filename
        safe_title = "".join([c for c in row['Title'] if c.isalnum() or c in (' ', '-')])[:30]
        output_path = os.path.join(full_output_path, f"reel_{index+1:02d}_{safe_title}.mp4")
        
        try:
            create_reel(story_data, output_path, index)
            success_count += 1
        except Exception as e:
            print(f"\n⚠️ Skipping reel #{index+1} due to error\n")
            continue
        
        # Delay to avoid rate limits
        if index < len(stories) - 1:
            time.sleep(DELAY_BETWEEN_REELS)
    
    # Summary
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "="*70)
    print(f"✅ BATCH COMPLETE!")
    print(f"   Success: {success_count}/{len(stories)} reels created")
    print(f"   Time: {minutes}m {seconds}s")
    print(f"   Location: {os.path.abspath(full_output_path)}")
    print("="*70 + "\n")
    
    if success_count < len(stories):
        print(f"⚠️ {len(stories) - success_count} reels failed")
        print("   Check errors above for details\n")


# ========== MAIN ==========

if __name__ == "__main__":
    print("\n📂 Checking files...\n")
    
    # Check if CSV exists
    csv_path = STORIES_CSV
    if not os.path.exists(csv_path):
        print(f"⚠️ CSV not found: {csv_path}")
        print("\n💡 Creating example CSV...")
        
        os.makedirs("templates", exist_ok=True)
        
        example_data = {
            'Title': ['Library of Alexandria', 'Evil Nurse'],
            'Hook': [
                'It contained all human knowledge. Then it burned.',
                'She was the most trusted nurse. Then they counted the bodies.'
            ],
            'Script': [
                'The Library of Alexandria... the greatest collection of knowledge in the ancient world. Hundreds of thousands of scrolls... containing the secrets of lost civilizations. Then... it burned. Some say Julius Caesar started the fire accidentally. Others blame religious fanatics. But the truth? We may never know. What we do know... is what was lost. Works of Aristotle we will never read. Scientific discoveries... forgotten for a thousand years. The library didn not burn in one night. It died slowly... over centuries. Each fire... each invasion... took more knowledge with it. Today... we can only imagine... what humanity lost forever.',
                'Genene Jones seemed like the perfect pediatric nurse. Caring... dedicated... always there when a child crashed. But then... doctors noticed a pattern. Babies only coded on her shift. The hospital investigated. What they found... was horrifying. Jones had been injecting children with dangerous drugs... causing them to crash... so she could play the hero and save them. But many didn not survive. In 1984... she was convicted. Suspected in over 60 infant deaths. She is still in prison today. The most trusted... became the most deadly.'
            ],
            'Category': ['Historical', 'True Crime'],
            'CTA': ['Follow for more mysteries!', 'Part 2 tomorrow!']
        }
        
        pd.DataFrame(example_data).to_csv(csv_path, index=False)
        print(f"✓ Created example CSV: {csv_path}")
        print("\n📝 Edit this file with your 21 stories, then run again!\n")
        sys.exit(0)
    
    # Run batch creation
    batch_create_reels(csv_path, OUTPUT_FOLDER)
    
    print("🎉 All done! Your reels are ready to schedule.\n")
