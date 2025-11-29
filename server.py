from flask import Flask, render_template_string, jsonify
from web3 import Web3
import json
import os

app = Flask(__name__)

# Configuración
CONFIG = {
    'TOKEN_CONTRACT': '0xfb146E2601c5F77743E4888E75D6577C2F56bAbb',
    'TOKEN_SYMBOL': 'FMC',
    'TOKEN_NAME': 'FlashMorCoin'
}

# HTML COMPLETO EMBEBIDO
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlashMorCoin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .card h2 { color: #333; margin-bottom: 15px; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        .status-item { display: flex; justify-content: space-between; margin-bottom: 10px; padding: 8px 0; border-bottom: 1px solid #eee; }
        .btn { background: #667eea; color: white; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; width: 100%; margin: 5px 0; }
        .btn:hover { background: #5a6fd8; }
        input { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; margin: 10px 0; }
        .result { margin-top: 15px; padding: 15px; border-radius: 8px; background: #f8f9fa; }
        .success { background: #e6ffe6; border-left: 4px solid #28a745; }
        .error { background: #ffe6e6; border-left: 4px solid #dc3545; }
        .loading { color: #667eea; text-align: center; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 FlashMorCoin</h1>
            <p>Dashboard Automático - Polygon Network</p>
        </div>

        <div class="dashboard">
            <div class="card">
                <h2>🌐 Estado del Sistema</h2>
                <div id="systemStatus">
                    <div class="loading">Inicializando sistema...</div>
                </div>
                <button class="btn" onclick="checkSystemStatus()">🔄 Verificar Estado</button>
            </div>

            <div class="card">
                <h2>🪙 Información del Token</h2>
                <div id="tokenInfo">
                    <div class="loading">Esperando datos...</div>
                </div>
                <button class="btn" onclick="getTokenInfo()">📊 Obtener Info</button>
            </div>

            <div class="card">
                <h2>💰 Consultar Balance</h2>
                <input type="text" id="walletAddress" placeholder="0x..." value="0xfb146E2601c5F77743E4888E75D6577C2F56bAbb">
                <button class="btn" onclick="getBalance()">Consultar Balance FMC</button>
                <div id="balanceResult"></div>
            </div>

            <div class="card">
                <h2>🔗 Conexión Blockchain</h2>
                <div id="blockchainStatus">
                    <div class="loading">Verificando conexión...</div>
                </div>
                <button class="btn" onclick="testBlockchain()">🔍 Test Blockchain</button>
            </div>
        </div>
    </div>

    <script>
        // Función para verificar el estado del sistema
        async function checkSystemStatus() {
            const statusElement = document.getElementById('systemStatus');
            statusElement.innerHTML = '<div class="loading">Verificando servidor...</div>';
            
            try {
                const response = await fetch('/api/system/status');
                const data = await response.json();
                
                statusElement.innerHTML = `
                    <div class="status-item">
                        <span>Servidor:</span>
                        <span style="color: green;">✅ ACTIVO</span>
                    </div>
                    <div class="status-item">
                        <span>Timestamp:</span>
                        <span>${new Date(data.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div class="status-item">
                        <span>Contrato:</span>
                        <span>${data.contract_address}</span>
                    </div>
                `;
            } catch (error) {
                statusElement.innerHTML = '<div class="error">❌ Error conectando al servidor</div>';
            }
        }

        // Función para obtener información del token
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
                        <div class="status-item">
                            <span>Nombre:</span>
                            <span>${data.name || 'N/A'}</span>
                        </div>
                        <div class="status-item">
                            <span>Símbolo:</span>
                            <span>${data.symbol || 'N/A'}</span>
                        </div>
                        <div class="status-item">
                            <span>Decimales:</span>
                            <span>${data.decimals || 'N/A'}</span>
                        </div>
                        <div class="status-item">
                            <span>Supply:</span>
                            <span>${data.formatted_supply ? data.formatted_supply.toLocaleString() : 'N/A'}</span>
                        </div>
                    `;
                }
            } catch (error) {
                tokenElement.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
        }

        // Función para consultar balance
        async function getBalance() {
            const walletAddress = document.getElementById('walletAddress').value;
            const resultElement = document.getElementById('balanceResult');
            
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
                            <strong>Balance:</strong> ${data.balance} ${data.symbol}<br>
                            <strong>Wallet:</strong> ${data.address}
                        </div>
                    `;
                }
            } catch (error) {
                resultElement.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
        }

        // Función para testear blockchain
        async function testBlockchain() {
            const statusElement = document.getElementById('blockchainStatus');
            statusElement.innerHTML = '<div class="loading">Testeando conexiones...</div>';
            
            try {
                const response = await fetch('/api/blockchain/test');
                const data = await response.json();
                
                if (data.connected) {
                    statusElement.innerHTML = `
                        <div class="status-item">
                            <span>Blockchain:</span>
                            <span style="color: green;">✅ CONECTADO</span>
                        </div>
                        <div class="status-item">
                            <span>Block:</span>
                            <span>${data.block_number}</span>
                        </div>
                        <div class="status-item">
                            <span>Chain ID:</span>
                            <span>${data.chain_id}</span>
                        </div>
                    `;
                } else {
                    statusElement.innerHTML = '<div class="error">❌ Blockchain no disponible</div>';
                }
            } catch (error) {
                statusElement.innerHTML = '<div class="error">❌ Error de conexión</div>';
            }
        }

        // Inicializar al cargar la página
        document.addEventListener('DOMContentLoaded', function() {
            checkSystemStatus();
            testBlockchain();
        });
    </script>
</body>
</html>
'''

# Conexión Web3
def get_web3():
    """Conectar a Polygon con múltiples fallbacks"""
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
                print(f"✅ Conectado via: {rpc[:50]}...")
                return web3
        except Exception as e:
            print(f"❌ Falló {rpc[:50]}: {e}")
            continue
    
    print("❌ Todas las conexiones fallaron")
    return None

web3 = get_web3()

# Routes
@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/system/status')
def system_status():
    """Estado del sistema"""
    return jsonify({
        'status': 'active',
        'timestamp': 1000,  # Esto se arreglará después
        'contract_address': CONFIG['TOKEN_CONTRACT'],
        'version': '1.0.0'
    })

@app.route('/api/token/info')
def token_info():
    """Información del token"""
    try:
        if not web3 or not web3.is_connected():
            return jsonify({'error': 'Blockchain no conectada'})
        
        # ABI básica ERC-20
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "name",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
        
        contract = web3.eth.contract(
            address=Web3.to_checksum_address(CONFIG['TOKEN_CONTRACT']),
            abi=abi
        )
        
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
    """Obtener balance de una wallet"""
    try:
        if not web3 or not web3.is_connected():
            return jsonify({'error': 'Blockchain no conectada'})
        
        # ABI mínima para balance
        abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function"
            }
        ]
        
        contract = web3.eth.contract(
            address=Web3.to_checksum_address(CONFIG['TOKEN_CONTRACT']),
            abi=abi
        )
        
        balance = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        decimals = contract.functions.decimals().call()
        
        return jsonify({
            'balance': balance / (10 ** decimals),
            'address': address,
            'symbol': CONFIG['TOKEN_SYMBOL']
        })
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

@app.route('/api/blockchain/test')
def blockchain_test():
    """Test de conexión blockchain"""
    try:
        if web3 and web3.is_connected():
            return jsonify({
                'connected': True,
                'block_number': web3.eth.block_number,
                'chain_id': web3.eth.chain_id,
                'network': 'Polygon Mainnet'
            })
        else:
            return jsonify({'connected': False})
    except Exception as e:
        return jsonify({'connected': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Iniciando FlashMorCoin Server...")
    print(f"📍 Contrato: {CONFIG['TOKEN_CONTRACT']}")
    print(f"🌐 Servidor: http://localhost:5000")
    
    # Verificar conexión
    if web3 and web3.is_connected():
        print("✅ Blockchain: CONECTADO")
        print(f"📡 Block: {web3.eth.block_number}")
        print(f"🔗 Chain ID: {web3.eth.chain_id}")
    else:
        print("❌ Blockchain: DESCONECTADO (Modo offline)")
    
    app.run(host='0.0.0.0', port=5000, debug=True)