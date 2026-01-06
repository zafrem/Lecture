# Step 6: Publishing Your Work (GitHub Pages & Jekyll)

Now that you've built your AI Agent and written your documentation, you probably want to share it with the world. Instead of sending people a zip file, you can turn your GitHub repository into a **live website** for free.

We will use **Jekyll**, the engine behind GitHub Pages, to make it look professional.

---

## 1. What is Jekyll?

GitHub Pages uses a tool called **Jekyll** behind the scenes. It takes your simple text files (Markdown) and wraps them in beautiful HTML templates.
-   **Without Jekyll**: Your site looks like a plain text document.
-   **With Jekyll**: Your site looks like a modern blog or documentation site with headers, footers, and colors.

---

## 2. Setting it up (The `_config.yml` file)

To tell GitHub "I want to use a nice theme", you only need to create **one file**.

### Action: Create `_config.yml`
Create a file named `_config.yml` in your project folder with this content:

```yaml
title: AI Education Assistant
description: A step-by-step guide to building an AI Agent for Teachers.
theme: jekyll-theme-slate
```

**That's it!**
-   `theme`: You can choose from built-in themes like `jekyll-theme-cayman`, `jekyll-theme-slate`, or `jekyll-theme-architect`.

---

## 3. Enable GitHub Pages

1.  **Open your Repository** on GitHub.com.
2.  Click on the ⚙️ **Settings** tab.
3.  Click on **Pages** (sidebar).
4.  Under **Build and deployment** > **Branch**:
    -   Select `main` (or `master`).
    -   Select the folder where your `_config.yml` is (usually `/ (root)`).
    -   Click **Save**.

---

## 4. Customizing the Landing Page (HTML)

If you want a custom homepage instead of just your README, you can create an `index.html` file.

**Example `index.html`:**
```html
---
layout: default
title: Home
---
<div style="text-align: center; padding: 50px;">
  <h1>Welcome to the AI Education Assistant</h1>
  <p>Learn how to build your own AI Co-Pilot.</p>
  <a href="Class/01_Concept_and_Design.md" style="background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Start the Course</a>
</div>
```

By adding this file, GitHub will use it as the "Front Door" to your website, while keeping the rest of your documentation in the nice theme!

---

## 5. The Result

Once active, you can send a link (`https://your-username.github.io/repo-name/`).
Your students will see a professional site that looks like you hired a web designer, all generated from your simple text files!