# Implementation Plan: 英文书词汇等级分析工具

**Branch**: `main` | **Date**: 2025-11-03 | **Spec**: [need.md](../need.md)
**Project**: English Book Vocabulary Level Analyzer
**Type**: CLI Application (Single Project)

---

## Summary

构建一个命令行工具，将英文书籍（TXT/PDF/DOCX）转换为按CEFR等级（A1-C2）分类的单词表，包含中文释义和例句，帮助用户有针对性地背单词。采用管道模式（Pipeline Pattern）处理文本流，外观模式（Facade Pattern）统一协调各模块。核心技术栈：Python 3.10+ + spaCy + pandas + click。

---

## Technical Context

### 核心技术栈

**Language/Version**: Python 3.10+
**Primary Dependencies**:
- spaCy 3.7 + en_core_web_sm 模型（NLP处理）
- PyPDF2 2.x（PDF文本提取）
- python-docx 1.x（Word文档提取）
- pandas 2.x（数据处理和统计）
- click 8.x（CLI框架）
- rich 13.x（终端美化输出）

**Development Tools**:
- pytest + pytest-cov（测试和覆盖率）
- black + isort（代码格式化）
- pylint + flake8 + mypy（代码质量检查）
- pre-commit（Git hooks）

**Storage**:
- CSV文件（词汇表、词组表）
- JSON文件（配置、映射表、输出结果）
- 无数据库依赖

**Testing**: pytest + unittest.mock
**Target Platform**: macOS/Linux/Windows（跨平台CLI）
**Project Type**: Single project（单体命令行应用）

### 性能目标与约束

**Performance Goals**:
- 小文件（<5页）：<5秒
- 中文件（20-50页）：<30秒
- 大文件（100页）：<90秒
- 内存峰值：<500MB
- 拒绝处理：>50MB的文件

**Constraints**:
- 单线程处理（不使用多进程/多线程）
- spaCy模型全局加载一次
- 词汇查询必须使用@lru_cache缓存
- spaCy批处理：100句/批次
- pandas必须使用索引加速查询

**Scale/Scope**:
- 支持词汇量：5000-10000词
- 词组数量：500+
- 样例书籍：3-5本
- 单次处理：1本书（不支持批量）

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Simplicity Gates

- ✅ **Single Project**: CLI工具，不需要前后端分离
- ✅ **No Framework Overkill**: 使用click（轻量CLI框架），不需要Flask/Django
- ✅ **Minimal Dependencies**: 只使用必需的NLP和文件处理库
- ✅ **Direct Data Access**: 直接读取CSV/JSON，不需要ORM或数据库
- ✅ **No Premature Abstraction**: 外观模式+管道模式，架构清晰简单

### ⚠️ Complexity Justifications

| Potential Complexity | Why Needed | Simpler Alternative Rejected |
|---------------------|------------|------------------------------|
| spaCy依赖（>100MB） | 词形还原、词性标注必需 | 正则表达式无法准确处理词形变化 |
| 管道模式6个模块 | 各阶段职责明确，易测试 | 单个大函数难以维护和扩展 |
| dataclass数据结构 | 类型安全，IDE友好 | 字典传递数据易出错，难调试 |

---

## Architecture Overview

### 设计模式

#### 1. Pipeline Pattern（管道模式）

```
文件输入 → 文本提取 → NLP处理 → 词组识别 →
等级匹配 → 统计分析 → 输出生成 → 结果文件
```

每个阶段独立、可测试、可替换。

#### 2. Facade Pattern（外观模式）

```python
class VocabularyAnalyzer:
    """统一协调所有模块的外观类"""
    def analyze(self, file_path: str) -> VocabularyAnalysis:
        # 协调6个模块的执行
        pass
```

CLI只调用`VocabularyAnalyzer`，不直接访问底层模块。

### 核心数据结构（dataclass）

```python
@dataclass
class Word:
    word: str              # 词形还原后的单词
    level: str             # CEFR等级 (A1-C2+)
    word_type: str         # 词性 (noun/verb/adj等)
    definition_cn: str     # 中文释义
    frequency: int         # 出现频次
    examples: List[str]    # 例句

@dataclass
class Phrase:
    phrase: str            # 词组 (如 look up)
    type: str              # 类型 (phrasal_verb/collocation)
    level: str             # CEFR等级
    separable: bool        # 是否可分离
    definition_cn: str     # 中文释义
    frequency: int         # 出现频次
    examples: List[str]    # 例句

@dataclass
class VocabularyAnalysis:
    metadata: Dict         # 元数据（文件名、日期等）
    statistics: Dict       # 统计数据（各等级词数）
    words_by_level: Dict[str, List[Word]]    # 按等级分类的单词
    phrases: List[Phrase]                     # 词组列表
    proper_nouns: List[Word]                  # 专有名词
```

---

## Project Structure

### Documentation (this feature)

```text
.specify/
├── implementation-plan.md           # 本文件（技术实现计划）
├── story-0-data-preparation-spec.md # Story 0规格
├── story-0-clarifications.md         # 澄清问题
├── story-0-execution-summary.md      # Story 0执行总结
└── templates/                         # Specify模板
```

### Source Code (repository root)

```text
vocab-analyzer/                       # 项目根目录
├── README.md                          # 项目说明
├── requirements.txt                   # Python依赖
├── setup.py                           # 安装配置
├── pyproject.toml                     # 项目配置（black/isort/mypy）
├── .pre-commit-config.yaml            # Git hooks配置
│
├── config/                            # 配置文件
│   └── default_config.yaml            # 默认配置（模型、路径、批次大小）
│
├── data/                              # 数据资源（见data/README.md）
│   ├── vocabularies/                  # CEFR词汇表
│   ├── phrases/                       # 词组词典
│   ├── dictionaries/                  # 中英词典
│   ├── sample_books/                  # 样例书籍
│   └── mappings/                      # CEFR-IELTS映射表
│
├── src/                               # 源代码
│   ├── vocab_analyzer/                # 主包
│   │   ├── __init__.py
│   │   ├── __main__.py                # 入口点（python -m vocab_analyzer）
│   │   │
│   │   ├── models/                    # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── word.py                # Word dataclass
│   │   │   ├── phrase.py              # Phrase dataclass
│   │   │   └── analysis.py            # VocabularyAnalysis dataclass
│   │   │
│   │   ├── extractors/                # 文本提取模块
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # BaseExtractor抽象类
│   │   │   ├── txt_extractor.py       # TXT提取器
│   │   │   ├── pdf_extractor.py       # PDF提取器
│   │   │   └── docx_extractor.py      # DOCX提取器
│   │   │
│   │   ├── processors/                # NLP处理模块
│   │   │   ├── __init__.py
│   │   │   ├── tokenizer.py           # 分词和词形还原
│   │   │   ├── phrase_detector.py     # 词组识别
│   │   │   └── proper_noun_filter.py  # 专有名词识别
│   │   │
│   │   ├── matchers/                  # 等级匹配模块
│   │   │   ├── __init__.py
│   │   │   ├── level_matcher.py       # CEFR等级匹配
│   │   │   └── dictionary_loader.py   # 词典加载器
│   │   │
│   │   ├── analyzers/                 # 统计分析模块
│   │   │   ├── __init__.py
│   │   │   ├── statistics.py          # 统计计算
│   │   │   └── example_extractor.py   # 例句提取
│   │   │
│   │   ├── exporters/                 # 输出生成模块
│   │   │   ├── __init__.py
│   │   │   ├── json_exporter.py       # JSON导出
│   │   │   ├── csv_exporter.py        # CSV导出
│   │   │   └── markdown_exporter.py   # Markdown导出
│   │   │
│   │   ├── core/                      # 核心协调模块
│   │   │   ├── __init__.py
│   │   │   ├── analyzer.py            # VocabularyAnalyzer（外观类）
│   │   │   ├── pipeline.py            # Pipeline管理
│   │   │   └── config.py              # 配置加载
│   │   │
│   │   ├── cli/                       # 命令行界面
│   │   │   ├── __init__.py
│   │   │   ├── main.py                # click命令定义
│   │   │   └── display.py             # rich输出格式化
│   │   │
│   │   └── utils/                     # 工具函数
│   │       ├── __init__.py
│   │       ├── file_utils.py          # 文件操作
│   │       ├── text_utils.py          # 文本处理
│   │       └── cache.py               # 缓存装饰器
│
├── tests/                             # 测试代码
│   ├── __init__.py
│   ├── conftest.py                    # pytest配置和fixtures
│   │
│   ├── unit/                          # 单元测试
│   │   ├── test_extractors.py
│   │   ├── test_processors.py
│   │   ├── test_matchers.py
│   │   ├── test_analyzers.py
│   │   └── test_exporters.py
│   │
│   ├── integration/                   # 集成测试
│   │   ├── test_pipeline.py           # 测试完整管道
│   │   └── test_analyzer.py           # 测试VocabularyAnalyzer
│   │
│   └── fixtures/                      # 测试数据
│       ├── sample_text.txt
│       ├── sample.pdf
│       └── expected_output.json
│
└── scripts/                           # 辅助脚本
    ├── prepare_data.py                # 数据准备脚本
    ├── download_model.py              # 下载spaCy模型
    └── validate_data.py               # 验证数据完整性
```

**Structure Decision**:
选择单项目结构（Option 1），因为：
1. CLI工具无需前后端分离
2. 模块按功能垂直切分（extractors/processors/matchers等）
3. 每个模块职责单一，易于测试和维护
4. 使用`core/`目录统一协调各模块（外观模式）

---

## Module Responsibilities

### 1. Extractors（文本提取模块）

**职责**: 从不同格式的文件中提取纯文本

**接口**:
```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> str:
        """提取文本，返回纯文本字符串"""
        pass
```

**实现**:
- `TxtExtractor`: UTF-8解码
- `PdfExtractor`: PyPDF2提取文字
- `DocxExtractor`: python-docx提取段落

**输出**: 纯文本字符串

---

### 2. Processors（NLP处理模块）

**职责**: 分词、词形还原、词组识别、专有名词过滤

**接口**:
```python
class Tokenizer:
    def process(self, text: str) -> List[Token]:
        """分词和词形还原"""
        pass

class PhraseDetector:
    def detect(self, tokens: List[Token]) -> List[Phrase]:
        """识别词组（包括分离的动词短语）"""
        pass
```

**关键技术**:
- spaCy的`nlp.pipe()`批处理（100句/批）
- 依存句法分析识别分离词组
- 词性标注（PROPN）识别专有名词

**输出**: Token列表 + Phrase列表

---

### 3. Matchers（等级匹配模块）

**职责**: 将单词和词组匹配到CEFR等级，添加中文释义

**接口**:
```python
class LevelMatcher:
    @lru_cache(maxsize=10000)
    def match_word(self, word: str) -> Optional[WordInfo]:
        """匹配单词等级和释义（带缓存）"""
        pass
```

**关键技术**:
- pandas DataFrame + 索引加速查询
- @lru_cache缓存查询结果
- 超纲词标记为C2+

**输出**: 带等级和释义的Word对象列表

---

### 4. Analyzers（统计分析模块）

**职责**: 统计词汇分布、提取例句

**接口**:
```python
class StatisticsAnalyzer:
    def analyze(self, words: List[Word]) -> Dict:
        """生成统计数据"""
        pass

class ExampleExtractor:
    def extract(self, word: str, text: str, max_examples: int = 3) -> List[str]:
        """提取例句"""
        pass
```

**输出**: 统计数据字典 + 例句列表

---

### 5. Exporters（输出生成模块）

**职责**: 生成JSON/CSV/Markdown格式的输出文件

**接口**:
```python
class BaseExporter(ABC):
    @abstractmethod
    def export(self, analysis: VocabularyAnalysis, output_path: str) -> None:
        """导出分析结果"""
        pass
```

**输出**: 文件（JSON/CSV/MD）

---

### 6. Core（核心协调模块）

**职责**: 协调整个分析流程（外观模式）

**接口**:
```python
class VocabularyAnalyzer:
    def __init__(self, config: Config):
        """初始化并加载spaCy模型、词汇表"""
        pass

    def analyze(self, file_path: str) -> VocabularyAnalysis:
        """执行完整分析流程"""
        # 1. 提取文本
        # 2. NLP处理
        # 3. 等级匹配
        # 4. 统计分析
        # 5. 返回结果
        pass
```

**输出**: VocabularyAnalysis对象

---

## Data Flow

```
用户输入文件路径
    ↓
CLI (main.py)
    ↓
VocabularyAnalyzer.analyze()
    ↓
1. Extractor.extract() → 纯文本
    ↓
2. Tokenizer.process() → List[Token]
    ↓
3. PhraseDetector.detect() → List[Phrase]
    ↓
4. LevelMatcher.match_word() → List[Word]
    ↓
5. StatisticsAnalyzer.analyze() → Dict
    ↓
6. ExampleExtractor.extract() → 添加例句
    ↓
7. 组装 VocabularyAnalysis 对象
    ↓
Exporter.export() → 输出文件
    ↓
CLI显示统计结果（rich格式化）
```

---

## Configuration Management

### default_config.yaml

```yaml
# NLP模型配置
nlp:
  model: "en_core_web_sm"
  batch_size: 100
  disable_components: ["ner"]  # 禁用不需要的组件

# 文件处理配置
files:
  max_size_mb: 50
  encoding: "utf-8"

# 数据路径配置
data:
  vocabularies_dir: "data/vocabularies"
  phrases_file: "data/phrases/phrasal_verbs.csv"
  dictionary_file: "data/dictionaries/ecdict_core.csv"
  mappings_file: "data/mappings/cefr_ielts_mapping.json"

# 性能配置
performance:
  cache_size: 10000
  max_examples: 3

# 输出配置
output:
  default_format: "json"
  include_examples: true
  include_statistics: true
```

---

## CLI Interface Design

### 命令行用法

```bash
# 基本用法
vocab-analyzer input.txt

# 指定输出格式
vocab-analyzer input.pdf --format json,csv,md

# 指定输出目录
vocab-analyzer input.docx --output ./results

# 显示详细过程
vocab-analyzer input.txt --verbose

# 只输出特定等级
vocab-analyzer input.txt --levels B2,C1,C2

# 显示帮助
vocab-analyzer --help
```

### 输出示例（rich格式化）

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

## Performance Optimization Strategies

### 1. spaCy优化

```python
# 全局加载模型（仅加载一次）
class VocabularyAnalyzer:
    _nlp = None

    @classmethod
    def get_nlp(cls):
        if cls._nlp is None:
            cls._nlp = spacy.load("en_core_web_sm", disable=["ner"])
        return cls._nlp

# 批处理文本
def process_in_batches(texts: List[str], batch_size: int = 100):
    nlp = VocabularyAnalyzer.get_nlp()
    for doc in nlp.pipe(texts, batch_size=batch_size):
        yield doc
```

### 2. 词汇查询缓存

```python
from functools import lru_cache

class LevelMatcher:
    @lru_cache(maxsize=10000)
    def match_word(self, word: str) -> Optional[WordInfo]:
        # 查询被缓存，重复词汇直接返回
        return self._lookup_in_dataframe(word)
```

### 3. pandas索引加速

```python
# 加载词汇表时创建索引
df = pd.read_csv("vocabulary.csv")
df.set_index("word", inplace=True)  # 使用word列作为索引

# 查询时使用.loc（O(1)复杂度）
word_info = df.loc[word]
```

### 4. 内存管理

```python
# 及时释放大对象
def analyze(self, file_path: str):
    text = self.extract_text(file_path)
    tokens = self.process_text(text)
    del text  # 释放原始文本内存
    # ...继续处理
```

---

## Error Handling Strategy

### 文件处理错误

```python
class FileError(Exception):
    """文件相关错误基类"""
    pass

class FileTooLargeError(FileError):
    """文件超过50MB"""
    pass

class UnsupportedFormatError(FileError):
    """不支持的文件格式"""
    pass
```

### 用户友好的错误提示

```python
try:
    analyzer.analyze(file_path)
except FileTooLargeError:
    console.print("[red]❌ 文件过大（>50MB），请使用较小的文件[/red]")
except UnsupportedFormatError:
    console.print("[red]❌ 不支持的格式，请使用 .txt, .pdf 或 .docx 文件[/red]")
except Exception as e:
    console.print(f"[red]❌ 处理失败: {str(e)}[/red]")
```

---

## Testing Strategy

### 单元测试（Unit Tests）

每个模块独立测试，使用mock隔离依赖：

```python
# tests/unit/test_tokenizer.py
def test_tokenizer_lemmatization():
    tokenizer = Tokenizer()
    tokens = tokenizer.process("I went to school yesterday")
    assert tokens[1].lemma == "go"  # went → go
```

### 集成测试（Integration Tests）

测试完整流程：

```python
# tests/integration/test_pipeline.py
def test_full_pipeline():
    analyzer = VocabularyAnalyzer(config)
    result = analyzer.analyze("tests/fixtures/sample.txt")
    assert result.statistics["B1"] > 0
    assert len(result.words_by_level["B1"]) > 0
```

### 测试覆盖率目标

- 单元测试覆盖率：>80%
- 集成测试：覆盖核心流程
- 关键模块（Tokenizer, LevelMatcher）：>90%

---

## Development Phases

### Phase 0: 环境准备（1天）
- [ ] 创建项目目录结构
- [ ] 配置pyproject.toml、requirements.txt
- [ ] 配置pre-commit hooks
- [ ] 下载spaCy模型：`python -m spacy download en_core_web_sm`
- [ ] 完成Story 0数据准备

### Phase 1: 核心模块开发（Story 1, 1周）
- [ ] 实现Extractors（TXT/PDF/DOCX）
- [ ] 实现Tokenizer（分词+词形还原）
- [ ] 实现LevelMatcher（等级匹配）
- [ ] 实现基础VocabularyAnalyzer
- [ ] 单元测试覆盖率>70%

### Phase 2: 输出和CLI（Story 2, 3-4天）
- [ ] 实现StatisticsAnalyzer
- [ ] 实现Exporters（JSON/CSV/MD）
- [ ] 实现CLI命令（click）
- [ ] 实现rich格式化输出
- [ ] 集成测试通过

### Phase 3: 高级功能（Story 3-4, 1-2周）
- [ ] 实现PhraseDetector（词组识别）
- [ ] 实现ExampleExtractor（例句提取）
- [ ] 集成中文释义
- [ ] 性能优化

### Phase 4: 完善和测试（Story 5, 1周）
- [ ] 添加例句提取
- [ ] 完善CLI输出
- [ ] 性能测试和优化
- [ ] 文档编写

---

## Dependencies Management

### requirements.txt

```txt
# Core NLP
spacy>=3.7.0,<4.0.0
# 运行后执行: python -m spacy download en_core_web_sm

# File processing
PyPDF2>=2.0.0,<3.0.0
python-docx>=1.0.0,<2.0.0

# Data processing
pandas>=2.0.0,<3.0.0

# CLI
click>=8.1.0,<9.0.0
rich>=13.0.0,<14.0.0

# Configuration
PyYAML>=6.0,<7.0

# Development
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
isort>=5.12.0
pylint>=2.17.0
flake8>=6.0.0
mypy>=1.4.0
pre-commit>=3.3.0
```

---

## Risk Mitigation

### 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| spaCy模型加载慢 | 启动时间长 | 高 | 全局加载一次，提示用户等待 |
| 词组识别不准确 | 功能质量下降 | 中 | Phase 1先不做，Phase 3再优化 |
| 大文件内存溢出 | 程序崩溃 | 中 | 限制50MB，批处理文本 |
| PDF提取失败 | 部分文件无法处理 | 低 | 捕获异常，提示用户转换格式 |

---

## Success Criteria

### 功能完整性
- ✅ 支持TXT/PDF/DOCX三种格式
- ✅ 词形还原准确率>95%
- ✅ 等级匹配准确率>95%（基于词汇表）
- ✅ 输出JSON/CSV/MD三种格式

### 性能达标
- ✅ 100页书籍<60秒
- ✅ 内存峰值<500MB
- ✅ 测试覆盖率>80%

### 用户体验
- ✅ CLI输出清晰美观（rich格式化）
- ✅ 错误提示友好
- ✅ 进度实时显示

---

## Next Actions

1. ✅ **完成Story 0数据准备**（已调研，待下载）
2. ⏳ **创建项目结构**（按本plan执行）
3. ⏳ **配置开发环境**（requirements.txt + pre-commit）
4. ⏳ **开始Story 1开发**（核心功能）

---

**Plan Version**: 1.0
**Created**: 2025-11-03
**Status**: ✅ 规划完成，准备执行
**Estimated Total Time**: 4-5周
