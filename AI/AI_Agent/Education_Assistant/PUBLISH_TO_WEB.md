# How to Publish This Documentation to the Web

You can turn these Markdown files into a beautiful, searchable website (like the one you see for many open-source projects) using a tool called **MkDocs**.

## Step 1: Install MkDocs
Open your terminal and run:

```bash
pip install mkdocs mkdocs-material
```

## Step 2: Preview the Site Locally
To see what your website looks like on your own computer:

1.  Navigate to this directory:
    ```bash
    cd AI/AI_Agent/Education_Assistant
    ```
2.  Run the server:
    ```bash
    mkdocs serve
    ```
3.  Open your browser to `http://127.0.0.1:8000`.

## Step 3: Publish to GitHub Pages (Free)
If this code is already on GitHub, you can publish the site for free.

1.  **Ensure you are in the directory** (`AI/AI_Agent/Education_Assistant`).
2.  Run this command:
    ```bash
    mkdocs gh-deploy
    ```
3.  That's it! 
    -   MkDocs will build the site and push it to a special branch (`gh-pages`).
    -   Your site will be live at `https://your-username.github.io/repository-name/`.

## Why use this?
-   **Search Bar**: Users can search for "Ollama" or "Database".
-   **Dark Mode**: Built-in toggle.
-   **Mobile Friendly**: Looks great on phones.
-   **Navigation**: Automatic sidebar and tabs.
