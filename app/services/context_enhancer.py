from typing import List, Dict
from app.models.messages import Message
from app.core.exceptions import ValidationError
from .rf_client import RFClient
import re

class ContextEnhancer:
    def __init__(self, rf_client: RFClient):
        self.rf_client = rf_client
        self.ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        self.domain_pattern = re.compile(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]\b')
        self.cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}', re.IGNORECASE)

    async def enhance_messages(self, messages: List[Message]) -> List[Message]:
        enhanced_messages = []
        for message in messages:
            if message.role == "user":
                context = await self._get_rf_context(message.get_text())
                if context:
                    enhanced_messages.append(Message(
                        role="system",
                        content=self._format_context(context)
                    ))
            enhanced_messages.append(message)
        return enhanced_messages

    async def _get_rf_context(self, text: str) -> Dict:
        context = {}
        ips = self.ip_pattern.findall(text)
        domains = self.domain_pattern.findall(text)
        cves = self.cve_pattern.findall(text)

        for ip in ips:
            try:
                info = await self.rf_client.get_ip_info(ip)
                context[f"ip_{ip}"] = info
            except Exception as e:
                continue

        # Similar for domains and CVEs
        return context

    def _format_context(self, context: Dict) -> str:
        # Format the context information for Claude
        formatted = ["Recorded Future Intelligence:"]
        for key, value in context.items():
            formatted.append(f"\n{key}:")
            if "risk" in value:
                formatted.append(f"Risk Score: {value['risk'].get('score', 'N/A')}")
            if "timestamps" in value:
                formatted.append(f"First Seen: {value['timestamps'].get('firstSeen', 'N/A')}")
        return "\n".join(formatted)
