import re
import json
from typing import Any, Dict, Optional, List
from ephor_cli.types.agent import AgentConfig


class ArtifactParserService:
    """Service for parsing artifacts from agent responses using custom parsers."""
    
    def parse_artifacts(self, agent_config: AgentConfig, conversation_history: str) -> Optional[Dict[str, Any]]:
        """Parse artifacts from conversation history using the agent's custom parser.
        
        Args:
            agent_config: The agent configuration containing the parser
            conversation_history: The full conversation history as a string
            
        Returns:
            Parsed artifact data or None if no parser or parsing fails
        """
        if not agent_config.parser:
            return None
            
        try:
            # Create a safe execution environment
            parser_globals = {
                '__builtins__': {
                    'len': len,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'isinstance': isinstance,
                    'ValueError': ValueError,
                    'Exception': Exception,
                },
                'json': json,
                're': re,
            }
            
            # Execute the parser code to define the parse function
            exec(agent_config.parser, parser_globals)
            
            # Check if parse function was defined
            if 'parse' not in parser_globals:
                raise ValueError("Parser must define a 'parse' function")
                
            # Call the parse function with the conversation history
            parse_func = parser_globals['parse']
            result = parse_func(conversation_history)
            
            return result
            
        except Exception as e:
            print(f"Error parsing artifacts: {e}")
            return None
    