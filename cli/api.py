from flask import Flask, jsonify, request
import os
import consul
import subprocess
import json
from pathlib import Path

app = Flask(__name__)

def get_state_manager():
    return consul.Consul()

def save_config(config):
    consul_client = get_state_manager()
    for key, value in config.items():
        consul_client.kv.put(f'config/{key}', value)

def get_config():
    consul_client = get_state_manager()
    config = {}
    index, items = consul_client.kv.get('config/', recurse=True) or (None, [])
    if items:
        for item in items:
            key = item['Key'].replace('config/', '')
            config[key] = item['Value'].decode() if item['Value'] else ''
    return config

@app.route('/config', methods=['GET', 'POST'])
def handle_config():
    if request.method == 'POST':
        config = request.json
        save_config(config)
        
        # Update .env file for services that need it
        env_content = []
        for key, value in config.items():
            env_content.append(f'{key}={value}')
        
        with open('.env', 'w') as f:
            f.write('\n'.join(env_content))
            
        return jsonify({'status': 'success'})
    else:
        return jsonify(get_config())

@app.route('/ansible/playbook/<playbook>', methods=['POST'])
def run_playbook(playbook):
    # Get variables from request
    vars_dict = request.json or {}
    
    # Create vars file
    vars_file = Path('ansible/vars.json')
    vars_file.write_text(json.dumps(vars_dict))
    
    # Run ansible playbook
    cmd = [
        'ansible-playbook',
        f'ansible/playbooks/{playbook}.yml',
        '-e', f'@{vars_file}'
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = process.communicate()
    
    return jsonify({
        'status': 'success' if process.returncode == 0 else 'error',
        'output': stdout.decode(),
        'error': stderr.decode() if stderr else None
    })

@app.route('/status/<server_type>')
def server_status(server_type):
    state_manager = get_state_manager()
    server_info = state_manager.kv.get(f'servers/{server_type}')[1]
    return jsonify(server_info or {'status': 'not_running'})

@app.route('/setup', methods=['POST'])
def initial_setup():
    """Handle initial setup with provided credentials"""
    config = request.json
    
    # Save configuration
    save_config(config)
    
    # Run initial setup playbook if provided
    if config.get('run_setup', False):
        return run_playbook('initial_setup')
    
    return jsonify({'status': 'success'})

@app.route('/validate/credentials', methods=['POST'])
def validate_credentials():
    """Validate provided credentials"""
    credentials = request.json
    valid = True
    messages = []
    
    # Check Hetzner token
    if 'HCLOUD_TOKEN' in credentials:
        try:
            # Add Hetzner API check
            pass
        except Exception as e:
            valid = False
            messages.append(f'Invalid Hetzner token: {str(e)}')
    
    # Check S3 credentials
    if credentials.get('S3_ENABLED') == 'true':
        try:
            # Add S3 connection check
            pass
        except Exception as e:
            valid = False
            messages.append(f'Invalid S3 credentials: {str(e)}')
    
    return jsonify({
        'valid': valid,
        'messages': messages
    })

@app.route('/start/<server_type>', methods=['POST'])
def start_server(server_type):
    # Run the appropriate Ansible playbook
    return run_playbook(f'start_{server_type}_server')

@app.route('/stop/<server_type>', methods=['POST'])
def stop_server(server_type):
    # Run the appropriate Ansible playbook
    return run_playbook(f'stop_{server_type}_server')

@app.route('/logs')
def get_logs():
    # Implement log retrieval
    return jsonify({'logs': []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)