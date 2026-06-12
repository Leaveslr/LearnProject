# Knowledge Core

这是个人学习和领域知识沉淀仓库。

它负责把零散输入逐步变成可复习、可教学、可导出的知识资产。内容生产仓库不直接消费原始笔记，而是消费这里导出的标准知识包。

## 主链路

```text
inbox -> Knowledge -> domains -> exports/knowledge-packs -> content-production-studio
```

## 目录

```text
knowledge-core/
├── inbox/                 # 新信息入口和前沿雷达
├── Knowledge/             # 个人知识库，允许自由记录和临时沉淀
├── domains/               # 长期维护的领域知识体系
│   ├── llm-ai/
│   │   └── llm-knowledge-book/
│   └── quant-finance/
├── exports/
│   └── knowledge-packs/   # 给内容生产系统消费的标准知识包
├── templates/             # 知识包、专题、雷达模板
└── docs/                  # 仓库治理和流程文档
```

## 边界

- `inbox/` 放未判断价值的新信息。
- `Knowledge/` 放个人学习记录、灵感、调研、草稿和上下文。
- `domains/` 放已经决定长期维护的领域知识体系。
- `exports/knowledge-packs/` 放可交付给内容生产系统的稳定知识包。

## 当前领域

- `domains/llm-ai/`：LLM、Agent、RAG、AI 工程和相关学习体系。
- `domains/quant-finance/`：金融量化学习、研究、策略、回测、风控和项目实践。

## 知识包规则

知识包是本仓库和内容生产仓库之间的接口。只有成熟到可以被讲解、写作或视频化的知识，才进入 `exports/knowledge-packs/`。

每个知识包建议包含：

```text
metadata.yaml
knowledge-card.md
teaching-brief.md
examples.md
misconceptions.md
references.md
```

状态建议使用：

- `draft`
- `reviewed`
- `ready-for-production`
- `deprecated`
