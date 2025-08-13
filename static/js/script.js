// Flask-integrated JavaScript for Student Performance Predictor
// DOM Elements
const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const resetBtn = document.getElementById('resetBtn');
const resultContainer = document.getElementById('resultContainer');
const progressBar = document.getElementById('progressFill');
const readingScore = document.getElementById('reading_score');
const writingScore = document.getElementById('writing_score');

// Configuration
const CONFIG = {
    enableAjax: true, // Set to false to use traditional form submission
    debounceTime: 300,
    animationDuration: 500
};

// Form validation rules
const validationRules = {
    gender: { required: true, message: 'Please select your gender' },
    ethnicity: { required: true, message: 'Please select your ethnicity' },
    parental_education: { required: true, message: 'Please select parental education level' },
    lunch: { required: true, message: 'Please select lunch type' },
    test_prep: { required: true, message: 'Please select test preparation status' },
    reading_score: { 
        required: true, 
        min: 0, 
        max: 100, 
        message: 'Reading score must be between 0 and 100' 
    },
    writing_score: { 
        required: true, 
        min: 0, 
        max: 100, 
        message: 'Writing score must be between 0 and 100' 
    }
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for Flask data to be available
    setTimeout(() => {
        initializeForm();
        attachEventListeners();
        updateProgress();
        handleFlaskResults();
    }, 50);
});

function initializeForm() {
    // Check for Flask data and display results if available
    if (window.flaskData && window.flaskData.results) {
        displayResult(window.flaskData.results, window.flaskData.error);
    }
    
    // Initialize score indicators
    updateScoreIndicator('reading_score', 0);
    updateScoreIndicator('writing_score', 0);
    
    // Set up form for AJAX if enabled
    if (CONFIG.enableAjax) {
        form.addEventListener('submit', handleAjaxSubmit);
    } else {
        form.addEventListener('submit', handleSubmit);
    }
}

function attachEventListeners() {
    // Real-time validation for all form fields
    const formInputs = form.querySelectorAll('input, select');
    formInputs.forEach(input => {
        input.addEventListener('input', debounce((e) => handleInputChange(e.target), CONFIG.debounceTime));
        input.addEventListener('blur', (e) => validateField(e.target));
        input.addEventListener('focus', (e) => clearError(e.target));
    });
    
    // Score inputs special handling
    readingScore.addEventListener('input', (e) => {
        updateScoreIndicator('reading_score', e.target.value);
        validateScoreRange(e.target);
    });
    
    writingScore.addEventListener('input', (e) => {
        updateScoreIndicator('writing_score', e.target.value);
        validateScoreRange(e.target);
    });
    
    // Reset button functionality
    resetBtn.addEventListener('click', resetForm);
    
    // Form progress tracking
    const allInputs = form.querySelectorAll('input[required], select[required]');
    allInputs.forEach(input => {
        input.addEventListener('change', updateProgress);
        input.addEventListener('input', debounce(updateProgress, 100));
    });
}

// Handle Flask template results
function handleFlaskResults() {
    if (window.flaskData && window.flaskData.results) {
        setTimeout(() => {
            resultContainer.classList.add('show');
            if (!window.flaskData.error) {
                const numericResult = parseFloat(window.flaskData.results);
                if (!isNaN(numericResult)) {
                    animateScoreCounter(numericResult);
                }
            }
        }, 300);
    }
}

// AJAX form submission
async function handleAjaxSubmit(e) {
    e.preventDefault();

    // 1. Client-side form validation
    if (!validateForm()) {
        showNotification('Please fill in all required fields correctly', 'error');
        return;
    }

    showLoadingState(true);

    try {
        // 2. Collect form data
        const formData = new FormData(form);
        const data = {
            gender: formData.get('gender'),
            ethnicity: formData.get('ethnicity'),
            parental_level_of_education: formData.get('parental_level_of_education'),
            lunch: formData.get('lunch'),
            test_preparation_course: formData.get('test_preparation_course'),
            reading_score: formData.get('reading_score'),
            writing_score: formData.get('writing_score')
        };

        // 3. Send POST request
        const response = await fetch(window.flaskData.apiEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        // 4. Check for HTTP errors before parsing JSON
        if (!response.ok) {
            throw new Error(`HTTP ${response.status} - ${response.statusText}`);
        }

        const result = await response.json();

        // 5. Handle API response
        if (result.success) {
            displayResult(result.prediction, false);
            showNotification(result.message || 'Prediction successful!', 'success');
        } else {
            displayResult(result.error || 'Unknown error', true);
            showNotification(result.error || 'Unknown error', 'error');
        }

    } catch (error) {
        // 6. Catch network or parsing errors
        console.error('Prediction error:', error);
        displayResult('Network error occurred. Please try again.', true);
        showNotification('Network error. Please check your connection.', 'error');
    } finally {
        // 7. Always remove loading state
        showLoadingState(false);
    }
}


// Traditional form submission
function handleSubmit(e) {
    if (!validateForm()) {
        e.preventDefault();
        showNotification('Please fill in all required fields correctly', 'error');
        return;
    }
    
    showLoadingState(true);
    // Form will submit normally to Flask route
}

function displayResult(result, isError = false) {
    const resultValue = document.getElementById('resultValue');
    const resultTitle = document.querySelector('.result-title');
    
    resultContainer.classList.remove('show');
    
    setTimeout(() => {
        if (isError) {
            resultValue.textContent = result;
            resultValue.classList.add('error');
            resultTitle.innerHTML = '❌ Error';
        } else {
            resultValue.textContent = typeof result === 'number' ? `${result}/100` : result;
            resultValue.classList.remove('error');
            resultTitle.innerHTML = '🎯 Predicted Math Score';
            
            // Update performance level
            updatePerformanceLevel(parseFloat(result));
        }
        
        resultContainer.classList.add('show');
        
        if (!isError && typeof result === 'number') {
            animateScoreCounter(result);
        }
    }, 200);
}

function updatePerformanceLevel(score) {
    const performanceElement = document.getElementById('performanceLevel');
    if (!performanceElement) return;
    
    let level = '';
    let color = '';
    
    if (score >= 90) {
        level = 'Excellent';
        color = '#38a169';
    } else if (score >= 80) {
        level = 'Very Good';
        color = '#3182ce';
    } else if (score >= 70) {
        level = 'Good';
        color = '#38a169';
    } else if (score >= 60) {
        level = 'Average';
        color = '#ed8936';
    } else {
        level = 'Needs Improvement';
        color = '#e53e3e';
    }
    
    performanceElement.textContent = level;
    performanceElement.style.color = color;
}

function animateScoreCounter(targetScore) {
    const scoreElement = document.getElementById('resultValue');
    if (!scoreElement || isNaN(targetScore)) return;
    
    let currentScore = 0;
    const increment = targetScore / 30; // 30 steps for smooth animation
    const timer = setInterval(() => {
        currentScore += increment;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(timer);
        }
        scoreElement.textContent = `${Math.round(currentScore * 10) / 10}/100`;
    }, 30);
}

function showLoadingState(show = true) {
    if (show) {
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Add loading messages
        const loadingMessages = [
            'Processing data...',
            'Analyzing patterns...',
            'Calculating prediction...',
            'Almost done...'
        ];
        
        let messageIndex = 0;
        const messageInterval = setInterval(() => {
            const btnText = submitBtn.querySelector('.btn-text');
            if (btnText && messageIndex < loadingMessages.length && submitBtn.classList.contains('loading')) {
                btnText.textContent = loadingMessages[messageIndex];
                messageIndex++;
            } else {
                clearInterval(messageInterval);
            }
        }, 800);
        
        // Store interval ID to clear it later
        submitBtn.dataset.messageInterval = messageInterval;
    } else {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        
        // Clear loading messages
        if (submitBtn.dataset.messageInterval) {
            clearInterval(submitBtn.dataset.messageInterval);
            delete submitBtn.dataset.messageInterval;
        }
        
        const btnText = submitBtn.querySelector('.btn-text');
        if (btnText) {
            btnText.textContent = 'Predict Math Score';
        }
    }
}

// Validation functions
function validateForm() {
    let isValid = true;
    const formData = new FormData(form);
    
    for (const [fieldName, rules] of Object.entries(validationRules)) {
        const field = form.querySelector(`[name="${fieldName}"], [id="${fieldName}"]`);
        const value = formData.get(field.name || field.id);
        
        if (!validateField(field, value, rules)) {
            isValid = false;
        }
    }
    
    return isValid;
}

function validateField(field, value = null, rules = null) {
    const fieldName = field.name || field.id;
    const fieldValue = value || field.value;
    const fieldRules = rules || validationRules[fieldName];
    
    if (!fieldRules) return true;
    
    clearError(field);
    
    // Required field validation
    if (fieldRules.required && (!fieldValue || fieldValue.trim() === '')) {
        showError(field, fieldRules.message || 'This field is required');
        return false;
    }
    
    // Numeric range validation
    if (fieldRules.min !== undefined || fieldRules.max !== undefined) {
        const numValue = parseFloat(fieldValue);
        
        if (fieldValue && isNaN(numValue)) {
            showError(field, 'Please enter a valid number');
            return false;
        }
        
        if (fieldValue && fieldRules.min !== undefined && numValue < fieldRules.min) {
            showError(field, `Value must be at least ${fieldRules.min}`);
            return false;
        }
        
        if (fieldValue && fieldRules.max !== undefined && numValue > fieldRules.max) {
            showError(field, `Value must be at most ${fieldRules.max}`);
            return false;
        }
    }
    
    // Mark field as valid
    if (fieldValue) {
        field.classList.add('success');
        field.classList.remove('error');
    }
    
    return true;
}

function validateScoreRange(field) {
    const value = parseFloat(field.value);
    const indicator = document.getElementById(field.id.replace('_score', '-indicator'));
    
    if (!isNaN(value) && value >= 0 && value <= 100) {
        field.classList.add('success');
        field.classList.remove('error');
        if (indicator) indicator.classList.add('show');
    } else if (field.value !== '') {
        field.classList.add('error');
        field.classList.remove('success');
        if (indicator) indicator.classList.remove('show');
    }
}

function showError(field, message) {
    field.classList.add('error');
    field.classList.remove('success');
    
    const errorElement = document.getElementById((field.name || field.id) + '-error');
    
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

function clearError(field) {
    field.classList.remove('error');
    
    const errorElement = document.getElementById((field.name || field.id) + '-error');
    
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.classList.remove('show');
    }
}

function updateScoreIndicator(scoreType, value) {
    const indicator = document.getElementById(scoreType.replace('_score', '-indicator'));
    if (!indicator) return;
    
    const numValue = parseFloat(value);
    
    if (!isNaN(numValue) && numValue >= 0 && numValue <= 100) {
        const percentage = (numValue / 100) * 100;
        indicator.style.setProperty('--score-width', `${percentage}%`);
        indicator.classList.add('show');
    } else {
        indicator.classList.remove('show');
    }
}

function updateProgress() {
    const requiredFields = form.querySelectorAll('input[required], select[required]');
    const filledFields = Array.from(requiredFields).filter(field => {
        if (field.type === 'number') {
            const value = parseFloat(field.value);
            return !isNaN(value) && value >= 0 && value <= 100;
        }
        return field.value.trim() !== '' && field.value !== field.querySelector('option[disabled]')?.value;
    });
    
    const progress = (filledFields.length / requiredFields.length) * 100;
    progressBar.style.width = `${progress}%`;
    
    // Enable/disable submit button
    submitBtn.disabled = progress < 100;
    submitBtn.style.opacity = progress === 100 ? '1' : '0.7';
}

function resetForm() {
    // Reset form fields
    form.reset();
    
    // Clear all validation states
    const allFields = form.querySelectorAll('input, select');
    allFields.forEach(field => {
        field.classList.remove('error', 'success', 'interacted');
        clearError(field);
    });
    
    // Reset score indicators
    updateScoreIndicator('reading_score', 0);
    updateScoreIndicator('writing_score', 0);
    
    // Reset progress bar
    progressBar.style.width = '0%';
    
    // Hide result container
    resultContainer.classList.remove('show');
    
    // Reset submit button
    showLoadingState(false);
    
    showNotification('Form has been reset', 'success');
    
    // Focus first field
    const firstField = form.querySelector('select, input');
    if (firstField) {
        setTimeout(() => firstField.focus(), 100);
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function handleInputChange(field) {
    clearError(field);
    field.classList.add('interacted');
    updateProgress();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#fed7d7' : type === 'success' ? '#c6f6d5' : '#bee3f8'};
        color: ${type === 'error' ? '#c53030' : type === 'success' ? '#2f855a' : '#2c5282'};
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-weight: 500;
        border-left: 4px solid ${type === 'error' ? '#e53e3e' : type === 'success' ? '#38a169' : '#3182ce'};
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Enhanced features for Flask integration
function addFlaskSpecificFeatures() {
    // Real-time score correlation with Flask API
    let correlationTimeout;
    
    function updateScoreCorrelation() {
        const reading = parseFloat(readingScore.value) || 0;
        const writing = parseFloat(writingScore.value) || 0;
        
        if (reading > 0 && writing > 0) {
            clearTimeout(correlationTimeout);
            correlationTimeout = setTimeout(() => {
                displayScoreInsights(reading, writing);
            }, 500);
        }
    }
    
    readingScore.addEventListener('input', updateScoreCorrelation);
    writingScore.addEventListener('input', updateScoreCorrelation);
}

function displayScoreInsights(reading, writing) {
    let insightsContainer = document.getElementById('score-insights');
    
    if (!insightsContainer) {
        insightsContainer = document.createElement('div');
        insightsContainer.id = 'score-insights';
        insightsContainer.style.cssText = `
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            opacity: 0;
            transition: opacity 0.3s ease;
            border: 1px solid rgba(102, 126, 234, 0.2);
        `;
        
        const scoresContainer = document.querySelector('.form-row:last-of-type');
        if (scoresContainer) {
            scoresContainer.parentNode.insertBefore(insightsContainer, scoresContainer.nextSibling);
        }
    }
    
    const average = (reading + writing) / 2;
    const difference = Math.abs(reading - writing);
    
    let message = `Average Score: ${average.toFixed(1)}`;
    let emoji = '📊';
    let color = '#4a5568';
    
    if (difference <= 5) {
        message += ' - Excellent Balance! ';
        emoji = '🎯';
        color = '#38a169';
    } else if (difference <= 15) {
        message += ' - Good Consistency ';
        emoji = '👍';
        color = '#3182ce';
    } else {
        message += ' - Consider improving the lower score ';
        emoji = '📚';
        color = '#ed8936';
    }
    
    // Predict likely math score range
    const predictedMath = Math.round(average * 0.95 + Math.random() * 10 - 5);
    const range = `${Math.max(0, predictedMath - 5)}-${Math.min(100, predictedMath + 5)}`;
    
    insightsContainer.innerHTML = `
        <div style="text-align: center;">
            <div style="color: ${color}; font-weight: 600; margin-bottom: 8px; font-size: 1.1em;">
                ${emoji} ${message}
            </div>
            <div style="font-size: 0.9em; color: #718096; margin-bottom: 8px;">
                Reading: ${reading} | Writing: ${writing} | Difference: ${difference}
            </div>
            <div style="font-size: 0.85em; color: #4a5568; padding: 8px; background: rgba(255,255,255,0.5); border-radius: 6px;">
                Estimated Math Score Range: <strong>${range}</strong>
            </div>
        </div>
    `;
    
    insightsContainer.style.opacity = '1';
}

// Flask error handling
function handleFlaskErrors() {
    // Check for Flask flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        const type = message.classList.contains('error') ? 'error' : 'info';
        showNotification(message.textContent, type);
        message.remove();
    });
    
    // Handle form validation errors from Flask
    if (window.flaskData && flaskData.validationErrors) {
        Object.entries(flaskData.validationErrors).forEach(([field, errors]) => {
            const fieldElement = form.querySelector(`[name="${field}"]`);
            if (fieldElement && errors.length > 0) {
                showError(fieldElement, errors[0]);
            }
        });
    }
}

// Performance monitoring for Flask
function addFlaskPerformanceMonitoring() {
    let formStartTime = Date.now();
    let interactionCount = 0;
    let validationErrors = 0;
    
    // Track user interactions
    form.addEventListener('input', () => {
        interactionCount++;
    });
    
    form.addEventListener('submit', () => {
        const timeSpent = (Date.now() - formStartTime) / 1000;
        
        // Send analytics to Flask (optional)
        if (CONFIG.enableAnalytics) {
            fetch('/api/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    timeSpent,
                    interactionCount,
                    validationErrors,
                    timestamp: new Date().toISOString()
                })
            }).catch(() => {}); // Fail silently
        }
        
        console.log(`Form submitted - Time: ${timeSpent}s, Interactions: ${interactionCount}, Errors: ${validationErrors}`);
    });
    
    // Track validation errors
    document.addEventListener('error-shown', () => {
        validationErrors++;
    });
}

// Auto-save functionality (Flask session-based)
function addAutoSave() {
    let saveTimeout;
    
    function saveFormData() {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(async () => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            try {
                await fetch('/api/save-draft', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
            } catch (error) {
                console.log('Auto-save failed:', error);
            }
        }, 2000);
    }
    
    // Auto-save on input changes
    form.addEventListener('input', saveFormData);
    form.addEventListener('change', saveFormData);
}

// Load saved draft from Flask session
async function loadDraft() {
    try {
        const response = await fetch('/api/load-draft');
        if (response.ok) {
            const draft = await response.json();
            
            Object.entries(draft).forEach(([key, value]) => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field && value) {
                    field.value = value;
                    field.dispatchEvent(new Event('input', { bubbles: true }));
                    field.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
            
            if (Object.keys(draft).length > 0) {
                showNotification('Draft restored from previous session', 'info');
            }
        }
    } catch (error) {
        console.log('Failed to load draft:', error);
    }
}

// Accessibility enhancements for Flask
function addAccessibilityFeatures() {
    // Add ARIA live region for dynamic updates
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.style.cssText = 'position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden;';
    document.body.appendChild(liveRegion);
    
    // Announce form changes to screen readers
    form.addEventListener('change', (e) => {
        if (e.target.tagName === 'SELECT') {
            liveRegion.textContent = `${e.target.previousElementSibling.textContent}: ${e.target.options[e.target.selectedIndex].text} selected`;
        }
    });
    
    // Announce validation errors
    document.addEventListener('error-shown', (e) => {
        liveRegion.textContent = `Error: ${e.detail.message}`;
    });
    
    // Announce successful predictions
    resultContainer.addEventListener('DOMSubtreeModified', () => {
        if (resultContainer.classList.contains('show')) {
            const resultText = document.getElementById('resultValue').textContent;
            liveRegion.textContent = `Prediction result: ${resultText}`;
        }
    });
    
    // Enhanced keyboard navigation
    form.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
            e.preventDefault();
            const formElements = Array.from(form.querySelectorAll('input, select, button'));
            const currentIndex = formElements.indexOf(e.target);
            const nextElement = formElements[currentIndex + 1];
            
            if (nextElement) {
                nextElement.focus();
            } else {
                submitBtn.focus();
            }
        }
    });
}

// Initialize Flask-specific features
document.addEventListener('DOMContentLoaded', function() {
    // Add Flask-specific enhancements
    setTimeout(() => {
        addFlaskSpecificFeatures();
        handleFlaskErrors();
        addFlaskPerformanceMonitoring();
        addAccessibilityFeatures();
        
        if (CONFIG.enableAutoSave) {
            addAutoSave();
            loadDraft();
        }
    }, 100);
});

// Custom event for error tracking
function showErrorWithEvent(field, message) {
    showError(field, message);
    
    // Dispatch custom event for analytics
    document.dispatchEvent(new CustomEvent('error-shown', {
        detail: { field: field.name || field.id, message }
    }));
}

// Export functions for Flask templates to use
window.StudentFormApp = {
    validateForm,
    resetForm,
    showNotification,
    displayResult,
    updateProgress
};