/**
 * Raspberry Pi Art Display - Frontend Application
 * Main application module
 */

// Configuration
const CONFIG = {
    apiBase: window.location.origin,
    pollInterval: 5000,
    transitionDuration: 1000,
    imageDuration: 30000
};

// Application state
const state = {
    images: [],
    currentImageIndex: 0,
    todos: [],
    presence: null,
    timePeriod: 'day',
    isAway: false,
    showingTodos: false
};

// DOM elements
const elements = {
    app: null,
    imageContainer: null,
    currentImage: null,
    todoOverlay: null,
    todoList: null,
    statusIndicator: null,
    presenceStatus: null,
    timePeriod: null
};

/**
 * Initialize the application
 */
async function init() {
    console.log('Initializing Raspberry Pi Art Display...');

    // Get DOM elements
    elements.app = document.getElementById('app');
    elements.imageContainer = document.getElementById('imageContainer');
    elements.currentImage = document.getElementById('currentImage');
    elements.todoOverlay = document.getElementById('todoOverlay');
    elements.todoList = document.getElementById('todoList');
    elements.statusIndicator = document.getElementById('statusIndicator');
    elements.presenceStatus = document.getElementById('presenceStatus');
    elements.timePeriod = document.getElementById('timePeriod');

    // Load configuration from API
    await loadConfig();

    // Initialize modules
    const { initSlideshow } = await import('./slideshow.js');
    await initSlideshow();

    const { initTodos } = await import('./todos.js');
    initTodos();

    const { initStateManager } = await import('./stateManager.js');
    initStateManager();

    console.log('Application initialized successfully');
}

/**
 * Load configuration from API
 */
async function loadConfig() {
    try {
        const response = await fetch(`${CONFIG.apiBase}/api/config`);
        if (response.ok) {
            const config = await response.json();

            // Update CONFIG with values from server
            if (config.image_duration) {
                CONFIG.imageDuration = config.image_duration * 1000; // Convert to ms
            }
            if (config.display && config.display.transition_duration) {
                CONFIG.transitionDuration = config.display.transition_duration;
            }
            if (config.display && config.display.poll_interval) {
                CONFIG.pollInterval = config.display.poll_interval;
            }

            console.log('Configuration loaded:', config);
        }
    } catch (error) {
        console.error('Failed to load configuration:', error);
    }
}

/**
 * Fetch data from API
 */
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`${CONFIG.apiBase}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`API fetch failed for ${endpoint}:`, error);
        return null;
    }
}

/**
 * Update application state
 */
function updateState(updates) {
    Object.assign(state, updates);
    console.log('State updated:', updates);
}

/**
 * Show error message
 */
function showError(message) {
    console.error(message);
    // TODO: Show error UI
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export for use in other modules (if needed)
export { CONFIG, state, elements, fetchAPI, updateState };
