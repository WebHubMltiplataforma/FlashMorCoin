import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ✅ TOKEN FLASHMORCOIN
    TOKEN_NAME = "FlashMorCoin"
    TOKEN_SYMBOL = "FMC"
    TOKEN_DECIMALS = 18
    TOKEN_CONTRACT_ADDRESS = "0xfb146E2601c5F77743E4888E75D6577C2F56bAbb"
    
    # ✅ WALLETS
    TOKEN_OWNER_ADDRESS = os.getenv('TOKEN_OWNER_ADDRESS', '0xfb146E2601c5F77743E4888E75D6577C2F56bAbb')
    TOKEN_PRIVATE_KEY = os.getenv('TOKEN_PRIVATE_KEY', '4df8eead51294cd09eadf4b51efaa014')
    
    # ✅ CONEXIONES CON FALLBACK
    INFURA_KEY = "4df8eead51294cd09eadf4b51efaa014"
    QUICKNODE_URL = "https://purple-bold-sunset.matic.quiknode.pro/6e2958c9720ad8d75f46b01d483e002df46d4524"
    
    # ✅ MÚLTIPLES RPCs PARA POLYGON
    POLYGON_RPCS = [
        QUICKNODE_URL,  # Tu QuickNode
        f"https://polygon-mainnet.infura.io/v3/{INFURA_KEY}",  # Infura
        "https://polygon-rpc.com",  # Público 1
        "https://rpc-mainnet.matic.network",  # Público 2
        "https://rpc.ankr.com/polygon",  # Público 3
        "https://polygon-rpc.com",  # Público 4
    ]
    
    # ✅ CONFIGURACIÓN WEB
    API_HOST = "0.0.0.0"
    API_PORT = 5000
    DEBUG = True
    
    # ✅ DEX
    QUICKSWAP_ROUTER = "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"