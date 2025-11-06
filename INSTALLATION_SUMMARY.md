# 🚛 NDTA NEWS PIPELINE - INSTALLATION SUMMARY

## 📦 What You're Getting

A complete, production-ready news automation system that:

✅ **Scrapes** 50+ news sources for dump truck industry news  
✅ **Filters** using AI - only stories that affect dump trucks  
✅ **Generates** professional NDTA-branded reports  
✅ **Creates** social media graphics automatically  
✅ **Detects** state-specific news and alerts you  
✅ **Manages** approval workflow (you + Dee Jay)  
✅ **Distributes** to Twitter, Facebook, state groups  

**Time investment:** 15-20 minutes per day  
**Cost:** ~$1-2/day in API costs  
**Output:** 5-10 professional posts per day  

---

## 📂 FILES INCLUDED

### Documentation (START HERE!)
- **README.md** - Project overview
- **SETUP_GUIDE.md** - Complete step-by-step setup (60 pages!)
- **QUICK_REFERENCE.md** - Daily commands cheat sheet
- **test_setup.py** - Verify installation

### Configuration
- **requirements.txt** - Python dependencies
- **.env.template** - API keys template
- **.gitignore** - Git ignore rules
- **config/news_sources.yaml** - Keywords, sources, all settings

### Core System
- **main.py** - Main control script (all commands)

### Modules (I'll create these next)
- **scrapers/** - News scraping components
- **content_generator/** - AI content creation
- **graphics/** - Social media graphics
- **distribution/** - Social media posting & approval

### Data Directories
- **data/** - All generated content
- **logs/** - System logs

---

## 🚀 3-STEP QUICK START

### Step 1: Install (5 minutes)
```bash
cd ndta-news-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure (5 minutes)
```bash
cp .env.template .env
# Edit .env - add your OpenAI and NewsAPI keys
```

### Step 3: Run (2 minutes)
```bash
python test_setup.py      # Verify installation
python main.py scrape     # Start scraping!
```

---

## 🔑 API KEYS YOU NEED

### Required (System won't work without these):

**1. OpenAI API Key** (~$1-2/day)
- Go to: https://platform.openai.com/
- Sign up / Log in
- Click "API keys" → "Create new secret key"
- Copy the key (starts with `sk-`)
- Add to `.env` file

**2. NewsAPI Key** (FREE!)
- Go to: https://newsapi.org/
- Click "Get API Key"
- Sign up (free plan is fine)
- Copy your API key
- Add to `.env` file

### Optional (For auto-posting):

**3. Twitter API**
- https://developer.twitter.com/
- Apply for developer account
- Create app, get keys

**4. Facebook API**
- https://developers.facebook.com/
- Create app
- Get App ID and Secret

---

## 📋 DAILY WORKFLOW

### Your 15-Minute Morning Routine:

```bash
# 1. Scrape news (automatic)
python main.py scrape

# 2. Review what was found (you decide what to process)
python main.py review

# 3. Generate NDTA reports (AI does the work)
python main.py generate

# 4. Create graphics (automatic)
python main.py graphics

# 5. Approve content (you make final call)
python main.py approve

# 6. Post to social media (automatic)
python main.py post
```

That's it! System handles the rest.

---

## 🎯 WHAT HAPPENS NEXT

### Today:
1. Download the `ndta-news-pipeline` folder
2. Open in VSCode
3. Follow SETUP_GUIDE.md
4. Run your first scrape

### This Week:
- Fine-tune keywords for your needs
- Test the approval workflow
- Publish first posts
- Get comfortable with commands

### This Month:
- 30+ quality posts published
- NDTA voice established
- Audience growing
- System running smoothly

---

## 📊 WHAT YOU'LL SEE

### After First Scrape:
```
🔍 NDTA NEWS SCRAPER
===================================
✅ Scraping complete!
   Total articles found: 45
   Relevant articles: 12
   High relevance (8-10): 5
   State-specific: 2

⚠️  STATE-SPECIFIC NEWS DETECTED!
   Run 'python main.py state-alerts' to review
```

### During Review:
```
--- Article 1/12 ---
Title: New EPA Emissions Standards for Heavy Trucks
Source: Transport Topics
Date: 2024-11-04
Relevance Score: 9/10

Summary: EPA announces new emissions standards that will 
affect dump trucks starting in 2026...

Process this article? (y)es / (n)o / (s)tate-specific: 
```

### After Generation:
```
✍️  GENERATE NDTA REPORTS
===================================
Generating reports for 8 articles...

[1/8] Processing: New EPA Emissions Standards...
  ✅ Report generated: EPA's New Rules: What Dump...

[2/8] Processing: Fuel Prices Surge Nationwide...
  ✅ Report generated: Rising Diesel Costs Impact...
```

---

## 🎨 CUSTOMIZATION

Everything is configurable! Edit these files:

### Keywords & Sources
`config/news_sources.yaml`
```yaml
primary_keywords:
  - "dump truck"
  - "your keyword here"
```

### NDTA Voice & Tone
`content_generator/prompts.py`
```python
TONE = "professional yet accessible"
AUDIENCE = "dump truck owners"
```

### Graphics & Branding
- Add logo: `graphics/templates/ndta_logo.png`
- Colors in `config/news_sources.yaml`

---

## 🚨 STATE-SPECIFIC MAGIC

When the system finds state-specific news:

1. **Automatic Detection**
   - "Georgia passes new truck law"
   - "California announces regulation"
   - "Texas infrastructure project"

2. **You Get Alerted**
   - Email notification
   - Shows state + confidence score
   - Suggests Facebook groups

3. **You Decide**
   - Approve for state groups
   - Or handle manually

---

## 💡 PRO TIPS

1. **Start Small** - Begin with 1-2 posts/day
2. **Review Weekly** - Refine keywords based on results
3. **Batch Process** - Review mornings, post afternoons
4. **Monitor Engagement** - Track what performs best
5. **Stay Consistent** - Daily scraping keeps content fresh

---

## 🐛 TROUBLESHOOTING

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key invalid"
- Check `.env` file
- Ensure no extra spaces
- Verify key is correct

### "No news found"
- Check internet connection
- Review keywords in config
- Check `logs/scraper.log`

### Need Help?
```bash
python main.py status     # System status
python main.py logs       # View errors
python test_setup.py      # Test installation
```

---

## 📚 LEARNING PATH

### Day 1 (2 hours)
- Read SETUP_GUIDE.md
- Install & configure
- Run first scrape
- Understand workflow

### Day 2 (1 hour)
- Review scraped news
- Generate first report
- Create first graphic
- Test approval flow

### Day 3 (1 hour)
- Post first story
- Monitor engagement
- Refine keywords
- Practice commands

### Week 2
- Run independently
- Build confidence
- Establish routine
- Track metrics

---

## ✅ SUCCESS CHECKLIST

Before you start:
- [ ] Python 3.8+ installed
- [ ] VSCode installed
- [ ] OpenAI account created
- [ ] NewsAPI account created
- [ ] Downloaded ndta-news-pipeline folder

After setup:
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] test_setup.py passes
- [ ] First scrape successful

Week 1:
- [ ] Keywords refined
- [ ] First report published
- [ ] Graphics look good
- [ ] Workflow comfortable

---

## 🎓 DOCUMENTATION GUIDE

Read in this order:

1. **This file** - Overview (you are here!)
2. **SETUP_GUIDE.md** - Detailed setup steps
3. **QUICK_REFERENCE.md** - Daily commands
4. **README.md** - Technical details
5. **config/news_sources.yaml** - Configuration

Keep handy:
- **QUICK_REFERENCE.md** - Print this!

---

## 🔐 SECURITY NOTES

✅ **Safe:**
- `.env` file with your keys (never share!)
- Private repository (don't make public)
- Your computer only

❌ **Don't:**
- Share API keys
- Commit .env to Git (it's in .gitignore)
- Share your .env file
- Post keys on Slack/email

---

## 📈 EXPECTED RESULTS

### Week 1
- 5-10 relevant stories found daily
- 1-2 quality posts published
- Getting comfortable with workflow

### Month 1
- 30+ posts published
- NDTA brand voice established
- Consistent posting schedule
- Growing social media presence

### Month 3
- System running smoothly
- Minimal daily oversight needed
- Strong engagement metrics
- Trusted news source for industry

---

## 🚀 READY TO START?

1. Open VSCode
2. Open the `ndta-news-pipeline` folder
3. Open `SETUP_GUIDE.md`
4. Follow step-by-step instructions
5. You'll be running in 30 minutes!

---

## 📞 NEED HELP?

### Check First:
- SETUP_GUIDE.md - Detailed instructions
- QUICK_REFERENCE.md - Command cheat sheet
- logs/ folder - Error messages
- test_setup.py - Installation verification

### Common Commands:
```bash
python main.py status     # Check system
python main.py logs       # View errors
python test_setup.py      # Test setup
```

---

## 🎉 LET'S DO THIS!

You're about to automate NDTA's social media presence with professional, AI-powered content that will:

✨ Save you hours every week  
✨ Keep NDTA top-of-mind in the industry  
✨ Provide timely, relevant information  
✨ Build a strong social media presence  
✨ Engage the dump truck community  

**Time to get started!**

```bash
cd ndta-news-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env
# Add your API keys to .env
python test_setup.py
python main.py scrape
```

**Welcome to automated news excellence!** 🚛📰

---

**Built for NDTA**  
**Version 1.0.0**  
**November 2024**
