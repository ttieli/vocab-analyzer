# Tasks: 英文书词汇等级分析工具

**Input**:
- Spec: [need.md](../need.md)
- Plan: [implementation-plan.md](./implementation-plan.md)
- User Stories: [user-stories-index.md](../user-stories-index.md)

**Project Type**: Single CLI application
**Path Convention**: `src/vocab_analyzer/`, `tests/` at repository root

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US0, US1, US2, etc.)
- Exact file paths included in descriptions

---

## Phase 0: 数据准备 (Story 0) ✅ 95%完成

**Goal**: 收集并整理所有必需的基础数据资源

**Status**: 数据下载和验证完成，待数据转换脚本

### 数据下载 ✅

- [x] T001 [P] [US0] 创建data目录结构（vocabularies/phrases/dictionaries/sample_books/mappings）
- [x] T002 [P] [US0] 创建CEFR-IELTS映射表 data/mappings/cefr_ielts_mapping.json
- [x] T003 [P] [US0] 编写数据说明文档 data/README.md
- [x] T004 [US0] 下载ECDICT词典数据到 data/dictionaries/ECDICT/ (770,612词条)
  ```bash
  cd data/dictionaries
  git clone https://github.com/skywind3000/ECDICT.git
  ```
- [x] T005 [P] [US0] 下载样例书籍1：Pride and Prejudice 到 data/sample_books/pride_and_prejudice.txt (735KB)
- [x] T006 [P] [US0] 下载样例书籍2：Alice in Wonderland 到 data/sample_books/alice_in_wonderland.txt (148KB)
- [x] T007 [P] [US0] 下载样例书籍3：Animal Farm 到 data/sample_books/animal_farm.txt (21KB)
- [x] T008 [US0] 下载phrasal verbs数据到 data/phrases/ (124个)
  ```bash
  cd data/phrases
  git clone https://github.com/Semigradsky/phrasal-verbs.git
  ```

### 数据转换

- [ ] T009 [US0] 编写数据转换脚本 scripts/prepare_data.py
  - 从ECDICT筛选Oxford 3000词汇
  - 根据词频和标签分配CEFR等级
  - 提取字段：word, level, pos, translation, phonetic
- [ ] T010 [US0] 运行转换脚本，生成 data/vocabularies/cefr_wordlist.csv (目标5000+词)
- [ ] T011 [US0] 转换phrasal verbs为CSV格式 data/phrases/phrasal_verbs.csv (100+词组)

### 数据验证

- [ ] T012 [US0] 编写数据验证脚本 scripts/validate_data.py
- [ ] T013 [US0] 验证词汇表：统计词数≥5000，检查各等级分布
- [ ] T014 [US0] 验证中英词典：随机抽样100词检查释义准确性
- [ ] T015 [US0] 验证样例书籍：UTF-8编码，文件可读
- [ ] T016 [US0] 生成数据统计报告 data/data_statistics.md

**Checkpoint**: 数据准备完成，可以开始代码开发

---

## Phase 1: 项目初始化 (Setup) ✅ 100%完成

**Purpose**: 创建项目结构和开发环境配置

**Dependencies**: Story 0完成

**Status**: 已完成，详见 .specify/phase-1-implementation-summary.md

- [x] T017 [US1] 创建项目根目录 vocab-analyzer/
- [x] T018 [US1] 创建源代码目录结构
  ```
  src/vocab_analyzer/
  ├── __init__.py
  ├── models/
  ├── extractors/
  ├── processors/
  ├── matchers/
  ├── analyzers/
  ├── exporters/
  ├── core/
  ├── cli/
  └── utils/
  ```
- [x] T019 [P] [US1] 创建tests目录结构
  ```
  tests/
  ├── __init__.py
  ├── conftest.py (含7个fixtures)
  ├── unit/
  ├── integration/
  └── fixtures/
  ```
- [x] T020 [P] [US1] 创建配置文件 config/default_config.yaml (完整配置)
- [x] T021 [P] [US1] 创建requirements.txt with core dependencies
  ```
  spacy>=3.7.0
  PyPDF2>=2.0.0
  python-docx>=1.0.0
  pandas>=2.0.0
  click>=8.1.0
  rich>=13.0.0
  PyYAML>=6.0
  tqdm>=4.65.0
  ```
- [x] T022 [P] [US1] 创建开发依赖 requirements-dev.txt
  ```
  pytest>=7.4.0
  pytest-cov>=4.1.0
  pytest-mock>=3.11.0
  black>=23.0.0
  isort>=5.12.0
  pylint>=2.17.0
  flake8>=6.0.0
  mypy>=1.5.0
  pre-commit>=3.3.0
  ```
- [x] T023 [P] [US1] 配置pyproject.toml (black, isort, mypy, pytest, coverage完整配置)
- [ ] T024 [P] [US1] 配置.pre-commit-config.yaml (Git hooks) - 非阻塞，可后补
- [x] T025 [US1] 创建setup.py for package installation (完整metadata和entry_points)
- [x] T026 [US1] 下载spaCy模型：en_core_web_sm v3.8.0 已安装
  ```bash
  python -m venv venv
  source venv/bin/activate
  pip install spacy
  python -m spacy download en_core_web_sm
  ```
- [x] T027 [P] [US1] 创建README.md with installation instructions (详尽文档)
- [x] T028 [P] [US1] 创建.gitignore (Python/IDE/Data完整配置)

**Checkpoint**: ✅ 项目结构就绪，可以开始Phase 2编码

---

## Phase 2: 基础设施 (Foundational) ✅ 100%完成

**Purpose**: 核心基础设施，阻塞所有用户故事

**Status**: 已完成，详见 .specify/phase-2-implementation-summary.md

**⚠️ CRITICAL**: 此阶段已100%完成，所有User Story实现已解除阻塞 ✅

### 数据模型定义 ✅

- [x] T029 [P] [Foundation] 创建Word dataclass in src/vocab_analyzer/models/word.py (125行)
  ```python
  @dataclass
  class Word:
      word: str
      level: str
      word_type: str
      definition_cn: str = ""
      frequency: int = 0
      examples: List[str] = field(default_factory=list)
      phonetic: Optional[str] = None
      original_forms: List[str] = field(default_factory=list)
      # 含验证、add_example()、increment_frequency()、to_dict()等方法
  ```
- [x] T030 [P] [Foundation] 创建Phrase dataclass in src/vocab_analyzer/models/phrase.py (155行)
  - 支持separable标记解析 (parse_phrasal_verb_notation)
- [x] T031 [P] [Foundation] 创建VocabularyAnalysis dataclass in src/vocab_analyzer/models/analysis.py (235行)
  - 自动统计计算、按等级/词性筛选、top words等

### 配置管理 ✅

- [x] T032 [Foundation] 实现Config类 in src/vocab_analyzer/core/config.py (190行)
  - ✅ 加载YAML配置文件
  - ✅ 提供配置访问接口 (点符号get/set)
  - ✅ 20+个便捷属性 (nlp_model, batch_size, etc.)
  - ✅ 自动路径解析 (相对→绝对)

### 工具函数 ✅

- [x] T033 [P] [Foundation] 实现文件操作工具 in src/vocab_analyzer/utils/file_utils.py (180行)
  - ✅ check_file_exists(), check_file_size(), get_file_extension()
  - ✅ validate_file_for_analysis(), get_output_file_path()
  - ✅ read_file_safely(), write_file_safely()
  - 共12个工具函数
- [x] T034 [P] [Foundation] 实现文本处理工具 in src/vocab_analyzer/utils/text_utils.py (210行)
  - ✅ clean_text(), split_sentences(), normalize_word()
  - ✅ extract_context_around_word(), is_likely_proper_noun()
  - ✅ contains_digit(), is_all_punctuation(), word_count()
  - 共14个工具函数
- [x] T035 [P] [Foundation] 实现缓存装饰器 in src/vocab_analyzer/utils/cache.py (190行)
  - ✅ @cached_property, @memoize (lru_cache包装)
  - ✅ SimpleCache类 (含统计: hit_rate, stats)
  - ✅ 全局缓存: get_vocabulary_cache(), get_phrase_cache()

### 测试基础设施 ✅

- [x] T036 [P] [Foundation] 配置pytest in tests/conftest.py (已在Phase 1完成)
  - ✅ 7个fixtures定义
  - ✅ 测试路径配置
- [x] T037 [P] [Foundation] 准备测试数据 in tests/fixtures/
  - ✅ sample_text.txt (4段英文文本)
  - ✅ expected_output.json (预期输出格式)
  - ✅ tests/unit/test_word.py (15个测试用例)

**Checkpoint**: ✅ Foundation complete - User story implementation can begin

**代码统计**:
- 生产代码: 1,285行 (7个核心模块)
- 测试代码: ~150行 (15个测试用例)
- 工具函数: 40+个

---

## Phase 3: User Story 1 - 基础词汇等级分析 (Priority: P0) 🎯 MVP

**Goal**: 实现核心的文本提取、分词、词形还原和等级匹配功能

**Independent Test**: 输入一个TXT文件，输出包含单词、等级、频次的基础JSON文件

### 实现文本提取器 (Extractors)

- [ ] T038 [P] [US1] 创建BaseExtractor抽象类 in src/vocab_analyzer/extractors/base.py
  ```python
  class BaseExtractor(ABC):
      @abstractmethod
      def extract(self, file_path: str) -> str:
          pass
  ```
- [ ] T039 [P] [US1] 实现TxtExtractor in src/vocab_analyzer/extractors/txt_extractor.py
  - 读取UTF-8文本文件
  - 处理编码错误
- [ ] T040 [P] [US1] 实现PdfExtractor in src/vocab_analyzer/extractors/pdf_extractor.py
  - 使用PyPDF2提取文本
  - 处理无法提取的PDF
- [ ] T041 [P] [US1] 实现DocxExtractor in src/vocab_analyzer/extractors/docx_extractor.py
  - 使用python-docx提取段落
  - 合并段落文本

### 实现NLP处理器 (Processors)

- [ ] T042 [US1] 实现Tokenizer in src/vocab_analyzer/processors/tokenizer.py
  - 全局加载spaCy模型 (get_nlp() classmethod)
  - 实现批处理：nlp.pipe(texts, batch_size=100)
  - 词形还原：token.lemma_
  - 词性标注：token.pos_
  - 过滤停用词
- [ ] T043 [US1] 实现ProperNounFilter in src/vocab_analyzer/processors/proper_noun_filter.py
  - 识别专有名词（词性=PROPN）
  - 排除句首大写词的误判

### 实现等级匹配器 (Matchers)

- [ ] T044 [US1] 实现DictionaryLoader in src/vocab_analyzer/matchers/dictionary_loader.py
  - 加载cefr_wordlist.csv为pandas DataFrame
  - 创建word列索引
  - 加载ecdict_core.csv
- [ ] T045 [US1] 实现LevelMatcher in src/vocab_analyzer/matchers/level_matcher.py
  - @lru_cache(maxsize=10000)
  - match_word(word) -> Optional[WordInfo]
  - 使用df.loc[word]快速查询
  - 超纲词返回C2+

### 实现核心分析器 (Core Analyzer)

- [ ] T046 [US1] 实现Pipeline类 in src/vocab_analyzer/core/pipeline.py
  - 定义6个处理阶段
  - 管道执行逻辑
- [ ] T047 [US1] 实现VocabularyAnalyzer外观类 in src/vocab_analyzer/core/analyzer.py
  - 初始化所有模块
  - analyze(file_path) -> VocabularyAnalysis
  - 协调Extractor -> Tokenizer -> LevelMatcher
  - 统计词频
  - 组装VocabularyAnalysis对象

### 基础JSON导出

- [ ] T048 [US1] 实现JsonExporter in src/vocab_analyzer/exporters/json_exporter.py
  - export(analysis, output_path)
  - 格式化JSON输出（indent=2）
  - 处理dataclass序列化

### 单元测试 (Story 1)

- [ ] T049 [P] [US1] 测试TxtExtractor in tests/unit/test_extractors.py
- [ ] T050 [P] [US1] 测试Tokenizer in tests/unit/test_processors.py
  - 测试词形还原准确性
  - 测试停用词过滤
- [ ] T051 [P] [US1] 测试LevelMatcher in tests/unit/test_matchers.py
  - 测试已知词匹配
  - 测试超纲词返回C2+
- [ ] T052 [US1] 集成测试VocabularyAnalyzer in tests/integration/test_analyzer.py
  - 使用fixtures/sample_text.txt
  - 验证输出包含正确字段

**Checkpoint**: Story 1完成 - 可生成基础词汇表JSON文件

---

## Phase 4: User Story 2 - 格式化输出和统计展示 (Priority: P0) 🎯 MVP

**Goal**: 将分析结果格式化并生成易用的多种格式输出文件，添加统计数据

**Independent Test**: 输入JSON结果，输出CSV/MD文件，CLI显示美观统计图表

### 实现统计分析器 (Statistics Analyzer)

- [ ] T053 [US2] 实现StatisticsAnalyzer in src/vocab_analyzer/analyzers/statistics.py
  - calculate_level_distribution(words) -> Dict
  - calculate_percentages(statistics) -> Dict
  - 生成metadata字典

### 实现多格式导出器 (Exporters)

- [ ] T054 [P] [US2] 实现CsvExporter in src/vocab_analyzer/exporters/csv_exporter.py
  - export(analysis, output_path)
  - 按等级分类导出
  - UTF-8编码，逗号分隔
- [ ] T055 [P] [US2] 实现MarkdownExporter in src/vocab_analyzer/exporters/markdown_exporter.py
  - export(analysis, output_path)
  - 生成按等级分类的Markdown表格
  - 添加统计摘要

### 实现CLI界面 (CLI)

- [ ] T056 [US2] 实现CLI命令 in src/vocab_analyzer/cli/main.py
  - 使用click定义命令
  - 参数：file_path, --format, --output, --verbose, --levels
  - 调用VocabularyAnalyzer.analyze()
  - 调用相应的Exporter
- [ ] T057 [US2] 实现rich输出格式化 in src/vocab_analyzer/cli/display.py
  - display_progress(stage, total) - 进度条
  - display_statistics(stats) - 等级分布图表
  - display_summary(analysis) - 摘要信息

### 入口点配置

- [ ] T058 [US2] 配置__main__.py in src/vocab_analyzer/__main__.py
  - if __name__ == "__main__": cli.main()
- [ ] T059 [US2] 配置setup.py entry_points
  - console_scripts: vocab-analyzer = vocab_analyzer.cli.main:cli

### 单元测试 (Story 2)

- [ ] T060 [P] [US2] 测试StatisticsAnalyzer in tests/unit/test_analyzers.py
- [ ] T061 [P] [US2] 测试CsvExporter in tests/unit/test_exporters.py
- [ ] T062 [P] [US2] 测试MarkdownExporter in tests/unit/test_exporters.py
- [ ] T063 [US2] 集成测试CLI in tests/integration/test_cli.py
  - 测试完整命令执行
  - 验证多格式输出

**Checkpoint**: Story 2完成 - MVP可交付，支持JSON/CSV/MD输出

---

## Phase 5: User Story 3 - 词组识别 (Priority: P1)

**Goal**: 识别动词短语、分离词组和常见搭配

**Independent Test**: 输入包含phrasal verbs的文本，输出的JSON包含识别出的词组列表

### 实现词组检测器 (Phrase Detector)

- [ ] T064 [US3] 加载phrasal verbs词典 in src/vocab_analyzer/matchers/dictionary_loader.py
  - load_phrasal_verbs() -> pd.DataFrame
- [ ] T065 [US3] 实现PhraseDetector in src/vocab_analyzer/processors/phrase_detector.py
  - detect_phrasal_verbs(doc) -> List[Phrase]
  - 使用spaCy依存句法分析
  - 识别[动词 + 介词/副词]模式
  - 识别分离的词组（如 "look the word up"）
  - 匹配词组词典
- [ ] T066 [US3] 集成PhraseDetector到VocabularyAnalyzer
  - 在Pipeline中添加词组识别阶段
  - 更新VocabularyAnalysis添加phrases字段

### 词组等级匹配

- [ ] T067 [US3] 扩展LevelMatcher支持词组匹配
  - match_phrase(phrase) -> Optional[PhraseInfo]
  - 查询phrasal_verbs.csv

### 更新导出器支持词组

- [ ] T068 [P] [US3] 更新JsonExporter支持phrases字段
- [ ] T069 [P] [US3] 更新CsvExporter导出phrases到单独CSV
- [ ] T070 [P] [US3] 更新MarkdownExporter显示词组表格

### 单元测试 (Story 3)

- [ ] T071 [US3] 测试PhraseDetector in tests/unit/test_processors.py
  - 测试简单phrasal verbs识别
  - 测试分离词组识别（准确率>80%）
- [ ] T072 [US3] 集成测试 in tests/integration/test_phrase_detection.py
  - 使用包含已知phrasal verbs的文本
  - 验证输出包含正确词组

**Checkpoint**: Story 3完成 - 支持词组识别

---

## Phase 6: User Story 4 - 中文释义集成 (Priority: P1)

**Goal**: 为每个单词和词组添加中文释义和词性标注

**Independent Test**: 输出的词汇表包含准确的中文释义字段

### 扩展词典加载器

- [ ] T073 [US4] 加载ECDICT中英词典 in src/vocab_analyzer/matchers/dictionary_loader.py
  - load_ecdict() -> pd.DataFrame
  - 提取字段：word, pos, translation
  - 创建索引

### 扩展等级匹配器

- [ ] T074 [US4] 扩展LevelMatcher添加中文释义
  - match_word() 返回包含definition_cn的WordInfo
  - 从ECDICT查询translation字段
  - 简化释义（保留前3个含义）
  - @lru_cache缓存释义查询

### 更新数据模型

- [ ] T075 [US4] 确认Word dataclass已包含definition_cn字段
- [ ] T076 [US4] 确认Phrase dataclass已包含definition_cn字段

### 更新导出器显示中文释义

- [ ] T077 [P] [US4] 更新JsonExporter包含definition_cn
- [ ] T078 [P] [US4] 更新CsvExporter包含definition_cn列
- [ ] T079 [P] [US4] 更新MarkdownExporter显示中文释义

### 单元测试 (Story 4)

- [ ] T080 [US4] 测试中文释义查询 in tests/unit/test_matchers.py
  - 测试常用词释义准确性
  - 测试释义简化逻辑
- [ ] T081 [US4] 集成测试 in tests/integration/test_cn_definition.py
  - 抽样验证100个高频词
  - 验证释义格式正确

**Checkpoint**: Story 4完成 - 完整支持中英对照

---

## Phase 7: User Story 5 - 例句提取和完整功能 (Priority: P2)

**Goal**: 从原文提取例句，完善所有用户体验细节

**Independent Test**: 输出包含每个词的1-3条原文例句

### 实现例句提取器 (Example Extractor)

- [ ] T082 [US5] 实现ExampleExtractor in src/vocab_analyzer/analyzers/example_extractor.py
  - extract_examples(word, text, max=3) -> List[str]
  - 搜索包含该词的句子
  - 提取不超过20词的句子
  - 按出现顺序返回前3条

### 集成例句提取

- [ ] T083 [US5] 在VocabularyAnalyzer中集成ExampleExtractor
  - 保存原始文本
  - 为每个Word提取examples
  - 为每个Phrase提取examples

### 性能优化

- [ ] T084 [US5] 优化spaCy批处理
  - 确认batch_size=100
  - 测试不同文件大小的性能
- [ ] T085 [US5] 优化内存使用
  - 及时释放大对象
  - 使用生成器处理大文件
- [ ] T086 [US5] 优化词典查询
  - 验证@lru_cache工作正常
  - 确认pandas索引加速查询

### 完善CLI输出

- [ ] T087 [US5] 添加进度条 in src/vocab_analyzer/cli/display.py
  - 使用rich.progress显示实时进度
  - 显示每个阶段的耗时
- [ ] T088 [US5] 添加统计图表
  - 等级分布条形图（ASCII art）
  - 百分比显示
- [ ] T089 [US5] 添加建议信息
  - 根据等级分布推荐适合的IELTS分数段

### 错误处理完善

- [ ] T090 [US5] 实现自定义异常类 in src/vocab_analyzer/utils/exceptions.py
  - FileTooLargeError
  - UnsupportedFormatError
  - ExtractionError
- [ ] T091 [US5] 在CLI中添加友好错误提示
  - 捕获所有异常
  - rich格式化错误信息
  - 提供解决建议

### 性能测试

- [ ] T092 [US5] 测试小文件性能 (<5页) in tests/integration/test_performance.py
  - 验证<5秒
- [ ] T093 [US5] 测试中文件性能 (20-50页)
  - 验证<30秒
- [ ] T094 [US5] 测试大文件性能 (100页)
  - 验证<90秒
- [ ] T095 [US5] 测试内存使用
  - 验证峰值<500MB

### 单元测试 (Story 5)

- [ ] T096 [US5] 测试ExampleExtractor in tests/unit/test_analyzers.py
  - 测试例句提取准确性
  - 测试例句长度限制
- [ ] T097 [US5] 集成测试完整功能 in tests/integration/test_full_pipeline.py
  - 使用sample_books中的真实书籍
  - 验证所有输出字段完整

**Checkpoint**: Story 5完成 - 功能完整，体验完善

---

## Phase 8: 完善与优化 (Polish)

**Purpose**: 跨故事的改进和最终优化

**Dependencies**: 所有核心User Stories (1-5) 完成

### 文档完善

- [ ] T098 [P] [Polish] 完善README.md
  - 添加安装说明
  - 添加使用示例
  - 添加命令行参数说明
  - 添加输出格式说明
- [ ] T099 [P] [Polish] 编写CONTRIBUTING.md
  - 开发环境配置
  - 代码规范
  - 提交规范
- [ ] T100 [P] [Polish] 编写用户手册 docs/user_guide.md
  - 完整使用教程
  - 常见问题解答
  - 示例截图

### 代码质量

- [ ] T101 [Polish] 代码格式化
  - 运行black格式化所有代码
  - 运行isort整理导入
- [ ] T102 [Polish] 代码检查
  - 运行pylint检查所有代码
  - 修复警告和错误
  - 运行mypy类型检查
- [ ] T103 [Polish] 重构优化
  - 提取重复代码
  - 简化复杂函数
  - 优化命名

### 测试完善

- [ ] T104 [P] [Polish] 提高单元测试覆盖率到>80%
- [ ] T105 [P] [Polish] 添加边界测试
  - 空文件
  - 超大文件
  - 特殊字符
  - 编码错误
- [ ] T106 [Polish] 运行完整测试套件
  - pytest tests/ --cov
  - 生成覆盖率报告

### 打包发布

- [ ] T107 [Polish] 配置setup.py完整信息
  - version, author, license
  - long_description from README
  - classifiers
- [ ] T108 [Polish] 测试安装流程
  - pip install -e .
  - 验证命令可用
- [ ] T109 [Polish] 准备PyPI发布（可选）
  - 创建.pypirc
  - python setup.py sdist bdist_wheel
  - twine upload dist/*

### 最终验证

- [ ] T110 [Polish] 在干净环境中测试
  - 创建新虚拟环境
  - 安装package
  - 运行示例命令
  - 验证输出正确
- [ ] T111 [Polish] 性能基准测试
  - 记录不同大小文件的处理时间
  - 记录内存使用情况
  - 生成性能报告 docs/performance.md

**Checkpoint**: 项目完成，可以交付

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 0 (Story 0: 数据准备)
    ↓
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) 🚨 BLOCKS ALL STORIES
    ↓
Phase 3 (Story 1: P0) ────┐
Phase 4 (Story 2: P0) ────┤ 可并行（如果有多人）
Phase 5 (Story 3: P1) ────┤ 或按优先级顺序执行
Phase 6 (Story 4: P1) ────┤
Phase 7 (Story 5: P2) ────┘
    ↓
Phase 8 (Polish)
```

### Critical Path (单人开发，按优先级)

1. **Week 0**: Phase 0 (数据准备) → 2天
2. **Week 1**: Phase 1-2 (Setup + Foundation) → 2天
3. **Week 1-2**: Phase 3 (Story 1) → 5天 ✅ MVP可用
4. **Week 2-3**: Phase 4 (Story 2) → 3天 ✅ MVP完整
5. **Week 3-4**: Phase 5 (Story 3) → 5天
6. **Week 4**: Phase 6 (Story 4) → 3天
7. **Week 5**: Phase 7 (Story 5) → 5天
8. **Week 5**: Phase 8 (Polish) → 2天

**Total**: ~5周

### Parallel Opportunities (如果有团队)

**After Foundation Complete**:
- Developer A: Story 1 (T038-T052)
- Developer B: Story 2 (T053-T063，等待Story 1的VocabularyAnalysis)
- Developer C: Story 3 (T064-T072)

**Highly Parallelizable Tasks**:
- 所有标记[P]的任务可并行（不同文件）
- 同一Story的单元测试可并行编写

---

## Task Statistics

### By Phase
- Phase 0 (数据准备): 16 tasks
- Phase 1 (Setup): 12 tasks
- Phase 2 (Foundational): 9 tasks 🚨
- Phase 3 (Story 1 - P0): 15 tasks ⭐ MVP核心
- Phase 4 (Story 2 - P0): 11 tasks ⭐ MVP完整
- Phase 5 (Story 3 - P1): 9 tasks
- Phase 6 (Story 4 - P1): 9 tasks
- Phase 7 (Story 5 - P2): 16 tasks
- Phase 8 (Polish): 14 tasks

**Total**: 111 tasks

### By Type
- Setup/Infrastructure: 21 tasks
- Implementation: 60 tasks
- Testing: 18 tasks
- Documentation: 7 tasks
- Optimization: 5 tasks

### Parallelizable Tasks
- Tasks marked [P]: 42 tasks (37.8%)
- Sequential dependencies: 69 tasks

---

## Execution Strategy

### 🚀 MVP First (Recommended)

**Goal**: 最快获得可用产品

1. ✅ Complete Phase 0 (数据准备)
2. ✅ Complete Phase 1 (Setup)
3. ✅ Complete Phase 2 (Foundation) - 必须完成
4. ✅ Complete Phase 3 (Story 1) - 核心功能
5. ✅ Complete Phase 4 (Story 2) - 完整输出
6. **STOP HERE** - 测试MVP
7. Demo给用户，收集反馈
8. 根据反馈决定是否继续Story 3-5

**MVP Timeline**: ~2周（Phase 0-4）

### 📈 Incremental Delivery

每完成一个Story就可以交付：
- Story 1完成 → 有基础词汇表JSON
- Story 2完成 → 有CLI和多格式输出 ✅ MVP
- Story 3完成 → 支持词组识别
- Story 4完成 → 支持中文释义
- Story 5完成 → 完整功能

### 👥 Team Parallel Strategy

如果有3个开发者：

**Week 1**: 一起完成Phase 0-2（数据+基础设施）
**Week 2**:
- Dev A → Story 1
- Dev B → Story 2（等待Story 1 API）
- Dev C → Story 3
**Week 3**: Integration + Testing
**Week 4-5**: Story 4-5 + Polish

---

## Notes

- ✅ = 已完成任务
- ⏳ = 进行中任务
- 🚨 = 阻塞任务（必须完成）
- ⭐ = MVP关键任务
- [P] = 可并行执行
- [Story] = 所属用户故事

### Best Practices

1. **测试驱动**: 单元测试和实现可以并行开发
2. **小步提交**: 每完成一个任务就commit
3. **独立验证**: 每个Story完成后独立测试
4. **性能监控**: 定期运行性能测试
5. **文档同步**: 代码变更时同步更新文档

### Risk Mitigation

- Phase 2 (Foundation) 是关键路径，优先完成
- spaCy模型加载慢，提前下载和测试
- 大文件处理可能超时，早期测试性能
- PDF提取可能失败，准备降级方案

---

**Tasks Version**: 1.0
**Created**: 2025-11-03
**Status**: Ready for execution
**Total Tasks**: 111
**Estimated Time**: 4-5周
