# 数据资源说明文档

**项目**: 英文书词汇等级分析工具
**创建日期**: 2025-11-03
**版本**: 1.0
**状态**: 数据源调研完成，待下载和整理

---

## 📋 数据概览

本目录包含英文书词汇等级分析工具所需的所有基础数据资源，包括CEFR分级词汇表、词组词典、中英词典、样例书籍和等级映射表。

### 目录结构

```
data/
├── README.md                        # 本说明文档
├── vocabularies/                     # 词汇表目录
│   ├── [待下载] cefr_wordlist.csv   # 主CEFR词汇表
│   └── [待下载] oxford_3000.csv     # Oxford 3000词汇
├── phrases/                          # 词组目录
│   └── [待下载] phrasal_verbs.csv   # 动词短语词典
├── dictionaries/                     # 词典目录
│   └── [待下载] ecdict_core.csv     # ECDICT核心词汇
├── sample_books/                     # 样例书籍目录
│   └── [待下载] 样例书籍文件
└── mappings/                         # 映射关系目录
    └── ✅ cefr_ielts_mapping.json   # CEFR↔IELTS映射表
```

---

## 🎯 数据源调研结果

### 1. CEFR分级词汇表

#### 推荐数据源

**选项A: ECDICT (推荐) ⭐**
- **仓库**: https://github.com/skywind3000/ECDICT
- **内容**: 340万英文词条，包含中英释义、词性、音标、词频、考试标签（包含Oxford 3000标记）
- **格式**: CSV (UTF-8编码)
- **许可证**: MIT License
- **字段**:
  - word (单词)
  - phonetic (音标)
  - definition (英文释义)
  - translation (中文释义)
  - pos (词性)
  - collins (柯林斯星级)
  - oxford (是否Oxford 3000)
  - tag (考试标签：CET4/CET6/TOEFL等)
  - bnc (英国国家语料库词频)
  - frq (当代语料库词频)

**优势**:
- ✅ 同时解决词汇表和中英词典两个需求
- ✅ 数据量大，覆盖全面
- ✅ MIT许可证，完全开源
- ✅ 包含Oxford 3000标记

**下载方式**:
```bash
# 方式1: 克隆仓库
git clone https://github.com/skywind3000/ECDICT.git

# 方式2: 下载Release版本
# 访问 https://github.com/skywind3000/ECDICT/releases
```

---

**选项B: winterdl/oxford-5000-vocabulary**
- **仓库**: https://github.com/winterdl/oxford-5000-vocabulary-audio-definition
- **内容**: Oxford 3000/5000词汇，含音频、释义、例句
- **格式**: CSV, JSON
- **许可证**: 未明确标注
- **优势**: 数据结构化好，包含音频链接
- **劣势**: 许可证不明确

---

**选项C: Kolia951/The_Oxford_3000_CEFR**
- **仓库**: https://github.com/Kolia951/The_Oxford_3000_CEFR
- **内容**: Oxford 3000词汇，按CEFR等级分组
- **格式**: JSON
- **许可证**: Unlicense (公共域)
- **优势**: 完全开放，按等级分类
- **劣势**: 只包含词汇列表，无释义和词性信息；只覆盖A1-B2

---

### 2. 词组词典 (Phrasal Verbs)

#### 调研结果

找到的资源主要有：

**选项A: Semigradsky/phrasal-verbs**
- **仓库**: https://github.com/Semigradsky/phrasal-verbs
- **内容**: ~100个常用phrasal verbs
- **格式**: JSON
- **特点**: 包含separable标注（用+标记）
- **劣势**: 数量不足500个

**选项B: PDF/XLS资源**
- **来源**: engxam.com, Scribd等
- **内容**: 300-550个phrasal verbs
- **格式**: PDF, XLS (需转换为CSV)
- **劣势**: 需要手动处理，版权可能不明确

**建议方案**:
1. 先使用Semigradsky的100个高质量数据
2. 补充从教育网站收集的常用phrasal verbs
3. Separable标注可以在使用过程中逐步补充

---

### 3. 中英词典

**推荐方案**: 使用ECDICT（见上方"选项A"）

ECDICT已经包含完整的中英对照数据，无需单独下载其他中英词典。

---

### 4. 样例英文书籍

#### 推荐来源: Project Gutenberg

**网站**: https://www.gutenberg.org/

**推荐书目**:

| 难度 | 书名 | CEFR等级 | Project Gutenberg ID |
|------|------|---------|---------------------|
| 初级 | The Little Prince（小王子） | A2-B1 | 待查找 |
| 中级 | Animal Farm（动物农场） | B1-B2 | #7 (George Orwell) |
| 高级 | Pride and Prejudice（傲慢与偏见） | B2-C1 | #1342 (Jane Austen) |
| 高级 | Alice's Adventures in Wonderland（爱丽丝） | B1-B2 | #11 (Lewis Carroll) |

**下载方式**:
```bash
# 示例：下载傲慢与偏见
wget https://www.gutenberg.org/files/1342/1342-0.txt -O pride_and_prejudice.txt
```

**许可证**: Public Domain（公版，无版权限制）

---

### 5. CEFR-IELTS映射表

**状态**: ✅ 已创建

**文件**: `data/mappings/cefr_ielts_mapping.json`

**来源**: 基于British Council和Cambridge Assessment官方指南整理

**内容**:
- A1-C2的CEFR等级
- 对应的IELTS分数区间
- 考试对应关系（KET/PET/FCE/CAE/CPE）
- 词汇量估算

---

## 📥 数据下载清单

### 立即可用
- [x] ✅ CEFR-IELTS映射表 (`mappings/cefr_ielts_mapping.json`)

### 待下载
- [ ] ECDICT词典数据 (340万词条，~200MB)
- [ ] Phrasal Verbs数据 (至少100个)
- [ ] 样例书籍：Pride and Prejudice (TXT)
- [ ] 样例书籍：Animal Farm (TXT)
- [ ] 样例书籍：Alice in Wonderland (TXT)

---

## 🔧 数据处理计划

### Phase 1: 下载核心数据
1. 克隆ECDICT仓库或下载CSV文件
2. 从Project Gutenberg下载3本样例书籍
3. 下载phrasal verbs JSON文件

### Phase 2: 数据转换与整理
1. **ECDICT处理**:
   - 筛选出Oxford 3000标记的词汇
   - 根据词频和考试标签分配CEFR等级
   - 提取核心字段：word, level, pos, translation, phonetic
   - 导出为 `vocabularies/cefr_wordlist.csv`

2. **Phrasal Verbs处理**:
   - 合并多个来源的phrasal verbs数据
   - 统一格式：phrase, type, level, separable, definition
   - 导出为 `phrases/phrasal_verbs.csv`

3. **样例书籍处理**:
   - 验证编码为UTF-8
   - 清理格式，保留纯文本
   - 重命名为规范文件名

### Phase 3: 数据验证
1. 统计词汇量是否达到5000+
2. 随机抽样100条验证准确性
3. 检查数据完整性和格式正确性

---

## 📊 预期数据规模

| 数据类型 | 目标数量 | 实际数量 | 状态 |
|---------|---------|---------|------|
| CEFR词汇表 | 5000+ | ECDICT有340万 | ⏳ 待下载 |
| Phrasal Verbs | 500+ | 初步100+ | ⏳ 待补充 |
| 中英释义 | 5000+ | ECDICT覆盖 | ⏳ 待下载 |
| 样例书籍 | 3-5本 | 0本 | ⏳ 待下载 |
| 映射表 | 1份 | 1份 | ✅ 已完成 |

---

## 📜 版权和许可说明

### 已确认开源许可的数据
- ✅ **ECDICT**: MIT License - 可自由使用、修改、分发
- ✅ **Project Gutenberg书籍**: Public Domain - 公版，无版权限制
- ✅ **CEFR-IELTS映射表**: 自行整理，基于公开资料

### 许可证待确认的数据
- ⚠️ **winterdl/oxford-5000**: 许可证未标注，建议联系作者
- ⚠️ **Semigradsky/phrasal-verbs**: 许可证未标注

### 使用建议
- ✅ 本项目为个人学习工具，符合Fair Use
- ✅ 优先使用MIT或Public Domain资源
- ✅ 在README中注明所有数据来源
- ⚠️ 如需商用，请重新评估许可证

---

## 🚀 下一步行动

1. **下载ECDICT** (优先级：P0)
   ```bash
   git clone https://github.com/skywind3000/ECDICT.git
   cd ECDICT
   # 查看文件大小和格式
   ls -lh *.csv
   ```

2. **下载样例书籍** (优先级：P1)
   - 从Project Gutenberg下载3本不同难度的书籍
   - 转换为UTF-8 TXT格式

3. **收集Phrasal Verbs** (优先级：P2)
   - 下载Semigradsky仓库数据
   - 补充常用短语至500+

4. **数据转换脚本** (优先级：P1)
   - 编写Python脚本筛选和转换ECDICT数据
   - 生成符合项目需求的CSV格式

---

## 📞 联系与支持

如有数据相关问题，请查阅：
- ECDICT Issues: https://github.com/skywind3000/ECDICT/issues
- Project Gutenberg Help: https://www.gutenberg.org/help/

---

**文档维护者**: 开发团队
**最后更新**: 2025-11-03
**下次更新**: 数据下载完成后
