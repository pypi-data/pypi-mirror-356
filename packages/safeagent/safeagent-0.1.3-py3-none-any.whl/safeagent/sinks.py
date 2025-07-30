# src/minillm/sinks.py

import json
import os
from pathlib import Path
from typing import Any, Dict

class BaseOutputSink:
    """Abstract base class for all tool output sinks."""
    def handle(self, tool_name: str, result: Any, run_id: str, **kwargs) -> Dict:
        """
        Processes the tool's result. Must be implemented by subclasses.
        Should return a dictionary with metadata about the sink operation.
        """
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__

class FileOutputSink(BaseOutputSink):
    """An output sink that saves the tool's result to a local JSON file."""
    def __init__(self, base_path: str = "tool_outputs"):
        self.base_path = Path(base_path)
        # Ensure the output directory exists
        self.base_path.mkdir(parents=True, exist_ok=True)

    def handle(self, tool_name: str, result: Any, run_id: str, **kwargs) -> Dict:
        # Use a combination of tool name and run_id for a unique filename
        filename = f"{tool_name}_{run_id}.json"
        filepath = self.base_path / filename
        
        try:
            # Prepare data for JSON serialization
            serializable_result = result
            if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
                serializable_result = str(result)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({"tool_name": tool_name, "result": serializable_result}, f, indent=2)
                
            return {"status": "success", "path": str(filepath)}
        except Exception as e:
            return {"status": "failure", "error": str(e)}

    def __str__(self):
        return f"FileOutputSink(path='{self.base_path}')"

# --- Conceptual Example for a Cloud Sink ---
# A real implementation would require the google-cloud-pubsub library
# and would handle authentication (e.g., via environment variables).

class PubSubSink(BaseOutputSink):
    """A conceptual output sink for Google Cloud Pub/Sub."""
    def __init__(self, project_id: str, topic_id: str):
        self.project_id = project_id
        self.topic_id = topic_id
        # In a real app: from google.cloud import pubsub_v1
        # self.publisher = pubsub_v1.PublisherClient()
        # self.topic_path = self.publisher.topic_path(project_id, topic_id)
        print("NOTE: PubSubSink is a conceptual example. Using mock implementation.")

    def handle(self, tool_name: str, result: Any, run_id: str, **kwargs) -> Dict:
        message_data = json.dumps({
            "tool_name": tool_name,
            "result": result,
            "run_id": run_id
        }, default=str).encode("utf-8")
        
        # future = self.publisher.publish(self.topic_path, message_data)
        # message_id = future.result()
        message_id = f"mock_message_id_for_{run_id}"
        
        print(f"MOCK PUBLISH: Message to Pub/Sub topic '{self.topic_id}' with ID: {message_id}")
        return {"status": "success", "message_id": message_id}
        
    def __str__(self):
        return f"PubSubSink(topic='{self.topic_id}')"