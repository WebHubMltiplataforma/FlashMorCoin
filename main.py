#!/usr/bin/env python3
"""
FLASHMORCOIN - SISTEMA PRINCIPAL
"""

from web_dashboard.app import app
from wallet.token_manager import token_manager
from config.settings import Config

def main():
    print("🚀 Iniciando FlashMorCoin...")
    print(f"📍 Contrato: {Config.TOKEN_CONTRACT_ADDRESS}")
    print(f"🌐 Dashboard: http://{Config.API_HOST}:{Config.API_PORT}")
    
    # Verificar conexión
    if token_manager.web3 and token_manager.web3.is_connected():
        print("✅ Conexión blockchain: ACTIVA")
        network_info = token_manager.get_network_info()
        print(f"📡 Chain ID: {network_info.get('chain_id', 'N/A')}")
        print(f"🔢 Block: {network_info.get('block_number', 'N/A')}")
    else:
        print("❌ Conexión blockchain: FALLIDA - Usando modo offline")
    
    # Iniciar servidor web
    app.run(
        host=Config.API_HOST,
        port=Config.API_PORT,
        debug=Config.DEBUG
    )

if __name__ == "__main__":
    main()