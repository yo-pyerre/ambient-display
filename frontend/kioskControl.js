/**
 * Kiosk Control Module
 * Handles exit from kiosk mode and fullscreen toggle
 */

let exitPanel = null;
let exitTrigger = null;
let isExitPanelVisible = false;

/**
 * Initialize kiosk controls
 */
export function initKioskControl() {
    console.log('Initializing kiosk controls...');

    exitPanel = document.getElementById('exitPanel');
    exitTrigger = document.getElementById('exitTrigger');

    if (!exitPanel || !exitTrigger) {
        console.error('Exit panel elements not found');
        return;
    }

    // Click on trigger area (top-right corner) to show panel
    exitTrigger.addEventListener('click', toggleExitPanel);

    // Double-click anywhere to show panel (alternative)
    document.addEventListener('dblclick', (e) => {
        // Only if clicking in top-right quadrant
        if (e.clientX > window.innerWidth * 0.8 && e.clientY < window.innerHeight * 0.2) {
            toggleExitPanel();
        }
    });

    // Button handlers
    const toggleFullscreenBtn = document.getElementById('toggleFullscreen');
    const exitKioskBtn = document.getElementById('exitKiosk');

    if (toggleFullscreenBtn) {
        toggleFullscreenBtn.addEventListener('click', toggleFullscreen);
    }

    if (exitKioskBtn) {
        exitKioskBtn.addEventListener('click', exitKiosk);
    }

    // Escape key to close panel
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && isExitPanelVisible) {
            hideExitPanel();
        }

        // Ctrl+Shift+Q to show exit panel (alternative keyboard shortcut)
        if (e.ctrlKey && e.shiftKey && e.key === 'Q') {
            toggleExitPanel();
        }

        // F11 to toggle fullscreen
        if (e.key === 'F11') {
            e.preventDefault();
            toggleFullscreen();
        }
    });

    // Click outside panel to close
    document.addEventListener('click', (e) => {
        if (isExitPanelVisible &&
            !exitPanel.contains(e.target) &&
            !exitTrigger.contains(e.target)) {
            hideExitPanel();
        }
    });

    console.log('Kiosk controls initialized');
    console.log('Tip: Click top-right corner or press Ctrl+Shift+Q to access exit controls');
}

/**
 * Toggle exit panel visibility
 */
function toggleExitPanel() {
    if (isExitPanelVisible) {
        hideExitPanel();
    } else {
        showExitPanel();
    }
}

/**
 * Show exit panel
 */
function showExitPanel() {
    if (exitPanel) {
        exitPanel.classList.remove('hidden');
        isExitPanelVisible = true;
        // Show cursor when panel is visible
        document.body.style.cursor = 'default';
    }
}

/**
 * Hide exit panel
 */
function hideExitPanel() {
    if (exitPanel) {
        exitPanel.classList.add('hidden');
        isExitPanelVisible = false;
        // Hide cursor again
        document.body.style.cursor = 'none';
    }
}

/**
 * Toggle fullscreen mode
 */
function toggleFullscreen() {
    if (!document.fullscreenElement) {
        // Enter fullscreen
        document.documentElement.requestFullscreen().catch(err => {
            console.error('Error entering fullscreen:', err);
        });
    } else {
        // Exit fullscreen
        document.exitFullscreen().catch(err => {
            console.error('Error exiting fullscreen:', err);
        });
    }
    hideExitPanel();
}

/**
 * Exit kiosk mode
 * This will attempt to close the browser window
 */
function exitKiosk() {
    console.log('Attempting to exit kiosk mode...');

    // Try to close the window (works in kiosk mode)
    try {
        window.close();
    } catch (e) {
        console.error('Could not close window:', e);
    }

    // If window.close() doesn't work, show a message
    setTimeout(() => {
        // If we're still here, the close didn't work
        alert('To exit kiosk mode:\n\n' +
              '1. Press Alt+F4\n' +
              '2. Or press Ctrl+W\n' +
              '3. Or use a keyboard to press Ctrl+Alt+T to open terminal\n\n' +
              'Then run: pkill chromium');
    }, 500);
}

/**
 * Check if currently in fullscreen
 */
export function isFullscreen() {
    return !!document.fullscreenElement;
}
