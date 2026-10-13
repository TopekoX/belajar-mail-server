# Task: Rebuild MkDocs for Mail Server Ubuntu Learning Portal

Recreate the MkDocs documentation setup for the existing project from scratch because the previous MkDocs configuration has been removed.

## Instructions

1. Inspect `CLAUDE.md`, `docs/PRD.md`, `docs/TECHNICAL-DESIGN.md`, `docs/project-audit.md`, the repository structure, the HTML dashboard, and all existing Markdown learning materials.
2. Determine the intended architecture from the current project files. Treat existing project decisions as the source of truth; do not blindly follow external examples or invent a new architecture.
3. Recreate the necessary MkDocs configuration, dependencies, navigation, theme, plugins, Markdown extensions, and build integration based on the actual project requirements.
4. Preserve all existing learning materials, folder structures, filenames, content, and dashboard functionality.
5. Integrate MkDocs with the existing curriculum dashboard according to the established project architecture. Ensure links between the dashboard and learning materials use the correct URLs.
6. Reuse existing deployment workflows and project scripts where possible. Modify only what is necessary.
7. Keep the implementation minimal, maintainable, and token-efficient. Do not create duplicate configuration files or rewrite unrelated documentation.
8. If an essential architectural decision cannot be determined from the repository, choose the safest minimal solution and explicitly report the assumption.

## Validation

- Install or verify the required dependencies.
- Run the MkDocs build.
- Verify navigation, search, Markdown rendering, code blocks, and representative material URLs.
- Verify the dashboard and its links remain functional.
- Check that generated files do not overwrite source files.
- Fix errors found during validation and rerun the relevant checks.
- Report only tests that were actually executed.

## Documentation

Update the existing technical documentation and project audit only where necessary to reflect the rebuilt configuration and actual validation results. Keep `CLAUDE.md` concise.

## Final Report

Summarize the files created or modified, the resulting architecture, local development and build commands, validation results, and any remaining deployment issues.

Proceed with implementation, not just a proposal or audit. Do not stop after creating the configuration files.