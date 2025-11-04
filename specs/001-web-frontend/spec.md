# Feature Specification: Web Frontend for Vocabulary Analyzer

**Feature Branch**: `001-web-frontend`
**Created**: 2025-11-04
**Status**: Draft
**Input**: User description: "1）增加前端web端 2）简单上传分析，分析后的格式可展示可下载 3）当前支持单本书分析即可 4）显示分析进度和阶段 4）简单快速可实现"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Simple File Upload and Analysis (Priority: P1)

A user visits the web interface, uploads a single book file (TXT, PDF, or DOCX), and receives a vocabulary analysis report that can be viewed in the browser and downloaded in multiple formats.

**Why this priority**: This is the core functionality that delivers immediate value to users who want to analyze books without installing CLI tools or knowing command-line operations. It makes the existing analyzer accessible to non-technical users.

**Independent Test**: Can be fully tested by uploading a sample book file and verifying that the analysis completes successfully with downloadable results. Delivers standalone value as a complete analysis workflow.

**Acceptance Scenarios**:

1. **Given** a user is on the upload page, **When** they select a valid book file (TXT, PDF, or DOCX) and click "Analyze", **Then** the system begins processing the file and displays a progress indicator
2. **Given** a file is being analyzed, **When** the analysis completes successfully, **Then** the system displays the vocabulary results with CEFR level distribution, statistics, and word lists
3. **Given** analysis results are displayed, **When** the user clicks a download button, **Then** the system provides the analysis in the selected format (JSON, CSV, or Markdown)
4. **Given** a user uploads an invalid file type, **When** they attempt to analyze it, **Then** the system displays a clear error message indicating supported file types

---

### User Story 2 - Real-time Progress Tracking (Priority: P2)

During analysis, users see detailed progress updates showing which stage of processing is currently running (extraction, tokenization, phrase detection, level matching, statistics generation).

**Why this priority**: Enhances user experience by providing transparency into what's happening during longer analysis operations. Helps users understand that the system is actively working, especially for larger books that may take 30-60 seconds to process.

**Independent Test**: Can be tested independently by uploading a medium-sized book and observing that progress indicators update correctly through each processing stage. Adds value even if other features are incomplete.

**Acceptance Scenarios**:

1. **Given** a file analysis is in progress, **When** the system moves between processing stages, **Then** the progress indicator updates to show the current stage name and percentage complete
2. **Given** a large book is being analyzed, **When** processing time exceeds 10 seconds, **Then** the system may display estimated time remaining (best-effort calculation based on current progress rate)
3. **Given** an error occurs during any processing stage, **When** the system detects the failure, **Then** the progress indicator shows which stage failed and displays a helpful error message

---

### User Story 3 - Interactive Results Visualization (Priority: P3)

After analysis completes, users can interact with the results by filtering words by CEFR level, searching for specific words, and viewing detailed information including Chinese translations and example usage.

**Why this priority**: Adds significant value for learning purposes but is not essential for the basic analysis workflow. Users can still download results and view them externally if this feature is not yet available.

**Independent Test**: Can be tested independently by completing an analysis and verifying that filtering, searching, and detail views work correctly. Enhances the existing analysis results without requiring changes to core processing.

**Acceptance Scenarios**:

1. **Given** analysis results are displayed, **When** a user clicks on a CEFR level filter, **Then** the word list updates to show only words from that level
2. **Given** results contain Chinese translations, **When** a user hovers over or clicks a word, **Then** the system displays the Chinese translation and additional metadata
3. **Given** a user wants to find specific words, **When** they type in a search box, **Then** the results filter in real-time to match the search query

---

### Edge Cases

- What happens when a user uploads a corrupted or unreadable file?
- How does the system handle extremely large books (500+ pages) that may take several minutes to process?
- What happens if a user closes the browser window during analysis? (Handled by: sessions expire after 1 hour, temporary files are automatically cleaned up, analysis continues in background until completion or timeout)
- How does the system respond if the uploaded file contains no recognizable English text?
- What happens when multiple users upload files simultaneously?
- How does the system handle network interruptions during file upload or result download?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept file uploads of TXT, PDF, and DOCX formats up to 50MB in size
- **FR-002**: System MUST validate uploaded files and reject unsupported file types with clear error messages
- **FR-003**: System MUST invoke the existing VocabularyAnalyzer core engine to process uploaded files
- **FR-004**: System MUST display real-time progress updates during analysis, showing current processing stage and percentage complete
- **FR-005**: System MUST present analysis results in a web-friendly format showing CEFR level distribution, statistics, and word lists
- **FR-006**: System MUST provide download options for results in JSON, CSV, and Markdown formats
- **FR-007**: System MUST handle one book analysis at a time per user session
- **FR-008**: System MUST complete analysis of typical books (100-200 pages) within 60 seconds
- **FR-009**: System MUST display Chinese translations for words when available from the ECDICT dictionary
- **FR-010**: System MUST show all detected phrasal verbs separately from individual words in results
- **FR-011**: System MUST persist uploaded files temporarily during analysis and clean them up after completion or error
- **FR-012**: System MUST provide clear feedback for all user actions (upload, analyze, download)
- **FR-013**: System MUST be responsive and usable on desktop browsers (Chrome, Firefox, Safari, Edge)

### Key Entities *(include if feature involves data)*

- **UploadedFile**: Represents a book file uploaded by the user; includes filename, file type, size, upload timestamp, and processing status
- **AnalysisSession** (implemented as **UploadSession** in code): Represents a single analysis operation; includes session ID, current processing stage, progress percentage, start time, and result data
- **AnalysisResult**: Contains the complete vocabulary analysis output; includes word lists organized by CEFR level, phrasal verbs, statistics, and metadata (aligned with existing VocabularyAnalysis model)
- **ProcessingStage**: Represents a stage in the analysis pipeline; includes stage name (extraction, tokenization, phrase detection, level matching, statistics), status (pending, in-progress, completed, failed), and progress percentage

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can upload a book file and complete analysis in under 3 clicks from landing page
- **SC-002**: System processes 100-page books in under 60 seconds with visible progress updates
- **SC-003**: Users can view analysis results and download them in their preferred format within 5 seconds of analysis completion
- **SC-004**: 90% of users successfully complete their first analysis without encountering errors
- **SC-005**: System handles concurrent uploads from multiple users without performance degradation or errors
- **SC-006**: Progress indicators update at least every 2 seconds during analysis, providing clear feedback on processing status
- **SC-007**: Downloaded files are formatted correctly and match the quality of current CLI output
- **SC-008**: Users can access the web interface from any modern desktop browser without installation or configuration
