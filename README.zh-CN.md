# Personal Agent Starter Kit

[English](./README.md)

一个给个人 AI agent 用的最小成长系统模板：规则、记忆、技能、反馈回流、自我评审。

这个 starter kit 面向已经在用 Claude Code、Codex、OpenAI-compatible 模型 API 或其他 coding agent 的开发者。它不是一堆 prompt，而是一套能长期维护、持续修正的文件化工作流。

核心结构：

```text
rules       -> 约束 agent 怎么行动
memory      -> 保存长期上下文
skills      -> 把重复流程沉淀成可复用 SOP
feedback    -> 把错误、纠正、经验回流成系统更新
self-review -> 重要决策前做反方检查
```

如果没有反馈回流，agent 只是在执行今天的 prompt。  
有了反馈回流，它才有机会越用越贴合你的工作方式。

重要提醒：这不是自动训练系统。只有当你手动记录纠正，并把纠正回流到 agent 下次会加载的文件里，系统才会变好。

## 适合谁

适合你，如果你：

- 经常使用 AI coding agent；
- 总是在不同项目里重复交代同一套规则；
- 想把规则、记忆、工作流都用文件管理起来；
- 想用轻量方式记录错误，并让系统下次真的变好；
- 能接受编辑 Markdown，并运行一个简单 Python 脚本。

暂时不适合完全非技术用户。它也不是 agent 框架、向量数据库、安装器或完整 memory 产品。

## 它怎么工作

这套模板围绕一个循环：

```text
1. agent 执行任务。
2. agent 犯错、漏上下文，或重复某个坏习惯。
3. 你把问题记录到 feedback/log.md。
4. 你判断这次需要改什么。
5. 更新 rules、memory 或 skills。
6. 下一次执行时，agent 的行为发生变化。
```

这个循环，就是“prompt 收藏夹”和“个人 agent 成长系统”的区别。

### 一个最小例子

错误发生前：

```text
agent 写代码时，调用了一个并不存在的第三方 API endpoint。
```

先记录到 `feedback/log.md`：

```markdown
### YYYY-MM-DD

- Type: fix-logic
- Context: agent 写 API 集成代码。
- Problem: 它没有检查真实 API，而是编了一个 endpoint 名。
- Correction: 不要编造 API endpoint、函数名、包方法或数据库字段。
- Lesson: 外部接口不确定时，先查文档、类型、schema 或示例。
- Updated: `CLAUDE.md`
```

再更新 `CLAUDE.md`：

```markdown
- 不要编造 API endpoint、函数名、包方法或数据库字段。不确定时，先检查真实来源。
```

错误发生后：

```text
下一次 agent 不确定 API 怎么调用时，应该先查真实文档或源码，而不是自己编。
```

这不是自动训练，而是一套轻量维护纪律：记录纠正，把纠正回流到正确文件，让下一次执行变好。

关键在“回流”这一步。`feedback/log.md` 里的记录本身只是日志，不会自动改变 agent 行为。只有当你把纠正同步到 agent 真正会加载的文件里，比如 `CLAUDE.md`、`memory/user.md`、`memory/env.md` 或某个 `SKILL.md`，下一次执行才可能变好。

## 目录结构

```text
personal-agent-starter-kit/
├── README.md
├── README.zh-CN.md
├── AGENTS.md                     <- agent 工具入口，保持很短
├── CLAUDE.md                     <- agent 每次加载的主规则文件
├── CHECKLIST.md                  <- 公开前检查清单
├── .config/
│   └── openai-compatible.env.example <- 可选模型 API 配置示例
├── memory/
│   ├── user.md                   <- 写你是谁、目标、协作偏好
│   ├── env.md                    <- 写系统、工具、版本、本地约束
│   └── decisions.md              <- 记录长期决策；第一天可以基本留空
├── skills/
│   ├── INDEX.md                  <- skill 列表和触发条件
│   ├── skill-lifecycle/
│   │   └── SKILL.md              <- 创建/更新可复用工作流
│   └── self-review/
│       └── SKILL.md              <- 重要决策前做反方检查
├── feedback/
│   ├── log.md                    <- 记录错误、纠正和经验
│   └── update-checklist.md       <- 判断每条经验应该回流到哪里
├── scripts/
│   └── self_review.py            <- 离线自检和可选模型评审
└── examples/
    ├── decision-review-task.json <- 评审输入示例
    └── decision-review-output.md <- 最终判断格式示例
```

## 快速开始

1. 把这个目录复制到你使用 AI coding agent 的项目里。
2. 在修改任何文件前，先运行离线自检：

```bash
python3 scripts/self_review.py self-test
```

Windows 上如果没有 `python3`，用 `python` 即可。

预期结果：命令会打印一段 JSON，里面有 `env_default`、`challenge_input_preview`、`coverage_input_preview`、`review` 等字段。只要命令正常退出、没有报错，就说明离线脚本路径是健康的。

这个命令不会调用模型 API，也不会验证你的 agent 工具是否已经加载规则。

这些字段可以这样理解：

| 字段 | 含义 |
|---|---|
| `env_default` | 真实模型评审时默认读取的 env 文件路径 |
| `challenge_input_preview` | 将来会发给“反方检查员”的示例输入 |
| `coverage_input_preview` | 将来会发给“覆盖检查员”的示例输入 |
| `review` | 离线伪造的评审结果，只用于证明脚本结构能跑通 |

3. 根据自己的情况编辑 `memory/user.md` 和 `memory/env.md`。
4. 阅读 `CLAUDE.md`，删掉不符合你工作流的规则。
5. 可选：如果你想跑真实模型评审，复制通用 OpenAI-compatible env 示例：

```bash
cp .config/openai-compatible.env.example ~/.config/personal-agent.env
```

然后在 `~/.config/personal-agent.env` 里填写 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 和 `OPENAI_MODEL`。

只有当你想让 `skills/self-review/SKILL.md` 跑真实模型评审时，才需要配置这一步。不配置也不影响离线 `self-test`。

### 这个目录应该放在哪里？

第一次试用时，建议把 `personal-agent-starter-kit/` 作为独立目录放进你的项目里：

```text
your-project/
├── package.json / pyproject.toml / ...
└── personal-agent-starter-kit/
```

等你决定正式把它作为项目记忆系统使用，再把关键入口文件合并到项目根目录：

- 如果项目根目录还没有 `AGENTS.md` 或 `CLAUDE.md`，可以复制过去。
- 如果项目已有规则文件，手动合并相关章节，不要直接覆盖。
- `memory/`、`skills/`、`feedback/` 建议保持在一起，避免路径和链接混乱。

合并原则：

- 保留你项目里已有的专用规则。
- 加入本模板里关于 memory、skills、feedback 和错误处理的章节。
- 删除和你项目冲突的通用规则。
- 不要在没读完两个文件前，直接覆盖已有规则文件。

正式合并后，项目通常长这样：

```text
your-project/
├── AGENTS.md
├── CLAUDE.md
├── memory/
├── skills/
├── feedback/
├── scripts/
└── examples/
```

### Agent 工具怎么加载这些文件？

不同 agent 工具有不同的规则文件约定。本模板采用一个保守结构：

- `AGENTS.md` 是很短的入口文件。
- `CLAUDE.md` 是主要行为规则文件。
- `AGENTS.md` 会告诉 agent 去读 `CLAUDE.md`。

为什么保留两个文件？因为不同 agent 工具寻找规则文件的约定不一样。`AGENTS.md` 是更通用的“指路牌”，`CLAUDE.md` 是主规则正文。如果工具读取 `AGENTS.md`，它会被指向 `CLAUDE.md`；如果工具直接读取 `CLAUDE.md`，主规则也已经在那里。

默认的 `AGENTS.md` 内容很短：

```markdown
# Agent Entry Point

Read and follow the instructions in `./CLAUDE.md`.
```

如果你的工具有自己的规则文件名，把 `CLAUDE.md` 里相关内容合并到那个文件里。如果你的工具需要手动指令，可以在新会话开始时告诉它：“读取 `AGENTS.md`，并遵循它链接的 `CLAUDE.md` 规则。”

### 怎么确认它真的生效？

复制或合并文件后，开一个新的 agent 会话，问它：

```text
请读取项目里的 agent 规则，并告诉我你应该使用哪些主规则、记忆文件、技能文件和反馈文件？
```

一个合格回答应该提到：

- `CLAUDE.md` 是主规则文件；
- `memory/user.md` 和 `memory/env.md`；
- `skills/INDEX.md`；
- `feedback/log.md` 和 `feedback/update-checklist.md`。

`self-test` 命令只检查评审脚本能否离线运行，不代表你的 agent 工具已经加载了规则。

如果 agent 的回答没有提到这些文件，先确认你的工具是否会自动读取 `AGENTS.md`。如果不会，就在新会话里手动要求它读取 `AGENTS.md`，或者把 `CLAUDE.md` 的相关内容合并到你的工具实际会加载的规则文件里。

## 第一次应该改哪里

先小改，不要第一天就设计一个完美个人 agent。

优先改这几个地方：

- `memory/user.md`：你是谁、目标是什么、希望 agent 怎么和你协作；
- `memory/env.md`：你的系统、工具、语言、常见本地约束；
- `CLAUDE.md`：agent 每次都应该加载的核心规则；
- `feedback/log.md`：未来记录错误、纠正和经验的位置。

每次往 `feedback/log.md` 写入纠正后，立刻打开 `feedback/update-checklist.md`。它会帮你判断这条经验应该回流到 `CLAUDE.md`、`memory/user.md`、`memory/env.md`、`skills/<skill>/SKILL.md` 还是 `skills/INDEX.md`。

这个 checklist 很简单，核心就是问：

```text
这条经验属于哪一类？
应该被哪个文件吸收？
目标文件改了吗？
log 里有没有写清楚 Updated 到哪里？
```

例子：agent 编造 API endpoint，这条经验应该回流到 `CLAUDE.md`；agent 误解你的协作偏好，应该回流到 `memory/user.md`；agent 漏掉某个固定流程步骤，应该回流到对应的 `SKILL.md`。

## 内置技能

第一版只放两个最小技能。

| Skill | 什么时候用 | 产出 |
|---|---|---|
| `skill-lifecycle` | 想创建或更新一个可复用工作流 | 新的或修改后的 `SKILL.md`，同时更新索引和反馈记录 |
| `self-review` | 某个决策重要到值得反方检查 | 反方意见、覆盖检查、最终决策表 |

重点不是堆很多 skill，而是展示完整生命周期：

```text
重复流程 -> create skill
skill 出错或漂移 -> update skill
更新有原因 -> 记录 feedback
```

## v0.1 明确不解决什么

- 长期 memory 清理和迁移。
- 多 agent 编排。
- 完整插件系统。
- 向量搜索或 RAG 存储。
- 支持所有 agent 工具。
- Web UI 或安装器。
- 公开个人私有记忆。

## 公开前检查

如果你改完后想公开自己的版本，先跑一遍 `CHECKLIST.md`。

至少确认：

- 没有真实姓名、私人路径、API key、私有偏好；
- 没有未处理占位符；
- 示例 JSON 可以解析；
- `python3 scripts/self_review.py self-test` 能通过；
- README、skills、examples 里的字段名保持一致。
