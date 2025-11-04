# Feature Specification: Bilingual UI with CEFR Descriptions and Local Translation

**Feature Branch**: `002-bilingual-ui-translation`
**Created**: 2025-11-04
**Status**: Draft
**Input**: User description: "1）页面改为双语版本 2）增加分词级别介绍 A1是什么 A2是什么 3）增加本地的英文翻译功能，可以翻译没有翻译的词组和摘抄出来的例句 4)还是本地应用,无需联网使用"

## User Scenarios & Testing

### User Story 1 - Bilingual Interface Navigation (Priority: P1)

Chinese-speaking users who are learning English need to navigate the vocabulary analyzer interface comfortably. They want to see all interface text in both English and Chinese so they can understand the application while also learning English terminology.

**Why this priority**: Core accessibility feature that makes the application usable for the primary target audience (Chinese learners of English). Without this, users struggle with navigation and feature discovery.

**Independent Test**: Can be fully tested by navigating through all pages and verifying every UI element (buttons, labels, headings, instructions) displays both English and Chinese text. Delivers immediate value by making the interface accessible to Chinese speakers.

**Acceptance Scenarios**:

1. **Given** a user opens the web interface, **When** they view the homepage, **Then** they see the title "Vocabulary Analyzer / 词汇分析器" and all navigation elements in both languages
2. **Given** a user is on the upload page, **When** they view the file upload area, **Then** they see instructions like "Choose a file... / 选择文件..." and format descriptions in both languages
3. **Given** a user views the results page, **When** they read section headings, **Then** they see headings like "Statistics / 统计数据" and "CEFR Distribution / CEFR级别分布"
4. **Given** a user encounters an error message, **When** the error is displayed, **Then** they see the error description in both English and Chinese

---

### User Story 2 - CEFR Level Education (Priority: P2)

Users who are new to CEFR levels need to understand what each level (A1, A2, B1, B2, C1, C2, C2+) means. They want to see clear descriptions of each level's characteristics and difficulty so they can interpret their vocabulary analysis results meaningfully.

**Why this priority**: Essential for users to understand their analysis results, but not blocking basic functionality. Users can still use the app without this knowledge, though they won't fully understand what the levels mean.

**Independent Test**: Can be tested by clicking on any CEFR level indicator and verifying a popup or tooltip displays comprehensive information about that level including typical learner characteristics, vocabulary range, and example contexts. Delivers value by educating users about the CEFR framework.

**Acceptance Scenarios**:

1. **Given** a user views the results page, **When** they hover over or click a CEFR level badge (e.g., "B2"), **Then** they see a description explaining that B2 is "Upper Intermediate / 中高级" with details about typical learner abilities
2. **Given** a user views the CEFR distribution chart, **When** they click on a level bar, **Then** they see an information panel showing the level's description in both English and Chinese
3. **Given** a user is viewing word details, **When** they see the word's CEFR level, **Then** they can access a "?" icon or link to learn what that level means
4. **Given** a user accesses CEFR information, **When** they read the description, **Then** they see bilingual content explaining proficiency levels, typical vocabulary size, and learning context

---

### User Story 3 - Local Translation of Untranslated Content (Priority: P1)

Users frequently encounter words, phrases, or example sentences that don't have Chinese translations in the current vocabulary database. They need to translate these items on-demand without leaving the application or requiring internet connectivity, ensuring they can fully understand all vocabulary items even when offline.

**Why this priority**: Critical for complete user experience. Without translations, users cannot understand unfamiliar vocabulary, defeating the purpose of the learning tool. Must work offline to maintain the local-first approach.

**Independent Test**: Can be tested by identifying words/phrases without Chinese translations, clicking a "Translate" button, and verifying the translation appears instantly without network requests. Delivers immediate value by providing translations for all vocabulary items.

**Acceptance Scenarios**:

1. **Given** a user views a word detail modal without a Chinese translation, **When** they click a "Translate / 翻译" button, **Then** the system generates a Chinese translation using a local translation model and displays it immediately
2. **Given** a user views an example sentence without translation, **When** they click "Translate this sentence / 翻译此句", **Then** the sentence is translated to Chinese and displayed below the original
3. **Given** a user is offline with no internet connection, **When** they request translation of untranslated content, **Then** the local translation system provides the translation without errors or delays
4. **Given** a user translates content, **When** the translation is generated, **Then** the system caches it locally so subsequent views show the translation without re-translation
5. **Given** a user views a phrasal verb without translation, **When** they click translate, **Then** the system provides both the literal translation and the idiomatic meaning in Chinese

---

### Edge Cases

- What happens when the local translation model encounters extremely rare or technical vocabulary not in its training data?
- How does the system handle translation requests for sentences longer than the model's maximum token limit?
- What happens if the user's system lacks sufficient memory to load the translation model?
- How does the bilingual UI handle text overflow when Chinese text is significantly longer than English text in constrained layouts?
- What happens when CEFR level descriptions are accessed repeatedly in quick succession?

## Requirements

### Functional Requirements

#### Bilingual UI Requirements

- **FR-001**: System MUST display all user interface text (buttons, labels, headings, instructions, error messages) in both English and Chinese
- **FR-002**: System MUST maintain consistent bilingual formatting throughout the application using the pattern "English / 中文"
- **FR-003**: System MUST ensure both language versions are equally visible and readable without requiring user interaction to switch languages
- **FR-004**: System MUST provide bilingual text for all new UI elements including modal dialogs, tooltips, and notifications

#### CEFR Level Description Requirements

- **FR-005**: System MUST provide detailed descriptions for all CEFR levels (A1, A2, B1, B2, C1, C2, C2+) in both English and Chinese
- **FR-006**: System MUST display CEFR descriptions including: proficiency level name, typical learner characteristics, approximate vocabulary size, and usage contexts
- **FR-007**: System MUST make CEFR descriptions accessible through interactive elements (hover, click, or icon) adjacent to level indicators
- **FR-008**: System MUST include examples of typical vocabulary or sentence complexity for each CEFR level

#### Local Translation Requirements

- **FR-009**: System MUST provide on-demand translation for words without Chinese translations using a local translation model
- **FR-010**: System MUST provide on-demand translation for phrasal verbs without Chinese translations
- **FR-011**: System MUST provide on-demand translation for example sentences without Chinese translations
- **FR-012**: System MUST operate entirely offline without requiring internet connectivity for translation functionality
- **FR-013**: System MUST use a lightweight, efficient local translation model that can run on typical user hardware
- **FR-014**: System MUST cache all user-generated translations locally to avoid redundant translation requests
- **FR-015**: System MUST provide visual indicators (e.g., "Translate" button) for untranslated content in word detail modals
- **FR-016**: System MUST handle translation errors gracefully by displaying error messages in both languages
- **FR-017**: System MUST complete translation requests within 3 seconds for typical vocabulary items

### Key Entities

- **Translation Cache**: Stores user-generated translations mapped to original English text to avoid redundant translation operations
  - Attributes: source_text, target_text (Chinese), timestamp, translation_type (word/phrase/sentence)
  - Persistence: Local storage or application database

- **CEFR Level Definition**: Contains bilingual descriptions and metadata for each CEFR level
  - Attributes: level_code (A1-C2+), name_en, name_cn, description_en, description_cn, typical_vocabulary_size, example_contexts
  - Persistence: Static data file or embedded resource

- **Translation Request**: Represents a single translation operation
  - Attributes: source_text, translation_type, user_context (word detail, phrase list, example sentence)
  - Lifecycle: Created on-demand, processed immediately, result cached

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can navigate the entire application and understand all interface elements without language barriers (100% of UI text bilingual)
- **SC-002**: Users can access CEFR level descriptions within 1 click/hover from any level indicator
- **SC-003**: Users can translate any untranslated vocabulary item (word, phrase, or sentence) within 3 seconds without internet connection
- **SC-004**: Translation feature has 95%+ success rate for common English vocabulary items (A1-C1 levels)
- **SC-005**: Application remains fully functional in offline mode with no degradation in translation capabilities
- **SC-006**: Users report improved understanding of CEFR levels (measured by post-feature survey or reduced support questions)
- **SC-007**: Bilingual UI increases task completion rate by Chinese-speaking users by at least 30% compared to English-only interface

## Assumptions

- Users have sufficient local storage (at least 500MB) for the local translation model
- Users' systems meet minimum hardware requirements to run machine learning models (at least 4GB RAM)
- The local translation model focuses on general English-to-Chinese translation, not domain-specific technical translations
- CEFR level descriptions are static content that doesn't require dynamic updates or user customization
- Users prefer seeing both languages simultaneously rather than a language toggle switch
- The existing vocabulary database already has Chinese translations for the majority of common words; local translation is primarily for gaps
- Translation quality from local model is acceptable at approximately 80-90% accuracy for educational purposes (doesn't need to be perfect)

## Dependencies

- Local machine translation model (e.g., lightweight Hugging Face model, OPUS-MT, or similar) that can run offline
- CEFR level description content in bilingual format
- Existing vocabulary analyzer web interface (from Feature 001)
- Local caching mechanism for storing user-generated translations

## Out of Scope

- User-selectable language preferences (always show both languages)
- Translation of user-uploaded book content (only translates vocabulary items and UI text)
- Professional-grade translation quality (educational-quality is sufficient)
- Translation between languages other than English and Chinese
- Voice or audio translation features
- Real-time translation as users type
- User editing or correction of translations
- Export of translations to external formats
- Integration with online translation services (must remain fully offline)
