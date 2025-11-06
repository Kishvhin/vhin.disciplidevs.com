# 🔒 Article Verification System

## Overview

The NDTA News Pipeline now includes a comprehensive **multi-layer verification system** to ensure all scraped articles are legitimate, accurate, and from trusted sources before being processed and shared.

---

## 🛡️ Verification Layers

### **Layer 1: Source Verification**
Checks if the article comes from a trusted, reputable news source.

**Trusted Sources Include:**
- ✅ **Engineering News-Record (ENR)** - Trust Score: 10/10
- ✅ **Construction Dive** - Trust Score: 10/10
- ✅ **Equipment World** - Trust Score: 9/10
- ✅ **For Construction Pros** - Trust Score: 9/10
- ✅ **Reuters, AP, Bloomberg, WSJ** - Trust Score: 9-10/10
- ✅ **Trucking Info, Fleet Owner, CCJ** - Trust Score: 9/10

**What It Checks:**
- Domain verification
- Source reputation in construction/trucking industry
- Trust score (1-10)

---

### **Layer 2: Content Quality Check**
Analyzes the article content for quality and red flags.

**Quality Checks:**
- ✅ **Red Flag Detection** - Scans for clickbait phrases like:
  - "Click here now"
  - "You won't believe"
  - "One weird trick"
  - "Doctors hate this"
  - etc.

- ✅ **Article Freshness** - Checks publication date
  - Articles up to 30 days old are considered recent
  - Older articles receive lower quality scores

- ✅ **Content Length** - Ensures sufficient content
  - Minimum 100 characters in summary
  - Checks for required fields (title, URL, summary, source)

- ✅ **Quality Score** - Overall content quality (1-10)

---

### **Layer 3: AI Fact-Checking**
Uses OpenAI GPT-3.5 to verify factual accuracy and detect misinformation.

**AI Checks:**
- ✅ **Factual Accuracy** - Does it make verifiable claims?
- ✅ **Credibility** - Does it cite sources or provide evidence?
- ✅ **Bias Detection** - Is it objective or promotional?
- ✅ **Misinformation Risk** - LOW / MEDIUM / HIGH
- ✅ **Concerns** - Lists any specific concerns found

**AI Recommendation:**
- `APPROVE` - High confidence, factual, credible
- `REVIEW` - Needs manual verification
- `REJECT` - High misinformation risk or low credibility

---

## 📊 Overall Verification Score

The system calculates an **Overall Verification Score (1-10)** based on:

```
Overall Score = (Source Trust × 40%) + (Quality Score × 30%) + (Credibility × 30%)
```

### **Score Interpretation:**

| Score | Recommendation | Action |
|-------|---------------|--------|
| **8-10** | AUTO_APPROVE | Automatically approved if relevance ≥ 8 |
| **6-7.9** | MANUAL_REVIEW | Requires human review |
| **0-5.9** | REJECT | Automatically rejected |

---

## 🎯 How It Works in the Pipeline

### **During Scraping:**

1. **Article is scraped** from RSS feed
2. **Source verification** runs immediately
3. **Quality check** analyzes content
4. **AI fact-checking** verifies accuracy (for trusted sources only)
5. **Overall score** is calculated
6. **Status is set:**
   - `auto_approved` - High score + high relevance
   - `pending_review` - Medium score or lower relevance
   - `rejected` - Failed verification

### **In the Web Dashboard:**

Articles display a **Verification Report** showing:
- ✅ Overall verification score
- ✅ Source name and trust level
- ✅ Quality score
- ✅ Article age
- ✅ Credibility score
- ✅ Misinformation risk level
- ✅ AI recommendation
- ⚠️ Any concerns found

### **In Command Line Review:**

```
🔒 VERIFICATION:
   Overall Score: 9.2/10
   Source: ✓ Engineering News-Record (Trusted - 10/10)
   Credibility: 9/10
   Misinformation Risk: LOW
   Recommendation: AUTO_APPROVE

📊 RELEVANCE:
   Score: 8/10
   Reason: Directly relevant to dump truck operations
```

---

## 🚨 Red Flags Detected

The system automatically flags articles containing:

- Clickbait language
- Promotional content
- Unverified sources
- Missing citations
- High bias levels
- Outdated information (>30 days)
- Insufficient content
- Missing required fields

---

## 💡 Benefits

### **For NDTA:**
✅ **Protects Reputation** - Only share verified, accurate information  
✅ **Saves Time** - Auto-rejects low-quality content  
✅ **Builds Trust** - Members know content is fact-checked  
✅ **Reduces Risk** - Avoids spreading misinformation  

### **For You:**
✅ **Confidence** - Know every article is verified  
✅ **Transparency** - See exactly why articles pass/fail  
✅ **Control** - Manual review for borderline cases  
✅ **Efficiency** - High-quality articles auto-approved  

---

## 📈 Verification Statistics

After each scrape, you'll see:

```
✅ Verification Summary:
   Total Articles: 10
   Auto-Approved: 5 (50%)
   Pending Review: 3 (30%)
   Rejected: 2 (20%)
   
   Average Verification Score: 8.2/10
   Trusted Sources: 8 (80%)
   Misinformation Risk: LOW
```

---

## 🔧 Configuration

### **Adding Trusted Sources:**

Edit `scrapers/verification.py`:

```python
TRUSTED_SOURCES = {
    'yoursource.com': {'name': 'Your Source', 'trust_score': 9},
}
```

### **Adjusting Red Flags:**

Edit `scrapers/verification.py`:

```python
RED_FLAGS = [
    'your custom red flag',
    'another phrase to avoid',
]
```

### **Changing Score Thresholds:**

Edit `scrapers/verification.py` in the `comprehensive_verification` method:

```python
if overall_score >= 8:  # Change threshold here
    final_recommendation = 'auto_approve'
```

---

## 🎓 Best Practices

1. **Review Borderline Cases** - Always manually review articles with scores 6-7.9
2. **Check Concerns** - Pay attention to AI-flagged concerns
3. **Verify Unfamiliar Sources** - Research new sources before trusting
4. **Update Trusted List** - Add reputable sources as you discover them
5. **Monitor Rejections** - Periodically review rejected articles to ensure system accuracy

---

## 📞 Support

If you notice:
- ❌ Legitimate articles being rejected
- ❌ Low-quality articles passing through
- ❌ Incorrect verification scores

**Action:** Review the verification settings and adjust thresholds as needed.

---

## 🎉 Summary

Your NDTA News Pipeline now has **enterprise-grade verification** ensuring:

✅ Only trusted sources  
✅ Factually accurate content  
✅ No clickbait or misinformation  
✅ Fresh, relevant news  
✅ Professional credibility  

**You can confidently share NDTA content knowing it's been thoroughly verified!** 🔒✨

