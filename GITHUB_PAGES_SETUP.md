# GitHub Pages Setup Guide

This guide explains how to deploy your MkDocs documentation to GitHub Pages.

## Quick Setup

1. **Enable GitHub Pages**:
   - Go to your repository → Settings → Pages
   - Under "Source", select **"GitHub Actions"**

2. **Update Repository URLs** in `mkdocs.yml`:
   ```yaml
   repo_name: yourusername/freepik-ai-orchestrator
   repo_url: https://github.com/yourusername/freepik-ai-orchestrator
   site_url: https://yourusername.github.io/freepik-ai-orchestrator/
   ```

3. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Deploy documentation"
   git push origin main
   ```

4. **Check deployment**:
   - Go to Actions tab to monitor the build
   - Once complete, visit: `https://yourusername.github.io/freepik-ai-orchestrator/`

## How It Works

- **Workflow**: `.github/workflows/deploy-docs.yml` handles automatic deployment
- **Theme**: Material theme is installed during build (no local installation needed)
- **Triggers**: Deploys on pushes to main branch when docs change

## Theme Configuration

The Material theme is configured in `mkdocs.yml`:
- Dark/light mode toggle
- Navigation features
- Code highlighting
- Search functionality

Replace `yourusername` with your GitHub username to complete setup!
