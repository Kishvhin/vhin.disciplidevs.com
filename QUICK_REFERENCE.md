# NDTA NEWS PIPELINE - QUICK REFERENCE CARD
## Keep this handy! 📋

---

## ⚡ DAILY COMMANDS (In Order)

```bash
# 1. Scrape for news (5-10 min)
python main.py scrape

# 2. Review what was found (2-3 min)
python main.py review

# 3. Generate NDTA reports (automatic)
python main.py generate

# 4. Create graphics (automatic)
python main.py graphics

# 5. Approve content (5 min)
python main.py approve

# 6. Check state-specific news
python main.py state-alerts

# 7. Post approved content (automatic)
python main.py post
```

**Total time: ~15-20 minutes per day**

---

## 🔧 USEFUL COMMANDS

```bash
# Check system status
python main.py status

# View logs
python main.py logs

# Test API connections
python test_setup.py

# See pending approvals
python main.py pending

# View today's posts
python main.py today

# Backup everything
python main.py backup

# View help
python main.py --help
```

---

## 📊 UNDERSTANDING OUTPUT

### Relevance Scores:
- **9-10**: Perfect match - dump truck industry directly affected
- **7-8**: Highly relevant - trucking/logistics with dump truck impact
- **5-6**: Moderately relevant - general trucking news
- **Below 5**: Not relevant - skip

### State Detection:
- ✅ **State Found**: Shows state + suggested groups
- ⚠️ **Multi-State**: Regional/national story
- ❌ **No State**: General industry news

---

## 🎯 QUICK DECISIONS

### During Review:
- **y** = Yes, process this story
- **n** = No, skip it
- **s** = State-specific, alert me
- **q** = Quit review

### During Approval:
- **approve** = Ready to post
- **edit** = Make changes
- **reject** = Discard
- **schedule** = Post later

---

## 🚨 QUICK FIXES

### "No news found"
```bash
# Check keywords
code config/news_sources.yaml
```

### "AI error"
```bash
# Check API key
code .env
# Verify OpenAI credits
```

### "Graphic failed"
```bash
# Check logo exists
ls graphics/templates/
```

### "Can't post"
```bash
# Test social media connection
python main.py test-social
```

---

## 📁 KEY FILES

```
.env                          # Your API keys
config/news_sources.yaml     # Keywords & sources
data/raw_news/               # Scraped articles
data/processed_news/         # NDTA reports
data/graphics/               # Social media images
data/approved_content/       # Ready to post
logs/                        # Error logs
```

---

## ⏰ RECOMMENDED SCHEDULE

### Morning (6 AM):
- Auto-scrape runs

### Mid-Morning (9 AM):
- Review scraped news (5 min)
- Generate reports (automatic)
- Create graphics (automatic)

### Lunchtime (12 PM):
- Approve content (5 min)

### Afternoon (2 PM):
- Post approved content (automatic)

**Total active time: ~10 minutes**

---

## 💡 PRO TIPS

1. **Check email alerts** for state-specific news
2. **Review graphics** before approving
3. **Refine keywords** weekly based on results
4. **Monitor engagement** to see what works
5. **Backup weekly**: `python main.py backup`

---

## 🎨 CUSTOMIZATION

### Change Keywords:
```bash
code config/news_sources.yaml
```

### Adjust Report Style:
```bash
code content_generator/prompts.py
```

### Modify Graphics:
```bash
code graphics/templates/
```

### Change Posting Schedule:
```bash
code config/schedule.yaml
```

---

## 📞 EMERGENCY

### System won't start:
1. Activate virtual environment
2. Check logs: `python main.py logs`
3. Test setup: `python test_setup.py`

### Bad content posted:
```bash
python main.py delete --post-id [ID]
```

### Out of API credits:
1. Check OpenAI dashboard
2. Add credits
3. Update billing

---

## 📈 METRICS TO TRACK

Weekly review:
- Stories scraped: ___
- Stories posted: ___
- State-specific alerts: ___
- Engagement rate: ___
- Best performing topic: ___

---

## ✅ DAILY CHECKLIST

Morning:
- [ ] Check if scrape ran successfully
- [ ] Review email alerts for state news

Mid-Day:
- [ ] Review scraped articles
- [ ] Approve/reject reports & graphics

Afternoon:
- [ ] Verify posts went live
- [ ] Check engagement

End of Day:
- [ ] Quick review of metrics
- [ ] Note any issues for tomorrow

---

## 🔑 KEY CONTACTS

- **Technical Issues**: [Your email]
- **Content Approval**: You + Dee Jay
- **API Support**: Check status.openai.com

---

## 📚 QUICK LINKS

- [Full Setup Guide](SETUP_GUIDE.md)
- [Troubleshooting](SETUP_GUIDE.md#part-6-troubleshooting)
- [OpenAI Dashboard](https://platform.openai.com/)
- [NewsAPI Dashboard](https://newsapi.org/account)

---

**Print this page and keep it at your desk!** 📄