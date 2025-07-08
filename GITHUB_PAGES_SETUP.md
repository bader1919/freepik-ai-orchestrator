# Setting Up GitHub Pages for Documentation

This guide explains how to set up automatic deployment of your MkDocs documentation to GitHub Pages.

## Prerequisites

- GitHub repository for your project
- MkDocs configuration (`mkdocs.yml`) already set up
- Documentation files in the `docs/` directory

## Setup Steps

### 1. Enable GitHub Pages

1. Go to your GitHub repository
2. Click on **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **GitHub Actions**

### 2. Configure Repository Settings

The GitHub Actions workflow is already configured in `.github/workflows/deploy-docs.yml`. This workflow will:

- Build the documentation using MkDocs
- Deploy it to GitHub Pages
- Run automatically on pushes to `main`/`master` branch

### 3. Update Repository URLs

Update the following files with your actual repository information:

#### In `mkdocs.yml`:
```yaml
repo_name: yourusername/freepik-ai-orchestrator
repo_url: https://github.com/yourusername/freepik-ai-orchestrator
site_url: https://yourusername.github.io/freepik-ai-orchestrator/
```

#### In `README.md`:
```markdown
[![Documentation](https://img.shields.io/badge/docs-MkDocs-blue)](https://yourusername.github.io/freepik-ai-orchestrator/)
```

Replace `yourusername` with your GitHub username.

### 4. Commit and Push

Commit all the documentation files and push to your main branch:

```bash
git add .
git commit -m "Add MkDocs documentation with GitHub Pages deployment"
git push origin main
```

### 5. Verify Deployment

1. Go to the **Actions** tab in your GitHub repository
2. You should see a workflow run for "Deploy MkDocs to GitHub Pages"
3. Once it completes successfully, your documentation will be available at:
   `https://yourusername.github.io/freepik-ai-orchestrator/`

## Workflow Details

The GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) does the following:

1. **Triggers** on:
   - Pushes to main/master branch that modify docs
   - Pull requests that modify docs
   - Manual workflow dispatch

2. **Build Job**:
   - Sets up Python 3.11
   - Installs MkDocs and dependencies
   - Builds the documentation
   - Uploads the built site as an artifact

3. **Deploy Job**:
   - Deploys the built site to GitHub Pages
   - Only runs on main/master branch pushes

## Customization

### Custom Domain

To use a custom domain:

1. Add a `CNAME` file to your `docs/` directory:
   ```
   your-custom-domain.com
   ```

2. Configure DNS to point to GitHub Pages:
   ```
   CNAME: yourusername.github.io
   ```

3. Update `site_url` in `mkdocs.yml`:
   ```yaml
   site_url: https://your-custom-domain.com/
   ```

### Branch Protection

Consider setting up branch protection rules:

1. Go to Settings > Branches
2. Add rule for `main` branch
3. Require status checks to pass (including the docs build)

## Troubleshooting

### Build Failures

If the documentation build fails:

1. Check the Actions tab for error details
2. Common issues:
   - Missing Python dependencies
   - Invalid markdown syntax
   - Broken internal links
   - Invalid `mkdocs.yml` configuration

### Local Testing

Test your documentation locally before pushing:

```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocs-material-extensions pymdown-extensions

# Serve locally
mkdocs serve

# Build to check for errors
mkdocs build --strict
```

### Permissions Issues

If you get permissions errors:

1. Go to Settings > Actions > General
2. Under "Workflow permissions", select "Read and write permissions"
3. Check "Allow GitHub Actions to create and approve pull requests"

## Maintenance

### Updating Dependencies

The workflow installs the latest versions of MkDocs and plugins. To pin specific versions:

1. Create `docs/requirements.txt`:
   ```
   mkdocs==1.5.3
   mkdocs-material==9.4.6
   pymdown-extensions==10.3.1
   ```

2. Update the workflow to use this file:
   ```yaml
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install -r docs/requirements.txt
   ```

### Monitoring

- Set up GitHub notifications for failed workflows
- Monitor site analytics if using custom domain
- Regularly check for broken links

## Next Steps

1. Replace `yourusername` with your actual GitHub username
2. Commit and push changes
3. Verify the documentation site is accessible
4. Share the documentation URL with your team
5. Set up monitoring and maintenance procedures

Your documentation will now automatically update whenever you push changes to the docs or mkdocs configuration!
