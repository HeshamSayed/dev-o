# DEV-O Deployment Guide

## Quick Deployment (Recommended)

### Frontend Only
```bash
./deploy.sh
```

### Backend Only
```bash
./deploy-backend.sh
```

### Full Stack (Frontend + Backend)
```bash
./deploy-backend.sh && ./deploy.sh
```

---

## What Each Script Does

### `deploy.sh` (Frontend)
1. Pull latest changes from git
2. Build the frontend with production settings
3. Restart nginx to ensure fresh serving
4. Verify deployment was successful

### `deploy-backend.sh` (Backend)
1. Pull latest changes from git
2. Rebuild containers if requirements.txt changed
3. Run database migrations
4. Collect static files
5. Restart backend and celery services
6. Verify services are running

---

## Manual Deployment

### Frontend (Manual Steps)
```bash
# 1. Pull latest changes
git pull origin master

# 2. Build frontend
cd frontend
VITE_API_URL=https://api.dev-o.ai VITE_WS_URL=wss://api.dev-o.ai npm run build
cd ..

# 3. Restart nginx (optional but recommended)
docker compose restart nginx

# 4. Verify
docker ps | grep devo_nginx
```

### Backend (Manual Steps)
```bash
# 1. Pull latest changes
git pull origin master

# 2. If requirements.txt changed, rebuild containers
docker compose build backend celery

# 3. Run database migrations
docker compose exec backend python manage.py migrate

# 4. Collect static files
docker compose exec backend python manage.py collectstatic --noinput

# 5. Restart backend services
docker compose restart backend celery

# 6. Verify
docker ps | grep -E "devo_backend|devo_celery"
docker compose logs --tail=20 backend
```

---

## When to Use Each Deployment

### Frontend Only (`./deploy.sh`)
- UI/UX changes
- Frontend bug fixes
- Component updates
- Styling changes
- No backend/API changes

### Backend Only (`./deploy-backend.sh`)
- API changes
- Database model changes
- Background task updates
- Django admin changes
- Backend bug fixes
- No frontend changes

### Full Stack (`./deploy-backend.sh && ./deploy.sh`)
- Features requiring both frontend and backend changes
- Major updates
- New routes/endpoints with UI
- After merging branches with full-stack changes

---

## How It Works

### Automatic Updates
- Frontend builds to `./frontend/dist` on the host machine
- Nginx serves directly from `./frontend/dist` via bind mount
- **No volume management needed** - new builds are immediately available

### Cache Strategy
- **HTML files**: No cache (users always get latest version)
- **Assets (JS/CSS)**: Cached for 1 year with immutable flag
- **Cache busting**: Vite generates unique filenames (content hashes)
  - When code changes → new filenames → browser downloads new files
  - When code unchanged → same filenames → browser uses cache

### Example Update Flow

```
You: Make code changes
  ↓
You: Run ./deploy.sh (or npm run build)
  ↓
Vite: Generates new files with new hashes
  - index-OLD123.js → index-NEW456.js
  ↓
User: Visits site
  ↓
Browser: Downloads fresh HTML (not cached)
  ↓
Browser: Sees new filename → Downloads new file
  ↓
Result: User gets updates automatically! ✅
```

---

## Deployment Checklist

- [ ] Pull latest code: `git pull origin master`
- [ ] Build frontend: `npm run build` (in frontend directory)
- [ ] Restart nginx: `docker compose restart nginx`
- [ ] Test site: Visit https://dev-o.ai
- [ ] Check cache headers: `curl -I https://dev-o.ai/assets/index-*.js`

---

## Troubleshooting

### Site shows old version after deployment
- **Solution**: Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- **Why**: Browser might have cached the old HTML file

### Assets not loading
- **Check**: `docker exec devo_nginx ls -lh /var/www/landing/assets/`
- **Verify**: Files should match `./frontend/dist/assets/`
- **Fix**: Ensure bind mounts are correctly configured in docker-compose.yml

### Build fails
- **Check**: `npm install` in frontend directory
- **Verify**: Node version (should be 20+)
- **Logs**: Check build output for specific errors

---

## Performance Tips

### Current Setup (Optimized)
- ✅ Content hashing enabled (Vite default)
- ✅ Aggressive asset caching (1 year)
- ✅ HTML no-cache for freshness
- ✅ Gzip compression enabled

### Monitoring
```bash
# Check asset cache headers
curl -I https://dev-o.ai/assets/index-*.js | grep cache

# Expected: cache-control: max-age=31536000, public, immutable

# Check HTML cache headers
curl -I https://dev-o.ai/ | grep cache

# Expected: cache-control: no-store, no-cache, must-revalidate
```

---

## Production Deployment Best Practices

1. **Test locally first**
   ```bash
   npm run build
   npm run preview
   ```

2. **Deploy during low traffic** (if possible)

3. **Monitor after deployment**
   - Check error logs: `docker compose logs nginx`
   - Verify site loads: `curl https://dev-o.ai`
   - Test key features: Login, Chat, Projects

4. **Rollback if needed**
   ```bash
   git revert HEAD
   ./deploy.sh
   ```

---

## Questions?

The deployment process is now streamlined. Every `./deploy.sh` run will:
- Pull latest code
- Build with new content hashes
- Serve immediately
- Cache efficiently

No volume removal or manual intervention needed! 🎉
