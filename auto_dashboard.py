from flask import Flask, render_template_string, jsonify, request
from web3 import Web3
import json
import time
import schedule
import threading
from datetime import datetime
import requests

app = Flask(__name__)

# CONFIGURACIÓN AUTOMÁTICA
CONFIG = {
    'TOKEN_CONTRACT': '0xfb146E2601c5F77743E4888E75D6577C2F56bAbb',
    'TOKEN_SYMBOL': 'FMC',
    'TOKEN_NAME': 'FlashMorCoin',
    'OWNER_WALLET': '0xTU_WALLET_AQUI',  # Cambia por tu wallet
    'PRIVATE_KEY': 'TU_PRIVATE_KEY_AQUI'  # Cambia por tu private key
}

# SISTEMA DE AUTOMATIZACIÓN
class AutoSystem:
    def __init__(self):
        self.web3 = self.connect_web3()
        self.auto_tasks = {
            'liquidity': {'last_run': None, 'status': 'waiting'},
            'buyback': {'last_run': None, 'status': 'waiting'},
            'rewards': {'last_run': None, 'status': 'waiting'},
            'marketing': {'last_run': None, 'status': 'waiting'}
        }
        self.stats = {
            'total_liquidity_added': 0,
            'total_buyback': 0,
            'total_rewards': 0,
            'total_transactions': 0
        }
        
    def connect_web3(self):
        """Conexión automática a múltiples RPCs"""
        rpcs = [
            "https://polygon-rpc.com",
            "https://rpc-mainnet.matic.network",
            "https://rpc.ankr.com/polygon",
            "https://polygon-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014",
            "https://purple-bold-sunset.matic.quiknode.pro/6e2958c9720ad8d75f46b01d483e002df46d4524"
        ]
        
        for rpc in rpcs:
            try:
                web3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 10}))
                if web3.is_connected():
                    print(f"✅ Conectado: {rpc[:50]}...")
                    return web3
            except:
                continue
        return None

    def get_token_contract(self):
        """Obtener contrato del token"""
        abi = [
            {
                "constant": True, "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": False, "inputs": [
                    {"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}
                ],
                "name": "transfer", "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "constant": True, "inputs": [],
                "name": "name", "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
            {
                "constant": True, "inputs": [],
                "name": "symbol", "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
            {
                "constant": True, "inputs": [],
                "name": "decimals", "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True, "inputs": [],
                "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        return self.web3.eth.contract(
            address=Web3.to_checksum_address(CONFIG['TOKEN_CONTRACT']),
            abi=abi
        )

    # ACCIONES AUTOMÁTICAS
    def auto_add_liquidity(self):
        """Añadir liquidez automáticamente"""
        try:
            print("💧 Ejecutando Auto-Liquidez...")
            self.auto_tasks['liquidity']['status'] = 'running'
            self.auto_tasks['liquidity']['last_run'] = datetime.now().isoformat()
            
            # Simular añadir liquidez (en producción sería real)
            time.sleep(2)
            
            self.stats['total_liquidity_added'] += 1000
            self.stats['total_transactions'] += 1
            
            self.auto_tasks['liquidity']['status'] = 'completed'
            return {"status": "success", "message": "Liquidez añadida automáticamente"}
            
        except Exception as e:
            self.auto_tasks['liquidity']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_buyback(self):
        """Ejecutar buyback automático"""
        try:
            print("🔄 Ejecutando Auto-Buyback...")
            self.auto_tasks['buyback']['status'] = 'running'
            self.auto_tasks['buyback']['last_run'] = datetime.now().isoformat()
            
            # Simular buyback
            time.sleep(1)
            
            self.stats['total_buyback'] += 500
            self.stats['total_transactions'] += 1
            
            self.auto_tasks['buyback']['status'] = 'completed'
            return {"status": "success", "message": "Buyback ejecutado automáticamente"}
            
        except Exception as e:
            self.auto_tasks['buyback']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_distribute_rewards(self):
        """Distribuir recompensas automáticamente"""
        try:
            print("🎁 Distribuyendo Recompensas...")
            self.auto_tasks['rewards']['status'] = 'running'
            self.auto_tasks['rewards']['last_run'] = datetime.now().isoformat()
            
            # Simular distribución
            time.sleep(3)
            
            self.stats['total_rewards'] += 200
            self.stats['total_transactions'] += 5
            
            self.auto_tasks['rewards']['status'] = 'completed'
            return {"status": "success", "message": "Recompensas distribuidas automáticamente"}
            
        except Exception as e:
            self.auto_tasks['rewards']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_marketing(self):
        """Ejecutar acciones de marketing"""
        try:
            print("📢 Ejecutando Marketing...")
            self.auto_tasks['marketing']['status'] = 'running'
            self.auto_tasks['marketing']['last_run'] = datetime.now().isoformat()
            
            # Simular acciones de marketing
            time.sleep(1)
            
            self.auto_tasks['marketing']['status'] = 'completed'
            return {"status": "success", "message": "Acciones de marketing ejecutadas"}
            
        except Exception as e:
            self.auto_tasks['marketing']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def start_auto_scheduler(self):
        """Iniciar programador automático"""
        # Programar tareas cada 5 minutos para demo (en producción serían horas/días)
        schedule.every(5).minutes.do(self.auto_add_liquidity)
        schedule.every(7).minutes.do(self.auto_buyback)
        schedule.every(10).minutes.do(self.auto_distribute_rewards)
        schedule.every(15).minutes.do(self.auto_marketing)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        print("✅ Programador automático iniciado")

# Instancia global del sistema automático
auto_system = AutoSystem()

# HTML COMPLETO CON INTERFAZ AUTOMÁTICA
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlashMorCoin - Sistema Automático</title>
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --dark: #1f2937;
            --light: #f8fafc;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            min-height: 100vh;
            padding: 20px;
            color: var(--dark);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        .auto-badge {
            background: var(--success);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin-left: 10px;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        
        .card h2 {
            color: var(--dark);
            margin-bottom: 20px;
            font-size: 1.6em;
            border-bottom: 3px solid var(--primary);
            padding-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .status-grid {
            display: grid;
            gap: 15px;
        }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .status-item:last-child {
            border-bottom: none;
        }
        
        .status-label {
            font-weight: 600;
            color: #555;
            font-size: 1em;
        }
        
        .status-value {
            color: var(--dark);
            font-weight: 500;
            text-align: right;
        }
        
        .connected { color: var(--success); font-weight: bold; }
        .disconnected { color: var(--danger); font-weight: bold; }
        .running { color: var(--warning); font-weight: bold; }
        .waiting { color: #6b7280; font-weight: bold; }
        
        .btn {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            margin: 8px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-success { background: linear-gradient(135deg, var(--success) 0%, #059669 100%); }
        .btn-warning { background: linear-gradient(135deg, var(--warning) 0%, #d97706 100%); }
        .btn-danger { background: linear-gradient(135deg, var(--danger) 0%, #dc2626 100%); }
        
        .btn-small {
            padding: 10px 15px;
            font-size: 14px;
            width: auto;
            margin: 5px;
        }
        
        .action-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        .input-group label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        
        .input-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: #f9fafb;
        }
        
        .input-group input:focus {
            outline: none;
            border-color: var(--primary);
            background: white;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 12px;
            background: #f8fafc;
            border-left: 4px solid var(--primary);
            animation: fadeIn 0.5s ease;
        }
        
        .error {
            background: #fef2f2;
            border-left-color: var(--danger);
            color: #dc2626;
        }
        
        .success {
            background: #f0fdf4;
            border-left-color: var(--success);
            color: #059669;
        }
        
        .warning {
            background: #fffbeb;
            border-left-color: var(--warning);
            color: #d97706;
        }
        
        .loading {
            text-align: center;
            padding: 30px;
            color: var(--primary);
            font-size: 1.1em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
            border: 2px solid #e5e7eb;
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        
        .stat-value {
            font-size: 1.8em;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #6b7280;
            font-weight: 600;
        }
        
        .task-status {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            background: #f8fafc;
            border-radius: 8px;
            margin: 5px 0;
        }
        
        .status-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }
        
        .status-running { background: var(--warning); }
        .status-completed { background: var(--success); }
        .status-waiting { background: #6b7280; }
        .status-failed { background: var(--danger); }
        
        .contract-box {
            background: #fff7ed;
            border: 2px solid #fdba74;
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
            word-break: break-all;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }
        
        .auto-controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        .last-update {
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 FlashMorCoin</h1>
            <p>Sistema Automático Completo - Polygon Network</p>
            <div class="auto-badge">MODO AUTOMÁTICO ACTIVADO</div>
        </div>

        <div class="dashboard">
            <!-- Panel de Control Automático -->
            <div class="card">
                <h2>🎮 Control Central</h2>
                <div class="status-grid">
                    <div class="status-item">
                        <span class="status-label">Estado Sistema:</span>
                        <span class="status-value connected" id="systemStatus">✅ ACTIVO</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Blockchain:</span>
                        <span class="status-value" id="blockchainStatus">Verificando...</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Última Actualización:</span>
                        <span class="status-value" id="lastUpdate">--:--:--</span>
                    </div>
                </div>
                
                <div class="auto-controls">
                    <button class="btn btn-success" onclick="runAction('liquidity')">
                        💧 Auto-Liquidez
                    </button>
                    <button class="btn btn-warning" onclick="runAction('buyback')">
                        🔄 Auto-Buyback
                    </button>
                    <button class="btn" onclick="runAction('rewards')">
                        🎁 Auto-Recompensas
                    </button>
                    <button class="btn" onclick="runAction('marketing')">
                        📢 Auto-Marketing
                    </button>
                </div>
                
                <button class="btn btn-danger" onclick="runAllActions()">
                    🚀 EJECUTAR TODAS LAS ACCIONES
                </button>
            </div>

            <!-- Estado de Tareas Automáticas -->
            <div class="card">
                <h2>📊 Tareas Automáticas</h2>
                <div id="tasksStatus">
                    <div class="loading">Cargando estado de tareas...</div>
                </div>
                <div class="last-update" id="tasksUpdate"></div>
            </div>

            <!-- Estadísticas en Tiempo Real -->
            <div class="card">
                <h2>📈 Estadísticas Automáticas</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="statLiquidity">0</div>
                        <div class="stat-label">Liquidez Añadida</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statBuyback">0</div>
                        <div class="stat-label">Total Buyback</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statRewards">0</div>
                        <div class="stat-label">Recompensas</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="statTransactions">0</div>
                        <div class="stat-label">Total Transacciones</div>
                    </div>
                </div>
            </div>

            <!-- Información del Token -->
            <div class="card">
                <h2>🪙 FlashMorCoin (FMC)</h2>
                <div id="tokenInfo">
                    <div class="loading">Cargando información del token...</div>
                </div>
                <div class="contract-box">
                    <strong>CONTRATO AUTOMÁTICO:</strong><br>
                    0xfb146E2601c5F77743E4888E75D6577C2F56bAbb
                </div>
            </div>

            <!-- Consultas Rápidas -->
            <div class="card">
                <h2>🔍 Consultas Rápidas</h2>
                <div class="input-group">
                    <label>Wallet a Consultar:</label>
                    <input type="text" id="walletAddress" 
                           value="0xfb146E2601c5F77743E4888E75D6577C2F56bAbb"
                           placeholder="0x...">
                </div>
                <div class="action-buttons">
                    <button class="btn btn-small" onclick="getBalance()">
                        💰 Balance FMC
                    </button>
                    <button class="btn btn-small btn-success" onclick="getTokenInfo()">
                        📊 Info Token
                    </button>
                    <button class="btn btn-small btn-warning" onclick="getSystemStats()">
                        📈 Estadísticas
                    </button>
                    <button class="btn btn-small" onclick="refreshAll()">
                        🔄 Actualizar Todo
                    </button>
                </div>
                <div id="queryResult"></div>
            </div>

            <!-- Log de Actividad -->
            <div class="card">
                <h2>📝 Log de Actividad</h2>
                <div id="activityLog" style="max-height: 300px; overflow-y: auto;">
                    <div class="loading">Inicializando sistema...</div>
                </div>
                <button class="btn btn-small" onclick="clearLog()">
                    🗑️ Limpiar Log
                </button>
            </div>
        </div>
    </div>

    <script>
        let activityLog = [];
        
        // Función para agregar al log
        function addToLog(message, type = 'info') {
            const timestamp = new Date().toLocaleTimeString();
            activityLog.unshift({timestamp, message, type});
            
            if (activityLog.length > 20) activityLog.pop();
            
            updateLogDisplay();
        }
        
        // Actualizar display del log
        function updateLogDisplay() {
            const logElement = document.getElementById('activityLog');
            logElement.innerHTML = activityLog.map(entry => `
                <div class="task-status" style="border-left: 3px solid ${
                    entry.type === 'success' ? '#10b981' : 
                    entry.type === 'error' ? '#ef4444' : 
                    entry.type === 'warning' ? '#f59e0b' : '#667eea'
                }">
                    <div class="status-dot status-${entry.type}"></div>
                    <div style="flex: 1;">
                        <small style="color: #6b7280;">[${entry.timestamp}]</small><br>
                        ${entry.message}
                    </div>
                </div>
            `).join('');
        }
        
        // Ejecutar acción automática
        async function runAction(action) {
            addToLog(`Iniciando ${action}...`, 'info');
            
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = '⏳ Ejecutando...';
            button.disabled = true;
            
            try {
                const response = await fetch(`/api/auto/${action}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    addToLog(`✅ ${data.message}`, 'success');
                    button.innerHTML = '✅ Completado';
                } else {
                    addToLog(`❌ Error en ${action}: ${data.message}`, 'error');
                    button.innerHTML = '❌ Error';
                }
                
                // Actualizar estadísticas
                getSystemStats();
                getTasksStatus();
                
            } catch (error) {
                addToLog(`❌ Error de conexión: ${error.message}`, 'error');
                button.innerHTML = '❌ Falló';
            }
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        }
        
        // Ejecutar todas las acciones
        async function runAllActions() {
            addToLog('🚀 Iniciando ejecución completa...', 'warning');
            
            const actions = ['liquidity', 'buyback', 'rewards', 'marketing'];
            const button = event.target;
            const originalText = button.innerHTML;
            
            button.innerHTML = '⏳ Ejecutando Todo...';
            button.disabled = true;
            
            for (const action of actions) {
                await runAction(action);
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
            
            button.innerHTML = '🎉 Todo Completado!';
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 5000);
        }
        
        // Obtener estado de las tareas
        async function getTasksStatus() {
            try {
                const response = await fetch('/api/auto/status');
                const data = await response.json();
                
                document.getElementById('tasksStatus').innerHTML = `
                    ${Object.entries(data.tasks).map(([task, info]) => `
                        <div class="task-status">
                            <div class="status-dot status-${info.status}"></div>
                            <div style="flex: 1;">
                                <strong>${task.toUpperCase()}</strong><br>
                                <small>Última ejecución: ${info.last_run || 'Nunca'}</small>
                            </div>
                            <span class="${info.status}">${info.status.toUpperCase()}</span>
                        </div>
                    `).join('')}
                `;
                
                document.getElementById('tasksUpdate').textContent = 
                    `Actualizado: ${new Date().toLocaleTimeString()}`;
                    
            } catch (error) {
                console.error('Error obteniendo estado:', error);
            }
        }
        
        // Obtener estadísticas del sistema
        async function getSystemStats() {
            try {
                const response = await fetch('/api/auto/stats');
                const data = await response.json();
                
                document.getElementById('statLiquidity').textContent = 
                    data.total_liquidity_added.toLocaleString();
                document.getElementById('statBuyback').textContent = 
                    data.total_buyback.toLocaleString();
                document.getElementById('statRewards').textContent = 
                    data.total_rewards.toLocaleString();
                document.getElementById('statTransactions').textContent = 
                    data.total_transactions.toLocaleString();
                    
            } catch (error) {
                console.error('Error obteniendo stats:', error);
            }
        }
        
        // Obtener información del token
        async function getTokenInfo() {
            const tokenElement = document.getElementById('tokenInfo');
            tokenElement.innerHTML = '<div class="loading">Consultando blockchain...</div>';
            
            try {
                const response = await fetch('/api/token/info');
                const data = await response.json();
                
                if (data.error) {
                    tokenElement.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                } else {
                    tokenElement.innerHTML = `
                        <div class="status-grid">
                            <div class="status-item">
                                <span class="status-label">Nombre:</span>
                                <span class="status-value">${data.name}</span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Símbolo:</span>
                                <span class="status-value">${data.symbol}</span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Decimales:</span>
                                <span class="status-value">${data.decimals}</span>
                            </div>
                            <div class="status-item">
                                <span class="status-label">Supply Total:</span>
                                <span class="status-value">${data.formatted_supply.toLocaleString()} ${data.symbol}</span>
                            </div>
                        </div>
                    `;
                }
            } catch (error) {
                tokenElement.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
        }
        
        // Obtener balance
        async function getBalance() {
            const walletAddress = document.getElementById('walletAddress').value.trim();
            const resultElement = document.getElementById('queryResult');
            
            if (!walletAddress) {
                resultElement.innerHTML = '<div class="error">Ingresa una dirección</div>';
                return;
            }
            
            resultElement.innerHTML = '<div class="loading">Consultando balance...</div>';
            
            try {
                const response = await fetch('/api/balance/' + walletAddress);
                const data = await response.json();
                
                if (data.error) {
                    resultElement.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                } else {
                    resultElement.innerHTML = `
                        <div class="success">
                            <strong>✅ Balance Encontrado</strong><br><br>
                            <strong>Wallet:</strong> ${data.address}<br>
                            <strong>Balance FMC:</strong> ${data.balance} ${data.symbol}<br>
                            <strong>Red:</strong> Polygon Mainnet
                        </div>
                    `;
                    addToLog(`Consultado balance: ${data.balance} FMC`, 'success');
                }
            } catch (error) {
                resultElement.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
        }
        
        // Verificar estado de blockchain
        async function checkBlockchainStatus() {
            try {
                const response = await fetch('/api/blockchain/status');
                const data = await response.json();
                
                const statusElement = document.getElementById('blockchainStatus');
                if (data.connected) {
                    statusElement.innerHTML = '<span class="connected">✅ CONECTADO</span>';
                    statusElement.className = 'status-value connected';
                } else {
                    statusElement.innerHTML = '<span class="disconnected">❌ DESCONECTADO</span>';
                    statusElement.className = 'status-value disconnected';
                }
            } catch (error) {
                document.getElementById('blockchainStatus').innerHTML = 
                    '<span class="disconnected">❌ ERROR</span>';
            }
        }
        
        // Actualizar todo
        async function refreshAll() {
            addToLog('🔄 Actualizando toda la información...', 'info');
            await checkBlockchainStatus();
            await getTokenInfo();
            await getTasksStatus();
            await getSystemStats();
            document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
            addToLog('✅ Actualización completada', 'success');
        }
        
        // Limpiar log
        function clearLog() {
            activityLog = [];
            updateLogDisplay();
            addToLog('Log limpiado', 'info');
        }
        
        // Inicializar sistema
        document.addEventListener('DOMContentLoaded', function() {
            addToLog('Sistema FlashMorCoin iniciado', 'success');
            refreshAll();
            
            // Actualizar automáticamente cada 30 segundos
            setInterval(() => {
                refreshAll();
            }, 30000);
            
            // Actualizar estado de tareas cada 10 segundos
            setInterval(() => {
                getTasksStatus();
            }, 10000);
        });
    </script>
</body>
</html>
'''

# RUTAS DE LA API
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/auto/<action>')
def run_auto_action(action):
    """Ejecutar acción automática"""
    if action == 'liquidity':
        result = auto_system.auto_add_liquidity()
    elif action == 'buyback':
        result = auto_system.auto_buyback()
    elif action == 'rewards':
        result = auto_system.auto_distribute_rewards()
    elif action == 'marketing':
        result = auto_system.auto_marketing()
    else:
        result = {"status": "error", "message": "Acción no válida"}
    
    return jsonify(result)

@app.route('/api/auto/status')
def get_auto_status():
    """Obtener estado de las tareas automáticas"""
    return jsonify({
        'tasks': auto_system.auto_tasks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/auto/stats')
def get_auto_stats():
    """Obtener estadísticas automáticas"""
    return jsonify(auto_system.stats)

@app.route('/api/token/info')
def token_info():
    """Información del token"""
    try:
        if not auto_system.web3 or not auto_system.web3.is_connected():
            return jsonify({'error': 'Blockchain no conectada'})
        
        contract = auto_system.get_token_contract()
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        
        return jsonify({
            'name': name,
            'symbol': symbol,
            'decimals': decimals,
            'total_supply': total_supply,
            'formatted_supply': total_supply / (10 ** decimals),
            'contract_address': CONFIG['TOKEN_CONTRACT']
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/api/balance/<address>')
def get_balance(address):
    """Obtener balance"""
    try:
        if not auto_system.web3 or not auto_system.web3.is_connected():
            return jsonify({'error': 'Blockchain no conectada'})
        
        contract = auto_system.get_token_contract()
        balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        decimals = contract.functions.decimals().call()
        
        return jsonify({
            'balance': balance / (10 ** decimals),
            'address': address,
            'symbol': CONFIG['TOKEN_SYMBOL']
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/api/blockchain/status')
def blockchain_status():
    """Estado de la blockchain"""
    connected = auto_system.web3 and auto_system.web3.is_connected()
    return jsonify({
        'connected': connected,
        'block_number': auto_system.web3.eth.block_number if connected else 0,
        'chain_id': auto_system.web3.eth.chain_id if connected else 0
    })

if __name__ == '__main__':
    print("🚀 Iniciando FlashMorCoin - Sistema Automático Completo...")
    print(f"📍 Contrato: {CONFIG['TOKEN_CONTRACT']}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print("✅ Sistema automático iniciado")
    
    # Iniciar programador automático
    auto_system.start_auto_scheduler()
    
    app.run(host='0.0.0.0', port=5000, debug=True)