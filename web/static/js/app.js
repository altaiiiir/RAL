// Global state
let accounts = [];
let regions = [];
let currentAccount = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('Initializing app...');
    
    // Setup event listeners
    setupEventListeners();
    
    // Wait for pywebview to be ready
    if (window.pywebview) {
        onPyWebViewReady();
    } else {
        // Wait for pywebview ready event
        window.addEventListener('pywebviewready', onPyWebViewReady);
    }
}

function onPyWebViewReady() {
    console.log('PyWebView is ready');
    loadAccounts();
    loadRegions();
}

function setupEventListeners() {
    // Window controls
    document.getElementById('minimize-btn').addEventListener('click', minimizeWindow);
    document.getElementById('close-btn').addEventListener('click', closeWindow);
    
    // Account selection
    document.getElementById('account-select').addEventListener('change', onAccountSelect);
    document.getElementById('login-btn').addEventListener('click', loginToClient);
    
    // Form actions
    document.getElementById('save-btn').addEventListener('click', saveAccount);
    document.getElementById('delete-btn').addEventListener('click', deleteAccount);
    
    // Notification close
    document.getElementById('notification-close').addEventListener('click', hideNotification);
    
    // Confirmation dialog
    document.getElementById('confirm-cancel').addEventListener('click', hideConfirmDialog);
    document.getElementById('confirm-ok').addEventListener('click', confirmDelete);
    
    // Clear form when username changes
    document.getElementById('username').addEventListener('input', clearForm);
}

function loadAccounts() {
    if (!window.pywebview || !window.pywebview.api) {
        console.error('PyWebView API not available');
        return;
    }
    
    window.pywebview.api.get_accounts().then(function(result) {
        console.log('Loaded accounts:', result);
        accounts = result || [];
        updateAccountSelect();
    }).catch(function(error) {
        console.error('Error loading accounts:', error);
        showNotification('Error loading accounts: ' + error.message, 'error');
    });
}

function loadRegions() {
    if (!window.pywebview || !window.pywebview.api) {
        console.error('PyWebView API not available');
        return;
    }
    
    window.pywebview.api.get_regions().then(function(result) {
        console.log('Loaded regions:', result);
        regions = result || [];
        updateRegionSelect();
    }).catch(function(error) {
        console.error('Error loading regions:', error);
        showNotification('Error loading regions: ' + error.message, 'error');
    });
}

function updateAccountSelect() {
    const select = document.getElementById('account-select');
    
    // Clear existing options except the first one
    while (select.children.length > 1) {
        select.removeChild(select.lastChild);
    }
    
    // Add account options
    accounts.forEach(function(account) {
        const option = document.createElement('option');
        option.value = account.username;
        option.textContent = `${account.username} (${account.region})`;
        select.appendChild(option);
    });
}

function updateRegionSelect() {
    const select = document.getElementById('region');
    
    // Clear existing options
    select.innerHTML = '';
    
    // Add region options
    regions.forEach(function(region) {
        const option = document.createElement('option');
        option.value = region.code;
        option.textContent = region.name;
        select.appendChild(option);
    });
}

function onAccountSelect() {
    const select = document.getElementById('account-select');
    const selectedUsername = select.value;
    
    if (selectedUsername) {
        currentAccount = accounts.find(acc => acc.username === selectedUsername);
        if (currentAccount) {
            // Fill form with account details
            document.getElementById('username').value = currentAccount.username;
            document.getElementById('password').value = currentAccount.password;
            document.getElementById('region').value = currentAccount.region;
        }
    } else {
        clearForm();
    }
}

function clearForm() {
    if (document.getElementById('account-select').value === '') {
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        document.getElementById('region').value = '';
        currentAccount = null;
    }
}

function saveAccount() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const region = document.getElementById('region').value;
    
    if (!username || !password || !region) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    if (!window.pywebview || !window.pywebview.api) {
        showNotification('PyWebView API not available', 'error');
        return;
    }
    
    window.pywebview.api.save_account(username, password, region).then(function(result) {
        console.log('Save result:', result);
        if (result.success) {
            showNotification('Account saved successfully', 'success');
            loadAccounts(); // Reload accounts
            
            // Select the saved account
            setTimeout(function() {
                document.getElementById('account-select').value = username;
            }, 100);
        } else {
            showNotification('Error saving account: ' + result.message, 'error');
        }
    }).catch(function(error) {
        console.error('Error saving account:', error);
        showNotification('Error saving account: ' + error.message, 'error');
    });
}

function deleteAccount() {
    if (!currentAccount) {
        showNotification('Please select an account to delete', 'error');
        return;
    }
    
    // Show confirmation dialog
    document.getElementById('confirm-message').textContent = 
        `Are you sure you want to delete the account "${currentAccount.username}"?`;
    showConfirmDialog();
}

function confirmDelete() {
    if (!currentAccount || !window.pywebview || !window.pywebview.api) {
        hideConfirmDialog();
        return;
    }
    
    window.pywebview.api.delete_account(currentAccount.username).then(function(result) {
        console.log('Delete result:', result);
        hideConfirmDialog();
        
        if (result.success) {
            showNotification('Account deleted successfully', 'success');
            loadAccounts(); // Reload accounts
            clearForm();
            document.getElementById('account-select').value = '';
            currentAccount = null;
        } else {
            showNotification('Error deleting account: ' + result.message, 'error');
        }
    }).catch(function(error) {
        console.error('Error deleting account:', error);
        hideConfirmDialog();
        showNotification('Error deleting account: ' + error.message, 'error');
    });
}

function loginToClient() {
    const selectedUsername = document.getElementById('account-select').value;
    
    if (!selectedUsername) {
        showNotification('Please select an account to login', 'error');
        return;
    }
    
    if (!window.pywebview || !window.pywebview.api) {
        showNotification('PyWebView API not available', 'error');
        return;
    }
    
    showNotification('Logging in...', 'info');
    
    window.pywebview.api.login_to_client(selectedUsername).then(function(result) {
        console.log('Login result:', result);
        if (result.success) {
            showNotification('Login successful!', 'success');
        } else {
            showNotification('Login failed: ' + result.message, 'error');
        }
    }).catch(function(error) {
        console.error('Error during login:', error);
        showNotification('Login error: ' + error.message, 'error');
    });
}

function minimizeWindow() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.minimize_window().catch(function(error) {
            console.error('Error minimizing window:', error);
        });
    }
}

function closeWindow() {
    if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.close_window().catch(function(error) {
            console.error('Error closing window:', error);
        });
    }
}

function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    const messageElement = document.getElementById('notification-message');
    
    messageElement.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');
    
    // Auto hide after 5 seconds for success/info messages
    if (type === 'success' || type === 'info') {
        setTimeout(hideNotification, 5000);
    }
}

function hideNotification() {
    const notification = document.getElementById('notification');
    notification.classList.add('hidden');
}

function showConfirmDialog() {
    const dialog = document.getElementById('confirm-dialog');
    dialog.classList.remove('hidden');
}

function hideConfirmDialog() {
    const dialog = document.getElementById('confirm-dialog');
    dialog.classList.add('hidden');
}

// PyWebView bridge function
window.onbridge = function() {
    console.log('PyWebView bridge ready');
    onPyWebViewReady();
}; 