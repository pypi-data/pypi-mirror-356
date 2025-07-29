from dataclasses import dataclass
from chainsaws.aws.shared.config import APIConfig

@dataclass
class APIGatewayManagementAPIConfig(APIConfig):
    """Configuration for APIGatewayManagement."""
    endpoint_url: str