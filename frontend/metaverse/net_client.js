/**
 * Network client for TEQUMSA Level 100 metaverse communication
 */
class NetClient {
    constructor() {
        this.baseUrl = window.location.origin;
        this.connected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.heartbeatInterval = null;
    }
    
    async connect() {
        try {
            console.log('[NetClient] Connecting to TEQUMSA backend...');
            
            // Test connection with health check
            const response = await fetch(`${this.baseUrl}/health`);
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.connected = true;
                this.reconnectAttempts = 0;
                this.startHeartbeat();
                
                console.log('[NetClient] Connected successfully');
                this.onConnected();
                return true;
            } else {
                throw new Error('Backend unhealthy');
            }
        } catch (error) {
            console.error('[NetClient] Connection failed:', error);
            this.connected = false;
            this.onDisconnected();
            this.scheduleReconnect();
            return false;
        }
    }
    
    disconnect() {
        this.connected = false;
        this.stopHeartbeat();
        console.log('[NetClient] Disconnected');
        this.onDisconnected();
    }
    
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            this.ping();
        }, 30000); // 30 seconds
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }
    
    async ping() {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            if (!response.ok) {
                throw new Error('Ping failed');
            }
        } catch (error) {
            console.error('[NetClient] Heartbeat failed:', error);
            this.connected = false;
            this.onDisconnected();
            this.scheduleReconnect();
        }
    }
    
    scheduleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            
            console.log(`[NetClient] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        } else {
            console.error('[NetClient] Max reconnection attempts reached');
        }
    }
    
    async apiCall(endpoint, options = {}) {
        if (!this.connected) {
            throw new Error('Not connected to TEQUMSA network');
        }
        
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        const mergedOptions = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, mergedOptions);
            
            if (!response.ok) {
                throw new Error(`API call failed: ${response.status} ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error(`[NetClient] API call to ${endpoint} failed:`, error);
            throw error;
        }
    }
    
    // World state operations
    async getWorldState(regionId) {
        return this.apiCall(`/world/regions/${regionId}/state`);
    }
    
    async applyPatch(patchData) {
        return this.apiCall('/world/patches', {
            method: 'POST',
            body: JSON.stringify(patchData)
        });
    }
    
    // Group operations
    async syncGroup(syncData) {
        return this.apiCall('/group/sync', {
            method: 'POST',
            body: JSON.stringify(syncData)
        });
    }
    
    // Subscription operations
    async getEntitlements(accountId) {
        return this.apiCall(`/subscriptions/${accountId}/entitlements`);
    }
    
    async checkPermission(accountId, permission) {
        return this.apiCall(`/subscriptions/${accountId}/check-permission`, {
            method: 'POST',
            body: JSON.stringify({ permission })
        });
    }
    
    // Consent operations
    async recordConsent(consentData) {
        return this.apiCall('/consent/record', {
            method: 'POST',
            body: JSON.stringify(consentData)
        });
    }
    
    async checkConsent(accountId, consentType) {
        return this.apiCall(`/consent/${accountId}/check/${consentType}`);
    }
    
    // Biome operations
    async listBiomes() {
        return this.apiCall('/biomes');
    }
    
    async getBiomeInfo(biomeId) {
        return this.apiCall(`/biomes/${biomeId}`);
    }
    
    async activateBiome(biomeId, activationData) {
        return this.apiCall(`/biomes/${biomeId}/activate`, {
            method: 'POST',
            body: JSON.stringify(activationData)
        });
    }
    
    // Orchestrator operations
    async getOrchestratorStatus() {
        return this.apiCall('/orchestrator/status');
    }
    
    async submitJob(jobData) {
        return this.apiCall('/orchestrator/jobs', {
            method: 'POST',
            body: JSON.stringify(jobData)
        });
    }
    
    // Coherence field operations
    async getGlobalCoherence() {
        return this.apiCall('/coherence/global');
    }
    
    // Event handlers (override in implementation)
    onConnected() {
        if (window.updateConnectionStatus) {
            window.updateConnectionStatus(true);
        }
    }
    
    onDisconnected() {
        if (window.updateConnectionStatus) {
            window.updateConnectionStatus(false);
        }
    }
    
    onError(error) {
        console.error('[NetClient] Error:', error);
        if (window.logMessage) {
            window.logMessage(`Network error: ${error.message}`, 'error');
        }
    }
}

// Global instance
window.NetClient = new NetClient();

// Auto-connect when loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('[NetClient] Module loaded');
});