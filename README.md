# NDTA News Pipeline 🚛📰

**Automated news monitoring, AI-powered content generation, and social media distribution for the National Dump Track Association**

---

## 🎯 What This Does

This system automatically:
1. **Scrapes** 50+ news sources for dump truck industry news
2. **Filters** using AI to find only relevant stories (must affect dump truck industry)
3. **Generates** professional NDTA-branded news reports
4. **Creates** social media graphics with your branding
5. **Detects** state-specific news and alerts you
6. **Manages** approval workflow (you + Dee Jay)
7. **Distributes** to Twitter, Facebook, and state groups

---

## ⚡ Quick Start

### 1. Install
```bash
cd ndta-news-pipeline
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
# Copy template and add your API keys
cp .env.template .env
# Edit .env with your keys
```

### 3. Run
```bash
python main.py scrape      # Find news
python main.py review      # Review & approve
python main.py generate    # Create NDTA reports
python main.py graphics    # Make graphics
python main.py approve     # Final approval
python main.py post        # Publish to social media
```

**Total time: 15-20 minutes per day**

### 4. Deploy to Cloud (Optional)

For remote access and client demos:

```bash
# See QUICK_START.md for full instructions
# Deploy to Render.com in 15 minutes
# Free tier available - $0/month
```

**Your client can access from anywhere:** `https://ndta-news-pipeline.onrender.com`

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete step-by-step setup (START HERE!)
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Daily commands cheat sheet
- **[config/news_sources.yaml](config/news_sources.yaml)** - Configure keywords & sources

---

## 🔑 Required API Keys

1. **OpenAI** (required) - AI content generation
   - Get at: https://platform.openai.com/
   - Cost: ~$1-2/day

2. **NewsAPI** (required) - News scraping
   - Get at: https://newsapi.org/
   - Cost: Free tier works fine

3. **Twitter API** (optional) - Auto-posting
   - Get at: https://developer.twitter.com/

4. **Facebook API** (optional) - Auto-posting
   - Get at: https://developers.facebook.com/

---

## 📁 Project Structure

```
ndta-news-pipeline/
├── main.py                    # Main control script
├── requirements.txt           # Dependencies
├── .env                      # API keys (you create this)
│
├── config/                   # Configuration
│   └── news_sources.yaml    # Keywords, sources, settings
│
├── scrapers/                 # News scraping
│   ├── news_scraper.py
│   ├── rss_scraper.py
│   └── web_scraper.py
│
├── content_generator/        # AI content creation
│   ├── report_generator.py
│   ├── headline_generator.py
│   └── state_detector.py
│
├── graphics/                 # Graphic creation
│   ├── graphic_generator.py
│   └── templates/
│
├── distribution/             # Social media posting
│   ├── approval_manager.py
│   ├── twitter_poster.py
│   └── facebook_poster.py
│
├── data/                     # Generated data
│   ├── raw_news/            # Scraped articles
│   ├── processed_news/      # NDTA reports
│   ├── graphics/            # Social media images
│   └── approved_content/    # Ready to post
│
└── logs/                     # System logs
```

---

## 🔄 Daily Workflow

### Morning (10 minutes)
```bash
python main.py scrape    # Scrape news (automatic)
python main.py review    # Review articles (you decide)
```

### Afternoon (5 minutes)
```bash
python main.py generate  # AI creates reports (automatic)
python main.py graphics  # Creates graphics (automatic)
python main.py approve   # You approve (you decide)
python main.py post      # Posts to social (automatic)
```

---

## 🎨 Customization

### Change Keywords
Edit `config/news_sources.yaml`:
```yaml
primary_keywords:
  - "dump truck"
  - "your keyword here"
```

### Modify NDTA Voice
Edit `content_generator/prompts.py`:
```python
TONE = "professional yet accessible"
AUDIENCE = "dump truck business owners"
```

### Update Branding
Replace files in `graphics/templates/`:
- `ndta_logo.png` - Your logo
- Update colors in `config/news_sources.yaml`

---

## 🚨 State-Specific Alerts

When state-specific news is detected:

1. You receive an email alert
2. Run: `python main.py state-alerts`
3. Review state and suggested Facebook groups
4. Approve for state group posting

Example states detected:
- Georgia passes new dump truck regulations
- California announces emission standards
- Texas infrastructure project

---

## 📊 What Success Looks Like

### Week 1
- ✅ System running smoothly
- ✅ Finding 5-10 relevant stories/day
- ✅ Quality NDTA reports generated
- ✅ Professional graphics created

### Month 1
- ✅ 30+ quality posts published
- ✅ NDTA brand voice established
- ✅ Audience engagement growing
- ✅ State-specific content distributed

---

## 🐛 Troubleshooting

### "No module named X"
```bash
pip install -r requirements.txt
```

### "API key invalid"
Check `.env` file - ensure no extra spaces around keys

### "No news found"
- Check internet connection
- Verify keywords in config
- Check `logs/scraper.log`

### "AI generation failed"
- Verify OpenAI API key
- Check account has credits
- View `logs/generator.log`

---

## 🔒 Security

- ✅ API keys in `.env` (never commit to Git)
- ✅ `.env` in `.gitignore`
- ✅ Only scrape public data
- ✅ Respect social media Terms of Service
- ✅ Follow copyright laws

---

## 📈 Analytics & Reporting

View system metrics:
```bash
python main.py status      # Current status
python main.py stats       # Usage statistics
python main.py dashboard   # Web dashboard (coming soon)
```

---

## 🛠️ Advanced Features

### Automated Scheduling
Set up cron job (Mac/Linux) or Task Scheduler (Windows) to run:
```bash
# Daily at 6 AM
0 6 * * * cd /path/to/ndta-news-pipeline && python main.py scrape
```

### Batch Processing
```bash
python main.py scrape --days 7    # Scrape last 7 days
python main.py generate --all     # Process all pending
```

### Testing
```bash
python main.py test               # Run test suite
python test_setup.py              # Verify installation
```

---

## 📞 Support

### Check Logs
```bash
python main.py logs               # View recent errors
cat logs/scraper.log             # Detailed scraper logs
```

### Test Components
```bash
python scrapers/news_scraper.py   # Test scraper only
python content_generator/report_generator.py  # Test AI
```

### Debug Mode
```bash
python main.py scrape --debug     # Verbose output
```

---

## 🎓 Training Resources

1. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup walkthrough
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Daily commands
3. **config/** - Commented configuration files
4. **logs/** - System logs for troubleshooting

---

## 📝 TODO / Roadmap

- [ ] Web dashboard for monitoring
- [ ] Sentiment analysis on industry news
- [ ] Automated A/B headline testing
- [ ] LinkedIn integration
- [ ] Email newsletter generation
- [ ] Analytics reporting
- [ ] Mobile app for approvals

---

## ⚖️ Legal & Compliance

- Only scrapes publicly available data
- Respects robots.txt and API rate limits
- Follows social media Terms of Service
- Complies with copyright laws
- NDTA retains rights to generated content

---

## 🤝 Contributing

To modify or enhance:

1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Document changes
5. Submit for review

---

## 📜 License

Proprietary - National Dump Track Association (NDTA)
© 2024 NDTA. All rights reserved.

---

## 🎉 Get Started Now!

```bash
# 1. Read the setup guide
cat SETUP_GUIDE.md

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.template .env
# Edit .env with your keys

# 4. Run first scrape
python main.py scrape

# 5. You're live! 🚀
```

---

**Built for NDTA by [Your Name/Company]**
**Last Updated: November 2024**
**Version: 1.0.0**

For questions or support, contact: [your-email@ndta.com]