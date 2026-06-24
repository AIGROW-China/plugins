# PatX Platform Tree and Reporting

PatX user skills are text-only and have a shallow tree.

## Platform Tree Rules

The exported `items` array must obey these rules:

- `folder` items are top-level only: their `parent_node_key` must be `null`.
- `content` items may be top-level or directly under a folder.
- A folder may contain only content items.
- Do not create folders under folders.
- Do not put children under content items.
- Each skill must include at least one content item.
- Each content item must have non-empty text.
- Keep item names short, descriptive, and user-facing.

Flatten deeper source structures. For example:

- Source `references/spec/examples/good.md` can become folder `模板与示例` + content `说明书优秀示例`.
- Source `rules/claims/checklist.md` can become folder `质量检查` + content `权利要求检查清单`.

## Readme Content

`readme_content` should contain:

- concise skill purpose;
- reading navigation;
- mandatory vs conditional content guidance.

Do not put the conversion report into `readme_content` unless the note is necessary for runtime behavior. The report is for the user, not for the skill itself.

## Item Organization

Prefer this order when applicable:

1. top-level mandatory content items;
2. scenario-rule folders;
3. template/example folders;
4. quality-check folders;
5. terms/style folders.

Use top-level content for core mandatory rules. Use folders only to group multiple related conditional/reference items.

## Brief Conversion Report

After export, provide a concise report. Usually include only:

- converted skill name and source path;
- validation result;
- major preserved content groups;
- important removed unsafe, non-patent, or unsupported content;
- important lossy conversions, especially scripts/tools/API/file generation that became text rules or were discarded.

Keep the report short. Expand only when there is a material risk that the converted PatX skill behaves differently from the source.

Suggested format:

```markdown
转换报告：
- 已转换：<skill name>
- 校验：VALID / INVALID: <reason>
- 保留：主提示词、核心流程、输出模板、质量检查
- 调整：脚本校验逻辑已转为文字检查清单
- 舍弃：安装命令、缓存文件、无关广告内容
- 注意：原技能的自动文件生成能力在 PatX 中不可执行
```
