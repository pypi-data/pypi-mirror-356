#!/usr/bin/env python3
"""
System tray application for Alita MCP Client.
Provides easy access to configuration and server management.
"""
import os
import sys
import threading
import subprocess
import platform
import multiprocessing
import logging

logger = logging.getLogger(__name__)

# Fix for macOS fork safety with GUI applications
if platform.system() == "Darwin":
    # Set environment variable to disable fork safety check as a fallback
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    
    # Set multiprocessing start method to spawn to avoid fork issues
    try:
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        # Already set, ignore
        logger.debug("Multiprocessing start method already set to 'spawn'")
        pass

import pystray
from PIL import Image, ImageDraw
from .config import get_bootstrap_config, set_bootstrap_config, interactive_bootstrap, get_config_file
from .utils.server_controller import get_server_controller
from .main import main, setup_file_logger, get_default_paths


class MCPTrayApp:
    def __init__(self):
        self.icon = None
        self.server_controller = get_server_controller()
        self.is_server_running = False
        
        # Set up callbacks for server controller
        self.server_controller.set_status_callback(self.on_server_status_change)
        self.server_controller.set_error_callback(self.on_server_error)
        
    def create_icon_image(self):
        """Create an icon for the system tray using the Alita logo."""
        try:
            # Load the PNG logo using package resources (works when packaged)
            logo_data = self._load_icon_data()
            
            if logo_data:
                # Create image from binary data
                from io import BytesIO
                image = Image.open(BytesIO(logo_data))
                
                # Ensure the image is the right size
                if image.size != (64, 64):
                    image = image.resize((64, 64), Image.Resampling.LANCZOS)
                
                # Convert to RGBA if not already
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                
                # For macOS, create a monochrome version for better tray integration
                if platform.system().lower() == "darwin":
                    # Create a monochrome version
                    # Convert to grayscale first
                    gray_image = image.convert('L')
                    
                    # Create a new RGBA image
                    mono_image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
                    
                    # Apply the grayscale as an alpha mask to create white/transparent icon
                    for x in range(64):
                        for y in range(64):
                            # Get the grayscale value
                            gray_value = gray_image.getpixel((x, y))
                            
                            # Create white pixels where the logo is visible
                            if gray_value > 50:  # Threshold to avoid very faint pixels
                                # Use the grayscale value as alpha for smooth edges
                                alpha = min(255, gray_value + 50)  # Boost contrast slightly
                                mono_image.putpixel((x, y), (255, 255, 255, alpha))
                    
                    return mono_image
                else:
                    # For other platforms, use the full-color logo
                    return image
            else:
                # Fallback: create a simple icon if logo file not found
                return self._create_fallback_icon()
                
        except Exception as e:
            logger.warning(f"Could not load logo icon ({e}), using fallback")
            return self._create_fallback_icon()
    
    def _load_icon_data(self):
        """Load icon data using package resources (works when packaged)."""
        try:
            # Try modern importlib.resources first (Python 3.9+)
            try:
                import importlib.resources as resources
                
                # Try to load the icon from the package
                try:
                    # For Python 3.9+
                    icon_package = resources.files('alita_mcp.icons')
                    icon_file = icon_package / 'logo64x64.png'
                    return icon_file.read_bytes()
                except AttributeError:
                    # For Python 3.9-3.10 compatibility
                    with resources.path('alita_mcp.icons', 'logo64x64.png') as icon_path:
                        return icon_path.read_bytes()
                        
            except (ImportError, ModuleNotFoundError):
                # Fallback to pkg_resources for older Python versions
                try:
                    import pkg_resources
                    return pkg_resources.resource_string('alita_mcp', 'icons/logo64x64.png')
                except (ImportError, FileNotFoundError):
                    pass
            
            # Final fallback: try direct file access (development mode)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_dir, 'icons', 'logo64x64.png')
            
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    return f.read()
                    
        except Exception as e:
            logger.error(f"Failed to load icon data: {e}")
            
        return None
    
    def _create_fallback_icon(self):
        """Create a fallback icon when the PNG logo is not available."""
        # Create a simple icon - a blue circle with "MCP" text
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw circle background
        draw.ellipse([2, 2, width-2, height-2], fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=2)
        
        # Draw "MCP" text (simplified)
        try:
            # Try to use a font, fall back to default if not available
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("Arial", 14)
            except OSError:
                font = ImageFont.load_default()
            draw.text((width//2, height//2), "MCP", fill=(255, 255, 255, 255), 
                     font=font, anchor="mm")
        except ImportError:
            # Fallback for basic drawing
            draw.text((18, 25), "MCP", fill=(255, 255, 255, 255))
            
        return image
            
        return image

    def get_menu_items(self):
        """Create the context menu for the tray icon."""
        config = get_bootstrap_config()
        is_configured = config.get('deployment_url') and config.get('auth_token')
        
        menu_items = [
            pystray.MenuItem("ELITEA MCP Client", lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
        ]
        
        if is_configured:
            if not self.is_server_running:
                # Show start options when server is not running
                menu_items.extend([
                    pystray.MenuItem("Start MCP Server", lambda: self.start_server(daemon_mode=False))
                ]),
            else:
                menu_items.extend([
                    pystray.MenuItem(f"Stop MCP Server", self.stop_server),
                    pystray.MenuItem("Restart MCP Server", self.restart_server),
                ])
            menu_items.append(pystray.Menu.SEPARATOR)
        
        menu_items.extend([
            pystray.MenuItem("Configuration", pystray.Menu(
                pystray.MenuItem("Open Config File", self.open_config_file),
                pystray.MenuItem("Open Config Folder", self.open_config_folder),
                pystray.MenuItem("Bootstrap (Terminal)", self.bootstrap_config),
                pystray.MenuItem("View Current Config", self.view_config),
            )),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("About", self.show_about),
            pystray.MenuItem("Quit", self.quit_app),
        ])
        
        return menu_items
        
    def on_server_status_change(self, status: str):
        """Handle server status changes."""
        self.is_server_running = self.server_controller.is_running
        self.update_menu()
        if status:
            self.show_notification("Server Status", status)
    
    def on_server_error(self, error: str):
        """Handle server errors."""
        self.is_server_running = False
        self.update_menu()
        self.show_error("Server Error", error)

    def start_server(self, daemon_mode: bool = False):
        """Start the MCP server using the server controller.
        
        Args:
            daemon_mode: If True, start as separate daemon process. If False, start in current process.
        """
        if self.is_server_running:
            return
            
        config = get_bootstrap_config()
        if not config.get('deployment_url') or not config.get('auth_token'):
            self.show_error("Configuration Required", 
                          "Please configure the client first using Bootstrap.")
            return
            
        # Use the server controller to start servers
        success = self.server_controller.start_servers(daemon_mode=daemon_mode)
        if not success:
            mode_str = "daemon" if daemon_mode else "embedded"
            self.show_error("Server Start Failed", f"Failed to start MCP servers in {mode_str} mode.")

    def stop_server(self):
        """Stop the MCP server using the server controller."""
        if not self.is_server_running:
            return

        self.server_controller.stop_servers()

    def restart_server(self):
        """Restart the MCP server to reload configuration."""
        self.server_controller.restart_servers()

    def open_config_file(self, icon=None, item=None):
        """Open the configuration file in the default text editor."""
        config_file = get_config_file()
        
        # Ensure the config file exists
        if not config_file.exists():
            # Create an empty config file
            config_file.parent.mkdir(parents=True, exist_ok=True)
            config_file.write_text('{}')
            logger.info(f"Created config file: {config_file}")
        
        self._open_file(config_file)
        logger.info(f"Opening config file: {config_file}")

    def open_config_folder(self, icon=None, item=None):
        """Open the configuration folder in the file manager."""
        config_file = get_config_file()
        config_folder = config_file.parent
        
        # Ensure the config folder exists
        config_folder.mkdir(parents=True, exist_ok=True)
        
        self._open_file(config_folder)
        logger.info(f"Opening config folder: {config_folder}")

    def _open_file(self, file_path):
        """Open a file or folder using the system's default application."""
        try:
            system = platform.system().lower()
            
            if system == "darwin":  # macOS
                # Create environment for subprocess to handle fork safety
                env = os.environ.copy()
                env['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
                
                subprocess.run(
                    ["open", str(file_path)], 
                    check=True,
                    env=env,
                    start_new_session=True
                )
            elif system == "linux":
                subprocess.run(["xdg-open", str(file_path)], check=True)
            elif system == "windows":
                os.startfile(str(file_path))
            else:
                logger.warning(f"Unsupported platform: {system}")
                logger.info(f"Please manually open: {file_path}")
        except Exception as e:
            logger.error(f"Failed to open {file_path}: {e}")
            logger.info(f"Please manually open: {file_path}")

    def bootstrap_config(self, icon=None, item=None):
        """Run the interactive bootstrap configuration in terminal."""
        logger.info("\n" + "="*50)
        logger.info("Running Bootstrap Configuration...")
        logger.info("="*50)
        
        try:
            # Run bootstrap in the current process
            config = interactive_bootstrap()
            logger.info("Configuration updated successfully!")
            self.update_menu()
            self.show_notification("Bootstrap Complete", "Configuration has been updated.")
        except Exception as e:
            error_msg = f"Bootstrap failed: {str(e)}"
            logger.error(error_msg)
            self.show_error("Bootstrap Error", error_msg)

    def view_config(self, icon=None, item=None):
        """Display current configuration in the console."""
        config = get_bootstrap_config()
        
        logger.info("\n" + "="*50)
        logger.info("Current Configuration:")
        logger.info("="*50)
        logger.info(f"Deployment URL: {config.get('deployment_url', 'Not set')}")
        
        auth_token = config.get('auth_token', '')
        if auth_token:
            masked_token = '*' * 8 + auth_token[-4:] if len(auth_token) > 4 else '*' * 8
            logger.info(f"Auth Token: {masked_token}")
        else:
            logger.info("Auth Token: Not set")
            
        logger.info(f"Host: {config.get('host', '0.0.0.0')}")
        logger.info(f"Port: {config.get('port', 8000)}")
        logger.info(f"Project ID: {config.get('project_id', 'Not set')}")
        
        servers = config.get('servers', {})
        if servers:
            logger.info(f"\nConfigured Servers ({len(servers)}):")
            for server_name in servers.keys():
                logger.info(f"  - {server_name}")
        else:
            logger.info("\nNo servers configured")
        
        logger.info(f"\nConfig file location: {get_config_file()}")
        logger.info("="*50)

    def show_about(self, icon=None, item=None):
        """Show about information in console."""
        logger.info("\n" + "="*50)
        logger.info("About Alita MCP Client")
        logger.info("="*50)
        logger.info("Version: 0.1.6")
        logger.info("A Model Context Protocol client for the ELITEA platform.")
        logger.info("\nThis tray application provides easy access to:")
        logger.info("• Configuration management")
        logger.info("• MCP server control")
        logger.info("• Quick status monitoring")
        logger.info("="*50)

    def show_error(self, title, message):
        """Show error message in console and as notification."""
        logger.error(f"{title}: {message}")
        if self.icon:
            self.icon.notify(f"{title}: {message}", "Error")

    def show_notification(self, title, message):
        """Show notification using the system tray."""
        logger.info(f"{title}: {message}")
        if self.icon:
            self.icon.notify(message, title)

    def update_menu(self):
        """Update the tray menu."""
        if self.icon:
            self.icon.menu = pystray.Menu(*self.get_menu_items())

    def quit_app(self, icon=None, item=None):
        """Quit the application."""
        if self.is_server_running:
            self.stop_server()
        if self.icon:
            self.icon.stop()

    def run(self):
        """Start the tray application."""
        # Hide from dock on macOS
        self._hide_from_dock()
        
        image = self.create_icon_image()
        menu = pystray.Menu(*self.get_menu_items())
        
        self.icon = pystray.Icon(
            "alita_mcp",
            image,
            "Alita MCP Client",
            menu
        )
        
        logger.info("Starting Alita MCP Client tray application...")
        logger.info("Right-click the tray icon for options")
        logger.info("Use 'Open Config File' to edit configuration")
        self.icon.run()

    def _hide_from_dock(self):
        """Hide the application from the macOS dock."""
        if platform.system().lower() == "darwin":
            try:
                # Import PyObjC modules for macOS
                from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
                
                # Get the shared application instance
                app = NSApplication.sharedApplication()
                
                # Set activation policy to accessory (no dock icon)
                app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
                
                logger.info("Successfully hidden from macOS dock")
                
            except ImportError:
                logger.warning("PyObjC not available, cannot hide from dock")
                logger.info("Install with: pip install pyobjc-framework-Cocoa")
            except Exception as e:
                logger.warning(f"Failed to hide from dock: {e}")
        else:
            # Not macOS, no action needed
            pass


def run_tray():
    """Entry point for the tray application."""
    # Set fork safety for macOS BEFORE any other imports or operations
    if platform.system() == "Darwin":
        os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    
    # Set up file logging
    try:
        default_paths = get_default_paths()
        log_file = default_paths['tray_log']
        file_handler = setup_file_logger(str(log_file))
        logger.info(f"Logging to file: {log_file}")
    except Exception as e:
        logger.warning(f"Could not set up file logging: {e}")
    
    app = MCPTrayApp()
    app.run()


def main():
    """Main entry point that sets up environment before any imports."""
    import platform
    import os
    
    # Critical: Set fork safety for macOS BEFORE importing pystray or any GUI frameworks
    if platform.system() == "Darwin":
        os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
        
        # Also set multiprocessing method to spawn
        try:
            import multiprocessing
            multiprocessing.set_start_method('spawn', force=True)
        except RuntimeError:
            pass  # Already set
    
    # Now it's safe to run the tray
    run_tray()


if __name__ == "__main__":
    main()
