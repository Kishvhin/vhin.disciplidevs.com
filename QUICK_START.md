# 🚀 QUICK START - Deploy in 15 Minutes

## ⚡ **Super Fast Deployment Guide**

Your client needs remote access TODAY. Here's the fastest way:

---

## 📋 **What You Need**

1. GitHub account (create at https://github.com/signup)
2. Render.com account (create at https://render.com/)
3. Your API keys ready

---

## 🎯 **Step 1: Push to GitHub (5 minutes)**

### **Open terminal in this folder and run:**

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "NDTA News Pipeline - Initial deployment"

# Create GitHub repo at: https://github.com/new
# Name it: ndta-news-pipeline
# Make it PRIVATE
# Then run (replace YOUR_USERNAME):

git remote add origin https://github.com/YOUR_USERNAME/ndta-news-pipeline.git
git branch -M main
git push -u origin main
```

**Enter your GitHub username and password when asked.**

---

## 🌐 **Step 2: Deploy to Render (10 minutes)**

### **2.1: Sign up**
1. Go to https://render.com/
2. Click "Get Started"
3. Sign up with GitHub (easiest!)

### **2.2: Create Web Service**
1. Click "New +" → "Web Service"
2. Connect your `ndta-news-pipeline` repository
3. Click "Connect"

### **2.3: Configure**

**Settings:**
- Name: `ndta-news-pipeline`
- Region: Oregon (US West)
- Branch: `main`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python web_dashboard.py`
- Instance Type: **Free**

**Environment Variables (click "Advanced"):**

```
OPENAI_API_KEY = sk-proj-...your key...
REDDIT_CLIENT_ID = SR5KIWa3FopHYJGioEF09g
REDDIT_CLIENT_SECRET = 1-tqr56wJ7vNfOutuSizfBIy1pwqzQ
REDDIT_USER_AGENT = NDTA News Pipeline v1.0
FLASK_ENV = production
```

### **2.4: Deploy**
1. Click "Create Web Service"
2. Wait 5-10 minutes
3. Watch the build logs

---

## 🎉 **Step 3: Share with Client**

### **Your URL will be:**
```
https://ndta-news-pipeline.onrender.com
```

### **Send this to your client:**

```
Hi [Client Name],

Your NDTA News Pipeline is now live!

Dashboard: https://ndta-news-pipeline.onrender.com

You can:
✅ View all scraped articles
✅ Run the automated workflow
✅ See generated reports
✅ View social media graphics
✅ Access from anywhere, anytime

The Reddit scraper is using the official Reddit API and working perfectly!

Note: The free tier may sleep after 15 minutes of inactivity. 
It will wake up automatically when you visit (takes 30-60 seconds).

Let me know if you have any questions!
```

---

## ⚠️ **Important Notes**

### **Free Tier Limitations:**
- ✅ Free forever
- ✅ 750 hours/month (enough for 24/7)
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Takes 30-60 sec to wake up
- ✅ Perfect for demos and testing

### **Upgrade to Paid ($7/month) for:**
- ✅ Always-on (no sleep)
- ✅ Faster performance
- ✅ More RAM and CPU
- ✅ Better for production use

---

## 🔧 **Troubleshooting**

### **"This site can't be reached"**
- Wait 1-2 minutes after deployment
- Check Render dashboard for errors
- Check build logs

### **App crashes**
- Check environment variables are set
- Check logs in Render dashboard
- Make sure all API keys are correct

### **Free tier sleeping**
- Normal behavior after 15 min
- Wakes up when someone visits
- Upgrade to $7/month for always-on

---

## 📊 **What Your Client Will See**

### **Dashboard:**
- 📊 Statistics (articles, reports, graphics)
- 🚀 Automated Workflow button
- 📰 View Articles
- 📝 View Reports
- 🎨 View Graphics

### **Features:**
- ✅ Reddit scraping (official API)
- ✅ RSS feed scraping
- ✅ State DOT scraping
- ✅ AI-powered report generation
- ✅ Social media graphics
- ✅ Auto-approval system

---

## 🎯 **Quick Commands**

### **Update your app:**
```bash
git add .
git commit -m "Update"
git push
```
(Render auto-deploys on push!)

### **View logs:**
- Go to Render dashboard
- Click your service
- Click "Logs"

### **Restart:**
- Render dashboard
- "Manual Deploy" → "Deploy"

---

## ✅ **Checklist Before Sharing**

- [ ] App deployed successfully
- [ ] Dashboard loads
- [ ] Can run automated workflow
- [ ] Reddit posts are showing up
- [ ] Reports are generating
- [ ] Graphics are creating
- [ ] URL is working
- [ ] Client email is ready

---

## 🚀 **You're Ready!**

**Time to deploy:** 15 minutes  
**Cost:** $0/month (free tier)  
**Client access:** Worldwide, 24/7  
**Your URL:** https://ndta-news-pipeline.onrender.com

**Deploy now and share with your client today!** 🎉

---

*Need help? Check DEPLOYMENT_GUIDE.md for detailed instructions.*

