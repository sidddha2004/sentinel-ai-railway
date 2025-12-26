# Sentinel AI - Railway Demo Backend

Lightweight fraud detection system optimized for Railway deployment.

## 🚀 Features

- ✅ In-memory vector search (no external DB)
- ✅ 200 pre-loaded demo transactions
- ✅ Mock AI fraud analysis
- ✅ Federated learning simulation
- ✅ Real-time polling support (no WebSocket)
- ✅ **~120MB RAM usage** (Railway free tier safe)

## 📦 Deployment to Railway

### Method 1: Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Method 2: GitHub Integration

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repo
6. Railway will auto-detect and deploy!

## 🔧 Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

Visit: `http://localhost:8000`

## 🌐 After Deployment

Railway will give you a URL like:
```
https://your-app-name.up.railway.app
```

Update your frontend's API URL to this Railway URL.

## 📋 Environment Variables

No environment variables required! Everything works out of the box.

Optional:
- `PORT` - Railway sets this automatically

## ✅ Endpoints

- `GET /` - Health check
- `POST /secure-ingest` - Add transaction
- `POST /secure-search` - Search transactions
- `POST /secure-broadcast` - Broadcast threat
- `GET /streaming-stats` - Get statistics
- `POST /rag-analysis` - Mock AI analysis
- `POST /quick-threat-check` - Quick threat assessment

## 🔄 Differences from Full Version

| Feature | Demo | Production |
|---------|------|------------|
| Database | In-memory | CyborgDB |
| Streaming | Polling | Kafka + WebSocket |
| ML Models | Rule-based | Sentence Transformers |
| Storage | Temporary | Persistent Redis |
| AI Analysis | Mock | Real Gemini API |

## 💰 Cost

**Free!** Optimized for Railway's free tier:
- ~120MB RAM usage
- Fast cold starts (<2s)
- No external services

## 🐛 Troubleshooting

**Build fails?**
- Make sure `requirements.txt` is in root
- Check Railway build logs

**App crashes?**
- Check RAM usage in Railway dashboard
- Should be <200MB

**Can't access endpoints?**
- Check CORS settings in `main.py`
- Update allowed origins with your frontend URL

## 📞 Support

For issues, check Railway's documentation:
- https://docs.railway.app

## 🎯 Next Steps

After deploying backend:
1. Copy your Railway URL
2. Update frontend API configuration
3. Test all endpoints
4. Deploy frontend to Vercel/Netlify

---

Made with ❤️ for Railway deployment# sentinel-ai-railway
