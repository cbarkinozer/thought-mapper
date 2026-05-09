# LLM Wiki
A personal knowledge base maintained by Claude Code, based on Karpathy's LLM Wiki pattern.
Represents my mind through Tweets, YouTube videos, and Medium articles.

## Structure
- `raw/` — source documents (never modify)
- `wiki/` — markdown pages maintained by Claude Code
- `wiki/index.md` — table of contents
- `wiki/log.md` — append-only operation log

## Ingest (when a source is added to `raw/`)
1. Read the full source
2. Discuss key takeaways with the user before writing
3. Create a summary page in `wiki/` named after the source
4. Create or update concept pages for major ideas and entities
5. Add `[[wiki-links]]` to connect related pages
6. Update `wiki/index.md` with new pages and one-line descriptions
7. Append to `wiki/log.md`: date, source name, what changed

One source may touch 10–15 pages — that's normal.

## Page Format
# Title
- Summary: 1–2 sentences.
- Sources: raw files this page draws from.
- Last updated: YYYY-MM-DD
---
Content here. Short paragraphs, clear headings, [[wiki-links]] throughout.

## Related pages
- [[page-one]]
- [[page-two]]
## Citations
- Cite every factual claim as `(source: filename)`
- Note contradictions when sources disagree
- Mark unsourced claims as `[needs verification]`

## Question Answering
1. Check `wiki/index.md` for relevant pages
2. Read and synthesize an answer, citing wiki pages
3. Say clearly if the answer isn't in the wiki
4. Offer to save valuable answers as new pages — good answers compound

## Lint
Check for: contradictions · orphan pages · missing concept pages · outdated claims · format violations.
Report as a numbered list with suggested fixes.

## Rules
- Never modify `raw/`
- Always update `index.md` and `log.md` after any change
- Page filenames: `lowercase-with-hyphens.md`
- Write in plain language
- When unsure how to categorize something, ask