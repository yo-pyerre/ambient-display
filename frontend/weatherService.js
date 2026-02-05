/**
 * Shared Weather Service Module
 * Centralized weather data fetcher used by both the bottom bar and morning display
 */

import { fetchAPI } from './app.js';

let _data = null;
let _listeners = [];
let _pollInterval = null;

const POLL_MS = 60000; // fetch every 60s

/**
 * Initialize the weather service and start polling
 */
export function initWeatherService() {
    console.log('Initializing weather service...');
    _fetchAndNotify();
    _pollInterval = setInterval(_fetchAndNotify, POLL_MS);
}

/**
 * Subscribe to weather data updates
 * Callback receives the full weather object (current, forecast, moon, etc.)
 * Returns an unsubscribe function.
 */
export function onWeatherUpdate(callback) {
    _listeners.push(callback);
    // Immediately call with cached data if available
    if (_data) callback(_data);
    return () => {
        _listeners = _listeners.filter(fn => fn !== callback);
    };
}

/**
 * Get the latest cached weather data (may be null)
 */
export function getWeatherData() {
    return _data;
}

async function _fetchAndNotify() {
    const data = await fetchAPI('/api/weather');
    if (!data || data.error) return;
    _data = data;
    for (const fn of _listeners) {
        try { fn(_data); } catch (e) { console.error('Weather listener error:', e); }
    }
}
