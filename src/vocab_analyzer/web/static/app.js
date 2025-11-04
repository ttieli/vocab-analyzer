// Vocabulary Analyzer Web Interface - Main JavaScript

let currentSessionId = null;
let analysisResults = null;  // Store full analysis results
let currentFilter = 'all';  // Current CEFR level filter
let searchTerm = '';  // Current search term

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
        updateProgress(data.progress, formatStageName(data.stage));
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

    // Render words
    wordList.innerHTML = filteredWords.slice(0, 200).map(word => `
        <div class="word-item" data-word='${JSON.stringify(word)}'>
            <div class="word-text">${word.word}</div>
            <div class="word-level">${word.level}</div>
        </div>
    `).join('');

    // Render phrases
    phraseList.innerHTML = filteredPhrases.slice(0, 100).map(phrase => `
        <div class="word-item" data-word='${JSON.stringify(phrase)}'>
            <div class="word-text">${phrase.phrase}</div>
            <div class="word-level">${phrase.level}</div>
        </div>
    `).join('');

    // Add click handlers for word details (T041)
    document.querySelectorAll('.word-item').forEach(item => {
        item.addEventListener('click', () => {
            const wordData = JSON.parse(item.getAttribute('data-word'));
            showWordDetails(wordData);
        });
    });
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
        });
    });

    // Search input with debounce
    let searchTimeout;
    wordSearch.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            searchTerm = e.target.value;
            updateWordDisplay();
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
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Chinese Translation (中文释义)</div>
                <div class="detail-value">${wordData.definition_cn}</div>
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
        const examples = wordData.examples.slice(0, 3).map(ex => `<li>${ex}</li>`).join('');
        detailsHTML += `
            <div class="detail-row">
                <div class="detail-label">Example Sentences</div>
                <div class="detail-value">
                    <ul style="margin-top: 0.5rem; padding-left: 1.5rem;">
                        ${examples}
                    </ul>
                </div>
            </div>
        `;
    }

    modalDetails.innerHTML = detailsHTML;
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
    errorText.textContent = message;
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
