# thought-mapper

Thought Mapper is a project designed to help users export, analyze, and understand their data. By automatized categorizing, clustering, and finding semantic similarities between text, this tool will enable users to create a Zettelkasten in Obsidian. This will provide a unique way to visualize and connect their thoughts and ideas shared over time. The ultimate goal is to automate and deploy this process, making it accessible to a wider audience.

## Project Goals

1.  **Data Acquisition:** Securely download a user's complete Twitter archive.
2.  **Data Processing & Analysis:** Develop a pipeline to categorize, cluster, and identify semantic relationships between tweets.
3.  **Zettelkasten Integration:** Format the processed data for seamless batch import into Obsidian as a Zettelkasten.
4.  **Automation & Deployment:** Create a user-friendly, automated system that can be deployed for public use.

---

## Phase 1: Data Acquisition - Getting Your Tweets

The first step is to obtain Twitter data. Twitter allows you to download an archive of all your activity on the platform.

### **To-Do:**

*   **Request Twitter Archive:**
    *   Navigate to your Twitter "Settings and privacy".
    *   Go to "Your account" and select "Download an archive of your data".
    *   You will be prompted to verify your password and complete a verification step.
    *   Click "Request archive". It may take up to 24 hours for Twitter to prepare your data.
*   **Download and Understand the Archive:**
    *   You will receive an email and a push notification when your archive is ready.
    *   Download the `.zip` file from the link provided.
    *   Familiarize yourself with the structure of the archive. The tweets are contained in a file named `tweets.js` (or a similar variation) within the "data" subfolder. This file will be the primary input for the next phase.

---

## Phase 2: Data Processing and Analysis

With your Twitter archive in hand, the next step is to process and analyze the content of your tweets. This involves several layers of natural language processing (NLP).

### **To-Do:**

*   **Tweet Extraction and Cleaning:**
    *   **Sub-task:** Write a script (Python is recommended) to parse the `tweets.js` file and extract the text of each tweet.
    *   **Sub-task:** Clean the tweet text by removing URLs, mentions, hashtags (or keeping them as metadata), and other noise.
*   **Categorization (Topic Modeling):**
    *   **Sub-task:** Research and implement a topic modeling technique (e.g., Latent Dirichlet Allocation - LDA, or newer transformer-based methods) to automatically group tweets into broad categories.
    *   **Sub-task:** Experiment with the number of topics to find a meaningful representation of your data.
*   **Clustering:**
    *   **Sub-task:** Use clustering algorithms (e.g., K-Means, DBSCAN) to group similar tweets together based on their content. This can be more granular than topic modeling.
*   **Semantic Similarity and Relation Generation:**
    *   **Sub-task:** Utilize word embeddings (e.g., Word2Vec, GloVe) or sentence transformers (e.g., from the Hugging Face library) to generate vector representations of your tweets.
    *   **Sub-task:** Calculate the cosine similarity between tweet vectors to identify tweets that are semantically similar.
    *   **Sub-task:** Define a threshold for similarity to establish "links" or "relations" between tweets.

---

## Phase 3: Zettelkasten Integration with Obsidian

The goal of this phase is to transform your analyzed tweets into a format that can be imported into Obsidian to create a connected web of notes, known as a Zettelkasten.

### **To-Do:**

*   **Define the Zettelkasten Note Format:**
    *   **Sub-task:** Each tweet will become a separate note in Obsidian.
    *   **Sub-task:** The note's title could be a unique identifier (e.g., timestamp + first few words of the tweet).
    *   **Sub-task:** The body of the note will contain the full text of the tweet.
    *   **Sub-task:** Metadata for each note should be included (e.g., using YAML frontmatter in Markdown). This will include:
        *   Date of the tweet
        *   Assigned category (from Phase 2)
        *   Cluster ID (from Phase 2)
        *   Links to the original tweet
*   **Generate Inter-Note Links:**
    *   **Sub-task:** Based on the semantic similarity analysis (Phase 2), automatically generate internal links (wiki-links in Markdown) between related tweet-notes. For example, if Tweet A is highly similar to Tweet B, the note for Tweet A should contain a link to the note for Tweet B, and vice-versa.
*   **Create the Batch Import Data:**
    *   **Sub-task:** Write a script to generate a folder of Markdown (`.md`) files, with each file representing a tweet-note, formatted as defined above.

---

## Phase 4: Automation and Deployment

This final phase focuses on making the entire process from data download to Zettelkasten generation as seamless as possible for any user.

### **To-Do:**

*   **Create a Unified Pipeline:**
    *   **Sub-task:** Combine all the scripts from the previous phases into a single, executable pipeline.
    *   **Sub-task:** The pipeline should take the user's Twitter archive `.zip` file as input and produce a folder of Markdown files as output.
*   **Develop a User Interface (Optional but Recommended):**
    *   **Sub-task:** For broader accessibility, create a simple graphical user interface (GUI) or a web-based interface where a user can upload their archive and trigger the process.
    *   **Sub-task:** Libraries like Streamlit or Flask in Python are good options for creating a web app.
*   **Containerization and Deployment:**
    *   **Sub-task:** To ensure the tool runs consistently across different environments, containerize the application using Docker.
    *   **Sub-task:** Write a `Dockerfile` that includes all the necessary dependencies.
*   **Public Deployment:**
    *   **Sub-task:** Deploy the containerized application to a cloud platform (e.g., Google Cloud Run, Heroku, or a similar service) to make it publicly accessible.
*   **Documentation and Open Sourcing:**
    *   **Sub-task:** Create comprehensive documentation explaining how to use the tool.
    *   **Sub-task:** Consider open-sourcing the project on a platform like GitHub to allow for community contributions and improvements.