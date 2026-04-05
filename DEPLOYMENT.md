# Deployment Guide

## Free Deployment on Render.com

### Step 1: Deploy Backend

1. **Sign up on Render.com**
   - Go to https://render.com
   - Sign up with your GitHub account (PARTU1616)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `PARTU1616/finance-backend`
   - Configure:
     - **Name**: finance-backend-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
     - **Plan**: Free

3. **Add Environment Variables**
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (generate a random string)
   - `DATABASE_URL` = (will be auto-filled after creating database)
   - `REDIS_URL` = (will be auto-filled after creating Redis)
   - `CORS_ORIGINS` = `https://finance.prathameshgalugade.in`

4. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - **Name**: finance-db
   - **Plan**: Free
   - Copy the "Internal Database URL"
   - Add it to your web service as `DATABASE_URL`

5. **Create Redis Instance**
   - Click "New +" → "Redis"
   - **Name**: finance-redis
   - **Plan**: Free
   - Copy the "Internal Redis URL"
   - Add it to your web service as `REDIS_URL`

6. **Initialize Database**
   - After deployment, go to your web service shell
   - Run: `python init_db.py`

7. **Your Backend URL**
   - Will be: `https://finance-backend-api.onrender.com`
   - API endpoints: `https://finance-backend-api.onrender.com/api/...`

### Step 2: Deploy Frontend on Vercel (Free)

1. **Build Frontend**
   ```bash
   cd quasar-project
   npm install
   npm run build
   ```

2. **Sign up on Vercel**
   - Go to https://vercel.com
   - Sign up with GitHub

3. **Deploy**
   - Click "Add New" → "Project"
   - Import `PARTU1616/finance-backend`
   - Configure:
     - **Framework Preset**: Other
     - **Root Directory**: `quasar-project`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist/spa`

4. **Add Environment Variable**
   - `VITE_API_URL` = `https://finance-backend-api.onrender.com`

5. **Configure Custom Domain**
   - Go to Project Settings → Domains
   - Add: `finance.prathameshgalugade.in`
   - Add DNS records to your domain:
     - Type: `CNAME`
     - Name: `finance`
     - Value: `cname.vercel-dns.com`

### Step 3: Update Backend CORS

Update your backend environment variable:
- `CORS_ORIGINS` = `https://finance.prathameshgalugade.in`

### Alternative: Deploy Frontend on Render

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Connect repository
   - Configure:
     - **Build Command**: `cd quasar-project && npm install && npm run build`
     - **Publish Directory**: `quasar-project/dist/spa`

2. **Custom Domain**
   - Add `finance.prathameshgalugade.in`
   - Follow DNS instructions

## Free Alternatives

### Railway.app
- Similar to Render
- Free tier: 500 hours/month
- Includes PostgreSQL and Redis
- Deploy: https://railway.app

### Fly.io
- Free tier: 3 VMs
- Includes PostgreSQL
- Deploy: https://fly.io

### Netlify (Frontend only)
- Free static hosting
- Custom domain support
- Deploy: https://netlify.com

## Expected URLs

After deployment:
- **Backend API**: `https://finance-backend-api.onrender.com`
- **Frontend**: `https://finance.prathameshgalugade.in`
- **API Docs**: Add to README

## Notes

- Render free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- PostgreSQL free tier: 1GB storage
- Redis free tier: 25MB storage
- For production, consider paid tiers

## Testing Deployment

```bash
# Test backend
curl https://finance-backend-api.onrender.com/api/auth/session/

# Test frontend
open https://finance.prathameshgalugade.in
```
