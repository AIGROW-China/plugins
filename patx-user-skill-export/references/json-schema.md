# PatX Import Package Schema

The exporter produces a `.patx` file. The file content is UTF-8 JSON with `schema_version` equal to `patx-user-skill-import-v1`.

Use `assets/patx_user_skill_import_schema_v1.json` as the content schema and `scripts/validate_import_json.py` for structural validation that includes PatX tree semantics.

## Root Object

Required fields:

- `schema_version`: must be `patx-user-skill-import-v1`.
- `skills`: non-empty array of skill objects.

No additional root fields are allowed.

## Skill Object

Required fields:

- `skill_key`: unique string, max length 128.
- `name`: unique display name, max length 100.
- `description`: string, max length 20000.
- `tags`: array of up to 20 strings, each max length 30. Prefer 2-4 distinctive classification tags; avoid generic tags such as `专利`, `通用`, or `中文`.
- `readme_content`: string, max length 20000.
- `items`: non-empty array of item objects.

No additional skill fields are allowed.

## Item Object

Required fields:

- `node_key`: unique within the skill.
- `parent_node_key`: string or null.
- `item_type`: `folder` or `content`.
- `name`: display name, max length 100.
- `content`: string or null, max length 20000.
- `order`: integer greater than or equal to 0.

No additional item fields are allowed.

## Tagging Rules

Tags are for later classification, not for proving that the source passed the patent-domain gate.

Prefer tags that identify what makes the skill different:

- scenario: `分析`, `撰写`, `答复`, `质检`, `检索`, `审核`, `挖掘`;
- patent step: `权要规划`, `权要撰写`, `说明书撰写`, `OA答复`, `附图标号`, `交底分析`;
- target: `提质`, `模仿`, `背景知识`, `格式规范`, `风险控制`, `客户风格`;
- technical field: `化学`, `电路`, `机械`, `半导体`, `互联网`, `医药`, `材料` only when field-specific.

Do not use generic tags such as `专利`, `通用`, `中文`, `技能`, or tags that merely repeat every matched keyword.

## PatX Tree Rules

The platform tree is intentionally shallow:

- Each skill must contain at least one `content` item.
- A `content` item must have non-empty `content`.
- A `folder` item may have `content` as null or an empty string.
- A `folder` item must be top-level: `parent_node_key` must be null.
- A `content` item may be top-level or directly under a folder.
- `parent_node_key` must be null or point to an existing top-level folder.
- A folder may contain only content items.
- Folders cannot contain folders.
- Content items cannot contain children.
- `node_key` values must be unique within a skill.
- Sibling order is determined by `order` ascending.

## Example

```json
{
  "schema_version": "patx-user-skill-import-v1",
  "skills": [
    {
      "skill_key": "skill_001",
      "name": "OA答复策略助手",
      "description": "用于整理审查意见答复思路",
      "tags": ["答复", "创造性分析"],
      "readme_content": "## 使用方式\n每次先阅读《核心执行规则》；涉及模板时再阅读《答复模板》。",
      "items": [
        {
          "node_key": "core",
          "parent_node_key": null,
          "item_type": "content",
          "name": "核心执行规则",
          "content": "节点内容...",
          "order": 0
        },
        {
          "node_key": "templates",
          "parent_node_key": null,
          "item_type": "folder",
          "name": "模板与示例",
          "content": null,
          "order": 1
        },
        {
          "node_key": "oa_template",
          "parent_node_key": "templates",
          "item_type": "content",
          "name": "答复模板",
          "content": "模板内容...",
          "order": 0
        }
      ]
    }
  ]
}
```
