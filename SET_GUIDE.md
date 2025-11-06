# NDTA NEWS PIPELINE - COMPLETE SETUP GUIDE
## Step-by-Step Instructions

---

## 🎯 WHAT THIS SYSTEM DOES

This automated news pipeline:
1. **SCRAPES** the web for dump truck industry news
2. **FILTERS** only relevant stories (must affect dump truck industry)
3. **GENERATES** professional NDTA news reports using AI
4. **CREATES** branded graphics for social media
5. **DETECTS** state-specific news and alerts you
6. **MANAGES** approval workflow (you + Dee Jay approve before posting)
7. **DISTRIBUTES** to social media after approval

---

## 📋 PREREQUISITES

### What You Need:
- [ ] Computer (Windows, Mac, or Linux)
- [ ] Internet connection
- [ ] VSCode installed
- [ ] Python 3.8+ installed
- [ ] Basic command line knowledge

### Accounts You'll Need:
- [ ] OpenAI account (for AI content generation) - https://platform.openai.com/
- [ ] NewsAPI account (free tier works) - https://newsapi.org/
- [ ] Twitter/X Developer account (for posting)
- [ ] Facebook Developer account (for posting)

---

## 🚀 PART 1: INITIAL SETUP (Do this ONCE)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Install VSCode
1. Go to https://code.visualstudio.com/
2. Download and install
3. Open VSCode
4. Install Python extension:
   - Click Extensions icon (left sidebar)
   - Search "Python"
   - Install the Microsoft Python extension

### Step 3: Download This Project
1. Create a folder on your computer: `C:\NDTA\news-pipeline` (Windows) or `~/NDTA/news-pipeline` (Mac/Linux)
2. Copy ALL files I'm creating into that folder
3. Open VSCode
4. File → Open Folder → Select your `news-pipeline` folder

### Step 4: Create Virtual Environment
Open VSCode Terminal (View → Terminal) and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal.

### Step 5: Install Dependencies
```bash
pip install -r requirements.txt
```

This will take 2-3 minutes. You'll see lots of text scrolling.

### Step 6: Get API Keys

#### OpenAI API Key (REQUIRED):
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Click your profile → "View API Keys"
4. Click "Create new secret key"
5. **COPY IT IMMEDIATELY** (you can't see it again)
6. Cost: ~$0.50-$2.00 per day depending on usage

#### NewsAPI Key (REQUIRED):
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Sign up (FREE plan is fine)
4. Copy your API key

#### Twitter API (Optional - for auto-posting):
1. Go to https://developer.twitter.com/
2. Apply for Developer account
3. Create a new app
4. Get your keys from "Keys and Tokens" tab

#### Facebook API (Optional - for auto-posting):
1. Go to https://developers.facebook.com/
2. Create an app
3. Add "Facebook Login" product
4. Get App ID and App Secret

### Step 7: Configure Environment Variables
1. In VSCode, find `.env.template` file
2. Right-click → "Rename" → Change to `.env`
3. Open `.env` file
4. Fill in your API keys:
   ```
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
   NEWS_API_KEY=xxxxxxxxxxxxxxxxx
   ALERT_EMAIL=your_email@ndta.com,dj@ndta.com
   ```
5. Save the file (Ctrl+S or Cmd+S)

### Step 8: Configure News Sources
1. Open `config/news_sources.yaml`
2. Review the dump truck industry keywords
3. Add any additional keywords relevant to NDTA
4. Review RSS feeds - add/remove as needed
5. Save the file

### Step 9: Test Installation
```bash
python test_setup.py
```

You should see:
```
✅ Python version OK
✅ All packages installed
✅ API keys configured
✅ System ready!
```

---

## 📊 PART 2: DAILY WORKFLOW

### Morning Routine (10-15 minutes):

#### Step 1: Run News Scraper
```bash
python main.py scrape
```

What happens:
- Searches 50+ news sources
- Finds dump truck industry news
- Saves to `data/raw_news/`
- Shows you summary

#### Step 2: Review Scraped News
```bash
python main.py review
```

What you see:
- List of all news stories found
- Relevance score (1-10)
- State detection (if applicable)
- Quick summary

**Your job:** Mark which stories to process:
- Type `y` to process
- Type `n` to skip
- Type `s` to mark as state-specific

#### Step 3: Generate NDTA Reports
```bash
python main.py generate
```

What happens:
- AI reads each approved story
- Writes it in NDTA voice/style
- Creates professional report
- Saves to `data/processed_news/`

Takes 1-2 minutes per story.

#### Step 4: Create Graphics
```bash
python main.py graphics
```

What happens:
- Creates branded social media graphic for each story
- NDTA logo + headline + key visual
- Saves to `data/graphics/`
- Shows you preview

#### Step 5: Review & Approve
```bash
python main.py approve
```

What you see:
- Report text
- Graphic preview
- Distribution plan

**Your decision:**
- Type `approve` - Moves to ready-to-post queue
- Type `edit` - Make changes
- Type `reject` - Discards story

#### Step 6: Review State-Specific Alerts
If any state-specific news was detected:
```bash
python main.py state-alerts
```

Shows:
- Story headline
- Which state
- Suggested Facebook groups
- Draft message

**Your decision:**
- Approve for state group posting
- Or handle manually

#### Step 7: Post to Social Media
```bash
python main.py post
```

Posts all approved content to:
- Twitter/X
- Facebook main page
- State-specific groups (if approved)

---

## 🔄 PART 3: AUTOMATION (Optional)

### Schedule Daily Runs

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Name: "NDTA News Pipeline"
4. Trigger: Daily at 6:00 AM
5. Action: Start a program
6. Program: `C:\NDTA\news-pipeline\venv\Scripts\python.exe`
7. Arguments: `main.py scrape`
8. Start in: `C:\NDTA\news-pipeline`

**Mac/Linux (Cron):**
```bash
crontab -e
```
Add:
```
0 6 * * * cd /path/to/news-pipeline && ./venv/bin/python main.py scrape
```

---

## 📁 PART 4: UNDERSTANDING THE FOLDER STRUCTURE

```
ndta-news-pipeline/
├── main.py                          # Main control script
├── requirements.txt                 # Python packages
├── .env                            # Your API keys (KEEP SECRET!)
├── .env.template                   # Template for .env
│
├── config/                         # Configuration files
│   ├── news_sources.yaml          # Keywords, RSS feeds, sources
│   ├── state_detection.yaml       # State detection rules
│   └── social_templates.yaml      # Post templates
│
├── scrapers/                       # News scraping modules
│   ├── news_scraper.py            # Main scraper
│   ├── rss_scraper.py             # RSS feed reader
│   └── web_scraper.py             # Web page scraper
│
├── content_generator/              # AI content creation
│   ├── report_generator.py        # Creates NDTA reports
│   ├── headline_generator.py      # Creates catchy headlines
│   └── state_detector.py          # Detects state-specific news
│
├── graphics/                       # Graphic creation
│   ├── graphic_generator.py       # Creates social media graphics
│   └── templates/                 # Graphic templates
│       ├── ndta_template.png
│       └── state_template.png
│
├── distribution/                   # Social media posting
│   ├── twitter_poster.py          # Posts to Twitter
│   ├── facebook_poster.py         # Posts to Facebook
│   └── approval_manager.py        # Manages approval workflow
│
├── data/                          # All generated data
│   ├── raw_news/                  # Scraped articles (JSON)
│   ├── processed_news/            # NDTA reports (TXT/JSON)
│   ├── graphics/                  # Generated images (PNG)
│   └── approved_content/          # Ready to post
│
└── logs/                          # System logs
    ├── scraper.log
    ├── generator.log
    └── distribution.log
```

---

## 🎨 PART 5: CUSTOMIZATION

### Change NDTA Branding
Edit: `config/brand_settings.yaml`
- Upload your logo: `graphics/templates/ndta_logo.png`
- Change colors
- Modify fonts

### Adjust News Relevance
Edit: `config/news_sources.yaml`
- Add/remove keywords
- Change relevance thresholds
- Add new RSS feeds

### Modify Report Style
Edit: `content_generator/prompts.py`
- Change tone (formal, casual, technical)
- Adjust length
- Modify structure

### Add New Social Platforms
Create new file: `distribution/new_platform.py`
Follow pattern from `twitter_poster.py`

---

## 🐛 PART 6: TROUBLESHOOTING

### "ModuleNotFoundError"
**Problem:** Python can't find a package
**Solution:**
```bash
pip install -r requirements.txt
```

### "API Key Invalid"
**Problem:** API key not working
**Solution:**
1. Check `.env` file
2. Ensure no extra spaces
3. Regenerate key if needed

### "No news found"
**Problem:** Scraper isn't finding articles
**Solution:**
1. Check internet connection
2. Verify keywords in `config/news_sources.yaml`
3. Check `logs/scraper.log` for errors

### "AI generation failed"
**Problem:** OpenAI API error
**Solution:**
1. Check OpenAI account has credits
2. Verify API key is correct
3. Check rate limits

### Graphics won't generate
**Problem:** Image creation failing
**Solution:**
1. Install Pillow: `pip install Pillow`
2. Check logo file exists
3. Verify write permissions in `data/graphics/`

---

## 📞 PART 7: GETTING HELP

### Check Logs
```bash
# View recent errors
python main.py logs

# View specific log
cat logs/scraper.log
```

### Test Individual Components
```bash
# Test scraper only
python scrapers/news_scraper.py

# Test AI generator only
python content_generator/report_generator.py

# Test graphic creator only
python graphics/graphic_generator.py
```

### Debug Mode
```bash
# Run with verbose output
python main.py scrape --debug
```

---

## 🎯 PART 8: WHAT SUCCESS LOOKS LIKE

### Week 1:
- [ ] System installed and running
- [ ] Finding 5-10 relevant stories per day
- [ ] Generating quality NDTA reports
- [ ] Graphics look professional

### Week 2:
- [ ] Refined keywords for better accuracy
- [ ] Established approval workflow
- [ ] Posting 1-2 stories per day
- [ ] State detection working

### Week 3:
- [ ] Automated daily scraping
- [ ] Smooth approval process
- [ ] Consistent posting schedule
- [ ] State-specific groups receiving content

### Month 1:
- [ ] 30+ quality posts published
- [ ] NDTA brand voice established
- [ ] Audience engagement growing
- [ ] System running smoothly

---

## 🔒 PART 9: SECURITY & BEST PRACTICES

### Protect Your API Keys
- ✅ NEVER commit `.env` to Git
- ✅ NEVER share API keys
- ✅ Rotate keys every 90 days
- ✅ Use separate keys for testing/production

### Data Privacy
- Only scrape public data
- Don't store personal information
- Follow social media Terms of Service
- Comply with copyright laws

### Backup Strategy
```bash
# Backup weekly
python main.py backup
```

Saves to: `backups/YYYY-MM-DD/`

---

## 📈 PART 10: ADVANCED FEATURES

### A/B Testing Headlines
```bash
python main.py generate --variants 3
```
Creates 3 different versions of each report.

### Scheduled Posting
```bash
python main.py schedule --time "2:00 PM" --days "Mon,Wed,Fri"
```

### Analytics Dashboard
```bash
python main.py dashboard
```
Opens web interface showing:
- Stories found per day
- Engagement metrics
- Top-performing content

### Bulk Operations
```bash
# Process last 7 days
python main.py scrape --days 7

# Regenerate all graphics
python main.py graphics --regenerate-all
```

---

## 🚨 PART 11: EMERGENCY PROCEDURES

### System Down
1. Check logs: `python main.py logs`
2. Verify API keys: `python test_setup.py`
3. Restart services: `python main.py restart`

### Bad Content Posted
1. Delete from social: `python main.py delete --post-id [ID]`
2. Review approval process
3. Update filters

### API Costs Too High
1. Check usage: `python main.py usage`
2. Reduce scraping frequency
3. Adjust AI model (use GPT-3.5 instead of GPT-4)

---

## 📚 PART 12: LEARNING RESOURCES

### Python Basics
- https://www.python.org/about/gettingstarted/
- https://realpython.com/

### API Integration
- OpenAI Docs: https://platform.openai.com/docs
- NewsAPI Docs: https://newsapi.org/docs

### Social Media APIs
- Twitter: https://developer.twitter.com/en/docs
- Facebook: https://developers.facebook.com/docs

---

## ✅ QUICK START CHECKLIST

- [ ] Python installed
- [ ] VSCode installed and configured
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured with API keys
- [ ] `config/news_sources.yaml` reviewed
- [ ] `test_setup.py` runs successfully
- [ ] First scrape completed: `python main.py scrape`
- [ ] First report generated: `python main.py generate`
- [ ] First graphic created: `python main.py graphics`
- [ ] Approval workflow tested: `python main.py approve`
- [ ] First post published: `python main.py post`

---

## 🎓 TRAINING TIMELINE

### Day 1 (2 hours):
- Install Python, VSCode
- Set up project
- Get API keys
- Run first scrape

### Day 2 (1 hour):
- Review scraped news
- Generate first report
- Create first graphic
- Understand approval flow

### Day 3 (1 hour):
- Post first story
- Test state detection
- Refine keywords
- Practice workflow

### Week 2:
- Run independently
- Fine-tune settings
- Build confidence
- Establish routine

---

## 💡 PRO TIPS

1. **Start Small**: Begin with 1-2 posts per day, then scale up
2. **Review Regularly**: Check `data/processed_news/` to ensure quality
3. **Refine Keywords**: Adjust based on what's working
4. **Batch Process**: Review morning scrapes, post in afternoon
5. **Monitor Engagement**: Track which stories perform best
6. **Stay Consistent**: Daily scraping keeps content fresh
7. **Backup Often**: Don't lose your work
8. **Document Changes**: Keep notes on what you modify

---

## 📞 SUPPORT

For issues with this system:
1. Check logs first
2. Review troubleshooting section
3. Test individual components
4. Check API status pages

For NDTA-specific questions:
- Contact: [Your contact info]
- Email: [Your email]

---

## 🎉 YOU'RE READY!

Start with:
```bash
python main.py scrape
```

Then follow the daily workflow in Part 2.

**Good luck with the NDTA News Pipeline!** 🚛📰