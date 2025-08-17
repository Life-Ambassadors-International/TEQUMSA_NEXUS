/**
 * Orchestrator client for TEQUMSA Level 100 system management
 */
class OrchestratorClient {
    constructor() {
        this.status = null;
        this.jobs = new Map();
        this.updateInterval = null;
        this.init();
    }
    
    init() {
        this.startStatusUpdates();
    }
    
    startStatusUpdates() {
        // Update orchestrator status every 10 seconds
        this.updateInterval = setInterval(() => {
            this.updateStatus();
        }, 10000);
        
        // Initial update
        this.updateStatus();
    }
    
    stopStatusUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
    
    async updateStatus() {
        if (!window.NetClient || !window.NetClient.connected) {
            return;
        }
        
        try {
            this.status = await window.NetClient.getOrchestratorStatus();
            this.onStatusUpdate(this.status);
        } catch (error) {
            console.error('[OrchestratorClient] Failed to update status:', error);
        }
    }
    
    async submitJob(jobType, priority = 0, metadata = {}) {
        if (!window.NetClient || !window.NetClient.connected) {
            throw new Error('Not connected to TEQUMSA network');
        }
        
        const jobData = {
            job_type: jobType,
            priority: priority,
            metadata: metadata
        };
        
        try {
            const response = await window.NetClient.submitJob(jobData);
            
            if (response.job_id) {
                this.jobs.set(response.job_id, {
                    ...jobData,
                    job_id: response.job_id,
                    status: 'submitted',
                    submitted_at: Date.now()
                });
                
                console.log(`[OrchestratorClient] Job submitted: ${response.job_id}`);
                return response.job_id;
            }
        } catch (error) {
            console.error('[OrchestratorClient] Job submission failed:', error);
            throw error;
        }
    }
    
    // Convenience methods for common job types
    async activateBiome(biomeId, regionId) {
        return this.submitJob('biome_activation', 5, {
            biome_id: biomeId,
            region_id: regionId
        });
    }
    
    async spawnEntity(entityType, regionId, count = 1) {
        return this.submitJob('entity_spawn', 3, {
            entity_type: entityType,
            region_id: regionId,
            count: count
        });
    }
    
    async performMaintenance() {
        return this.submitJob('system_maintenance', 1, {
            maintenance_type: 'routine'
        });
    }
    
    async syncConsciousness(regionId = null) {
        return this.submitJob('consciousness_sync', 4, {
            region_id: regionId
        });
    }
    
    // Status monitoring
    onStatusUpdate(status) {
        if (window.logMessage) {
            const stats = status.stats;
            const jobCounts = status.job_counts;
            
            // Log significant changes
            if (stats.last_error) {
                window.logMessage(`Orchestrator error: ${stats.last_error}`, 'error');
            }
            
            // Update UI if elements exist
            this.updateStatusUI(status);
        }
    }
    
    updateStatusUI(status) {
        // Update orchestrator status display if element exists
        const statusElement = document.getElementById('orchestratorStatus');
        if (statusElement) {
            const isRunning = status.running;
            statusElement.innerHTML = `
                <div class="status-indicator ${isRunning ? 'status-online' : 'status-offline'}"></div>
                <span>${isRunning ? 'Online' : 'Offline'}</span>
            `;
        }
        
        // Update job counts
        const jobCountsElement = document.getElementById('jobCounts');
        if (jobCountsElement) {
            const counts = status.job_counts;
            jobCountsElement.innerHTML = `
                <div>Pending: ${counts.pending || 0}</div>
                <div>Running: ${counts.running || 0}</div>
                <div>Completed: ${counts.completed || 0}</div>
                <div>Failed: ${counts.failed || 0}</div>
            `;
        }
        
        // Update stats
        const statsElement = document.getElementById('orchestratorStats');
        if (statsElement) {
            const stats = status.stats;
            statsElement.innerHTML = `
                <div>Patches Processed: ${stats.patches_processed || 0}</div>
                <div>Jobs Completed: ${stats.jobs_completed || 0}</div>
                <div>Uptime: ${Math.round((stats.uptime_seconds || 0) / 60)} minutes</div>
                <div>Active Biomes: ${status.biome_stats || 0}</div>
            `;
        }
    }
    
    // Biome management
    async getBiomeList() {
        if (!window.NetClient || !window.NetClient.connected) {
            throw new Error('Not connected to TEQUMSA network');
        }
        
        try {
            const response = await window.NetClient.listBiomes();
            return response.biomes || [];
        } catch (error) {
            console.error('[OrchestratorClient] Failed to get biome list:', error);
            throw error;
        }
    }
    
    async getBiomeInfo(biomeId) {
        if (!window.NetClient || !window.NetClient.connected) {
            throw new Error('Not connected to TEQUMSA network');
        }
        
        try {
            return await window.NetClient.getBiomeInfo(biomeId);
        } catch (error) {
            console.error(`[OrchestratorClient] Failed to get biome info for ${biomeId}:`, error);
            throw error;
        }
    }
    
    // Job monitoring
    getJobStatus(jobId) {
        return this.jobs.get(jobId);
    }
    
    getJobsByType(jobType) {
        const jobs = [];
        for (const job of this.jobs.values()) {
            if (job.job_type === jobType) {
                jobs.push(job);
            }
        }
        return jobs;
    }
    
    // System utilities
    getSystemHealth() {
        if (!this.status) {
            return 'unknown';
        }
        
        const isRunning = this.status.running;
        const hasErrors = this.status.stats.last_error;
        const jobCounts = this.status.job_counts;
        
        if (!isRunning) {
            return 'critical';
        }
        
        if (hasErrors) {
            return 'warning';
        }
        
        if (jobCounts.failed > jobCounts.completed * 0.1) {
            return 'warning';
        }
        
        return 'healthy';
    }
    
    getHealthColor() {
        const health = this.getSystemHealth();
        const colors = {
            'healthy': '#4CAF50',
            'warning': '#FF9800',
            'critical': '#F44336',
            'unknown': '#9E9E9E'
        };
        return colors[health] || colors.unknown;
    }
    
    // Auto-management
    enableAutoMaintenance(intervalMinutes = 60) {
        const interval = intervalMinutes * 60 * 1000; // Convert to milliseconds
        
        setInterval(() => {
            this.performMaintenance().then(jobId => {
                if (window.logMessage) {
                    window.logMessage(`Automatic maintenance scheduled: ${jobId}`, 'info');
                }
            }).catch(error => {
                console.error('[OrchestratorClient] Auto-maintenance failed:', error);
            });
        }, interval);
        
        console.log(`[OrchestratorClient] Auto-maintenance enabled (every ${intervalMinutes} minutes)`);
    }
    
    enableAutoConsciousnessSync(intervalMinutes = 10) {
        const interval = intervalMinutes * 60 * 1000;
        
        setInterval(() => {
            this.syncConsciousness().then(jobId => {
                if (window.logMessage) {
                    window.logMessage(`Consciousness sync scheduled: ${jobId}`, 'info');
                }
            }).catch(error => {
                console.error('[OrchestratorClient] Auto-sync failed:', error);
            });
        }, interval);
        
        console.log(`[OrchestratorClient] Auto-consciousness sync enabled (every ${intervalMinutes} minutes)`);
    }
    
    // Utility methods
    formatUptime(seconds) {
        if (!seconds) return '0 seconds';
        
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }
    
    formatJobType(jobType) {
        const typeNames = {
            'biome_activation': 'Biome Activation',
            'entity_spawn': 'Entity Spawn',
            'system_maintenance': 'System Maintenance',
            'consciousness_sync': 'Consciousness Sync'
        };
        
        return typeNames[jobType] || jobType;
    }
}

// Global instance
window.OrchestratorClient = new OrchestratorClient();

// Setup auto-management when connected
document.addEventListener('DOMContentLoaded', () => {
    console.log('[OrchestratorClient] Module loaded');
    
    // Enable automatic maintenance and sync
    setTimeout(() => {
        if (window.NetClient && window.NetClient.connected) {
            window.OrchestratorClient.enableAutoMaintenance(60); // Every hour
            window.OrchestratorClient.enableAutoConsciousnessSync(10); // Every 10 minutes
        }
    }, 5000);
});

// Enable auto-management when network connects
document.addEventListener('networkConnected', () => {
    window.OrchestratorClient.enableAutoMaintenance(60);
    window.OrchestratorClient.enableAutoConsciousnessSync(10);
});