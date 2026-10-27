# Push this project to GitHub

Run these commands from the project root after creating an empty repository on GitHub.

```bash
git init
git add .
git status
git commit -m "Initial commit: fuel consumption analysis system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/fuel-consumption-analysis.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and use the repository URL shown by GitHub.

Before pushing, check that `.env` is not staged:
```bash
git status
```
The `.env` file is ignored by `.gitignore`; only `.env.example` should be committed. Never commit database passwords.

For later changes:
```bash
git add .
git commit -m "Describe your changes"
git push
```
