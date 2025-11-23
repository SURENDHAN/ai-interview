# Railway Deployment Guide

## 🚂 Deploy SURA AI Interview to Railway

This guide will help you deploy your AI Interview Practice platform to Railway.app.

---

## ✅ Prerequisites

- [x] GitHub repository created and pushed
- [x] Railway configuration files added
- [x] Environment variables ready (from `.env`)

---

## 📋 Step-by-Step Deployment

### Step 1: Sign Up for Railway

1. Go to https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with your **GitHub account** (SURENDHAN)
4. Authorize Railway to access your repositories

---

### Step 2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`SURENDHAN/ai-interview`**
4. Railway will automatically detect it's a Python project

---

### Step 3: Configure Environment Variables

Railway needs your API keys. Add these environment variables:

1. In your Railway project, click **"Variables"** tab
2. Click **"+ New Variable"**
3. Add each variable from your `.env` file:

#### Required Variables:

```env
GEMINI_API_KEY=AIzaSyD_7RhGB-H1lDwUwSquj28jqrtgDTkGdF8
FIREBASE_API_KEY=AIzaSyAXwfD-DdrDHkGytxRoGxtjfoHBBKlpuo8
FIREBASE_AUTH_DOMAIN=eightfold-d59a6.firebaseapp.com
FIREBASE_PROJECT_ID=eightfold-d59a6
FIREBASE_STORAGE_BUCKET=eightfold-d59a6.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=212958608666
FIREBASE_APP_ID=1:212958608666:web:ffb4c60a9a8f958d4a80a3
FIREBASE_MEASUREMENT_ID=G-Z282DM1ZYP
```

#### Optional Variables (use defaults if not set):

```env
MODEL_ID=gemini-2.5-flash
WHISPER_MODEL_SIZE=base.en
WHISPER_COMPUTE=int8
VOICE_NAME=en-US-AriaNeural
QUESTIONS_FILE=questions.json
PISTON_API_URL=https://emkc.org/api/v2/piston/execute
HOST=0.0.0.0
```

**Note:** Railway automatically sets `PORT` - don't add it manually!

---

### Step 4: Deploy

1. Click **"Deploy"** button
2. Railway will:
   - ✅ Clone your repository
   - ✅ Install dependencies from `requirements.txt`
   - ✅ Start your FastAPI server
   - ✅ Assign a public URL

**Deployment takes 3-5 minutes** (Whisper model download is large)

---

### Step 5: Get Your URL

1. Once deployed, click **"Settings"** tab
2. Under **"Domains"**, you'll see your Railway URL:
   - Format: `your-app-name.up.railway.app`
   - Example: `ai-interview-production.up.railway.app`

3. Click **"Generate Domain"** if not auto-generated

---

### Step 6: Update Firebase Authorized Domains

Your Railway URL needs to be authorized in Firebase:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **eightfold-d59a6**
3. Go to **Authentication** → **Settings** → **Authorized domains**
4. Click **"Add domain"**
5. Add your Railway URL (without `https://`):
   ```
   your-app-name.up.railway.app
   ```
6. Save

---

### Step 7: Test Your Deployment

1. Open your Railway URL in browser
2. You should see the login page
3. Test the flow:
   - ✅ Login with Google
   - ✅ Upload resume (optional)
   - ✅ Select role
   - ✅ Start interview
   - ✅ Test voice interaction
   - ✅ Try coding challenge

---

## 🔧 Configuration Files Added

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main3:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `Procfile`
```
web: uvicorn main3:app --host 0.0.0.0 --port $PORT
```

### `runtime.txt`
```
3.10.*
```

---

## 📊 Railway Dashboard Overview

### Metrics Tab
- CPU usage
- Memory usage
- Network traffic
- Request logs

### Deployments Tab
- View deployment history
- Rollback to previous versions
- See build logs

### Variables Tab
- Manage environment variables
- Add/edit/delete variables
- Bulk import from `.env`

### Settings Tab
- Custom domain
- Restart policy
- Health checks
- Sleep settings

---

## 💰 Free Tier Limits

Railway gives you **$5 free credit per month**:

- **Estimated usage for your app:**
  - ~$0.01-0.02 per hour when active
  - ~$7-15/month if running 24/7
  - **Free tier covers ~250-500 hours/month**

- **Tips to stay within free tier:**
  - Enable sleep after inactivity (Settings)
  - Use for development/testing only
  - Upgrade to paid when ready for production

---

## 🚀 Custom Domain (Optional)

### Add Your Own Domain

1. Go to **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Enter your domain: `interview.yourdomain.com`
4. Add DNS records (Railway will show you):
   ```
   Type: CNAME
   Name: interview
   Value: your-app.up.railway.app
   ```
5. Wait for DNS propagation (5-30 minutes)

### Update Firebase

Add your custom domain to Firebase authorized domains!

---

## 🔄 Continuous Deployment

Railway automatically redeploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Railway automatically:
# 1. Detects the push
# 2. Rebuilds the app
# 3. Deploys new version
# 4. Zero downtime!
```

---

## 📝 Monitoring & Logs

### View Logs

1. Click **"Deployments"** tab
2. Click on active deployment
3. Click **"View Logs"**
4. See real-time application logs

### Common Log Messages

```
✅ "Loading Whisper (base.en)..." - Model loading
✅ "Ready" - Server started successfully
✅ "Connected" - WebSocket connection established
✅ "User: [text]" - Transcription working
✅ "Generating TTS for: [text]" - Audio generation
```

---

## 🐛 Troubleshooting

### Issue: Deployment Failed

**Check build logs:**
1. Go to Deployments tab
2. Click failed deployment
3. Check error messages

**Common fixes:**
- Verify `requirements.txt` is correct
- Check Python version in `runtime.txt`
- Ensure all files are committed to GitHub

---

### Issue: App Crashes on Start

**Check logs for errors:**
```bash
# Common issues:
- Missing environment variables
- Invalid API keys
- Port binding issues
```

**Solution:**
1. Verify all environment variables are set
2. Check API keys are valid
3. Ensure PORT is not hardcoded

---

### Issue: WebSocket Not Working

**Symptoms:**
- "Reconnecting..." status
- No AI responses

**Solution:**
1. Railway supports WebSockets by default
2. Check firewall/proxy settings
3. Verify URL uses `wss://` (secure WebSocket)

---

### Issue: Slow Cold Starts

**Cause:** Whisper model download on first request

**Solutions:**
1. Keep app awake with health checks
2. Use smaller model: `WHISPER_MODEL_SIZE=tiny.en`
3. Upgrade to paid tier (always-on)

---

### Issue: Out of Memory

**Symptoms:**
- App crashes randomly
- "Out of memory" in logs

**Solutions:**
1. Use smaller Whisper model
2. Upgrade Railway plan (more RAM)
3. Optimize memory usage

---

## 📈 Scaling & Production

### When to Upgrade

Upgrade to paid tier ($5-20/month) when:
- ✅ Ready for production users
- ✅ Need 24/7 uptime
- ✅ Exceeding free credit
- ✅ Need more resources

### Production Checklist

- [ ] Custom domain configured
- [ ] Environment variables secured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Error tracking (Sentry, etc.)
- [ ] Rate limiting configured
- [ ] CORS properly configured

---

## 🔐 Security Best Practices

### Environment Variables
- ✅ Never commit `.env` to GitHub
- ✅ Use Railway's variable management
- ✅ Rotate API keys regularly

### CORS Configuration
Already configured in `main3.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For production**, update to:
```python
allow_origins=[
    "https://your-railway-app.up.railway.app",
    "https://yourdomain.com"
]
```

---

## 📞 Support

### Railway Support
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

### Your App Issues
- GitHub Issues: https://github.com/SURENDHAN/ai-interview/issues
- Check logs in Railway dashboard
- Review troubleshooting section above

---

## ✅ Deployment Checklist

Before deploying:
- [x] Railway configuration files created
- [x] GitHub repository pushed
- [ ] Railway account created
- [ ] Project deployed
- [ ] Environment variables added
- [ ] Firebase authorized domains updated
- [ ] App tested and working
- [ ] Custom domain configured (optional)

---

## 🎉 Success!

Once deployed, your app will be live at:
```
https://your-app-name.up.railway.app
```

Share it with friends, add it to your portfolio, and start practicing interviews! 🚀

---

**Next Steps:**
1. Deploy to Railway (follow steps above)
2. Test thoroughly
3. Share the URL
4. Monitor usage
5. Upgrade when needed

Good luck with your deployment! 🎊
