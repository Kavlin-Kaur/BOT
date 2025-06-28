# QonnectBot Integration Examples

This document provides integration examples for different platforms to help you integrate QonnectBot into your existing Qonnect app.

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Authentication
All requests require a Bearer token in the Authorization header:
```
Authorization: Bearer your-secret-key
```

### Endpoints

1. **Health Check**: `GET /`
2. **Chat**: `POST /chat`
3. **Analytics**: `GET /analytics`

## 1. React/JavaScript Integration

```javascript
// qonnectBot.js
class QonnectBot {
    constructor(apiUrl = 'http://localhost:8000', apiKey = 'your-secret-key') {
        this.apiUrl = apiUrl;
        this.apiKey = apiKey;
        this.sessionId = `session_${Date.now()}`;
    }

    async sendMessage(message, userId = null) {
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: userId,
                    session_id: this.sessionId,
                    language: 'en'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    async getAnalytics() {
        try {
            const response = await fetch(`${this.apiUrl}/analytics`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error getting analytics:', error);
            throw error;
        }
    }
}

// Usage in React component
import React, { useState, useEffect } from 'react';

function ChatComponent() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [bot] = useState(new QonnectBot());

    const sendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage = { role: 'user', content: inputMessage };
        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');
        setIsLoading(true);

        try {
            const response = await bot.sendMessage(inputMessage, 'user123');
            
            const botMessage = {
                role: 'assistant',
                content: response.answer,
                confidence: response.confidence,
                sources: response.sources
            };
            
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'Sorry, I encountered an error. Please try again.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.role}`}>
                        <div className="content">{msg.content}</div>
                        {msg.confidence && (
                            <div className="confidence">
                                Confidence: {(msg.confidence * 100).toFixed(1)}%
                            </div>
                        )}
                    </div>
                ))}
                {isLoading && (
                    <div className="message assistant">
                        <div className="content">🤔 Thinking...</div>
                    </div>
                )}
            </div>
            
            <div className="input-area">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask me anything..."
                    disabled={isLoading}
                />
                <button onClick={sendMessage} disabled={isLoading}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default ChatComponent;
```

## 2. Flutter/Dart Integration

```dart
// qonnect_bot.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class QonnectBot {
  final String apiUrl;
  final String apiKey;
  final String sessionId;

  QonnectBot({
    this.apiUrl = 'http://localhost:8000',
    this.apiKey = 'your-secret-key',
  }) : sessionId = 'session_${DateTime.now().millisecondsSinceEpoch}';

  Future<Map<String, dynamic>> sendMessage(
    String message, {
    String? userId,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$apiUrl/chat'),
        headers: {
          'Authorization': 'Bearer $apiKey',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'message': message,
          'user_id': userId,
          'session_id': sessionId,
          'language': 'en',
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to send message: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error sending message: $e');
    }
  }

  Future<Map<String, dynamic>> getAnalytics() async {
    try {
      final response = await http.get(
        Uri.parse('$apiUrl/analytics'),
        headers: {
          'Authorization': 'Bearer $apiKey',
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Failed to get analytics: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error getting analytics: $e');
    }
  }
}

// Usage in Flutter widget
import 'package:flutter/material.dart';

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Map<String, dynamic>> messages = [];
  final TextEditingController _controller = TextEditingController();
  final QonnectBot _bot = QonnectBot();
  bool _isLoading = false;

  void _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;

    final userMessage = {
      'role': 'user',
      'content': _controller.text,
    };

    setState(() {
      messages.add(userMessage);
      _isLoading = true;
    });

    _controller.clear();

    try {
      final response = await _bot.sendMessage(userMessage['content']);
      
      final botMessage = {
        'role': 'assistant',
        'content': response['answer'],
        'confidence': response['confidence'],
        'sources': response['sources'],
      };

      setState(() {
        messages.add(botMessage);
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        messages.add({
          'role': 'assistant',
          'content': 'Sorry, I encountered an error. Please try again.',
        });
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('QonnectBot Chat')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == messages.length && _isLoading) {
                  return ListTile(
                    leading: CircleAvatar(child: Text('🤖')),
                    title: Text('🤔 Thinking...'),
                  );
                }

                final message = messages[index];
                final isUser = message['role'] == 'user';

                return ListTile(
                  leading: CircleAvatar(
                    child: Text(isUser ? '👤' : '🤖'),
                  ),
                  title: Text(message['content']),
                  subtitle: message['confidence'] != null
                      ? Text('Confidence: ${(message['confidence'] * 100).toStringAsFixed(1)}%')
                      : null,
                );
              },
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Ask me anything...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _isLoading ? null : _sendMessage,
                  child: Text('Send'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

## 3. Python Integration

```python
# qonnect_bot_client.py
import requests
import json
from typing import Optional, Dict, Any

class QonnectBotClient:
    def __init__(self, api_url: str = "http://localhost:8000", api_key: str = "your-secret-key"):
        self.api_url = api_url
        self.api_key = api_key
        self.session_id = f"session_{int(time.time())}"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def send_message(self, message: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to QonnectBot"""
        try:
            data = {
                "message": message,
                "user_id": user_id,
                "session_id": self.session_id,
                "language": "en"
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error sending message: {e}")
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        try:
            response = requests.get(
                f"{self.api_url}/analytics",
                headers=self.headers,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting analytics: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Health check failed: {e}")

# Usage example
if __name__ == "__main__":
    bot = QonnectBotClient()
    
    # Check health
    try:
        health = bot.health_check()
        print(f"Bot status: {health['status']}")
    except Exception as e:
        print(f"Health check failed: {e}")
        exit(1)
    
    # Send a message
    try:
        response = bot.send_message("What is Qonnect?", user_id="test_user")
        print(f"Bot response: {response['answer']}")
        print(f"Confidence: {response['confidence']:.1%}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Get analytics
    try:
        analytics = bot.get_analytics()
        print(f"Total sessions: {analytics['total_sessions']}")
        print(f"Total exchanges: {analytics['total_exchanges']}")
    except Exception as e:
        print(f"Analytics error: {e}")
```

## 4. cURL Examples

```bash
# Health check
curl -X GET "http://localhost:8000/" \
  -H "Authorization: Bearer your-secret-key"

# Send a message
curl -X POST "http://localhost:8000/chat" \
  -H "Authorization: Bearer your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Qonnect?",
    "user_id": "user123",
    "session_id": "session_123",
    "language": "en"
  }'

# Get analytics
curl -X GET "http://localhost:8000/analytics" \
  -H "Authorization: Bearer your-secret-key"
```

## 5. Environment Variables

Create a `.env` file for your application:

```env
QONNECT_API_URL=http://localhost:8000
QONNECT_API_KEY=your-secret-key
QONNECT_SESSION_ID=your-session-id
```

## 6. Error Handling

Always implement proper error handling:

```javascript
// JavaScript example
try {
    const response = await bot.sendMessage(message);
    // Handle success
} catch (error) {
    if (error.message.includes('401')) {
        // Handle authentication error
        console.error('Invalid API key');
    } else if (error.message.includes('503')) {
        // Handle service unavailable
        console.error('Bot service is down');
    } else {
        // Handle other errors
        console.error('Unexpected error:', error);
    }
}
```

## 7. Best Practices

1. **Rate Limiting**: Implement rate limiting to avoid overwhelming the API
2. **Caching**: Cache common responses for better performance
3. **Retry Logic**: Implement exponential backoff for failed requests
4. **Logging**: Log all interactions for debugging and analytics
5. **Security**: Never expose API keys in client-side code
6. **Session Management**: Use consistent session IDs for conversation continuity

## 8. Deployment

For production deployment:

1. **Change the API URL** to your production server
2. **Use environment variables** for API keys
3. **Implement proper CORS** configuration
4. **Add SSL/TLS** encryption
5. **Set up monitoring** and logging
6. **Configure load balancing** if needed

## Support

For questions or issues with integration, check the API documentation at `http://localhost:8000/docs` when the server is running. 