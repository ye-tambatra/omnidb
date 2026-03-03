from typing import Any

def parse_agent_output(output_content: Any) -> str:
    """
    Safely extract flat text from Langchain Agent outputs.
    Handles cases where the LLM returns rich content block schemas (list of dicts).
    """
    if isinstance(output_content, str):
        return output_content
        
    if isinstance(output_content, list):
        try:
            extracted = []
            for block in output_content:
                if isinstance(block, dict) and "text" in block:
                    extracted.append(str(block["text"]))
                else:
                    extracted.append(str(block))
            return "".join(extracted)
        except Exception:
            return str(output_content)
    
    return str(output_content)
