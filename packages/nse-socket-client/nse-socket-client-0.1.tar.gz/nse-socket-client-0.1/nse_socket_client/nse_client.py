#!/usr/bin/env python3
"""
NSE Socket Client Library
A professional Python client library for the NSE Socket server with WebSocket and REST API support.
"""

import json
import time
import threading
import requests
import websocket
from typing import Optional, Dict, Any, Callable, List, Set, Union
from datetime import datetime, date
import logging
import signal
import sys

# Configure professional logging format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_token(api_uri: str, username: str) -> Optional[str]:
    """
    Standalone function to request JWT token from the NSE server.
    
    Args:
        api_uri: HTTP API server URI (e.g., "http://localhost:3000")
        username: Username for token generation
        
    Returns:
        str: JWT token string if successful, None if failed
        
    Raises:
        AuthenticationError: If token retrieval fails
        
    Example:
        token = get_token("http://localhost:3000", "admin")
        if token:
            print(f"Token: {token}")
    """
    try:
        logger.info(f"Requesting JWT token for user: {username}")
        
        response = requests.post(
            f"{api_uri}/api/login",
            json={"username": username},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token"):
                token = data["token"]
                user_id = data.get("user_id", username)
                permissions = data.get("permissions", [])
                
                logger.info(f"JWT token obtained successfully for user: {user_id}")
                logger.info(f"Granted permissions: {', '.join(permissions)}")
                
                return token
            else:
                error_msg = data.get("message", "Token generation failed")
                raise AuthenticationError(f"Token generation failed: {error_msg}")
        else:
            raise AuthenticationError(f"Token request failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise AuthenticationError(f"Token request failed: {str(e)}")
    except Exception as e:
        raise AuthenticationError(f"Token generation error: {str(e)}")


class NSESocketError(Exception):
    """Base exception for NSE Socket client errors."""
    pass


class AuthenticationError(NSESocketError):
    """Exception raised for authentication-related errors."""
    pass


class ConnectionError(NSESocketError):
    """Exception raised for connection-related errors."""
    pass


class SubscriptionError(NSESocketError):
    """Exception raised for subscription-related errors."""
    pass


class HistoricalDataError(NSESocketError):
    """Exception raised for historical data API errors."""
    pass


class AdminError(NSESocketError):
    """Exception raised for admin operation errors."""
    pass


class NSEClient:
    """
    Professional NSE Socket Client for real-time market data streaming and order management.
    
    This client provides a robust interface for connecting to the NSE Socket server,
    subscribing to real-time market data feeds, managing trading orders, and accessing
    historical market data with advanced filtering and date scaling capabilities.
    
    Example Usage:
        # Method 1: Request token and connect
        client = NSEClient("ws://localhost:8080", "http://localhost:3000")
        if client.authenticate("username"):
            # Real-time data
            client.connect_and_subscribe(["NIFTY", "RELIANCE", "TCS"])
            
            # Historical data
            historical_data = client.get_historical_data("NIFTY", limit=100)
            daily_data = client.get_historical_data("NIFTY", time_period="day", limit=30)
            
            client.run()
        
        # Method 2: Use existing token
        client = NSEClient("localhost", "jwt-token")
        client.on_ticks = lambda data: print(f"Received: {data}")
        client.connect_and_subscribe(["NIFTY", "RELIANCE"])
        client.run()
    """
    
    def __init__(self, ws_uri: str, api_uri: str, token: Optional[str] = None):
        """
        Initialize NSE Socket Client.
        
        Args:
            ws_uri: WebSocket server URI (e.g., "ws://localhost:8080")
            api_uri: HTTP API server URI (e.g., "http://localhost:3000")  
            token: JWT authentication token (optional, can be obtained via authenticate())
        
        Raises:
            ValueError: If URIs are invalid
        """
        # Validate and normalize URIs
        if not ws_uri or not api_uri:
            raise ValueError("WebSocket and API URIs must be provided")
            
        self.ws_uri = ws_uri
        self.api_uri = api_uri
        self.token = token
        
        # Connection state
        self.ws = None
        self.connected = False
        self.running = False
        self.ws_thread = None
        self._stop_event = threading.Event()
        
        # Subscription management
        self.subscribed_symbols: Set[str] = set()
        
        # API configuration
        self.headers = self._get_headers()
        
        # Event callbacks
        self.on_ticks: Optional[Callable[[Dict], None]] = None
        self.on_connect: Optional[Callable[[], None]] = None
        self.on_disconnect: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        self.on_order_update: Optional[Callable[[Dict], None]] = None
        
        # Connection settings
        self.auto_reconnect = True
        self.reconnect_interval = 5
        self.max_reconnect_attempts = 10
        self.reconnect_attempts = 0
        
        # Heartbeat configuration
        self.heartbeat_enabled = True
        self.heartbeat_interval = 25
        self.ping_timeout = 10
        self.last_pong_time = None
        
        # Setup graceful shutdown
        self._setup_signal_handlers()

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def _setup_signal_handlers(self):
        """Configure signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info("⚠️ Shutdown signal received - forcing immediate stop")
            self.force_shutdown()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    def get_token(self, username: str) -> Optional[str]:
        """
        Request JWT token from the server using username.
        Uses the standalone get_token function and updates internal state.
        
        Args:
            username: Username for token generation
            
        Returns:
            str: JWT token string if successful, None if failed
            
        Raises:
            AuthenticationError: If token retrieval fails
        """
        try:
            token = get_token(self.api_uri, username)
            if token:
                self.token = token
                self.headers = self._get_headers()
            return token
        except Exception as e:
            raise e

    def connect_and_subscribe(self, symbols: List[str]) -> bool:
        """
        Connect to WebSocket and subscribe to multiple symbols in one call.
        
        Args:
            symbols: List of symbols to subscribe to
            
        Returns:
            bool: True if connection and all subscriptions successful
        """
        if not self.ws_connect():
            return False
            
        # Wait a moment for connection to stabilize
        time.sleep(0.5)
        
        results = self.subscribe_multiple(symbols)
        success_count = sum(1 for success in results.values() if success)
        
        logger.info(f"📡 Successfully subscribed to {success_count}/{len(symbols)} symbols")
        return success_count > 0

    def run(self, timeout: Optional[float] = None):
        """
        Run the client in blocking mode until stopped or disconnected.
        This eliminates the need for sleep in your main program.
        
        Args:
            timeout: Maximum time to run in seconds (None = run indefinitely)
        """
        if not self.connected:
            logger.error("❌ Not connected. Call ws_connect() or connect_and_subscribe() first")
            return
            
        logger.info("🚀 Starting data stream... Press Ctrl+C to stop")
        
        try:
            if timeout:
                self._stop_event.wait(timeout)
            else:
                # Run until stop event is set
                self._stop_event.wait()
                
        except KeyboardInterrupt:
            logger.info("🛑 Interrupted by user - forcing shutdown")
            self.force_shutdown()
            return
        finally:
            # Only call normal stop if we weren't force-shutdown
            if self.running:
                self.stop()

    def stop(self):
        """Stop the client and disconnect."""
        logger.info("🛑 Stopping NSE Client...")
        
        # Set stop event first to signal all threads
        self._stop_event.set()
        self.running = False
        self.auto_reconnect = False
        
        # Disconnect WebSocket
        self.ws_disconnect()
        
        # Give a moment for everything to cleanup
        time.sleep(0.1)
        
        logger.info("✅ NSE Client stopped")

    def ws_connect(self) -> bool:
        """
        Connect to WebSocket server.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            if self.connected:
                logger.warning("Already connected to WebSocket")
                return True
                
            logger.info(f"Connecting to WebSocket: {self.ws_uri}")
            
            # Reset stop event
            self._stop_event.clear()
            
            # Create WebSocket connection with built-in ping/pong
            self.ws = websocket.WebSocketApp(
                self.ws_uri,
                header=[f"Authorization: Bearer {self.token}"],
                on_open=self._on_ws_open,
                on_message=self._on_ws_message,
                on_error=self._on_ws_error,
                on_close=self._on_ws_close,
                on_ping=self._on_ws_ping,
                on_pong=self._on_ws_pong
            )
            
            # Start WebSocket in separate thread with built-in ping
            self.running = True
            if self.heartbeat_enabled:
                # Use websocket-client's built-in ping functionality with interruptible dispatcher
                self.ws_thread = threading.Thread(target=self._run_websocket_with_ping)
            else:
                # No ping functionality but still interruptible
                self.ws_thread = threading.Thread(target=self._run_websocket_simple)
                
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            # Wait for connection
            timeout = 10
            start_time = time.time()
            while not self.connected and time.time() - start_time < timeout:
                time.sleep(0.1)
                
            if self.connected:
                self.reconnect_attempts = 0
                logger.info("✅ WebSocket connected successfully")
                
                if self.heartbeat_enabled:
                    logger.info(f"💓 Heartbeat enabled (ping every {self.heartbeat_interval}s)")
                
                return True
            else:
                logger.error("❌ WebSocket connection timeout")
                return False
                
        except Exception as e:
            logger.error(f"❌ WebSocket connection failed: {e}")
            return False

    def ws_disconnect(self):
        """Disconnect from WebSocket server."""
        try:
            logger.info("Disconnecting from WebSocket...")
            self.running = False
            self.auto_reconnect = False
            
            # Stop heartbeat
            self._stop_heartbeat()
            
            # Close WebSocket connection first
            if self.ws:
                try:
                    self.ws.close()
                except Exception as e:
                    logger.debug(f"Error closing WebSocket: {e}")
                    
            # Force thread to stop by setting stop event
            self._stop_event.set()
            
            # Wait for thread to finish with shorter timeout
            if self.ws_thread and self.ws_thread.is_alive():
                logger.debug("Waiting for WebSocket thread to stop...")
                self.ws_thread.join(timeout=3)
                
                # If thread is still alive, it's probably stuck
                if self.ws_thread and self.ws_thread.is_alive():
                    logger.warning("WebSocket thread didn't stop cleanly - it may be stuck")
                else:
                    logger.debug("WebSocket thread stopped successfully")
                
            self.connected = False
            self.subscribed_symbols.clear()
            self.ws = None
            self.ws_thread = None
            logger.info("✅ WebSocket disconnected")
            
        except Exception as e:
            logger.error(f"❌ Error disconnecting: {e}")
            # Force cleanup even if there was an error
            self.connected = False
            self.running = False
            self.ws = None
            self.ws_thread = None

    def subscribe_feed(self, symbol: str) -> bool:
        """
        Subscribe to real-time data feed for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., "NIFTY", "INDIGO")
            
        Returns:
            bool: True if subscription successful, False otherwise
        """
        if not self.connected:
            logger.error("❌ Not connected to WebSocket")
            return False
            
        try:
            symbol = symbol.upper()
            message = {
                "action": "subscribe",
                "symbol": symbol
            }
            
            self.ws.send(json.dumps(message))
            self.subscribed_symbols.add(symbol)
            logger.info(f"📡 Subscribed to {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Subscription failed for {symbol}: {e}")
            return False

    def subscribe_multiple(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Subscribe to real-time data feeds for multiple symbols.
        
        Args:
            symbols: List of stock symbols (e.g., ["NIFTY", "INDIGO", "RELIANCE"])
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to subscription success status
        """
        if not self.connected:
            logger.error("❌ Not connected to WebSocket")
            return {symbol: False for symbol in symbols}
            
        results = {}
        successful_subscriptions = []
        
        for symbol in symbols:
            try:
                symbol = symbol.upper()
                message = {
                    "action": "subscribe",
                    "symbol": symbol
                }
                
                self.ws.send(json.dumps(message))
                self.subscribed_symbols.add(symbol)
                results[symbol] = True
                successful_subscriptions.append(symbol)
                
                # Small delay between subscriptions to avoid overwhelming the server
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Subscription failed for {symbol}: {e}")
                results[symbol] = False
        
        if successful_subscriptions:
            logger.info(f"📡 Subscribed to {len(successful_subscriptions)} symbols: {', '.join(successful_subscriptions)}")
        
        return results

    def subscribe_batch(self, symbols: List[str], batch_size: int = 10) -> Dict[str, bool]:
        """
        Subscribe to multiple symbols in batches to avoid overwhelming the server.
        
        Args:
            symbols: List of symbols to subscribe to
            batch_size: Number of symbols to subscribe to at once
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to subscription success status
        """
        if not self.connected:
            logger.error("❌ Not connected to WebSocket")
            return {symbol: False for symbol in symbols}
            
        all_results = {}
        
        # Process symbols in batches
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            batch_results = self.subscribe_multiple(batch)
            all_results.update(batch_results)
            
            # Pause between batches if not the last batch
            if i + batch_size < len(symbols):
                time.sleep(0.5)
                
        return all_results

    def unsubscribe_feed(self, symbol: Optional[str] = None) -> bool:
        """
        Unsubscribe from data feed.
        
        Args:
            symbol: Symbol to unsubscribe from (optional, unsubscribes from all if not provided)
            
        Returns:
            bool: True if unsubscription successful, False otherwise
        """
        if not self.connected:
            logger.error("❌ Not connected to WebSocket")
            return False
            
        try:
            if symbol:
                # Unsubscribe from specific symbol
                symbol = symbol.upper()
                if symbol not in self.subscribed_symbols:
                    logger.warning(f"⚠️ Not subscribed to {symbol}")
                    return False
                    
                message = {
                    "action": "unsubscribe", 
                    "symbol": symbol
                }
                
                self.ws.send(json.dumps(message))
                self.subscribed_symbols.discard(symbol)
                logger.info(f"📡 Unsubscribed from {symbol}")
                return True
            else:
                # Unsubscribe from all symbols
                if not self.subscribed_symbols:
                    logger.warning("⚠️ No active subscriptions")
                    return False
                
                symbols_to_unsubscribe = list(self.subscribed_symbols)
                success = True
                
                for sym in symbols_to_unsubscribe:
                    try:
                        message = {
                            "action": "unsubscribe", 
                            "symbol": sym
                        }
                        self.ws.send(json.dumps(message))
                        time.sleep(0.1)  # Small delay between unsubscriptions
                    except Exception as e:
                        logger.error(f"❌ Failed to unsubscribe from {sym}: {e}")
                        success = False
                
                self.subscribed_symbols.clear()
                logger.info(f"📡 Unsubscribed from all symbols")
                return success
                
        except Exception as e:
            logger.error(f"❌ Unsubscription failed: {e}")
            return False

    def unsubscribe_multiple(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Unsubscribe from multiple symbols.
        
        Args:
            symbols: List of symbols to unsubscribe from
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to unsubscription success status
        """
        if not self.connected:
            logger.error("❌ Not connected to WebSocket")
            return {symbol: False for symbol in symbols}
            
        results = {}
        successful_unsubscriptions = []
        
        for symbol in symbols:
            try:
                symbol = symbol.upper()
                if symbol not in self.subscribed_symbols:
                    logger.warning(f"⚠️ Not subscribed to {symbol}")
                    results[symbol] = False
                    continue
                    
                message = {
                    "action": "unsubscribe", 
                    "symbol": symbol
                }
                
                self.ws.send(json.dumps(message))
                self.subscribed_symbols.discard(symbol)
                results[symbol] = True
                successful_unsubscriptions.append(symbol)
                
                # Small delay between unsubscriptions
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Unsubscription failed for {symbol}: {e}")
                results[symbol] = False
        
        if successful_unsubscriptions:
            logger.info(f"📡 Unsubscribed from {len(successful_unsubscriptions)} symbols: {', '.join(successful_unsubscriptions)}")
        
        return results

    def place_order(self, symbol: str, side: str, order_type: str, quantity: int, 
                   price: Optional[float] = None, stop_price: Optional[float] = None) -> Optional[Dict]:
        """
        Place a stock order.
        
        Args:
            symbol: Stock symbol
            side: "buy" or "sell"  
            order_type: "market", "limit", or "stop_loss"
            quantity: Number of shares
            price: Price for limit orders (optional)
            stop_price: Stop price for stop-loss orders (optional)
            
        Returns:
            Dict: Order details if successful, None if failed
        """
        try:
            order_data = {
                "symbol": symbol.upper(),
                "side": side.lower(),
                "order_type": order_type.lower(),
                "quantity": quantity
            }
            
            if price is not None:
                order_data["price"] = price
            if stop_price is not None:
                order_data["stop_price"] = stop_price
                
            response = requests.post(
                f"{self.api_uri}/api/orders",
                headers=self.headers,
                json=order_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    order = result.get("order")
                    logger.info(f"✅ Order placed: {order['id']} - {side.upper()} {quantity} {symbol}")
                    
                    # Trigger callback if set
                    if self.on_order_update and order:
                        try:
                            self.on_order_update(order)
                        except Exception as e:
                            logger.error(f"Error in order callback: {e}")
                    
                    return order
                else:
                    logger.error(f"❌ Order failed: {result.get('message')}")
                    return None
            else:
                logger.error(f"❌ Order request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Order placement error: {e}")
            return None

    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id: Order ID to cancel
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.delete(
                f"{self.api_uri}/api/orders/{order_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"✅ Order cancelled: {order_id}")
                    
                    # Trigger callback if set
                    if self.on_order_update:
                        try:
                            self.on_order_update(result.get("order"))
                        except Exception as e:
                            logger.error(f"Error in order callback: {e}")
                    
                    return True
                else:
                    logger.error(f"❌ Cancel failed: {result.get('message')}")
                    return False
            else:
                logger.error(f"❌ Cancel request failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Order cancellation error: {e}")
            return False

    def get_orders(self, symbol: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """
        Get user's orders.
        
        Args:
            symbol: Filter by symbol (optional)
            status: Filter by status (optional)
            
        Returns:
            List[Dict]: List of orders
        """
        try:
            params = {}
            if symbol:
                params['symbol'] = symbol.upper()
            if status:
                params['status'] = status.lower()
                
            response = requests.get(
                f"{self.api_uri}/api/orders",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("orders", [])
                    
            logger.error(f"❌ Failed to get orders: {response.status_code}")
            return []
            
        except Exception as e:
            logger.error(f"❌ Error getting orders: {e}")
            return []

    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Get specific order details.
        
        Args:
            order_id: Order ID
            
        Returns:
            Dict: Order details if found, None otherwise
        """
        try:
            response = requests.get(
                f"{self.api_uri}/api/orders/{order_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    return result.get("order")
                    
            logger.error(f"❌ Failed to get order: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting order: {e}")
            return None

    def health_check(self) -> bool:
        """
        Check API server health.
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.api_uri}/api/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    # Historical Data API Methods
    def get_historical_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get summary of all available symbols and their record counts.
        
        Returns:
            Dict: Summary with symbols, counts, and totals, or None if failed
            
        Raises:
            HistoricalDataError: If request fails or authentication required
        """
        try:
            response = requests.get(
                f"{self.api_uri}/api/historical",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    logger.info(f"📊 Historical data summary: {result.get('total_symbols', 0)} symbols, "
                              f"{result.get('total_records', 0)} total records")
                    return result
                else:
                    raise HistoricalDataError(f"Failed to get historical summary: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Authentication required for historical data access")
            else:
                raise HistoricalDataError(f"Failed to get historical summary: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise HistoricalDataError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (HistoricalDataError, AuthenticationError)):
                raise
            raise HistoricalDataError(f"Unexpected error: {str(e)}")

    
    def get_historical_data(
        self,
        symbol: str,
        limit: Optional[int] = None,
        from_date: Optional[Union[str, date]] = None,
        to_date: Optional[Union[str, date]] = None,
        time_period: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical data with clean format - only essential fields in exact order.
        
        Args:
            symbol: Symbol to get data for (e.g., "NIFTY", "RELIANCE")
            limit: Maximum number of records to return
            from_date: Start date filter (YYYY-MM-DD format or date object)
            to_date: End date filter (YYYY-MM-DD format or date object)
            time_period: Time period filtering - "minutes"/"min"/"m", "hour"/"hours"/"h", "day"/"days"/"d"
        
        Returns:
            List[Dict]: Clean list with only [date, open, high, low, close, volume] fields
        
        Examples:
            # Get last 100 records with clean format
            data = client.get_historical_data_clean("NIFTY", limit=100)
            # Returns: [{"date": "2025-06-21", "open": 21500.0, "high": 21650.0, "low": 21480.0, "close": 21620.0, "volume": 1500000}, ...]
        """
        try:
            # Get the full data first
            result = self.get_historical_data(symbol, limit=limit, from_date=from_date, 
                                            to_date=to_date, time_period=time_period)
            
            if not result or not result.get("success"):
                return []
            
            # Extract and clean the data - keep only essential fields in exact order
            clean_data = []
            for record in result.get("data", []):
                clean_record = {
                    "date": record.get("date"),
                    "open": record.get("open"),
                    "high": record.get("high"), 
                    "low": record.get("low"),
                    "close": record.get("close"),
                    "volume": record.get("volume")
                }
                clean_data.append(clean_record)
            
            logger.info(f"📊 Retrieved {len(clean_data)} clean records for {symbol}")
            return clean_data
            
        except Exception as e:
            logger.error(f"❌ Failed to get clean historical data for {symbol}: {e}")
            return []

    def get_available_symbols(self) -> List[str]:
        """
        Get list of available symbols for historical data.
        
        Returns:
            List: List of available symbols, empty list if failed
        """
        try:
            summary = self.get_historical_summary()
            if summary and summary.get("success"):
                return summary.get("symbols", [])
            return []
        except Exception as e:
            logger.error(f"❌ Failed to get available symbols: {e}")
            return []

    # Admin Broadcast Control Methods (require admin token)
    def start_broadcast(self) -> bool:
        """
        Start real-time data broadcasting (admin only).
        
        Returns:
            bool: True if broadcasting started successfully
            
        Raises:
            AdminError: If operation fails or insufficient permissions
            AuthenticationError: If authentication required
        """
        try:
            response = requests.post(
                f"{self.api_uri}/api/start-broadcast",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message = result.get("message", "Broadcasting started")
                    logger.info(f"📡 {message}")
                    return True
                else:
                    raise AdminError(f"Failed to start broadcast: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to start broadcast: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    def stop_broadcast(self) -> bool:
        """
        Stop data broadcasting (admin only).
        
        Returns:
            bool: True if broadcasting stopped successfully
            
        Raises:
            AdminError: If operation fails or insufficient permissions
        """
        try:
            response = requests.post(
                f"{self.api_uri}/api/stop-broadcast",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message = result.get("message", "Broadcasting stopped")
                    logger.info(f"📡 {message}")
                    return True
                else:
                    raise AdminError(f"Failed to stop broadcast: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to stop broadcast: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    def pause_broadcast(self) -> bool:
        """
        Pause data broadcasting (admin only).
        
        Returns:
            bool: True if broadcasting paused successfully
            
        Raises:
            AdminError: If operation fails or insufficient permissions
        """
        try:
            response = requests.post(
                f"{self.api_uri}/api/pause-broadcast",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message = result.get("message", "Broadcasting paused")
                    logger.info(f"📡 {message}")
                    return True
                else:
                    raise AdminError(f"Failed to pause broadcast: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to pause broadcast: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    def resume_broadcast(self) -> bool:
        """
        Resume paused data broadcasting (admin only).
        
        Returns:
            bool: True if broadcasting resumed successfully
            
        Raises:
            AdminError: If operation fails or insufficient permissions
        """
        try:
            response = requests.post(
                f"{self.api_uri}/api/resume-broadcast",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message = result.get("message", "Broadcasting resumed")
                    logger.info(f"📡 {message}")
                    return True
                else:
                    raise AdminError(f"Failed to resume broadcast: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to resume broadcast: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    def restart_broadcast(self) -> bool:
        """
        Restart data broadcasting from the beginning (admin only).
        
        Returns:
            bool: True if broadcasting restarted successfully
            
        Raises:
            AdminError: If operation fails or insufficient permissions
        """
        try:
            response = requests.post(
                f"{self.api_uri}/api/restart-broadcast",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    message = result.get("message", "Broadcasting restarted")
                    logger.info(f"📡 {message}")
                    return True
                else:
                    raise AdminError(f"Failed to restart broadcast: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to restart broadcast: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    def get_broadcast_status(self) -> Optional[Dict[str, Any]]:
        """
        Get current broadcasting status and statistics (admin only).
        
        Returns:
            Dict: Broadcasting status information, or None if failed
            
        Raises:
            AdminError: If operation fails or insufficient permissions
        """
        try:
            response = requests.get(
                f"{self.api_uri}/api/broadcast-status",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    state = result.get("state", "Unknown")
                    symbol_count = result.get("symbol_count", 0)
                    total_records = result.get("total_records", 0)
                    
                    logger.info(f"📡 Broadcast status: {state} ({symbol_count} symbols, {total_records} records)")
                    return result
                else:
                    raise AdminError(f"Failed to get broadcast status: {result.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise AuthenticationError("Admin authentication required")
            elif response.status_code == 403:
                raise AdminError("Insufficient permissions - admin role required")
            else:
                raise AdminError(f"Failed to get broadcast status: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise AdminError(f"Request failed: {str(e)}")
        except Exception as e:
            if isinstance(e, (AdminError, AuthenticationError)):
                raise
            raise AdminError(f"Unexpected error: {str(e)}")

    # WebSocket event handlers
    def _on_ws_open(self, ws):
        """Handle WebSocket connection open."""
        self.connected = True
        self.last_pong_time = time.time()
        logger.info("🔌 WebSocket connection opened")
        
        if self.on_connect:
            try:
                self.on_connect()
            except Exception as e:
                logger.error(f"Error in connect callback: {e}")

    def _on_ws_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            
            # Handle subscription responses
            if "status" in data:
                status = data.get("status")
                symbol = data.get("symbol")
                msg = data.get("message", "")
                
                if status == "success":
                    logger.info(f"✅ {msg} - Symbol: {symbol}")
                else:
                    logger.error(f"❌ {msg} - Symbol: {symbol}")
            
            # Handle market data
            elif "symbol" in data and "data" in data:
                tick_data = {
                    "symbol": data["symbol"],
                    "data": data["data"],
                    "timestamp": data.get("timestamp", ""),
                    "received_at": datetime.now()
                }
                
                if self.on_ticks:
                    try:
                        self.on_ticks(tick_data)
                    except Exception as e:
                        logger.error(f"Error in ticks callback: {str(e)}")
            
            # Handle batch data
            elif "ticks" in data:
                for tick in data["ticks"]:
                    tick_data = {
                        "symbol": tick["symbol"],
                        "data": tick["data"], 
                        "timestamp": tick.get("timestamp", ""),
                        "received_at": datetime.now()
                    }
                    
                    if self.on_ticks:
                        try:
                            self.on_ticks(tick_data)
                        except Exception as e:
                            logger.error(f"Error in ticks callback: {str(e)}")
            
            else:
                logger.debug(f"Received message: {message}")
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse message: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    def _on_ws_error(self, ws, error):
        """Handle WebSocket errors."""
        logger.error(f"❌ WebSocket error: {error}")
        
        if self.on_error:
            try:
                self.on_error(error)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")

    def _on_ws_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        self.connected = False
        logger.info("🔌 WebSocket connection closed")
        
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except Exception as e:
                logger.error(f"Error in disconnect callback: {e}")
        
        # Auto-reconnect if enabled
        if self.auto_reconnect and self.running:
            self._attempt_reconnect()

    def _on_ws_ping(self, ws, data):
        """Handle incoming ping from server."""
        logger.debug("💓 Received ping from server")
        # Pong response is handled automatically by websocket-client

    def _on_ws_pong(self, ws, data):
        """Handle incoming pong from server."""
        logger.debug("💓 Received pong from server")
        self.last_pong_time = time.time()

    def _start_heartbeat(self):
        """Start the heartbeat thread."""
        # With the new implementation, heartbeat is handled by websocket-client
        # This method is kept for backward compatibility but doesn't start a separate thread
        if self.heartbeat_enabled:
            logger.info(f"💓 Using built-in websocket heartbeat (interval: {self.heartbeat_interval}s)")

    def _stop_heartbeat(self):
        """Stop the heartbeat thread."""
        # With the new implementation, heartbeat is handled by websocket-client
        # This method is kept for backward compatibility
        if self.heartbeat_enabled:
            logger.info("💓 Heartbeat will stop with connection")

    def _heartbeat_worker(self):
        """
        Legacy heartbeat worker - no longer used.
        Heartbeat is now handled by websocket-client's built-in ping functionality.
        """
        # This method is kept for backward compatibility but is no longer used
        pass

    def _attempt_reconnect(self):
        """Attempt to reconnect to WebSocket."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"❌ Max reconnect attempts ({self.max_reconnect_attempts}) reached")
            self._stop_event.set()  # Signal to stop the run loop
            return
            
        self.reconnect_attempts += 1
        logger.info(f"🔄 Attempting to reconnect ({self.reconnect_attempts}/{self.max_reconnect_attempts})")
        
        time.sleep(self.reconnect_interval)
        
        if self.ws_connect():
            # Re-subscribe to current symbols if any
            if self.subscribed_symbols:
                symbols_to_resubscribe = list(self.subscribed_symbols)
                self.subscribed_symbols.clear()  # Clear before re-subscribing
                self.subscribe_multiple(symbols_to_resubscribe)

    def is_connected(self) -> bool:
        """Check if WebSocket is connected."""
        return self.connected

    def get_subscribed_symbols(self) -> Set[str]:
        """Get set of currently subscribed symbols."""
        return self.subscribed_symbols.copy()

    def get_current_symbol(self) -> Optional[str]:
        """Get currently subscribed symbol (for backward compatibility)."""
        # Return the first symbol if any are subscribed, None otherwise
        return next(iter(self.subscribed_symbols)) if self.subscribed_symbols else None

    def is_subscribed(self, symbol: str) -> bool:
        """Check if subscribed to a specific symbol."""
        return symbol.upper() in self.subscribed_symbols

    def get_subscription_count(self) -> int:
        """Get the number of active subscriptions."""
        return len(self.subscribed_symbols)

    def set_log_level(self, level: str):
        """Set logging level."""
        log_levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        if level.upper() in log_levels:
            logger.setLevel(log_levels[level.upper()])

    def add_symbols(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Add new symbols to existing subscriptions.
        
        Args:
            symbols: List of new symbols to add
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to subscription success status
        """
        # Filter out already subscribed symbols
        new_symbols = [s for s in symbols if s.upper() not in self.subscribed_symbols]
        
        if not new_symbols:
            logger.info("ℹ️ All symbols already subscribed")
            return {symbol: True for symbol in symbols}
            
        return self.subscribe_multiple(new_symbols)

    def remove_symbols(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Remove symbols from current subscriptions.
        
        Args:
            symbols: List of symbols to remove
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to unsubscription success status
        """
        return self.unsubscribe_multiple(symbols)

    def replace_symbols(self, symbols: List[str]) -> Dict[str, bool]:
        """
        Replace all current subscriptions with new symbols.
        
        Args:
            symbols: List of symbols to subscribe to (replaces all current)
            
        Returns:
            Dict[str, bool]: Dictionary mapping symbol to subscription success status
        """
        # Unsubscribe from all current symbols
        if self.subscribed_symbols:
            self.unsubscribe_feed()  # Unsubscribe from all
            
        # Subscribe to new symbols
        return self.subscribe_multiple(symbols)

    def get_heartbeat_status(self) -> Dict[str, Any]:
        """
        Get heartbeat status information.
        
        Returns:
            Dict containing heartbeat configuration and status
        """
        return {
            "enabled": self.heartbeat_enabled,
            "interval": self.heartbeat_interval,
            "timeout": self.ping_timeout,
            "last_pong": self.last_pong_time,
            "implementation": "built-in websocket-client ping/pong",
            "connected": self.connected
        }

    def set_heartbeat_config(self, enabled: bool = True, interval: int = 25, timeout: int = 10):
        """
        Configure heartbeat settings.
        
        Args:
            enabled: Whether to enable heartbeat/ping
            interval: Seconds between ping messages (default 25s, server expects within 30s)
            timeout: Seconds to wait for pong response before considering connection dead
        """
        self.heartbeat_enabled = enabled
        self.heartbeat_interval = interval
        self.ping_timeout = timeout
        logger.info(f"💓 Heartbeat configured: enabled={enabled}, interval={interval}s, timeout={timeout}s")

    def _run_websocket_with_ping(self):
        """Run WebSocket with ping/pong in an interruptible way."""
        try:
            # Check if we should stop before even starting
            while self.running and not self._stop_event.is_set():
                try:
                    # Run with a shorter timeout so we can check stop event more often
                    self.ws.run_forever(
                        ping_interval=self.heartbeat_interval,
                        ping_timeout=self.ping_timeout,
                        ping_payload="ping"
                    )
                    break  # If run_forever exits normally, break the loop
                except Exception as e:
                    if self._stop_event.is_set() or not self.running:
                        break  # Exit if stop was requested
                    logger.error(f"WebSocket error, retrying: {e}")
                    if self.auto_reconnect:
                        time.sleep(1)
                    else:
                        break
        except Exception as e:
            if not self._stop_event.is_set():
                logger.error(f"WebSocket thread error: {e}")
        finally:
            logger.debug("WebSocket thread with ping exiting")

    def _run_websocket_simple(self):
        """Run WebSocket without ping in an interruptible way."""
        try:
            # Check if we should stop before even starting
            while self.running and not self._stop_event.is_set():
                try:
                    self.ws.run_forever()
                    break  # If run_forever exits normally, break the loop
                except Exception as e:
                    if self._stop_event.is_set() or not self.running:
                        break  # Exit if stop was requested
                    logger.error(f"WebSocket error, retrying: {e}")
                    if self.auto_reconnect:
                        time.sleep(1)
                    else:
                        break
        except Exception as e:
            if not self._stop_event.is_set():
                logger.error(f"WebSocket thread error: {e}")
        finally:
            logger.debug("WebSocket thread exiting")

    def _create_interruptible_dispatcher(self):
        """Create a dispatcher that can be interrupted by the stop event."""
        # This approach doesn't work well with websocket-client library
        # Let's use the WebSocket's built-in close mechanism instead
        pass

    def force_shutdown(self):
        """Force immediate shutdown of all components."""
        logger.info("🚨 Force shutdown initiated...")
        
        # Set all stop flags immediately
        self._stop_event.set()
        self.running = False
        self.auto_reconnect = False
        self.connected = False
        
        # Force close WebSocket without waiting
        if self.ws:
            try:
                self.ws.close()
                self.ws.keep_running = False  # Force websocket-client to stop
            except:
                pass  # Ignore any errors during force close
        
        # Don't wait for thread - just mark it as done
        self.ws = None
        self.ws_thread = None
        self.subscribed_symbols.clear()
        
        logger.info("🚨 Force shutdown completed")

    def authenticate(self, username: str) -> bool:
        """
        Authenticate the client using a username.
        
        Args:
            username: Username for authentication
            
        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            token = self.get_token(username)
            return token is not None
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False


# Convenience function for quick setup
def create_client(ws_uri: str = "ws://localhost:8080", 
                 api_uri: str = "http://localhost:3000",
                 token: Optional[str] = None,
                 username: Optional[str] = None) -> NSEClient:
    """
    Create NSE client with default settings.
    
    Args:
        ws_uri: WebSocket URI
        api_uri: REST API URI  
        token: JWT token (will try to load from file if not provided)
        username: Username for authentication (optional, used if no token provided)
        
    Returns:
        NSEClient: Configured client instance
    """
    if not token:
        # Try to load token from file
        try:
            with open("test_tokens.json", "r") as f:
                tokens = json.load(f)
                token = list(tokens.values())[0]
                print(f"🔑 Loaded token for user: {list(tokens.keys())[0]}")
        except:
            # Use hardcoded token as fallback
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImp0aSI6ImMzOWY4NzgzLWFmZTYtNDk5Zi1hNTg1LWRjYTkxNjk1ZjFhZCIsImV4cCI6MTc0ODk2OTYyNiwiaWF0IjoxNzQ4OTYyNDI2LCJ1c2VyX2lkIjoiYWRtaW4iLCJwZXJtaXNzaW9ucyI6WyJyZWFkX2RhdGEiLCJ3ZWJzb2NrZXRfY29ubmVjdCIsImFkbWluIl19.PTCECjo-wCdr9Tgp6bRYR2bcrBtv7uZzr6N4z7L-TkU"
            print("🔑 Using default token")
    
    client = NSEClient(ws_uri, api_uri, token)
    
    # Authenticate if username provided and no token
    if not token and username:
        if not client.authenticate(username):
            raise AuthenticationError(f"Failed to authenticate user: {username}")
    
    return client


if __name__ == "__main__":
    # Example usage
    print("NSE Socket Client Library")
    print("=" * 40)
    
    # Create client
    client = create_client()
    
    # Configure event handlers
    def handle_market_data(data):
        symbol = data["symbol"]
        price_data = data["data"]
        print(f"{symbol}: Price=${price_data['close']:.2f}, Volume={price_data['volume']:,}")
    
    def handle_connection():
        print("Market data connection established")
    
    def handle_disconnection():
        print("Market data connection lost")
    
    def handle_order_update(order):
        print(f"Order {order['id']}: {order['status']}")
    
    # Assign event handlers
    client.on_ticks = handle_market_data
    client.on_connect = handle_connection
    client.on_disconnect = handle_disconnection
    client.on_order_update = handle_order_update
    
    # Method 1: Connect and subscribe in one call, then run
    symbols = ["NIFTY", "INDIGO", "RELIANCE", "TCS", "HDFC"]
    if client.connect_and_subscribe(symbols):
        print("🚀 Streaming data for multiple symbols... Press Ctrl+C to stop")
        client.run()  # This blocks until stopped
    else:
        print("❌ Failed to connect and subscribe") 