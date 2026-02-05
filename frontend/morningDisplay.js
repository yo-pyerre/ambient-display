/**
 * Morning Display Module
 * Shows time, weather, forecast, and celestial info during the first hour of daytime
 * Design C: soft mono aesthetic
 */

import { CONFIG, state, elements, fetchAPI, updateState } from './app.js';
import { pauseSlideshow, resumeSlideshow } from './slideshow.js';
import { onWeatherUpdate } from './weatherService.js';
import { setWeatherBarVisible } from './weatherBar.js';

let morningCheckInterval = null;
let timeUpdateInterval = null;

/**
 * Initialize the morning display
 */
export function initMorningDisplay() {
    console.log('Initializing morning display...');

    elements.morningOverlay = document.getElementById('morningOverlay');
    elements.morningTime = document.getElementById('morningTime');
    elements.morningDate = document.getElementById('morningDate');
    elements.morningEmoji = document.getElementById('morningEmoji');
    elements.morningTemp = document.getElementById('morningTemp');
    elements.morningDesc = document.getElementById('morningDesc');
    elements.morningFeelsLike = document.getElementById('morningFeelsLike');
    elements.morningHumidity = document.getElementById('morningHumidity');
    elements.morningWind = document.getElementById('morningWind');
    elements.morningUV = document.getElementById('morningUV');
    elements.morningForecast = document.getElementById('morningForecast');
    elements.morningRise = document.getElementById('morningRise');
    elements.morningSet = document.getElementById('morningSet');
    elements.morningMoonEmoji = document.getElementById('morningMoonEmoji');
    elements.morningMoonName = document.getElementById('morningMoonName');

    // Subscribe to weather updates for live data
    onWeatherUpdate(_onWeather);

    // Check morning status immediately
    checkMorningStatus();

    // Set up periodic check (every 60 seconds)
    morningCheckInterval = setInterval(checkMorningStatus, 60000);

    console.log('Morning display initialized');
}

/**
 * Check if it's currently morning hour and update display
 */
async function checkMorningStatus() {
    const data = await fetchAPI('/api/morning-info');
    if (!data) return;

    if (data.is_morning_hour && !state.showingMorning) {
        showMorningDisplay();
    } else if (!data.is_morning_hour && state.showingMorning) {
        hideMorningDisplay();
    }
}

function showMorningDisplay() {
    if (!elements.morningOverlay) return;
    console.log('Showing morning display');

    pauseSlideshow();
    updateState({ showingMorning: true });
    setWeatherBarVisible(false);

    updateTimeDisplay();
    elements.morningOverlay.classList.remove('hidden');

    if (timeUpdateInterval) clearInterval(timeUpdateInterval);
    timeUpdateInterval = setInterval(updateTimeDisplay, 1000);
}

function hideMorningDisplay() {
    if (!elements.morningOverlay) return;
    console.log('Hiding morning display');

    if (timeUpdateInterval) {
        clearInterval(timeUpdateInterval);
        timeUpdateInterval = null;
    }

    elements.morningOverlay.classList.add('hidden');
    updateState({ showingMorning: false });
    setWeatherBarVisible(true);
    resumeSlideshow();
}

function updateTimeDisplay() {
    const now = new Date();
    const h = String(now.getHours()).padStart(2, '0');
    const m = String(now.getMinutes()).padStart(2, '0');
    if (elements.morningTime) elements.morningTime.textContent = `${h}:${m}`;

    if (elements.morningDate) {
        const days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
        const months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
        const day = days[now.getDay()];
        const month = months[now.getMonth()];
        const date = String(now.getDate()).padStart(2, '0');
        elements.morningDate.textContent = `${day} ${month} ${date}\n${now.getFullYear()}`;
    }
}

function _onWeather(data) {
    if (!data) return;
    const c = data.current;
    const unit = data.unit_symbol || '°F';

    // Current conditions
    if (elements.morningEmoji) elements.morningEmoji.textContent = c.emoji || '';
    if (elements.morningTemp) elements.morningTemp.textContent = c.temperature != null ? `${Math.round(c.temperature)}${unit}` : '--';
    if (elements.morningDesc) elements.morningDesc.textContent = (c.description || 'unknown').toLowerCase();

    // Detail cells
    if (elements.morningFeelsLike) elements.morningFeelsLike.textContent = c.feels_like != null ? `${Math.round(c.feels_like)}${unit}` : '--';
    if (elements.morningHumidity) elements.morningHumidity.textContent = c.humidity != null ? `${Math.round(c.humidity)}%` : '--';
    if (elements.morningWind) elements.morningWind.textContent = c.wind_speed != null ? `${Math.round(c.wind_speed)} mph` : '--';
    if (elements.morningUV) elements.morningUV.textContent = c.uv_index != null ? `${Math.round(c.uv_index)}` : '--';

    // Forecast
    if (elements.morningForecast && data.forecast && data.forecast.days) {
        const days = data.forecast.days;
        elements.morningForecast.innerHTML = days.map((d, i) => `
            <div class="forecast-day${i === 0 ? ' forecast-today' : ''}">
                <div class="forecast-name">${i === 0 ? 'today' : d.day_name}</div>
                <div class="forecast-emoji">${d.emoji}</div>
                <span class="forecast-high">${Math.round(d.high)}°</span>
                <span class="forecast-low">${Math.round(d.low)}°</span>
            </div>
        `).join('');

        // Sunrise/sunset from first day
        if (days[0]) {
            const rise = _formatTime(days[0].sunrise);
            const set = _formatTime(days[0].sunset);
            if (elements.morningRise) elements.morningRise.textContent = rise;
            if (elements.morningSet) elements.morningSet.textContent = set;
        }
    }

    // Moon
    if (data.moon) {
        if (elements.morningMoonEmoji) elements.morningMoonEmoji.textContent = data.moon.emoji || '';
        if (elements.morningMoonName) elements.morningMoonName.textContent = (data.moon.name || '').toLowerCase();
    }
}

/**
 * Format an ISO datetime string to 24h time (HH:MM)
 */
function _formatTime(isoStr) {
    if (!isoStr) return '--';
    try {
        const d = new Date(isoStr);
        return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
    } catch {
        return '--';
    }
}

export function stopMorningDisplay() {
    if (morningCheckInterval) { clearInterval(morningCheckInterval); morningCheckInterval = null; }
    if (timeUpdateInterval) { clearInterval(timeUpdateInterval); timeUpdateInterval = null; }
}
