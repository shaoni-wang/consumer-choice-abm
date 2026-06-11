# Consumer Choice ABM - User Guide

## 📖 Overview

Consumer Choice ABM is an Agent-Based Modeling simulation that studies how consumers choose between two competing products (Orange and Blue) under the influence of personal experience, social networks, and information exchange. The model replicates classic innovation diffusion and social influence dynamics.

## 🎯 Key Features

- **Interactive Web Interface**: Real-time visualization of agents and social networks
- **Live Parameter Tuning**: Adjust agent and product parameters 
- **Social Network Dynamics**: Agents connected through geometric proximity networks
- **Dual Influence Mechanism**: Balance between personal experience and social norms
- **Real-time Charts**: Track market shares and clustering coefficients over time

## 🏗️ Model Architecture
<img width="397" height="204" alt="Screenshot 2026-06-11 at 22 13 54" src="https://github.com/user-attachments/assets/0d791039-3531-453d-8a52-160b6dcaa8ff" />



## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
git clone https://github.com/yourusername/consumer-choice-abm.git

cd consumer-choice-abm

### Step 2: Install Dependencies
pip install -r requirements.txt

### Step 3: Run the Simulation
python app.py

### Step 4:  Open Browser
Navigate to: http://localhost:5001

The interface will automatically open in your default browser.

### Step 5: How to Run a Scenario
To begin your exploration, first configure the parameters based on the research question you wish to investigate. For example, if you want to watch how product quality drives market share, set Quality Orange and Quality Blue to different values (e.g., 0.2 vs 0.8). To see how peer pressure influences choices, increase Norm Influence and Info Exchange (e.g., 0.7 and 0.9). Alternatively, to observe how information sharing accelerates adoption, set Info Exchange high (e.g., 0.95) with moderate Exploration (e.g., 0.05). After adjusting your parameters, click the Setup button if you modified any Community Settings (Number of Consumers, Avg Connections, or Initial Orange %), then click Start to watch the simulation run.

As the simulation runs, observe three key visual elements simultaneously. The Agent Space shows orange and blue circles representing consumer choices, with circle size indicating satisfaction level and gray lines representing social network connections. The Market Share chart on the bottom-left tracks how orange and blue adoption evolves over time, while the Clustering chart on the bottom-right shows how socially clustered agents become. The Statistics panel displays current step number, market share percentage, and clustering coefficient in real-time.

A unique feature of this interface is the ability to interact with the simulation while it runs. Try adjusting the Agent Settings (Norm Influence, Info Exchange, Exploration) or Product Settings (Quality Orange, Quality Blue) during simulation to see immediate behavioral changes without restarting. You can also use the Pause button to freeze and inspect a specific moment, Reset to restart with the same parameters, or Step to advance one tick at a time for careful analysis. This real-time interactivity allows you to explore causal relationships dynamically.

## 🙏 Acknowledgments
This Python implementation is based on the original NetLogo model:

Jager, W., Wang, S. (2024). NetLogo Consumer Choice model.
http://ccl.northwestern.edu/netlogo/models/ConsumerChoice. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.
