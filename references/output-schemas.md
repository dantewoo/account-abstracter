# 输出 Schema 定义

本文档定义各层输出的 JSON Schema，确保数据结构一致。

---

## Layer 1 输出：账号基础档案

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AccountProfile",
  "type": "object",
  "properties": {
    "account_name": {
      "type": "string",
      "description": "用户确认的账号名"
    },
    "platforms": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "platform": {
            "type": "string",
            "enum": ["微信公众号", "微博", "小红书", "知乎", "B站", "抖音", "Twitter/X", "其他"]
          },
          "platform_url": {
            "type": "string",
            "description": "账号在该平台的主页链接"
          },
          "bio": {
            "type": "string",
            "description": "账号简介"
          },
          "tags": {
            "type": "array",
            "items": { "type": "string" },
            "description": "定位标签"
          },
          "followers_count": {
            "type": "string",
            "description": "粉丝量级（如'10w+'，精确数字可能不可得）"
          },
          "content_frequency": {
            "type": "string",
            "description": "内容发布频率描述"
          },
          "verification": {
            "type": "string",
            "description": "认证信息"
          },
          "recent_titles": {
            "type": "array",
            "items": { "type": "string" },
            "description": "近期3-5条内容标题"
          }
        }
      }
    },
    "identity_confirmed": {
      "type": "boolean",
      "description": "是否经过用户身份确认"
    },
    "search_notes": {
      "type": "string",
      "description": "搜索过程中的备注（如登录要求、反爬情况等）"
    },
    "data_quality": {
      "type": "string",
      "enum": ["充足", "有限", "不足"],
      "description": "检索数据量评估"
    }
  },
  "required": ["account_name", "platforms", "identity_confirmed"]
}
```

---

## Layer 2 输出：文本特征向量

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TextFeatureVector",
  "type": "object",
  "properties": {
    "works_analyzed": {
      "type": "integer",
      "description": "分析的作品数量"
    },
    "quality_tier": {
      "type": "string",
      "enum": ["粗略(1-2篇)", "基础(3-4篇)", "推荐(5-10篇)", "深度(10+篇)"],
      "description": "输入量对应的质量等级"
    },
    "title_patterns": {
      "type": "object",
      "properties": {
        "avg_length": { "type": "number" },
        "length_range": { "type": "string" },
        "dominant_sentence_type": { "type": "string" },
        "emotion_words": { "type": "array", "items": { "type": "string" } },
        "hook_types": { "type": "array", "items": { "type": "string" } },
        "structural_patterns": { "type": "array", "items": { "type": "string" } }
      },
      "description": "标题规律"
    },
    "opening_patterns": {
      "type": "object",
      "properties": {
        "dominant_hook": { "type": "string" },
        "hook_distribution": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "frequency": { "type": "number" }
            }
          }
        }
      },
      "description": "开头模式"
    },
    "closing_patterns": {
      "type": "object",
      "properties": {
        "dominant_pattern": { "type": "string" },
        "pattern_distribution": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "frequency": { "type": "number" }
            }
          }
        }
      },
      "description": "结尾模式"
    },
    "paragraph_structure": {
      "type": "object",
      "properties": {
        "avg_paragraph_length": { "type": "number" },
        "long_short_ratio": { "type": "string" },
        "uses_subheadings": { "type": "boolean" },
        "uses_lists": { "type": "boolean" },
        "transition_style": { "type": "string" }
      },
      "description": "段落结构"
    },
    "vocabulary": {
      "type": "object",
      "properties": {
        "top_words": { "type": "array", "items": { "type": "string" } },
        "signature_phrases": { "type": "array", "items": { "type": "string" } },
        "domain_jargon": { "type": "array", "items": { "type": "string" } }
      },
      "description": "高频词汇与表达"
    },
    "data_usage": {
      "type": "object",
      "properties": {
        "density": { "type": "string" },
        "source_types": { "type": "array", "items": { "type": "string" } },
        "presentation_style": { "type": "string" }
      },
      "description": "数据引用习惯"
    },
    "case_usage": {
      "type": "object",
      "properties": {
        "density": { "type": "string" },
        "case_types": { "type": "array", "items": { "type": "string" } },
        "case_length": { "type": "string" }
      },
      "description": "案例使用习惯"
    },
    "topic_clustering": {
      "type": "object",
      "properties": {
        "core_topics": { "type": "array", "items": { "type": "string" } },
        "evergreen_topics": { "type": "array", "items": { "type": "object" } },
        "occasional_topics": { "type": "array", "items": { "type": "object" } },
        "breadth": { "type": "string" }
      },
      "description": "内容主题聚类"
    },
    "cta_patterns": {
      "type": "object",
      "properties": {
        "dominant_type": { "type": "string" },
        "phrases": { "type": "array", "items": { "type": "string" } },
        "position": { "type": "string" },
        "frequency": { "type": "string" }
      },
      "description": "互动/CTA模式"
    },
    "length_rhythm": {
      "type": "object",
      "properties": {
        "typical_range": { "type": "string" },
        "average": { "type": "number" },
        "distribution_pattern": { "type": "string" }
      },
      "description": "篇幅规律"
    },
    "emotion_arc": {
      "type": "object",
      "properties": {
        "dominant_type": { "type": "string" },
        "arc_distribution": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "frequency": { "type": "number" }
            }
          }
        }
      },
      "description": "情感弧线"
    },
    "layout_habits": {
      "type": "object",
      "properties": {
        "paragraph_density": { "type": "string" },
        "emoji_frequency": { "type": "string" },
        "emoji_types": { "type": "array", "items": { "type": "string" } },
        "separator_usage": { "type": "string" },
        "emphasis_style": { "type": "string" }
      },
      "description": "排版习惯"
    },
    "confidence_map": {
      "type": "object",
      "additionalProperties": {
        "type": "string",
        "enum": ["高", "中", "低"]
      },
      "description": "各维度的置信度标签"
    }
  },
  "required": ["works_analyzed", "quality_tier", "confidence_map"]
}
```

---

## Layer 3 输出：综合画像

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CreatorProfile",
  "type": "object",
  "properties": {
    "account_name": { "type": "string" },
    "profile_dimensions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dimension": { "type": "string" },
          "conclusion": { "type": "string" },
          "confidence": { "type": "string", "enum": ["高", "中", "低"] },
          "evidence": { "type": "string" },
          "data_source": { "type": "string", "enum": ["文本分析", "检索信息", "综合"] }
        }
      }
    },
    "data_alignment_notes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "数据对齐中的矛盾和标记"
    },
    "style_evolution": {
      "type": "object",
      "properties": {
        "available": { "type": "boolean" },
        "trends": { "type": "array", "items": { "type": "string" } },
        "current_characteristics": { "type": "string" }
      },
      "description": "风格演进追踪（可选）"
    },
    "user_confirmed": {
      "type": "boolean",
      "description": "是否经过用户确认"
    },
    "user_modifications": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dimension": { "type": "string" },
          "original": { "type": "string" },
          "modified": { "type": "string" }
        }
      },
      "description": "用户修改记录"
    }
  },
  "required": ["account_name", "profile_dimensions", "user_confirmed"]
}
```

---

## Layer 4 输出：Skill 封装结果

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SkillPackage",
  "type": "object",
  "properties": {
    "skill_file_path": { "type": "string" },
    "account_name": { "type": "string" },
    "file_format": { "type": "string", "enum": ["markdown+frontmatter", "yaml"] },
    "sections_included": {
      "type": "array",
      "items": { "type": "string" }
    },
    "validation_result": {
      "type": "object",
      "properties": {
        "passed": { "type": "boolean" },
        "errors": { "type": "array", "items": { "type": "string" } },
        "warnings": { "type": "array", "items": { "type": "string" } }
      }
    },
    "backtest_result": {
      "type": "object",
      "properties": {
        "style_similarity": { "type": "number", "minimum": 0, "maximum": 1 },
        "structure_similarity": { "type": "number", "minimum": 0, "maximum": 1 },
        "vocabulary_similarity": { "type": "number", "minimum": 0, "maximum": 1 },
        "emotion_similarity": { "type": "number", "minimum": 0, "maximum": 1 },
        "overall_score": { "type": "number", "minimum": 0, "maximum": 1 },
        "notes": { "type": "string" }
      }
    }
  },
  "required": ["skill_file_path", "account_name", "validation_result"]
}
```
