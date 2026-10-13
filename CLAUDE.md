# CLAUDE.md

## Project

Mail Server Ubuntu Learning Portal: Indonesian learning curriculum from Linux fundamentals to production mail server administration.

## Source of Truth

- `docs/PRD.md`: product requirements and acceptance criteria.
- `docs/TECHNICAL-DESIGN.md`: architecture, build, URLs, and deployment.
- `kurikulum-mail-server-ubuntu.html`: canonical curriculum dashboard and chapter structure.
- `materi/`: canonical Markdown learning materials.
- `README.md`: setup and usage instructions.

Read only the documents relevant to the current task. Do not load every chapter or document by default.

## Core Rules

- Preserve existing content, chapter IDs, navigation, and working features.
- Follow the PRD and technical design; do not invent conflicting requirements.
- Use Indonesian for learning materials and documentation.
- Implement one chapter or clearly scoped task at a time.
- Inspect relevant files before editing.
- Avoid unrelated refactoring and unnecessary dependencies.
- Never claim a test or deployment succeeded without verifying it.
- Never store credentials, private keys, tokens, or production secrets.
- Ask before destructive changes or changes outside the requested scope.

## Curriculum

- Keep category, module, and chapter IDs consistent with the HTML dashboard.
- Use one Markdown file per chapter under the appropriate `materi/` category.
- Follow existing filenames and metadata conventions.
- Do not create duplicate chapters or invent missing curriculum IDs.
- Link only to documentation pages that exist or are explicitly planned.
- Never mark a chapter complete without the required evidence.

## Learning Materials

Every chapter should follow the established curriculum specification and include, where applicable:

- Objectives and prerequisites.
- Theory and architecture.
- Step-by-step implementation.
- Commands and configuration explanations.
- Verification and expected results.
- Troubleshooting and security review.
- Exercises, assessment, completion checklist, and official references.

Distinguish laboratory instructions from production procedures. Validate version-sensitive commands against the target Ubuntu release.

## MkDocs Integration

- Use `mkdocs.yml` and `docs/TECHNICAL-DESIGN.md` as the configuration references.
- Keep Markdown source files under `materi/`.
- Generate documentation under `site/materi/`.
- Publish the existing dashboard as `site/index.html`.
- Keep generated files separate from canonical source files.
- Preserve dashboard functionality, progress tracking, and responsive styling.
- Ensure dashboard links work with the configured GitHub Pages base path.
- Keep chapter IDs mapped consistently to their MkDocs URLs.
- Do not introduce broken links or overwrite source files during builds.

## Validation

After relevant changes:

1. Validate Markdown and configuration syntax.
2. Build MkDocs.
3. Run the integrated site build when dashboard or deployment files change.
4. Check affected navigation, links, assets, and JavaScript.
5. Run relevant tests and report actual results.
6. Summarize changed files, validation results, and remaining issues.

Use existing project scripts when available. Do not deploy to production unless explicitly requested.

## Task Workflow

1. Inspect relevant files.
2. Identify requirements and dependencies.
3. Make the smallest appropriate change.
4. Validate the change.
5. Report results and next steps.