# 🤖 Python Automation Scripts (Advanced/Optional)

## ⚠️ Do You Need This?

**NO** - if you're comfortable with Canva (recommended method)  
**YES** - if you want 100% automation AND are comfortable with Python

**Time savings:** Canva = 90 min/week | Python = 30 min/week  
**Difficulty:** Canva = Easy | Python = Advanced (coding required)

---

## 📋 What These Scripts Do

**Fully automated reel creation:**
1. Read stories from CSV file
2. Generate voiceovers via ElevenLabs API
3. Download stock footage from Pexels API
4. Create text overlays
5. Assemble video + audio + text
6. Export 21 finished reels

**Input:** CSV with 21 stories  
**Output:** 21 finished MP4 reels  
**Time:** ~30 minutes (runs automatically)

---

## 🔧 Setup (One-Time, ~2 Hours)

### Step 1: Install Python

**Windows:**
1. Download: [python.org/downloads](https://python.org/downloads)
2. Run installer
3. ✅ **CHECK "Add Python to PATH"** (critical!)
4. Install

**Verify:**
```bash
python --version
```
Should show: Python 3.7 or higher

---

### Step 2: Install Dependencies

Open Command Prompt in this folder:
```bash
cd C:\Users\jitan\Documents\social-media\Execution\storytelling-6-month-roadmap\scripts
pip install -r requirements.txt
```

Wait 5-10 minutes for installation.

---

### Step 3: Get API Keys

**ElevenLabs API:**
1. Go to: [elevenlabs.io](https://elevenlabs.io)
2. Sign up for Creator plan ($22/month - required for API)
3. Profile → API Keys → Generate
4. Copy key: `sk_abc123...`

**Pexels API:**
1. Go to: [pexels.com/api](https://pexels.com/api)
2. Sign up (FREE)
3. Get API key
4. Copy key

---

### Step 4: Configure API Keys

**Edit `config.py`:**

```python
# Line 9-10: Paste your API keys
ELEVENLABS_API_KEY = "sk_your_actual_key_here"
PEXELS_API_KEY = "your_actual_pexels_key_here"
```

Save the file.

---

## 🚀 How To Use

### Every Sunday (To Create 21 Reels):

**Step 1: Prepare Stories CSV**

Option A - Manual:
1. Open: `../02-MASTER-STORY-DATABASE.md`
2. Pick 21 stories
3. Copy to: `../templates/week_stories.csv`
4. Format: `Title,Hook,Script,Category,CTA`

Option B - Use ChatGPT:
```
Generate CSV for these 21 stories:
1. Library of Alexandria
2. Evil Nurse
... [list all 21]

Format: Title,Hook,Script,Category,CTA
Each script should be 150-180 words.
```

Copy output to `../templates/week_stories.csv`

---

**Step 2: Run The Script**

```bash
cd scripts
python auto_reel_creator.py
```

**What happens:**
- Script reads CSV
- Generates 21 voiceovers (ElevenLabs API)
- Downloads 21 stock videos (Pexels API)
- Creates 21 text overlays
- Assembles all elements
- Exports 21 finished reels

**Time: ~25-35 minutes** (runs automatically, walk away!)

**Output:** All reels saved to `exports/batch_[date]/`

---

**Step 3: Schedule Reels**

Same as Canva method:
1. Go to Meta Business Suite
2. Upload all 21 reels
3. Schedule 3x/day for 7 days

---

## ⚙️ Customization

**Edit `config.py` to change:**
- Video quality (bitrate, FPS)
- Text font sizes and colors
- Voice selection per category
- Color grading intensity
- Export settings

**All settings are commented and explained.**

---

## 🐛 Troubleshooting

### "pip not recognized"
**Fix:** Python not in PATH. Reinstall Python with "Add to PATH" checked.

### "Module not found"
**Fix:** Run `pip install -r requirements.txt` again

### "API key invalid"
**Fix:** Check `config.py` - keys must not have "your_" in them

### "No videos found on Pexels"
**Fix:** Check internet connection. Script has fallback searches.

### "Export fails"
**Fix:** 
- Check disk space (each reel = ~10-20MB)
- Close other programs
- Try lower bitrate in config.py

### Script runs but creates broken videos
**Fix:**
- Check if ffmpeg is installed (moviepy requirement)
- Update moviepy: `pip install --upgrade moviepy`

---

## 📊 Cost Comparison

| Method | Monthly Cost | Time/Week | Difficulty |
|--------|-------------|-----------|------------|
| **Canva** | $0 | 90 min | Easy |
| **Python** | $22 | 30 min | Advanced |

**Python saves 1 hour/week BUT:**
- Requires $22/month (ElevenLabs API not available on free tier)
- Requires Python knowledge
- More potential for bugs/issues
- Less control over design

**Recommendation:** Start with Canva. Switch to Python only if:
- You're creating 50+ reels/month
- You're comfortable debugging code
- $22/month is worth saving 1 hour/week

---

## 🎯 When To Use Python Automation

**Good reasons:**
- ✅ Scaling to multiple channels (100+ reels/month)
- ✅ You already code in Python
- ✅ You want fully hands-off content creation

**Bad reasons:**
- ❌ "It sounds cool" (stick with Canva)
- ❌ You're new to programming (too frustrating)
- ❌ You want more design control (Canva is better)

---

## 📁 File Structure

```
scripts/
├── README.md (this file)
├── auto_reel_creator.py (main script)
├── config.py (your settings and API keys)
└── requirements.txt (dependencies)

templates/
└── week_stories.csv (your story data)

exports/
└── batch_[timestamp]/
    ├── reel_01_story-title.mp4
    ├── reel_02_story-title.mp4
    └── ... (all 21 reels)
```

---

## ✅ Quick Start Checklist

Setup (one-time):
- [ ] Python installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] ElevenLabs API key obtained ($22/month plan)
- [ ] Pexels API key obtained (free)
- [ ] Both keys added to `config.py`
- [ ] Test run with 2 example stories

Weekly use:
- [ ] Pick 21 stories from database
- [ ] Create `week_stories.csv`
- [ ] Run: `python auto_reel_creator.py`
- [ ] Wait 30 minutes
- [ ] Upload exported reels to Meta Suite

---

## 💡 Pro Tips

1. **Test first:** Start with just 2 stories to test setup
2. **Check quality:** Review first batch manually before scheduling
3. **Backup config:** Save `config.py` somewhere safe (has your API keys)
4. **Monitor costs:** ElevenLabs charges per character ($22/month ≈ 100 reels)
5. **Update regularly:** `pip install --upgrade -r requirements.txt`

---

## 🚀 Bottom Line

**Python automation is OPTIONAL.**

Most successful creators use Canva because:
- More design control
- Less technical knowledge needed
- Troubleshooting is visual, not code
- $0 vs $22/month

**Use Python only if you're technical AND creating at massive scale (50+ reels/week).**

**For 21 reels/week, Canva is perfect.**

---

**Need help? Check the main README.md for Canva method (recommended!).**

---

*Last Updated: February 15, 2026*
