"""Environment script parser for TEQUMSA Level 100 DSL."""
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import re
import yaml


class ConditionType(str, Enum):
    """Types of conditions in the DSL."""
    ENTITY_COUNT = "entity_count"
    CONSCIOUSNESS_LEVEL = "consciousness_level"
    TIME_ELAPSED = "time_elapsed"
    RESOURCE_AMOUNT = "resource_amount"
    WEATHER_STATE = "weather_state"
    USER_PRESENCE = "user_presence"
    COHERENCE_FIELD = "coherence_field"


class ActionType(str, Enum):
    """Types of actions in the DSL."""
    SPAWN_ENTITY = "spawn_entity"
    REMOVE_ENTITY = "remove_entity"
    MODIFY_COMPONENT = "modify_component"
    TRIGGER_EVENT = "trigger_event"
    SEND_MESSAGE = "send_message"
    CHANGE_WEATHER = "change_weather"
    ADJUST_PHYSICS = "adjust_physics"


class DSLCondition:
    """Represents a condition in the DSL."""
    
    def __init__(self, condition_type: ConditionType, operator: str, value: Any, **kwargs):
        """Initialize DSL condition."""
        self.condition_type = condition_type
        self.operator = operator  # >, <, >=, <=, ==, !=, contains, not_contains
        self.value = value
        self.metadata = kwargs
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate the condition against a context."""
        try:
            actual_value = self._get_actual_value(context)
            return self._compare_values(actual_value, self.value, self.operator)
        except Exception as e:
            print(f"Error evaluating condition {self.condition_type}: {e}")
            return False
    
    def _get_actual_value(self, context: Dict[str, Any]) -> Any:
        """Get the actual value from context based on condition type."""
        if self.condition_type == ConditionType.ENTITY_COUNT:
            entity_type = self.metadata.get('entity_type')
            entities = context.get('entities', {})
            return entities.get(entity_type, 0)
        
        elif self.condition_type == ConditionType.CONSCIOUSNESS_LEVEL:
            consciousness_data = context.get('consciousness', {})
            return consciousness_data.get('average_level', 0.0)
        
        elif self.condition_type == ConditionType.TIME_ELAPSED:
            return context.get('time_elapsed_minutes', 0)
        
        elif self.condition_type == ConditionType.RESOURCE_AMOUNT:
            resource_name = self.metadata.get('resource_name')
            resources = context.get('resources', {})
            return resources.get(resource_name, 0)
        
        elif self.condition_type == ConditionType.WEATHER_STATE:
            weather = context.get('weather', {})
            return weather.get('current_pattern')
        
        elif self.condition_type == ConditionType.USER_PRESENCE:
            return context.get('user_count', 0)
        
        elif self.condition_type == ConditionType.COHERENCE_FIELD:
            consciousness_data = context.get('consciousness', {})
            return consciousness_data.get('coherence_field', 0.0)
        
        else:
            return None
    
    def _compare_values(self, actual: Any, expected: Any, operator: str) -> bool:
        """Compare two values using the specified operator."""
        if operator == ">":
            return actual > expected
        elif operator == "<":
            return actual < expected
        elif operator == ">=":
            return actual >= expected
        elif operator == "<=":
            return actual <= expected
        elif operator == "==":
            return actual == expected
        elif operator == "!=":
            return actual != expected
        elif operator == "contains":
            return expected in str(actual)
        elif operator == "not_contains":
            return expected not in str(actual)
        else:
            return False


class DSLAction:
    """Represents an action in the DSL."""
    
    def __init__(self, action_type: ActionType, parameters: Dict[str, Any]):
        """Initialize DSL action."""
        self.action_type = action_type
        self.parameters = parameters
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the action and return result."""
        try:
            if self.action_type == ActionType.SPAWN_ENTITY:
                return self._execute_spawn_entity(context)
            elif self.action_type == ActionType.REMOVE_ENTITY:
                return self._execute_remove_entity(context)
            elif self.action_type == ActionType.MODIFY_COMPONENT:
                return self._execute_modify_component(context)
            elif self.action_type == ActionType.TRIGGER_EVENT:
                return self._execute_trigger_event(context)
            elif self.action_type == ActionType.SEND_MESSAGE:
                return self._execute_send_message(context)
            elif self.action_type == ActionType.CHANGE_WEATHER:
                return self._execute_change_weather(context)
            elif self.action_type == ActionType.ADJUST_PHYSICS:
                return self._execute_adjust_physics(context)
            else:
                return {'success': False, 'error': f'Unknown action type: {self.action_type}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _execute_spawn_entity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute spawn entity action."""
        entity_type = self.parameters.get('entity_type')
        region_id = self.parameters.get('region_id', context.get('region_id'))
        count = self.parameters.get('count', 1)
        
        return {
            'success': True,
            'action': 'spawn_entity',
            'entity_type': entity_type,
            'region_id': region_id,
            'count': count
        }
    
    def _execute_remove_entity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute remove entity action."""
        entity_id = self.parameters.get('entity_id')
        entity_type = self.parameters.get('entity_type')
        
        return {
            'success': True,
            'action': 'remove_entity',
            'entity_id': entity_id,
            'entity_type': entity_type
        }
    
    def _execute_modify_component(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute modify component action."""
        entity_id = self.parameters.get('entity_id')
        component_type = self.parameters.get('component_type')
        modifications = self.parameters.get('modifications', {})
        
        return {
            'success': True,
            'action': 'modify_component',
            'entity_id': entity_id,
            'component_type': component_type,
            'modifications': modifications
        }
    
    def _execute_trigger_event(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute trigger event action."""
        event_type = self.parameters.get('event_type')
        event_data = self.parameters.get('event_data', {})
        
        return {
            'success': True,
            'action': 'trigger_event',
            'event_type': event_type,
            'event_data': event_data
        }
    
    def _execute_send_message(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute send message action."""
        target = self.parameters.get('target', 'all')
        message = self.parameters.get('message', '')
        
        return {
            'success': True,
            'action': 'send_message',
            'target': target,
            'message': message
        }
    
    def _execute_change_weather(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute change weather action."""
        weather_pattern = self.parameters.get('weather_pattern')
        duration = self.parameters.get('duration', 60)
        
        return {
            'success': True,
            'action': 'change_weather',
            'weather_pattern': weather_pattern,
            'duration': duration
        }
    
    def _execute_adjust_physics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adjust physics action."""
        property_name = self.parameters.get('property')
        value = self.parameters.get('value')
        
        return {
            'success': True,
            'action': 'adjust_physics',
            'property': property_name,
            'value': value
        }


class DSLRule:
    """Represents a complete DSL rule with conditions and actions."""
    
    def __init__(self, rule_id: str, name: str, conditions: List[DSLCondition], 
                 actions: List[DSLAction], priority: int = 0):
        """Initialize DSL rule."""
        self.rule_id = rule_id
        self.name = name
        self.conditions = conditions
        self.actions = actions
        self.priority = priority
        self.execution_count = 0
        self.last_executed = None
    
    def evaluate(self, context: Dict[str, Any]) -> bool:
        """Evaluate all conditions (AND logic)."""
        return all(condition.evaluate(context) for condition in self.conditions)
    
    def execute(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute all actions if conditions are met."""
        if not self.evaluate(context):
            return []
        
        results = []
        for action in self.actions:
            result = action.execute(context)
            results.append(result)
        
        self.execution_count += 1
        from datetime import datetime
        self.last_executed = datetime.utcnow()
        
        return results


class EnvScriptParser:
    """Parser for environment scripts in TEQUMSA DSL."""
    
    def __init__(self):
        """Initialize parser."""
        self.rules: Dict[str, DSLRule] = {}
    
    def parse_yaml_script(self, script_content: str) -> List[DSLRule]:
        """Parse a YAML-formatted environment script."""
        try:
            data = yaml.safe_load(script_content)
            rules = []
            
            for rule_data in data.get('rules', []):
                rule = self._parse_rule(rule_data)
                if rule:
                    rules.append(rule)
                    self.rules[rule.rule_id] = rule
            
            return rules
            
        except Exception as e:
            print(f"Error parsing YAML script: {e}")
            return []
    
    def _parse_rule(self, rule_data: Dict[str, Any]) -> Optional[DSLRule]:
        """Parse a single rule from data."""
        try:
            rule_id = rule_data['id']
            name = rule_data['name']
            priority = rule_data.get('priority', 0)
            
            # Parse conditions
            conditions = []
            for cond_data in rule_data.get('conditions', []):
                condition = self._parse_condition(cond_data)
                if condition:
                    conditions.append(condition)
            
            # Parse actions
            actions = []
            for action_data in rule_data.get('actions', []):
                action = self._parse_action(action_data)
                if action:
                    actions.append(action)
            
            return DSLRule(rule_id, name, conditions, actions, priority)
            
        except Exception as e:
            print(f"Error parsing rule: {e}")
            return None
    
    def _parse_condition(self, cond_data: Dict[str, Any]) -> Optional[DSLCondition]:
        """Parse a condition from data."""
        try:
            condition_type = ConditionType(cond_data['type'])
            operator = cond_data['operator']
            value = cond_data['value']
            
            # Extract additional metadata
            metadata = {k: v for k, v in cond_data.items() 
                       if k not in ['type', 'operator', 'value']}
            
            return DSLCondition(condition_type, operator, value, **metadata)
            
        except Exception as e:
            print(f"Error parsing condition: {e}")
            return None
    
    def _parse_action(self, action_data: Dict[str, Any]) -> Optional[DSLAction]:
        """Parse an action from data."""
        try:
            action_type = ActionType(action_data['type'])
            parameters = action_data.get('parameters', {})
            
            return DSLAction(action_type, parameters)
            
        except Exception as e:
            print(f"Error parsing action: {e}")
            return None
    
    def get_rule(self, rule_id: str) -> Optional[DSLRule]:
        """Get a rule by ID."""
        return self.rules.get(rule_id)
    
    def list_rules(self) -> List[DSLRule]:
        """List all parsed rules."""
        return list(self.rules.values())
    
    def evaluate_all_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate all rules against context and return execution results."""
        results = []
        
        # Sort rules by priority
        sorted_rules = sorted(self.rules.values(), key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            rule_results = rule.execute(context)
            if rule_results:
                results.extend(rule_results)
        
        return results


# Global parser instance
_parser = None


def get_env_script_parser() -> EnvScriptParser:
    """Get the global environment script parser."""
    global _parser
    if _parser is None:
        _parser = EnvScriptParser()
    return _parser