# 用户故事 0：数据资源准备

**优先级**: P0（准备阶段，最先执行）

## 整体业务需求
将英文书籍转换为分级单词表，帮助用户根据自己的英语水平（A1-C2）有针对性地背单词。

## 本次业务需求
在开发前准备所有必需的基础数据资源：包括CEFR分级词汇表、词组词典、中英对照词典，以及用于测试的样例英文书籍。确保数据来源可靠、格式统一、覆盖面广。

## 期望成果
- 获取剑桥CEFR词汇表（A1-C2，至少5000词）
- 收集词组词典（至少500个常用动词短语）
- 准备中英词典数据（支持离线查询）
- 准备3-5本样例英文书籍（TXT/PDF/DOCX格式）
- 整理雅思等级映射关系表
- 所有数据整理为统一的CSV/JSON格式

---

## 数据清单

### 1. 剑桥CEFR分级词汇表

**来源选项**：
- [ ] English Vocabulary Profile (EVP) - 剑桥官方
- [ ] CEFR-J Wordlist - 日本版CEFR扩展
- [ ] Oxford 3000/5000 - 牛津核心词汇
- [ ] Academic Word List (AWL) - 学术词汇

**所需字段**：
```
word, level, word_type, exam, definition
```

### 2. 词组词典

**来源选项**：
- [ ] Cambridge Phrasal Verbs Dictionary
- [ ] 开源项目：phrasal-verbs-machine
- [ ] EnglishClub Phrasal Verbs List

**所需字段**：
```
phrase, type, level, separable, definition
```

### 3. 中英词典

**方案选择**：
- [ ] StarDict开源词典（离线）
- [ ] ECDICT开源词典
- [ ] 自建核心词汇对照表（5000-10000词）

**所需字段**：
```
word, word_type, definition_cn, phonetic
```

### 4. 样例英文书籍

**推荐书目**（不同难度）：
- [ ] 初级：《The Little Prince》（小王子）- A2-B1
- [ ] 中级：《Animal Farm》（动物农场）- B1-B2
- [ ] 高级：《Pride and Prejudice》（傲慢与偏见）- B2-C1
- [ ] 学术：《Brief History of Time》（时间简史）- C1-C2
- [ ] 现代：《The Hunger Games》（饥饿游戏）- B1-B2

**文件格式**：TXT、PDF（纯文本）、DOCX

### 5. 雅思等级映射表

**映射关系**（需验证）：
```
A1: IELTS 2.0-3.0
A2: IELTS 3.0-4.0
B1: IELTS 4.5-5.5
B2: IELTS 6.0-6.5
C1: IELTS 7.0-8.0
C2: IELTS 8.5-9.0
```

---

## 数据组织结构

建议创建以下目录：
```
data/
├── vocabularies/
│   ├── cefr_wordlist.csv
│   ├── oxford_3000.csv
│   └── academic_wordlist.csv
├── phrases/
│   ├── phrasal_verbs.csv
│   └── collocations.csv
├── dictionaries/
│   ├── en_cn_dict.csv
│   └── stardict/
├── sample_books/
│   ├── little_prince.txt
│   ├── animal_farm.pdf
│   └── pride_and_prejudice.docx
└── mappings/
    └── cefr_ielts_mapping.json
```

---

## 验收标准

- [ ] 至少获取一个完整的CEFR分级词汇表（>5000词）
- [ ] 词组词典包含至少500个常用短语
- [ ] 中英词典能覆盖常用5000词
- [ ] 准备至少3本不同难度的样例书籍
- [ ] 所有数据文件格式统一且可被程序读取
- [ ] 数据来源有明确的授权或开源许可
- [ ] 编写数据说明文档（来源、格式、使用方式）

---

**状态**: 待准备
**预计时间**: 1-2天（数据搜集和整理）
