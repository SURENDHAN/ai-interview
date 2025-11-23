# 🚂 Railway Deployment - Quick Start

## ⚡ Fast Track (5 Minutes)

### 1️⃣ Go to Railway
👉 https://railway.app

### 2️⃣ Sign in with GitHub
- Click "Login"
- Choose "GitHub"
- Authorize Railway

### 3️⃣ Create Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose **`SURENDHAN/ai-interview`**

### 4️⃣ Add Environment Variables
Click "Variables" tab and add these **8 required variables**:

```
GEMINI_API_KEY=AIzaSyD_7RhGB-H1lDwUwSquj28jqrtgDTkGdF8
FIREBASE_API_KEY=AIzaSyAXwfD-DdrDHkGytxRoGxtjfoHBBKlpuo8
FIREBASE_AUTH_DOMAIN=eightfold-d59a6.firebaseapp.com
FIREBASE_PROJECT_ID=eightfold-d59a6
FIREBASE_STORAGE_BUCKET=eightfold-d59a6.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=212958608666
FIREBASE_APP_ID=1:212958608666:web:ffb4c60a9a8f958d4a80a3
FIREBASE_MEASUREMENT_ID=G-Z282DM1ZYP
```

### 5️⃣ Deploy
- Click "Deploy"
- Wait 3-5 minutes
- Get your URL from "Settings" → "Domains"

### 6️⃣ Update Firebase
- Go to Firebase Console
- Authentication → Settings → Authorized domains
- Add your Railway URL: `your-app.up.railway.app`

### 7️⃣ Test
Open your Railway URL and test the app!

---

## 📋 Environment Variables Checklist

Copy-paste these into Railway Variables tab:

- [ ] GEMINI_API_KEY
- [ ] FIREBASE_API_KEY
- [ ] FIREBASE_AUTH_DOMAIN
- [ ] FIREBASE_PROJECT_ID
- [ ] FIREBASE_STORAGE_BUCKET
- [ ] FIREBASE_MESSAGING_SENDER_ID
- [ ] FIREBASE_APP_ID
- [ ] FIREBASE_MEASUREMENT_ID

---

## 🔗 Important Links

- **Railway Dashboard**: https://railway.app/dashboard
- **Your GitHub Repo**: https://github.com/SURENDHAN/ai-interview
- **Firebase Console**: https://console.firebase.google.com/project/eightfold-d59a6
- **Full Guide**: See `RAILWAY_DEPLOYMENT.md`

---

## 💡 Tips

✅ Railway auto-deploys on every GitHub push  
✅ Free tier: $5 credit/month (~250-500 hours)  
✅ WebSocket works out of the box  
✅ Logs available in Deployments tab  

---

## 🆘 Quick Troubleshooting

**App not starting?**
→ Check all 8 environment variables are set

**Login not working?**
→ Add Railway URL to Firebase authorized domains

**Slow first load?**
→ Normal! Whisper model downloads on first start

---

**Ready? Let's deploy! 🚀**

👉 Start here: https://railway.app
