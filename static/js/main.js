// main.js - 修复版本
console.log('JavaScript loaded');

let socket = io();
let agentsData = [];
let networkData = [];

// Connection events
socket.on('connect', function() {
    console.log('✓ Connected to server');
    const statusEl = document.getElementById('status');
    if (statusEl) {
        statusEl.textContent = 'Connected';
        statusEl.style.color = '#28a745';
    }
});

socket.on('disconnect', function() {
    console.log('✗ Disconnected from server');
    const statusEl = document.getElementById('status');
    if (statusEl) {
        statusEl.textContent = 'Disconnected';
        statusEl.style.color = '#dc3545';
    }
});

socket.on('simulation_update', function(data) {
    console.log('Received update - Step:', data.step);
    console.log('  Agents:', data.agents ? data.agents.length : 0);
    console.log('  Network:', data.network ? data.network.length : 0);
    
    // Update statistics
    const stepCountEl = document.getElementById('step_count');
    const marketShareEl = document.getElementById('market_share');
    const clusteringEl = document.getElementById('clustering');
    
    if (stepCountEl) stepCountEl.textContent = data.step;
    if (marketShareEl) marketShareEl.textContent = data.market_share.toFixed(1) + '%';
    if (clusteringEl) clusteringEl.textContent = data.clustering.toFixed(3);
    
    // Update visualization data
    agentsData = data.agents || [];
    networkData = data.network || [];
});

// Button handlers
function setupSimulation() {
    console.log('Setup button clicked');
    const params = {
        num_consumers: parseInt(document.getElementById('num_consumers').value),
        avg_connections: parseFloat(document.getElementById('avg_connections').value),
        init_orange_pct: parseFloat(document.getElementById('init_orange_pct').value),
        quality_orange: parseFloat(document.getElementById('quality_orange').value),
        quality_blue: parseFloat(document.getElementById('quality_blue').value),
        norm_influence: parseFloat(document.getElementById('norm_influence').value),
        info_exchange: parseFloat(document.getElementById('info_exchange').value),
        exploration: parseFloat(document.getElementById('exploration').value)
    };
    console.log('Params:', params);
    socket.emit('setup_simulation', params);
}

function startSimulation() {
    console.log('Start button clicked');
    socket.emit('start_simulation');
}

function pauseSimulation() {
    console.log('Pause button clicked');
    socket.emit('pause_simulation');
}

function resetSimulation() {
    console.log('Reset button clicked');
    socket.emit('reset_simulation');
}

function stepSimulation() {
    console.log('Step button clicked');
    socket.emit('step_simulation');
}

// Update parameter displays
function updateParameterDisplays() {
    const numVal = document.getElementById('num_consumers_val');
    const avgVal = document.getElementById('avg_connections_val');
    const initVal = document.getElementById('init_orange_pct_val');
    const qOrangeVal = document.getElementById('quality_orange_val');
    const qBlueVal = document.getElementById('quality_blue_val');
    const normVal = document.getElementById('norm_influence_val');
    const infoVal = document.getElementById('info_exchange_val');
    const expVal = document.getElementById('exploration_val');
    
    if (numVal) numVal.textContent = document.getElementById('num_consumers').value;
    if (avgVal) avgVal.textContent = parseFloat(document.getElementById('avg_connections').value).toFixed(1);
    if (initVal) initVal.textContent = document.getElementById('init_orange_pct').value + '%';
    if (qOrangeVal) qOrangeVal.textContent = parseFloat(document.getElementById('quality_orange').value).toFixed(2);
    if (qBlueVal) qBlueVal.textContent = parseFloat(document.getElementById('quality_blue').value).toFixed(2);
    if (normVal) normVal.textContent = parseFloat(document.getElementById('norm_influence').value).toFixed(2);
    if (infoVal) infoVal.textContent = parseFloat(document.getElementById('info_exchange').value).toFixed(2);
    if (expVal) expVal.textContent = parseFloat(document.getElementById('exploration').value).toFixed(2);
}

// p5.js visualization
function setup() {
    const canvas = createCanvas(800, 600);
    canvas.parent('canvas-container');
    background(240);
    console.log('p5.js setup complete');
}

function draw() {
    background(240);
    
    // Draw network edges
    if (networkData && networkData.length > 0) {
        stroke(150, 150, 150, 100);
        strokeWeight(1);
        for (let edge of networkData) {
            let source = agentsData.find(a => a.id === edge.source);
            let target = agentsData.find(a => a.id === edge.target);
            if (source && target) {
                line(source.x, source.y, target.x, target.y);
            }
        }
    }
    
    // Draw agents
    if (agentsData && agentsData.length > 0) {
        for (let agent of agentsData) {
            if (agent.choice === 0) {
                fill(255, 165, 0);  // Orange
            } else {
                fill(0, 0, 255);     // Blue
            }
            
            let size = map(agent.satisfaction, 0, 1, 8, 20);
            noStroke();
            circle(agent.x, agent.y, size);
        }
    }
    
    // Display stats
    fill(0);
    noStroke();
    textSize(12);
    text(`Agents: ${agentsData.length}`, 10, 20);
    text(`Network edges: ${networkData.length}`, 10, 35);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded, setting up event listeners');
    
    // Add slider listeners
    const sliders = [
        'num_consumers', 'avg_connections', 'init_orange_pct',
        'quality_orange', 'quality_blue', 'norm_influence',
        'info_exchange', 'exploration'
    ];
    
    sliders.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener('input', updateParameterDisplays);
        }
    });
    
    // Add button listeners
    const setupBtn = document.getElementById('setup_btn');
    const startBtn = document.getElementById('start_btn');
    const pauseBtn = document.getElementById('pause_btn');
    const resetBtn = document.getElementById('reset_btn');
    const stepBtn = document.getElementById('step_btn');
    
    if (setupBtn) setupBtn.onclick = setupSimulation;
    if (startBtn) startBtn.onclick = startSimulation;
    if (pauseBtn) pauseBtn.onclick = pauseSimulation;
    if (resetBtn) resetBtn.onclick = resetSimulation;
    if (stepBtn) stepBtn.onclick = stepSimulation;
    
    // Update displays
    updateParameterDisplays();
    
    // Auto setup after connection
    setTimeout(() => {
        console.log('Auto-setup simulation');
        setupSimulation();
    }, 1000);
});