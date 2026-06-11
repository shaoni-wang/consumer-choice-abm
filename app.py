from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time
import eventlet
from eventlet import sleep

from config import Config
from model.abm_model import ABM_Model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global model instance
model = None
simulation_thread = None
is_running = False


def get_agents_data():
    """Extract agent data for visualization"""
    if not model or not model.consumers:
        return []
    
    agents_data = []
    for c in model.consumers:
        agents_data.append({
            'id': c.id,
            'x': c.x,
            'y': c.y,
            'choice': c.choice,
            'satisfaction': c.satisfaction[c.choice] if c.satisfaction[c.choice] else 0.5,
            'utility0': round(c.utilities[0], 3),
            'utility1': round(c.utilities[1], 3),
            'neighbors': [n.id for n in c.neighbors]
        })
    return agents_data


def get_network_data():
    """Extract network edges for visualization"""
    if not model or not model.consumers:
        return []
    
    edges = []
    seen = set()
    for c in model.consumers:
        for n in c.neighbors:
            edge = tuple(sorted([c.id, n.id]))
            if edge not in seen:
                seen.add(edge)
                edges.append({'source': c.id, 'target': n.id})
    return edges


def run_simulation():
    """Background thread to run simulation steps"""
    global is_running, model
    
    while is_running:
        if model:
            try:
                # Perform one simulation step
                model.step()
                
                # Prepare data
                data = {
                    'step': model.step_count,
                    'market_share': model.history['market_share'][-1] if model.history['market_share'] else 0,
                    'clustering': model.history['clustering'][-1] if model.history['clustering'] else 0,
                    'agents': get_agents_data(),
                    'network': get_network_data()
                }
                
                # Emit using socketio's background task
                socketio.emit('simulation_update', data)
                
                # Control simulation speed
                eventlet.sleep(0.1)
                
            except Exception as e:
                print(f"Error in simulation: {e}")
                break


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print('✓ Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    print('✗ Client disconnected')


@socketio.on('setup_simulation')
def handle_setup(data):
    """Initialize simulation with parameters"""
    global model, simulation_thread, is_running
    print("🔄 Setting up simulation...")
    
    # Stop any running simulation
    if is_running:
        is_running = False
        if simulation_thread:
            simulation_thread.join(timeout=1)
    
    # Update config with UI parameters
    Config.NUM_CONSUMERS = int(data.get('num_consumers', 100))
    Config.AVG_CONNECTIONS = float(data.get('avg_connections', 6))
    Config.INIT_ORANGE_PCT = float(data.get('init_orange_pct', 50))
    Config.QUALITY_ORANGE = float(data.get('quality_orange', 0.45))
    Config.QUALITY_BLUE = float(data.get('quality_blue', 0.50))
    Config.NORM_INFLUENCE = float(data.get('norm_influence', 0.00))
    Config.INFO_EXCHANGE = float(data.get('info_exchange', 0.50))
    Config.EXPLORATION = float(data.get('exploration', 0.01))
    
    print(f"  - Consumers: {Config.NUM_CONSUMERS}")
    print(f"  - Orange quality: {Config.QUALITY_ORANGE}, Blue quality: {Config.QUALITY_BLUE}")
    
    # Create and setup new model
    model = ABM_Model(Config)
    model.setup()
    
    # Send initial data
    agents_data = get_agents_data()
    network_data = get_network_data()
    
    print(f"  - Agents created: {len(agents_data)}")
    print(f"  - Network edges: {len(network_data)}")
    
    emit('simulation_update', {
        'step': 0,
        'market_share': model.get_market_share(),
        'clustering': 0,
        'agents': agents_data,
        'network': network_data
    })
    
    print("✓ Simulation setup complete")


@socketio.on('start_simulation')
def handle_start():
    """Start the simulation loop"""
    global is_running, simulation_thread
    print("▶ Starting simulation...")
    
    if not is_running and model:
        is_running = True
        # Use eventlet.spawn instead of threading for better compatibility
        simulation_thread = eventlet.spawn(run_simulation)
        emit('simulation_started', {'status': 'running'})


@socketio.on('pause_simulation')
def handle_pause():
    """Pause the simulation"""
    global is_running
    print("⏸ Pausing simulation...")
    is_running = False
    emit('simulation_paused', {'status': 'paused'})


@socketio.on('reset_simulation')
def handle_reset():
    """Reset simulation to initial state"""
    global model, is_running
    print("🔄 Resetting simulation...")
    
    is_running = False
    if model:
        model.setup()
        emit('simulation_update', {
            'step': 0,
            'market_share': model.get_market_share(),
            'clustering': 0,
            'agents': get_agents_data(),
            'network': get_network_data()
        })


@socketio.on('step_simulation')
def handle_step():
    """Run single simulation step"""
    global model
    print("👣 Running single step...")
    
    if model:
        model.step()
        emit('simulation_update', {
            'step': model.step_count,
            'market_share': model.history['market_share'][-1] if model.history['market_share'] else 0,
            'clustering': model.history['clustering'][-1] if model.history['clustering'] else 0,
            'agents': get_agents_data(),
            'network': get_network_data()
        })

@socketio.on('update_parameters')
def handle_update_parameters(data):
    """Update model parameters in real-time without resetting"""
    global model
    
    if model:
        # Update config with new parameters
        Config.NUM_CONSUMERS = int(data.get('num_consumers', 100))
        Config.AVG_CONNECTIONS = float(data.get('avg_connections', 6))
        Config.INIT_ORANGE_PCT = float(data.get('init_orange_pct', 50))
        Config.QUALITY_ORANGE = float(data.get('quality_orange', 0.45))
        Config.QUALITY_BLUE = float(data.get('quality_blue', 0.50))
        Config.NORM_INFLUENCE = float(data.get('norm_influence', 0.00))
        Config.INFO_EXCHANGE = float(data.get('info_exchange', 0.50))
        Config.EXPLORATION = float(data.get('exploration', 0.01))
        
        # Update model's quality references
        model.qualities = Config.get_quality_list()
        
        # Update all consumers' quality references
        for consumer in model.consumers:
            consumer.qualities = model.qualities
        
        print(f"✓ Parameters updated in real-time")
        print(f"  - Quality Orange: {Config.QUALITY_ORANGE}, Quality Blue: {Config.QUALITY_BLUE}")
        print(f"  - Norm Influence: {Config.NORM_INFLUENCE}, Info Exchange: {Config.INFO_EXCHANGE}")
        print(f"  - Exploration: {Config.EXPLORATION}")
        
        emit('parameters_updated', {'status': 'success'})

if __name__ == '__main__':
    import webbrowser
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5001')
        print("\n🌐 Opening browser at http://localhost:5001")
    
    threading.Thread(target=open_browser, daemon=True).start()
    print("\n🚀 Starting server at http://localhost:5001")
    socketio.run(app, host='127.0.0.1', port=5001, debug=True, use_reloader=False)