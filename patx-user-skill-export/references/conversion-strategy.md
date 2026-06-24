# Conversion Strategy

The conversion goal is to preserve the source skill's patent business capability, not its engineering implementation. Preserve original Markdown prompts as much as possible and adapt only what PatX text-only skills require.

## Conversion Order

1. Identify the main Markdown entry:
   - Prefer `SKILL.md`.
   - Then prefer `README.md`, primary `.prompt`, or primary `.txt` files.
   - Treat YAML frontmatter as metadata, not runtime instructions.
2. Classify all Markdown-like files as one of: main prompt, workflow, checklist, output template, example, terms/glossary, customer style, test material, installation/development note, or unrelated material.
3. Classify non-Markdown files by purpose using `non-md-content-handling.md`.
4. Convert the main Markdown prompt first. Non-Markdown content may supplement it but must not rewrite or override it.
5. Restructure into PatX `readme_content` plus `items` using `platform-tree-and-reporting.md`.
6. Produce a brief conversion report only outside the skill JSON.

## Markdown-First Preservation

Keep source Markdown wording verbatim where possible. Do not summarize or rewrite core prompt text merely to make it stylistically cleaner.

Allowed adaptations:

- remove YAML frontmatter;
- remove or rewrite file-path references into PatX content item names;
- remove unsupported tool/script execution promises;
- remove installation, environment, and development-only instructions;
- remove unsafe, advertising, non-patent, or unrelated content;
- add short reading navigation that explains mandatory and conditional content;
- split or move sections to match PatX folder/content structure.

Do not casually change:

- patent reasoning logic;
- output format requirements;
- quality standards;
- term definitions;
- examples and counterexamples;
- customer style rules;
- missing-information questions;
- prohibitions and risk-control rules.

## Mandatory vs Conditional Content

Mandatory content should be read for every invocation. It includes:

- task scope and boundaries;
- input requirements and missing-information handling;
- core workflow steps;
- output format;
- patent/legal risk control;
- prohibitions;
- rules the source prompt says must always be followed.

Conditional content should be read only in specific situations. It includes:

- templates for a specific output type;
- examples and counterexamples;
- customer or jurisdiction style details;
- stage-specific rules such as claims, specification, OA response, drawings, or search;
- long checklists used only during review.

Do not split mandatory content into many optional-looking files unless length forces it. If mandatory content is split, name the files clearly, such as `必读-核心流程` and `必读-输出格式与禁止事项`.

## Reading Navigation

Every exported skill should include a short reading navigation in `readme_content` or the first content item. Use it to say which items are mandatory and which are conditional. Do not add platform-adaptation explanations to the skill instructions; put conversion loss or adaptation notes only in the external conversion report.

Example pattern:

```markdown
## 使用方式

每次调用本技能时，必须先阅读：
1. 《核心执行规则》
2. 《输出格式与风险控制》

然后根据任务选择阅读：
- 涉及权利要求：阅读《权利要求处理规则》
- 涉及说明书：阅读《说明书处理规则》
- 涉及 OA 答复：阅读《OA答复规则》
- 需要固定格式：阅读《输出模板》
- 需要参考写法：阅读《示例与反例》
```

Adapt names to the actual exported items. Do not add irrelevant branches.

## Folder and Content Grouping

Group content by use case, not by original technical path when that path is an implementation artifact.

Recommended groupings:

- `核心规则` for mandatory prompt, workflow, boundaries, and output rules;
- `场景规则` for claims, specification, OA response, drawings, search, or audit branches;
- `模板与示例` for output templates, examples, and counterexamples;
- `质量检查` for review checklists and risk checks;
- `术语与风格` for terms, forbidden wording, customer style, and naming rules.

Create a folder only when it contains multiple related conditional/reference content items. If a section is mandatory and short, use a top-level content item instead of hiding it in a folder.

## Conflict Handling

When source materials conflict:

1. `SKILL.md` or the main prompt has priority over supplemental files.
2. Files explicitly referenced by the main prompt have priority over unreferenced files.
3. Specific scenario rules have priority over generic rules for that scenario.
4. Safer patent/legal risk-control rules have priority over convenience rules.
5. If the conflict cannot be resolved, preserve the original conflicting wording where safe and note the conflict briefly in the conversion report.

Non-Markdown files never override the main Markdown prompt. They can only supplement, convert into checklists/templates, or be discarded.
