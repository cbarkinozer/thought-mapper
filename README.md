# thought-mapper

In an era of rapid information growth, we are generating content faster than we can organize it. Thought Mapper is a project designed to tackle this challenge by creating an automated system to analyze and structure textual data, transforming it into a connected web of knowledge.

The first implementation of this vision focuses on helping users understand their own digital footprint by converting their Twitter archive into a personal Zettelkasten within Obsidian. By automatically categorizing, clustering, and finding semantic similarities between tweets, this tool provides a unique way to visualize and connect thoughts and ideas shared over time.

The long-term goal is to evolve Thought Mapper into a versatile tool that can analyze and map any collection of text—be it personal notes, company documentation, or even code repositories—to help individuals and teams navigate and generate insights from their knowledge bases.

## Project Goals

1.  **Data Ingestion:** Securely process a user's complete Twitter archive as the initial data source.
2.  **AI-Powered Analysis:** Develop a robust pipeline using NLP and Machine Learning to categorize, cluster, and identify semantic relationships between tweets with an initial accuracy target of ~70%.
3.  **Zettelkasten Generation:** Format the analyzed data for seamless import into Obsidian, creating an interconnected knowledge graph where each tweet is a single, atomic note.
4.  **User-Friendly Automation:** Create a simple, automated system that is accessible to a wider audience, with future potential for public deployment.

---

## Phase 1: Data Ingestion - Getting Your Tweets

The first step is to obtain your Twitter data. Twitter allows you to download an archive of all your activity on the platform.

### **To-Do:**

*   **Request Twitter Archive:**
    *   Navigate to your Twitter "Settings and privacy".
    *   Go to "Your account" and select "Download an archive of your data".
    *   You will be prompted to verify your password and complete a verification step.
    *   Click "Request archive". It may take up to 24 hours for Twitter to prepare your data.
*   **Download and Understand the Archive:**
    *   You will receive an email and a push notification when your archive is ready.
    *   Download the `.zip` file from the link provided.
    *   The primary data source for this project is the `tweets.js` file located within the "data" subfolder of your archive.

---

## Phase 2: AI-Powered Analysis

With your Twitter archive, the next step is to process and analyze the content of your tweets. This involves a multi-layered approach using natural language processing (NLP) and machine learning models. The aim is not perfection, but to provide a high-quality initial structure for your knowledge base.

### **To-Do:**

*   **Tweet Extraction and Cleaning:**
    *   **Sub-task:** Write a Python script to parse the `tweets.js` file and extract the full text of each tweet.
    *   **Sub-task:** Clean the tweet text by removing noise like URLs and mentions, while retaining hashtags as potential metadata.
*   **Automated Categorization & Clustering:**
    *   **Sub-task:** Employ a hybrid approach of topic modeling (e.g., LDA, transformer-based methods) and clustering algorithms (e.g., K-Means, DBSCAN) to discover both broad themes and granular groupings within your tweets. The value lies in the system's ability to identify emergent, fine-grained categories automatically.
*   **Semantic Relation Mapping:**
    *   **Sub-task:** Utilize sentence transformers (e.g., from the Hugging Face library) to generate vector representations (embeddings) of your tweets.
    *   **Sub-task:** Calculate the cosine similarity between tweet vectors to identify semantically similar, but not necessarily identically worded, thoughts.
    *   **Sub-task:** Define a similarity threshold to establish meaningful "links" or "relations" that will form the connections in your knowledge graph.

---

## Phase 3: Zettelkasten Generation for Obsidian

The goal of this phase is to transform your analyzed tweets into a format that Obsidian can understand, creating a connected web of notes that you own and control.

### **To-Do:**

*   **Define the Zettelkasten Note Format:**
    *   **Sub-task:** Each tweet will become a separate Markdown note.
    *   **Sub-task:** The note's title will be a unique identifier (e.g., timestamp + first few words).
    *   **Sub-task:** The body will contain the full text of the tweet.
    *   **Sub-task:** Metadata will be included in YAML frontmatter:
        *   `date`: The original date of the tweet.
        *   `category`: The assigned category from Phase 2.
        *   `cluster_id`: The cluster ID from Phase 2.
        *   `source_link`: A link to the original tweet.
*   **Generate Inter-Note Links:**
    *   **Sub-task:** Based on the semantic similarity analysis (Phase 2), automatically generate wiki-links between related tweet-notes. If Tweet A is highly similar to Tweet B, the note for A will contain a link `[[Note B's Title]]`, and vice-versa.
*   **Create the Batch Import Data:**
    *   **Sub-task:** Write a script to generate a folder of `.md` files, with each file representing a tweet-note, formatted and linked as defined above, ready to be opened as an Obsidian vault.

---

## Phase 4: Pipeline and Accessibility

This final phase focuses on making the entire process seamless for any user and setting the stage for future development.

### **To-Do:**

*   **Create a Unified Pipeline:**
    *   **Sub-task:** Combine all scripts into a single, executable pipeline that takes the user's Twitter archive `.zip` file as input and produces the folder of Markdown files as output.
*   **Develop a User Interface (Optional but Recommended):**
    *   **Sub-task:** For broader accessibility, create a simple graphical user interface (GUI) or a web-based interface (using Streamlit or Flask) where a user can upload their archive and trigger the process.
*   **Containerization and Deployment:**
    *   **Sub-task:** Containerize the application using Docker to ensure it runs consistently across different environments.
*   **Public Deployment:**
    *   **Sub-task:** Deploy the containerized application to a cloud platform (e.g., Google Cloud Run, Heroku) to make it publicly accessible.
*   **Documentation and Open Sourcing:**
    *   **Sub-task:** Create comprehensive documentation and open-source the project on GitHub to invite community contributions.