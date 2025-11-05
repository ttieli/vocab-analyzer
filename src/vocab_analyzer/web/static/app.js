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

// Display statistics summary (T044)
function displayStatistics(results) {
    const statsDiv = document.getElementById('stats-summary');

    const stats = results.statistics || {};
    const totalWords = stats.total_word_occurrences || 0;
    const uniqueWords = stats.total_unique_words || 0;
    const totalPhrases = stats.total_unique_phrases || 0;

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
                    <div class="stat-bar-fill" style="width: ${percentage}%"></div>
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
        <div class="cefr-distribution">
            <h4>CEFR Distribution</h4>
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

    // CEFR level colors
    const cefrColors = {
        'A1': '#4CAF50',
        'A2': '#8BC34A',
        'B1': '#FFC107',
        'B2': '#FF9800',
        'C1': '#FF5722',
        'C2': '#F44336',
        'C2+': '#9C27B0'
    };

    // Render words (Feature 004: T008, T009 - Entire card clickable, no translate button)
    wordList.innerHTML = filteredWords.slice(0, 200).map(word => {
        const levelColor = cefrColors[word.level] || '#757575';
        return `
            <div class="word-item word-card"
                 data-word='${JSON.stringify(word)}'
                 tabindex="0"
                 role="button"
                 aria-label="View details for '${word.word}'">
                <div class="word-text">${word.word}</div>
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

    // Feature 004: Initialize tab navigation and keyboard controls after rendering
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

// Download result in specified format
function downloadResult(format) {
    if (!currentSessionId) {
        showError('No analysis session found');
        return;
    }

    // Trigger download by navigating to download URL
    window.location.href = `/download/${currentSessionId}/${format}`;
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
// FEATURE 004: T018 - Tab Switching Logic
// ===================================================================

/**
 * Initialize tab navigation system
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
    const wordLookupMap = new Map();

    analysisResults.words?.forEach(word => {
        wordLookupMap.set(word.word.toLowerCase(), {
            ...word,
            type: 'word'
        });
    });

    analysisResults.phrasal_verbs?.forEach(pv => {
        wordLookupMap.set(pv.phrase.toLowerCase(), {
            ...pv,
            word: pv.phrase,
            type: 'phrasal_verb'
        });
    });

    // Get current filter state
    const activeLevel = document.querySelector('.filter-btn.active')?.getAttribute('data-level') || 'all';
    const searchTerm = document.getElementById('word-search')?.value.toLowerCase() || '';

    // Split text into paragraphs
    const paragraphs = processedText.split('\n\n').filter(p => p.trim().length > 0);

    // Process each paragraph
    let html = '';

    paragraphs.forEach(para => {
        // Split paragraph into tokens (words and punctuation)
        const tokens = para.split(/(\s+|[.,;:!?—\-\[\](){}'""])/);

        let paraHTML = '<p>';

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
                // Check if word matches filter
                const matchesFilter = activeLevel === 'all' || wordData.cefr_level === activeLevel;

                // Check if word matches search
                const matchesSearch = !searchTerm || token.toLowerCase().includes(searchTerm);

                if (matchesFilter) {
                    const searchClass = matchesSearch && searchTerm ? ' search-match' : '';
                    paraHTML += `<span class="cefr-word${searchClass}" data-word="${wordData.word}" data-level="${wordData.cefr_level}" onclick="handleWordClick('${wordData.word}')">${token}</span>`;
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
 * T013: Initialize reading view tab
 */
function initReadingView() {
    const readingTab = document.getElementById('reading-tab');

    if (readingTab) {
        readingTab.addEventListener('click', () => {
            if (window.currentAnalysisResults && window.currentAnalysisResults.processed_text) {
                parseTextForReading(window.currentAnalysisResults.processed_text, window.currentAnalysisResults);
            }
        });
    }

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
