import click
import os
from nimbit.agentfile import Agentfile
import yaml
import tempfile
import shutil
import subprocess
from nimbit.utils.prompts import yellow
import json

@click.group()
def cli():
    """Nimbit CLI"""
    pass

# GET COMMANDS
@cli.group()
def get():
    """Get resources"""
    pass

@get.command()
def tenant():
    """Get tenants"""
    click.echo("[MOCK] Listing tenants: tenant1, tenant2, tenant3")

@get.command()
def workspaces():
    """Get workspaces"""
    click.echo("[MOCK] Listing workspaces: workspace1, workspace2")

@get.command()
def agents():
    """Get agents"""
    click.echo("[MOCK] Listing agents: agent1, agent2")

# CREATE COMMANDS
@cli.group()
def create():
    """Create resources"""
    pass

@create.command()
@click.argument('tenant_name')
def tenant(tenant_name):
    """Create a tenant"""
    click.echo(f"[MOCK] Created tenant: {tenant_name}")

@create.command()
@click.argument('workspace_name')
@click.option('--tenant', default='default', help='Tenant name')
def workspace(workspace_name, tenant):
    """Create a workspace"""
    click.echo(f"[MOCK] Created workspace: {workspace_name} under tenant: {tenant}")

@create.command()
@click.argument('agent_name')
@click.option('--agentfile', required=True, help='Path to agent file')
def agent(agent_name, agentfile):
    """Create an agent"""
    click.echo(f"[MOCK] Created agent: {agent_name} using file: {agentfile}")

# AGENT SUBCOMMANDS
@cli.group()
def agent():
    """Agent operations"""
    pass

@agent.command('listen')
@click.argument('agent_name')
def agent_listen(agent_name):
    """Listen to an agent"""
    click.echo(f"[MOCK] Listening to agent: {agent_name}")

@agent.group()
def image():
    """Agent image operations"""
    pass

@image.command('ls')
def image_ls():
    """List agent images (from ~/.nimbit/agent_images.json)"""
    images = load_agent_images()
    if not images:
        click.echo("No nimbit agent images found.")
        return
    click.echo(f"{'TAG':30} {'NAME':20} {'DESCRIPTION':30}")
    for img in images:
        meta = img.get('meta', {})
        click.echo(f"{img['tag']:30} {meta.get('name', ''):20} {meta.get('description', ''):30}")

@agent.command('rm')
@click.argument('image')
def agent_rm(image):
    """Remove an agent image by name:tag or ID, and from ~/.nimbit/agent_images.json"""
    import subprocess
    try:
        cmd = ['docker', 'rmi', image]
        click.echo(f"[INFO] Removing image: {image}")
        subprocess.run(cmd, check=True)
        click.echo(f"[SUCCESS] Removed image: {image}")
        # Remove from agent images list
        images = load_agent_images()
        images = [img for img in images if img['tag'] != image]
        save_agent_images(images)
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Failed to remove image: {e}")
    except Exception as e:
        click.echo(f"[ERROR] {e}")

@agent.command('run')
@click.argument('image')
@click.option('--port', type=int, default=None, help='Host port to map to the agent container (overrides metadata)')
@click.option('--detach', '-d', is_flag=True, default=False, help='Run container in background (detached)')
def agent_run(image, port, detach):
    """Run an agent image in a Docker container (interactive by default)."""
    import subprocess, sys
    # Try to get port from metadata if not provided
    images = load_agent_images()
    meta = None
    for img in images:
        if img['tag'] == image:
            meta = img.get('meta', {})
            break
    container_port = None
    if port:
        container_port = port
    elif meta and 'port' in meta:
        try:
            container_port = int(meta['port'])
        except Exception:
            container_port = None
    port_args = []
    if container_port:
        port_args = ['-p', f'{container_port}:{container_port}']
        click.echo(f"[INFO] Mapping port {container_port} -> {container_port}")
    try:
        cmd = ['docker', 'run']
        if detach:
            cmd.append('-d')
        else:
            cmd += ['-it']
        cmd += port_args + [image]
        click.echo(f"[INFO] Running: {' '.join(cmd)}")
        if detach:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            container_id = result.stdout.strip()
            click.echo(f"[SUCCESS] Agent running in container: {container_id}")
            if container_port:
                click.echo(f"[INFO] Access the agent at http://localhost:{container_port}")
        else:
            # Attach stdin/stdout for interactive mode
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Failed to run agent: {e.stderr or e}")
    except Exception as e:
        click.echo(f"[ERROR] {e}")

NIMBIT_HOME = os.path.expanduser('~/.nimbit')
AGENT_IMAGES_FILE = os.path.join(NIMBIT_HOME, 'agent_images.json')

def ensure_nimbit_home():
    if not os.path.exists(NIMBIT_HOME):
        os.makedirs(NIMBIT_HOME, exist_ok=True)
    if not os.path.exists(AGENT_IMAGES_FILE):
        with open(AGENT_IMAGES_FILE, 'w') as f:
            json.dump([], f)

def load_agent_images():
    ensure_nimbit_home()
    with open(AGENT_IMAGES_FILE, 'r') as f:
        return json.load(f)

def save_agent_images(images):
    ensure_nimbit_home()
    with open(AGENT_IMAGES_FILE, 'w') as f:
        json.dump(images, f, indent=2)

def build_docker_image(context, agentfile, meta, tag):
    import yaml, tempfile, shutil, subprocess, os
    print(yellow(f"[BUILD] Preparing Docker build context for tag: {tag}"))
    with tempfile.TemporaryDirectory() as build_ctx:
        # Copy all files from context to build_ctx
        for item in os.listdir(context):
            s = os.path.join(context, item)
            d = os.path.join(build_ctx, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        # Write metadata.yaml
        nimbit_dir = os.path.join(build_ctx, 'nimbit')
        os.makedirs(nimbit_dir, exist_ok=True)
        metadata_path = os.path.join(nimbit_dir, 'metadata.yaml')
        with open(metadata_path, 'w') as f:
            yaml.safe_dump(meta, f)
        # Write Dockerfile
        dockerfile_path = os.path.join(build_ctx, 'Dockerfile')
        with open(dockerfile_path, 'w') as f:
            f.write(agentfile.get_dockerfile())
        # Build the Docker image
        try:
            cmd = [
                'docker', 'build',
                '-t', tag,
                build_ctx
            ]
            print(yellow(f"[BUILD] Running: {' '.join(cmd)}"))
            subprocess.run(cmd, check=True)
            print(yellow(f"[SUCCESS] Built Docker image with tag: {tag}"))
            # Add to agent images list
            images = load_agent_images()
            images = [img for img in images if img['tag'] != tag]  # Remove any old entry for this tag
            images.append({
                'tag': tag,
                'meta': meta
            })
            save_agent_images(images)
        except FileNotFoundError:
            print(yellow("[ERROR] Docker is not installed or not in PATH."))
            raise click.Abort()
        except subprocess.CalledProcessError as e:
            print(yellow(f"[ERROR] Docker build failed: {e}"))
            raise click.Abort()

@agent.command('build')
@click.option('-t', '--tag', required=False, help='Tag for the built agent image (e.g., myagent:latest). If not provided, will use <name>:<version> from Agentfile.')
@click.argument('context', type=click.Path(exists=True, file_okay=False))
def agent_build(tag, context):
    """Build an agent image"""
    agentfile_path = os.path.join(context, 'Agentfile')
    if not os.path.isfile(agentfile_path):
        click.echo(f"[ERROR] No Agentfile found in {context}")
        raise click.Abort()
    try:
        agentfile = Agentfile.from_file(agentfile_path)
        meta = agentfile.get_meta()
        if not tag:
            name = meta.get('name', 'agent')
            version = meta.get('version', 'latest')
            tag = f"{name}:{version}"
            click.echo(f"[INFO] No tag provided. Using auto-generated tag: {tag}")
        click.echo(f"[INFO] Parsed Agentfile meta: {meta}")
        click.echo(f"[INFO] Dockerfile section:\n{agentfile.get_dockerfile()}")
        build_docker_image(context, agentfile, meta, tag)
    except Exception as e:
        click.echo(f"[ERROR] Failed to build agent: {e}")
        raise click.Abort()

@agent.command('push')
@click.argument('image')
def agent_push(image):
    """Push an agent image"""
    click.echo(f"[MOCK] Pushing agent image: {image}")

# LOGS COMMAND
@cli.command()
@click.argument('agent_name')
@click.option('--debug', is_flag=True, help='Show debug logs')
def logs(agent_name, debug):
    """Show logs for an agent"""
    if debug:
        click.echo(f"[MOCK] Showing DEBUG logs for agent: {agent_name}")
    else:
        click.echo(f"[MOCK] Showing logs for agent: {agent_name}")

if __name__ == '__main__':
    cli()
