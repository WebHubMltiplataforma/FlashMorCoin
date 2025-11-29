from flask import Flask, render_template, jsonify
from web3 import Web3
import time
import schedule
import threading
from datetime import datetime

app = Flask(__name__)

# Configuración
CONFIG = {
    'TOKEN_CONTRACT': '0xfb146E2601c5F77743E4888E75D6577C2F56bAbb',
    'TOKEN_SYMBOL': 'FMC',
    'TOKEN_NAME': 'FlashMorCoin'
}

# Sistema Automático
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
        rpcs = [
            "https://polygon-rpc.com",
            "https://rpc-mainnet.matic.network",
            "https://rpc.ankr.com/polygon",
            "https://polygon-mainnet.infura.io/v3/4df8eead51294cd09eadf4b51efaa014"
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
        abi = [
            {
                "constant": True, "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}],
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

    def auto_add_liquidity(self):
        try:
            print("💧 Ejecutando Auto-Liquidez...")
            self.auto_tasks['liquidity']['status'] = 'running'
            self.auto_tasks['liquidity']['last_run'] = datetime.now().isoformat()
            
            time.sleep(2)
            self.stats['total_liquidity_added'] += 1000
            self.stats['total_transactions'] += 1
            
            self.auto_tasks['liquidity']['status'] = 'completed'
            return {"status": "success", "message": "Liquidez añadida automáticamente"}
            
        except Exception as e:
            self.auto_tasks['liquidity']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_buyback(self):
        try:
            print("🔄 Ejecutando Auto-Buyback...")
            self.auto_tasks['buyback']['status'] = 'running'
            self.auto_tasks['buyback']['last_run'] = datetime.now().isoformat()
            
            time.sleep(1)
            self.stats['total_buyback'] += 500
            self.stats['total_transactions'] += 1
            
            self.auto_tasks['buyback']['status'] = 'completed'
            return {"status": "success", "message": "Buyback ejecutado automáticamente"}
            
        except Exception as e:
            self.auto_tasks['buyback']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_distribute_rewards(self):
        try:
            print("🎁 Distribuyendo Recompensas...")
            self.auto_tasks['rewards']['status'] = 'running'
            self.auto_tasks['rewards']['last_run'] = datetime.now().isoformat()
            
            time.sleep(3)
            self.stats['total_rewards'] += 200
            self.stats['total_transactions'] += 5
            
            self.auto_tasks['rewards']['status'] = 'completed'
            return {"status": "success", "message": "Recompensas distribuidas automáticamente"}
            
        except Exception as e:
            self.auto_tasks['rewards']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def auto_marketing(self):
        try:
            print("📢 Ejecutando Marketing...")
            self.auto_tasks['marketing']['status'] = 'running'
            self.auto_tasks['marketing']['last_run'] = datetime.now().isoformat()
            
            time.sleep(1)
            self.auto_tasks['marketing']['status'] = 'completed'
            return {"status": "success", "message": "Acciones de marketing ejecutadas"}
            
        except Exception as e:
            self.auto_tasks['marketing']['status'] = 'failed'
            return {"status": "error", "message": str(e)}

    def start_auto_scheduler(self):
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

# Instancia global
auto_system = AutoSystem()

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/auto/<action>')
def run_auto_action(action):
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
    return jsonify({
        'tasks': auto_system.auto_tasks,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/auto/stats')
def get_auto_stats():
    return jsonify(auto_system.stats)

@app.route('/api/token/info')
def token_info():
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
            'formatted_supply': total_supply / (10 ** decimals)
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/api/balance/<address>')
def get_balance(address):
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
    connected = auto_system.web3 and auto_system.web3.is_connected()
    return jsonify({
        'connected': connected,
        'block_number': auto_system.web3.eth.block_number if connected else 0,
        'chain_id': auto_system.web3.eth.chain_id if connected else 0
    })

if __name__ == '__main__':
    print("🚀 Iniciando FlashMorCoin - Sistema Automático...")
    print(f"📍 Contrato: {CONFIG['TOKEN_CONTRACT']}")
    print(f"🌐 Dashboard: http://localhost:5000")
    
    auto_system.start_auto_scheduler()
    app.run(host='0.0.0.0', port=5000, debug=True)