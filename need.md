# 英文书词汇等级分析工具 - 需求文档 v2.0

## 📋 项目定位

**项目类型**：个人背单词辅助工具
**用户群体**：个人或小团队（<10人）
**交互方式**：命令行工具（CLI），后期可扩展Web界面
**技术栈**：Python + NLP库（spaCy/NLTK）
**核心价值**：将英文书籍转换为分级单词表，便于有针对性地背单词

---

## 🎯 核心功能需求

### 1. 文本输入处理

#### 支持的文件格式
- **纯文本文件**：`.txt`
- **PDF文档**：仅支持文字可选中/复制的PDF（非扫描版）
- **Word文档**：`.docx` 格式
- **JSON数据**：结构化文本数据

#### 文本预处理
- 自动去除标点符号和特殊字符
- 过滤章节标题、页码等非正文内容
- 保留连字符单词（如 `well-known`）
- 统一编码为 UTF-8

---

### 2. 词汇分析核心功能

#### 2.1 单词词形还原
- 将单词还原为词典原形
  - 动词：`went` → `go`
  - 名词：`children` → `child`
  - 形容词：`better` → `good`

#### 2.2 停用词处理
- 过滤高频停用词（a, the, of, to, in 等）
- 保留助动词和情态动词（因为可能在词组中）

#### 2.3 词组识别（重点功能）

**需要识别的词组类型**：

1. **动词短语**（Phrasal Verbs）
   ```
   look up（查询）
   take off（脱下/起飞）
   give up（放弃）
   ```

2. **分离的词组**（Separable Phrasal Verbs）
   ```
   原文："She looked the word up in the dictionary"
   识别为：look up（而非单独的 look 和 up）
   ```

3. **常见搭配**（Collocations）
   ```
   make a decision
   take part in
   pay attention to
   ```

**识别策略**：
- 使用词组词典（需从开源数据库获取）
- 基于词性标注识别动词+介词/副词组合
- 在句子上下文中识别分离的词组

#### 2.4 专有名词处理
- 识别人名、地名、组织名等（首字母大写的词）
- 专有名词不进行词形还原
- 归类到独立的 "专有名词" 类别（或最高等级 C2+）

---

### 3. 等级标注与映射

#### 3.1 剑桥 CEFR 等级体系
- **A1** - Beginner（KET 入门前）
- **A2** - Elementary（KET）
- **B1** - Intermediate（PET）
- **B2** - Upper Intermediate（FCE）
- **C1** - Advanced（CAE）
- **C2** - Proficiency（CPE）
- **C2+** - 超纲词/专有名词

#### 3.2 雅思分数映射（参考）
| CEFR 等级 | 雅思分数段 | 说明 |
|-----------|-----------|------|
| A2 | 3.0-4.0 | 基础词汇 |
| B1 | 4.5-5.5 | 日常词汇 |
| B2 | 6.0-6.5 | 学术基础词汇 |
| C1 | 7.0-8.0 | 高级学术词汇 |
| C2 | 8.5-9.0 | 专业/文学词汇 |

#### 3.3 超纲词处理规则
- **定义**：不在剑桥官方词汇表中的词
- **处理方式**：
  - 归入 `C2+` 级别
  - 单独标记为 `out_of_syllabus: true`
  - 包括专有名词、罕见词汇、专业术语

---

### 4. 输出格式规范

#### 4.1 输出文件结构

**主输出文件**：`{book_name}_vocabulary.json`

```json
{
  "metadata": {
    "source_file": "pride_and_prejudice.txt",
    "analyzed_date": "2025-11-03",
    "total_words": 12450,
    "unique_words": 3876,
    "unique_phrases": 234
  },
  "statistics": {
    "A2": 850,
    "B1": 1020,
    "B2": 680,
    "C1": 450,
    "C2": 320,
    "C2+": 556
  },
  "vocabulary_by_level": {
    "A2": [
      {
        "word": "book",
        "word_type": "noun",
        "definition_cn": "书籍",
        "level": "A2",
        "exam": "KET",
        "ielts": "3.5-4.0",
        "frequency": 37,
        "example_sentences": [
          "She opened the book and began to read.",
          "This book was published in 1813."
        ]
      }
    ],
    "B1": [...],
    "phrases": [
      {
        "phrase": "look up",
        "type": "phrasal_verb",
        "definition_cn": "查找",
        "level": "B1",
        "frequency": 8,
        "example_sentences": [
          "She looked the word up in the dictionary."
        ]
      }
    ],
    "proper_nouns": [
      {
        "word": "Elizabeth",
        "type": "person_name",
        "level": "C2+",
        "frequency": 156
      }
    ]
  }
}
```

#### 4.2 次要输出格式

**CSV 格式**：`{book_name}_vocabulary.csv`
```csv
word,word_type,definition_cn,level,exam,ielts,frequency,example
book,noun,书籍,A2,KET,3.5-4.0,37,"She opened the book"
develop,verb,发展,B1,PET,5.0-5.5,14,"The story develops slowly"
```

**Markdown 格式**：`{book_name}_vocabulary.md`
- 分级列表展示
- 便于阅读和导出到笔记应用

---

## 🔧 技术实现方案

### 架构设计

```
英文书文件
    ↓
文本提取模块 (PyPDF2 / python-docx)
    ↓
分词与标注模块 (spaCy)
    ↓
词组识别模块 (自定义规则 + 词组词典)
    ↓
等级匹配模块 (剑桥词汇表数据库)
    ↓
统计分析模块 (Pandas)
    ↓
输出生成模块 (JSON/CSV/MD)
```

### 核心技术组件

| 模块 | 技术选型 | 说明 |
|------|---------|------|
| 文本提取 | PyPDF2 / python-docx | 支持PDF和Word文档 |
| NLP处理 | spaCy (en_core_web_sm) | 分词、词性标注、词形还原 |
| 词组识别 | 自定义规则 + 词组词典 | 基于依存关系和模式匹配 |
| 等级匹配 | CSV/JSON词汇表 + Pandas | 高效查询和映射 |
| 中文释义 | StarDict词典 / 有道API | 可选在线或离线词典 |
| 输出生成 | json/csv/markdown库 | 标准Python库 |

### 数据源需求

#### 1. 剑桥官方词汇表
- **来源**：需从开源数据库获取（如 English Vocabulary Profile）
- **格式**：CSV 或 JSON
- **字段要求**：
  ```json
  {
    "word": "develop",
    "level": "B1",
    "word_type": "verb",
    "exam": "PET"
  }
  ```

#### 2. 词组词典
- **来源**：需整理开源phrasal verbs数据库
- **覆盖范围**：至少包含500+常用动词短语

#### 3. 英汉词典
- **方案A**：使用StarDict开源词典（离线）
- **方案B**：调用有道/百度翻译API（在线，有配额限制）
- **方案C**：预先构建核心词汇的中英对照表

#### 4. 雅思等级映射表
- **来源**：根据公开资料整理CEFR到IELTS的映射关系

---

## 💻 命令行界面设计

### 基本用法

```bash
# 分析单个文件
python vocab_analyzer.py input.txt

# 指定输出格式
python vocab_analyzer.py input.pdf --format json,csv,md

# 指定输出目录
python vocab_analyzer.py input.docx --output ./results

# 显示详细处理过程
python vocab_analyzer.py input.txt --verbose

# 只输出特定等级的单词
python vocab_analyzer.py input.txt --levels B2,C1,C2
```

### 输出示例

```
📚 分析文件: pride_and_prejudice.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/6] 提取文本... ✓ (2.3s)
[2/6] 分词与词形还原... ✓ (8.7s)
[3/6] 识别词组... ✓ (3.2s)
[4/6] 匹配词汇等级... ✓ (1.8s)
[5/6] 获取中文释义... ✓ (12.4s)
[6/6] 生成输出文件... ✓ (0.9s)

📊 统计结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总单词数: 12,450
独立单词: 3,876
识别词组: 234

等级分布:
  A2 (KET)  ████████████████░░░░  850 词 (21.9%)
  B1 (PET)  ████████████████████  1020 词 (26.3%)
  B2 (FCE)  █████████████░░░░░░░  680 词 (17.5%)
  C1 (CAE)  ████████░░░░░░░░░░░░  450 词 (11.6%)
  C2 (CPE)  ██████░░░░░░░░░░░░░░  320 词 (8.3%)
  C2+ (超纲) ██████████░░░░░░░░░░  556 词 (14.4%)

✅ 输出文件已生成:
  • pride_and_prejudice_vocabulary.json
  • pride_and_prejudice_vocabulary.csv
  • pride_and_prejudice_vocabulary.md

💡 建议: 该书主要使用 B1-B2 词汇，适合雅思 5.5-6.5 分水平阅读
```

---

## 🚀 开发计划

### MVP 阶段 (Phase 1)
**目标**：实现核心功能，可以使用的命令行工具

- [ ] 搭建项目框架
- [ ] 实现文本提取（TXT/PDF/DOCX）
- [ ] 集成 spaCy 进行基础NLP处理
- [ ] **查找并整合剑桥词汇表数据**
- [ ] 实现等级匹配功能
- [ ] 输出 JSON 格式结果
- [ ] 基础统计功能

### Phase 2 - 增强功能
**目标**：提升准确性和用户体验

- [ ] 实现词组识别（包括分离词组）
- [ ] 集成中文释义（StarDict或API）
- [ ] 添加例句提取
- [ ] 支持 CSV 和 Markdown 输出
- [ ] 优化命令行输出显示
- [ ] 添加进度条

### Phase 3 - 扩展功能（可选）
**目标**：提供更多便利功能

- [ ] 支持批量处理多个文件
- [ ] 导出 Anki 卡片格式
- [ ] 简单的本地 Web 界面
- [ ] 生成学习计划建议
- [ ] 添加配置文件支持

---

## 📌 关键注意事项

### 1. 词组识别的挑战
分离词组识别是最复杂的部分，例如：
- "look it up" - 需要识别 "look...up" 是一个整体
- "turn the lights off" - 需要识别 "turn...off"

**解决方案**：
1. 使用依存句法分析（Dependency Parsing）
2. 维护一个可分离词组列表
3. 在句子中搜索 [动词 + (宾语) + 介词/副词] 的模式

### 2. 专有名词的处理
- 首字母大写不一定是专有名词（句首单词）
- 需要结合词性标注（PROPN）判断
- 人名、地名通常不需要背诵，但要统计

### 3. 中文释义的获取
- **优先方案**：预先构建核心词汇的中英对照表（5000-10000词）
- **备选方案**：集成在线词典API（注意速率限制）
- **离线方案**：使用StarDict格式词典文件

### 4. 性能考虑
- 单本书（10万词）预计处理时间：30-60秒
- spaCy模型加载较慢（约2-3秒），应全局加载一次
- 可考虑缓存已分析的词汇

---

## 🎯 验收标准

### 功能验收
- [ ] 成功提取 TXT/PDF/DOCX 文件内容
- [ ] 正确识别并还原单词词形
- [ ] 准确匹配词汇等级（A2-C2）
- [ ] 识别至少300+常用词组
- [ ] 识别分离的动词短语（准确率>80%）
- [ ] 生成包含中文释义的完整输出
- [ ] 专有名词单独归类

### 质量验收
- [ ] 对同一本书重复分析结果一致
- [ ] 等级标注与剑桥词汇表匹配度>95%
- [ ] 处理100页的书籍时间<60秒
- [ ] 输出文件格式正确且可解析

### 用户体验验收
- [ ] 命令行界面清晰易用
- [ ] 提供详细的进度反馈
- [ ] 错误信息明确具体
- [ ] 输出文件便于导入其他工具

---

## 📚 参考资源

### 词汇表数据源（待查找）
- English Vocabulary Profile (Cambridge)
- CEFR-J Wordlist
- Oxford 3000/5000
- Academic Word List (AWL)

### 词组数据源
- Cambridge Phrasal Verbs Dictionary
- 开源项目：phrasal-verbs-machine

### 技术文档
- spaCy 官方文档：https://spacy.io/
- PyPDF2 文档：https://pypdf2.readthedocs.io/

---

**文档版本**: v2.0
**更新日期**: 2025-11-03
**状态**: 需求已明确，待数据源确认后可开始开发
