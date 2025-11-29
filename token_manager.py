from web3 import Web3
import json
import requests
from config.settings import Config

class FlashMorTokenManager:
    def __init__(self):
        self.web3 = None
        self.token_contract = None
        self.connected_network = None
        self.setup_provider_with_fallback()
        
    def setup_provider_with_fallback(self):
        """Sistema de conexión con múltiples fallbacks"""
        print("🌐 Conectando a Polygon Mainnet...")
        
        for i, rpc_url in enumerate(Config.POLYGON_RPCS):
            try:
                print(f"🔄 Intentando RPC {i+1}: {rpc_url[:50]}...")
                self.web3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 30}))
                
                if self.web3.is_connected():
                    chain_id = self.web3.eth.chain_id
                    block = self.web3.eth.block_number
                    
                    print(f"✅ Conectado via RPC {i+1}")
                    print(f"📡 Chain ID: {chain_id}")
                    print(f"🔢 Block: {block}")
                    print(f"🌐 Network: {'Polygon Mainnet' if chain_id == 137 else 'Otra red'}")
                    
                    self.connected_network = rpc_url
                    self.load_token_contract()
                    return True
                    
            except Exception as e:
                print(f"❌ RPC {i+1} falló: {str(e)[:100]}...")
                continue
        
        print("❌ Todas las conexiones RPC fallaron")
        return False

    def load_token_contract(self):
        """Carga el contrato con ABI mejorada"""
        try:
            # ABI ERC-20 completa
            erc20_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "constant": False,
                    "inputs": [
                        {"name": "_to", "type": "address"},
                        {"name": "_value", "type": "uint256"}
                    ],
                    "name": "transfer",
                    "outputs": [{"name": "", "type": "bool"}],
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
            
            self.token_contract = self.web3.eth.contract(
                address=Web3.to_checksum_address(Config.TOKEN_CONTRACT_ADDRESS),
                abi=erc20_abi
            )
            print("✅ Contrato cargado exitosamente")
            return True
            
        except Exception as e:
            print(f"❌ Error cargando contrato: {e}")
            return False

    def get_token_info(self):
        """Obtiene información del token con manejo de errores"""
        try:
            if not self.web3 or not self.web3.is_connected():
                return {"error": "No conectado a blockchain"}
                
            if not self.token_contract:
                return {"error": "Contrato no cargado"}
            
            name = self.token_contract.functions.name().call()
            symbol = self.token_contract.functions.symbol().call()
            decimals = self.token_contract.functions.decimals().call()
            total_supply = self.token_contract.functions.totalSupply().call()
            
            return {
                'name': name,
                'symbol': symbol,
                'decimals': decimals,
                'total_supply': total_supply,
                'contract_address': Config.TOKEN_CONTRACT_ADDRESS,
                'formatted_supply': total_supply / (10 ** decimals),
                'network': 'Polygon Mainnet',
                'connected_rpc': self.connected_network[:50] + '...' if self.connected_network else 'None'
            }
        except Exception as e:
            return {'error': f"Error obteniendo info: {str(e)}"}

    def get_balance(self, wallet_address):
        """Obtiene balance con manejo de errores"""
        try:
            if not self.web3 or not self.web3.is_connected():
                return 0
                
            balance = self.token_contract.functions.balanceOf(
                Web3.to_checksum_address(wallet_address)
            ).call()
            decimals = self.token_contract.functions.decimals().call()
            return balance / (10 ** decimals)
        except Exception as e:
            print(f"Error obteniendo balance: {e}")
            return 0

    def get_network_info(self):
        """Información de la red conectada"""
        if not self.web3 or not self.web3.is_connected():
            return {"connected": False}
            
        try:
            return {
                "connected": True,
                "chain_id": self.web3.eth.chain_id,
                "block_number": self.web3.eth.block_number,
                "gas_price": self.web3.from_wei(self.web3.eth.gas_price, 'gwei'),
                "rpc": self.connected_network
            }
        except Exception as e:
            return {"connected": False, "error": str(e)}

# Instancia global
token_manager = FlashMorTokenManager()