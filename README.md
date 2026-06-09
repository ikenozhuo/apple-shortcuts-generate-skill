# Shortcuts Generator — Apple Shortcuts 编程化创建工具

[![macOS](https://img.shields.io/badge/macOS-≥14.0-blue?logo=apple)](https://support.apple.com/shortcuts)
[![Python](https://img.shields.io/badge/Python-≥3.10-blue?logo=python)](https://python.org)

**以代码驱动的方式创建、验证、签名、解包和审查 macOS/iOS Apple Shortcuts。**

告别手动拖拽 —— 用 JSON 描述你的自动化流程，一键生成 `.shortcut` 文件，并利用 macOS `shortcuts` CLI 签名后直接导入设备。

---

## 目录

- [为什么用这个？](#为什么用这个)
- [快速开始](#快速开始)
- [工作流概览](#工作流概览)
- [脚本参考](#脚本参考)
- [参考文档](#参考文档)
- [JSON Spec 格式](#json-spec-格式)
- [作为 AI Agent Skill 安装](#作为-ai-agent-skill-安装)
- [高级模式](#高级模式)
- [常见问题](#常见问题)

---

## 为什么用这个？

| 场景 | 手动 Shortcuts.app | Shortcuts Generator |
|------|-------------------|---------------------|
| 创建复杂流程 | 拖拽 + 配置，易出错 | JSON 描述，可版本控制 |
| 批量/重复性创建 | 逐个手动 | 脚本化批量生成 |
| 团队协作 | 无法 diff | `.shortcut` 可 diff |
| 验证 | 运行才能知道对不对 | 静态验证，提前发现错误 |
| 使用 AI 生成 | ❌ 无法直接生成 | JSON spec → 签名文件一步到位 |

---

## 作为 AI Agent Skill 安装

本项目核心是一个 **AI Agent Skill** —— 让 Claude Code、Codex 等 AI Agent 能够自动生成、验证和签名 Apple Shortcuts。

### 安装

在任意项目目录下执行：

```bash
npx skills add https://github.com/ikenozhuo/apple-shortcuts-generate-skill.git
```

此命令会从 GitHub 拉取 skill 定义并注册到你的 Agent 环境中。安装完成后，Agent 便具备生成 Apple Shortcuts 的全部能力。

### 使用方法

安装后，直接在 Agent 会话中自然语言描述你想要创建的 Shortcut 即可：

> **例子**：
> *"帮我创建一个快捷指令，每天早上8点提醒我吃药"*
> *"为一个网页内容创建一个 HTML 审查界面的 Shortcut"*
> *"解包这个 signed.shortcut 文件，看看它的结构"*

Agent 会自动：
1. 查阅相关参考文档
2. 编写 JSON spec
3. 用 `build_shortcut.py` 生成 `.shortcut` 文件
4. 用 `validate_shortcut.py` 验证结构
5. 用 `shortcuts sign` 签名供导入


---

## 快速开始

### 前置条件

- macOS 14.0+（需要 `shortcuts` CLI）
- Python 3.10+

### 安装

```bash
git clone https://github.com/drewocarr/generate-shortcuts-skill.git
cd generate-shortcuts-skill
```

本项目是纯脚本工具，无需 `pip install` 或虚拟环境 —— 所有依赖均为 Python 标准库。

### 最简单的例子

创建一个输出 "Hello World" 的快捷指令：

**spec.json**
```json
{
  "name": "Hello World",
  "actions": [
    {
      "id": "is.workflow.actions.gettext",
      "params": {
        "UUID": "11111111-1111-1111-1111-111111111111",
        "WFTextActionText": "Hello World"
      }
    }
  ]
}
```

```bash
# 1. 生成 .shortcut 文件
python3 scripts/build_shortcut.py spec.json --output Hello.shortcut

# 2. 验证
python3 scripts/validate_shortcut.py Hello.shortcut
plutil -lint Hello.shortcut

# 3. 签名（生成可导入的文件）
shortcuts sign --mode anyone --input Hello.shortcut --output Hello_signed.shortcut
```

双击 `Hello_signed.shortcut` 即可导入。

---

## 工作流概览

```
用户需求 → JSON Spec → build_shortcut.py → .shortcut plist
                         ↓
                    validate_shortcut.py ←─── 发现问题？回到 JSON
                         ↓
                    plutil -lint
                         ↓
                    shortcuts sign → xxx_signed.shortcut → 导入 Shortcuts.app
```

对已签名的文件反向操作：

```
已签名的 .shortcut → extract_shortcut.py → 明文 XML plist → 编辑 → 重新签名
```

---

## 脚本参考

| 脚本 | 用途 | 关键特性 |
|------|------|---------|
| `scripts/build_shortcut.py` | JSON spec → `.shortcut` plist | 支持 XML / 二进制 plist，可内联签名 |
| `scripts/validate_shortcut.py` | 静态检查 plist | 检查 UUID 格式、变量引用、控制流闭环、参数结构等 20+ 规则 |
| `scripts/extract_shortcut.py` | 解包已签名的 `.shortcut` | 处理 AEA1 格式，提取明文 XML |
| `scripts/render_token_template.py` | 渲染文本 token 模板 | 自动计算 U+FFFC 占位符偏移量 |
| `scripts/build_localized_menu.py` | 生成多语言菜单 spec | 支持 locale 键值验证，生成一致性 UUID |
| `scripts/link_skill.sh` | Shell 辅助脚本 | 快捷链接工具 |

### build_shortcut.py

将 JSON spec 编译为 Apple Shortcuts 的标准 plist 格式（.shortcut 文件）。

```bash
# 基本用法
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut

# 生成时同时签名（需要 macOS shortcuts CLI）
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut --sign

# 指定最小客户端版本
python3 scripts/build_shortcut.py spec.json --output MyShortcut.shortcut \
  --client-version 3000.0.0
```

### validate_shortcut.py

检查常见结构错误，包括：

- ✅ 每个 action 是否包含 `WFWorkflowActionIdentifier` 和 `WFWorkflowActionParameters`
- ✅ UUID 是否为大写格式
- ✅ 变量引用（`attachmentsByRange`）中的 UUID 是否有对应 action
- ✅ 控制流（Repeat / If / Menu）是否成对、`WFControlFlowMode` 是否为整数
- ✅ Token 字符串的 U+FFFC 偏移量是否匹配
- ✅ `choosefromlist` 的多语言菜单输入是否正确
- ✅ 常见参数拼写错误

```bash
python3 scripts/validate_shortcut.py MyShortcut.shortcut
```

### extract_shortcut.py

现代 Apple Shortcuts 用 AEA1（Apple Encryption Archive 1）格式签名，`plutil` 无法直接读取。此脚本解包并还原为明文 XML。

```bash
python3 scripts/extract_shortcut.py Input.shortcut --output Input_plaintext.plist

# 调试模式：保留中间文件
python3 scripts/extract_shortcut.py Input.shortcut --output Input_plaintext.plist \
  --keep-workdir debug-dir
```

### render_token_template.py

处理包含变量占位符的文本模板。将 `{{变量名}}` 转换为 U+FFFC 占位符，并自动计算 `attachmentsByRange` 偏移数组。

```bash
python3 scripts/render_token_template.py template.json
```

### build_localized_menu.py

为多语言菜单生成稳定的 JSON spec。保证同一个逻辑选项在不同语言中映射到相同的内部 UUID。

```bash
python3 scripts/build_localized_menu.py spec.json --locales zh,en,ja --output menu_spec.json
```

---

## 参考文档

`references/` 目录下存放了 Apple Shortcuts 逆向工程的详细资料，是编写 spec 时的手边指南：

| 文件 | 内容 |
|------|------|
| `actions.md` | `is.workflow.actions.*` 标识符及常用参数 |
| `appintents.md` | AppIntent（含 wrapper 与直接标识符） |
| `parameter-types.md` | 复杂字典、附件、Quantity、Token 字符串 |
| `variables.md` | `OutputUUID`、`OutputName`、`attachmentsByRange`、U+FFFC |
| `control-flow.md` | Repeat、If/Otherwise、Menu 分组 |
| `filters.md` | `WFContentItemFilter` 负载 |
| `plist-format.md` | 根 Workflow 键、图标/输入/输出元数据 |
| `examples.md` | 完整的可用模式 |
| `extraction.md` | 手动解包方案与故障排查 |
| `design/linear-review-ui.md` | 类 Linear 审查界面的 HTML 设计 |
| `patterns/` | 进阶架构模式（见下方） |

### 进阶模式

`references/patterns/` 收录了生产级 Shortcuts 的架构模式：

- **config-shortcut.md** — 分离设置/控制面板 Shortcut
- **main-runtime.md** — 运行时 Shortcut：读取配置、处理输入、路由分发
- **file-storage.md** — 文件级持久化与 JSON/Dictionary 存储
- **update-check.md** — 版本检查与更新提示流程
- **import-export-reset.md** — 备份、导入、导出、重置
- **action-extension-input.md** — Share Sheet 与无输入时的降级设计
- **localization.md** — 多语言字典、首次运行语言选择、动态菜单
- **html-interaction.md** — 通过剪贴板返回决策的 HTML 审查页面
- **ai-inbox.md** — 高耐久的 AI 捕获、修复、审查、写入与报告流程

每个模式文档都包含完整的 JSON spec 结构说明与设计原则。

---

## JSON Spec 格式

### 基础结构

```json
{
  "name": "快捷指令名称",
  "actions": [
    {
      "id": "is.workflow.actions.gettext",
      "params": {
        "UUID": "11111111-1111-1111-1111-111111111111",
        "WFTextActionText": "Hello World"
      }
    }
  ]
}
```

### 可选的根字段

```json
{
  "client_version": "2700.0.4",
  "client_release": "2700.0.4",
  "minimum_client_version": "2700",
  "icon": {
    "glyph": "ShortcutGlyphTypeApple",
    "start_color": "3679C8FF"
  },
  "input_content_item_classes": ["WFContentItem"],
  "output_content_item_classes": ["WFContentItem"],
  "import_questions": [],
  "quick_action_surfaces": [],
  "has_output_fallback": false,
  "has_shortcut_input_variables": false,
  "no_input_behavior": false
}
```

### 核心规则

1. **每个 action 必须有 `id`（→ `WFWorkflowActionIdentifier`）和 `params`（→ `WFWorkflowActionParameters`）**
2. **被引用的 action UUID 必须是大写**，如 `11111111-1111-1111-1111-111111111111`
3. **变量引用**使用 `OutputUUID`、`OutputName`、`Type`，放在 `attachmentsByRange` 内
4. **Token 字符串**使用 U+FFFC 对象替换字符，配合 `{offset, length}` 范围键
5. **控制流模式** `WFControlFlowMode` 为整数：`0`=开始，`1`=中间，`2`=结束
6. **分组**（Repeat / If / Menu）需要相同的 `GroupingIdentifier`

---

## 高级模式

### 多语言动态菜单

结合 `build_localized_menu.py` + `references/patterns/localization.md` 生成：

- 同一个逻辑选项在不同语言中映射到相同 UUID
- 运行时根据用户语言偏好显示对应文字
- `choosefromlist` 的结果通过一致的路由值匹配

完整例子见 `examples/advanced/localized-review/`。

### HTML 审查界面

通过 `showwebpage` action 嵌入 HTML 页面，用户操作后结果通过剪贴板返回给 Shortcut。设计文档见 `references/design/linear-review-ui.md`，HTML 模板见 `assets/templates/linear-review.html`。

### AI 收件箱工作流

`references/patterns/ai-inbox.md` 描述了"先捕获再分类"的生产级 Shortcut 架构：

1. **捕获** — Share Sheet / 快捷方式 / 闹钟触发
2. **AI 分类** — 识别类型、提取关键信息
3. **修复** — 针对解析失败进行降级处理
4. **审查** — 提供 HTML 审查界面
5. **写入** — 多 App 写入（Notes、Reminders、Files…）
6. **报告** — 汇总结果

### 配置 + 运行时分离

通过两个 Shortcut（Config + Runtime）实现类似 App 的设置体系：

- `examples/advanced/config-and-runtime/` 提供了一个可构建的最小脚手架
- 配置 Shortcut 管理所有用户设置
- 运行时 Shortcut 读取配置、处理输入、路由执行

---

## 常见问题

### 生成的 .shortcut 无法导入？

```bash
# 1. 检查 plist 结构
plutil -lint MyShortcut.shortcut

# 2. 运行完整验证
python3 scripts/validate_shortcut.py MyShortcut.shortcut

# 3. 确认已签名
head -c 4 MyShortcut.shortcut   # 应该输出 AEA1

# 4. 解包检查明文
python3 scripts/extract_shortcut.py MyShortcut.shortcut --output debug.plist
```

### `plutil -lint` 通过但导入时提示格式错误？

有些沙箱/运行环境可能会限制 `shortcuts` CLI。使用分离签名：

```bash
shortcuts sign --mode anyone --input MyShortcut.shortcut --output MyShortcut_signed.shortcut
```

如果沙箱内失败，在沙箱外重新运行同样的签名命令即可 —— 不需要修改 plist。

### 我从哪里获取 action 的 id 和参数？

查阅 `references/actions.md`（遗留的 `is.workflow.actions.*`）和 `references/appintents.md`（AppIntents）。对于复杂参数类型，参考 `references/parameter-types.md`。

### 如何为已有的 Shortcut 添加注释或查看结构？

用 `extract_shortcut.py` 解包签名文件得到明文 XML 后，你可以用任何文本编辑器查看和修改。修改后重新签名即可。

---

## 项目结构

```
├── SKILL.md                    # 技能入口（Reasonix/Codex Agent 使用）
├── scripts/
│   ├── build_shortcut.py       # JSON → .shortcut 编译器
│   ├── build_localized_menu.py # 多语言菜单生成器
│   ├── render_token_template.py# Token 模板渲染器
│   ├── validate_shortcut.py    # 结构验证器
│   ├── extract_shortcut.py     # 签名文件解包器
│   └── link_skill.sh           # Shell 辅助
├── references/
│   ├── actions.md, appintents.md, parameter-types.md ...
│   ├── patterns/               # 进阶架构模式
│   └── design/                 # 界面设计文档
├── assets/templates/           # HTML / UI 模板
├── examples/advanced/          # 可构建的完整示例
│   ├── config-and-runtime/
│   └── localized-review/
└── agents/
    └── openai.yaml             # AI Agent 配置
```

---

## License

MIT
