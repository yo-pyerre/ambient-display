/**
 * TODO Display Module
 * Handles fetching and displaying TODO list overlay
 */

import { CONFIG, state, elements, fetchAPI, updateState } from './app.js';

let todoUpdateInterval = null;
let toggleTimeout = null;

/**
 * Initialize TODO display
 */
export function initTodos() {
    console.log('Initializing TODO display...');

    // Load TODOs initially
    loadTodos();

    // Set up periodic updates
    todoUpdateInterval = setInterval(loadTodos, CONFIG.pollInterval);

    // Set up keyboard toggle (T key for TODO)
    document.addEventListener('keydown', (e) => {
        if (e.key === 't' || e.key === 'T') {
            toggleTodos();
        }
    });

    console.log('TODO display initialized');
}

/**
 * Load TODO list from API
 */
async function loadTodos() {
    const data = await fetchAPI('/api/todos');

    if (data && data.items) {
        updateState({ todos: data.items });
        renderTodos();
        console.log(`Loaded ${data.items.length} TODO items`);
    } else {
        console.log('No TODOs found or failed to load');
        updateState({ todos: [] });
    }
}

/**
 * Render TODO items in the overlay
 */
function renderTodos() {
    if (!elements.todoList) return;

    // Clear existing items
    elements.todoList.innerHTML = '';

    // Add TODO items
    if (state.todos.length === 0) {
        const emptyMessage = document.createElement('div');
        emptyMessage.className = 'todo-item';
        emptyMessage.textContent = 'No TODOs found';
        elements.todoList.appendChild(emptyMessage);
    } else {
        state.todos.forEach(todo => {
            const todoItem = document.createElement('div');
            todoItem.className = 'todo-item';
            todoItem.textContent = todo;
            elements.todoList.appendChild(todoItem);
        });
    }
}

/**
 * Show TODO overlay
 */
export function showTodos() {
    if (!elements.todoOverlay) return;

    elements.todoOverlay.classList.remove('hidden');
    updateState({ showingTodos: true });
    console.log('TODO overlay shown');
}

/**
 * Hide TODO overlay
 */
export function hideTodos() {
    if (!elements.todoOverlay) return;

    elements.todoOverlay.classList.add('hidden');
    updateState({ showingTodos: false });
    console.log('TODO overlay hidden');
}

/**
 * Toggle TODO overlay visibility
 */
export function toggleTodos() {
    if (state.showingTodos) {
        hideTodos();
    } else {
        showTodos();
    }
}

/**
 * Auto-hide TODOs after specified duration
 */
export function showTodosTemporarily(duration = 30000) {
    showTodos();

    // Clear any existing timeout
    if (toggleTimeout) {
        clearTimeout(toggleTimeout);
    }

    // Set new timeout
    toggleTimeout = setTimeout(() => {
        hideTodos();
    }, duration);
}

/**
 * Stop TODO updates
 */
export function stopTodoUpdates() {
    if (todoUpdateInterval) {
        clearInterval(todoUpdateInterval);
        todoUpdateInterval = null;
    }
}
