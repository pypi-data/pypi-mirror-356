/**
 * Healthcare Management Platform - Main JavaScript
 * Enhances user experience with interactive features
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeHealthcarePlatform();
});

/**
 * Main initialization function
 */
function initializeHealthcarePlatform() {
    // Initialize all components
    initializeFormValidation();
    initializeSearchFunctionality();
    initializeModalHandlers();
    initializeTooltips();
    initializeAccessibility();
    initializeAnimations();
    initializeDataTables();
    initializeConfirmationDialogs();
    initializeAutoSave();
    initializeRealTimeUpdates();
    
    console.log('Healthcare Platform initialized successfully');
}

/**
 * Enhanced form validation
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form[data-validate="true"], .needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Highlight first invalid field
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    showFieldError(firstInvalidField, 'Please fill out this field correctly.');
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(input);
            });
        });
    });
    
    // Custom validation rules
    addCustomValidationRules();
}

/**
 * Add custom validation rules for healthcare data
 */
function addCustomValidationRules() {
    // Medical Record Number validation
    const mrnInputs = document.querySelectorAll('input[name*="medical_record"]');
    mrnInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = this.value.toUpperCase();
            this.value = value;
            
            if (value && !/^MRN-[A-Z0-9]{8}$/.test(value)) {
                this.setCustomValidity('Medical Record Number must be in format MRN-XXXXXXXX');
            } else {
                this.setCustomValidity('');
            }
        });
    });
    
    // Phone number validation
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = this.value.replace(/\D/g, '');
            if (value.length >= 10) {
                this.value = formatPhoneNumber(value);
            }
        });
    });
    
    // Date of birth validation
    const dobInputs = document.querySelectorAll('input[name="date_of_birth"]');
    dobInputs.forEach(input => {
        input.addEventListener('change', function() {
            const birthDate = new Date(this.value);
            const today = new Date();
            const age = today.getFullYear() - birthDate.getFullYear();
            
            if (age > 150 || birthDate > today) {
                this.setCustomValidity('Please enter a valid date of birth');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

/**
 * Format phone number
 */
function formatPhoneNumber(phoneNumber) {
    const cleaned = phoneNumber.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phoneNumber;
}

/**
 * Show field error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Clear field error
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Validate individual field
 */
function validateField(field) {
    if (!field.checkValidity()) {
        let message = field.validationMessage;
        
        // Custom messages for better UX
        if (field.type === 'email' && field.validity.typeMismatch) {
            message = 'Please enter a valid email address (e.g., user@example.com)';
        } else if (field.type === 'tel' && field.validity.patternMismatch) {
            message = 'Please enter a valid phone number (e.g., (555) 123-4567)';
        }
        
        showFieldError(field, message);
        return false;
    } else {
        clearFieldError(field);
        return true;
    }
}

/**
 * Enhanced search functionality
 */
function initializeSearchFunctionality() {
    const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="search" i]');
    
    searchInputs.forEach(input => {
        // Add search icon
        if (!input.parentNode.querySelector('.search-icon')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'position-relative';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            
            const icon = document.createElement('i');
            icon.className = 'fas fa-search search-icon position-absolute';
            icon.style.cssText = 'right: 10px; top: 50%; transform: translateY(-50%); color: #adb5bd; pointer-events: none;';
            wrapper.appendChild(icon);
        }
        
        // Add real-time search with debouncing
        let searchTimeout;
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchTerm = this.value.toLowerCase();
            
            searchTimeout = setTimeout(() => {
                performSearch(searchTerm, input);
            }, 300);
        });
        
        // Clear search functionality
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                this.value = '';
                performSearch('', input);
            }
        });
    });
}

/**
 * Perform search operation
 */
function performSearch(searchTerm, input) {
    const targetTable = input.closest('.card').querySelector('table tbody');
    
    if (targetTable) {
        const rows = targetTable.querySelectorAll('tr');
        let visibleCount = 0;
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const isVisible = searchTerm === '' || text.includes(searchTerm);
            
            row.style.display = isVisible ? '' : 'none';
            if (isVisible) visibleCount++;
        });
        
        // Update search results count
        updateSearchResultsCount(input, visibleCount, rows.length);
    }
}

/**
 * Update search results count
 */
function updateSearchResultsCount(input, visible, total) {
    let countElement = input.parentNode.querySelector('.search-count');
    
    if (!countElement) {
        countElement = document.createElement('small');
        countElement.className = 'search-count text-muted mt-1 d-block';
        input.parentNode.appendChild(countElement);
    }
    
    if (input.value) {
        countElement.textContent = `Showing ${visible} of ${total} results`;
        countElement.style.display = 'block';
    } else {
        countElement.style.display = 'none';
    }
}

/**
 * Enhanced modal handlers
 */
function initializeModalHandlers() {
    // Auto-focus first input in modals
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = this.querySelector('input, select, textarea');
            if (firstInput && !firstInput.disabled) {
                firstInput.focus();
            }
        });
        
        // Clear form when modal is closed
        modal.addEventListener('hidden.bs.modal', function() {
            const form = this.querySelector('form');
            if (form) {
                form.reset();
                form.classList.remove('was-validated');
                
                // Clear any error messages
                form.querySelectorAll('.invalid-feedback').forEach(error => error.remove());
                form.querySelectorAll('.is-invalid').forEach(field => field.classList.remove('is-invalid'));
            }
        });
    });
    
    // Enhanced lab order modal
    const labOrderModal = document.getElementById('labOrderModal');
    if (labOrderModal) {
        setupLabOrderModal(labOrderModal);
    }
}

/**
 * Setup lab order modal functionality
 */
function setupLabOrderModal(modal) {
    const testNameSelect = modal.querySelector('select[name="test_name"]');
    const testTypeSelect = modal.querySelector('select[name="test_type"]');
    const referenceRangeInput = modal.querySelector('input[name="reference_range"]');
    
    if (testNameSelect && testTypeSelect && referenceRangeInput) {
        // Auto-populate reference ranges based on test selection
        const referenceRanges = {
            'Complete Blood Count': 'WBC: 4.5-11.0 K/uL, RBC: 4.5-5.9 M/uL, Hgb: 14-18 g/dL',
            'Basic Metabolic Panel': 'Glucose: 70-100 mg/dL, BUN: 6-24 mg/dL, Creatinine: 0.84-1.21 mg/dL',
            'Lipid Panel': 'Total Cholesterol: <200 mg/dL, HDL: >40 mg/dL, LDL: <100 mg/dL',
            'Thyroid Function': 'TSH: 0.27-4.20 uIU/mL, Free T4: 0.93-1.70 ng/dL',
            'Liver Function': 'ALT: 10-40 U/L, AST: 10-40 U/L, Bilirubin: 0.1-1.2 mg/dL'
        };
        
        testNameSelect.addEventListener('change', function() {
            const selectedTest = this.value;
            if (referenceRanges[selectedTest]) {
                referenceRangeInput.value = referenceRanges[selectedTest];
            }
            
            // Auto-select appropriate test type
            const testTypeMapping = {
                'Complete Blood Count': 'Hematology',
                'Basic Metabolic Panel': 'Chemistry',
                'Lipid Panel': 'Chemistry',
                'Thyroid Function': 'Endocrinology',
                'Liver Function': 'Chemistry'
            };
            
            if (testTypeMapping[selectedTest]) {
                testTypeSelect.value = testTypeMapping[selectedTest];
            }
        });
    }
}

/**
 * Initialize tooltips for better UX
 */
function initializeTooltips() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add custom tooltips for important elements
    addCustomTooltips();
}

/**
 * Add custom tooltips
 */
function addCustomTooltips() {
    // Add tooltips to status badges
    document.querySelectorAll('.badge').forEach(badge => {
        if (badge.textContent.includes('Pending')) {
            badge.setAttribute('data-bs-toggle', 'tooltip');
            badge.setAttribute('title', 'Test results are being processed');
        } else if (badge.textContent.includes('Completed')) {
            badge.setAttribute('data-bs-toggle', 'tooltip');
            badge.setAttribute('title', 'Test results are available');
        }
    });
    
    // Add tooltips to action buttons
    document.querySelectorAll('button[onclick*="orderLabTest"]').forEach(btn => {
        btn.setAttribute('data-bs-toggle', 'tooltip');
        btn.setAttribute('title', 'Order new lab test for this patient');
    });
}

/**
 * Accessibility enhancements
 */
function initializeAccessibility() {
    // Add ARIA labels where missing
    addAriaLabels();
    
    // Keyboard navigation enhancements
    enhanceKeyboardNavigation();
    
    // Screen reader announcements
    setupScreenReaderAnnouncements();
    
    // Focus management
    manageFocus();
}

/**
 * Add ARIA labels for better accessibility
 */
function addAriaLabels() {
    // Add labels to search inputs
    document.querySelectorAll('input[type="search"]').forEach(input => {
        if (!input.getAttribute('aria-label')) {
            input.setAttribute('aria-label', 'Search patients and records');
        }
    });
    
    // Add labels to action buttons
    document.querySelectorAll('button[onclick]').forEach(btn => {
        if (!btn.getAttribute('aria-label') && btn.querySelector('i')) {
            const icon = btn.querySelector('i');
            if (icon.classList.contains('fa-eye')) {
                btn.setAttribute('aria-label', 'View details');
            } else if (icon.classList.contains('fa-flask')) {
                btn.setAttribute('aria-label', 'Order lab test');
            }
        }
    });
}

/**
 * Enhance keyboard navigation
 */
function enhanceKeyboardNavigation() {
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+/ or Cmd+/ for search
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) {
                    modal.hide();
                }
            }
        }
    });
    
    // Improve tab navigation in tables
    document.querySelectorAll('table').forEach(table => {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.setAttribute('tabindex', '0');
            row.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    const link = row.querySelector('a');
                    if (link) {
                        link.click();
                    }
                }
            });
        });
    });
}

/**
 * Setup screen reader announcements
 */
function setupScreenReaderAnnouncements() {
    // Create live region for announcements
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-announcements';
    document.body.appendChild(liveRegion);
    
    // Announce form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            announceToScreenReader('Form submitted. Please wait for processing.');
        });
    });
}

/**
 * Announce messages to screen readers
 */
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('live-announcements');
    if (liveRegion) {
        liveRegion.textContent = message;
        
        // Clear after a delay
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }
}

/**
 * Manage focus for better accessibility
 */
function manageFocus() {
    // Store focus before modal opens
    let focusBeforeModal;
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            focusBeforeModal = document.activeElement;
        });
        
        modal.addEventListener('hidden.bs.modal', function() {
            if (focusBeforeModal) {
                focusBeforeModal.focus();
            }
        });
    });
}

/**
 * Add smooth animations and transitions
 */
function initializeAnimations() {
    // Fade in animations for cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Hover effects for interactive elements
    document.querySelectorAll('.btn, .card, .table-hover tbody tr').forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
}

/**
 * Enhanced data table functionality
 */
function initializeDataTables() {
    document.querySelectorAll('table').forEach(table => {
        // Add sorting functionality to headers
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (header.textContent.trim() && !header.querySelector('.sort-icon')) {
                header.style.cursor = 'pointer';
                header.style.userSelect = 'none';
                
                const sortIcon = document.createElement('i');
                sortIcon.className = 'fas fa-sort ms-2 sort-icon text-muted';
                header.appendChild(sortIcon);
                
                header.addEventListener('click', () => sortTable(table, index));
            }
        });
        
        // Add row highlighting
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function() {
                // Remove previous highlights
                rows.forEach(r => r.classList.remove('table-active'));
                // Add highlight to clicked row
                this.classList.add('table-active');
            });
        });
    });
}

/**
 * Sort table by column
 */
function sortTable(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const header = table.querySelectorAll('th')[columnIndex];
    const sortIcon = header.querySelector('.sort-icon');
    
    // Determine sort direction
    const isAscending = sortIcon.classList.contains('fa-sort') || sortIcon.classList.contains('fa-sort-down');
    
    // Reset all sort icons
    table.querySelectorAll('.sort-icon').forEach(icon => {
        icon.className = 'fas fa-sort ms-2 sort-icon text-muted';
    });
    
    // Set current sort icon
    sortIcon.className = `fas fa-sort-${isAscending ? 'up' : 'down'} ms-2 sort-icon text-primary`;
    
    // Sort rows
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as numbers
        const aNum = parseFloat(aText);
        const bNum = parseFloat(bText);
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAscending ? aNum - bNum : bNum - aNum;
        }
        
        // Sort as strings
        return isAscending ? aText.localeCompare(bText) : bText.localeCompare(aText);
    });
    
    // Reorder rows in DOM
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Confirmation dialogs for important actions
 */
function initializeConfirmationDialogs() {
    // Add confirmation to delete actions
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm');
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Add confirmation to form submissions with data loss risk
    document.querySelectorAll('form').forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        let hasChanges = false;
        
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                hasChanges = true;
            });
        });
        
        // Warn before page unload if there are unsaved changes
        window.addEventListener('beforeunload', function(e) {
            if (hasChanges) {
                e.preventDefault();
                e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
                return e.returnValue;
            }
        });
        
        // Clear flag on successful submit
        form.addEventListener('submit', () => {
            hasChanges = false;
        });
    });
}

/**
 * Auto-save functionality for forms
 */
function initializeAutoSave() {
    const autoSaveForms = document.querySelectorAll('[data-autosave="true"]');
    
    autoSaveForms.forEach(form => {
        const formId = form.id || 'autosave-form';
        let autoSaveTimeout;
        
        // Load saved data
        loadAutoSavedData(form, formId);
        
        // Save on input
        form.addEventListener('input', function() {
            clearTimeout(autoSaveTimeout);
            autoSaveTimeout = setTimeout(() => {
                saveFormData(form, formId);
            }, 2000);
        });
        
        // Clear saved data on successful submit
        form.addEventListener('submit', function() {
            clearAutoSavedData(formId);
        });
    });
}

/**
 * Save form data to localStorage
 */
function saveFormData(form, formId) {
    const data = {};
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        if (input.name && input.type !== 'password') {
            data[input.name] = input.value;
        }
    });
    
    try {
        localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
        showAutoSaveIndicator();
    } catch (e) {
        console.warn('Auto-save failed:', e);
    }
}

/**
 * Load auto-saved form data
 */
function loadAutoSavedData(form, formId) {
    try {
        const saved = localStorage.getItem(`autosave_${formId}`);
        if (saved) {
            const data = JSON.parse(saved);
            
            Object.keys(data).forEach(name => {
                const input = form.querySelector(`[name="${name}"]`);
                if (input && input.type !== 'password') {
                    input.value = data[name];
                }
            });
            
            showAutoSaveRestoreNotice();
        }
    } catch (e) {
        console.warn('Auto-save restore failed:', e);
    }
}

/**
 * Clear auto-saved data
 */
function clearAutoSavedData(formId) {
    try {
        localStorage.removeItem(`autosave_${formId}`);
    } catch (e) {
        console.warn('Auto-save clear failed:', e);
    }
}

/**
 * Show auto-save indicator
 */
function showAutoSaveIndicator() {
    let indicator = document.getElementById('autosave-indicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'autosave-indicator';
        indicator.className = 'position-fixed bottom-0 end-0 m-3 alert alert-success alert-sm fade show';
        indicator.style.zIndex = '9999';
        indicator.innerHTML = '<i class="fas fa-check-circle me-2"></i>Auto-saved';
        document.body.appendChild(indicator);
    }
    
    // Show and hide after delay
    indicator.classList.add('show');
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 2000);
}

/**
 * Show auto-save restore notice
 */
function showAutoSaveRestoreNotice() {
    const notice = document.createElement('div');
    notice.className = 'alert alert-info alert-dismissible fade show';
    notice.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>
        Previous form data has been restored.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const firstForm = document.querySelector('form');
    if (firstForm) {
        firstForm.parentNode.insertBefore(notice, firstForm);
    }
}

/**
 * Real-time updates for dynamic content
 */
function initializeRealTimeUpdates() {
    // Check for updates periodically (for audit logs, etc.)
    if (window.location.pathname.includes('audit-logs')) {
        setInterval(updateAuditLogs, 30000); // Every 30 seconds
    }
    
    // Update timestamps to relative time
    updateRelativeTimestamps();
    setInterval(updateRelativeTimestamps, 60000); // Every minute
}

/**
 * Update audit logs if on that page
 */
function updateAuditLogs() {
    // Only update if no user interaction recently
    const lastInteraction = Date.now() - (window.lastUserInteraction || 0);
    if (lastInteraction > 30000) { // 30 seconds of inactivity
        // In a real application, this would fetch new data via AJAX
        console.log('Checking for audit log updates...');
    }
}

/**
 * Update timestamps to show relative time
 */
function updateRelativeTimestamps() {
    document.querySelectorAll('[data-timestamp]').forEach(element => {
        const timestamp = new Date(element.getAttribute('data-timestamp'));
        const now = new Date();
        const diff = now - timestamp;
        
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);
        
        let relativeTime;
        if (minutes < 1) {
            relativeTime = 'Just now';
        } else if (minutes < 60) {
            relativeTime = `${minutes} minute${minutes !== 1 ? 's' : ''} ago`;
        } else if (hours < 24) {
            relativeTime = `${hours} hour${hours !== 1 ? 's' : ''} ago`;
        } else {
            relativeTime = `${days} day${days !== 1 ? 's' : ''} ago`;
        }
        
        element.textContent = relativeTime;
        element.setAttribute('title', timestamp.toLocaleString());
    });
}

// Track user interactions for real-time update decisions
document.addEventListener('click', () => {
    window.lastUserInteraction = Date.now();
});

document.addEventListener('keydown', () => {
    window.lastUserInteraction = Date.now();
});

/**
 * Utility functions
 */

// Debounce function for performance optimization
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Throttle function for scroll events
function throttle(func, delay) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => (inThrottle = false), delay);
        }
    };
}

// Show loading spinner
function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner-border spinner-border-sm me-2';
    spinner.setAttribute('role', 'status');
    
    const originalContent = element.innerHTML;
    element.innerHTML = '';
    element.appendChild(spinner);
    element.appendChild(document.createTextNode('Loading...'));
    element.disabled = true;
    
    return () => {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Export functions for use in inline scripts
window.HealthcarePlatform = {
    showLoading,
    formatCurrency,
    formatDate,
    announceToScreenReader,
    debounce,
    throttle
};

console.log('Healthcare Management Platform JavaScript loaded successfully');
