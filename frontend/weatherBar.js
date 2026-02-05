/**
 * Weather Bottom Bar Module
 * Always-on thin bar at the bottom showing time + weather (Design C: soft mono)
 */

import { state } from './app.js';
import { onWeatherUpdate } from './weatherService.js';

let _barEl = null;
let _timeEl = null;
let _emojiEl = null;
let _tempEl = null;
let _descEl = null;
let _clockInterval = null;

export function initWeatherBar() {
    console.log('Initializing weather bar...');

    _barEl = document.getElementById('weatherBar');
    _timeEl = document.getElementById('barTime');
    _emojiEl = document.getElementById('barEmoji');
    _tempEl = document.getElementById('barTemp');
    _descEl = document.getElementById('barDesc');

    if (!_barEl) return;

    // Start clock
    _updateClock();
    _clockInterval = setInterval(_updateClock, 1000);

    // Subscribe to weather updates
    onWeatherUpdate(_onWeather);

    console.log('Weather bar initialized');
}

function _updateClock() {
    if (!_timeEl) return;
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    _timeEl.textContent = `${h}:${m}`;
}

function _onWeather(data) {
    if (!data || !data.current) return;
    const c = data.current;
    if (_emojiEl) _emojiEl.textContent = c.emoji || '';
    if (_tempEl) _tempEl.textContent = c.temperature != null ? `${Math.round(c.temperature)}${data.unit_symbol}` : '--';
    if (_descEl) _descEl.textContent = (c.description || '').toLowerCase();
}

/**
 * Show or hide the bar. Called by app.js to coordinate with morning/away states.
 */
export function setWeatherBarVisible(visible) {
    if (!_barEl) return;
    if (visible) {
        _barEl.classList.remove('hidden');
    } else {
        _barEl.classList.add('hidden');
    }
}
