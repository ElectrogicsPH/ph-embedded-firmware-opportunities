# 🇵🇭 PH Embedded & Firmware Opportunities

A curated directory of companies and organizations in the Philippines offering opportunities in **embedded systems**, **firmware engineering**, **hardware design**, and **IoT**. This resource is intended for engineers, students, and tech enthusiasts exploring career paths or collaboration opportunities in embedded technology.

---

## 🔹 How to Use

- Browse the list of companies below.
- Each entry includes:
  - Company name
  - Focus area
  - Roles or projects
  - Website or LinkedIn link
- Use this as a starting point to research and reach out directly to organizations of interest.

---

## 🚀 Running Locally

**⚠️ Important:** This project requires a live server to run properly. Opening `index.html` directly in a browser (using `file://` protocol) will not work due to CORS restrictions when loading `data.json`.

### Option 1: VS Code Live Server (Recommended)
1. Install the [Live Server extension](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 2: Python HTTP Server
```bash
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

### Option 3: Node.js http-server
```bash
npx http-server -p 8000
```
Then open `http://localhost:8000` in your browser.

### Option 4: GitHub Pages (Production)

The site is automatically deployed to GitHub Pages using GitHub Actions when you push to the `main` branch.

**First-time setup:**
1. Go to your repository on GitHub
2. Click **Settings** → **Pages** (in the left sidebar)
3. Under **Source**, select **GitHub Actions**
4. Save the settings

**After setup:**
- The workflow (`.github/workflows/deploy.yml`) will automatically deploy on every push to `main`
- Your site will be available at: `https://[your-username].github.io/[repository-name]/`
- You can view deployment status in the **Actions** tab

---

## ⚠️ Disclaimer

- This repository is a **curated list only**.  
- Opportunities listed may **not be currently available**.  
- We do **not guarantee job openings or responses** from listed companies.  
- Always check the company's official career page or LinkedIn for up-to-date information.

---

## 📌 Contributions

Contributions are welcome! Please submit a **pull request** to add new companies, update information, or improve the formatting.

### How to Add a New Company

1. **Open `data.json`** in the repository root.

2. **Add a new entry** following this JSON structure:
   ```json
   {
     "company": "Company Name",
     "focus_area": "Industry or Focus Area",
     "roles_or_projects": "Job Roles or Project Types",
     "website_or_linkedin": "https://company-website.com/"
   }
   ```

3. **Important Guidelines:**
   - **Maintain alphabetical order** by company name (A-Z)
   - Use proper JSON formatting (commas, quotes, brackets)
   - Ensure the `website_or_linkedin` field contains a valid URL
   - Keep descriptions concise and relevant

4. **Example Entry:**
   ```json
    {
      "company": "Dyson Electronics",
      "focus_area": "Consumer Electronics",
      "roles_or_projects": "Embedded Systems, Firmware Engineering, Robotics, R&D",
      "website_or_linkedin": "https://www.dyson.com/"
    }
   ```

5. **Test Locally (Optional):**
   - **Important:** Use a live server (see "Running Locally" section above) - do not open `index.html` directly
   - Verify the new company appears in the table in alphabetical order
   - Check that all links work correctly

6. **Submit Your Changes:**
   - Commit your changes with a descriptive message
   - Push to your fork
   - Create a pull request

### Required Fields

- **Company**: Full company name
- **Focus Area**: Industry, sector, or primary focus (e.g., "IoT, Medical Devices, Wearables")
- **Roles / Projects**: Job roles or project types offered (e.g., "Senior Firmware Engineer", "Embedded Systems, Firmware Engineering")
- **Website / LinkedIn**: Valid URL to company website, career page, or LinkedIn profile

---

> Note: This list is **community-maintained**. If you notice outdated information or broken links, feel free to open an issue or submit a pull request.
