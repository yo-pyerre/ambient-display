/**
 * State Management Module
 * Handles presence detection polling and state transitions
 */

import { CONFIG, state, elements, fetchAPI, updateState } from './app.js';
import { pauseSlideshow, resumeSlideshow } from './slideshow.js';

let presenceCheckInterval = null;
let stateCheckInterval = null;

/**
 * Initialize state management
 */
export function initStateManager() {
    console.log('Initializing state manager...');

    // Start presence monitoring
    startPresenceMonitoring();

    // Start periodic state checks
    startStateChecks();

    console.log('State manager initialized');
}

/**
 * Start monitoring device presence
 */
function startPresenceMonitoring() {
    // Initial check
    checkPresence();

    // Set up periodic checks
    presenceCheckInterval = setInterval(checkPresence, CONFIG.pollInterval);
}

/**
 * Check device presence from API
 */
async function checkPresence() {
    const data = await fetchAPI('/api/presence');

    if (data) {
        const wasAway = state.isAway;
        const isPresent = data.present;

        updateState({ presence: data });

        // Determine if away
        const shouldBeAway = !isPresent;

        if (shouldBeAway !== wasAway) {
            if (shouldBeAway) {
                enterAwayMode();
            } else {
                exitAwayMode();
            }
        }

        // Update status indicator if visible
        if (elements.presenceStatus) {
            elements.presenceStatus.textContent = isPresent ? '👤 Present' : '🚪 Away';
        }
    }
}

/**
 * Enter away mode (screen blanking)
 */
function enterAwayMode() {
    console.log('Entering away mode...');

    updateState({ isAway: true });

    // Add away class for screen blanking
    if (elements.app) {
        elements.app.classList.add('away');
    }

    // Pause slideshow to save resources
    pauseSlideshow();

    console.log('Away mode activated');
}

/**
 * Exit away mode
 */
function exitAwayMode() {
    console.log('Exiting away mode...');

    updateState({ isAway: false });

    // Remove away class
    if (elements.app) {
        elements.app.classList.remove('away');
    }

    // Resume slideshow
    resumeSlideshow();

    console.log('Away mode deactivated');
}

/**
 * Start periodic state checks
 */
function startStateChecks() {
    stateCheckInterval = setInterval(updateUIState, 1000);
}

/**
 * Update UI based on current state
 */
function updateUIState() {
    // Sync app class with away state
    if (state.isAway && !elements.app.classList.contains('away')) {
        elements.app.classList.add('away');
    } else if (!state.isAway && elements.app.classList.contains('away')) {
        elements.app.classList.remove('away');
    }
}

/**
 * Force enter away mode (for testing)
 */
export function forceAwayMode() {
    enterAwayMode();
}

/**
 * Force exit away mode (for testing)
 */
export function forceActiveMode() {
    exitAwayMode();
}

/**
 * Stop state management
 */
export function stopStateManager() {
    if (presenceCheckInterval) {
        clearInterval(presenceCheckInterval);
        presenceCheckInterval = null;
    }

    if (stateCheckInterval) {
        clearInterval(stateCheckInterval);
        stateCheckInterval = null;
    }

    console.log('State manager stopped');
}

/**
 * Get current state summary
 */
export function getStateSummary() {
    return {
        isAway: state.isAway,
        showingTodos: state.showingTodos,
        currentImageIndex: state.currentImageIndex,
        totalImages: state.images.length,
        presenceStatus: state.presence ? state.presence.present : null
    };
}
