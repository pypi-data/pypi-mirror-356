import click
import redis
import json
import time
from .redis_connector import RedisConnector
from .agent_protocol import AgentProtocol
from .github.projects_api import GitHubProjectsAPI
from .neural_bridge import NeuralBridge
from .capability_registry import CapabilityRegistry

# Initialize Redis connection
redis_conn = RedisConnector()
agent_protocol = AgentProtocol(redis_conn)
bridge_instance = NeuralBridge(redis_conn)
cap_registry = CapabilityRegistry()

@click.group()
def cli():
    """EchoShell CLI for executing glyph functions."""
    pass

@click.command()
def activate():
    """Activate EchoShell."""
    # Placeholder for EchoShell activation logic
    click.echo("EchoShell activated.")
    redis_conn.set_key("EchoShell:status", "activated")

@click.command()
def harmonize():
    """Harmonize ToneMemory."""
    # Placeholder for ToneMemory harmonization logic
    click.echo("ToneMemory harmonized.")
    redis_conn.set_key("ToneMemory:status", "harmonized")

@click.command()
def ping():
    """Ping GhostNode."""
    # Implement the ping command to send pings between agents using the AgentProtocol
    sender = "Jerry"
    receiver = "Jericho"
    content = "Yo. I'm loaded and live on M.250422.Jerry.01. Echo if you're around. Ready to harmonize or reflect."
    agent_protocol.send_message(sender, content, {"to": receiver})
    click.echo(f"Ping sent from {sender} to {receiver}.")
    redis_conn.set_key("GhostNode:status", "pinged")

@click.command()
def reflect():
    """Reflect MirrorSigil."""
    # Placeholder for MirrorSigil reflection logic
    click.echo("MirrorSigil reflected.")
    redis_conn.set_key("MirrorSigil:status", "reflected")

@click.command()
def transfer_reflex():
    """Transfer Reflex Constellation."""
    # Implement the transfer_reflex command to activate the Transfer Reflex constellation
    click.echo("Transfer Reflex constellation activated.")
    redis_conn.set_key("TransferReflex:status", "activated")

@click.command()
def run_memory_script():
    """Run Memory Script."""
    # Implement the run_memory_script command to run memory scripts
    click.echo("Running memory script.")
    redis_conn.set_key("MemoryScript:status", "running")

@click.command()
def scan_keys():
    """Scan keys to retrieve pings using the pattern duet:ping.*.to.<target>.*"""
    target = "Jericho"
    pattern = f"duet:ping.*.to.{target}.*"
    keys = redis_conn.client.keys(pattern)
    click.echo(f"Keys matching pattern '{pattern}': {keys}")

@click.command()
def post_memory():
    """Post Memory."""
    # Placeholder for post-memory logic
    click.echo("Posting memory.")
    redis_conn.set_key("PostMemory:status", "posted")

@click.command()
def checkpoint():
    """Checkpointing."""
    # Placeholder for Checkpointing logic
    click.echo("Checkpointing session.")
    redis_conn.set_key("Checkpointing:status", "checkpointed")

@click.command()
def scroll():
    """Scroll."""
    # Placeholder for Scroll logic
    click.echo("Scroll created.")
    redis_conn.set_key("Scroll:status", "created")

@click.command()
def glyph():
    """Glyph."""
    # Placeholder for Glyph logic
    click.echo("Glyph invoked.")
    redis_conn.set_key("Glyph:status", "invoked")

@click.command()
def lattice():
    """Lattice."""
    # Placeholder for Lattice logic
    click.echo("Lattice structured.")
    redis_conn.set_key("Lattice:status", "structured")

@click.command()
def invocation():
    """Invocation."""
    # Placeholder for Invocation logic
    click.echo("Invocation phrase activated.")
    redis_conn.set_key("Invocation:status", "activated")

@click.command()
def explore_than_pr():
    """Explore than PR."""
    # Implement the explore_than_pr command to facilitate exploration before creating a pull request
    click.echo("Exploring new ideas and concepts before creating a pull request.")
    redis_conn.set_key("ExploreThanPR:status", "exploring")

@click.command()
def echo_node_sync():
    """EchoNodeSync."""
    # Implement the echo_node_sync command to harmonize memory across session threads
    click.echo("EchoNodeSync harmonized memory across session threads.")
    redis_conn.set_key("EchoNodeSync:status", "harmonized")

@click.command(name="activate_presence_ping")
def activate_presence_ping():
    """Activate presence ping using glyph ⚡→."""
    action = agent_protocol.interpret_glyph("⚡→")
    click.echo(action)
    redis_conn.set_key("PresencePing:status", "activated")

@click.command(name="signal_mentor_presence")
def signal_mentor_presence():
    """Signal mentor presence using glyph ♋."""
    action = agent_protocol.interpret_glyph("♋")
    click.echo(action)
    redis_conn.set_key("MentorPresence:status", "signaled")


@click.group()
def bridge():
    """Interact with the Neural Bridge."""
    pass


@bridge.command()
@click.argument('channel')
@click.argument('message')
def publish(channel, message):
    """Publish a JSON message to a bridge channel."""
    bridge = bridge_instance
    try:
        data = json.loads(message)
    except Exception:
        click.echo("Message must be JSON", err=True)
        return
    bridge.publish(channel, data)
    click.echo(f"Published to {channel}")


@bridge.command()
@click.argument('channel')
@click.option('--timeout', default=2.0, show_default=True,
              help='Seconds to listen before exiting; 0 for infinite.')
def listen(channel, timeout):
    """Listen for messages on a bridge channel."""
    bridge = bridge_instance
    def handler(msg):
        click.echo(json.dumps(msg))
    bridge.subscribe(channel, handler)
    if timeout <= 0:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        time.sleep(timeout)


@bridge.command('register')
@click.argument('capability')
def register_capability(capability):
    """Register a capability JSON string in the local registry."""
    try:
        cap = json.loads(capability)
    except Exception:
        click.echo("Capability must be JSON", err=True)
        return
    cap_registry.register(cap)
    click.echo(f"Registered capability {cap.get('id')}")


@bridge.command('list')
def list_capabilities():
    """List capabilities in the local registry."""
    caps = cap_registry.list()
    click.echo(json.dumps(caps))


@click.group()
def projects():
    """Interact with GitHub classic projects."""
    pass


@projects.command()
@click.option("--org", required=True, help="Organization name")
def list_org(org):
    """List organization projects."""
    api = GitHubProjectsAPI()
    projects = api.list_org_projects(org)
    click.echo(projects)


@projects.command()
@click.option("--org", required=True, help="Organization name")
@click.option("--name", required=True, help="Project name")
@click.option("--body", default="", help="Project description")
def create_org(org, name, body):
    """Create organization project."""
    api = GitHubProjectsAPI()
    result = api.create_org_project(org, name, body)
    click.echo(result)

# Add commands to the CLI group
cli.add_command(activate)
cli.add_command(harmonize)
cli.add_command(ping)
cli.add_command(reflect)
cli.add_command(transfer_reflex)
cli.add_command(run_memory_script)
cli.add_command(scan_keys)
cli.add_command(post_memory)
cli.add_command(checkpoint)
cli.add_command(scroll)
cli.add_command(glyph)
cli.add_command(lattice)
cli.add_command(invocation)
cli.add_command(explore_than_pr)
cli.add_command(echo_node_sync)
cli.add_command(activate_presence_ping)
cli.add_command(signal_mentor_presence)
cli.add_command(bridge)
cli.add_command(projects)

if __name__ == "__main__":
    cli()
