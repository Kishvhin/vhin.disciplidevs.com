# 🚀 NDTA News Pipeline - Cloud Deployment Guide

## ✅ Deploy to Render.com in 15 Minutes

This guide will help you deploy your NDTA News Pipeline to the cloud so your client can access it from anywhere.

---

## 📋 **What You'll Need**

1. ✅ GitHub account (free)
2. ✅ Render.com account (free)
3. ✅ Your API keys (OpenAI, Reddit, etc.)
4. ✅ 15 minutes of time

---

## 🎯 **Step 1: Create GitHub Repository (5 minutes)**

### **1.1: Create a GitHub account**
- Go to https://github.com/signup
- Create a free account (if you don't have one)

### **1.2: Create a new repository**
1. Go to https://github.com/new
2. Repository name: `ndta-news-pipeline`
3. Description: `NDTA News Pipeline - Automated dump truck industry news`
4. Select: **Private** (keep your code private)
5. Click **"Create repository"**

### **1.3: Push your code to GitHub**

Open your terminal in the project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - NDTA News Pipeline"

# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ndta-news-pipeline.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Enter your GitHub username and password when prompted.**

---

## 🌐 **Step 2: Deploy to Render.com (10 minutes)**

### **2.1: Create Render.com account**
1. Go to https://render.com/
2. Click **"Get Started"**
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your GitHub

### **2.2: Create a new Web Service**
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if needed
   - Find `ndta-news-pipeline` repository
   - Click **"Connect"**

### **2.3: Configure the Web Service**

**Basic Settings:**
- **Name:** `ndta-news-pipeline`
- **Region:** Oregon (US West) - Free tier
- **Branch:** `main`
- **Root Directory:** (leave blank)
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python web_dashboard.py`

**Instance Type:**
- Select **"Free"** (Free tier - $0/month)

### **2.4: Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables one by one:

```
OPENAI_API_KEY = your_openai_key_here
REDDIT_CLIENT_ID = SR5KIWa3FopHYJGioEF09g
REDDIT_CLIENT_SECRET = 1-tqr56wJ7vNfOutuSizfBIy1pwqzQ
REDDIT_USER_AGENT = NDTA News Pipeline v1.0
FLASK_ENV = production
PORT = 5000
```

**Optional (if you have them):**
```
NEWSAPI_KEY = your_newsapi_key_here
TWITTER_API_KEY = your_twitter_key_here
TWITTER_API_SECRET = your_twitter_secret_here
TWITTER_ACCESS_TOKEN = your_twitter_token_here
TWITTER_ACCESS_SECRET = your_twitter_access_secret_here
FACEBOOK_ACCESS_TOKEN = your_facebook_token_here
FACEBOOK_PAGE_ID = your_facebook_page_id_here
```

### **2.5: Deploy!**

1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Watch the build logs (you'll see it installing dependencies)

---

## 🎉 **Step 3: Access Your Dashboard**

### **3.1: Get your URL**

Once deployed, Render will give you a URL like:
```
https://ndta-news-pipeline.onrender.com
```

### **3.2: Test it**

1. Open the URL in your browser
2. You should see the NDTA News Pipeline dashboard
3. Click **"Run Full Automated Workflow"** to test

### **3.3: Share with your client**

Send your client the URL:
```
https://ndta-news-pipeline.onrender.com
```

They can:
- ✅ View the dashboard
- ✅ See scraped articles
- ✅ Run the workflow
- ✅ View reports and graphics
- ✅ Access from anywhere in the world

---

## 🔧 **Troubleshooting**

### **Problem: Build fails**

**Solution:** Check the build logs for errors. Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors in code

### **Problem: App crashes on startup**

**Solution:** Check the logs. Common issues:
- Missing environment variables
- Port configuration issues
- Database connection errors

### **Problem: "This site can't be reached"**

**Solution:**
- Wait 1-2 minutes after deployment
- Check if the service is running in Render dashboard
- Check the logs for errors

### **Problem: Free tier sleeps after 15 minutes**

**Solution:**
- Free tier apps sleep after 15 minutes of inactivity
- They wake up when someone visits (takes 30-60 seconds)
- Upgrade to paid tier ($7/month) for always-on

---

## 💡 **Tips for Success**

### **1. Keep your .env file LOCAL**
- ✅ Never commit `.env` to GitHub
- ✅ It's already in `.gitignore`
- ✅ Add secrets in Render dashboard instead

### **2. Monitor your app**
- Check Render dashboard for logs
- Set up email alerts for crashes
- Monitor usage and performance

### **3. Update your app**
- Push changes to GitHub: `git push`
- Render auto-deploys on every push
- Check deployment logs to confirm success

### **4. Free tier limitations**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Sleeps after 15 min inactivity
- ✅ 512 MB RAM
- ✅ Shared CPU
- ⚠️ Wakes up in 30-60 seconds when accessed

---

## 🎯 **Quick Reference**

### **Your URLs:**
- **Dashboard:** https://ndta-news-pipeline.onrender.com
- **GitHub Repo:** https://github.com/YOUR_USERNAME/ndta-news-pipeline
- **Render Dashboard:** https://dashboard.render.com/

### **Useful Commands:**

**Update your app:**
```bash
git add .
git commit -m "Update description"
git push
```

**View logs:**
- Go to Render dashboard
- Click on your service
- Click "Logs" tab

**Restart service:**
- Go to Render dashboard
- Click "Manual Deploy" → "Clear build cache & deploy"

---

## 📊 **What Your Client Will See**

### **Dashboard Features:**
1. ✅ **Automated Workflow** - Run full pipeline with one click
2. ✅ **View Articles** - See all scraped articles
3. ✅ **View Reports** - See generated NDTA reports
4. ✅ **View Graphics** - See created social media graphics
5. ✅ **Statistics** - Real-time stats on articles, reports, etc.

### **Manual Controls:**
1. ✅ **Run Scrape** - Scrape news manually
2. ✅ **Generate Reports** - Generate reports manually
3. ✅ **Create Graphics** - Create graphics manually
4. ✅ **View Workflow** - See pipeline status

---

## 🎊 **Success Checklist**

Before sharing with your client, verify:

- [ ] App is deployed and running
- [ ] Dashboard loads without errors
- [ ] Can run automated workflow
- [ ] Articles are being scraped
- [ ] Reports are being generated
- [ ] Graphics are being created
- [ ] Reddit API is working (check for Reddit posts)
- [ ] No sensitive data exposed (API keys hidden)
- [ ] URL is professional and shareable

---

## 🚀 **Next Steps After Deployment**

### **1. Custom Domain (Optional)**
- Buy a domain (e.g., `ndta-pipeline.com`)
- Point it to your Render app
- Makes it more professional

### **2. Upgrade to Paid Tier (Optional)**
- $7/month for always-on
- No sleep after inactivity
- Better performance
- More RAM and CPU

### **3. Set Up Monitoring**
- Enable email alerts in Render
- Monitor uptime and performance
- Track usage and costs

### **4. Add Authentication (Optional)**
- Add login page
- Protect dashboard with password
- Only authorized users can access

---

## 📞 **Support**

### **Render.com Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com/
- Status: https://status.render.com/

### **GitHub Support:**
- Docs: https://docs.github.com/
- Community: https://github.community/

---

## 🎉 **You're Done!**

Your NDTA News Pipeline is now:
- ✅ Deployed to the cloud
- ✅ Accessible from anywhere
- ✅ Running 24/7 (with free tier sleep)
- ✅ Using official Reddit API
- ✅ Ready for your client to use

**Share this URL with your client:**
```
https://ndta-news-pipeline.onrender.com
```

**They can access it from any device, anywhere in the world!** 🌍

---

*Deployment completed: Ready to go live!*
*Estimated time: 15 minutes*
*Cost: $0/month (free tier)*

