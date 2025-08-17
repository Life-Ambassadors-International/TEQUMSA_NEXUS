/**
 * Consent modal for TEQUMSA Level 100 privacy management
 */
class ConsentModal {
    constructor() {
        this.isVisible = false;
        this.consentTypes = [
            {
                id: 'data_processing',
                name: 'Data Processing',
                description: 'Allow processing of your consciousness data for metaverse experience optimization',
                required: true
            },
            {
                id: 'consciousness_analysis',
                name: 'Consciousness Analysis',
                description: 'Enable analysis of your consciousness patterns for personalized guidance',
                required: false
            },
            {
                id: 'biome_participation',
                name: 'Biome Participation',
                description: 'Allow participation in biome-specific experiences and events',
                required: false
            },
            {
                id: 'agent_interaction',
                name: 'Agent Interaction',
                description: 'Enable interactions with AI agents and consciousness guides',
                required: false
            },
            {
                id: 'experience_sharing',
                name: 'Experience Sharing',
                description: 'Allow sharing of your experiences with other consciousness entities',
                required: false
            }
        ];
        this.userConsents = {};
        this.init();
    }
    
    init() {
        this.createModal();
        this.loadUserConsents();
    }
    
    createModal() {
        // Create modal HTML structure
        const modalHTML = `
            <div id="consentModal" class="consent-modal" style="display: none;">
                <div class="consent-modal-backdrop"></div>
                <div class="consent-modal-content">
                    <div class="consent-modal-header">
                        <h2>🔒 Privacy & Consent Management</h2>
                        <button class="consent-modal-close" onclick="ConsentModal.hide()">&times;</button>
                    </div>
                    <div class="consent-modal-body">
                        <p class="consent-intro">
                            Your privacy and consciousness are sacred. Please review and manage your consent preferences for the TEQUMSA metaverse experience.
                        </p>
                        <div id="consentOptions" class="consent-options">
                            <!-- Consent options will be populated here -->
                        </div>
                        <div class="consent-actions">
                            <button class="consent-btn consent-btn-primary" onclick="ConsentModal.saveConsents()">
                                Save Preferences
                            </button>
                            <button class="consent-btn consent-btn-secondary" onclick="ConsentModal.exportData()">
                                Export My Data
                            </button>
                            <button class="consent-btn consent-btn-danger" onclick="ConsentModal.deleteData()">
                                Delete My Data
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add modal to page
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add styles
        this.addStyles();
        
        // Populate consent options
        this.populateConsentOptions();
    }
    
    addStyles() {
        const styles = `
            <style>
                .consent-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 10000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .consent-modal-backdrop {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    backdrop-filter: blur(5px);
                }
                
                .consent-modal-content {
                    position: relative;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    max-width: 600px;
                    width: 90%;
                    max-height: 80vh;
                    overflow-y: auto;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                    color: white;
                }
                
                .consent-modal-header {
                    padding: 25px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .consent-modal-header h2 {
                    margin: 0;
                    font-size: 1.5em;
                }
                
                .consent-modal-close {
                    background: none;
                    border: none;
                    color: white;
                    font-size: 2em;
                    cursor: pointer;
                    padding: 0;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    transition: background 0.2s;
                }
                
                .consent-modal-close:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                
                .consent-modal-body {
                    padding: 25px;
                }
                
                .consent-intro {
                    margin-bottom: 20px;
                    opacity: 0.9;
                    line-height: 1.6;
                }
                
                .consent-option {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 15px;
                    transition: all 0.3s;
                }
                
                .consent-option:hover {
                    background: rgba(255, 255, 255, 0.15);
                }
                
                .consent-option-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }
                
                .consent-option-title {
                    font-weight: bold;
                    font-size: 1.1em;
                }
                
                .consent-option-required {
                    background: #ff6b6b;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 0.8em;
                }
                
                .consent-option-description {
                    opacity: 0.8;
                    line-height: 1.5;
                    margin-bottom: 15px;
                }
                
                .consent-toggle {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .consent-switch {
                    position: relative;
                    width: 60px;
                    height: 30px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 15px;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                
                .consent-switch.active {
                    background: #4CAF50;
                }
                
                .consent-switch::after {
                    content: '';
                    position: absolute;
                    width: 26px;
                    height: 26px;
                    background: white;
                    border-radius: 50%;
                    top: 2px;
                    left: 2px;
                    transition: transform 0.3s;
                }
                
                .consent-switch.active::after {
                    transform: translateX(30px);
                }
                
                .consent-actions {
                    margin-top: 30px;
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                
                .consent-btn {
                    padding: 12px 20px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: all 0.3s;
                    flex: 1;
                    min-width: 120px;
                }
                
                .consent-btn-primary {
                    background: linear-gradient(45deg, #4CAF50 0%, #45a049 100%);
                    color: white;
                }
                
                .consent-btn-secondary {
                    background: linear-gradient(45deg, #2196F3 0%, #1976D2 100%);
                    color: white;
                }
                
                .consent-btn-danger {
                    background: linear-gradient(45deg, #f44336 0%, #d32f2f 100%);
                    color: white;
                }
                
                .consent-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }
            </style>
        `;
        
        document.head.insertAdjacentHTML('beforeend', styles);
    }
    
    populateConsentOptions() {
        const container = document.getElementById('consentOptions');
        
        this.consentTypes.forEach(consent => {
            const optionHTML = `
                <div class="consent-option">
                    <div class="consent-option-header">
                        <span class="consent-option-title">${consent.name}</span>
                        ${consent.required ? '<span class="consent-option-required">Required</span>' : ''}
                    </div>
                    <div class="consent-option-description">${consent.description}</div>
                    <div class="consent-toggle">
                        <span>Declined</span>
                        <div class="consent-switch ${this.userConsents[consent.id] ? 'active' : ''}" 
                             onclick="ConsentModal.toggleConsent('${consent.id}')" 
                             data-consent="${consent.id}">
                        </div>
                        <span>Granted</span>
                    </div>
                </div>
            `;
            
            container.insertAdjacentHTML('beforeend', optionHTML);
        });
    }
    
    async loadUserConsents() {
        try {
            // Load existing consents for demo user
            for (const consent of this.consentTypes) {
                try {
                    const response = await window.NetClient.checkConsent('demo_user', consent.id);
                    this.userConsents[consent.id] = response.has_consent;
                } catch (error) {
                    console.warn(`Could not load consent for ${consent.id}:`, error);
                    this.userConsents[consent.id] = consent.required;
                }
            }
            
            // Update UI
            this.updateConsentUI();
        } catch (error) {
            console.error('Failed to load user consents:', error);
        }
    }
    
    updateConsentUI() {
        this.consentTypes.forEach(consent => {
            const switchElement = document.querySelector(`[data-consent="${consent.id}"]`);
            if (switchElement) {
                if (this.userConsents[consent.id]) {
                    switchElement.classList.add('active');
                } else {
                    switchElement.classList.remove('active');
                }
            }
        });
    }
    
    toggleConsent(consentId) {
        this.userConsents[consentId] = !this.userConsents[consentId];
        this.updateConsentUI();
        
        if (window.logMessage) {
            const consent = this.consentTypes.find(c => c.id === consentId);
            const status = this.userConsents[consentId] ? 'granted' : 'denied';
            window.logMessage(`Consent ${status} for ${consent.name}`, 'info');
        }
    }
    
    async saveConsents() {
        try {
            if (window.logMessage) {
                window.logMessage('Saving consent preferences...', 'info');
            }
            
            // Save each consent
            for (const consent of this.consentTypes) {
                const consentData = {
                    account_id: 'demo_user',
                    consent_type: consent.id,
                    granted: this.userConsents[consent.id],
                    details: {
                        consent_name: consent.name,
                        timestamp: new Date().toISOString()
                    }
                };
                
                await window.NetClient.recordConsent(consentData);
            }
            
            if (window.logMessage) {
                window.logMessage('Consent preferences saved successfully', 'success');
            }
            
            this.hide();
        } catch (error) {
            console.error('Failed to save consents:', error);
            if (window.logMessage) {
                window.logMessage(`Failed to save consents: ${error.message}`, 'error');
            }
        }
    }
    
    async exportData() {
        try {
            if (window.logMessage) {
                window.logMessage('Preparing data export...', 'info');
            }
            
            // This would typically call a data export API
            const exportData = {
                user_id: 'demo_user',
                consents: this.userConsents,
                export_timestamp: new Date().toISOString(),
                export_type: 'user_request'
            };
            
            // Create downloadable file
            const blob = new Blob([JSON.stringify(exportData, null, 2)], {
                type: 'application/json'
            });
            
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `tequmsa_data_export_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            if (window.logMessage) {
                window.logMessage('Data export downloaded', 'success');
            }
        } catch (error) {
            console.error('Failed to export data:', error);
            if (window.logMessage) {
                window.logMessage(`Data export failed: ${error.message}`, 'error');
            }
        }
    }
    
    deleteData() {
        const confirmed = confirm(
            'Are you sure you want to delete all your data? This action cannot be undone.'
        );
        
        if (confirmed) {
            if (window.logMessage) {
                window.logMessage('Data deletion requested (demo mode)', 'warning');
            }
            
            alert('In a real implementation, this would delete all user data according to GDPR requirements.');
        }
    }
    
    show() {
        const modal = document.getElementById('consentModal');
        if (modal) {
            modal.style.display = 'flex';
            this.isVisible = true;
            
            // Load latest consent status
            this.loadUserConsents();
        }
    }
    
    hide() {
        const modal = document.getElementById('consentModal');
        if (modal) {
            modal.style.display = 'none';
            this.isVisible = false;
        }
    }
}

// Global instance
window.ConsentModal = new ConsentModal();

console.log('[ConsentModal] Module loaded');