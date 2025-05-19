// League Auto Login App JavaScript

// Initialize app when window is loaded
window.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, waiting for pywebview...');
    
    // Try to initialize directly
    initApp();
    
    // Also try the pywebview_ready event
    window.addEventListener('pywebviewready', () => {
        console.log('PyWebView ready event triggered');
        initApp();
    });
});

// Initialize the application
function initApp() {
    console.log('Initializing app...');
    
    loadAccounts();
    loadRegions();
    setupEventListeners();
}

// API wrapper to support both pywebview and REST fallback
const api = {
    async get_accounts() {
        if (window.pywebview) {
            try {
                return await window.pywebview.api.get_accounts();
            } catch (err) {
                console.error('PyWebView API error (fallback to REST):', err);
            }
        }
        
        // Fallback to REST API
        const response = await fetch('http://localhost:8000/api/accounts');
        return await response.json();
    },
    
    async get_regions() {
        if (window.pywebview) {
            try {
                return await window.pywebview.api.get_regions();
            } catch (err) {
                console.error('PyWebView API error (fallback to REST):', err);
            }
        }
        
        // Fallback to REST API
        const response = await fetch('http://localhost:8000/api/regions');
        return await response.json();
    },
    
    async save_account(username, password, region) {
        if (window.pywebview) {
            try {
                return await window.pywebview.api.save_account(username, password, region);
            } catch (err) {
                console.error('PyWebView API error (fallback to REST):', err);
            }
        }
        
        // Fallback to REST API
        const response = await fetch('http://localhost:8000/api/account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password, region })
        });
        return await response.json();
    },
    
    async delete_account(username) {
        if (window.pywebview) {
            try {
                return await window.pywebview.api.delete_account(username);
            } catch (err) {
                console.error('PyWebView API error (fallback to REST):', err);
            }
        }
        
        // Fallback to REST API
        const response = await fetch(`http://localhost:8000/api/account/${username}`, {
            method: 'DELETE'
        });
        return await response.json();
    },
    
    async login_to_client(username) {
        if (window.pywebview) {
            try {
                // Try to minimize window first
                try {
                    await window.pywebview.api.minimize_window();
                } catch (err) {
                    console.error('Error minimizing window:', err);
                }
                
                return await window.pywebview.api.login_to_client(username);
            } catch (err) {
                console.error('PyWebView API error (fallback to REST):', err);
            }
        }
        
        // Fallback to REST API
        const response = await fetch(`http://localhost:8000/api/login/${username}`, {
            method: 'POST'
        });
        return await response.json();
    },
    
    async minimize_window() {
        if (window.pywebview) {
            try {
                return await window.pywebview.api.minimize_window();
            } catch (err) {
                console.error('Error minimizing window:', err);
            }
        }
        
        // No fallback for this one
        return { success: false, message: 'Minimize not available in REST mode' };
    }
};

// Load accounts from backend
async function loadAccounts() {
    console.log('Loading accounts...');
    try {
        const accounts = await api.get_accounts();
        console.log('Accounts loaded:', accounts);
        const accountSelect = document.getElementById('account-select');
        
        // Clear current options
        accountSelect.innerHTML = '<option value="" disabled selected>Select an account</option>';
        
        // Add accounts
        accounts.forEach(account => {
            const option = document.createElement('option');
            option.value = account.username;
            option.textContent = `${account.username} (${account.region})`;
            accountSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading accounts:', error);
        showNotification(`Error loading accounts: ${error}`, true);
    }
}

// Load regions from backend
async function loadRegions() {
    console.log('Loading regions...');
    try {
        const regions = await api.get_regions();
        console.log('Regions loaded:', regions);
        const regionSelect = document.getElementById('region');
        
        // Clear current options
        regionSelect.innerHTML = '';
        
        // Add regions
        regions.forEach(region => {
            const option = document.createElement('option');
            option.value = region;
            option.textContent = region;
            regionSelect.appendChild(option);
        });
        
        // Select first region
        if (regions.length > 0) {
            regionSelect.value = regions[0];
        }
    } catch (error) {
        console.error('Error loading regions:', error);
        showNotification(`Error loading regions: ${error}`, true);
    }
}

// Set up event listeners
function setupEventListeners() {
    console.log('Setting up event listeners...');
    // Account selection change
    document.getElementById('account-select').addEventListener('change', onAccountSelect);
    
    // Save button
    document.getElementById('save-btn').addEventListener('click', saveAccount);
    
    // Delete button
    document.getElementById('delete-btn').addEventListener('click', deleteAccount);
    
    // Login button
    document.getElementById('login-btn').addEventListener('click', loginToClient);
    
    // Notification close button
    document.getElementById('notification-close').addEventListener('click', hideNotification);
}

// Handle account selection
async function onAccountSelect(event) {
    const username = event.target.value;
    if (!username) return;
    
    try {
        const accounts = await api.get_accounts();
        const account = accounts.find(acc => acc.username === username);
        
        if (account) {
            document.getElementById('username').value = account.username;
            document.getElementById('password').value = account.password;
            document.getElementById('region').value = account.region;
        }
    } catch (error) {
        showNotification(`Error loading account details: ${error}`, true);
    }
}

// Save account
async function saveAccount() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const region = document.getElementById('region').value;
    
    if (!username || !password || !region) {
        showNotification('Please fill in all fields', true);
        return;
    }
    
    try {
        const result = await api.save_account(username, password, region);
        if (result.success) {
            showNotification(result.message);
            await loadAccounts();
            
            // Select the newly saved account
            const accountSelect = document.getElementById('account-select');
            for (let i = 0; i < accountSelect.options.length; i++) {
                if (accountSelect.options[i].value === username) {
                    accountSelect.selectedIndex = i;
                    break;
                }
            }
        } else {
            showNotification(result.message, true);
        }
    } catch (error) {
        showNotification(`Error saving account: ${error}`, true);
    }
}

// Delete account confirmation
function showDeleteConfirmation(username, callback) {
    const dialog = document.getElementById('confirm-dialog');
    const message = document.getElementById('confirm-message');
    const okButton = document.getElementById('confirm-ok');
    const cancelButton = document.getElementById('confirm-cancel');
    
    // Set message
    message.textContent = `Are you sure you want to delete account "${username}"?`;
    
    // Show dialog
    dialog.classList.remove('hidden');
    
    // Set up event handlers
    const handleOk = async () => {
        // Clean up event listeners
        okButton.removeEventListener('click', handleOk);
        cancelButton.removeEventListener('click', handleCancel);
        
        // Hide dialog
        dialog.classList.add('hidden');
        
        // Call callback
        if (callback) callback(true);
    };
    
    const handleCancel = () => {
        // Clean up event listeners
        okButton.removeEventListener('click', handleOk);
        cancelButton.removeEventListener('click', handleCancel);
        
        // Hide dialog
        dialog.classList.add('hidden');
        
        // Call callback
        if (callback) callback(false);
    };
    
    // Add event listeners
    okButton.addEventListener('click', handleOk);
    cancelButton.addEventListener('click', handleCancel);
}

// Delete account
async function deleteAccount() {
    const username = document.getElementById('username').value.trim();
    
    if (!username) {
        showNotification('Please select an account to delete', true);
        return;
    }
    
    // Show confirmation dialog
    showDeleteConfirmation(username, async (confirmed) => {
        if (!confirmed) return;
        
        try {
            const result = await api.delete_account(username);
            if (result.success) {
                showNotification(result.message);
                clearForm();
                await loadAccounts();
            } else {
                showNotification(result.message, true);
            }
        } catch (error) {
            showNotification(`Error deleting account: ${error}`, true);
        }
    });
}

// Login to League client
async function loginToClient() {
    const selectedAccount = document.getElementById('account-select').value;
    
    if (!selectedAccount) {
        showNotification('Please select an account to login', true);
        return;
    }
    
    try {
        showNotification('Attempting to login... please wait');
        
        // Minimize the window before login
        await api.minimize_window();
        
        const result = await api.login_to_client(selectedAccount);
        if (result.success) {
            showNotification(result.message);
        } else {
            showNotification(result.message, true);
        }
    } catch (error) {
        showNotification(`Error during login: ${error}`, true);
    }
}

// Clear form inputs
function clearForm() {
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('account-select').selectedIndex = 0;
}

// Show notification
function showNotification(message, isError = false) {
    console.log(`Notification: ${message} (Error: ${isError})`);
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    
    messageElement.textContent = message;
    notification.classList.remove('hidden');
    
    if (isError) {
        notification.classList.add('error');
    } else {
        notification.classList.remove('error');
    }
    
    // Auto-hide after 5 seconds
    setTimeout(hideNotification, 5000);
}

// Hide notification
function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('hidden');
} 