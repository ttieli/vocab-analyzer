# Feature Specification: Story 0 - 数据资源准备

**Feature Branch**: `story-0-data-preparation`
**Created**: 2025-11-03
**Status**: 🚀 执行中
**Input**: 准备英文书词汇等级分析工具所需的所有基础数据资源
**Decision Made**: 2025-11-03 - 接受快速决策建议

---

## 📌 最终决策记录

### 数据源选择
- ✅ **CEFR词汇表**: Oxford 3000 + CEFR-J (开源免费，合并达到5000+词)
- ✅ **词组词典**: phrasal-verbs-machine (GitHub开源项目)
- ✅ **中英词典**: ECDICT by skywind3000 (GitHub开源，180万词条)
- ✅ **样例书籍**: Project Gutenberg 公版书籍
- ✅ **雅思映射**: 参考British Council官方指南手动整理

### 数据格式标准
- ✅ **CSV**: 词汇表、词组表（UTF-8编码，逗号分隔）
- ✅ **JSON**: 映射表、元数据（格式化输出，便于阅读）

### 质量标准
- ✅ **词汇量**: 5000词是底线，争取8000+
- ✅ **释义详细度**: 使用ECDICT原有格式，保留主要释义
- ✅ **词组标注**: 先收集500个，separable字段可部分缺失，后续补充
- ✅ **数据验证**: 每个数据集随机抽样100条验证

### 版权合规
- ✅ 仅使用MIT/CC等开源许可或公版资源
- ✅ 在data/README.md中注明所有来源和许可
- ✅ 个人学习工具，暂不考虑商用

---

## User Scenarios & Testing

### User Story 1 - 获取CEFR分级词汇表 (Priority: P1)

作为开发者，我需要获取至少一份完整的CEFR分级词汇表（A1-C2），包含至少5000个单词及其等级标注，以便后续开发中能够准确匹配单词的难度等级。

**Why this priority**: 这是整个项目的核心数据依赖，没有词汇表就无法进行词汇等级匹配，是最基础且最关键的数据资源。

**Independent Test**:
- 下载并验证词汇表文件
- 检查是否包含必需字段：word, level, word_type
- 统计词汇总数是否≥5000
- 验证各等级（A1-C2）分布是否合理

**Acceptance Scenarios**:

1. **Given** 访问开源CEFR词汇表资源（如English Vocabulary Profile或Oxford 3000）
   **When** 下载并解析词汇表数据
   **Then** 获得至少5000个带有等级标注的单词，格式统一为CSV/JSON

2. **Given** 已下载的词汇表文件
   **When** 验证数据完整性
   **Then** 每个词条包含：单词原形、CEFR等级（A1-C2）、词性、可选的考试等级（KET/PET/FCE等）

3. **Given** 多个词汇表数据源
   **When** 需要选择或合并数据
   **Then** 优先选择剑桥官方EVP，其次考虑Oxford 3000/5000，确保数据权威性

---

### User Story 2 - 收集词组词典 (Priority: P2)

作为开发者，我需要收集至少500个常用英文词组（动词短语、搭配）的词典数据，包含词组的等级和是否可分离等信息，以便实现词组识别功能。

**Why this priority**: 词组识别是提升分析准确性的重要功能，虽然不是MVP必需，但对用户体验有显著提升。

**Independent Test**:
- 下载phrasal verbs和collocations数据
- 验证词组数量≥500
- 检查是否标注了可分离性（separable）
- 抽样验证词组的准确性

**Acceptance Scenarios**:

1. **Given** 访问开源词组资源（如phrasal-verbs-machine或Cambridge字典）
   **When** 下载词组数据
   **Then** 获得至少500个常用词组，包含：词组、类型、等级、是否可分离

2. **Given** 已收集的词组数据
   **When** 整理为统一格式
   **Then** 格式为CSV/JSON，字段包括：phrase, type, level, separable, definition

3. **Given** 词组词典数据
   **When** 验证可分离标注
   **Then** 像"look up"这样的可分离词组正确标记为separable: true

---

### User Story 3 - 准备中英词典数据 (Priority: P1)

作为开发者，我需要准备一份离线可用的中英词典数据，覆盖至少5000个常用词汇的中文释义，以便为用户提供单词的中文解释。

**Why this priority**: 中文释义是核心功能需求，用户明确表示需要中英文对照，属于MVP必备。

**Independent Test**:
- 下载并解析中英词典数据
- 验证覆盖常用5000词
- 检查释义质量和准确性
- 确认数据格式可被程序读取

**Acceptance Scenarios**:

1. **Given** 访问开源中英词典（如ECDICT或StarDict）
   **When** 下载词典数据
   **Then** 获得至少5000词的中英对照数据，包含：单词、词性、中文释义、可选音标

2. **Given** 已下载的词典文件
   **When** 转换为统一格式
   **Then** 格式为CSV/JSON，字段包括：word, word_type, definition_cn, phonetic

3. **Given** 词典数据质量检查
   **When** 抽样验证100个高频词
   **Then** 释义准确、简洁（1-3个主要含义），词性标注正确

---

### User Story 4 - 准备样例英文书籍 (Priority: P2)

作为开发者，我需要准备3-5本不同难度的英文书籍样本（TXT/PDF/DOCX格式），用于测试和验证词汇分析功能。

**Why this priority**: 测试数据很重要，但可以在开发过程中逐步补充，不是最紧急的准备任务。

**Independent Test**:
- 收集至少3本不同难度的英文书籍
- 确保文件格式可读（TXT/PDF纯文本/DOCX）
- 验证每本书的预期难度等级

**Acceptance Scenarios**:

1. **Given** 需要不同难度的测试样本
   **When** 收集公版或开源英文书籍
   **Then** 至少包含：初级（A2-B1）、中级（B1-B2）、高级（B2-C1）各一本

2. **Given** 已收集的书籍文件
   **When** 验证文件可读性
   **Then** TXT文件UTF-8编码，PDF为文字可选中类型，DOCX格式正常

3. **Given** 推荐书目清单
   **When** 选择具体书籍
   **Then** 优先选择：《The Little Prince》（初级）、《Animal Farm》（中级）、《Pride and Prejudice》（高级）

---

### User Story 5 - 整理雅思等级映射表 (Priority: P3)

作为开发者，我需要整理一份CEFR等级到雅思分数段的映射关系表，以便在输出中为用户提供参考性的雅思分数对应。

**Why this priority**: 这是锦上添花的功能，映射关系相对标准且数据量小，可以最后处理。

**Independent Test**:
- 整理CEFR↔IELTS映射关系
- 验证映射关系的合理性
- 创建JSON格式的映射表

**Acceptance Scenarios**:

1. **Given** 公开的CEFR和雅思对应资料
   **When** 整理映射关系
   **Then** 创建包含A1-C2到雅思分数段的映射表

2. **Given** 映射表数据
   **When** 验证合理性
   **Then** 映射关系符合主流认知（如B1对应4.5-5.5分，C1对应7.0-8.0分）

3. **Given** 映射表文件
   **When** 保存为JSON格式
   **Then** 格式为：{"A1": {"ielts_range": "2.0-3.0", ...}, ...}

---

### Edge Cases

- **数据源无法访问**: 如果首选数据源（如EVP）无法获取，需要备选方案（Oxford 3000）
- **数据格式不统一**: 不同来源的数据格式可能不同，需要编写转换脚本
- **数据质量问题**: 部分词汇表可能有错误或缺失，需要交叉验证
- **版权和授权**: 确保所有使用的数据都有合法的开源许可或公版授权
- **数据量不足**: 如果单一来源数据不足5000词，需要合并多个来源
- **中文释义缺失**: 部分生僻词可能没有中文释义，需要标记为待补充

---

## Requirements

### Functional Requirements

- **FR-001**: 系统必须获取至少一份包含5000+单词的CEFR分级词汇表
- **FR-002**: 词汇表必须包含字段：word（单词）, level（等级A1-C2）, word_type（词性）
- **FR-003**: 系统必须收集至少500个常用英文词组的数据
- **FR-004**: 词组数据必须包含字段：phrase（词组）, type（类型）, level（等级）, separable（是否可分离）
- **FR-005**: 系统必须准备中英词典数据，覆盖至少5000个常用词汇
- **FR-006**: 中英词典必须包含字段：word（单词）, word_type（词性）, definition_cn（中文释义）
- **FR-007**: 系统必须准备至少3本不同难度的英文书籍样本（TXT/PDF/DOCX）
- **FR-008**: 样例书籍必须涵盖初级（A2-B1）、中级（B1-B2）、高级（B2-C1）难度
- **FR-009**: 系统必须整理CEFR到雅思分数段的映射关系表（A1-C2）
- **FR-010**: 所有数据必须整理为统一的CSV或JSON格式，便于程序读取
- **FR-011**: 所有数据来源必须有明确的授权或开源许可证明
- **FR-012**: 必须编写数据说明文档，记录每个数据的来源、格式和使用方式

### Non-Functional Requirements

- **NFR-001**: 数据文件命名规范，使用小写字母和下划线（如cefr_wordlist.csv）
- **NFR-002**: CSV文件使用UTF-8编码，避免中文乱码
- **NFR-003**: JSON文件格式化输出，便于人工阅读和调试
- **NFR-004**: 数据组织结构清晰，按类型分目录存放（vocabularies/phrases/dictionaries等）
- **NFR-005**: 所有数据文件应包含元数据注释（来源、日期、版本）

### Key Entities

- **CEFR词汇表** (Vocabulary Wordlist)
  - 属性：word, level, word_type, exam, definition
  - 用途：核心的单词等级匹配数据库
  - 数量：5000+词条

- **词组词典** (Phrasal Dictionary)
  - 属性：phrase, type, level, separable, definition
  - 用途：识别和标注英文词组
  - 数量：500+词组

- **中英词典** (EN-CN Dictionary)
  - 属性：word, word_type, definition_cn, phonetic
  - 用途：提供中文释义
  - 数量：5000+词条

- **样例书籍** (Sample Books)
  - 属性：文件名、格式、难度等级、字数
  - 用途：测试和验证系统功能
  - 数量：3-5本

- **等级映射表** (Level Mapping)
  - 属性：cefr_level, ielts_range, description
  - 用途：提供雅思分数参考
  - 数量：7个等级（A1-C2+）

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: 成功获取至少一份包含5000+词条的CEFR词汇表，数据完整且格式统一
- **SC-002**: 收集至少500个常用词组数据，至少80%标注了可分离属性
- **SC-003**: 准备的中英词典覆盖常用5000词，抽样验证准确率>95%
- **SC-004**: 收集至少3本不同难度的样例书籍，文件格式正确可读
- **SC-005**: 创建完整的CEFR↔IELTS映射表（7个等级）
- **SC-006**: 所有数据文件格式统一为CSV/JSON，且能被Python程序成功解析
- **SC-007**: 编写完整的数据说明文档（data/README.md），记录所有数据来源和使用方式
- **SC-008**: 所有数据文件组织在规范的目录结构中（data/vocabularies, data/phrases等）
- **SC-009**: 所有数据来源都有明确的开源许可或公版声明
- **SC-010**: 数据准备工作在2天内完成，为后续开发扫清障碍

---

## Data Organization Structure

建议的数据目录结构：

```
data/
├── README.md                        # 数据说明文档
├── vocabularies/                     # 词汇表目录
│   ├── cefr_wordlist.csv            # 主CEFR词汇表
│   ├── oxford_3000.csv              # Oxford核心词汇（可选）
│   └── academic_wordlist.csv        # 学术词汇（可选）
├── phrases/                          # 词组目录
│   ├── phrasal_verbs.csv            # 动词短语
│   └── collocations.csv             # 常见搭配（可选）
├── dictionaries/                     # 词典目录
│   ├── en_cn_dict.csv               # 中英词典
│   └── stardict/                    # StarDict格式词典（可选）
├── sample_books/                     # 样例书籍目录
│   ├── little_prince.txt            # 小王子（初级）
│   ├── animal_farm.txt              # 动物农场（中级）
│   ├── pride_and_prejudice.txt      # 傲慢与偏见（高级）
│   └── books_metadata.json          # 书籍元数据
└── mappings/                         # 映射关系目录
    └── cefr_ielts_mapping.json      # CEFR↔IELTS映射
```

---

## Implementation Notes

### Recommended Data Sources

1. **CEFR词汇表**:
   - 首选：English Vocabulary Profile (EVP) - 剑桥官方数据
   - 备选：Oxford 3000/5000 Word List
   - 开源项目：CEFR-J Wordlist

2. **词组词典**:
   - GitHub: phrasal-verbs-machine
   - EnglishClub Phrasal Verbs List
   - 手动整理常用500个

3. **中英词典**:
   - ECDICT (skywind3000/ECDICT on GitHub) - 推荐
   - StarDict词典
   - 有道词典API（在线方案）

4. **样例书籍**:
   - Project Gutenberg（公版书籍）
   - Standard Ebooks（高质量排版）
   - 确保版权合规

### Data Conversion Scripts

建议编写简单的Python脚本用于：
- 将不同格式的词汇表转换为统一的CSV格式
- 合并多个词汇表数据源
- 验证数据完整性和格式
- 生成数据统计报告

---

## Risks & Mitigation

### Risks

1. **数据源不可用**: EVP等官方资源可能需要注册或付费
2. **数据质量问题**: 开源数据可能有错误或不完整
3. **版权风险**: 某些词汇表可能有使用限制
4. **时间超期**: 数据搜集和整理可能比预期耗时

### Mitigation

1. 准备多个备选数据源
2. 交叉验证多个来源的数据
3. 使用明确开源许可的数据
4. 优先处理P1数据，P3可后补

---

## Checklist

**准备工作**:
- [ ] 创建data/目录结构
- [ ] 安装必要的数据处理工具（pandas等）

**数据收集**:
- [ ] 获取CEFR词汇表（5000+词）
- [ ] 收集词组词典（500+词组）
- [ ] 准备中英词典（5000+词）
- [ ] 下载样例书籍（3-5本）
- [ ] 整理雅思映射表

**数据处理**:
- [ ] 转换所有数据为CSV/JSON格式
- [ ] 统一字段命名和数据格式
- [ ] 验证数据完整性和准确性
- [ ] 组织数据到规范目录结构

**文档编写**:
- [ ] 编写data/README.md说明文档
- [ ] 记录每个数据的来源和许可
- [ ] 编写数据使用示例
- [ ] 记录数据统计信息（词数、覆盖率等）

**验收**:
- [ ] 通过所有验收标准测试
- [ ] 数据能被Python程序成功读取
- [ ] 数据质量抽样检查通过
- [ ] 版权和授权问题已解决

---

**Status**: ⏳ 待开始
**Estimated Time**: 1-2天
**Next Action**: 开始搜集CEFR词汇表数据（P1优先级）
