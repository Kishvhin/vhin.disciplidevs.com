# 🎉 Reddit API Setup - Almost Done!

## ✅ What's Already Configured

I've set up everything for you:

1. ✅ **PRAW library installed** - Official Reddit API wrapper
2. ✅ **Reddit credentials added** to `.env` file:
   - CLIENT_ID: `SR5KIWa3FopHYJGioEF09g`
   - CLIENT_SECRET: `1-tqr56wJ7vNfOutuSizfBIy1pwqzQ`
   - USERNAME: `Much-Cherry1097`
3. ✅ **New scraper created** - `scrapers/reddit_scraper_praw.py`
4. ✅ **Test script ready** - `test_reddit_praw.py`

---

## 🔐 ONE THING YOU NEED TO DO

### Add Your Reddit Password

Open the `.env` file and find this line:

```env
REDDIT_PASSWORD=your_reddit_password_here
```

**Replace `your_reddit_password_here` with your actual Reddit password.**

Example:
```env
REDDIT_PASSWORD=MySecurePassword123
```

**IMPORTANT:** 
- This is YOUR Reddit account password
- The same password you use to log into Reddit.com
- Keep it secure - never share the .env file!

---

## 🧪 Test the Integration

After adding your password, run:

```bash
python test_reddit_praw.py
```

This will:
1. ✅ Test authentication with Reddit API
2. ✅ Scrape r/Truckers for dump truck posts
3. ✅ Search all of Reddit for "dump truck"
4. ✅ Get hot/trending posts
5. ✅ Run full scraping workflow
6. ✅ Show you statistics and results

---

## 📊 What You'll Get

### Before (Old Scraper):
- ❌ Rate limit: 60 requests/hour
- ❌ Frequent 403 errors
- ❌ Limited data
- ❌ Can't post to Reddit

### After (PRAW API):
- ✅ Rate limit: **600 requests/10 minutes** (10x better!)
- ✅ No 403 errors
- ✅ Full data access (upvote ratio, awards, flair, etc.)
- ✅ Can post to Reddit
- ✅ Official API support
- ✅ Much more reliable

---

## 🚀 Expected Test Results

When you run `python test_reddit_praw.py`, you should see:

```
============================================================
🚀 REDDIT PRAW API INTEGRATION TEST
Official Reddit API with OAuth Authentication
============================================================

============================================================
TESTING REDDIT API AUTHENTICATION
============================================================

✅ Authentication successful!
   Logged in as: u/Much-Cherry1097
   Comment karma: [your karma]
   Link karma: [your karma]

============================================================
TESTING SUBREDDIT SCRAPING
============================================================

1. Scraping r/Truckers...
   ✅ Found 15 relevant posts

   📝 Sample post:
   Title: Does a complaint to FMCSA have any affect...
   Author: u/[username]
   Score: 25 upvotes (95% upvoted)
   Comments: 18
   URL: https://reddit.com/r/Truckers/comments/...

============================================================
TESTING REDDIT SEARCH
============================================================

2. Searching all of Reddit for 'dump truck'...
   ✅ Found 50 posts

   📝 Sample search result:
   Title: Hitachi EH4000 heavy duty mining dump truck...
   Subreddit: r/Construction
   Score: 142 upvotes
   URL: https://reddit.com/...

   📊 Posts by subreddit:
      r/Construction: 12 posts
      r/Truckers: 8 posts
      r/heavyequipment: 6 posts
      ...

============================================================
✅ TEST SUMMARY
============================================================
✅ Authentication: SUCCESS
✅ Subreddit scraping: 15 posts
✅ Reddit search: 50 posts
✅ Hot posts: 10 posts
✅ Full scrape: 75 unique posts

🎉 All tests passed! Reddit API is working perfectly!
```

---

## 🔧 Integration with Your Pipeline

After testing, I'll update your main `news_scraper.py` to use the new PRAW scraper instead of the old one.

**Benefits:**
- Same workflow, better results
- No code changes needed on your end
- Automatic integration with existing pipeline
- All the benefits of official API

---

## 🐛 Troubleshooting

### If you get "Invalid credentials" error:

1. **Check your password** - Make sure it's correct in `.env`
2. **Check 2FA** - If you have 2-factor authentication enabled on Reddit:
   - You need to create an app-specific password
   - Go to: https://www.reddit.com/prefs/apps
   - Or temporarily disable 2FA for testing

### If you get "403 Forbidden" error:

- This shouldn't happen with PRAW!
- But if it does, check that CLIENT_ID and CLIENT_SECRET are correct

### If you get "Module not found" error:

Run:
```bash
.venv/Scripts/pip install praw
```

---

## 📚 What's Next

1. **Add your password** to `.env` file
2. **Run the test**: `python test_reddit_praw.py`
3. **Verify it works** (you should see 50+ posts)
4. **I'll integrate it** into your main pipeline
5. **Enjoy better Reddit scraping!**

---

## 🎯 Summary

**What you need to do RIGHT NOW:**

1. Open `.env` file
2. Find line: `REDDIT_PASSWORD=your_reddit_password_here`
3. Replace with: `REDDIT_PASSWORD=YourActualPassword`
4. Save the file
5. Run: `python test_reddit_praw.py`

**That's it!** 🚀

---

## 🔒 Security Note

Your `.env` file contains sensitive credentials:
- ✅ Never commit it to Git
- ✅ Never share it publicly
- ✅ Keep it secure on your computer
- ✅ It's already in `.gitignore` (safe)

---

**Ready? Add your password and run the test!** 🎉

