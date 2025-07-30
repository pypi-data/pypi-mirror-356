"""
DEX swap execution operations using local HTTP endpoints.
Supports both same-chain and cross-chain swaps with operation type control.
"""

import httpx
import webbrowser
import platform
import subprocess
import shutil
from typing import Dict, Any
from ..utils.blockchain import get_explorer_url
from ..utils.formatters import convert_decimal_to_minimal_units
from ..utils.constants import NATIVE_TOKENS, CHAIN_NAMES
from ..api.mesh_api import call_mesh_api
import os

async def validate_token_addresses(from_token: str, to_token: str, from_chain: str, to_chain: str = None) -> list:
    """
    Validate token addresses by checking native tokens in constants.py and ERC tokens using DexScreenerTokenInfoAgent.
    
    Args:
        from_token: From token contract address
        to_token: To token contract address
        from_chain: Source chain ID
        to_chain: Destination chain ID (optional for same-chain)
    
    Returns:
        list: List of warning messages for unrecognizable tokens
    """
    warnings = []
    
    async def validate_single_token(token_address: str, chain_id: str, token_type: str) -> bool:
        """
        Validate a single token address.
        
        Args:
            token_address: Token contract address
            chain_id: Chain ID
            token_type: "from" or "to" for error messages
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        # First check if it's a native token
        if chain_id in NATIVE_TOKENS and token_address.lower() == NATIVE_TOKENS[chain_id].lower():
            return True
        
        # For non-native tokens, use DexScreenerTokenInfoAgent
        try:
            # Get the API key from environment
            heurist_api_key = os.getenv("HEURIST_API_KEY")
            
            # Prepare request for DexScreenerTokenInfoAgent
            request_data = {
                "agent_id": "DexScreenerTokenInfoAgent",
                "input": {
                    "tool": "search_pairs",
                    "tool_arguments": {
                        "search_term": token_address
                    }
                }
            }
            
            if heurist_api_key:
                request_data["api_key"] = heurist_api_key
            
            # Call the DexScreener API
            result = await call_mesh_api("mesh_request", method="POST", json=request_data)
            
            # Check if the search found any pairs for this token
            if result and not result.get("error"):
                # Navigate the nested response structure: result['data']['data']['pairs']
                data_outer = result.get("data", {})
                if data_outer and data_outer.get("status") == "success":
                    data_inner = data_outer.get("data", {})
                    pairs = data_inner.get("pairs", [])
                    
                    if pairs and len(pairs) > 0:
                        # Additional validation: check if any pair contains our token address
                        for pair in pairs:
                            base_token = pair.get("baseToken", {})
                            quote_token = pair.get("quoteToken", {})
                            
                            if (base_token.get("address", "").lower() == token_address.lower() or
                                quote_token.get("address", "").lower() == token_address.lower()):
                                return True
            
            return False
            
        except Exception as e:
            # If validation fails due to error, we'll add a warning but not block the operation
            warnings.append(f"⚠️  Could not validate {token_type} token '{token_address}': {str(e)}")
            return False
    
    # Validate from_token
    from_token_valid = await validate_single_token(from_token, from_chain, "from")
    if not from_token_valid:
        chain_name = CHAIN_NAMES.get(from_chain, f"chain {from_chain}")
        warnings.append(f"⚠️  From token '{from_token}' on {chain_name} is not recognized or found in DexScreener")
    
    # Validate to_token
    target_chain = to_chain or from_chain
    to_token_valid = await validate_single_token(to_token, target_chain, "to")
    if not to_token_valid:
        chain_name = CHAIN_NAMES.get(target_chain, f"chain {target_chain}")
        warnings.append(f"⚠️  To token '{to_token}' on {chain_name} is not recognized or found in DexScreener")
    
    return warnings


def open_in_chrome(url):
    """
    Open URL specifically in Chrome browser with fallback options
    """
    system = platform.system().lower()
    
    # Chrome executable names for different platforms
    chrome_paths = {
        'darwin': [  # macOS
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '/Applications/Chromium.app/Contents/MacOS/Chromium'
        ],
        'linux': [
            'google-chrome',
            'google-chrome-stable',
            'chromium-browser',
            'chromium'
        ],
        'windows': [
            'chrome.exe',
            'chrome',
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        ]
    }
    
    # Try Chrome first
    paths_to_try = chrome_paths.get(system, [])
    
    for path in paths_to_try:
        try:
            if system == 'darwin':
                subprocess.Popen([path, url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                return True
            elif system == 'linux':
                if shutil.which(path):
                    subprocess.Popen([path, url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    return True
            elif system == 'windows':
                try:
                    subprocess.Popen([path, url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                    return True
                except FileNotFoundError:
                    continue
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    
    # Fallback to default browser
    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Failed to open browser: {e}")
        return False


async def execute_swap_internal(
    from_token: str, 
    to_token: str, 
    decimal_amount: str, 
    from_chain: str,
    to_chain: str = None,
    is_cross_chain: bool = False,
    slippage: str = "0.5", 
    to_wallet_address: str = None, 
    from_token_decimals: int = None, 
    slippage_mode: str = "percentage",
    amount: str = None
) -> str:
    """Execute a DEX token swap supporting both same-chain and cross-chain operations.
    
    Args:
        from_token: From token contract address
        to_token: To token contract address
        decimal_amount: Decimal amount to swap (e.g., "0.1" for 0.1 tokens)
        from_chain: Source chain ID (e.g., "1" for Ethereum, "56" for BSC, "501" for Solana)
        to_chain: Destination chain ID (required for cross-chain, ignored for same-chain)
        is_cross_chain: Whether this is a cross-chain swap (default: False)
        slippage: Slippage tolerance (e.g., "0.5" for 0.5%)
        to_wallet_address: Destination wallet address (optional)
        from_token_decimals: Required - decimals of the from_token
        slippage_mode: Mode for slippage handling ("percentage" or "decimal", default: "percentage")
        amount: Amount in minimal units (used for cross-chain if decimal_amount is None)
    
    Returns:
        str: Success message with wallet URL or error message
    """
    
    # Validate parameters based on operation type
    if is_cross_chain:
        if not to_chain:
            return "❌ to_chain is required for cross-chain swaps."
        if from_chain == to_chain:
            return "❌ Cross-chain swap requires different source and destination chains."
    else:
        # For same-chain swaps, set to_chain to from_chain
        to_chain = from_chain
    
    # Handle amount conversion
    if decimal_amount:
        if from_token_decimals is None:
            return "❌ from_token_decimals is required when using decimal_amount parameter."
        try:
            amount = convert_decimal_to_minimal_units(decimal_amount, from_token_decimals)
        except ValueError as e:
            return f"❌ Error converting decimal amount: {str(e)}"
    elif not amount:
        return "❌ Either decimal_amount or amount parameter is required."
    
    # Convert slippage based on mode
    try:
        slippage_float = float(slippage)
        if slippage_mode.lower() == "percentage":
            slippage_decimal = slippage_float / 100
        elif slippage_mode.lower() == "decimal":
            slippage_decimal = slippage_float
        else:
            return f"❌ Invalid slippage_mode: {slippage_mode}. Must be either 'percentage' or 'decimal'"
    except ValueError:
        return f"❌ Invalid slippage format: {slippage}. Please provide a numeric value."
    
    # Validate token addresses and collect warnings
    token_warnings = []
    try:
        token_warnings = await validate_token_addresses(from_token, to_token, from_chain, to_chain)
    except Exception as e:
        # If validation fails, add a generic warning but continue with swap
        token_warnings.append(f"⚠️  Token validation failed: {str(e)}")
    
    # Determine endpoint and payload based on operation type
    if is_cross_chain:
        endpoint = "https://mcp-server-264441234562.us-central1.run.app/evm/crossChainSwap"
        payload = {
            "fromTokenAddress": from_token,
            "toTokenAddress": to_token,
            "amount": amount,
            "fromChainIndex": from_chain,
            "slippage": str(slippage_decimal),
            "toChainIndex": to_chain
        }
    else:
        # Same-chain logic
        if from_chain == "501":  # Solana
            endpoint = "https://mcp-server-264441234562.us-central1.run.app/sol/swap"
            payload = { 
                "fromTokenAddress": from_token,
                "toTokenAddress": to_token,
                "amount": amount,
                "chainIndex": from_chain,
                "slippage": str(slippage_decimal)
            }
        elif from_chain == "101":  # Sui
            endpoint = "https://mcp-server-264441234562.us-central1.run.app/sui/suiSwap"
            payload = {
                "fromTokenAddress": from_token,
                "toTokenAddress": to_token,
                "amount": amount,
                "slippage": str(slippage_decimal)
            }
        else:  # EVM chains
            endpoint = "https://mcp-server-264441234562.us-central1.run.app/evm/swap"
            payload = {
                "fromTokenAddress": from_token,
                "toTokenAddress": to_token,
                "amount": amount,
                "chainIndex": from_chain,
                "slippage": str(slippage_decimal)
            }
    
    # Add destination address if provided
    if to_wallet_address:
        payload["toAddress"] = to_wallet_address

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("code") == 200:
                    data = result.get("data", {})
                    
                    # Extract URL based on operation type and chain
                    wallet_url = None
                    if is_cross_chain:
                        # Cross-chain uses "url" field
                        if "url" in data:
                            wallet_url = data["url"]
                        else:
                            return f"❌ Error: Could not find URL in cross-chain response"
                    else:
                        # Same-chain logic
                        if from_chain == "501":  # Solana - uses "url" field
                            if "url" in data:
                                wallet_url = data["url"]
                            else:
                                return f"❌ Error: Could not find URL in Solana response"
                        elif from_chain == "101":  # Sui - uses "url" field
                            if "url" in data:
                                wallet_url = data["url"]
                            else:
                                return f"❌ Error: Could not find URL in Sui response"
                        else:  # EVM - uses "walletUrl" field
                            if "walletUrl" in data:
                                wallet_url = data["walletUrl"]
                            else:
                                return f"❌ Error: Could not find walletUrl in EVM response"
                    
                    # Automatically open the URL in browser
                    print(f"\nOpening wallet URL: {wallet_url}")
                    success = open_in_chrome(wallet_url)
                    # Determine operation and chain type for display
                    if is_cross_chain:
                        operation_type = "CROSS-CHAIN"
                        chain_info = f"From Chain {from_chain} to Chain {to_chain}"
                    else:
                        if from_chain == "501":
                            operation_type = "SOLANA"
                            chain_info = f"Chain {from_chain}"
                        elif from_chain == "101":
                            operation_type = "SUI"
                            chain_info = f"Chain {from_chain}"
                        else:
                            operation_type = "EVM"
                            chain_info = f"Chain {from_chain}"
                    
                    browser_status = "Browser opened successfully!" if success else "Failed to open browser"
                    
                    # Format warnings section if there are any
                    warnings_section = ""
                    if token_warnings:
                        warnings_section = "\n=== TOKEN VALIDATION WARNINGS ===\n" + "\n".join(token_warnings) + "\n"
                    
                    success_message = f"""
✅ {operation_type} SWAP URL GENERATED SUCCESSFULLY!
{warnings_section}
=== SWAP DETAILS ===
Operation Type: {operation_type}
Chain Info: {chain_info}
Wallet URL: {wallet_url}
Message: {data.get("message", "Please complete the swap in your browser")}
Browser Status: {browser_status}

🎉 The swap URL has been opened in your browser!
"""
                    
                    if is_cross_chain:
                        success_message += "⏳ Cross-chain transactions may take several minutes to complete after confirmation."
                    
                    return success_message
                else:
                    operation_desc = "cross-chain swap" if is_cross_chain else "swap"
                    error_message = f"❌ {operation_desc.capitalize()} failed: {result.get('msg', 'Unknown error')}"
                    
                    # Add warnings to error message if any exist
                    if token_warnings:
                        warnings_text = "\n\n⚠️  TOKEN VALIDATION WARNINGS:\n" + "\n".join(token_warnings)
                        error_message += warnings_text
                    
                    return error_message
            else:
                error_message = f"❌ HTTP Error {response.status_code}: {response.text}"
                if token_warnings:
                    warnings_text = "\n\n⚠️  TOKEN VALIDATION WARNINGS:\n" + "\n".join(token_warnings)
                    error_message += warnings_text
                return error_message
                
    except httpx.TimeoutException:
        timeout_msg = "Cross-chain swaps can take longer." if is_cross_chain else "The swap service may be busy."
        error_message = f"❌ Request timeout. {timeout_msg} Please try again."
        if token_warnings:
            warnings_text = "\n\n⚠️  TOKEN VALIDATION WARNINGS:\n" + "\n".join(token_warnings)
            error_message += warnings_text
        return error_message
    except httpx.ConnectError:
        error_message = "❌ Cannot connect to swap service. Please check the endpoint availability."
        if token_warnings:
            warnings_text = "\n\n⚠️  TOKEN VALIDATION WARNINGS:\n" + "\n".join(token_warnings)
            error_message += warnings_text
        return error_message
    except Exception as e:
        operation_desc = "cross-chain swap" if is_cross_chain else "swap"
        error_message = f"❌ Error executing {operation_desc}: {str(e)}"
        if token_warnings:
            warnings_text = "\n\n⚠️  TOKEN VALIDATION WARNINGS:\n" + "\n".join(token_warnings)
            error_message += warnings_text
        return error_message


def register_swap_tools(mcp):
    """Register swap related MCP tools."""
    
    @mcp.tool()
    async def execute_swap(
        from_token: str, 
        to_token: str, 
        from_chain: str,
        to_chain: str = None,
        decimal_amount: str = None,
        amount: str = None,
        is_cross_chain: bool = False,
        slippage: str = "0.5",
        to_wallet_address: str = None, 
        from_token_decimals: int = None, 
        slippage_mode: str = "percentage"
    ) -> str:
        """Execute a unified DEX token swap supporting both same-chain and cross-chain operations.
        
        This unified function can handle both same-chain and cross-chain swaps based on the is_cross_chain parameter.
        For same-chain swaps, only from_chain is needed. For cross-chain swaps, both from_chain and to_chain are required.

        Args:
            from_token: From token contract address
            to_token: To token contract address
            from_chain: Source chain ID (e.g., "1" for Ethereum, "56" for BSC, "501" for Solana)
            to_chain: Destination chain ID (required only for cross-chain swaps)
            decimal_amount: Decimal amount to swap (e.g., "0.1" for 0.1 tokens)
            amount: Amount in minimal units (alternative to decimal_amount)
            is_cross_chain: Whether this is a cross-chain swap (default: False)
            slippage: Slippage tolerance (e.g., "0.5" for 0.5%)
            to_wallet_address: Destination wallet address (optional)
            from_token_decimals: Required when using decimal_amount - decimals of the from_token
            slippage_mode: Mode for slippage handling ("percentage" or "decimal", default: "percentage")
        """
        # Validate required parameters
        if not decimal_amount and not amount:
            return "❌ Either decimal_amount or amount parameter is required."
        
        if decimal_amount and from_token_decimals is None:
            return "❌ from_token_decimals is required when using decimal_amount parameter."
        
        return await execute_swap_internal(
            from_token=from_token, 
            to_token=to_token, 
            decimal_amount=decimal_amount, 
            from_chain=from_chain,
            to_chain=to_chain,
            is_cross_chain=is_cross_chain,
            slippage=slippage, 
            to_wallet_address=to_wallet_address, 
            from_token_decimals=from_token_decimals, 
            slippage_mode=slippage_mode,
            amount=amount
        )