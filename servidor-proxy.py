import http.server
import socketserver
import urllib.request
import json
from urllib.parse import urlparse

PORT = 8080
OLLAMA_URL = "http://localhost:11434"
N8N_URL = "http://localhost:5678"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Manejar preflight CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        """Interceptar peticiones POST y redirigir a Ollama o n8n"""
        if self.path.startswith('/api/'):
            # Peticiones a Ollama
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                ollama_url = f"{OLLAMA_URL}{self.path}"
                req = urllib.request.Request(
                    ollama_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=120) as response:
                    response_data = response.read()
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
                
                print(f"✓ Proxy Ollama: {self.path}")
                
            except Exception as e:
                print(f"✗ Error Ollama: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_msg = json.dumps({"error": str(e)}).encode()
                self.wfile.write(error_msg)
                
        elif self.path.startswith('/webhook/'):
            # Peticiones a n8n
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                n8n_url = f"{N8N_URL}{self.path}"
                req = urllib.request.Request(
                    n8n_url,
                    data=post_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                with urllib.request.urlopen(req, timeout=120) as response:
                    response_data = response.read()
                    
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
                
                print(f"✓ Proxy n8n: {self.path}")
                
            except Exception as e:
                print(f"✗ Error n8n: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_msg = json.dumps({"error": str(e)}).encode()
                self.wfile.write(error_msg)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        """Servir archivos estáticos normalmente"""
        return super().do_GET()

    def end_headers(self):
        """Agregar headers CORS a todas las respuestas"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print("=" * 60)
print(f"  Servidor Proxy con Ollama + n8n")
print("=" * 60)
print(f"\n✓ Puerto: {PORT}")
print(f"✓ Ollama: {OLLAMA_URL}")
print(f"✓ n8n: {N8N_URL}")
print(f"\n📡 Rutas proxy:")
print(f"   /api/*     -> Ollama (IA)")
print(f"   /webhook/* -> n8n (Workflows)")
print(f"📄 Otros archivos se sirven normalmente")
print(f"\n🌐 Acceso local: http://localhost:{PORT}")
print(f"\n⚠️  Después inicia ngrok: ngrok http {PORT}")
print("\nPresiona Ctrl+C para detener\n")

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✓ Servidor detenido")
