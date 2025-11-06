# 🚀 GETTING STARTED - NDTA News Pipeline

**Welcome! This guide will get you up and running in 15 minutes.**

---

## ✅ Step 1: Install Dependencies

```bash
# Make sure you're in the project directory
cd new-pipeline

# Install Python packages
pip install -r requirements.txt
```

**Expected output:** All packages install successfully

---

## 🔑 Step 2: Configure API Keys

### 2.1 Create your .env file

```bash
# Copy the template
cp .env.template .env

# Edit the file (use notepad, VS Code, or any text editor)
notepad .env
```

### 2.2 Get your API keys

You'll need these services:

#### **OpenAI (REQUIRED)** - For AI content generation
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key and paste it in `.env` as `OPENAI_API_KEY`
5. **Cost:** ~$1-2 per day for typical usage

#### **NewsAPI (OPTIONAL but recommended)** - For web news scraping
1. Go to: https://newsapi.org/
2. Sign up for free account
3. Copy your API key
4. Paste in `.env` as `NEWSAPI_KEY`
5. **Cost:** Free tier (100 requests/day)

#### **Twitter/X API (REQUIRED for Twitter posting)**
1. Go to: https://developer.twitter.com/
2. Apply for developer account
3. Create a new app
4. Get these 4 keys:
   - API Key → `TWITTER_API_KEY`
   - API Secret → `TWITTER_API_SECRET`
   - Access Token → `TWITTER_ACCESS_TOKEN`
   - Access Secret → `TWITTER_ACCESS_SECRET`
5. **Cost:** Free

#### **Facebook API (REQUIRED for Facebook posting)**
1. Go to: https://developers.facebook.com/
2. Create an app
3. Get Page Access Token
4. Get your Page ID
5. Paste in `.env`:
   - `FACEBOOK_ACCESS_TOKEN`
   - `FACEBOOK_PAGE_ID`
6. **Cost:** Free

#### **Email Alerts (OPTIONAL but recommended)**
For Gmail:
1. Enable 2-factor authentication
2. Create an app-specific password
3. Use these settings in `.env`:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ALERT_EMAIL=your_email@gmail.com
   ```

---

## 🧪 Step 3: Test Your Setup

```bash
python test_setup.py
```

**Expected output:**
```
✅ Python version OK
✅ All packages installed
✅ API keys configured
✅ System ready!
```

---

## 🎯 Step 4: Customize for NDTA

### 4.1 Update Brand Colors

Edit `config/news_sources.yaml`:

```yaml
graphics:
  brand_colors:
    primary: "#YOUR_PRIMARY_COLOR"    # NDTA dark blue
    secondary: "#YOUR_SECONDARY_COLOR" # NDTA orange
    accent: "#FFFFFF"
    text: "#333333"
```

### 4.2 Add Your Logo (Optional)

Place your NDTA logo at:
- `graphics/templates/ndta_logo.png`

The system will automatically include it in graphics.

### 4.3 Review Keywords

Edit `config/news_sources.yaml` and review:
- `primary_keywords` - Core dump truck terms
- `secondary_keywords` - Related industry terms

Add any NDTA-specific terms you want to track.

### 4.4 Configure State Facebook Groups

Edit `content_generator/state_detector.py`:

```python
self.facebook_groups = {
    'GA': ['Georgia Dump Truck Operators', 'Your Group Name'],
    'TX': ['Texas Dump Truck Association', 'Your Group Name'],
    # Add your state groups here
}
```

---

## 🚀 Step 5: Run Your First Scrape!

```bash
# Scrape news from the last 7 days
python main.py scrape
```

**What happens:**
1. Searches 50+ news sources
2. Finds dump truck industry news
3. AI filters for relevance (must help/affect dump truck industry)
4. Detects state-specific news
5. Saves results to `data/raw_news/`

**Expected output:**
```
🔍 NDTA NEWS SCRAPER
============================================================
✅ Scraping complete!
   Total articles found: 45
   Relevant articles: 12
   High relevance (8-10): 5
   State-specific: 2

⚠️  STATE-SPECIFIC NEWS DETECTED!
   Run 'python main.py state-alerts' to review
```

---

## 📋 Step 6: Review Articles

```bash
python main.py review
```

**What you do:**
- Review each article
- Type `y` to approve for processing
- Type `n` to skip
- Type `s` to mark as state-specific
- Type `q` to quit (saves progress)

**Time:** 2-3 minutes

---

## ✍️ Step 7: Generate NDTA Reports

```bash
python main.py generate
```

**What happens:**
- AI transforms each approved article into NDTA-branded report
- Creates professional headline
- Writes in NDTA voice
- Adds industry perspective
- Generates social media post

**Time:** 1-2 minutes per article (automatic)

---

## 🎨 Step 8: Create Graphics

```bash
python main.py graphics
```

**What happens:**
- Creates branded social media graphic for each report
- NDTA colors and branding
- Optimized for Twitter/Facebook (1200x630)
- Saves to `data/graphics/`

**Time:** Automatic (few seconds per graphic)

---

## ✅ Step 9: Approve Content

```bash
python main.py approve
```

**What you do:**
- Review each report + graphic
- Type `a` to approve for posting
- Type `e` to edit text
- Type `r` to reject
- Type `q` to quit (saves progress)

**Time:** 5 minutes

---

## 📱 Step 10: Post to Social Media

```bash
python main.py post
```

**What happens:**
- Posts all approved content to Twitter
- Posts all approved content to Facebook
- Logs all post URLs
- Marks content as posted

**Time:** Automatic

---

## 🗺️ Step 11: Handle State-Specific News

```bash
python main.py state-alerts
```

**What you see:**
- State-specific news items
- Suggested Facebook groups
- Draft messages

**What you do:**
- Manually post to state Facebook groups (for now)
- Later: System will automate this too

---

## 📊 Daily Workflow Summary

### Morning (10 minutes):
```bash
python main.py scrape    # Find news
python main.py review    # Approve articles
```

### Afternoon (10 minutes):
```bash
python main.py generate  # AI creates reports
python main.py graphics  # Creates graphics
python main.py approve   # Final approval
python main.py post      # Publish
```

**Total time:** 15-20 minutes per day
**Output:** 5-10 professional posts per day

---

## 🆘 Troubleshooting

### "No API key configured"
→ Check your `.env` file has the correct keys

### "No articles found"
→ Try increasing lookback days: `python main.py scrape --days 14`

### "OpenAI API error"
→ Check your OpenAI account has credits

### "Twitter posting failed"
→ Verify all 4 Twitter API keys are correct

### "Graphics look wrong"
→ Update brand colors in `config/news_sources.yaml`

---

## 📚 Next Steps

1. **Automate:** Set up daily cron job or Windows Task Scheduler
2. **Customize:** Adjust AI prompts in `content_generator/prompts.py`
3. **Expand:** Add more RSS feeds in `config/news_sources.yaml`
4. **Monitor:** Check `logs/` directory for any issues

---

## 💡 Pro Tips

- Run `python main.py status` anytime to see what's pending
- Check `python main.py logs` to see recent errors
- State alerts are emailed automatically (if configured)
- You can edit reports before posting (use `e` in approve step)
- Graphics are saved even if posting fails

---

## 🎉 You're Ready!

The NDTA News Pipeline is now set up and ready to make you the most informed voice in the dump truck industry.

**Questions?** Check the other docs:
- `README.md` - Full documentation
- `QUICK_REFERENCE.md` - Command cheat sheet
- `SET_GUIDE.md` - Detailed setup guide

**Let's make NDTA news the best in the industry! 🚛📰**

