# 🔗 Frontend-Backend Connection Guide

This guide will help you connect your frontend at **https://cydbfinanace.vercel.app/** with the backend deployed on Railway.

## ✅ What's Already Done

1. ✅ Backend CORS configured for your frontend domain
2. ✅ Frontend updated to use configurable API URL
3. ✅ All API endpoints ready

## 📋 Step-by-Step Instructions

### Step 1: Deploy Backend to Railway

#### Option A: Using Railway CLI (Recommended)

```bash
# Navigate to backend directory
cd d:\hackathon\sentinel-ai-railway

# Install Railway CLI (if not installed)
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

#### Option B: Using GitHub Integration

1. Push your `sentinel-ai-railway` folder to GitHub
2. Go to [railway.app](https://railway.app)
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will auto-detect Python and deploy!

### Step 2: Get Your Railway Backend URL

After deployment, Railway will provide a URL like:
```
https://your-app-name.up.railway.app
```

**Copy this URL** - you'll need it in the next step!

### Step 3: Update Frontend Environment Variable

1. Go to your Vercel project dashboard: https://vercel.com
2. Select your project (`cydbfinanace`)
3. Go to **Settings** → **Environment Variables**
4. Add a new environment variable:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://your-app-name.up.railway.app` (use your Railway URL)
   - **Environment**: Production, Preview, Development (select all)
5. Click **Save**

### Step 4: Redeploy Frontend

After adding the environment variable:

1. Go to **Deployments** tab in Vercel
2. Click **"Redeploy"** on the latest deployment
3. Or push a new commit to trigger automatic deployment

### Step 5: Verify Connection

1. Visit your frontend: https://cydbfinanace.vercel.app
2. Open browser DevTools (F12) → Console tab
3. Try using the app (search, add transaction, etc.)
4. Check for any CORS errors in the console
5. Check Network tab to see if API calls are going to Railway URL

## 🧪 Testing Locally (Optional)

If you want to test locally before deploying:

1. **Start backend locally:**
   ```bash
   cd d:\hackathon\sentinel-ai-railway
   uvicorn main:app --reload
   ```

2. **Start frontend locally:**
   ```bash
   cd d:\hackathon\cydb_finanace\secure-banking-system\frontend
   npm run dev
   ```

3. **Create `.env.local` file** in frontend directory:
   ```
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

4. Frontend will automatically use `http://127.0.0.1:8000` for local development

## 🔍 Troubleshooting

### CORS Errors
- ✅ Backend CORS is already configured for `https://cydbfinanace.vercel.app`
- If you see CORS errors, check that Railway URL is correct
- Make sure backend is running and accessible

### API Not Found (404)
- Verify Railway deployment is successful
- Check Railway logs: `railway logs`
- Test backend directly: Visit `https://your-railway-url/` in browser

### Environment Variable Not Working
- Make sure variable name is exactly: `VITE_API_BASE_URL`
- Vite requires `VITE_` prefix for environment variables
- Redeploy frontend after adding environment variable
- Check Vercel build logs to see if variable is being read

### Connection Timeout
- Check Railway service is running (not sleeping)
- Railway free tier may sleep after inactivity
- Consider upgrading or using Railway Pro for always-on service

## 📝 API Endpoints Reference

Your backend exposes these endpoints:

- `GET /` - Health check
- `POST /secure-ingest` - Add transaction
- `POST /secure-search` - Search transactions
- `POST /secure-broadcast` - Broadcast threat
- `DELETE /secure-delete/{id}` - Delete transaction
- `GET /streaming-stats` - Get statistics
- `POST /rag-analysis` - AI fraud analysis
- `POST /quick-threat-check` - Quick threat assessment
- `POST /federated-round` - Federated learning round
- `POST /secure-train` - Train index

## 🎯 Quick Checklist

- [ ] Backend deployed to Railway
- [ ] Railway URL copied
- [ ] Environment variable `VITE_API_BASE_URL` added to Vercel
- [ ] Frontend redeployed
- [ ] Tested connection in browser
- [ ] No CORS errors in console
- [ ] API calls working correctly

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Check Railway logs: `railway logs`
- Check Vercel build logs in dashboard

---

**Once connected, your frontend will communicate with the Railway backend!** 🚀

