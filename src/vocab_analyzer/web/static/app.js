// Vocabulary Analyzer Web Interface - Main JavaScript

let currentSessionId = null;
let analysisResults = null;  // Store full analysis results
let currentFilter = 'all';  // Current CEFR level filter
let searchTerm = '';  // Current search term

// Initialize bilingual UI on page load
document.addEventListener('DOMContentLoaded', () => {
    if (typeof initBilingualUI === 'function') {
        initBilingualUI();
    }

    // Hide translation tooltip when clicking outside
    document.addEventListener('click', (e) => {
        const tooltip = document.getElementById('translation-tooltip');
        if (tooltip && !tooltip.contains(e.target) && !e.target.classList.contains('translate-btn')) {
            if (typeof hideTranslationResult === 'function') {
                hideTranslationResult();
            }
        }
    });
});

// DOM Elements
const uploadSection = document.getElementById('upload-section');
const progressSection = document.getElementById('progress-section');
const resultsSection = document.getElementById('results-section');
const errorSection = document.getElementById('error-section');

const uploadForm = document.getElementById('upload-form');
const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');

// Text input elements
const textForm = document.getElementById('text-form');
const textInput = document.getElementById('text-input');
const charCount = document.getElementById('char-count');
const fileModeBtn = document.getElementById('file-mode-btn');
const textModeBtn = document.getElementById('text-mode-btn');

const progressFill = document.getElementById('progress-fill');
const progressStage = document.getElementById('progress-stage');
const progressPercent = document.getElementById('progress-percent');

const downloadJsonBtn = document.getElementById('download-json');
const downloadCsvBtn = document.getElementById('download-csv');
const downloadMarkdownBtn = document.getElementById('download-markdown');
const analyzeAnotherBtn = document.getElementById('analyze-another');

const errorText = document.getElementById('error-text');
const tryAgainBtn = document.getElementById('try-again');

// Interactive results elements
const wordSearch = document.getElementById('word-search');
const levelFilters = document.getElementById('level-filters');
const wordList = document.getElementById('word-list');
const phraseList = document.getElementById('phrase-list');
const wordCount = document.getElementById('word-count');
const phraseCount = document.getElementById('phrase-count');
const wordModal = document.getElementById('word-modal');
const modalClose = document.getElementById('modal-close');
const modalWord = document.getElementById('modal-word');
const modalDetails = document.getElementById('modal-details');

// File input change handler
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = file.name;
    } else {
        fileName.textContent = 'Choose a file...';
    }
});

// Upload form submit handler
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
        showError('Please select a file to analyze');
        return;
    }

    // Create form data
    const formData = new FormData();
    formData.append('file', file);

    try {
        // Show progress section
        hideAllSections();
        showSection(progressSection);

        // Upload file
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'Upload failed');
        }

        // Store session ID
        currentSessionId = data.session_id;

        // Connect to SSE for real-time progress
        connectToProgressStream(data.session_id);

    } catch (error) {
        showError(error.message);
    }
});

// Connect to SSE progress stream
let eventSource = null;

function connectToProgressStream(sessionId) {
    // Close existing connection if any
    if (eventSource) {
        eventSource.close();
    }

    // Create new EventSource connection
    eventSource = new EventSource(`/progress/${sessionId}`);

    // Handle progress events
    eventSource.addEventListener('progress', (e) => {
        const data = JSON.parse(e.data);
        // Use bilingual progress update if available
        if (typeof updateBilingualProgress === 'function') {
            updateBilingualProgress(data.progress, data.stage);
        } else {
            updateProgress(data.progress, formatStageName(data.stage));
        }
    });

    // Handle completion event
    eventSource.addEventListener('complete', (e) => {
        const data = JSON.parse(e.data);
        updateProgress(100, 'Complete!');
        eventSource.close();
        eventSource = null;

        // Show results after brief delay
        setTimeout(() => {
            showResults();
        }, 500);
    });

    // Handle error events
    eventSource.addEventListener('error', (e) => {
        if (e.data) {
            const data = JSON.parse(e.data);
            showError(data.error?.message || 'Analysis failed');
        } else {
            showError('Connection to server lost');
        }

        if (eventSource) {
            eventSource.close();
            eventSource = null;
        }
    });

    // Handle connection errors
    eventSource.onerror = (e) => {
        console.error('SSE connection error:', e);

        // Only show error if we haven't already completed
        if (progressSection && !progressSection.classList.contains('hidden')) {
            // Connection might have closed normally after completion
            // Don't show error in that case
            if (eventSource && eventSource.readyState === EventSource.CLOSED) {
                console.log('SSE connection closed');
            }
        }
    };
}

// Format stage name for display
function formatStageName(stage) {
    const stageNames = {
        'VALIDATING': 'Validating file...',
        'EXTRACTING': 'Extracting text...',
        'TOKENIZING': 'Tokenizing words...',
        'DETECTING_PHRASES': 'Detecting phrases...',
        'MATCHING_LEVELS': 'Matching CEFR levels...',
        'GENERATING_STATS': 'Generating statistics...',
        'COMPLETED': 'Complete!'
    };

    return stageNames[stage] || stage;
}

// Update progress display
function updateProgress(percent, stage) {
    progressFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent}%`;
    progressStage.textContent = stage;
}

// Show results section
async function showResults() {
    hideAllSections();
    showSection(resultsSection);

    // Fetch full analysis results
    try {
        const response = await fetch(`/download/${currentSessionId}/json`);
        if (!response.ok) {
            throw new Error('Failed to fetch results');
        }

        const blob = await response.blob();
        const text = await blob.text();
        analysisResults = JSON.parse(text);

        // Store in window for reading view access
        window.currentAnalysisResults = analysisResults;

        // DEBUG: Log analysis results
        console.log('[DEBUG] Analysis results loaded');
        console.log('[DEBUG] Has processed_text:', 'processed_text' in analysisResults);
        console.log('[DEBUG] processed_text type:', typeof analysisResults.processed_text);
        console.log('[DEBUG] processed_text length:', analysisResults.processed_text ? analysisResults.processed_text.length : 0);

        // Display statistics summary
        displayStatistics(analysisResults);

        // Display word lists
        displayWords(analysisResults);

        // Setup event listeners for filters
        setupInteractiveFilters();

    } catch (error) {
        console.error('Error fetching results:', error);
        const statsDiv = document.getElementById('stats-summary');
        statsDiv.innerHTML = `
            <p>Analysis completed successfully!</p>
            <p>Use the download buttons below to get your results.</p>
        `;
    }
}

/**
 * Calculate reading difficulty score based on CEFR distribution and text characteristics
 * 计算阅读难度评分（基于CEFR分布和文本特征）
 */
function calculateReadingDifficulty(stats) {
    const totalWords = stats.total_word_occurrences || 0;
    const uniqueWords = stats.total_unique_words || 0;
    const totalPhrases = stats.total_unique_phrases || 0;
    const distribution = stats.level_distribution || {};

    // CEFR level weights (权重)
    const weights = { 'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6, 'C2+': 7 };

    // 1. Base Score: Weighted CEFR Score (基础难度分)
    let baseScore = 0;
    for (const [level, weight] of Object.entries(weights)) {
        const percentage = (distribution[level]?.percentage || 0) / 100;
        baseScore += percentage * weight;
    }
    // Normalize base score from [1, 7] range to [0, 1] range
    // 将基础分从 [1, 7] 范围归一化到 [0, 1] 范围
    baseScore = (baseScore - 1) / 6;

    // 2. Lexical Diversity Factor (词汇多样性修正)
    const diversity = uniqueWords / totalWords;
    // Ensure diversity factor is between 0.7 and 1.5
    const diversityFactor = Math.max(0.7, Math.min(1.5, 1 + 0.5 * (diversity - 0.4)));

    // 3. Phrasal Verb Factor (短语动词修正)
    // Use ratio instead of absolute count, with a cap at 1.3
    const phrasalRatio = uniqueWords > 0 ? totalPhrases / uniqueWords : 0;
    const phrasalFactor = Math.min(1.3, 1 + 0.5 * phrasalRatio);

    // 4. Length Normalization (长度修正)
    const lengthFactor = 1 - Math.exp(-totalWords / 300);

    // 5. Final Score (综合难度得分, 0-100)
    let finalScore = baseScore * diversityFactor * phrasalFactor * lengthFactor * 100;

    // Ensure score is within 0-100 range
    finalScore = Math.max(0, Math.min(100, finalScore));

    // Determine level and interpretation
    let level, levelCn, audience, audienceCn, description, descriptionCn;

    if (finalScore < 20) {
        level = 'A1-A2';
        levelCn = '基础水平';
        audience = 'Beginner / Young Children';
        audienceCn = '英语初学者 / 儿童启蒙';
        description = 'Simple vocabulary, suitable for early language learners';
        descriptionCn = '词汇简单，适合英语启蒙阶段';
    } else if (finalScore < 40) {
        level = 'B1';
        levelCn = '独立运用 - 初级';
        audience = 'Elementary / ESL Intermediate';
        audienceCn = '小学高年级 / ESL 初中';
        description = 'Suitable for young learners with basic English foundation';
        descriptionCn = '适合有一定英语基础的小学生或初中生阅读';
    } else if (finalScore < 60) {
        level = 'B2-C1';
        levelCn = '独立运用 - 中级';
        audience = 'Teenagers / General Adults';
        audienceCn = '青少年 / 一般成人';
        description = 'Moderate difficulty, suitable for intermediate English readers';
        descriptionCn = '难度适中，适合中级英语水平读者';
    } else if (finalScore < 80) {
        level = 'C1-C2';
        levelCn = '熟练运用';
        audience = 'Advanced / Native High School';
        audienceCn = '高级学习者 / 母语中学生';
        description = 'Complex vocabulary, suitable for advanced learners';
        descriptionCn = '词汇较复杂，适合英语高级学习者';
    } else {
        level = 'C2+';
        levelCn = '专业水平';
        audience = 'Academic / Professional';
        audienceCn = '学术 / 专业领域';
        description = 'Highly specialized, academic or literary content';
        descriptionCn = '高度专业化，学术或文学性内容';
    }

    // Determine color based on score (green -> purple gradient)
    let gradientColor;
    if (finalScore < 20) {
        gradientColor = 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)'; // Green
    } else if (finalScore < 40) {
        gradientColor = 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'; // Blue
    } else if (finalScore < 60) {
        gradientColor = 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'; // Amber
    } else if (finalScore < 80) {
        gradientColor = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'; // Red
    } else {
        gradientColor = 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)'; // Purple
    }

    return {
        score: finalScore.toFixed(1),
        level,
        levelCn,
        audience,
        audienceCn,
        description,
        descriptionCn,
        gradientColor,
        details: {
            baseScore: baseScore.toFixed(2),
            diversity: diversity.toFixed(2),
            diversityFactor: diversityFactor.toFixed(2),
            phrasalRatio: phrasalRatio.toFixed(3),
            phrasalFactor: phrasalFactor.toFixed(2),
            lengthFactor: lengthFactor.toFixed(2)
        }
    };
}

// Display statistics summary (T044)
function displayStatistics(results) {
    const statsDiv = document.getElementById('stats-summary');

    const stats = results.statistics || {};
    const totalWords = stats.total_word_occurrences || 0;
    const uniqueWords = stats.total_unique_words || 0;
    const totalPhrases = stats.total_unique_phrases || 0;

    // Calculate reading difficulty
    const difficulty = calculateReadingDifficulty(stats);

    // Create CEFR distribution bars
    const cefrLevels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'C2+'];
    const distribution = stats.level_distribution || {};

    const distributionHTML = cefrLevels.map(level => {
        const levelData = distribution[level] || { count: 0, percentage: 0 };
        const count = levelData.count || 0;
        const percentage = levelData.percentage ? levelData.percentage.toFixed(1) : 0;
        return `
            <div class="stat-bar">
                <div class="stat-label">${level}: ${count} (${percentage}%)</div>
                <div class="stat-bar-bg">
                    <div class="stat-bar-fill level-${level}" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    }).join('');

    statsDiv.innerHTML = `
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">${totalWords}</div>
                <div class="stat-label">Total Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${uniqueWords}</div>
                <div class="stat-label">Unique Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${totalPhrases}</div>
                <div class="stat-label">Phrasal Verbs</div>
            </div>
        </div>

        <!-- Reading Difficulty Score -->
        <div class="difficulty-score">
            <h4 class="bilingual">
                <span class="en">📊 Reading Difficulty Assessment</span>
                <span class="cn">阅读难度评估</span>
            </h4>
            <div class="difficulty-main">
                <div class="difficulty-score-display">
                    <div class="score-value" style="background: ${difficulty.gradientColor}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">${difficulty.score}</div>
                    <div class="score-max">/ 100</div>
                </div>
                <div class="difficulty-info">
                    <div class="difficulty-level">
                        <span class="level-badge">${difficulty.level}</span>
                        <span class="level-cn">${difficulty.levelCn}</span>
                    </div>
                    <div class="difficulty-audience bilingual">
                        <span class="en">👥 ${difficulty.audience}</span>
                        <span class="cn">${difficulty.audienceCn}</span>
                    </div>
                    <div class="difficulty-desc bilingual">
                        <span class="en">${difficulty.description}</span>
                        <span class="cn">${difficulty.descriptionCn}</span>
                    </div>
                </div>
            </div>
            <details class="difficulty-details">
                <summary class="bilingual">
                    <span class="en">📐 Calculation Details</span>
                    <span class="cn">计算详情</span>
                </summary>
                <div class="detail-grid">
                    <div class="detail-item">
                        <span class="detail-label bilingual">
                            <span class="en">Base Score</span>
                            <span class="cn">基础难度分</span>
                        </span>
                        <span class="detail-value">${difficulty.details.baseScore}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label bilingual">
                            <span class="en">Diversity</span>
                            <span class="cn">词汇多样性</span>
                        </span>
                        <span class="detail-value">${difficulty.details.diversity} (×${difficulty.details.diversityFactor})</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label bilingual">
                            <span class="en">Phrasal Verbs</span>
                            <span class="cn">短语动词修正</span>
                        </span>
                        <span class="detail-value">×${difficulty.details.phrasalFactor}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label bilingual">
                            <span class="en">Length Factor</span>
                            <span class="cn">长度修正</span>
                        </span>
                        <span class="detail-value">×${difficulty.details.lengthFactor}</span>
                    </div>
                </div>
            </details>
        </div>

        <div class="cefr-distribution">
            <h4>CEFR Distribution</h4>
            <div class="cefr-guide">
                <div class="cefr-guide-item"><strong>A1-A2</strong>: Basic user (beginner) | 基础水平</div>
                <div class="cefr-guide-item"><strong>B1-B2</strong>: Independent user (intermediate) | 独立运用</div>
                <div class="cefr-guide-item"><strong>C1-C2</strong>: Proficient user (advanced) | 熟练运用</div>
                <div class="cefr-guide-item"><strong>C2+</strong>: Beyond CEFR (specialized) | 超出CEFR（专业词汇）</div>
            </div>
            ${distributionHTML}
        </div>
    `;
}

// Display words and phrasal verbs (T038)
function displayWords(results) {
    const words = results.words || [];
    const phrases = results.phrases || [];

    // Store in global for filtering
    window.allWords = words;
    window.allPhrases = phrases;

    // Initial display (all levels)
    updateWordDisplay();
}

// Update word display based on current filter and search (T039, T040)
function updateWordDisplay() {
    const words = window.allWords || [];
    const phrases = window.allPhrases || [];

    // Filter words
    let filteredWords = words.filter(word => {
        // Level filter
        const levelMatch = currentFilter === 'all' || word.level === currentFilter;

        // Search filter
        const searchMatch = !searchTerm ||
            word.word.toLowerCase().includes(searchTerm.toLowerCase());

        return levelMatch && searchMatch;
    });

    // Filter phrases
    let filteredPhrases = phrases.filter(phrase => {
        // Level filter
        const levelMatch = currentFilter === 'all' || phrase.level === currentFilter;

        // Search filter
        const searchMatch = !searchTerm ||
            phrase.phrase.toLowerCase().includes(searchTerm.toLowerCase());

        return levelMatch && searchMatch;
    });

    // Update counts
    wordCount.textContent = filteredWords.length;
    phraseCount.textContent = filteredPhrases.length;

    // CEFR level colors - unified gradient from green (easiest) to purple (hardest)
    const cefrColors = {
        'A1': '#22c55e',   // Green
        'A2': '#3b82f6',   // Blue
        'B1': '#f59e0b',   // Amber
        'B2': '#f97316',   // Orange
        'C1': '#ef4444',   // Red
        'C2': '#a855f7',   // Purple
        'C2+': '#9333ea'   // Dark purple
    };

    // Render words (Feature 004: T008, T009 - Entire card clickable, no translate button)
    wordList.innerHTML = filteredWords.slice(0, 200).map(word => {
        const levelColor = cefrColors[word.level] || '#757575';
        const phonetic = (word.phonetic && isValidPhonetic(word.phonetic, word.word))
            ? `<div class="word-phonetic">/${word.phonetic}/</div>`
            : '';
        return `
            <div class="word-item word-card"
                 data-word='${JSON.stringify(word)}'
                 tabindex="0"
                 role="button"
                 aria-label="View details for '${word.word}'">
                <div class="word-text">${word.word}</div>
                ${phonetic}
                <div class="word-level cefr-badge" style="background-color: ${levelColor};">${word.level}</div>
            </div>
        `;
    }).join('');

    // Render phrases (Feature 004: T008, T009 - Entire card clickable, no translate button)
    phraseList.innerHTML = filteredPhrases.slice(0, 100).map(phrase => {
        const levelColor = cefrColors[phrase.level] || '#757575';
        return `
            <div class="word-item word-card"
                 data-word='${JSON.stringify(phrase)}'
                 tabindex="0"
                 role="button"
                 aria-label="View details for '${phrase.phrase}'">
                <div class="word-text">${phrase.phrase}</div>
                <div class="word-level cefr-badge" style="background-color: ${levelColor};">${phrase.level}</div>
            </div>
        `;
    }).join('');

    // Add click handlers for word details (Feature 004: T011 - Entire card clickable)
    document.querySelectorAll('.word-item').forEach(item => {
        // Click handler for entire card
        item.addEventListener('click', (e) => {
            const wordData = JSON.parse(item.getAttribute('data-word'));
            showWordDetails(wordData);
        });

        // Keyboard accessibility: Enter/Space keys
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const wordData = JSON.parse(item.getAttribute('data-word'));
                showWordDetails(wordData);
            }
        });
    });

    // Feature 004: Translate button handlers removed - translation now auto-loads in modal
    // (Old inline translation functionality deprecated in favor of modal-based translation)

    // Initialize main tab navigation (Overview/Vocabulary/Reading/Download)
    if (!window.mainTabsInitialized) {
        initMainTabNavigation();
        window.mainTabsInitialized = true;
    }

    // Feature 004: Initialize sub-tab navigation and keyboard controls after rendering
    // Only initialize once per page load (check if tabs exist and haven't been initialized)
    const tabButtons = document.querySelectorAll('.tab-btn');
    if (tabButtons.length > 0 && !window.tabsInitialized) {
        initTabNavigation();
        restoreTabState();
        initKeyboardNavigation();
        window.tabsInitialized = true;

        // T014: Feature 005 - Initialize reading view tab
        initReadingView();
    }

    // Helper function to show inline translation
    function showInlineTranslation(wordItem, btn, result) {
        // Remove any existing translation
        const existing = wordItem.querySelector('.translation-result');
        if (existing) existing.remove();

        // Create translation display
        const translationDiv = document.createElement('div');
        translationDiv.className = 'translation-result';
        translationDiv.innerHTML = `
            <div class="translation-text">${result.translation || result.target_text || '翻译失败'}</div>
            <div class="translation-meta">
                <span>${result.source || 'Argos'}</span>
                ${result.cached ? '<span>• 缓存</span>' : ''}
            </div>
        `;

        // Insert after word text
        const wordText = wordItem.querySelector('.word-text');
        wordText.after(translationDiv);

        // Update button state
        btn.classList.add('active');
        btn.textContent = '✕';
    }
}

/**
 * Validate phonetic transcription to filter out obvious errors
 * @param {string} phonetic - Phonetic transcription to validate
 * @param {string} word - The word being checked
 * @returns {boolean} - True if phonetic appears valid
 */
function isValidPhonetic(phonetic, word) {
    if (!phonetic || phonetic.trim().length === 0) {
        return false;
    }

    // Filter out obviously wrong phonetics
    // 1. Too short (less than 2 characters is suspicious)
    if (phonetic.length < 2) {
        return false;
    }

    // 2. Contains Chinese characters (indicates wrong dictionary match)
    if (/[\u4e00-\u9fa5]/.test(phonetic)) {
        return false;
    }

    // 3. Phonetic is completely different from word (length-based heuristic)
    // If word is long but phonetic is very short, likely wrong
    if (word.length > 5 && phonetic.length < 3) {
        return false;
    }

    // 4. Common error patterns
    // "nan" is a common error for proper nouns
    if (phonetic.toLowerCase() === 'nan' && word.toLowerCase() !== 'nan') {
        return false;
    }

    return true;
}

// Setup interactive filters (T039, T040)
function setupInteractiveFilters() {
    // Level filter buttons
    levelFilters.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            levelFilters.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Update filter and refresh display
            currentFilter = btn.getAttribute('data-level');
            updateWordDisplay();

            // T015: Feature 005 - Update reading view when filter changes
            updateReadingView();
        });
    });

    // Search input with debounce
    let searchTimeout;
    wordSearch.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchTerm = e.target.value;
            updateWordDisplay();

            // T015: Feature 005 - Update reading view when search changes
            updateReadingView();
        }, 300);
    });
}

// Show word details modal (T041)
function showWordDetails(wordData) {
    modalWord.textContent = wordData.word || wordData.phrase;

    let detailsHTML = `
        <div class="detail-row">
            <div class="detail-label">CEFR Level</div>
            <div class="detail-value">${wordData.level}</div>
        </div>
    `;

    // Add phonetic transcription if available and valid
    if (wordData.phonetic && isValidPhonetic(wordData.phonetic, wordData.word)) {
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Phonetic (音标)</div>
                <div class="detail-value" style="font-family: 'Lucida Sans Unicode', 'Arial Unicode MS', sans-serif; font-style: italic;">/${wordData.phonetic}/</div>
            </div>
        `;
    }

    if (wordData.definition_cn) {
        // Convert \n to <br> for proper line breaks
        const formattedDefinition = wordData.definition_cn.replace(/\\n/g, '<br>');
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Chinese Translation (中文释义)</div>
                <div class="detail-value" style="white-space: normal;">${formattedDefinition}</div>
            </div>
        `;
    }

    if (wordData.frequency) {
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Frequency in Text</div>
                <div class="detail-value">${wordData.frequency} occurrence(s)</div>
            </div>
        `;
    }

    if (wordData.examples && wordData.examples.length > 0) {
        // Sort examples by length (shortest first) and take 3-5 shortest
        const sortedExamples = [...wordData.examples]
            .sort((a, b) => a.length - b.length)
            .slice(0, Math.min(5, wordData.examples.length));

        const examples = sortedExamples.map((ex, index) => `
            <li class="example-item" data-example-index="${index}">
                <div class="example-text">${ex}</div>
                <button class="example-translate-btn" data-text="${ex.replace(/"/g, '&quot;')}" title="Translate sentence / 翻译句子">翻</button>
                <div class="example-translation" style="display: none;"></div>
            </li>
        `).join('');
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Example Sentences</div>
                <div class="detail-value">
                    <ul style="margin-top: 0.5rem; padding-left: 0; list-style: none;">
                        ${examples}
                    </ul>
                </div>
            </div>
        `;
    }

    modalDetails.innerHTML = detailsHTML;

    // Feature 004: T014 - Auto-load Chinese translation on modal open
    if (!wordData.definition_cn && typeof translateText === 'function') {
        // Create translation section with skeleton loading
        const translationRow = document.createElement('div');
        translationRow.className = 'detail-row';
        translationRow.id = 'auto-translation-row';
        translationRow.innerHTML = `
            <div class="detail-label">Chinese Translation (中文释义)</div>
            <div class="detail-value">
                <div class="translation-skeleton">
                    <div class="skeleton-line" style="width: 90%;"></div>
                    <div class="skeleton-line" style="width: 75%;"></div>
                    <div class="skeleton-line" style="width: 85%;"></div>
                    <div class="loading-text">加载中...</div>
                </div>
            </div>
        `;

        // Insert after CEFR level row
        const firstRow = modalDetails.querySelector('.detail-row');
        if (firstRow && firstRow.nextSibling) {
            modalDetails.insertBefore(translationRow, firstRow.nextSibling);
        } else {
            modalDetails.insertBefore(translationRow, modalDetails.firstChild);
        }

        // Fetch translation
        const wordText = wordData.word || wordData.phrase;
        const translationType = wordData.word ? 'word' : 'phrase';

        translateText(wordText, translationType)
            .then(result => {
                const translationValue = translationRow.querySelector('.detail-value');
                const translation = result.translation || result.target_text || '翻译失败';
                const source = result.source || 'Argos';
                const cached = result.cached ? '<span class="translation-cached-label">缓存</span>' : '';

                translationValue.innerHTML = `
                    <div style="white-space: normal;">${translation}</div>
                    <div class="translation-meta" style="margin-top: 8px; font-size: 12px; color: var(--text-secondary);">
                        <span>来源: ${source}</span>
                        ${cached}
                    </div>
                `;
            })
            .catch(error => {
                const translationValue = translationRow.querySelector('.detail-value');
                translationValue.innerHTML = `
                    <div class="translation-error" style="color: var(--error-color, #dc2626);">
                        暂时无法获取释义
                    </div>
                    <button class="retry-translation-btn" onclick="location.reload()"
                            style="margin-top: 8px; padding: 6px 12px; font-size: 12px;
                                   background: var(--primary-color); color: white;
                                   border: none; border-radius: 4px; cursor: pointer;">
                        重试
                    </button>
                `;
                console.error('Auto-translation error:', error);
            });
    }

    // Add event listeners for example sentence translation buttons
    document.querySelectorAll('.example-translate-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();

            const exampleItem = btn.closest('.example-item');
            const translationDiv = exampleItem.querySelector('.example-translation');
            const text = btn.getAttribute('data-text');

            // Toggle translation visibility
            if (translationDiv.style.display === 'block') {
                translationDiv.style.display = 'none';
                btn.textContent = '翻';
                btn.classList.remove('active');
                return;
            }

            // Check if already translated
            if (translationDiv.innerHTML) {
                translationDiv.style.display = 'block';
                btn.textContent = '✕';
                btn.classList.add('active');
                return;
            }

            // Show loading
            btn.classList.add('loading');
            btn.disabled = true;
            btn.textContent = '...';

            try {
                if (typeof translateText === 'function') {
                    const result = await translateText(text, 'sentence');
                    const translation = result.translation || result.target_text || '翻译失败';
                    translationDiv.innerHTML = `
                        <div class="example-translation-text">${translation}</div>
                        <div class="example-translation-meta">
                            <span>${result.source || 'Argos'}</span>
                        </div>
                    `;
                    translationDiv.style.display = 'block';
                    btn.textContent = '✕';
                    btn.classList.add('active');
                } else {
                    alert('翻译功能未加载');
                }
            } catch (error) {
                alert('翻译失败: ' + error.message);
            } finally {
                btn.classList.remove('loading');
                btn.disabled = false;
            }
        });
    });

    wordModal.classList.remove('hidden');
}

// Close modal
modalClose.addEventListener('click', () => {
    wordModal.classList.add('hidden');
});

// Close modal when clicking outside
wordModal.addEventListener('click', (e) => {
    if (e.target === wordModal) {
        wordModal.classList.add('hidden');
    }
});

// Download handlers
downloadJsonBtn.addEventListener('click', () => {
    downloadResult('json');
});

downloadCsvBtn.addEventListener('click', () => {
    downloadResult('csv');
});

downloadMarkdownBtn.addEventListener('click', () => {
    downloadResult('markdown');
});

// TXT download handler with level filtering
const downloadTxtBtn = document.getElementById('download-txt');
if (downloadTxtBtn) {
    downloadTxtBtn.addEventListener('click', () => {
        downloadTxtWordList();
    });
}

// Level checkbox logic
const downloadLevelAll = document.getElementById('download-level-all');
const levelCheckboxItems = document.querySelectorAll('.level-checkbox-item');

if (downloadLevelAll) {
    downloadLevelAll.addEventListener('change', (e) => {
        // When "All Levels" is checked, uncheck all individual levels
        if (e.target.checked) {
            levelCheckboxItems.forEach(cb => {
                cb.checked = false;
            });
        }
    });
}

// When any individual level is checked, uncheck "All Levels"
levelCheckboxItems.forEach(cb => {
    cb.addEventListener('change', (e) => {
        if (e.target.checked && downloadLevelAll) {
            downloadLevelAll.checked = false;
        }
    });
});

// Download result in specified format
function downloadResult(format) {
    if (!currentSessionId) {
        showError('No analysis session found');
        return;
    }

    // Trigger download by navigating to download URL
    window.location.href = `/download/${currentSessionId}/${format}`;
}

/**
 * Download TXT word list with level filtering (auto-split into 500-word files)
 */
async function downloadTxtWordList() {
    if (!window.currentAnalysisResults || !window.currentAnalysisResults.words) {
        alert('No analysis results available / 没有可用的分析结果');
        return;
    }

    // Get selected levels
    const selectedLevels = getSelectedDownloadLevels();

    if (selectedLevels.length === 0) {
        alert('Please select at least one CEFR level / 请至少选择一个CEFR级别');
        return;
    }

    // Filter words by selected levels
    let filteredWords = window.currentAnalysisResults.words;

    if (!selectedLevels.includes('all')) {
        filteredWords = filteredWords.filter(word => selectedLevels.includes(word.level));
    }

    if (filteredWords.length === 0) {
        alert('No words found for selected levels / 所选级别没有找到单词');
        return;
    }

    // Extract all original forms (case-preserved)
    const allWords = [];
    filteredWords.forEach(word => {
        if (word.original_forms && word.original_forms.length > 0) {
            allWords.push(...word.original_forms);
        } else {
            allWords.push(word.word);
        }
    });

    // Add phrasal verbs (filtered by level)
    const phrasal_verbs = window.currentAnalysisResults.phrasal_verbs || [];
    let filteredPhrases = phrasal_verbs;

    if (!selectedLevels.includes('all')) {
        filteredPhrases = phrasal_verbs.filter(pv => selectedLevels.includes(pv.level));
    }

    filteredPhrases.forEach(pv => {
        allWords.push(pv.phrase);
    });

    // Remove duplicates while preserving case
    const uniqueWords = [...new Set(allWords)];

    // Split into chunks of 500 words
    const chunkSize = 500;
    const chunks = [];
    for (let i = 0; i < uniqueWords.length; i += chunkSize) {
        chunks.push(uniqueWords.slice(i, i + chunkSize));
    }

    // Generate base filename
    const levelStr = selectedLevels.includes('all') ? 'all-levels' : selectedLevels.join('-');
    const sourceName = window.currentAnalysisResults.source_file || 'vocabulary';
    const baseFilename = `${sourceName.replace(/\.[^/.]+$/, '')}_${levelStr}_words`;

    // Download each chunk
    for (let i = 0; i < chunks.length; i++) {
        const chunk = chunks[i];
        const txtContent = chunk.join(', ');

        // Create blob and download
        const blob = new Blob([txtContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;

        // Add part number if multiple files
        if (chunks.length > 1) {
            link.download = `${baseFilename}_part${i + 1}.txt`;
        } else {
            link.download = `${baseFilename}.txt`;
        }

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        // Add delay between downloads to avoid browser blocking
        if (i < chunks.length - 1) {
            await new Promise(resolve => setTimeout(resolve, 300));
        }
    }

    // Show completion message
    const totalWords = uniqueWords.length;
    const fileCount = chunks.length;

    if (fileCount > 1) {
        alert(
            `Downloaded ${totalWords} items (words + phrasal verbs) in ${fileCount} files (500 items each)\n` +
            `已下载 ${totalWords} 个词条（单词 + 短语动词），共 ${fileCount} 个文件（每个500词条）`
        );
    } else {
        alert(
            `Downloaded ${totalWords} items (words + phrasal verbs)\n` +
            `已下载 ${totalWords} 个词条（单词 + 短语动词）`
        );
    }
}

/**
 * Get selected download levels
 * @returns {Array<string>} Array of selected level codes
 */
function getSelectedDownloadLevels() {
    const levels = [];

    // Check if "All Levels" is selected
    const allCheckbox = document.getElementById('download-level-all');
    if (allCheckbox && allCheckbox.checked) {
        return ['all'];
    }

    // Get individual selected levels
    const checkboxes = document.querySelectorAll('.level-checkbox-item:checked');
    checkboxes.forEach(cb => {
        levels.push(cb.value);
    });

    return levels;
}

// Analyze another file
analyzeAnotherBtn.addEventListener('click', () => {
    resetForm();
});

tryAgainBtn.addEventListener('click', () => {
    resetForm();
});

// Reset form to initial state
function resetForm() {
    // Close SSE connection if active
    if (eventSource) {
        eventSource.close();
        eventSource = null;
    }

    currentSessionId = null;
    uploadForm.reset();
    fileName.textContent = 'Choose a file...';
    hideAllSections();
    showSection(uploadSection);
}

// Show error
function showError(message) {
    hideAllSections();

    // Try to use bilingual error display if available
    if (typeof showBilingualError === 'function') {
        // For generic errors, show as bilingual
        errorText.innerHTML = '';
        const errorDiv = document.createElement('div');
        errorDiv.className = 'bilingual';

        const enSpan = document.createElement('span');
        enSpan.className = 'en';
        enSpan.textContent = message;

        const cnSpan = document.createElement('span');
        cnSpan.className = 'cn';
        cnSpan.textContent = '发生错误'; // Generic Chinese error message

        errorDiv.appendChild(enSpan);
        errorDiv.appendChild(cnSpan);
        errorText.appendChild(errorDiv);
    } else {
        errorText.textContent = message;
    }

    showSection(errorSection);
}

// Helper functions
function hideAllSections() {
    uploadSection.classList.add('hidden');
    progressSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

function showSection(section) {
    section.classList.remove('hidden');
}

// ===================================================================
// Main Tab Navigation (Overview/Vocabulary/Reading/Download)
// ===================================================================

/**
 * Initialize main tab navigation system
 */
function initMainTabNavigation() {
    const mainTabButtons = document.querySelectorAll('.main-tab-btn');

    mainTabButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetTab = btn.getAttribute('data-tab');
            switchMainTab(targetTab);
        });
    });
}

/**
 * Switch between main tabs
 * @param {string} tabName - 'overview', 'vocabulary', 'reading', or 'download'
 */
function switchMainTab(tabName) {
    const allTabs = document.querySelectorAll('.main-tab-btn');
    const allPanels = document.querySelectorAll('.main-tab-panel');

    // Find target elements
    const targetButton = document.querySelector(`.main-tab-btn[data-tab="${tabName}"]`);
    const targetPanel = document.getElementById(`${tabName}-panel`);

    if (!targetButton || !targetPanel) {
        console.error(`Main tab not found: ${tabName}`);
        return;
    }

    // Update button states
    allTabs.forEach(tab => {
        tab.classList.remove('active');
        tab.setAttribute('aria-selected', 'false');
    });
    targetButton.classList.add('active');
    targetButton.setAttribute('aria-selected', 'true');

    // Update panel states
    allPanels.forEach(panel => {
        panel.classList.remove('active');
        panel.setAttribute('hidden', '');
    });
    targetPanel.classList.add('active');
    targetPanel.removeAttribute('hidden');

    // If switching to reading view, make sure it's rendered
    if (tabName === 'reading') {
        console.log('[DEBUG] Switching to reading view');
        console.log('[DEBUG] window.currentAnalysisResults:', !!window.currentAnalysisResults);

        if (window.currentAnalysisResults) {
            const readingContent = document.getElementById('reading-content');
            console.log('[DEBUG] readingContent element:', !!readingContent);

            if (readingContent) {
                // Check if content is empty (ignore HTML comments, use textContent)
                const hasContent = readingContent.textContent.trim().length > 0 || readingContent.children.length > 0;
                console.log('[DEBUG] readingContent has actual content:', hasContent);

                if (!hasContent) {
                    console.log('[DEBUG] Calling parseTextForReading()');
                    parseTextForReading(window.currentAnalysisResults.processed_text, window.currentAnalysisResults);
                } else {
                    console.log('[DEBUG] Reading content already rendered, skipping');
                }
            }
        }
    }
}

// ===================================================================
// FEATURE 004: T018 - Sub-Tab Switching Logic (Words/Phrases)
// ===================================================================

/**
 * Initialize sub-tab navigation system
 * Implements tab switching with fade transitions and ARIA attributes
 * Reference: tasks.md T018, spec.md FR-008
 */
function initTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetTab = btn.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

/**
 * Switch between word and phrase tabs
 * @param {string} tabName - 'words' or 'phrases'
 */
function switchTab(tabName) {
    const allTabs = document.querySelectorAll('.tab-btn');
    const allPanels = document.querySelectorAll('.tab-panel');

    // Find target elements
    const targetButton = document.querySelector(`[data-tab="${tabName}"]`);
    const targetPanel = document.getElementById(`${tabName}-panel`);

    if (!targetButton || !targetPanel) {
        console.error(`Tab not found: ${tabName}`);
        return;
    }

    // Update button states
    allTabs.forEach(tab => {
        tab.classList.remove('active');
        tab.setAttribute('aria-selected', 'false');
    });
    targetButton.classList.add('active');
    targetButton.setAttribute('aria-selected', 'true');

    // Fade out current panel, then fade in target panel
    const currentPanel = document.querySelector('.tab-panel.active');

    if (currentPanel && currentPanel !== targetPanel) {
        // Fade out current (CSS animation will handle this)
        currentPanel.classList.remove('active');
        currentPanel.setAttribute('hidden', '');

        // Delay fade in for smooth transition (100ms fade out + 200ms fade in)
        setTimeout(() => {
            targetPanel.removeAttribute('hidden');
            targetPanel.classList.add('active');
        }, 100);
    } else {
        // First load or same tab
        targetPanel.removeAttribute('hidden');
        targetPanel.classList.add('active');
    }

    // Save tab state to localStorage (T019)
    try {
        localStorage.setItem('activeTab', tabName);
    } catch (e) {
        console.warn('localStorage not available:', e);
    }
}

/**
 * Restore tab state from localStorage on page load (T019)
 */
function restoreTabState() {
    try {
        const savedTab = localStorage.getItem('activeTab');
        if (savedTab && (savedTab === 'words' || savedTab === 'phrases')) {
            switchTab(savedTab);
        }
    } catch (e) {
        console.warn('Could not restore tab state:', e);
    }
}

// ===================================================================
// FEATURE 004: T028, T029 - Keyboard Navigation
// ===================================================================

/**
 * Initialize keyboard navigation for accessibility
 * Implements arrow key tab switching and Escape key modal closing
 * Reference: tasks.md T028, T029, WCAG 2.1 AA
 */
function initKeyboardNavigation() {
    // T028: Arrow key navigation for tabs
    const tabButtons = document.querySelectorAll('.tab-btn');

    tabButtons.forEach((btn, index) => {
        btn.addEventListener('keydown', (e) => {
            let targetIndex = -1;

            if (e.key === 'ArrowLeft' || e.key === 'Left') {
                // Focus previous tab (wrap to last if at first)
                e.preventDefault();
                targetIndex = index === 0 ? tabButtons.length - 1 : index - 1;
            } else if (e.key === 'ArrowRight' || e.key === 'Right') {
                // Focus next tab (wrap to first if at last)
                e.preventDefault();
                targetIndex = index === tabButtons.length - 1 ? 0 : index + 1;
            }

            if (targetIndex >= 0) {
                const targetTab = tabButtons[targetIndex];
                targetTab.focus();
                // Auto-activate tab on arrow key navigation
                const tabName = targetTab.getAttribute('data-tab');
                switchTab(tabName);
            }
        });
    });

    // T029: Escape key closes modal
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' || e.key === 'Esc') {
            const modal = document.getElementById('word-modal');
            if (modal && !modal.classList.contains('hidden')) {
                e.preventDefault();
                closeModalWithFocusReturn();
            }
        }
    });
}

/**
 * Close modal and return focus to triggering element
 * Part of T029 - keyboard accessibility
 */
let lastFocusedElement = null;

// Store focused element before opening modal
const originalShowWordDetails = showWordDetails;
window.showWordDetails = function(wordData) {
    lastFocusedElement = document.activeElement;
    originalShowWordDetails(wordData);
};

function closeModalWithFocusReturn() {
    const modal = document.getElementById('word-modal');
    modal.classList.add('hidden');

    // Return focus to the element that triggered the modal
    if (lastFocusedElement && typeof lastFocusedElement.focus === 'function') {
        setTimeout(() => {
            lastFocusedElement.focus();
        }, 100);
    }
}

/* ===================================================================
   FEATURE 005: IMMERSIVE FULL-TEXT READING VIEW
   =================================================================== */

/**
 * T012: Find word data in analysis results
 * @param {string} token - Word to look up (lowercase)
 * @param {Object} analysisResults - Analysis results with words and phrasal verbs
 * @returns {Object|null} Word data object or null if not found
 */
function findWordData(token, analysisResults) {
    if (!analysisResults || !token) return null;

    const lowerToken = token.toLowerCase();

    // Check words array
    const wordMatch = analysisResults.words?.find(w => w.word.toLowerCase() === lowerToken);
    if (wordMatch) {
        return { ...wordMatch, type: 'word' };
    }

    // Check phrasal verbs array
    const phraseMatch = analysisResults.phrasal_verbs?.find(pv => pv.phrase.toLowerCase() === lowerToken);
    if (phraseMatch) {
        return { ...phraseMatch, word: phraseMatch.phrase, type: 'phrasal_verb' };
    }

    return null;
}

/**
 * T011 & T031: Parse processed text into reading view HTML with CEFR-colored, clickable words
 * Includes loading skeleton for large texts >500ms render time
 * @param {string} processedText - Full book text from analysis results
 * @param {Object} analysisResults - Analysis results containing words and phrasal verbs
 */
function parseTextForReading(processedText, analysisResults) {
    const readingContent = document.getElementById('reading-content');

    // DEBUG: Log to verify processed_text is available
    console.log('[DEBUG] parseTextForReading called');
    console.log('[DEBUG] processedText type:', typeof processedText);
    console.log('[DEBUG] processedText length:', processedText ? processedText.length : 0);
    console.log('[DEBUG] processedText preview:', processedText ? processedText.substring(0, 100) : 'null/undefined');

    // T031: Show loading skeleton for large texts
    const startTime = performance.now();
    const showSkeletonTimeout = setTimeout(() => {
        readingContent.innerHTML = '<div class="reading-skeleton"></div>';
    }, 500); // Show skeleton if render takes >500ms

    // Validate inputs
    if (!processedText || processedText.trim().length === 0) {
        readingContent.innerHTML = `
            <div style="text-align: center; padding: 4rem 2rem; color: #6b7280;">
                <p class="bilingual">
                    <span class="cn">暂无文本</span>
                    <span class="en">No text available</span>
                </p>
            </div>
        `;
        return;
    }

    if (!analysisResults || !analysisResults.words) {
        console.error('Invalid analysisResults');
        readingContent.innerHTML = `
            <div style="text-align: center; padding: 4rem 2rem; color: #6b7280;">
                <p class="bilingual">
                    <span class="cn">暂无文本</span>
                    <span class="en">No text available</span>
                </p>
            </div>
        `;
        return;
    }

    // Build word lookup map for O(1) access
    // Include both lemmatized form AND all original forms (running → run, etc.)
    const wordLookupMap = new Map();

    analysisResults.words?.forEach(word => {
        const wordEntry = {
            ...word,
            type: 'word'
        };

        // Add lemmatized form (e.g., "run")
        wordLookupMap.set(word.word.toLowerCase(), wordEntry);

        // Add all original forms (e.g., "running", "runs", "ran")
        if (word.original_forms && Array.isArray(word.original_forms)) {
            word.original_forms.forEach(form => {
                wordLookupMap.set(form.toLowerCase(), wordEntry);
            });
        }
    });

    analysisResults.phrasal_verbs?.forEach(pv => {
        wordLookupMap.set(pv.phrase.toLowerCase(), {
            ...pv,
            word: pv.phrase,
            type: 'phrasal_verb'
        });
    });

    // DEBUG: Check word data structure and coverage
    if (wordLookupMap.size > 0) {
        const firstWord = Array.from(wordLookupMap.values())[0];
        console.log('[DEBUG] Sample word data:', firstWord);
        console.log('[DEBUG] Total lookup entries (includes all word forms):', wordLookupMap.size);
        console.log('[DEBUG] Unique words:', analysisResults.words?.length || 0);
    }

    // Get current filter state
    const activeLevel = document.querySelector('.filter-btn.active')?.getAttribute('data-level') || 'all';
    const searchTerm = document.getElementById('word-search')?.value.toLowerCase() || '';

    // Split text into paragraphs with improved logic
    // Try double newline first, then fall back to single newline if no double newlines found
    let paragraphs = processedText.split('\n\n').filter(p => p.trim().length > 0);

    // If no double-newline paragraphs, try single newline
    if (paragraphs.length <= 1) {
        paragraphs = processedText.split('\n').filter(p => p.trim().length > 0);
    }

    // Process each paragraph
    let html = '';

    paragraphs.forEach((para, index) => {
        // Skip very short lines (likely titles or page numbers)
        if (para.trim().length < 3) {
            return;
        }

        // Split paragraph into tokens (words and punctuation)
        const tokens = para.split(/(\s+|[.,;:!?—\-\[\](){}'""])/);

        let paraHTML = '<p class="reading-paragraph">';

        tokens.forEach(token => {
            if (!token || token.trim().length === 0) {
                paraHTML += token;
                return;
            }

            // Check if token is a word (not punctuation or whitespace)
            const isWord = /^[a-zA-Z'-]+$/.test(token);

            if (!isWord) {
                paraHTML += token;
                return;
            }

            // Look up word data
            const wordData = wordLookupMap.get(token.toLowerCase());

            if (wordData) {
                // DEBUG: Log first few words to verify data-level
                if (Math.random() < 0.001) { // Log ~0.1% of words to avoid console spam
                    console.log('[DEBUG] Word:', token, 'Level:', wordData.cefr_level || wordData.level, 'Data:', wordData);
                }

                // Check if word matches filter
                const level = wordData.cefr_level || wordData.level; // Try both field names
                const matchesFilter = activeLevel === 'all' || level === activeLevel;

                // Check if word matches search
                const matchesSearch = !searchTerm || token.toLowerCase().includes(searchTerm);

                if (matchesFilter) {
                    const searchClass = matchesSearch && searchTerm ? ' search-match' : '';
                    paraHTML += `<span class="cefr-word${searchClass}" data-word="${wordData.word}" data-level="${level}" onclick="handleWordClick('${wordData.word}')">${token}</span>`;
                } else {
                    // Word exists but filtered out - show as plain text
                    paraHTML += token;
                }
            } else {
                // Word not in analysis - show as plain text
                paraHTML += token;
            }
        });

        paraHTML += '</p>';
        html += paraHTML;
    });

    // Clear skeleton timeout and render content
    clearTimeout(showSkeletonTimeout);
    readingContent.innerHTML = html;

    // T029: Performance logging for optimization
    const renderTime = performance.now() - startTime;
    console.log(`[Reading View] Rendered ${paragraphs.length} paragraphs in ${renderTime.toFixed(2)}ms`);
}

/**
 * T015: Update reading view when filters or search change
 */
function updateReadingView() {
    if (!window.currentAnalysisResults || !window.currentAnalysisResults.processed_text) {
        return;
    }

    const readingPanel = document.getElementById('reading-panel');
    if (readingPanel && !readingPanel.hasAttribute('hidden')) {
        // Reading view is active - re-render with current filters
        parseTextForReading(window.currentAnalysisResults.processed_text, window.currentAnalysisResults);
    }
}

/**
 * T016: Handle word click in reading view
 * @param {string} word - Word that was clicked
 */
function handleWordClick(word) {
    if (!window.currentAnalysisResults) {
        console.error('No analysis results available');
        return;
    }

    // Find word data using the findWordData helper
    const wordData = findWordData(word, window.currentAnalysisResults);

    if (wordData) {
        // Call existing showWordDetails function (Feature 004)
        showWordDetails(wordData);
    } else {
        console.warn(`Word "${word}" not found in analysis results`);
    }
}

/**
 * T013: Initialize reading view
 * Note: Main tab switching is now handled by initMainTabNavigation() and switchMainTab()
 */
function initReadingView() {
    // T020: Add Escape key listener for modal (Feature 005 enhancement)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const modal = document.getElementById('word-modal');
            if (modal && !modal.classList.contains('hidden')) {
                closeModalWithFocusReturn();
            }
        }
    });
}

// ========================================
// Text Input Mode Functionality
// ========================================

/**
 * Switch between file upload and text input modes
 */
function switchInputMode(mode) {
    const fileForm = document.getElementById('upload-form');
    const textForm = document.getElementById('text-form');
    const fileModeBtn = document.getElementById('file-mode-btn');
    const textModeBtn = document.getElementById('text-mode-btn');

    if (mode === 'file') {
        // Show file upload, hide text input
        fileForm.classList.add('active');
        textForm.classList.remove('active');
        fileModeBtn.classList.add('active');
        textModeBtn.classList.remove('active');
    } else if (mode === 'text') {
        // Show text input, hide file upload
        fileForm.classList.remove('active');
        textForm.classList.add('active');
        fileModeBtn.classList.remove('active');
        textModeBtn.classList.add('active');
    }
}

/**
 * Update character count for text input
 */
function updateCharCount() {
    const text = textInput.value;
    const count = text.length;
    charCount.textContent = count.toLocaleString();

    // Optional: warn when approaching limit
    if (count > 900000) {
        charCount.style.color = 'var(--error-color, #ef4444)';
    } else {
        charCount.style.color = 'var(--text-primary)';
    }
}

/**
 * Handle text form submission
 */
async function handleTextSubmit(e) {
    e.preventDefault();

    const text = textInput.value.trim();

    if (!text) {
        showError('Please enter some text to analyze / 请输入要分析的文本');
        return;
    }

    if (text.length < 50) {
        showError('Text is too short (minimum 50 characters) / 文本太短（最少50个字符）');
        return;
    }

    try {
        // Show progress section
        showSection('progress');

        // Send text to backend
        const response = await fetch('/analyze-text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                source_name: 'Pasted Text'
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Analysis failed');
        }

        const data = await response.json();
        currentSessionId = data.session_id;

        // Start listening for progress updates
        listenForProgress(currentSessionId);

    } catch (error) {
        console.error('Error analyzing text:', error);
        showError(error.message || 'Failed to analyze text / 文本分析失败');
    }
}

// Event Listeners for Text Input Mode

// Mode toggle buttons
if (fileModeBtn) {
    fileModeBtn.addEventListener('click', () => switchInputMode('file'));
}

if (textModeBtn) {
    textModeBtn.addEventListener('click', () => switchInputMode('text'));
}

// Character count
if (textInput) {
    textInput.addEventListener('input', updateCharCount);
}

// Text form submission
if (textForm) {
    textForm.addEventListener('submit', handleTextSubmit);
}

// ========================================
// History Functionality
// ========================================

/**
 * Open history modal and load history entries
 */
async function openHistoryModal() {
    const historyModal = document.getElementById('history-modal');
    const historyList = document.getElementById('history-list');

    if (!historyModal || !historyList) {
        console.error('History modal elements not found');
        return;
    }

    // Show modal
    historyModal.classList.remove('hidden');

    // Show loading state
    historyList.innerHTML = '<div class="history-loading bilingual"><span class="en">Loading history...</span><span class="cn">加载历史记录中...</span></div>';

    try {
        // Fetch history from API
        const response = await fetch('/api/history');
        if (!response.ok) {
            throw new Error('Failed to load history');
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to load history');
        }

        // Display history entries
        displayHistoryEntries(data.entries);

    } catch (error) {
        console.error('Error loading history:', error);
        historyList.innerHTML = `
            <div class="history-error bilingual">
                <span class="en">❌ Failed to load history</span>
                <span class="cn">加载历史记录失败</span>
            </div>
        `;
    }
}

/**
 * Display history entries in the modal
 */
function displayHistoryEntries(entries) {
    const historyList = document.getElementById('history-list');

    if (!entries || entries.length === 0) {
        historyList.innerHTML = `
            <div class="history-empty bilingual">
                <span class="en">📭 No analysis history yet</span>
                <span class="cn">暂无分析历史</span>
            </div>
        `;
        return;
    }

    // Create history items HTML
    let html = '';
    entries.forEach((entry) => {
        const date = new Date(entry.timestamp);
        const dateStr = date.toLocaleString();
        const dateStrCn = date.toLocaleString('zh-CN');

        html += `
            <div class="history-item" data-id="${entry.id}">
                <div class="history-item-header">
                    <div class="history-item-title">
                        <span class="history-item-id">#${entry.id}</span>
                        <span class="history-item-filename">${escapeHtml(entry.filename)}</span>
                    </div>
                    <button class="history-item-delete" data-id="${entry.id}" title="Delete / 删除">
                        🗑️
                    </button>
                </div>
                <div class="history-item-info">
                    <div class="history-item-date bilingual">
                        <span class="en">📅 ${dateStr}</span>
                        <span class="cn">${dateStrCn}</span>
                    </div>
                    <div class="history-item-stats bilingual">
                        <span class="en">📊 ${entry.total_unique_words.toLocaleString()} unique words (${entry.total_words.toLocaleString()} total)</span>
                        <span class="cn">${entry.total_unique_words.toLocaleString()} 个不同单词（共 ${entry.total_words.toLocaleString()} 个）</span>
                    </div>
                </div>
                <button class="history-item-load btn btn-primary bilingual" data-id="${entry.id}">
                    <span class="en">📂 Load Analysis</span>
                    <span class="cn">加载分析</span>
                </button>
            </div>
        `;
    });

    historyList.innerHTML = html;

    // Add event listeners for load buttons
    historyList.querySelectorAll('.history-item-load').forEach((btn) => {
        btn.addEventListener('click', async (e) => {
            const analysisId = parseInt(e.currentTarget.getAttribute('data-id'));
            await loadHistoryAnalysis(analysisId);
        });
    });

    // Add event listeners for delete buttons
    historyList.querySelectorAll('.history-item-delete').forEach((btn) => {
        btn.addEventListener('click', async (e) => {
            e.stopPropagation();
            const analysisId = parseInt(e.currentTarget.getAttribute('data-id'));
            await deleteHistoryAnalysis(analysisId);
        });
    });
}

/**
 * Load a specific analysis from history
 */
async function loadHistoryAnalysis(analysisId) {
    const historyModal = document.getElementById('history-modal');

    try {
        // Show loading state
        showSection('progress');
        closeHistoryModal();
        updateProgress(0, 'Loading analysis from history... / 从历史记录加载分析...');

        // Fetch analysis from API
        const response = await fetch(`/api/history/${analysisId}`);
        if (!response.ok) {
            throw new Error('Failed to load analysis');
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to load analysis');
        }

        // Process and display the analysis
        const analysis = data.analysis;

        // Convert the stored analysis format to match the expected format
        const processedAnalysis = {
            words: analysis.words,
            phrases: analysis.phrases,
            statistics: analysis.statistics,
            processed_text: analysis.processed_text,
            source_file: analysis.source_file || analysis.filename,
            analysis_date: analysis.analysis_date || analysis.timestamp
        };

        // Store in global state
        window.currentAnalysisResults = processedAnalysis;
        analysisResults = processedAnalysis;

        // Update progress to complete
        updateProgress(100, 'Analysis loaded / 分析已加载');

        // Display results
        setTimeout(() => {
            displayAnalysisResults(processedAnalysis);
            showSection('results');
        }, 500);

    } catch (error) {
        console.error('Error loading analysis:', error);
        showError(`Failed to load analysis: ${error.message} / 加载分析失败`);
    }
}

/**
 * Delete a specific analysis from history
 */
async function deleteHistoryAnalysis(analysisId) {
    // Confirm deletion
    const confirmMessage = getCurrentLanguage() === 'en'
        ? 'Are you sure you want to delete this analysis?'
        : '确定要删除此分析记录吗？';

    if (!confirm(confirmMessage)) {
        return;
    }

    try {
        // Delete via API
        const response = await fetch(`/api/history/${analysisId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete analysis');
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.error || 'Failed to delete analysis');
        }

        // Reload history list
        await openHistoryModal();

    } catch (error) {
        console.error('Error deleting analysis:', error);
        alert(`Failed to delete analysis: ${error.message}`);
    }
}

/**
 * Close history modal
 */
function closeHistoryModal() {
    const historyModal = document.getElementById('history-modal');
    if (historyModal) {
        historyModal.classList.add('hidden');
    }
}

/**
 * Helper function to get current language
 */
function getCurrentLanguage() {
    return document.documentElement.getAttribute('data-lang') || 'en';
}

/**
 * Helper function to escape HTML
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event Listeners for History

// History button
const historyBtn = document.getElementById('history-btn');
if (historyBtn) {
    historyBtn.addEventListener('click', openHistoryModal);
}

// History modal close button
const historyModalClose = document.getElementById('history-modal-close');
if (historyModalClose) {
    historyModalClose.addEventListener('click', closeHistoryModal);
}

// Close modal when clicking outside
const historyModal = document.getElementById('history-modal');
if (historyModal) {
    historyModal.addEventListener('click', (e) => {
        if (e.target === historyModal) {
            closeHistoryModal();
        }
    });
}
