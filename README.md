# 🇵🇭 PH Embedded & Firmware Opportunities

A curated directory of companies and organizations in the Philippines offering opportunities in **embedded systems**, **firmware engineering**, **hardware design**, and **IoT**. This resource is intended for engineers, students, and tech enthusiasts exploring career paths or collaboration opportunities in embedded technology.

**Last updated: Nov 15, 2026**

The Philippines list is the default ([index.html](index.html), [data.json](data.json)). A country menu on that page also loads the United Arab Emirates list from [data-uae.json](data-uae.json). Open `index.html?country=ae` to land on the UAE list. [uae.html](uae.html) redirects there. To add a country later, add a data file and one entry in the country list in `index.html`.

**UAE edition last updated: Nov 20, 2026**

---

## 🔹 How to Use

- The site is split into three sections:
  - **Open embedded & firmware roles**: verified, current roles in the Philippines, each linking to its posting
  - **Related roles**: a short list of adjacent hardware and test roles
  - **Companies to watch**: companies doing embedded/firmware work with no current role listed
- Each entry includes:
  - Company name
  - Focus area
  - Roles or projects
  - Website or LinkedIn link (the posting link for roles)
  - For roles: location, posted date, years of experience (when the posting states it), and skill tags taken from the posting
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

Contributions are welcome! You can contribute in two ways:

1. **Submit a Pull Request** - Add new companies, update information, or improve the formatting directly
2. **Open an Issue** - If you'd like to suggest a company but prefer not to make the changes yourself, you can open an issue with the company details and we'll add it for you

### How to Add or Update an Entry

1. **Open `data.json`** in the repository root. It is a flat JSON array; each object is either a **role** (one posting) or a **company to watch**.

2. **Add a role** (sections `open` or `related`):
   ```json
   {
     "company": "Company Name",
     "focus_area": "Industry or Focus Area",
     "roles_or_projects": "Exact job title from the posting",
     "website_or_linkedin": "https://link-to-the-posting",
     "section": "open",
     "posting_url": "https://link-to-the-posting",
     "location": "City, Region",
     "posted": "2026-10-24",
     "experience": "3+ years",
     "tags": ["FreeRTOS", "MCU", "I2C/SPI"]
   }
   ```

3. **Add a company to watch** (no current role):
   ```json
   {
     "company": "Company Name",
     "focus_area": "Industry or Focus Area",
     "roles_or_projects": "Typical roles or projects",
     "website_or_linkedin": "https://company-careers-page/",
     "section": "watch"
   }
   ```

4. **UAE edition:** add or update roles in `data-uae.json`, not `data.json`. The same fields and rules apply, with these differences:
   - Only list roles located in the UAE whose posting is live
   - `open` is embedded software, firmware, embedded Linux, MCU, RTOS, IoT device, and BSP/driver roles
   - `related` is adjacent hardware design, electronics, power electronics, PCB, and hardware test or validation roles
   - `watch` is UAE companies doing embedded, firmware, or hardware work with no current role found
   - `location` is the place stated on the posting, such as `Dubai, UAE` or `Abu Dhabi, UAE`
   - Update the UAE "Last updated" date in the country list in `index.html`, and the UAE date in this README, when you refresh that list
   - `scripts/link_check.py --data data-uae.json` checks those links. The weekly careers-feed check still scans Philippines feeds only.

5. **Important Guidelines:**
   - `section` is one of `open` (embedded/firmware roles), `related` (adjacent hardware/test roles) or `watch` (companies with no current role). Entries without `section` show under Companies to watch.
   - **Maintain alphabetical order** by company name (A-Z), then by title, within each section
   - Only list roles located in the Philippines whose posting is live; remove entries when the posting expires
   - `tags` must come from the posting text; add `"salary"` only when the posting states one
   - `posted` is the posting date (ISO `YYYY-MM-DD`) or the relative age shown on the posting with the date you checked it
   - `experience` is the years of experience stated in the posting, condensed (for example `3+ years`, `0-2 years`, `5-6+ years`). Use `Not stated` when the posting can be read but does not give a number. Do not guess from the job title. Omit the field if the posting cannot be read.
   - Use proper JSON formatting and valid URLs; keep descriptions concise
   - Update the "Last updated" date in `index.html` and this README when you refresh the list

6. **Test Locally (Optional):**
   - **Important:** Use a live server (see "Running Locally" section above) - do not open `index.html` directly
   - Verify the entry appears in the right section in alphabetical order and that links work

7. **Submit Your Changes:**
   - Commit your changes with a descriptive message
   - Push to your fork
   - Create a pull request

### Fields

| Field | Required | Description |
|---|---|---|
| `company` | Yes | Full company name |
| `focus_area` | Yes | Industry, sector, or primary focus |
| `roles_or_projects` | Yes | Job title (roles) or typical roles/projects (watch) |
| `website_or_linkedin` | Yes | Posting URL (roles) or careers/LinkedIn page (watch) |
| `section` | Recommended | `open`, `related` or `watch` |
| `posting_url` | Roles | Link to the job posting |
| `location` | Roles | Location stated in the posting |
| `posted` | Roles | Posting date or age as shown on the posting |
| `experience` | Roles | Years of experience from the posting, or `Not stated`. Omit if the posting cannot be read |
| `tags` | Optional | Skill tags from the posting text |
| `salary` | Optional | Only when the posting states it |

---

> Note: This list is **community-maintained**. If you notice outdated information or broken links, feel free to open an issue or submit a pull request.

---

## 📄 License

- This site is licensed under the **MIT License**, © Embedded Systems PH. See [LICENSE](LICENSE).
- The SPST theme toggle is © 2026 Jeferson De Leon, under the MIT License, from [jefersondeleon.dev](https://jefersondeleon.dev).
