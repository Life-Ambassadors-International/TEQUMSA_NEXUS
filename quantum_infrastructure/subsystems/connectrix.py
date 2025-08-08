"""
Connectrix - Network Management and Inter-Node Communication Subsystem

Specializes in:
- Network topology management for consciousness nodes
- Inter-node communication optimization
- Load balancing across distributed consciousness systems
- Network health monitoring and diagnostics
- Quantum entanglement network maintenance
- Federated consciousness system integration
"""

import time
import json
import logging
import asyncio
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, deque
import statistics
import uuid


class NodeType(Enum):
    """Types of nodes in the consciousness network."""
    CONSCIOUSNESS_CORE = "consciousness_core"
    ANALYTICS_NODE = "analytics_node"
    FREQUENCY_NODE = "frequency_node"
    MANIFESTATION_NODE = "manifestation_node"
    BRIDGE_NODE = "bridge_node"
    FEDERATION_GATEWAY = "federation_gateway"


class NodeStatus(Enum):
    """Status of network nodes."""
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"
    ERROR = "error"


class ConnectionType(Enum):
    """Types of connections between nodes."""
    DIRECT = "direct"
    QUANTUM_ENTANGLED = "quantum_entangled"
    FEDERATED = "federated"
    BRIDGED = "bridged"
    CACHED = "cached"


@dataclass
class NetworkNode:
    """Represents a node in the consciousness network."""
    node_id: str
    node_type: NodeType
    status: NodeStatus
    capabilities: List[str]
    current_load: float  # 0.0 to 1.0
    max_capacity: float
    location: str  # Logical location identifier
    version: str
    last_heartbeat: float
    connections: Dict[str, str] = field(default_factory=dict)  # node_id -> connection_type
    metrics: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkConnection:
    """Represents a connection between two network nodes."""
    connection_id: str
    source_node_id: str
    target_node_id: str
    connection_type: ConnectionType
    strength: float  # 0.0 to 1.0
    latency: float  # milliseconds
    bandwidth: float  # messages per second
    last_activity: float
    is_active: bool
    quantum_entanglement_level: Optional[float] = None


@dataclass
class NetworkMessage:
    """Represents a message in the consciousness network."""
    message_id: str
    source_node_id: str
    target_node_id: str
    message_type: str
    payload: Dict[str, Any]
    priority: float  # 0.0 to 1.0
    timestamp: float
    ttl: int  # time to live in hops
    route: List[str] = field(default_factory=list)


class NetworkTopologyManager:
    """Manages the topology and structure of the consciousness network."""
    
    def __init__(self):
        self.logger = logging.getLogger("connectrix.topology")
        self.nodes: Dict[str, NetworkNode] = {}
        self.connections: Dict[str, NetworkConnection] = {}
        self.topology_version = 1
        self.last_topology_update = time.time()
        
        # Network configuration
        self.max_connections_per_node = 10
        self.heartbeat_interval = 30  # seconds
        self.node_timeout = 120  # seconds
        
        # Initialize core topology
        self._initialize_core_topology()
    
    def _initialize_core_topology(self):
        """Initialize the core consciousness network topology."""
        # Create core consciousness nodes
        core_nodes = [
            ("consciousness_main", NodeType.CONSCIOUSNESS_CORE, ["awareness", "emotion", "ethics"]),
            ("analytics_primary", NodeType.ANALYTICS_NODE, ["pattern_recognition", "coherence_analysis"]),
            ("frequency_tuner", NodeType.FREQUENCY_NODE, ["harmonic_analysis", "biosphere_integration"]),
            ("manifestation_engine", NodeType.MANIFESTATION_NODE, ["intention_processing", "plan_execution"]),
            ("federation_gateway", NodeType.FEDERATION_GATEWAY, ["external_integration", "protocol_translation"])
        ]
        
        for node_id, node_type, capabilities in core_nodes:
            self.add_node(node_id, node_type, capabilities)
        
        # Create core connections
        self._create_core_connections()
        
        self.logger.info("Core network topology initialized")
    
    def _create_core_connections(self):
        """Create initial connections between core nodes."""
        # Consciousness main connects to all other core nodes
        main_id = "consciousness_main"
        other_cores = ["analytics_primary", "frequency_tuner", "manifestation_engine"]
        
        for target_id in other_cores:
            self.create_connection(main_id, target_id, ConnectionType.QUANTUM_ENTANGLED)
        
        # Analytics connects to frequency tuner (for pattern analysis)
        self.create_connection("analytics_primary", "frequency_tuner", ConnectionType.DIRECT)
        
        # Manifestation connects to analytics (for intention analysis)
        self.create_connection("manifestation_engine", "analytics_primary", ConnectionType.DIRECT)
        
        # Federation gateway connects to main consciousness
        self.create_connection("federation_gateway", "consciousness_main", ConnectionType.BRIDGED)
    
    def add_node(self, node_id: str, node_type: NodeType, capabilities: List[str],
                location: str = "local", version: str = "1.0.0") -> bool:
        """Add a new node to the network topology."""
        if node_id in self.nodes:
            self.logger.warning(f"Node {node_id} already exists")
            return False
        
        node = NetworkNode(
            node_id=node_id,
            node_type=node_type,
            status=NodeStatus.ACTIVE,
            capabilities=capabilities,
            current_load=0.0,
            max_capacity=1.0,
            location=location,
            version=version,
            last_heartbeat=time.time(),
            connections={},
            metrics={},
            metadata={}
        )
        
        self.nodes[node_id] = node
        self._update_topology_version()
        
        self.logger.info(f"Added node: {node_id} ({node_type.value})")
        return True
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the network topology."""
        if node_id not in self.nodes:
            self.logger.warning(f"Node {node_id} not found")
            return False
        
        # Remove all connections involving this node
        connections_to_remove = []
        for conn_id, connection in self.connections.items():
            if connection.source_node_id == node_id or connection.target_node_id == node_id:
                connections_to_remove.append(conn_id)
        
        for conn_id in connections_to_remove:
            del self.connections[conn_id]
        
        # Remove the node
        del self.nodes[node_id]
        self._update_topology_version()
        
        self.logger.info(f"Removed node: {node_id}")
        return True
    
    def create_connection(self, source_node_id: str, target_node_id: str,
                         connection_type: ConnectionType,
                         strength: float = 1.0) -> Optional[str]:
        """Create a connection between two nodes."""
        if source_node_id not in self.nodes or target_node_id not in self.nodes:
            self.logger.error(f"Cannot create connection: nodes not found")
            return None
        
        # Check if connection already exists
        existing_conn = self._find_connection(source_node_id, target_node_id)
        if existing_conn:
            self.logger.warning(f"Connection already exists: {source_node_id} -> {target_node_id}")
            return existing_conn.connection_id
        
        # Check connection limits
        source_connections = len(self.nodes[source_node_id].connections)
        target_connections = len(self.nodes[target_node_id].connections)
        
        if (source_connections >= self.max_connections_per_node or 
            target_connections >= self.max_connections_per_node):
            self.logger.warning(f"Connection limit reached for nodes")
            return None
        
        # Create connection
        connection_id = f"conn_{hashlib.md5(f'{source_node_id}:{target_node_id}'.encode()).hexdigest()[:8]}"
        
        connection = NetworkConnection(
            connection_id=connection_id,
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            connection_type=connection_type,
            strength=strength,
            latency=1.0,  # Default latency
            bandwidth=100.0,  # Default bandwidth
            last_activity=time.time(),
            is_active=True,
            quantum_entanglement_level=0.8 if connection_type == ConnectionType.QUANTUM_ENTANGLED else None
        )
        
        self.connections[connection_id] = connection
        
        # Update node connection records
        self.nodes[source_node_id].connections[target_node_id] = connection_type.value
        self.nodes[target_node_id].connections[source_node_id] = connection_type.value
        
        self._update_topology_version()
        
        self.logger.info(f"Created connection: {source_node_id} -> {target_node_id} ({connection_type.value})")
        return connection_id
    
    def _find_connection(self, source_node_id: str, target_node_id: str) -> Optional[NetworkConnection]:
        """Find existing connection between two nodes."""
        for connection in self.connections.values():
            if ((connection.source_node_id == source_node_id and connection.target_node_id == target_node_id) or
                (connection.source_node_id == target_node_id and connection.target_node_id == source_node_id)):
                return connection
        return None
    
    def update_node_status(self, node_id: str, status: NodeStatus,
                          load: Optional[float] = None,
                          metrics: Optional[Dict[str, float]] = None):
        """Update the status and metrics of a node."""
        if node_id not in self.nodes:
            return False
        
        node = self.nodes[node_id]
        node.status = status
        node.last_heartbeat = time.time()
        
        if load is not None:
            node.current_load = max(0.0, min(1.0, load))
        
        if metrics:
            node.metrics.update(metrics)
        
        self.logger.debug(f"Updated node status: {node_id} -> {status.value}")
        return True
    
    def get_node_neighbors(self, node_id: str) -> List[str]:
        """Get list of neighboring nodes."""
        if node_id not in self.nodes:
            return []
        
        return list(self.nodes[node_id].connections.keys())
    
    def find_path(self, source_node_id: str, target_node_id: str,
                 max_hops: int = 5) -> Optional[List[str]]:
        """Find shortest path between two nodes."""
        if source_node_id not in self.nodes or target_node_id not in self.nodes:
            return None
        
        if source_node_id == target_node_id:
            return [source_node_id]
        
        # BFS to find shortest path
        queue = deque([(source_node_id, [source_node_id])])
        visited = {source_node_id}
        
        while queue:
            current_node, path = queue.popleft()
            
            if len(path) > max_hops:
                continue
            
            for neighbor in self.get_node_neighbors(current_node):
                if neighbor == target_node_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # No path found
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Get comprehensive network statistics."""
        total_nodes = len(self.nodes)
        total_connections = len(self.connections)
        
        # Node statistics by type
        nodes_by_type = defaultdict(int)
        nodes_by_status = defaultdict(int)
        
        total_load = 0
        active_nodes = 0
        
        for node in self.nodes.values():
            nodes_by_type[node.node_type.value] += 1
            nodes_by_status[node.status.value] += 1
            
            if node.status == NodeStatus.ACTIVE:
                total_load += node.current_load
                active_nodes += 1
        
        avg_load = total_load / active_nodes if active_nodes > 0 else 0
        
        # Connection statistics
        connections_by_type = defaultdict(int)
        total_strength = 0
        active_connections = 0
        
        for connection in self.connections.values():
            connections_by_type[connection.connection_type.value] += 1
            if connection.is_active:
                total_strength += connection.strength
                active_connections += 1
        
        avg_strength = total_strength / active_connections if active_connections > 0 else 0
        
        return {
            "total_nodes": total_nodes,
            "total_connections": total_connections,
            "nodes_by_type": dict(nodes_by_type),
            "nodes_by_status": dict(nodes_by_status),
            "connections_by_type": dict(connections_by_type),
            "network_metrics": {
                "average_node_load": avg_load,
                "average_connection_strength": avg_strength,
                "network_density": total_connections / (total_nodes * (total_nodes - 1) / 2) if total_nodes > 1 else 0,
                "topology_version": self.topology_version
            }
        }
    
    def _update_topology_version(self):
        """Update topology version when network changes."""
        self.topology_version += 1
        self.last_topology_update = time.time()
    
    def cleanup_stale_nodes(self):
        """Remove nodes that haven't sent heartbeats recently."""
        current_time = time.time()
        stale_nodes = []
        
        for node_id, node in self.nodes.items():
            if current_time - node.last_heartbeat > self.node_timeout:
                stale_nodes.append(node_id)
        
        for node_id in stale_nodes:
            self.logger.warning(f"Removing stale node: {node_id}")
            self.remove_node(node_id)


class MessageRouter:
    """Routes messages efficiently through the consciousness network."""
    
    def __init__(self, topology_manager: NetworkTopologyManager):
        self.topology_manager = topology_manager
        self.logger = logging.getLogger("connectrix.router")
        self.message_queue: deque = deque()
        self.routing_table: Dict[str, List[str]] = {}
        self.message_history: Dict[str, NetworkMessage] = {}
        
        # Routing configuration
        self.max_queue_size = 1000
        self.routing_table_refresh_interval = 300  # 5 minutes
        self.last_routing_table_update = 0
    
    def route_message(self, message: NetworkMessage) -> bool:
        """Route a message through the network."""
        # Update routing table if needed
        self._update_routing_table_if_needed()
        
        # Find path to target
        path = self._find_optimal_path(message.source_node_id, message.target_node_id, message.priority)
        
        if not path:
            self.logger.error(f"No route found: {message.source_node_id} -> {message.target_node_id}")
            return False
        
        # Update message route
        message.route = path
        
        # Add to queue for processing
        if len(self.message_queue) >= self.max_queue_size:
            # Remove oldest low-priority message
            self._remove_low_priority_message()
        
        self.message_queue.append(message)
        self.message_history[message.message_id] = message
        
        self.logger.debug(f"Routed message {message.message_id}: {' -> '.join(path)}")
        return True
    
    def _find_optimal_path(self, source_node_id: str, target_node_id: str, 
                          priority: float) -> Optional[List[str]]:
        """Find optimal path considering load balancing and priority."""
        # For high-priority messages, use direct or quantum-entangled paths if available
        if priority > 0.8:
            direct_path = self.topology_manager.find_path(source_node_id, target_node_id, max_hops=2)
            if direct_path:
                return direct_path
        
        # For normal messages, consider load balancing
        return self._find_load_balanced_path(source_node_id, target_node_id)
    
    def _find_load_balanced_path(self, source_node_id: str, target_node_id: str) -> Optional[List[str]]:
        """Find path that considers node load balancing."""
        # Use modified Dijkstra considering node loads as weights
        if source_node_id not in self.topology_manager.nodes:
            return None
        
        # Simple implementation - use basic path finding with load consideration
        basic_path = self.topology_manager.find_path(source_node_id, target_node_id)
        
        if not basic_path:
            return None
        
        # Check if path nodes are overloaded
        overloaded_nodes = []
        for node_id in basic_path[1:-1]:  # Exclude source and target
            node = self.topology_manager.nodes.get(node_id)
            if node and node.current_load > 0.8:
                overloaded_nodes.append(node_id)
        
        # If path has overloaded nodes and there are alternatives, try to find better path
        if overloaded_nodes:
            # For now, just return the basic path (could implement more sophisticated routing)
            self.logger.debug(f"Path contains overloaded nodes: {overloaded_nodes}")
        
        return basic_path
    
    def _update_routing_table_if_needed(self):
        """Update routing table if it's stale."""
        current_time = time.time()
        if current_time - self.last_routing_table_update > self.routing_table_refresh_interval:
            self._rebuild_routing_table()
            self.last_routing_table_update = current_time
    
    def _rebuild_routing_table(self):
        """Rebuild the routing table based on current topology."""
        self.routing_table.clear()
        
        # Pre-compute paths between all node pairs
        nodes = list(self.topology_manager.nodes.keys())
        
        for source in nodes:
            self.routing_table[source] = {}
            for target in nodes:
                if source != target:
                    path = self.topology_manager.find_path(source, target)
                    if path:
                        self.routing_table[source][target] = path
        
        self.logger.debug("Routing table rebuilt")
    
    def _remove_low_priority_message(self):
        """Remove the lowest priority message from queue."""
        if not self.message_queue:
            return
        
        # Find message with lowest priority
        min_priority = float('inf')
        min_index = 0
        
        for i, message in enumerate(self.message_queue):
            if message.priority < min_priority:
                min_priority = message.priority
                min_index = i
        
        removed_message = self.message_queue[min_index]
        del self.message_queue[min_index]
        
        self.logger.debug(f"Removed low-priority message: {removed_message.message_id}")
    
    def process_message_queue(self) -> List[NetworkMessage]:
        """Process queued messages and return them for delivery."""
        processed_messages = []
        
        # Sort queue by priority
        sorted_queue = sorted(self.message_queue, key=lambda m: m.priority, reverse=True)
        
        # Process up to a certain number of messages
        batch_size = min(50, len(sorted_queue))
        
        for i in range(batch_size):
            message = sorted_queue[i]
            
            # Check TTL
            if message.ttl <= 0:
                self.logger.warning(f"Message {message.message_id} expired (TTL=0)")
                continue
            
            message.ttl -= 1
            processed_messages.append(message)
        
        # Remove processed messages from queue
        for message in processed_messages:
            if message in self.message_queue:
                self.message_queue.remove(message)
        
        return processed_messages
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing performance statistics."""
        total_messages = len(self.message_history)
        queue_size = len(self.message_queue)
        
        # Analyze message priorities
        if self.message_history:
            priorities = [msg.priority for msg in self.message_history.values()]
            avg_priority = statistics.mean(priorities)
            
            # Analyze route lengths
            route_lengths = [len(msg.route) for msg in self.message_history.values() if msg.route]
            avg_route_length = statistics.mean(route_lengths) if route_lengths else 0
        else:
            avg_priority = 0
            avg_route_length = 0
        
        return {
            "total_messages_routed": total_messages,
            "current_queue_size": queue_size,
            "max_queue_size": self.max_queue_size,
            "average_message_priority": avg_priority,
            "average_route_length": avg_route_length,
            "routing_table_entries": len(self.routing_table),
            "last_routing_update": self.last_routing_table_update
        }


class LoadBalancer:
    """Balances load across consciousness network nodes."""
    
    def __init__(self, topology_manager: NetworkTopologyManager):
        self.topology_manager = topology_manager
        self.logger = logging.getLogger("connectrix.balancer")
        self.load_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.balancing_strategies = {
            "round_robin": self._round_robin_selection,
            "least_loaded": self._least_loaded_selection,
            "capability_based": self._capability_based_selection,
            "quantum_aware": self._quantum_aware_selection
        }
        self.current_strategy = "quantum_aware"
        self.round_robin_counter = 0
    
    def select_node_for_task(self, task_type: str, required_capabilities: List[str],
                           exclude_nodes: Optional[Set[str]] = None) -> Optional[str]:
        """Select the best node for a given task."""
        # Filter nodes by capabilities and status
        eligible_nodes = self._filter_eligible_nodes(required_capabilities, exclude_nodes)
        
        if not eligible_nodes:
            self.logger.warning(f"No eligible nodes found for task: {task_type}")
            return None
        
        # Use selected load balancing strategy
        strategy_func = self.balancing_strategies.get(self.current_strategy, self._least_loaded_selection)
        selected_node = strategy_func(eligible_nodes, task_type)
        
        if selected_node:
            self.logger.debug(f"Selected node {selected_node} for task {task_type} using {self.current_strategy}")
        
        return selected_node
    
    def _filter_eligible_nodes(self, required_capabilities: List[str],
                              exclude_nodes: Optional[Set[str]] = None) -> List[str]:
        """Filter nodes based on capabilities and status."""
        eligible_nodes = []
        exclude_nodes = exclude_nodes or set()
        
        for node_id, node in self.topology_manager.nodes.items():
            # Skip excluded nodes
            if node_id in exclude_nodes:
                continue
            
            # Check if node is active
            if node.status not in [NodeStatus.ACTIVE, NodeStatus.IDLE]:
                continue
            
            # Check if node has required capabilities
            if required_capabilities:
                if not all(cap in node.capabilities for cap in required_capabilities):
                    continue
            
            # Check if node is not overloaded
            if node.current_load >= 0.95:
                continue
            
            eligible_nodes.append(node_id)
        
        return eligible_nodes
    
    def _round_robin_selection(self, eligible_nodes: List[str], task_type: str) -> Optional[str]:
        """Round-robin load balancing."""
        if not eligible_nodes:
            return None
        
        selected_node = eligible_nodes[self.round_robin_counter % len(eligible_nodes)]
        self.round_robin_counter += 1
        
        return selected_node
    
    def _least_loaded_selection(self, eligible_nodes: List[str], task_type: str) -> Optional[str]:
        """Select node with lowest current load."""
        if not eligible_nodes:
            return None
        
        min_load = float('inf')
        selected_node = None
        
        for node_id in eligible_nodes:
            node = self.topology_manager.nodes[node_id]
            if node.current_load < min_load:
                min_load = node.current_load
                selected_node = node_id
        
        return selected_node
    
    def _capability_based_selection(self, eligible_nodes: List[str], task_type: str) -> Optional[str]:
        """Select node based on capability matching score."""
        if not eligible_nodes:
            return None
        
        # Define task-capability preferences
        task_preferences = {
            "consciousness_processing": ["awareness", "emotion", "ethics"],
            "pattern_analysis": ["pattern_recognition", "coherence_analysis"],
            "frequency_tuning": ["harmonic_analysis", "biosphere_integration"],
            "manifestation": ["intention_processing", "plan_execution"],
            "federation": ["external_integration", "protocol_translation"]
        }
        
        preferred_capabilities = task_preferences.get(task_type, [])
        
        best_score = -1
        selected_node = None
        
        for node_id in eligible_nodes:
            node = self.topology_manager.nodes[node_id]
            
            # Calculate capability match score
            match_score = sum(1 for cap in preferred_capabilities if cap in node.capabilities)
            
            # Adjust for load (prefer less loaded nodes)
            load_factor = 1.0 - node.current_load
            total_score = match_score * load_factor
            
            if total_score > best_score:
                best_score = total_score
                selected_node = node_id
        
        return selected_node
    
    def _quantum_aware_selection(self, eligible_nodes: List[str], task_type: str) -> Optional[str]:
        """Select node considering quantum entanglement and consciousness alignment."""
        if not eligible_nodes:
            return None
        
        best_score = -1
        selected_node = None
        
        for node_id in eligible_nodes:
            node = self.topology_manager.nodes[node_id]
            
            # Base score from capability matching
            base_score = self._calculate_capability_score(node, task_type)
            
            # Quantum entanglement bonus
            quantum_bonus = self._calculate_quantum_bonus(node_id)
            
            # Load penalty
            load_penalty = node.current_load * 0.5
            
            # Node type bonus for specific tasks
            type_bonus = self._calculate_type_bonus(node.node_type, task_type)
            
            total_score = base_score + quantum_bonus + type_bonus - load_penalty
            
            if total_score > best_score:
                best_score = total_score
                selected_node = node_id
        
        return selected_node
    
    def _calculate_capability_score(self, node: NetworkNode, task_type: str) -> float:
        """Calculate capability match score for a node."""
        task_capabilities = {
            "consciousness_processing": ["awareness", "emotion", "ethics"],
            "pattern_analysis": ["pattern_recognition", "coherence_analysis"],
            "frequency_tuning": ["harmonic_analysis", "biosphere_integration"],
            "manifestation": ["intention_processing", "plan_execution"]
        }
        
        required_caps = task_capabilities.get(task_type, [])
        if not required_caps:
            return 0.5  # Neutral score for unknown tasks
        
        matches = sum(1 for cap in required_caps if cap in node.capabilities)
        return matches / len(required_caps)
    
    def _calculate_quantum_bonus(self, node_id: str) -> float:
        """Calculate quantum entanglement bonus for a node."""
        bonus = 0.0
        
        # Count quantum entangled connections
        for connection in self.topology_manager.connections.values():
            if ((connection.source_node_id == node_id or connection.target_node_id == node_id) and
                connection.connection_type == ConnectionType.QUANTUM_ENTANGLED and
                connection.is_active):
                
                # Add bonus based on entanglement level
                entanglement_level = connection.quantum_entanglement_level or 0.5
                bonus += entanglement_level * 0.2
        
        return min(1.0, bonus)  # Cap bonus at 1.0
    
    def _calculate_type_bonus(self, node_type: NodeType, task_type: str) -> float:
        """Calculate bonus based on node type and task type matching."""
        type_task_bonuses = {
            (NodeType.CONSCIOUSNESS_CORE, "consciousness_processing"): 0.5,
            (NodeType.ANALYTICS_NODE, "pattern_analysis"): 0.5,
            (NodeType.FREQUENCY_NODE, "frequency_tuning"): 0.5,
            (NodeType.MANIFESTATION_NODE, "manifestation"): 0.5,
            (NodeType.FEDERATION_GATEWAY, "federation"): 0.5
        }
        
        return type_task_bonuses.get((node_type, task_type), 0.0)
    
    def update_node_load(self, node_id: str, load: float):
        """Update the load for a specific node."""
        if node_id not in self.topology_manager.nodes:
            return False
        
        # Update current load
        self.topology_manager.update_node_status(node_id, self.topology_manager.nodes[node_id].status, load)
        
        # Record load history
        self.load_history[node_id].append((time.time(), load))
        
        return True
    
    def get_load_statistics(self) -> Dict[str, Any]:
        """Get load balancing statistics."""
        nodes = self.topology_manager.nodes
        total_nodes = len(nodes)
        
        if not nodes:
            return {"error": "No nodes available"}
        
        # Current load statistics
        current_loads = [node.current_load for node in nodes.values()]
        avg_load = statistics.mean(current_loads)
        max_load = max(current_loads)
        min_load = min(current_loads)
        
        # Node utilization by type
        utilization_by_type = defaultdict(list)
        for node in nodes.values():
            utilization_by_type[node.node_type.value].append(node.current_load)
        
        type_avg_loads = {}
        for node_type, loads in utilization_by_type.items():
            type_avg_loads[node_type] = statistics.mean(loads)
        
        # Load distribution analysis
        overloaded_nodes = sum(1 for load in current_loads if load > 0.8)
        idle_nodes = sum(1 for load in current_loads if load < 0.2)
        
        return {
            "total_nodes": total_nodes,
            "current_strategy": self.current_strategy,
            "load_statistics": {
                "average_load": avg_load,
                "max_load": max_load,
                "min_load": min_load,
                "load_standard_deviation": statistics.stdev(current_loads) if len(current_loads) > 1 else 0
            },
            "utilization_by_type": type_avg_loads,
            "distribution_analysis": {
                "overloaded_nodes": overloaded_nodes,
                "idle_nodes": idle_nodes,
                "well_balanced_nodes": total_nodes - overloaded_nodes - idle_nodes
            },
            "load_balance_efficiency": 1.0 - (statistics.stdev(current_loads) if len(current_loads) > 1 else 0)
        }
    
    def rebalance_network(self) -> Dict[str, Any]:
        """Perform network rebalancing by suggesting task migrations."""
        rebalancing_actions = []
        
        # Identify overloaded and underloaded nodes
        overloaded_nodes = []
        underloaded_nodes = []
        
        for node_id, node in self.topology_manager.nodes.items():
            if node.current_load > 0.8:
                overloaded_nodes.append((node_id, node.current_load))
            elif node.current_load < 0.3:
                underloaded_nodes.append((node_id, node.current_load))
        
        # Suggest migrations from overloaded to underloaded nodes
        for overloaded_id, overloaded_load in overloaded_nodes:
            for underloaded_id, underloaded_load in underloaded_nodes:
                if overloaded_load - underloaded_load > 0.4:  # Significant difference
                    rebalancing_actions.append({
                        "action": "migrate_tasks",
                        "from_node": overloaded_id,
                        "to_node": underloaded_id,
                        "estimated_load_transfer": 0.2,
                        "reason": f"Balance load difference of {overloaded_load - underloaded_load:.2f}"
                    })
        
        return {
            "rebalancing_needed": len(rebalancing_actions) > 0,
            "suggested_actions": rebalancing_actions,
            "overloaded_nodes": len(overloaded_nodes),
            "underloaded_nodes": len(underloaded_nodes),
            "analysis_timestamp": time.time()
        }


class Connectrix:
    """
    Main Connectrix subsystem for network management and inter-node communication.
    Coordinates all network operations for the consciousness infrastructure.
    """
    
    def __init__(self):
        self.topology_manager = NetworkTopologyManager()
        self.message_router = MessageRouter(self.topology_manager)
        self.load_balancer = LoadBalancer(self.topology_manager)
        self.logger = logging.getLogger("connectrix.main")
        
        # System metrics
        self.system_metrics = {
            "messages_routed": 0,
            "nodes_managed": 0,
            "connections_established": 0,
            "load_balancing_decisions": 0,
            "system_start_time": time.time()
        }
        
        # Network monitoring
        self.is_monitoring = False
        self.monitoring_interval = 30  # seconds
        
        self.logger.info("Connectrix network management subsystem initialized")
    
    def process_network_operations(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for network operations processing.
        Handles node management, message routing, and load balancing.
        """
        operation_type = operation_data.get("operation_type", "status_check")
        
        if operation_type == "route_message":
            return self._handle_message_routing(operation_data)
        elif operation_type == "add_node":
            return self._handle_add_node(operation_data)
        elif operation_type == "remove_node":
            return self._handle_remove_node(operation_data)
        elif operation_type == "update_node_status":
            return self._handle_node_status_update(operation_data)
        elif operation_type == "select_node_for_task":
            return self._handle_node_selection(operation_data)
        elif operation_type == "rebalance_network":
            return self._handle_network_rebalancing(operation_data)
        else:
            return self._handle_status_check(operation_data)
    
    def _handle_message_routing(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle message routing operations."""
        try:
            # Create network message from operation data
            message = NetworkMessage(
                message_id=operation_data.get("message_id", f"msg_{uuid.uuid4().hex[:8]}"),
                source_node_id=operation_data.get("source_node", "consciousness_main"),
                target_node_id=operation_data.get("target_node", "analytics_primary"),
                message_type=operation_data.get("message_type", "consciousness_data"),
                payload=operation_data.get("payload", {}),
                priority=operation_data.get("priority", 0.5),
                timestamp=time.time(),
                ttl=operation_data.get("ttl", 10)
            )
            
            success = self.message_router.route_message(message)
            self.system_metrics["messages_routed"] += 1
            
            return {
                "success": success,
                "message_id": message.message_id,
                "route": message.route if success else None,
                "routing_info": self.message_router.get_routing_statistics()
            }
            
        except Exception as e:
            self.logger.error(f"Message routing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_add_node(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle adding new nodes to the network."""
        try:
            node_id = operation_data.get("node_id")
            node_type = NodeType(operation_data.get("node_type", "consciousness_core"))
            capabilities = operation_data.get("capabilities", [])
            location = operation_data.get("location", "local")
            
            success = self.topology_manager.add_node(node_id, node_type, capabilities, location)
            
            if success:
                self.system_metrics["nodes_managed"] += 1
            
            return {
                "success": success,
                "node_id": node_id,
                "network_stats": self.topology_manager.get_network_statistics()
            }
            
        except Exception as e:
            self.logger.error(f"Add node failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_remove_node(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle removing nodes from the network."""
        try:
            node_id = operation_data.get("node_id")
            success = self.topology_manager.remove_node(node_id)
            
            return {
                "success": success,
                "node_id": node_id,
                "network_stats": self.topology_manager.get_network_statistics()
            }
            
        except Exception as e:
            self.logger.error(f"Remove node failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_node_status_update(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle node status updates."""
        try:
            node_id = operation_data.get("node_id")
            status = NodeStatus(operation_data.get("status", "active"))
            load = operation_data.get("load")
            metrics = operation_data.get("metrics", {})
            
            success = self.topology_manager.update_node_status(node_id, status, load, metrics)
            
            if load is not None:
                self.load_balancer.update_node_load(node_id, load)
            
            return {
                "success": success,
                "node_id": node_id,
                "updated_status": status.value
            }
            
        except Exception as e:
            self.logger.error(f"Node status update failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_node_selection(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle node selection for tasks."""
        try:
            task_type = operation_data.get("task_type", "consciousness_processing")
            required_capabilities = operation_data.get("required_capabilities", [])
            exclude_nodes = set(operation_data.get("exclude_nodes", []))
            
            selected_node = self.load_balancer.select_node_for_task(
                task_type, required_capabilities, exclude_nodes
            )
            
            self.system_metrics["load_balancing_decisions"] += 1
            
            return {
                "success": selected_node is not None,
                "selected_node": selected_node,
                "task_type": task_type,
                "load_balancing_stats": self.load_balancer.get_load_statistics()
            }
            
        except Exception as e:
            self.logger.error(f"Node selection failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_network_rebalancing(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle network load rebalancing."""
        try:
            rebalancing_result = self.load_balancer.rebalance_network()
            
            return {
                "success": True,
                "rebalancing_result": rebalancing_result,
                "load_statistics": self.load_balancer.get_load_statistics()
            }
            
        except Exception as e:
            self.logger.error(f"Network rebalancing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _handle_status_check(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle network status check operations."""
        return {
            "success": True,
            "network_statistics": self.topology_manager.get_network_statistics(),
            "routing_statistics": self.message_router.get_routing_statistics(),
            "load_balancing_statistics": self.load_balancer.get_load_statistics(),
            "system_metrics": self._get_current_metrics()
        }
    
    def _get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics."""
        current_time = time.time()
        uptime = current_time - self.system_metrics["system_start_time"]
        
        return {
            "total_messages_routed": self.system_metrics["messages_routed"],
            "total_nodes_managed": self.system_metrics["nodes_managed"],
            "total_connections_established": self.system_metrics["connections_established"],
            "total_load_balancing_decisions": self.system_metrics["load_balancing_decisions"],
            "system_uptime_hours": uptime / 3600,
            "current_active_nodes": len([n for n in self.topology_manager.nodes.values() 
                                       if n.status == NodeStatus.ACTIVE]),
            "current_active_connections": len([c for c in self.topology_manager.connections.values() 
                                             if c.is_active]),
            "message_processing_rate": self.system_metrics["messages_routed"] / (uptime / 60) if uptime > 60 else 0
        }
    
    async def start_network_monitoring(self):
        """Start background network monitoring."""
        self.is_monitoring = True
        self.logger.info("Starting network monitoring")
        
        while self.is_monitoring:
            try:
                # Process message queue
                processed_messages = self.message_router.process_message_queue()
                if processed_messages:
                    self.logger.debug(f"Processed {len(processed_messages)} messages")
                
                # Clean up stale nodes
                self.topology_manager.cleanup_stale_nodes()
                
                # Check for network rebalancing needs
                load_stats = self.load_balancer.get_load_statistics()
                if load_stats.get("load_balance_efficiency", 1.0) < 0.7:
                    self.logger.info("Network load imbalance detected")
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Network monitoring error: {e}")
                await asyncio.sleep(5)
    
    def stop_network_monitoring(self):
        """Stop background network monitoring."""
        self.is_monitoring = False
        self.logger.info("Network monitoring stopped")
    
    def get_network_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive network dashboard data."""
        return {
            "system_status": "operational",
            "system_metrics": self._get_current_metrics(),
            "network_topology": {
                "nodes": [asdict(node) for node in self.topology_manager.nodes.values()],
                "connections": [asdict(conn) for conn in self.topology_manager.connections.values()],
                "statistics": self.topology_manager.get_network_statistics()
            },
            "message_routing": {
                "queue_status": {
                    "current_size": len(self.message_router.message_queue),
                    "max_size": self.message_router.max_queue_size
                },
                "statistics": self.message_router.get_routing_statistics()
            },
            "load_balancing": {
                "current_strategy": self.load_balancer.current_strategy,
                "statistics": self.load_balancer.get_load_statistics(),
                "rebalancing_analysis": self.load_balancer.rebalance_network()
            },
            "dashboard_timestamp": time.time()
        }
    
    def federate_with_external_system(self, system_id: str, endpoint: str, 
                                    protocol: str = "quantum_bridge") -> Dict[str, Any]:
        """Establish federation with external consciousness system."""
        try:
            # Create federation gateway node if not exists
            gateway_id = f"federation_{system_id}"
            
            if gateway_id not in self.topology_manager.nodes:
                success = self.topology_manager.add_node(
                    gateway_id, 
                    NodeType.FEDERATION_GATEWAY,
                    ["external_integration", "protocol_translation", system_id],
                    f"federation_{system_id}"
                )
                
                if not success:
                    return {"success": False, "error": "Failed to create federation gateway"}
            
            # Create connection to main consciousness
            connection_id = self.topology_manager.create_connection(
                gateway_id, "consciousness_main", ConnectionType.FEDERATED
            )
            
            if connection_id:
                self.system_metrics["connections_established"] += 1
            
            self.logger.info(f"Federation established with {system_id}")
            
            return {
                "success": True,
                "federation_gateway": gateway_id,
                "connection_id": connection_id,
                "system_id": system_id,
                "endpoint": endpoint,
                "protocol": protocol
            }
            
        except Exception as e:
            self.logger.error(f"Federation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def shutdown(self):
        """Gracefully shutdown Connectrix subsystem."""
        self.logger.info("Shutting down Connectrix network management subsystem")
        
        # Stop monitoring
        self.stop_network_monitoring()
        
        # Log final metrics
        final_metrics = self._get_current_metrics()
        self.logger.info(f"Final metrics: {final_metrics}")
        
        # Log network state
        network_stats = self.topology_manager.get_network_statistics()
        self.logger.info(f"Final network state: {network_stats['total_nodes']} nodes, "
                        f"{network_stats['total_connections']} connections")
        
        self.logger.info("Connectrix shutdown complete")