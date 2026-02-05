/**
 * Image Slideshow Module
 * Handles image loading, preloading, and slideshow transitions
 */

import { CONFIG, state, elements, fetchAPI, updateState } from './app.js';

let slideshowInterval = null;
let imageRefreshInterval = null;
let preloadedImage = null;

/**
 * Initialize the slideshow
 */
export async function initSlideshow() {
    console.log('Initializing slideshow...');

    // Fetch images from API
    await loadImages();

    if (state.images.length === 0) {
        console.error('No images available');
        showError('No images found');
        return;
    }

    // Show first image
    await showImage(0);

    // Start slideshow
    startSlideshow();

    // Start periodic image refresh to detect new images
    startImageRefresh();

    console.log(`Slideshow started with ${state.images.length} images`);
}

/**
 * Load images from API
 */
async function loadImages() {
    const data = await fetchAPI('/api/images');

    if (data && data.images && data.images.length > 0) {
        updateState({ images: data.images });
        console.log(`Loaded ${data.images.length} images`);
    } else {
        console.error('Failed to load images or no images found');
    }
}

/**
 * Start periodic image refresh to detect new images in the folder
 */
function startImageRefresh() {
    // Check for new images every 60 seconds
    imageRefreshInterval = setInterval(async () => {
        const data = await fetchAPI('/api/images');
        if (data && data.images) {
            const currentCount = state.images.length;
            const newCount = data.images.length;

            if (newCount !== currentCount) {
                console.log(`Image count changed: ${currentCount} -> ${newCount}`);
                updateState({ images: data.images });
            }
        }
    }, 60000);
}

/**
 * Preload the next image
 */
function preloadNextImage() {
    const nextIndex = (state.currentImageIndex + 1) % state.images.length;
    const nextImageUrl = `${CONFIG.apiBase}${state.images[nextIndex].url}`;

    preloadedImage = new Image();
    preloadedImage.src = nextImageUrl;

    preloadedImage.onerror = () => {
        console.error(`Failed to preload image: ${nextImageUrl}`);
    };
}

/**
 * Show image at given index
 */
async function showImage(index) {
    if (!state.images || state.images.length === 0) {
        return;
    }

    const image = state.images[index];
    const imageUrl = `${CONFIG.apiBase}${image.url}`;

    try {
        // Fade out current image
        elements.currentImage.classList.remove('visible');

        // Wait for fade out
        await sleep(CONFIG.transitionDuration / 2);

        // Load new image
        elements.currentImage.src = imageUrl;

        // Wait for image to load
        await new Promise((resolve, reject) => {
            elements.currentImage.onload = resolve;
            elements.currentImage.onerror = () => {
                console.error(`Failed to load image: ${imageUrl}`);
                reject(new Error('Image load failed'));
            };
        });

        // Fade in new image
        elements.currentImage.classList.add('visible');

        // Update state
        updateState({ currentImageIndex: index });

        // Preload next image
        preloadNextImage();

        console.log(`Showing image ${index + 1}/${state.images.length}: ${image.filename}`);
    } catch (error) {
        console.error('Error showing image:', error);

        // Try to recover by showing next image
        const nextIndex = (index + 1) % state.images.length;
        if (nextIndex !== index) {
            setTimeout(() => showImage(nextIndex), 1000);
        }
    }
}

/**
 * Show next image in slideshow
 */
function showNextImage() {
    const nextIndex = (state.currentImageIndex + 1) % state.images.length;
    showImage(nextIndex);
}

/**
 * Show previous image in slideshow
 */
function showPreviousImage() {
    const prevIndex = (state.currentImageIndex - 1 + state.images.length) % state.images.length;
    showImage(prevIndex);
}

/**
 * Start the slideshow timer
 */
function startSlideshow() {
    if (slideshowInterval) {
        clearInterval(slideshowInterval);
    }

    slideshowInterval = setInterval(() => {
        // Only advance slideshow if not showing TODOs, not away, and not showing morning display
        if (!state.showingTodos && !state.isAway && !state.showingMorning) {
            showNextImage();
        }
    }, CONFIG.imageDuration);
}

/**
 * Stop the slideshow timer
 */
export function stopSlideshow() {
    if (slideshowInterval) {
        clearInterval(slideshowInterval);
        slideshowInterval = null;
        console.log('Slideshow stopped');
    }
}

/**
 * Stop the image refresh timer
 */
export function stopImageRefresh() {
    if (imageRefreshInterval) {
        clearInterval(imageRefreshInterval);
        imageRefreshInterval = null;
        console.log('Image refresh stopped');
    }
}

/**
 * Pause slideshow
 */
export function pauseSlideshow() {
    if (slideshowInterval) {
        clearInterval(slideshowInterval);
        slideshowInterval = null;
    }
}

/**
 * Resume slideshow
 */
export function resumeSlideshow() {
    if (!slideshowInterval) {
        startSlideshow();
    }
}

/**
 * Helper function to sleep
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Show error message
 */
function showError(message) {
    console.error(message);
    // Could display error on screen if needed
}
