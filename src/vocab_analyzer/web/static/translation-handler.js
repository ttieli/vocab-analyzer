// Translation Handler
// Handles translation button clicks and API calls

/**
 * Translation cache
 * Stores translated text to avoid repeated API calls
 */
const translationCache = new Map();

/**
 * Translate text using the translation API
 * @param {string} sourceText - Text to translate
 * @param {string} translationType - Type: 'word', 'phrase', or 'sentence'
 * @returns {Promise<Object>} Translation result
 */
async function translateText(sourceText, translationType = 'word') {
    // Check cache first
    const cacheKey = `${sourceText}:${translationType}`;
    if (translationCache.has(cacheKey)) {
        return translationCache.get(cacheKey);
    }

    try {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                source_text: sourceText,
                translation_type: translationType
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'Translation failed');
        }

        // Cache the result
        translationCache.set(cacheKey, data);

        return data;
    } catch (error) {
        console.error('Translation error:', error);
        throw error;
    }
}

/**
 * Show translation result in a tooltip or inline display
 * @param {HTMLElement} element - Element to show translation near
 * @param {Object} translationData - Translation result from API
 */
function showTranslationResult(element, translationData) {
    // Remove any existing translation tooltip
    hideTranslationResult();

    const tooltip = document.createElement('div');
    tooltip.id = 'translation-tooltip';
    tooltip.className = 'translation-tooltip';

    const { translation, source, confidence_score, cached } = translationData;

    tooltip.innerHTML = `
        <div class="translation-content">
            <div class="translation-text">${translation}</div>
            <div class="translation-meta">
                <span class="translation-source">${getSourceLabel(source)}</span>
                ${confidence_score ? `<span class="translation-confidence">${(confidence_score * 100).toFixed(0)}%</span>` : ''}
                ${cached ? '<span class="translation-cached">cached</span>' : ''}
            </div>
        </div>
        <button class="translation-close">&times;</button>
    `;

    // Position tooltip near element
    document.body.appendChild(tooltip);
    positionTooltip(tooltip, element);

    // Add close handler
    tooltip.querySelector('.translation-close').addEventListener('click', hideTranslationResult);

    // Auto-hide after 10 seconds
    setTimeout(hideTranslationResult, 10000);
}

/**
 * Hide translation tooltip
 */
function hideTranslationResult() {
    const tooltip = document.getElementById('translation-tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

/**
 * Position tooltip near target element
 * @param {HTMLElement} tooltip - Tooltip element
 * @param {HTMLElement} target - Target element
 */
function positionTooltip(tooltip, target) {
    const rect = target.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();

    // Position below target by default
    let top = rect.bottom + window.scrollY + 8;
    let left = rect.left + window.scrollX;

    // Ensure tooltip doesn't go off screen
    if (left + tooltipRect.width > window.innerWidth) {
        left = window.innerWidth - tooltipRect.width - 16;
    }

    if (top + tooltipRect.height > window.innerHeight + window.scrollY) {
        // Position above if no space below
        top = rect.top + window.scrollY - tooltipRect.height - 8;
    }

    tooltip.style.top = `${top}px`;
    tooltip.style.left = `${left}px`;
}

/**
 * Get human-readable label for translation source
 * @param {string} source - Source identifier
 * @returns {string} Display label
 */
function getSourceLabel(source) {
    const labels = {
        'ecdict': 'ECDICT',
        'mdict': 'Mdict',
        'argos': 'Argos Translate',
        'cached': 'Cache'
    };
    return labels[source] || source;
}

/**
 * Add translate button to word element
 * @param {HTMLElement} wordElement - Word item element
 * @returns {HTMLElement} Translate button
 */
function addTranslateButton(wordElement) {
    // Check if button already exists
    if (wordElement.querySelector('.translate-btn')) {
        return wordElement.querySelector('.translate-btn');
    }

    const btn = document.createElement('button');
    btn.className = 'translate-btn';
    btn.innerHTML = '翻';
    btn.title = 'Translate / 翻译';

    btn.addEventListener('click', async (e) => {
        e.stopPropagation();

        // Get word data
        const wordData = JSON.parse(wordElement.getAttribute('data-word'));
        const text = wordData.word || wordData.phrase;
        const type = wordData.phrase ? 'phrase' : 'word';

        // Check if already has translation in data
        if (wordData.definition_cn) {
            showTranslationResult(btn, {
                translation: wordData.definition_cn,
                source: 'cached',
                cached: true,
                confidence_score: 1.0
            });
            return;
        }

        // Show loading state
        btn.classList.add('loading');
        btn.disabled = true;

        try {
            const result = await translateText(text, type);
            showTranslationResult(btn, result);
        } catch (error) {
            // Show error message
            showTranslationError(btn, error.message);
        } finally {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    });

    wordElement.appendChild(btn);
    return btn;
}

/**
 * Show translation error
 * @param {HTMLElement} element - Element to show error near
 * @param {string} errorMessage - Error message
 */
function showTranslationError(element, errorMessage) {
    hideTranslationResult();

    const tooltip = document.createElement('div');
    tooltip.id = 'translation-tooltip';
    tooltip.className = 'translation-tooltip translation-error';

    tooltip.innerHTML = `
        <div class="translation-content">
            <div class="error-icon">⚠️</div>
            <div class="bilingual">
                <span class="en">Translation failed</span>
                <span class="cn">翻译失败</span>
            </div>
            <div class="error-detail">${errorMessage}</div>
        </div>
        <button class="translation-close">&times;</button>
    `;

    document.body.appendChild(tooltip);
    positionTooltip(tooltip, element);

    tooltip.querySelector('.translation-close').addEventListener('click', hideTranslationResult);

    // Auto-hide after 5 seconds
    setTimeout(hideTranslationResult, 5000);
}

/**
 * Initialize translation handlers
 * Attaches translate buttons to word items
 */
function initTranslationHandlers() {
    // Attach handlers to existing word items
    attachTranslateButtons();

    // Use MutationObserver to handle dynamically added word items
    const observer = new MutationObserver(() => {
        attachTranslateButtons();
    });

    const wordList = document.getElementById('word-list');
    const phraseList = document.getElementById('phrase-list');

    if (wordList) {
        observer.observe(wordList, {
            childList: true,
            subtree: true
        });
    }

    if (phraseList) {
        observer.observe(phraseList, {
            childList: true,
            subtree: true
        });
    }

    // Hide tooltip when clicking outside
    document.addEventListener('click', (e) => {
        const tooltip = document.getElementById('translation-tooltip');
        if (tooltip && !tooltip.contains(e.target) && !e.target.classList.contains('translate-btn')) {
            hideTranslationResult();
        }
    });
}

/**
 * Attach translate buttons to all word items
 */
function attachTranslateButtons() {
    document.querySelectorAll('.word-item:not([data-translate-btn])').forEach(item => {
        addTranslateButton(item);
        item.setAttribute('data-translate-btn', 'true');
    });
}

/**
 * Bulk translate words in current view
 * @param {Array} wordElements - Array of word item elements
 */
async function bulkTranslate(wordElements) {
    const promises = wordElements.map(async (element) => {
        const wordData = JSON.parse(element.getAttribute('data-word'));
        const text = wordData.word || wordData.phrase;
        const type = wordData.phrase ? 'phrase' : 'word';

        if (wordData.definition_cn) {
            return; // Skip if already has translation
        }

        try {
            const result = await translateText(text, type);
            // Store translation in word data
            wordData.definition_cn = result.translation;
            element.setAttribute('data-word', JSON.stringify(wordData));
        } catch (error) {
            console.error(`Failed to translate ${text}:`, error);
        }
    });

    await Promise.all(promises);
}

// Note: Translation handlers are now initialized directly in app.js
// This ensures proper timing with dynamic word list rendering
// The functions (translateText, showTranslationResult, etc.) are still available globally

// Export functions for browser environment (attach to window)
if (typeof window !== 'undefined') {
    window.translateText = translateText;
    window.showTranslationResult = showTranslationResult;
    window.hideTranslationResult = hideTranslationResult;
    window.showTranslationError = showTranslationError;
    window.addTranslateButton = addTranslateButton;
    window.initTranslationHandlers = initTranslationHandlers;
    window.bulkTranslate = bulkTranslate;
}

// Export functions for Node.js environment (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        translateText,
        showTranslationResult,
        hideTranslationResult,
        showTranslationError,
        addTranslateButton,
        initTranslationHandlers,
        bulkTranslate
    };
}
