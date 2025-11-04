# 英文书词汇等级分析工具 - 用户故事汇总文档

**项目名称**: Vocab Analyzer - English Vocabulary Level Analyzer
**文档版本**: v2.0
**创建日期**: 2025-11-03
**最后更新**: 2025-11-03

---

## 📋 目录

1. [项目概述](#1-项目概述)
2. [用户故事总览](#2-用户故事总览)
3. [开发路线图](#3-开发路线图)
4. [用户故事详细说明](#4-用户故事详细说明)
   - [Story 0: 数据资源准备](#story-0-数据资源准备)
   - [Story 1: 基础词汇等级分析](#story-1-基础词汇等级分析)
   - [Story 2: 格式化输出和统计展示](#story-2-格式化输出和统计展示)
   - [Story 3: 词组识别](#story-3-词组识别)
   - [Story 4: 中文释义集成](#story-4-中文释义集成)
   - [Story 5: 例句提取和完整功能](#story-5-例句提取和完整功能)
5. [进度追踪](#5-进度追踪)
6. [关键注意事项](#6-关键注意事项)

---

## 1. 项目概述

### 项目定位

**项目类型**: 个人背单词辅助工具
**用户群体**: 个人或小团队（<10人）
**交互方式**: 命令行工具（CLI），后期可扩展Web界面
**技术栈**: Python 3.10+ + spaCy + pandas + click + rich
**核心价值**: 将英文书籍转换为分级单词表，便于有针对性地背单词

### 核心功能

1. **文本提取处理** - 支持TXT/PDF/DOCX格式
2. **词汇分析** - 自动分词、词形还原、词性标注
3. **等级匹配** - 标注CEFR等级（A1-C2+）
4. **词组识别** - 识别动词短语和常见搭配
5. **中文释义** - 自动添加中文翻译和词性
6. **例句提取** - 从原文提取真实语境例句
7. **多格式输出** - 支持JSON/CSV/Markdown

### 技术架构

**架构模式**: Pipeline Pattern（管道模式） + Facade Pattern（外观模式）

```
Input File → Text Extraction → NLP Processing →
Phrase Detection → Level Matching → Statistics →
Output Generation → Output Files
```

**性能目标**:
- 小文件（<5页）: <5秒
- 中文件（20-50页）: <30秒
- 大文件（100+页）: <90秒
- 内存峰值: <500MB

---

## 2. 用户故事总览

### 故事优先级分类

| 故事编号 | 故事名称 | 优先级 | 预计工时 | 依赖关系 | 状态 |
|---------|---------|-------|---------|---------|------|
| **Story 0** | 数据资源准备 | 🟣 准备阶段 | 1-2天 | 无 | 🟢 95%完成 |
| **Story 1** | 基础词汇等级分析 | 🔴 P0 (MVP) | 1周 | Story 0 | ⏳ 待开始 |
| **Story 2** | 格式化输出和统计展示 | 🔴 P0 (MVP) | 3-4天 | Story 1 | ⏳ 待开始 |
| **Story 3** | 词组识别 | 🟠 P1 (增强) | 5-7天 | Story 1 | ⏳ 待开始 |
| **Story 4** | 中文释义集成 | 🟠 P1 (增强) | 3-4天 | Story 1 | ⏳ 待开始 |
| **Story 5** | 例句提取和完整功能 | 🟡 P2 (优化) | 4-5天 | Story 1,2,4 | ⏳ 待开始 |

**总预计时间**: 4-5周

### 里程碑规划

**🟣 准备阶段（第1-2天）**
- ✅ 需求文档和用户故事编写
- 🟢 Story 0: 数据资源收集（95%完成）

**🔴 第一阶段 - MVP开发（第3-16天）**
- ⏳ Story 1: 基础词汇等级分析（7天）
- ⏳ Story 2: 格式化输出和统计展示（3-4天）
- **里程碑**: 可运行的MVP版本，能生成基础分级单词表

**🟠 第二阶段 - 功能增强（第17-30天）**
- ⏳ Story 3: 词组识别（5-7天）
- ⏳ Story 4: 中文释义集成（3-4天）
- **里程碑**: 功能完善的版本，支持词组和中文释义

**🟡 第三阶段 - 完善优化（第31-37天）**
- ⏳ Story 5: 例句提取和完整功能（4-5天）
- ⏳ 整体测试和优化（2-3天）
- **里程碑**: 产品级质量，用户体验完善

---

## 3. 开发路线图

### 依赖关系图

```
Story 0 (数据准备)
    ↓
Story 1 (基础词汇分析) ← MVP核心
    ↓
    ├─→ Story 2 (格式化输出) ← MVP核心
    │
    ├─→ Story 3 (词组识别)
    │
    └─→ Story 4 (中文释义)
            ↓
        Story 5 (例句提取 + 完善)
```

### 阶段性交付计划

**第1次交付（第16天）- MVP版本**
- ✅ 功能：基础词汇分析 + 多格式输出
- ✅ 可用性：能处理TXT/PDF/DOCX，生成分级词汇表
- ✅ 质量：80%测试覆盖率，基本性能达标

**第2次交付（第30天）- 增强版本**
- ✅ 功能：词组识别 + 中文释义
- ✅ 可用性：输出更丰富实用，准确率>80%
- ✅ 质量：完整测试，性能优化

**第3次交付（第37天）- 完整版本**
- ✅ 功能：例句提取 + 用户体验优化
- ✅ 可用性：产品级质量，文档完善
- ✅ 质量：所有验收标准达标

---

## 4. 用户故事详细说明

---

## Story 0: 数据资源准备

### 基本信息

**优先级**: 🟣 准备阶段（最先执行）
**预计工时**: 1-2天
**依赖关系**: 无
**当前状态**: 🟢 95%完成

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
在开发前准备所有必需的基础数据资源：包括CEFR分级词汇表、词组词典、中英对照词典，以及用于测试的样例英文书籍。确保数据来源可靠、格式统一、覆盖面广。

### 期望成果

- ✅ 获取剑桥CEFR词汇表（A1-C2，至少5000词）
- ✅ 收集词组词典（至少500个常用动词短语）
- ✅ 准备中英词典数据（支持离线查询）
- ✅ 准备3-5本样例英文书籍（TXT/PDF/DOCX格式）
- ✅ 整理雅思等级映射关系表
- ⏳ 所有数据整理为统一的CSV/JSON格式（待转换脚本）

### 数据清单

#### 1. 剑桥CEFR分级词汇表

**已选择方案**: ✅ ECDICT（一站式解决方案）

**数据源信息**:
- **项目**: ECDICT - Free English to Chinese Dictionary Database
- **链接**: https://github.com/skywind3000/ECDICT
- **规模**: 770,612词条（340万完整版）
- **许可证**: MIT License（完全开源）
- **优势**:
  - 包含Oxford 3000标记（可用于CEFR映射）
  - 同时提供英文释义和中文翻译
  - 包含词频、音标、词性等完整信息
  - 一站式解决CEFR词汇表 + 中英词典需求

**数据字段**:
```
word, phonetic, definition, translation, pos, collins, oxford, tag, bnc, frq, exchange
```

**状态**: ✅ 已下载（770,612词条）

#### 2. 词组词典

**已选择方案**: ✅ Phrasal Verbs GitHub项目

**数据源信息**:
- **项目**: phrasal-verbs
- **链接**: https://github.com/Semigradsky/phrasal-verbs
- **规模**: 124个词组（需Phase 2扩充至500+）
- **格式**: JSON

**数据字段**:
```json
{
  "phrase": "look up",
  "type": "separable",
  "definition": "查找",
  "level": "B1"
}
```

**状态**: ✅ 已下载（124个），⏳ 待Phase 2扩充

#### 3. 中英词典

**已选择方案**: ✅ ECDICT（与CEFR词汇表同源）

**状态**: ✅ 已包含在ECDICT数据中

#### 4. 样例英文书籍

**已下载书目**:
- ✅ **Pride and Prejudice**（傲慢与偏见）- 735KB - B2-C1难度
- ✅ **Alice in Wonderland**（爱丽丝梦游仙境）- 148KB - A2-B1难度
- ✅ **Animal Farm**（动物农场）- 21KB - B1-B2难度

**文件格式**: TXT（来自Project Gutenberg，公有领域）

**状态**: ✅ 已下载

#### 5. 雅思等级映射表

**已创建映射**:
```json
{
  "A1": {"ielts_min": 2.0, "ielts_max": 3.0, "exam": "入门前"},
  "A2": {"ielts_min": 3.0, "ielts_max": 4.0, "exam": "KET"},
  "B1": {"ielts_min": 4.5, "ielts_max": 5.5, "exam": "PET"},
  "B2": {"ielts_min": 6.0, "ielts_max": 6.5, "exam": "FCE"},
  "C1": {"ielts_min": 7.0, "ielts_max": 8.0, "exam": "CAE"},
  "C2": {"ielts_min": 8.5, "ielts_max": 9.0, "exam": "CPE"},
  "C2+": {"ielts_min": 9.0, "ielts_max": 9.0, "exam": "超纲"}
}
```

**状态**: ✅ 已创建（data/mappings/cefr_ielts_mapping.json）

### 数据组织结构

**实际目录结构**:
```
data/
├── vocabularies/           # CEFR分级词汇（待转换）
├── phrases/
│   └── phrasal-verbs/     # ✅ 124个词组
│       ├── phrasal-verbs.json
│       └── README.md
├── dictionaries/
│   └── ECDICT/            # ✅ 770,612词条
│       ├── stardict.csv
│       ├── ecdict.mini.csv
│       └── README.md
├── sample_books/           # ✅ 3本样例书籍
│   ├── pride_and_prejudice.txt (735KB)
│   ├── alice_in_wonderland.txt (148KB)
│   └── animal_farm.txt (21KB)
├── mappings/
│   └── cefr_ielts_mapping.json  # ✅ 映射表
├── README.md              # ✅ 数据说明文档
└── DATA_VALIDATION_REPORT.md  # ✅ 验证报告
```

### 验收标准

- ✅ 至少获取一个完整的CEFR分级词汇表（>5000词） - ECDICT 770,612词条
- ⏳ 词组词典包含至少500个常用短语 - 当前124个，待扩充
- ✅ 中英词典能覆盖常用5000词 - ECDICT完整覆盖
- ✅ 准备至少3本不同难度的样例书籍 - 已完成3本
- ⏳ 所有数据文件格式统一且可被程序读取 - 待转换脚本
- ✅ 数据来源有明确的授权或开源许可 - MIT/公有领域
- ✅ 编写数据说明文档（来源、格式、使用方式） - data/README.md

### 待完成任务

**剩余工作（5%）**:
1. **T009**: 编写数据转换脚本 `scripts/prepare_data.py`
   - 从ECDICT筛选Oxford 3000词汇
   - 根据词频和标签分配CEFR等级（A1-C2）
   - 生成标准格式CSV文件到 `data/vocabularies/`
   - 为词组数据补充等级信息

**优先级**: 中（不阻塞MVP开发，可在Phase 1并行完成）

### 完成情况总结

**已完成**: 95%
- ✅ 所有核心数据已下载并验证
- ✅ 数据目录结构已创建
- ✅ 数据说明文档已编写
- ✅ 数据验证报告已生成

**待完成**: 5%
- ⏳ 数据转换脚本（不阻塞Story 1开发）

---

## Story 1: 基础词汇等级分析

### 基本信息

**优先级**: 🔴 P0（最高 - MVP核心）
**预计工时**: 1周（7天）
**依赖关系**: Story 0（数据准备）
**当前状态**: ⏳ 待开始

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
用户上传英文书籍文件（TXT/PDF/DOCX），系统自动提取所有单词，将每个单词还原为原形并标注CEFR等级（A2-C2+），统计每个单词的出现频次。

### 期望成果

- 成功读取并提取TXT/PDF/DOCX文件内容
- 准确识别单词并还原为原形（如went→go）
- 每个单词匹配正确的CEFR等级
- 输出包含单词、等级、频次的基础列表
- 超纲词和专有名词归入C2+级别

### 功能需求

#### 1. 文本提取功能

**支持格式**:
- TXT文件（UTF-8编码）
- PDF文件（纯文本，非扫描版）
- DOCX文件（Word文档）

**技术实现**:
- TXT: Python标准库 `open()`
- PDF: PyPDF2库
- DOCX: python-docx库

**异常处理**:
- 文件不存在/无权限
- 编码错误（自动检测并转换）
- PDF为扫描版（提示用户）
- 文件过大（>50MB拒绝，>10MB警告）

#### 2. NLP处理功能

**分词与词性标注**:
- 使用spaCy库（en_core_web_sm模型）
- 自动识别单词边界
- 标注词性（NOUN/VERB/ADJ等）

**词形还原**:
- 动词：went → go, running → run
- 名词：children → child, mice → mouse
- 形容词：better → good

**停用词处理**:
- 过滤高频停用词（a, the, of, to, in等）
- 保留语法功能词（can, will, should等）

#### 3. 等级匹配功能

**CEFR等级体系**:
- A1: Beginner（入门前）
- A2: Elementary（KET）
- B1: Intermediate（PET）
- B2: Upper Intermediate（FCE）
- C1: Advanced（CAE）
- C2: Proficiency（CPE）
- C2+: 超纲词/专有名词

**匹配逻辑**:
```python
1. 查询CEFR词汇表（优先）
2. 如果未找到，查询Oxford 3000/5000
3. 如果仍未找到，标记为C2+（超纲）
4. 专有名词（首字母大写+PROPN词性）直接标记为C2+
```

**准确率要求**: >95%

#### 4. 频次统计功能

**统计维度**:
- 单词原形（lemma）频次
- 总词数（包含重复）
- 独立词数（去重后）

**示例输出**:
```json
{
  "word": "develop",
  "lemma": "develop",
  "pos": "VERB",
  "level": "B1",
  "frequency": 14
}
```

### 技术架构

**模块设计**（遵循Constitution Principle II）:

```
src/vocab_analyzer/
├── models.py              # 数据结构定义
├── text_extraction.py     # 文本提取模块
├── nlp_processing.py      # NLP处理模块
├── level_matching.py      # 等级匹配模块
└── analyzer.py            # 外观类（协调器）
```

**核心类结构**:
```python
# models.py
@dataclass
class Word:
    lemma: str
    pos_tag: str
    level: str
    frequency: int
    is_proper_noun: bool

# analyzer.py
class VocabularyAnalyzer:
    def __init__(self):
        self.text_extractor = TextExtractor()
        self.nlp_processor = NLPProcessor()
        self.level_matcher = LevelMatcher()

    def analyze(self, file_path: Path) -> List[Word]:
        text = self.text_extractor.extract(file_path)
        tokens = self.nlp_processor.process(text)
        words = self.level_matcher.match(tokens)
        return words
```

### 性能要求

**处理速度**（遵循Constitution性能标准）:
- 小文件（<5页）: <5秒
- 中文件（20-50页）: <30秒
- 大文件（100+页）: <90秒

**优化策略**:
1. spaCy模型全局加载一次
2. 词汇查询使用LRU缓存（10,000条）
3. spaCy批处理（100句/批次）
4. pandas DataFrame索引优化

**内存限制**: <500MB峰值

### 验收标准

**功能验收**:
- [ ] 成功提取TXT/PDF/DOCX文件内容
- [ ] 词形还原准确率>95%（基于测试样本）
- [ ] 等级匹配准确率>95%（基于已知词汇）
- [ ] 专有名词正确归类为C2+
- [ ] 频次统计准确无误

**质量验收**:
- [ ] 单元测试覆盖率>80%
- [ ] 关键路径（提取、还原、匹配）100%覆盖
- [ ] 通过所有边缘案例测试
- [ ] 代码通过pylint检查（≥8.5分）

**性能验收**:
- [ ] Pride and Prejudice（735KB）处理时间<60秒
- [ ] 内存使用<500MB
- [ ] 可重复运行结果一致（确定性）

### 技术实现要点

**1. 文本提取**
```python
class TextExtractor:
    def extract(self, file_path: Path) -> str:
        if file_path.suffix == '.txt':
            return self._extract_txt(file_path)
        elif file_path.suffix == '.pdf':
            return self._extract_pdf(file_path)
        elif file_path.suffix == '.docx':
            return self._extract_docx(file_path)
```

**2. NLP处理**
```python
class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")  # 全局加载

    def process(self, text: str) -> List[Token]:
        doc = self.nlp(text)
        return [token for token in doc if not token.is_stop]
```

**3. 等级匹配**
```python
class LevelMatcher:
    def __init__(self):
        self.vocab_df = pd.read_csv("data/vocabularies/cefr_wordlist.csv")
        self.vocab_df.set_index('word', inplace=True)  # 索引优化

    @lru_cache(maxsize=10000)
    def get_level(self, lemma: str) -> str:
        if lemma in self.vocab_df.index:
            return self.vocab_df.loc[lemma, 'level']
        return 'C2+'
```

### 依赖数据

**必需数据文件**（来自Story 0）:
- `data/vocabularies/cefr_wordlist.csv` - CEFR分级词汇表
- `data/sample_books/` - 测试用样例书籍

**可选数据文件**:
- `data/vocabularies/oxford_3000.csv` - Oxford核心词汇（补充）

### 测试计划

**单元测试**:
- `test_text_extraction.py` - 测试所有文件格式提取
- `test_nlp_processing.py` - 测试词形还原、词性标注
- `test_level_matching.py` - 测试等级匹配逻辑

**集成测试**:
- `test_end_to_end.py` - 完整流程测试（文件→结果）

**测试数据**:
- 使用Animal Farm（21KB）作为快速测试样本
- 使用Pride and Prejudice（735KB）作为性能测试样本

---

## Story 2: 格式化输出和统计展示

### 基本信息

**优先级**: 🔴 P0（最高 - MVP核心）
**预计工时**: 3-4天
**依赖关系**: Story 1（基础词汇分析）
**当前状态**: ⏳ 待开始

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
在完成词汇等级分析后，系统将结果按等级分类整理，生成易于阅读和使用的文件格式。用户可以看到每个等级的词汇数量和占比，并能导出为JSON、CSV或Markdown格式。

### 期望成果

- 生成按等级分类的单词列表（A2/B1/B2/C1/C2/C2+）
- 提供统计数据：总词数、独立单词数、各等级占比
- 支持JSON、CSV、Markdown三种输出格式
- 文件命名清晰（如：书名_vocabulary.json）

### 功能需求

#### 1. 数据分类功能

**按等级分组**:
```python
vocabulary_by_level = {
    "A2": [word1, word2, ...],
    "B1": [word3, word4, ...],
    "B2": [...],
    "C1": [...],
    "C2": [...],
    "C2+": [proper_nouns, out_of_syllabus_words, ...]
}
```

**排序规则**:
- 同等级内按频次降序排列
- 频次相同按字母顺序排列

#### 2. 统计分析功能

**基础统计**:
```json
{
  "total_words": 12450,        // 总词数（含重复）
  "unique_words": 3876,        // 独立词数
  "unique_phrases": 0,         // Story 3后启用
  "statistics_by_level": {
    "A2": {"count": 850, "percentage": 21.9},
    "B1": {"count": 1020, "percentage": 26.3},
    "B2": {"count": 680, "percentage": 17.5},
    "C1": {"count": 450, "percentage": 11.6},
    "C2": {"count": 320, "percentage": 8.3},
    "C2+": {"count": 556, "percentage": 14.4}
  }
}
```

**高级统计**（可选）:
- 各等级单词的平均频次
- 高频词Top 100
- 建议阅读水平（基于主要等级分布）

#### 3. JSON输出格式

**文件命名**: `{book_name}_vocabulary.json`

**完整结构**:
```json
{
  "metadata": {
    "source_file": "pride_and_prejudice.txt",
    "analyzed_date": "2025-11-03",
    "analyzer_version": "1.0.0",
    "total_words": 12450,
    "unique_words": 3876,
    "unique_phrases": 0
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
        "level": "A2",
        "exam": "KET",
        "ielts": "3.5-4.0",
        "frequency": 37
      }
    ],
    "B1": [...],
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

#### 4. CSV输出格式

**文件命名**: `{book_name}_vocabulary.csv`

**列定义**:
```csv
word,word_type,level,exam,ielts,frequency
book,noun,A2,KET,3.5-4.0,37
develop,verb,B1,PET,5.0-5.5,14
Elizabeth,proper_noun,C2+,N/A,N/A,156
```

**特点**:
- 适合导入Excel/Google Sheets
- 适合Anki等记忆软件导入
- UTF-8 BOM编码（兼容Windows Excel）

#### 5. Markdown输出格式

**文件命名**: `{book_name}_vocabulary.md`

**示例结构**:
```markdown
# Pride and Prejudice - Vocabulary Analysis

**Analyzed Date**: 2025-11-03
**Total Words**: 12,450
**Unique Words**: 3,876

## Statistics

| Level | Count | Percentage |
|-------|-------|------------|
| A2    | 850   | 21.9%      |
| B1    | 1,020 | 26.3%      |
| ...   | ...   | ...        |

## A2 Level (KET)

- **book** (noun) - 37 times
- **house** (noun) - 28 times
- ...

## B1 Level (PET)

- **develop** (verb) - 14 times
- ...
```

**特点**:
- 便于阅读和打印
- 可导入Obsidian/Notion等笔记工具
- 支持Markdown渲染器展示

#### 6. 命令行输出功能

**实时进度显示**:
```
📚 Analyzing: pride_and_prejudice.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/5] Extracting text... ✓ (2.3s)
[2/5] Processing NLP... ✓ (8.7s)
[3/5] Matching levels... ✓ (1.8s)
[4/5] Analyzing statistics... ✓ (0.5s)
[5/5] Generating output... ✓ (0.9s)

📊 Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total words: 12,450
Unique words: 3,876

Level Distribution:
  A2 (KET)  ████████████████░░░░  850 (21.9%)
  B1 (PET)  ████████████████████  1020 (26.3%)
  B2 (FCE)  █████████████░░░░░░░  680 (17.5%)
  C1 (CAE)  ████████░░░░░░░░░░░░  450 (11.6%)
  C2 (CPE)  ██████░░░░░░░░░░░░░░  320 (8.3%)
  C2+ (超纲) ██████████░░░░░░░░░░  556 (14.4%)

✅ Output files generated:
  • pride_and_prejudice_vocabulary.json
  • pride_and_prejudice_vocabulary.csv
  • pride_and_prejudice_vocabulary.md

💡 Suggestion: This book mainly uses B1-B2 vocabulary,
   suitable for IELTS 5.5-6.5 level readers.
```

**使用技术**:
- rich库（美化表格和进度条）
- 颜色编码（等级用不同颜色）
- Unicode图表字符

### 技术架构

**新增模块**:
```
src/vocab_analyzer/
├── statistics.py          # 统计分析模块
└── output_generation.py   # 输出生成模块
```

**核心类**:
```python
class StatisticsAnalyzer:
    def analyze(self, words: List[Word]) -> Statistics:
        """生成统计数据"""
        pass

class OutputGenerator:
    def generate_json(self, analysis: VocabularyAnalysis, path: Path):
        """生成JSON文件"""
        pass

    def generate_csv(self, analysis: VocabularyAnalysis, path: Path):
        """生成CSV文件"""
        pass

    def generate_markdown(self, analysis: VocabularyAnalysis, path: Path):
        """生成Markdown文件"""
        pass
```

### CLI接口设计

**基本用法**:
```bash
# 默认生成所有格式
vocab-analyzer analyze book.txt

# 指定单一格式
vocab-analyzer analyze book.txt --format json
vocab-analyzer analyze book.txt --format csv
vocab-analyzer analyze book.txt --format markdown

# 指定输出目录
vocab-analyzer analyze book.pdf --output ./results/

# 仅显示统计，不生成文件
vocab-analyzer analyze book.txt --stats-only

# 静默模式（无终端输出）
vocab-analyzer analyze book.txt --quiet
```

### 验收标准

**功能验收**:
- [ ] JSON格式输出正确且可解析
- [ ] CSV格式可被Excel/Anki正确导入
- [ ] Markdown渲染正确且美观
- [ ] 统计数据准确（百分比之和=100%）
- [ ] 文件命名清晰规范

**质量验收**:
- [ ] 单元测试覆盖率>80%
- [ ] 所有输出格式的schema验证通过
- [ ] 终端输出在不同尺寸下正常显示

**用户体验验收**:
- [ ] 进度条实时更新
- [ ] 错误信息清晰明确
- [ ] 输出文件易于使用

### 技术实现要点

**1. 统计分析**:
```python
class StatisticsAnalyzer:
    def analyze(self, words: List[Word]) -> Statistics:
        stats = defaultdict(int)
        for word in words:
            stats[word.level] += 1

        total = len(words)
        percentages = {
            level: (count / total * 100)
            for level, count in stats.items()
        }
        return Statistics(stats, percentages)
```

**2. JSON输出**:
```python
def generate_json(self, analysis: VocabularyAnalysis, path: Path):
    output = {
        "metadata": {...},
        "statistics": {...},
        "vocabulary_by_level": {...}
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
```

**3. 终端输出**:
```python
from rich.console import Console
from rich.progress import Progress

console = Console()
with Progress() as progress:
    task = progress.add_task("Processing...", total=5)
    # 执行步骤...
    progress.update(task, advance=1)
```

---

## Story 3: 词组识别

### 基本信息

**优先级**: 🟠 P1（高优先级 - 重要功能）
**预计工时**: 5-7天
**依赖关系**: Story 1（基础词汇分析）
**当前状态**: ⏳ 待开始

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
系统能识别书中的动词短语（如look up、give up）和常见搭配（如make a decision），特别是能识别被拆开的词组（如"look the word up"识别为"look up"），并为词组标注等级和频次。

### 期望成果

- 准确识别至少300个常用动词短语
- 能识别分离的词组（准确率>80%）
- 识别常见搭配短语
- 词组与单词分开列出，包含等级和频次信息
- 避免将词组拆分为单独的词统计

### 功能需求

#### 1. 动词短语识别（Phrasal Verbs）

**类型1：连续型**
```
look up → "She looked up the word"
give up → "Don't give up hope"
take off → "The plane took off"
```

**类型2：分离型（Separable）**
```
look up → "She looked the word up"
turn on → "Please turn the light on"
pick up → "He picked it up"
```

**识别策略**:
1. 基于词组词典匹配
2. 依存句法分析（Dependency Parsing）
3. 模式匹配：[动词] + (宾语) + [介词/副词]

#### 2. 常见搭配识别（Collocations）

**动词+名词搭配**:
```
make a decision
take part in
pay attention to
do homework
```

**形容词+名词搭配**:
```
strong coffee
heavy rain
```

**识别策略**:
- n-gram分析（bigram, trigram）
- 基于搭配词典
- 频次阈值过滤

#### 3. 词组等级标注

**数据来源**:
- 词组词典中的预定义等级
- 根据组成单词的最高等级推断
- 手动标注的高频词组等级

**示例**:
```json
{
  "phrase": "look up",
  "type": "phrasal_verb",
  "separable": true,
  "level": "B1",
  "frequency": 8
}
```

#### 4. 去重处理

**问题**:
- "look" 和 "up" 单独也会被统计
- 如果识别出 "look up"，需要从单词列表中移除对应的出现

**解决方案**:
```python
# 1. 先识别词组
phrases = detect_phrases(text)

# 2. 标记词组位置
phrase_positions = mark_phrase_positions(phrases)

# 3. 分词时跳过词组内部的单词
words = tokenize_excluding_phrases(text, phrase_positions)
```

### 技术架构

**新增模块**:
```
src/vocab_analyzer/
└── phrase_detection.py    # 词组识别模块
```

**核心类**:
```python
class PhraseDetector:
    def __init__(self, phrasal_verbs_dict: Dict, collocations_dict: Dict):
        self.phrasal_verbs = phrasal_verbs_dict
        self.collocations = collocations_dict

    def detect(self, doc: spacy.Doc) -> List[Phrase]:
        """检测所有词组"""
        phrases = []
        phrases.extend(self._detect_phrasal_verbs(doc))
        phrases.extend(self._detect_collocations(doc))
        return phrases

    def _detect_phrasal_verbs(self, doc: spacy.Doc) -> List[Phrase]:
        """检测动词短语（包括分离型）"""
        pass

    def _detect_collocations(self, doc: spacy.Doc) -> List[Phrase]:
        """检测常见搭配"""
        pass
```

### 验收标准

**功能验收**:
- [ ] 识别至少300个常用动词短语
- [ ] 分离型词组识别准确率>80%
- [ ] 词组不被重复统计为单词
- [ ] 词组等级标注正确

**质量验收**:
- [ ] 单元测试覆盖率>80%
- [ ] 通过边缘案例测试（复杂句子结构）

**性能验收**:
- [ ] 不显著增加处理时间（<10%额外开销）

### 技术实现要点

**1. 依存句法分析**:
```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("She looked the word up")

# 分析依存关系
for token in doc:
    if token.pos_ == "VERB":
        for child in token.children:
            if child.dep_ == "prt":  # particle (up, down, etc.)
                # 可能是phrasal verb
                phrase = f"{token.lemma_} {child.text}"
```

**2. 模式匹配**:
```python
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)
# 模式: [动词] + [宾语] + [小品词]
pattern = [
    {"POS": "VERB"},
    {"POS": {"IN": ["NOUN", "PRON"]}},
    {"DEP": "prt"}
]
matcher.add("PHRASAL_VERB_SEP", [pattern])
```

---

## Story 4: 中文释义集成

### 基本信息

**优先级**: 🟠 P1（高优先级 - 重要功能）
**预计工时**: 3-4天
**依赖关系**: Story 1（基础词汇分析）
**当前状态**: ⏳ 待开始

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
为每个单词和词组自动添加中文释义和词性标注（名词/动词/形容词等），方便用户快速理解词义，无需手动查词典。

### 期望成果

- 每个单词包含准确的中文释义
- 标注清晰的词性（noun/verb/adjective等）
- 词组也包含中文翻译
- 释义简洁明了（1-3个主要含义）
- 支持离线或在线词典数据源

### 功能需求

#### 1. 中文释义获取

**优先方案：离线词典（ECDICT）**

**数据结构**:
```json
{
  "word": "develop",
  "phonetic": "/dɪˈveləp/",
  "pos": "v.",
  "translation": "发展；开发；研制",
  "definition": "to grow or change into a more advanced form"
}
```

**优势**:
- 完全离线，快速查询
- ECDICT已包含770,612词条
- 同时提供英文释义和中文翻译
- 无API调用限制

**备选方案：在线API（可选）**

**方案A：有道翻译API**
- 适用场景：ECDICT未覆盖的生僻词
- 调用限制：每秒10次，每日5000次（免费额度）
- 实现：带重试和降级机制

**方案B：百度翻译API**
- 调用限制：每秒10次

#### 2. 词性标注

**标准词性列表**:
```
n. / noun - 名词
v. / verb - 动词
adj. / adjective - 形容词
adv. / adverb - 副词
prep. / preposition - 介词
conj. / conjunction - 连词
pron. / pronoun - 代词
interj. / interjection - 感叹词
```

**数据来源**:
1. spaCy词性标注（实时）
2. ECDICT词典中的词性字段（预存）
3. 两者结合，优先使用词典数据

#### 3. 多义词处理

**策略**:
- 提供1-3个最常用的释义
- 按词频排序（高频释义优先）
- 标注释义的使用场景（如果有）

**示例**:
```json
{
  "word": "book",
  "pos": "noun",
  "translations": [
    "书籍；书",
    "本子；簿册",
    "卷；篇"
  ],
  "primary_translation": "书籍"
}
```

#### 4. 词组翻译

**动词短语**:
```json
{
  "phrase": "look up",
  "type": "phrasal_verb",
  "translation": "查找；查阅",
  "example": "look up a word in the dictionary"
}
```

**搭配短语**:
```json
{
  "phrase": "make a decision",
  "type": "collocation",
  "translation": "做决定；作出决定"
}
```

### 技术架构

**新增/修改模块**:
```
src/vocab_analyzer/
├── translation.py         # 翻译模块（新增）
└── level_matching.py      # 修改：集成翻译功能
```

**核心类**:
```python
class TranslationService:
    def __init__(self, ecdict_path: Path):
        self.ecdict = self._load_ecdict(ecdict_path)

    @lru_cache(maxsize=10000)
    def translate(self, word: str, pos: str) -> Translation:
        """获取中文释义"""
        # 1. 先查ECDICT
        if word in self.ecdict:
            return self.ecdict[word]

        # 2. 如果未找到，使用在线API（可选）
        if self.online_api_enabled:
            return self._query_online_api(word)

        # 3. 都失败则返回空
        return Translation(word=word, translation="[未找到释义]")
```

### 输出格式更新

**JSON格式（新增字段）**:
```json
{
  "word": "develop",
  "word_type": "verb",
  "definition_cn": "发展；开发；研制",
  "phonetic": "/dɪˈveləp/",
  "level": "B1",
  "exam": "PET",
  "frequency": 14
}
```

**CSV格式（新增列）**:
```csv
word,word_type,definition_cn,phonetic,level,exam,frequency
develop,verb,发展；开发；研制,/dɪˈveləp/,B1,PET,14
```

### 验收标准

**功能验收**:
- [ ] 所有常用词汇（A1-C1）都有中文释义
- [ ] 词性标注准确率>95%
- [ ] 释义简洁明了（不超过15字）
- [ ] 词组翻译准确

**质量验收**:
- [ ] 离线词典加载速度<2秒
- [ ] 单词翻译查询速度<1ms（有缓存）
- [ ] 测试覆盖率>80%

**用户体验验收**:
- [ ] 输出文件可直接用于背单词
- [ ] 未找到释义的词有清晰标注

### 技术实现要点

**1. ECDICT数据加载**:
```python
class ECDICTLoader:
    def load(self, path: Path) -> Dict[str, Translation]:
        df = pd.read_csv(path)

        # 构建快速查询字典
        translation_dict = {}
        for _, row in df.iterrows():
            translation_dict[row['word']] = Translation(
                word=row['word'],
                phonetic=row['phonetic'],
                pos=row['pos'],
                translation=row['translation'],
                definition=row['definition']
            )
        return translation_dict
```

**2. 在线API调用（可选）**:
```python
import requests

class YoudaoAPI:
    def translate(self, word: str) -> str:
        url = "https://openapi.youdao.com/api"
        params = {
            'q': word,
            'from': 'en',
            'to': 'zh-CHS',
            'appKey': self.app_key,
            'salt': random.randint(1, 65536),
            'sign': self._generate_sign(word)
        }

        response = requests.get(url, params=params, timeout=3)
        data = response.json()

        if data['errorCode'] == '0':
            return data['translation'][0]
        return None
```

---

## Story 5: 例句提取和完整功能

### 基本信息

**优先级**: 🟡 P2（中优先级 - 优化功能）
**预计工时**: 4-5天
**依赖关系**: Story 1, 2, 4
**当前状态**: ⏳ 待开始

### 业务需求

#### 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

#### 本次业务需求
从原文中提取每个单词和词组的实际使用例句（1-3条），帮助用户在真实语境中理解和记忆单词。完善所有输出格式和用户体验细节。

### 期望成果

- 每个单词提供1-3条原文例句
- 例句长度适中（不超过20个词）
- 例句能体现该词的典型用法
- 命令行显示清晰的进度条和统计图表
- 处理速度：100页书籍<60秒
- 输出文件可直接导入其他学习工具

### 功能需求

#### 1. 例句提取

**提取策略**:
```python
1. 找到包含目标单词的所有句子
2. 按以下标准筛选：
   - 句子长度：5-20词（太短缺乏语境，太长难以记忆）
   - 单词位置：目标词在句子中间更佳（有上下文）
   - 句子复杂度：避免过于复杂的从句结构
3. 选择最佳的1-3个例句
4. 标记目标单词在例句中的位置
```

**示例输出**:
```json
{
  "word": "develop",
  "examples": [
    {
      "sentence": "The story develops slowly in the first chapter.",
      "position": [2],  // 单词在句子中的索引
      "length": 8
    },
    {
      "sentence": "She helped develop the new software system.",
      "position": [2],
      "length": 7
    }
  ]
}
```

#### 2. 例句质量控制

**评分标准**:
```python
score = (
    length_score * 0.3 +      # 长度适中（10-15词最佳）
    position_score * 0.2 +    # 目标词位置居中
    simplicity_score * 0.3 +  # 句子结构简单
    context_score * 0.2       # 上下文清晰
)
```

**去重处理**:
- 避免选择非常相似的例句
- 使用Levenshtein距离或余弦相似度
- 相似度>80%的例句只保留一个

#### 3. 例句标注

**高亮目标单词**:
```markdown
She helped **develop** the new software system.
```

**词形变化标注**:
```json
{
  "word": "develop",
  "example": "The story developed slowly.",
  "word_form": "developed",  // 实际出现的形式
  "lemma": "develop"         // 原形
}
```

#### 4. 进度条和可视化

**实时进度**（使用rich库）:
```
📚 Analyzing: pride_and_prejudice.txt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

[1/6] Extracting text... ✓ (2.3s)
[2/6] Processing NLP... ✓ (8.7s)
[3/6] Detecting phrases... ✓ (3.2s)
[4/6] Matching levels... ✓ (1.8s)
[5/6] Extracting examples... ✓ (5.4s)
[6/6] Generating output... ✓ (0.9s)
```

**统计图表**:
```
📊 Vocabulary Distribution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A2  ████████████████░░░░  850  (21.9%)
B1  ████████████████████  1020 (26.3%)
B2  █████████████░░░░░░░  680  (17.5%)
C1  ████████░░░░░░░░░░░░  450  (11.6%)
C2  ██████░░░░░░░░░░░░░░  320  (8.3%)
C2+ ██████████░░░░░░░░░░  556  (14.4%)

💡 Recommended Study Path:
   1️⃣ Start with B1 (1020 words) - Core vocabulary
   2️⃣ Then B2 (680 words) - Build fluency
   3️⃣ Finally C1 (450 words) - Advanced reading
```

#### 5. 导出功能增强

**Anki格式导出**:
```csv
Front,Back,Example,Level
develop,发展；开发,She helped **develop** the new system.,B1
```

**JSON格式完整版**:
```json
{
  "word": "develop",
  "word_type": "verb",
  "definition_cn": "发展；开发；研制",
  "phonetic": "/dɪˈveləp/",
  "level": "B1",
  "exam": "PET",
  "ielts": "5.0-5.5",
  "frequency": 14,
  "examples": [
    {
      "sentence": "She helped develop the new software system.",
      "word_form": "develop",
      "context": "technology"
    },
    {
      "sentence": "The story developed slowly in the first chapter.",
      "word_form": "developed",
      "context": "narrative"
    }
  ]
}
```

### 技术架构

**新增模块**:
```
src/vocab_analyzer/
└── example_extraction.py  # 例句提取模块
```

**核心类**:
```python
class ExampleExtractor:
    def __init__(self, max_examples: int = 3):
        self.max_examples = max_examples

    def extract(self, word: str, doc: spacy.Doc) -> List[Example]:
        """提取单词的例句"""
        candidates = self._find_candidate_sentences(word, doc)
        scored = self._score_sentences(candidates, word)
        best = self._select_best(scored, self.max_examples)
        return best

    def _score_sentence(self, sentence: spacy.Span, word: str) -> float:
        """评分句子质量"""
        length_score = self._score_length(len(sentence))
        position_score = self._score_position(word, sentence)
        simplicity_score = self._score_simplicity(sentence)
        return (
            length_score * 0.3 +
            position_score * 0.2 +
            simplicity_score * 0.5
        )
```

### 性能优化

**优化目标**:
- 100页书籍处理时间：<60秒（包括例句提取）
- 例句提取不超过总时间的20%（~12秒）

**优化策略**:
1. **批处理**: 一次性处理所有句子，而不是逐词查找
2. **索引构建**: 预先建立单词→句子索引
3. **并行处理**（可选）: 多进程提取例句
4. **缓存**: 相同单词的例句重复使用

**实现**:
```python
# 预先建立索引
word_to_sentences = defaultdict(list)
for sent in doc.sents:
    for token in sent:
        word_to_sentences[token.lemma_].append(sent)

# 快速查询
examples = word_to_sentences.get(word, [])
```

### CLI增强

**新增命令选项**:
```bash
# 控制例句数量
vocab-analyzer analyze book.txt --examples 3

# 禁用例句提取（加速处理）
vocab-analyzer analyze book.txt --no-examples

# 例句长度限制
vocab-analyzer analyze book.txt --max-example-length 15

# 导出Anki格式
vocab-analyzer analyze book.txt --export-anki

# 彩色输出（默认）
vocab-analyzer analyze book.txt --color

# 纯文本输出（适合管道）
vocab-analyzer analyze book.txt --no-color

# 详细模式（显示所有步骤）
vocab-analyzer analyze book.txt --verbose

# 安静模式（仅输出文件路径）
vocab-analyzer analyze book.txt --quiet
```

### 验收标准

**功能验收**:
- [ ] 每个单词提供1-3条例句
- [ ] 例句长度在5-20词之间
- [ ] 例句质量符合评分标准
- [ ] 进度条实时更新

**质量验收**:
- [ ] 100页书籍处理时间<60秒
- [ ] 例句提取准确率>90%（人工抽查）
- [ ] 测试覆盖率>80%

**用户体验验收**:
- [ ] 命令行输出美观清晰
- [ ] 错误信息友好明确
- [ ] 输出文件可直接导入Anki

### 技术实现要点

**1. 例句评分**:
```python
def _score_length(self, length: int) -> float:
    """句子长度评分（10-15词最佳）"""
    if 10 <= length <= 15:
        return 1.0
    elif 8 <= length <= 17:
        return 0.8
    elif 5 <= length <= 20:
        return 0.5
    else:
        return 0.0

def _score_position(self, word: str, sentence: spacy.Span) -> float:
    """单词位置评分（居中最佳）"""
    tokens = [t.lemma_ for t in sentence]
    if word not in tokens:
        return 0.0

    pos = tokens.index(word)
    mid = len(tokens) / 2
    distance = abs(pos - mid) / mid
    return 1.0 - distance
```

**2. 高亮显示**:
```python
def highlight_word(sentence: str, word: str) -> str:
    """高亮目标单词"""
    pattern = re.compile(rf'\b{word}\b', re.IGNORECASE)
    return pattern.sub(f'**{word}**', sentence)
```

**3. Anki导出**:
```python
def export_anki(self, words: List[Word], path: Path):
    """导出Anki导入格式"""
    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Front', 'Back', 'Example', 'Level'])

        for word in words:
            example = word.examples[0].sentence if word.examples else ""
            writer.writerow([
                word.lemma,
                word.definition_cn,
                example,
                word.level
            ])
```

---

## 5. 进度追踪

### 当前状态概览

**当前阶段**: 🟣 准备阶段
**当前故事**: Story 0 - 数据资源准备
**整体进度**: 1/6 故事完成（16.7%）

### 里程碑完成情况

| 里程碑 | 计划日期 | 实际日期 | 状态 |
|--------|---------|---------|------|
| 准备阶段完成 | 第2天 | - | 🟢 95%完成 |
| MVP第一版 | 第16天 | - | ⏳ 待开始 |
| 功能增强版 | 第30天 | - | ⏳ 待开始 |
| 完整产品版 | 第37天 | - | ⏳ 待开始 |

### 已完成工作

**✅ 准备工作**:
- 需求文档编写（need.md）
- 用户故事拆分（本文档）
- 项目Constitution创建（v1.1.0）
- 技术架构设计
- 实施计划制定

**✅ Story 0（95%完成）**:
- 数据目录结构创建
- ECDICT词典下载（770,612词条）
- 样例书籍下载（3本）
- Phrasal verbs数据收集（124个）
- 雅思映射表创建
- 数据验证报告生成
- 数据说明文档编写

**✅ 项目骨架**:
- 目录结构搭建（符合Constitution）
- 配置文件创建（requirements.txt, pyproject.toml）
- README.md编写
- Git仓库初始化
- 虚拟环境配置

### 当前任务

**⏳ Story 0 - 剩余5%**:
- [ ] T009: 编写数据转换脚本 `scripts/prepare_data.py`
  - 从ECDICT筛选Oxford 3000词汇
  - 分配CEFR等级
  - 生成标准格式CSV

### 下一步计划

**即将开始**:
1. 完成Story 0剩余任务（数据转换脚本）
2. 开始Story 1开发（基础词汇分析）
   - 文本提取模块
   - NLP处理模块
   - 等级匹配模块

### 风险与挑战

**当前风险**:
1. **数据质量**: ECDICT到CEFR的映射准确性需验证
2. **词组识别复杂度**: 分离型词组识别技术难度较高
3. **性能优化**: 大文件处理速度可能需要额外优化

**应对措施**:
1. 使用Oxford 3000标记作为CEFR映射的参考基准
2. Story 3采用迭代开发，先实现基础功能
3. 遵循Constitution性能优化策略（全局加载、缓存、批处理）

### 时间线预测

**预计完成时间**:
- **MVP版本**（Story 1-2）: 第16天（约2周后）
- **增强版本**（Story 3-4）: 第30天（约4周后）
- **完整版本**（Story 5）: 第37天（约5周后）

---

## 6. 关键注意事项

### 技术风险

#### 1. 词组识别复杂度

**挑战**:
- 分离词组识别（如"look it up"）是技术难点
- 需要复杂的依存句法分析
- 准确率难以达到100%

**应对**:
- 采用多种策略组合（词典+模式+依存分析）
- 设定合理的准确率目标（>80%）
- 迭代优化，先覆盖常见情况

#### 2. 数据质量依赖

**挑战**:
- ECDICT到CEFR的映射不是官方标准
- 词组词典覆盖面有限（当前124个）
- 中文释义的准确性依赖数据源

**应对**:
- 使用Oxford 3000标记辅助CEFR映射
- Phase 2扩充词组词典到500+
- 提供多个数据源选项（离线+在线）

#### 3. 性能要求

**挑战**:
- 大文件（100+页）处理速度要求高
- spaCy模型加载耗时
- 内存使用需控制

**应对**:
- 严格遵循Constitution性能优化策略
- 全局模型加载
- LRU缓存
- 批处理
- 性能基准测试

### 数据依赖

**关键依赖**:
- Story 1-5 都依赖于 Story 0 的数据准备
- 必须先完成 Story 0 才能开始后续开发

**数据文件清单**:
```
必需:
- data/vocabularies/cefr_wordlist.csv (Story 1)
- data/sample_books/*.txt (测试)

重要:
- data/phrases/phrasal_verbs.json (Story 3)
- data/dictionaries/ECDICT/*.csv (Story 4)

可选:
- data/mappings/cefr_ielts_mapping.json (Story 2)
```

### 开发建议

#### 1. 优先保证MVP功能稳定

**MVP核心**（Story 1-2）:
- 基础词汇分析
- 多格式输出
- 统计展示

**验收标准**:
- 功能完整可用
- 测试覆盖率>80%
- 性能达标

#### 2. 每个Story完成后充分测试

**测试清单**:
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 性能基准测试
- [ ] 代码质量检查（pylint ≥8.5）
- [ ] 用户验收测试

#### 3. 及时更新进度和文档

**维护要求**:
- 每日更新任务进度
- 重要决策记录在文档中
- 代码提交遵循Conventional Commits
- 定期更新README和CHANGELOG

#### 4. 遵循Constitution原则

**核心原则**:
- 简单性优先（Principle I）
- 模块化设计（Principle II）
- 数据质量第一（Principle III）
- 测试驱动（Principle IV）
- CLI优先（Principle V）
- 项目结构清晰（Principle VI）

### 质量保证

**代码质量**:
- PEP 8严格遵守
- 类型注解100%
- Docstrings完整
- 代码审查

**测试质量**:
- 单元测试覆盖率>80%
- 关键路径100%覆盖
- 边缘案例覆盖
- 性能回归测试

**文档质量**:
- README清晰
- API文档完整
- 代码注释充分
- 用户指南友好

---

## 附录

### 相关文档

**核心文档**:
- [主需求文档](../need.md) - 完整的需求规格说明
- [项目Constitution](../.specify/memory/constitution.md) - 架构DNA和治理原则
- [实施计划](../.specify/implementation-plan.md) - 技术架构和实施细节
- [任务列表](../.specify/tasks.md) - 详细的任务清单

**用户故事**:
- [Story 0: 数据资源准备](../user-story-0-数据准备.md)
- [Story 1: 基础词汇等级分析](../user-story-1-基础词汇分析.md)
- [Story 2: 格式化输出和统计展示](../user-story-2-格式化输出.md)
- [Story 3: 词组识别](../user-story-3-词组识别.md)
- [Story 4: 中文释义集成](../user-story-4-中文释义.md)
- [Story 5: 例句提取和完整功能](../user-story-5-例句提取.md)

### 技术参考

**核心技术栈**:
- Python 3.10+
- spaCy 3.7（NLP处理）
- pandas 2.1（数据处理）
- click 8.1（CLI框架）
- rich 13.7（终端输出美化）

**数据源**:
- ECDICT: https://github.com/skywind3000/ECDICT
- Phrasal Verbs: https://github.com/Semigradsky/phrasal-verbs
- Project Gutenberg: https://www.gutenberg.org/

### 联系与反馈

**项目维护**:
- GitHub仓库: [待添加]
- 问题跟踪: [待添加]
- 文档更新: 每周

---

**文档版本**: v2.0
**创建日期**: 2025-11-03
**最后更新**: 2025-11-03
**下一步行动**: 🎯 完成Story 0数据转换脚本，准备开始Story 1开发
