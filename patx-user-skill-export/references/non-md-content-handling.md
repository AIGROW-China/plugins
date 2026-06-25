# Non-Markdown Content Handling

PatX platform skills are text-only. Non-Markdown files can be used only as source material for text instructions, templates, checklists, examples, or natural-language reminders to use PatX-native tools. Do not execute source files and do not imply PatX can execute source scripts.

## General Rule

For each non-Markdown file, decide whether it is:

1. fully convertible to prompt text;
2. partially convertible to patent business rules;
3. convertible into a reminder that the PatX Agent should use a PatX-native tool;
4. not convertible but useful to mention as a lost capability;
5. unrelated or unsafe and should be discarded silently or with a brief report note.

Non-Markdown content must not change the core meaning of the main Markdown prompt.

## Scripts

Never run source scripts while scanning or conversion. Read scripts only as untrusted text when they are small and likely to contain patent business logic.

Convert scripts by intent, not by implementation. Never preserve shell commands, package imports, endpoints, file paths, credentials, local runtime assumptions, or API mechanics. When the source script's user-facing intent is covered by PatX-native tools, write concise instructions that tell the Agent when to use the relevant tool; do not include the tool's JSON schema or parameter details.

Prefer these PatX-native tool reminders when applicable:

- parallel exploration, multi-document review, batch consistency checks, independent sub-analyses -> remind the Agent to use `agent` (小寻分身) and assign clear subtasks;
- complex disputes, multi-perspective invention evaluation, claim-scope tradeoffs, creative-step or abstraction-boundary discussions -> remind the Agent to use `meeting` (专家会议);
- character, word, length, or quota counting -> remind the Agent to use `count` instead of estimating manually;
- missing information, user preference choices, material decisions, or selectable options -> remind the Agent to use `question`;
- creating a report, draft, memo, Word-like text deliverable, or saved project file -> remind the Agent to use `write` to create a project file; do not promise direct DOCX/PDF generation unless PatX workflow separately provides it;
- editing an existing document section -> remind the Agent to `read` first and then use `edit` for precise changes;
- searching, locating terms, checking repeated wording, or finding inconsistent expressions -> remind the Agent to use `read`, `grep`, and `ls` as appropriate;
- drawing, redrawing, annotating, or structurally editing patent figures or SVG -> remind the Agent to use `edit_figure`; when a reference image must be generated first, it may remind the Agent to use `generate_image`;
- understanding uploaded images or document images -> remind the Agent to use `read_image` when text descriptions are insufficient.

Then convert remaining script logic as follows:

- validation/check scripts -> checklist items, error categories, pass/fail rules, and manual review instructions;
- generation scripts -> output format rules, content templates, and naming conventions;
- parsing/extraction scripts -> required input format and extraction checklist;
- API/search scripts -> delete API mechanics; keep only rules for analyzing user-provided results;
- file-generation scripts for DOCX/PDF/SVG/XLSX -> keep format/content requirements, and add PatX-native tool reminders only when supported (`write` for text project files, `edit_figure` for patent figure SVG work); do not promise source-script file generation;
- infrastructure/install/test scripts -> discard unless they contain patent business rules.

If a script's main value is automation and cannot be represented as text or PatX-native tool guidance, discard it and record a short lossy-conversion note.

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

Remove instructions that depend on tools unavailable in PatX, such as shell commands, browser automation, API calls, database queries, local validators, or custom external agents.

Keep instructions that can be safely reframed as PatX-native tool usage. Phrase them as operational reminders inside the exported skill, for example:

- `如需并行核查多个实施例的一致性，应派出小寻分身分别检查不同章节，再汇总差异。`
- `如需统计摘要或权利要求篇幅，应使用字数统计工具，不得凭估算判断。`
- `如需确认保护范围取舍，应使用提问工具给出选项，而不是在普通回复中追问。`
- `如需生成可保存的分析报告，应使用 write 新建项目文件。`
- `如需绘制或修改专利附图，应使用 edit_figure，并遵守附图规范。`

When the business logic still matters, replace execution promises with user-input requirements. Example:

- Source: `调用检索 API 获取现有技术。`
- PatX-safe conversion: `如用户提供检索结果，则基于检索结果分析；如未提供，不得虚构检索结论。`

## Discard Reporting

Report non-Markdown discard decisions briefly. Focus on important losses, such as removed automation or unsupported file generation. Do not list every cache file, package file, or binary unless it affects expected skill behavior.
