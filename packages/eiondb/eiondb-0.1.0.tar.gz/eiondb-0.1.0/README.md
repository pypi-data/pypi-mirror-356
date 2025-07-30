# Eion Python SDK

Python SDK for Eion - Shared memory storage and collaborative intelligence for AI agent systems.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Complete Examples](#complete-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Configuration](#configuration)
- [Features](#features)
- [License](#license)

## Installation

```bash
pip install eion-sdk-python
```

Or install from source:
```bash
git clone https://github.com/your-org/eion-sdk-python.git
cd eion-sdk-python
pip install -e .
```

## Quick Start

```python
from eion_sdk import EionClient

# Initialize client
client = EionClient(
    base_url="http://localhost:8080",
    cluster_api_key="your_cluster_api_key"
)

# Check server health
health = client.health_check()
print(f"Server status: {health['status']}")

# Create a user
user = client.create_user(
    user_id="demo_user",
    name="Demo User"
)

# Register an agent
agent = client.register_agent(
    agent_id="demo_agent",
    name="Demo Agent",
    permission="crud",
    description="A demo agent for testing"
)

# Create a session
session = client.create_session(
    session_id="demo_session",
    user_id="demo_user",
    session_name="Demo Session"
)

print("✅ Eion setup complete!")
```

## Authentication

The SDK supports multiple authentication methods:

### 1. Direct Parameters
```python
client = EionClient(
    base_url="http://localhost:8080",
    cluster_api_key="your_api_key"
)
```

### 2. Environment Variables
```bash
export EION_BASE_URL="http://localhost:8080"
export EION_CLUSTER_API_KEY="your_api_key"
```

```python
client = EionClient()  # Auto-loads from environment
```

### 3. Configuration File
Create `eion.yaml`:
```yaml
server:
  base_url: "http://localhost:8080"
auth:
  cluster_api_key: "your_api_key"
```

```python
client = EionClient(config_file="eion.yaml")
```

## Core Concepts

### Users
Users represent end-users of your application who will interact with agents.

### Agents
Agents are AI entities that can participate in sessions and perform operations based on their permissions.

### Sessions
Sessions are conversation contexts where users and agents interact.

### Agent Groups
Groups of agents that can be managed together and assigned to session types.

### Session Types
Templates that define which agent groups can participate in sessions.

## API Reference

### Health Check

```python
# Check server health
health = client.health_check()
# Returns: {"status": "healthy", "timestamp": "..."}
```

### User Management

```python
# Create user
user = client.create_user(
    user_id="user123",
    name="John Doe"  # Optional
)

# Delete user
client.delete_user("user123")
```

### Agent Management

```python
# Register agent
agent = client.register_agent(
    agent_id="agent123",
    name="My Agent",
    permission="crud",  # "r", "cr", "crud"
    description="Agent description",  # Optional
    guest=False  # Optional, default False
)

# Get agent details
agent = client.get_agent("agent123")

# Update agent
updated_agent = client.update_agent(
    "agent123",
    name="Updated Name",
    description="New description"
)

# List agents
agents = client.list_agents()
# With filters:
agents = client.list_agents(permission="crud", guest=False)

# Delete agent
client.delete_agent("agent123")
```

### Session Management

```python
# Create session
session = client.create_session(
    session_id="session123",
    user_id="user123",
    session_type_id="default",  # Optional
    session_name="My Session"   # Optional
)

# Delete session
client.delete_session("session123")
```

### Agent Group Management

```python
# Register agent group
group = client.register_agent_group(
    agent_group_id="group123",
    name="Customer Support Team",
    agent_ids=["agent1", "agent2"],  # Optional
    description="Support agents"     # Optional
)

# List agent groups
groups = client.list_agent_groups()

# Get group details
group = client.get_agent_group("group123")

# Update agent group
updated_group = client.update_agent_group(
    "group123",
    name="Updated Team Name",
    agent_ids=["agent1", "agent2", "agent3"]
)

# Delete agent group
client.delete_agent_group("group123")
```

### Session Type Management

```python
# Register session type
session_type = client.register_session_type(
    session_type_id="support_session",
    name="Customer Support",
    agent_group_ids=["support_team"],  # Optional
    description="Customer support sessions",  # Optional
    encryption="SHA256"  # Optional, default SHA256
)

# List session types
types = client.list_session_types()

# Get session type details
session_type = client.get_session_type("support_session")

# Update session type
updated_type = client.update_session_type(
    "support_session",
    name="Updated Support Type",
    description="Updated description"
)

# Delete session type
client.delete_session_type("support_session")
```

### Monitoring & Analytics

```python
# Monitor agent activity
agent_stats = client.monitor_agent(
    "agent123",
    time_range={
        "start_time": "2024-01-01T00:00:00Z",
        "end_time": "2024-01-31T23:59:59Z"
    }
)

# Monitor session activity
session_stats = client.monitor_session("session123")
```

## Complete Examples

### Customer Support System Setup

```python
from eion_sdk import EionClient, EionError

def setup_customer_support_system():
    """Set up a complete customer support system."""
    
    client = EionClient(
        base_url="http://localhost:8080",
        cluster_api_key="your_api_key"
    )
    
    try:
        # 1. Create users
        print("Creating users...")
        customer = client.create_user(
            user_id="customer_001",
            name="John Customer"
        )
        
        # 2. Register support agents
        print("Registering support agents...")
        agents = [
            ("support_l1", "Level 1 Support", "cr"),
            ("support_l2", "Level 2 Support", "crud"),
            ("supervisor", "Support Supervisor", "crud")
        ]
        
        for agent_id, name, permission in agents:
            client.register_agent(
                agent_id=agent_id,
                name=name,
                permission=permission,
                description=f"Customer support: {name}"
            )
        
        # 3. Create agent group
        print("Creating agent group...")
        support_group = client.register_agent_group(
            agent_group_id="support_team",
            name="Customer Support Team",
            agent_ids=["support_l1", "support_l2", "supervisor"],
            description="Complete customer support team"
        )
        
        # 4. Create session type
        print("Creating session type...")
        session_type = client.register_session_type(
            session_type_id="customer_support",
            name="Customer Support Session",
            agent_group_ids=["support_team"],
            description="Customer support conversations"
        )
        
        # 5. Create support session
        print("Creating support session...")
        session = client.create_session(
            session_id="support_session_001",
            user_id="customer_001",
            session_type_id="customer_support",
            session_name="Customer Issue #001"
        )
        
        print("✅ Customer support system setup complete!")
        
        # 6. Verify setup
        print("\n📊 System Summary:")
        agents_list = client.list_agents()
        print(f"   - {len(agents_list)} agents registered")
        
        groups_list = client.list_agent_groups()
        print(f"   - {len(groups_list)} agent groups created")
        
        types_list = client.list_session_types()
        print(f"   - {len(types_list)} session types configured")
        
        return True
        
    except EionError as e:
        print(f"❌ Setup failed: {e.message}")
        if e.status_code:
            print(f"   Status Code: {e.status_code}")
        return False

if __name__ == "__main__":
    setup_customer_support_system()
```

### Multi-Agent Development Team

```python
def setup_development_team():
    """Set up a software development team."""
    
    client = EionClient()
    
    # Create project manager user
    client.create_user("pm_user", "Project Manager")
    
    # Register development team agents
    dev_agents = [
        ("frontend_dev", "Frontend Developer", "crud"),
        ("backend_dev", "Backend Developer", "crud"),
        ("ui_designer", "UI/UX Designer", "cr"),
        ("qa_engineer", "QA Engineer", "crud"),
        ("devops_engineer", "DevOps Engineer", "crud")
    ]
    
    for agent_id, name, permission in dev_agents:
        client.register_agent(
            agent_id=agent_id,
            name=name,
            permission=permission,
            description=f"Development team: {name}"
        )
    
    # Create development team group
    client.register_agent_group(
        agent_group_id="dev_team",
        name="Software Development Team",
        agent_ids=[agent[0] for agent in dev_agents]
    )
    
    # Create project session type
    client.register_session_type(
        session_type_id="project_development",
        name="Project Development",
        agent_group_ids=["dev_team"]
    )
    
    # Create project session
    client.create_session(
        session_id="project_alpha",
        user_id="pm_user",
        session_type_id="project_development",
        session_name="Project Alpha Development"
    )
    
    print("🚀 Development team setup complete!")
```

### Bulk Operations

```python
def bulk_agent_registration():
    """Register multiple agents efficiently."""
    
    client = EionClient()
    
    # Agent configurations
    agent_configs = [
        {"id": "sales_001", "name": "Sales Agent 1", "perm": "cr"},
        {"id": "sales_002", "name": "Sales Agent 2", "perm": "cr"},
        {"id": "sales_003", "name": "Sales Agent 3", "perm": "cr"},
        {"id": "sales_manager", "name": "Sales Manager", "perm": "crud"},
    ]
    
    registered_agents = []
    
    for config in agent_configs:
        try:
            agent = client.register_agent(
                agent_id=config["id"],
                name=config["name"],
                permission=config["perm"],
                description=f"Sales team member: {config['name']}"
            )
            registered_agents.append(agent)
            print(f"✅ Registered: {config['id']}")
            
        except EionError as e:
            print(f"❌ Failed to register {config['id']}: {e.message}")
    
    return registered_agents
```

## Error Handling

The SDK provides structured exception handling:

```python
from eion_sdk import (
    EionClient, EionError, EionAuthenticationError, 
    EionValidationError, EionNotFoundError, EionServerError
)

try:
    client = EionClient()
    agent = client.register_agent("test_agent", "Test Agent")
    
except EionAuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    print("Please check your API key")
    
except EionValidationError as e:
    print(f"Validation error: {e.message}")
    if e.response_data.get("hint"):
        print(f"Hint: {e.response_data['hint']}")
    
except EionNotFoundError as e:
    print(f"Resource not found: {e.message}")
    
except EionServerError as e:
    print(f"Server error: {e.message}")
    print(f"Status code: {e.status_code}")
    
except EionError as e:
    print(f"General Eion error: {e.message}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Configuration Management
```python
# Use environment variables for production
import os

client = EionClient(
    base_url=os.getenv("EION_BASE_URL"),
    cluster_api_key=os.getenv("EION_CLUSTER_API_KEY")
)
```

### 2. Resource Naming
```python
# Use consistent, descriptive naming
user_id = f"user_{organization}_{department}_{timestamp}"
agent_id = f"agent_{team}_{role}_{version}"
session_id = f"session_{project}_{user}_{timestamp}"
```

### 3. Permission Management
```python
# Use appropriate permissions
# "r"    - Read only (monitoring agents)
# "cr"   - Create + Read (basic agents)
# "crud" - Full access (admin agents)

client.register_agent(
    agent_id="monitoring_agent",
    name="System Monitor",
    permission="r"  # Read-only for monitoring
)
```

### 4. Error Recovery
```python
def robust_agent_creation(client, agent_id, name):
    """Create agent with retry logic."""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            return client.register_agent(agent_id, name)
        except EionServerError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
        except EionValidationError:
            # Don't retry validation errors
            raise
```

### 5. Resource Cleanup
```python
def cleanup_test_resources(client, resource_ids):
    """Clean up test resources safely."""
    
    # Delete sessions first (they depend on users/agents)
    for session_id in resource_ids.get("sessions", []):
        try:
            client.delete_session(session_id)
        except EionNotFoundError:
            pass  # Already deleted
    
    # Then delete agents
    for agent_id in resource_ids.get("agents", []):
        try:
            client.delete_agent(agent_id)
        except EionNotFoundError:
            pass
    
    # Finally delete users
    for user_id in resource_ids.get("users", []):
        try:
            client.delete_user(user_id)
        except EionNotFoundError:
            pass
```

## Configuration

### Environment Variables

```bash
export EION_BASE_URL="http://localhost:8080"
export EION_CLUSTER_API_KEY="your_cluster_api_key"
```

### Configuration File

```python
client = EionClient(config_file="eion.yaml")
```

## Features

- **Cluster Management**: User, agent, and session management
- **Agent Registration**: Register and manage AI agents with permissions
- **Session Management**: Create and manage conversation sessions
- **Agent Groups**: Organize agents into teams
- **Session Types**: Define session templates with agent group assignments
- **Monitoring & Analytics**: Track agent performance and collaboration
- **Health Checks**: Monitor system health and connectivity
- **Structured Error Handling**: Comprehensive exception types
- **Authentication**: Multiple authentication methods
- **Type Hints**: Full type annotation support

## Documentation

- **Full API Documentation**: [docs/openapi.yaml](docs/openapi.yaml)
- **Agent API Guide**: [docs/agent-api-guide.json](docs/agent-api-guide.json)
- **Examples**: [example/](example/)

## Next Steps

1. **Explore Session-Level Operations**: Check out the [Agent API Guide](docs/agent-api-guide.json) for session-level operations
2. **Set up Monitoring**: Use the monitoring APIs to track agent and session performance
3. **Production Deployment**: Review security and scaling considerations for production use
4. **Advanced Features**: Explore agent groups and session types for complex workflows

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/eion-sdk-python/issues)
- **Documentation**: [Eion Documentation](https://docs.eion.ai)

## License

AGPL-3.0 License

---

Happy building with Eion! 🚀 