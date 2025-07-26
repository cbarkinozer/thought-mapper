# thought-mapper

In an era of rapid information growth, we are generating content faster than we can organize it. Thought Mapper is a project designed to tackle this challenge by creating an automated system to analyze and structure textual data, transforming it into a connected web of knowledge.

This initial version focuses on helping users understand their own digital footprint by converting their Twitter archive into a personal Zettelkasten within Obsidian. By automatically clustering tweets into emergent themes and finding semantic similarities, this tool provides a unique way to visualize and connect thoughts and ideas shared over time.

The long-term goal is to evolve Thought Mapper into a versatile tool that can analyze and map any collection of text—be it personal notes, company documentation, or even code repositories—to help individuals and teams navigate and generate insights from their knowledge bases.

**Project Status: Core functionality is complete. The script successfully generates an Obsidian vault from a `tweets.js` file.**

## How to Use (Getting Started)

Follow these steps to generate your own thought map.

### 1. Get Your Twitter Archive

Before you begin, you need the `tweets.js` file that contains all your tweet data.

*   Navigate to your Twitter "Settings and privacy".
*   Go to "Your account" and select "Download an archive of your data".
*   You will receive an email when your archive is ready. Download the `.zip` file.
*   Extract the archive and find the **`tweets.js`** file inside the `data` subfolder.

### 2. Set Up the Project

*   **Clone the Repository:**
    ```bash
    git clone https://github.com/cbarkinozer/thought-mapper.git
    cd thought-mapper
    ```
*   **Place Your Data:** Copy the `tweets.js` file you downloaded into the root of this `thought-mapper` project folder.

*   **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Run the Analysis

Execute the main script from your terminal. The process may take a few minutes depending on the number of tweets and your computer's performance.

```bash
python app.py
```

The script will print its progress as it moves through the pipeline. When it's finished, you will have a new folder named `obsidian_vault` in your project directory.

### 4. Open Your Knowledge Graph in Obsidian

*   Open the Obsidian application.
*   Click **"Open another vault"**.
*   Select **"Open folder as vault"**.
*   Navigate to and select the `obsidian_vault` folder that was just created.

You can now explore your tweets as a network of interconnected notes. Use the Graph View in Obsidian to see a visual representation of your thought clusters!

---

## How It Works: The AI Pipeline

The script transforms your raw tweets into a connected knowledge graph through a four-stage AI pipeline.

### Stage 1: Ingestion and Cleaning

The process begins by reading the `tweets.js` file. Each tweet's text is extracted and passed through a cleaning function that removes digital noise (like URLs and mentions) which could interfere with the analysis. This ensures the AI models focus only on the meaning of your words.

### Stage 2: Semantic Embedding

This is the core of the AI analysis. We use a powerful **Sentence Transformer** model (`all-MiniLM-L6-v2`) to convert each cleaned tweet into a high-dimensional vector (an "embedding"). These vectors mathematically represent the semantic meaning of the text, allowing tweets with similar ideas—even if they use different words—to be numerically close to each other.

### Stage 3: Thematic Clustering

With all tweets represented as vectors, we perform **community detection clustering**. This algorithm analyzes the similarity between all tweet embeddings and automatically groups them into thematic clusters. Unlike other methods, we do not need to specify the number of topics beforehand; the system discovers them organically. Through experimentation, a similarity **threshold of 0.50** was chosen as the optimal value to group a significant portion of tweets into coherent themes without being overly strict.

### Stage 4: Zettelkasten Generation

In the final stage, the script generates the `.md` files for your Obsidian vault:
1.  **Note Creation:** Each tweet becomes a single Markdown file.
2.  **Metadata:** YAML frontmatter is added to each note, containing the tweet's original date, the `Cluster_ID` it belongs to (or `Outlier` if it's unique), and a link to the original tweet.
3.  **Inter-linking:** For each note, the script calculates its similarity to all other notes and automatically inserts `[[wiki-links]]` to the most closely related thoughts, creating the connective tissue of your knowledge graph.

---

## Future Development

This project provides a solid foundation. Future versions could include:

*   **LLM-Powered Topic Naming:** Use a Large Language Model (like GPT or Llama) to automatically generate descriptive names for each cluster (e.g., "AI and the Future" instead of "Cluster_1").
*   **Guided Clustering Mode:** Allow users to provide their own category labels (e.g., "Work," "Philosophy") and have the system sort tweets into those predefined buckets.
*   **Advanced Clustering Algorithms:** Implement more sophisticated algorithms like HDBSCAN for potentially more nuanced cluster detection.
*   **Web User Interface:** Create a simple UI with Streamlit or Flask where a user can upload their archive file directly, making the tool more accessible.
*   **Support for More Data Sources:** Expand the pipeline to analyze other text sources, such as personal notes, documents, or even other social media archives.