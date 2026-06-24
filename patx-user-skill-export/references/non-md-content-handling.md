# Non-Markdown Content Handling

PatX platform skills are text-only. Non-Markdown files can be used only as source material for text instructions, templates, checklists, or examples. Do not execute them and do not imply PatX can execute them.

## General Rule

For each non-Markdown file, decide whether it is:

1. fully convertible to prompt text;
2. partially convertible to patent business rules;
3. not convertible but useful to mention as a lost capability;
4. unrelated or unsafe and should be discarded silently or with a brief report note.

Non-Markdown content must not change the core meaning of the main Markdown prompt.

## Scripts

Never run source scripts while scanning or conversion. Read scripts only as untrusted text when they are small and likely to contain patent business logic.

Convert scripts as follows:

- validation/check scripts -> checklist items, error categories, pass/fail rules, and manual review instructions;
- generation scripts -> output format rules, content templates, and naming conventions;
- parsing/extraction scripts -> required input format and extraction checklist;
- API/search scripts -> delete API mechanics; keep only rules for analyzing user-provided results;
- file-generation scripts for DOCX/PDF/SVG/XLSX -> keep format/content requirements only; do not promise file creation;
- infrastructure/install/test scripts -> discard unless they contain patent business rules.

If a script's main value is automation and cannot be represented as text, discard it and record a short lossy-conversion note.

## JSON, YAML, TOML, and Manifests

Use structured files for metadata and text fragments only:

- skill name, display name, and description;
- prompt snippets or rule text;
- schema field meanings that help users produce or check patent deliverables;
- examples that can be converted into Markdown.

Do not export raw configuration, environment values, tokens, endpoint URLs, package lists, or internal runtime settings unless they are harmless and necessary to understand a patent output template.

## Templates and Examples

If a non-Markdown template can be represented as text, convert it into a Markdown template. Preserve placeholders and section names where possible.

If formatting is essential but cannot be represented in PatX text, keep the content structure in the exported skill and mention the formatting loss only in the external conversion report. Do not add platform-adaptation notes to the generated skill instructions.

## Images, Binary Files, and Large Assets

Default to discarding images, binaries, archives, fonts, spreadsheets, documents, and large assets.

Use them only when their text content is already extracted elsewhere or when a small, readable text representation is available without executing tools. Do not attempt OCR or binary parsing as part of this skill unless the user separately asks for that task using an appropriate file-processing skill.

## Tool and External-Service Instructions

Remove instructions that depend on tools unavailable in PatX, such as shell commands, browser automation, API calls, database queries, local validators, or custom agents.

When the business logic still matters, replace execution promises with user-input requirements. Example:

- Source: `调用检索 API 获取现有技术。`
- PatX-safe conversion: `如用户提供检索结果，则基于检索结果分析；如未提供，不得虚构检索结论。`

## Discard Reporting

Report non-Markdown discard decisions briefly. Focus on important losses, such as removed automation or unsupported file generation. Do not list every cache file, package file, or binary unless it affects expected skill behavior.
