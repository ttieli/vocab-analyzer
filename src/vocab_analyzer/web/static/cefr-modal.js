// CEFR Modal Handler
// Displays educational content about CEFR levels in a modal dialog

/**
 * CEFR definitions cache
 * Loaded from /api/cefr endpoint
 */
let cefrDefinitions = null;

/**
 * Load all CEFR definitions from API
 * @returns {Promise<Object>} CEFR definitions object
 */
async function loadCEFRDefinitions() {
    if (cefrDefinitions !== null) {
        return cefrDefinitions;
    }

    try {
        const response = await fetch('/api/cefr');
        if (!response.ok) {
            throw new Error('Failed to load CEFR definitions');
        }
        const data = await response.json();
        cefrDefinitions = data.levels;
        return cefrDefinitions;
    } catch (error) {
        console.error('Error loading CEFR definitions:', error);
        cefrDefinitions = {};
        return cefrDefinitions;
    }
}

/**
 * Get CEFR level definition by level code
 * @param {string} levelCode - Level code (A1, A2, B1, B2, C1, C2, C2+)
 * @returns {Promise<Object>} Level definition object
 */
async function getCEFRLevel(levelCode) {
    // Try cache first
    if (cefrDefinitions && cefrDefinitions[levelCode]) {
        return cefrDefinitions[levelCode];
    }

    // Fetch from API
    try {
        const response = await fetch(`/api/cefr/${levelCode}`);
        if (!response.ok) {
            throw new Error(`Failed to load CEFR level ${levelCode}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error loading CEFR level ${levelCode}:`, error);
        return null;
    }
}

/**
 * Show CEFR modal with level details
 * @param {string} levelCode - Level code (A1, A2, B1, B2, C1, C2, C2+)
 */
async function showCEFRModal(levelCode) {
    // Get or create modal element
    let modal = document.getElementById('cefr-modal');

    if (!modal) {
        modal = createCEFRModal();
        document.body.appendChild(modal);
    }

    // Show loading state
    const modalContent = modal.querySelector('.cefr-modal-content');
    modalContent.innerHTML = '<div class="loading-spinner">Loading...</div>';
    modal.classList.remove('hidden');

    // Fetch level data
    const levelData = await getCEFRLevel(levelCode);

    if (!levelData) {
        modalContent.innerHTML = `
            <div class="error-message">
                <p class="en">Failed to load CEFR level information</p>
                <p class="cn">无法加载 CEFR 级别信息</p>
            </div>
        `;
        return;
    }

    // Render level details
    renderCEFRLevel(modalContent, levelData);
}

/**
 * Create CEFR modal element
 * @returns {HTMLElement} Modal element
 */
function createCEFRModal() {
    const modal = document.createElement('div');
    modal.id = 'cefr-modal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-overlay"></div>
        <div class="modal-dialog cefr-modal-dialog">
            <div class="modal-header">
                <h3 id="cefr-modal-title" class="bilingual">
                    <span class="en">CEFR Level Information</span>
                    <span class="cn">CEFR 级别信息</span>
                </h3>
                <button class="modal-close" id="cefr-modal-close">&times;</button>
            </div>
            <div class="modal-body">
                <div class="cefr-modal-content"></div>
            </div>
        </div>
    `;

    // Add close handlers
    const closeBtn = modal.querySelector('#cefr-modal-close');
    const overlay = modal.querySelector('.modal-overlay');

    closeBtn.addEventListener('click', () => hideCEFRModal());
    overlay.addEventListener('click', () => hideCEFRModal());

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            hideCEFRModal();
        }
    });

    return modal;
}

/**
 * Hide CEFR modal
 */
function hideCEFRModal() {
    const modal = document.getElementById('cefr-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/**
 * Render CEFR level details in modal content
 * @param {HTMLElement} container - Container element
 * @param {Object} levelData - Level data from API
 */
function renderCEFRLevel(container, levelData) {
    const {
        level_code,
        name_en,
        name_cn,
        short_description_en,
        short_description_cn,
        description_en,
        description_cn,
        vocabulary_size,
        example_words,
        learning_context_en,
        learning_context_cn
    } = levelData;

    // Get level color
    const levelColor = getCEFRLevelColor(level_code);

    container.innerHTML = `
        <div class="cefr-level-header">
            <div class="cefr-level-badge" style="background-color: ${levelColor}">
                ${level_code}
            </div>
            <div class="cefr-level-name bilingual">
                <span class="en">${name_en}</span>
                <span class="cn">${name_cn}</span>
            </div>
        </div>

        <div class="cefr-section">
            <h4 class="bilingual">
                <span class="en">Quick Description</span>
                <span class="cn">简要描述</span>
            </h4>
            <p class="bilingual">
                <span class="en">${short_description_en}</span>
                <span class="cn">${short_description_cn}</span>
            </p>
        </div>

        <div class="cefr-section">
            <h4 class="bilingual">
                <span class="en">Full Description</span>
                <span class="cn">详细描述</span>
            </h4>
            <p class="bilingual">
                <span class="en">${description_en}</span>
                <span class="cn">${description_cn}</span>
            </p>
        </div>

        <div class="cefr-stats-grid">
            <div class="cefr-stat-item">
                <div class="stat-label bilingual">
                    <span class="en">Vocabulary Size</span>
                    <span class="cn">词汇量</span>
                </div>
                <div class="stat-value">${vocabulary_size}</div>
            </div>

            <div class="cefr-stat-item">
                <div class="stat-label bilingual">
                    <span class="en">Learning Context</span>
                    <span class="cn">学习背景</span>
                </div>
                <div class="stat-value bilingual">
                    <span class="en">${learning_context_en}</span>
                    <span class="cn">${learning_context_cn}</span>
                </div>
            </div>
        </div>

        ${example_words && example_words.length > 0 ? `
            <div class="cefr-section">
                <h4 class="bilingual">
                    <span class="en">Example Words</span>
                    <span class="cn">示例单词</span>
                </h4>
                <div class="example-words">
                    ${example_words.map(word => `<span class="example-word">${word}</span>`).join('')}
                </div>
            </div>
        ` : ''}
    `;
}

/**
 * Get color for CEFR level
 * @param {string} level - Level code
 * @returns {string} Hex color code
 */
function getCEFRLevelColor(level) {
    const colors = {
        'A1': '#4CAF50',  // Green
        'A2': '#8BC34A',  // Light Green
        'B1': '#FFC107',  // Amber
        'B2': '#FF9800',  // Orange
        'C1': '#FF5722',  // Deep Orange
        'C2': '#F44336',  // Red
        'C2+': '#9C27B0'  // Purple
    };
    return colors[level] || '#757575';
}

/**
 * Initialize CEFR modal functionality
 * Attaches click handlers to all CEFR badges
 */
function initCEFRModal() {
    // Preload CEFR definitions
    loadCEFRDefinitions();

    // Attach click handlers to existing CEFR badges
    attachCEFRClickHandlers();

    // Use MutationObserver to handle dynamically added badges
    const observer = new MutationObserver(() => {
        attachCEFRClickHandlers();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

/**
 * Attach click handlers to CEFR level badges and labels
 */
function attachCEFRClickHandlers() {
    // Handle .word-level elements (CEFR badges in word lists)
    document.querySelectorAll('.word-level:not([data-cefr-handler])').forEach(badge => {
        badge.setAttribute('data-cefr-handler', 'true');
        badge.style.cursor = 'pointer';
        badge.title = 'Click to learn more about this CEFR level';

        badge.addEventListener('click', (e) => {
            e.stopPropagation();
            const levelCode = badge.textContent.trim();
            showCEFRModal(levelCode);
        });
    });

    // Handle filter buttons (for educational purposes)
    document.querySelectorAll('.filter-btn[data-level]:not([data-cefr-info])').forEach(btn => {
        const level = btn.getAttribute('data-level');
        if (level && level !== 'all') {
            // Add info icon
            if (!btn.querySelector('.cefr-info-icon')) {
                const infoIcon = document.createElement('span');
                infoIcon.className = 'cefr-info-icon';
                infoIcon.textContent = 'ⓘ';
                infoIcon.title = 'Click for CEFR level information';
                infoIcon.style.marginLeft = '0.5rem';
                infoIcon.style.cursor = 'pointer';

                infoIcon.addEventListener('click', (e) => {
                    e.stopPropagation();
                    showCEFRModal(level);
                });

                btn.appendChild(infoIcon);
                btn.setAttribute('data-cefr-info', 'true');
            }
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCEFRModal);
} else {
    initCEFRModal();
}

// Export functions for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadCEFRDefinitions,
        getCEFRLevel,
        showCEFRModal,
        hideCEFRModal,
        initCEFRModal
    };
}
