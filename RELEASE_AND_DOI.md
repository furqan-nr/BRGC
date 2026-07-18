# How to publish this folder and mint a DOI

This creates a citable DOI for the code via **GitHub + Zenodo**. Do it once; the
DOI can then go into the paper's Data Availability statement.

## 1. Create the GitHub repository
1. Sign in at https://github.com and create a **new public repository** named
   `BRGC` (public is required for a free Zenodo DOI).
2. Do **not** let GitHub add a README/License (this folder already has them).
3. Upload this folder's contents — either drag-and-drop via
   "Add file → Upload files", or from a terminal:
   ```bash
   cd "BRGC"
   git init
   git add .
   git commit -m "BRGC v1.0.0: code and training-free analysis for the relation-prediction study"
   git branch -M main
   git remote add origin https://github.com/furqan-nr/BRGC.git
   git push -u origin main
   ```
4. The `github.com/furqan-nr/BRGC` links in `CITATION.cff` are already set.

## 2. Connect Zenodo to GitHub
1. Go to https://zenodo.org and sign in **with your GitHub account**.
2. Open https://zenodo.org/account/settings/github/ and toggle the `BRGC`
   repository **ON**. (If it is not listed, click "Sync now".)

## 3. Create a release — this triggers the DOI
1. On GitHub: **Releases → Draft a new release**.
2. Tag version `v1.0.0`, title "BRGC v1.0.0", add a short description.
3. Click **Publish release**.
4. Zenodo automatically archives that release and mints a DOI within a minute or
   two. Find it back on the Zenodo GitHub settings page (or in your Zenodo
   uploads).

Zenodo issues two DOIs: a **concept DOI** that always points to the latest
version (use this one in the paper) and a **version DOI** for v1.0.0
specifically.

## 4. Put the DOI in the paper and repo
- Add the DOI badge to `README.md` (a commented template is already in the file).
- Update the manuscript's **Data Availability** statement to cite the concept
  DOI instead of "will be archived ... upon acceptance", e.g.:
  > The source code is archived at Zenodo, https://doi.org/10.5281/zenodo.XXXXXXX.

## Notes
- `.zenodo.json` in this folder pre-fills the Zenodo deposit (title, authors,
  ORCIDs, keywords, MIT license), so the metadata is correct automatically.
- To release an updated version later, push changes and publish a new GitHub
  release (e.g. `v1.1.0`); the concept DOI stays the same.
