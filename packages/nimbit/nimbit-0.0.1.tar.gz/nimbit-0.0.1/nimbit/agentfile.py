import yaml
from typing import Dict, Any, Tuple

class Agentfile:
    def __init__(self, meta: Dict[str, Any], dockerfile: str):
        self.meta = meta
        self.dockerfile = dockerfile

    @classmethod
    def from_file(cls, path: str) -> 'Agentfile':
        with open(path, 'r') as f:
            content = f.read()
        return cls.from_string(content)

    @classmethod
    def from_string(cls, content: str) -> 'Agentfile':
        # Split on the first occurrence of '---' (YAML section separator)
        if '---' not in content:
            raise ValueError("Agentfile must contain a '---' separator between meta and Dockerfile sections.")
        meta_section, dockerfile_section = content.split('---', 1)
        meta = yaml.safe_load(meta_section.strip())
        dockerfile = dockerfile_section.lstrip('\n')
        return cls(meta, dockerfile)

    def get_meta(self) -> Dict[str, Any]:
        return self.meta

    def get_dockerfile(self) -> str:
        return self.dockerfile
