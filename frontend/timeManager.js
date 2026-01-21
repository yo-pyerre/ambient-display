/**
 * Time-Based Behavior Module
 * Handles day/night mode transitions based on time of day
 */

import { CONFIG, state, elements, fetchAPI, updateState } from './app.js';

let timePeriodCheckInterval = null;
let currentPeriod = 'day';

/**
 * Initialize time-based behavior
 */
export function initTimeManager() {
    console.log('Initializing time manager...');

    // Initial check
    checkTimePeriod();

    // Set up periodic checks
    timePeriodCheckInterval = setInterval(checkTimePeriod, CONFIG.pollInterval);

    console.log('Time manager initialized');
}

/**
 * Check current time period from API
 */
async function checkTimePeriod() {
    const data = await fetchAPI('/api/time-period');

    if (data && data.period) {
        const newPeriod = data.period;

        // Check if period changed
        if (newPeriod !== currentPeriod) {
            console.log(`Time period changed: ${currentPeriod} -> ${newPeriod}`);
            currentPeriod = newPeriod;
            applyTimePeriodTheme(newPeriod);
        }

        updateState({ timePeriod: newPeriod });

        // Update status indicator if visible
        if (elements.timePeriod) {
            elements.timePeriod.textContent = newPeriod === 'day' ? '☀️ Day' : '🌙 Night';
        }
    }
}

/**
 * Apply theme based on time period
 */
function applyTimePeriodTheme(period) {
    const body = document.body;

    if (period === 'night') {
        body.classList.add('night-mode');
        console.log('Applied night mode theme');
    } else {
        body.classList.remove('night-mode');
        console.log('Applied day mode theme');
    }
}

/**
 * Force day mode
 */
export function forceDayMode() {
    currentPeriod = 'day';
    applyTimePeriodTheme('day');
    updateState({ timePeriod: 'day' });
}

/**
 * Force night mode
 */
export function forceNightMode() {
    currentPeriod = 'night';
    applyTimePeriodTheme('night');
    updateState({ timePeriod: 'night' });
}

/**
 * Toggle between day and night mode (for testing)
 */
export function toggleDayNight() {
    if (currentPeriod === 'day') {
        forceNightMode();
    } else {
        forceDayMode();
    }
}

/**
 * Stop time period monitoring
 */
export function stopTimeManager() {
    if (timePeriodCheckInterval) {
        clearInterval(timePeriodCheckInterval);
        timePeriodCheckInterval = null;
    }

    console.log('Time manager stopped');
}

/**
 * Get current time period
 */
export function getCurrentPeriod() {
    return currentPeriod;
}
