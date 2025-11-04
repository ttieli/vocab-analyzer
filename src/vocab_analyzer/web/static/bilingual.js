// Bilingual UI Utilities
// Provides helper functions for creating and managing bilingual text elements

/**
 * UI Strings cache
 * Loaded from /api/ui/strings endpoint
 */
let uiStrings = null;

/**
 * Load UI strings from API
 * @returns {Promise<Object>} UI strings object
 */
async function loadUIStrings() {
    if (uiStrings !== null) {
        return uiStrings;
    }

    try {
        const response = await fetch('/api/ui/strings');
        if (!response.ok) {
            throw new Error('Failed to load UI strings');
        }
        const data = await response.json();
        uiStrings = data.strings;
        return uiStrings;
    } catch (error) {
        console.error('Error loading UI strings:', error);
        // Return empty object as fallback
        uiStrings = {};
        return uiStrings;
    }
}

/**
 * Get bilingual string by key
 * @param {string} key - String key (e.g., 'buttons.analyze')
 * @returns {Object} Object with text_en and text_cn properties
 */
function getString(key) {
    if (!uiStrings || !uiStrings[key]) {
        console.warn(`Missing UI string: ${key}`);
        return { text_en: key, text_cn: key };
    }
    return uiStrings[key];
}

/**
 * Create a bilingual text element
 * @param {string} textEn - English text
 * @param {string} textCn - Chinese text
 * @param {string} tag - HTML tag name (default: 'span')
 * @param {string} className - Additional CSS classes
 * @returns {HTMLElement} DOM element with bilingual structure
 *
 * @example
 * const elem = createBilingualText('Analyze', '分析', 'button', 'btn btn-primary');
 * document.body.appendChild(elem);
 */
function createBilingualText(textEn, textCn, tag = 'span', className = '') {
    const element = document.createElement(tag);
    element.className = `bilingual ${className}`.trim();

    const enSpan = document.createElement('span');
    enSpan.className = 'en';
    enSpan.textContent = textEn;

    const cnSpan = document.createElement('span');
    cnSpan.className = 'cn';
    cnSpan.textContent = textCn;

    element.appendChild(enSpan);
    element.appendChild(cnSpan);

    return element;
}

/**
 * Update existing bilingual element's text
 * @param {HTMLElement} element - Element with .bilingual class
 * @param {string} textEn - New English text
 * @param {string} textCn - New Chinese text
 */
function updateBilingualText(element, textEn, textCn) {
    const enSpan = element.querySelector('.en');
    const cnSpan = element.querySelector('.cn');

    if (enSpan) enSpan.textContent = textEn;
    if (cnSpan) cnSpan.textContent = textCn;
}

/**
 * Show bilingual error message
 * @param {string} errorKey - Error key from ui_strings.json (e.g., 'errors.upload_failed')
 * @param {string} fallbackEn - Fallback English message if key not found
 * @param {string} fallbackCn - Fallback Chinese message if key not found
 */
function showBilingualError(errorKey, fallbackEn = 'An error occurred', fallbackCn = '发生错误') {
    const errorString = getString(errorKey);
    const textEn = errorString.text_en || fallbackEn;
    const textCn = errorString.text_cn || fallbackCn;

    const errorText = document.getElementById('error-text');
    if (errorText) {
        // Clear existing content
        errorText.innerHTML = '';

        // Create bilingual error message
        const errorDiv = createBilingualText(textEn, textCn, 'div', 'error-message');
        errorText.appendChild(errorDiv);
    }
}

/**
 * Set bilingual loading state for an element
 * @param {HTMLElement} element - Button or element to update
 * @param {boolean} isLoading - Whether element is in loading state
 * @param {string} loadingKey - UI string key for loading text (e.g., 'loading.analyzing')
 */
function setBilingualLoading(element, isLoading, loadingKey = 'loading.analyzing') {
    if (isLoading) {
        element.disabled = true;
        element.setAttribute('data-original-content', element.innerHTML);

        const loadingString = getString(loadingKey);
        const textEn = loadingString.text_en || 'Loading...';
        const textCn = loadingString.text_cn || '加载中...';

        element.innerHTML = '';
        const enSpan = document.createElement('span');
        enSpan.className = 'en';
        enSpan.textContent = textEn;

        const cnSpan = document.createElement('span');
        cnSpan.className = 'cn';
        cnSpan.textContent = textCn;

        element.appendChild(enSpan);
        element.appendChild(cnSpan);

        // Add loading class for animation
        element.classList.add('loading');
    } else {
        element.disabled = false;
        const originalContent = element.getAttribute('data-original-content');
        if (originalContent) {
            element.innerHTML = originalContent;
            element.removeAttribute('data-original-content');
        }
        element.classList.remove('loading');
    }
}

/**
 * Initialize bilingual UI strings
 * Should be called when page loads
 */
async function initBilingualUI() {
    await loadUIStrings();
    console.log('Bilingual UI strings loaded');
}

/**
 * Create bilingual badge (for CEFR levels, tags, etc.)
 * @param {string} textEn - English text
 * @param {string} textCn - Chinese text
 * @param {string} variant - Badge style variant (primary, success, info, warning)
 * @returns {HTMLElement} Badge element
 */
function createBilingualBadge(textEn, textCn, variant = 'primary') {
    const badge = createBilingualText(textEn, textCn, 'span', `badge badge-${variant}`);
    return badge;
}

/**
 * Format stage name with bilingual support
 * @param {string} stage - Stage key (e.g., 'VALIDATING', 'EXTRACTING')
 * @returns {Object} Object with text_en and text_cn
 */
function formatBilingualStageName(stage) {
    const stageMap = {
        'VALIDATING': { text_en: 'Validating file...', text_cn: '验证文件...' },
        'EXTRACTING': { text_en: 'Extracting text...', text_cn: '提取文本...' },
        'TOKENIZING': { text_en: 'Tokenizing words...', text_cn: '分词...' },
        'DETECTING_PHRASES': { text_en: 'Detecting phrases...', text_cn: '检测短语...' },
        'MATCHING_LEVELS': { text_en: 'Matching CEFR levels...', text_cn: '匹配CEFR级别...' },
        'GENERATING_STATS': { text_en: 'Generating statistics...', text_cn: '生成统计...' },
        'COMPLETED': { text_en: 'Complete!', text_cn: '完成！' }
    };

    return stageMap[stage] || { text_en: stage, text_cn: stage };
}

/**
 * Update progress display with bilingual stage name
 * @param {number} percent - Progress percentage (0-100)
 * @param {string} stage - Stage key
 */
function updateBilingualProgress(percent, stage) {
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressStage = document.getElementById('progress-stage');

    if (progressFill) {
        progressFill.style.width = `${percent}%`;
    }

    if (progressPercent) {
        progressPercent.textContent = `${percent}%`;
    }

    if (progressStage) {
        const stageText = formatBilingualStageName(stage);
        progressStage.innerHTML = '';

        const enSpan = document.createElement('span');
        enSpan.className = 'en';
        enSpan.textContent = stageText.text_en;

        const cnSpan = document.createElement('span');
        cnSpan.className = 'cn';
        cnSpan.textContent = stageText.text_cn;

        progressStage.appendChild(enSpan);
        progressStage.appendChild(cnSpan);
    }
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadUIStrings,
        getString,
        createBilingualText,
        updateBilingualText,
        showBilingualError,
        setBilingualLoading,
        initBilingualUI,
        createBilingualBadge,
        formatBilingualStageName,
        updateBilingualProgress
    };
}
