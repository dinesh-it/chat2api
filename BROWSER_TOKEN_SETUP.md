# Automatic Browser Token Retrieval

This feature allows the chat2api service to automatically retrieve ChatGPT access tokens from your default browser session, eliminating the need to manually copy tokens.

## Prerequisites

1. **Install Dependencies**
   ```bash
   pip install playwright aiofiles
   
   # Install browser binaries (required for playwright)
   playwright install chromium
   ```

2. **Browser Requirements**
   - You must be logged into ChatGPT in your default Chrome browser
   - The browser should have a valid ChatGPT session

## Configuration

Set the environment variable to enable automatic browser token retrieval:

```bash
export AUTO_BROWSER_TOKEN=true
```

Or add it to your `.env` file:
```
AUTO_BROWSER_TOKEN=true
```

## How It Works

1. **Automatic Token Retrieval**: When enabled, the service will automatically launch a headless browser instance using your existing Chrome profile
2. **Session Access**: It navigates to `https://chatgpt.com/api/auth/session` to retrieve the current access token
3. **Token Integration**: The retrieved token is automatically integrated into the existing authentication flow
4. **Token Management**: The token is added to the token list and can be refreshed automatically

## Usage Scenarios

### Scenario 1: No Manual Tokens Required
If you have `AUTO_BROWSER_TOKEN=true` and no authorization list configured, the service will automatically use your browser session.

### Scenario 2: Fallback Token Source  
If you have other tokens configured but they fail, the browser token can serve as a fallback.

### Scenario 3: Token Refresh
The browser token will be refreshed during the regular token refresh cycle.

## Testing

Test the functionality with the included test script:

```bash
python test_browser_token.py
```

## Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `AUTO_BROWSER_TOKEN` | `false` | Enable automatic browser token retrieval |
| `AUTHORIZATION` | empty | Manual authorization tokens (if any) |

## Troubleshooting

### Common Issues

1. **Browser Not Found**
   - Ensure Chrome is installed and in the default location
   - The service will attempt to find your Chrome user data directory automatically

2. **No Active Session**
   - Make sure you're logged into ChatGPT in your default browser
   - Try opening https://chatgpt.com manually to verify your session

3. **Permission Issues**
   - Ensure the service has permission to access your browser profile
   - On some systems, you may need to run with appropriate permissions

4. **Headless Browser Fails**
   - Check that all playwright dependencies are installed
   - Verify that `playwright install chromium` was run successfully

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## Security Considerations

- The browser token retrieval runs in a headless mode and doesn't display any UI
- Your browser profile data is accessed read-only
- Tokens are handled the same way as manually provided tokens
- Consider the security implications of automated token access in your environment

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| macOS | ✅ Supported | Uses ~/Library/Application Support/Google/Chrome |
| Windows | ✅ Supported | Uses %LOCALAPPDATA%\Google\Chrome\User Data |
| Linux | ✅ Supported | Uses ~/.config/google-chrome |

## Example Configuration

Complete `.env` file example:
```bash
# Enable automatic browser token retrieval
AUTO_BROWSER_TOKEN=true

# Optional: Disable other auth requirements
AUTHORIZATION=

# Optional: Other settings
CHATGPT_BASE_URL=https://chatgpt.com
RANDOM_TOKEN=true
```