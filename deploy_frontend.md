# Frontend Deployment Guide (Netlify)

## Step 1: Install Dependencies
```bash
npm install --legacy-peer-deps
```

## Step 2: Build the Project
```bash
npm run build
```

## Step 3: Deploy to Netlify

### Option A: Drag & Drop
1. Go to [netlify.com](https://netlify.com)
2. Sign up/Login
3. Drag the `build` folder to the deploy area
4. Wait for deployment

### Option B: Git Integration
1. Push your code to GitHub
2. Connect your GitHub repo to Netlify
3. Set build command: `npm run build`
4. Set publish directory: `build`
5. Deploy

## Step 4: Set Environment Variables
In Netlify dashboard, go to Site Settings > Environment Variables:
- `REACT_APP_API_URL`: Your Railway API URL (e.g., https://your-api.railway.app)

## Step 5: Get Your URL
After deployment, you'll get a URL like:
```
https://your-app-name.netlify.app
```

## Step 6: Update Bot Configuration
Update your bot's environment variables:
- `VERIFICATION_URL`: https://your-app-name.netlify.app 