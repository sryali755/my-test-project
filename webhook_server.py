from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
import os
from datetime import datetime


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/webhook':
            # Read payload
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                
                # Check if it's a push event
                if 'ref' in payload and 'commits' in payload:
                    print(f"\n{'='*60}")
                    print(f"📦 GitHub Push Event Received!")
                    print(f"{'='*60}")
                    print(f"Repository: {payload['repository']['full_name']}")
                    print(f"Branch: {payload['ref'].replace('refs/heads/', '')}")
                    print(f"Commits: {len(payload['commits'])}")
                    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    # Save payload to file
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    payload_file = f'webhook_payload_{timestamp}.json'
                    
                    with open(payload_file, 'w') as f:
                        json.dump(payload, f, indent=2)
                    
                    print(f"\n✅ Payload saved to: {payload_file}")
                    print(f"\n🔄 Processing with GitHub Code Analyzer skill...")
                    print(f"{'='*60}\n")
                    
                    # Process the webhook
                    self.process_webhook(payload_file)
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'status': 'success', 'message': 'Webhook processed'}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(400)
                    self.end_headers()
                    
            except Exception as e:
                print(f"Error processing webhook: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def process_webhook(self, payload_file):
        """Process webhook payload and log information"""
        try:
            with open(payload_file, 'r') as f:
                payload = json.load(f)
            
            repo_name = payload['repository']['full_name']
            commits = payload.get('commits', [])
            
            print(f"\n--- Processing Webhook for: {repo_name} ---")
            print(f"Total Commits: {len(commits)}")
            
            # Extract file changes
            added, modified, removed = [], [], []
            for commit in commits:
                added.extend(commit.get('added', []))
                modified.extend(commit.get('modified', []))
                removed.extend(commit.get('removed', []))
            
            print(f"Files Added: {len(added)}")
            print(f"Files Modified: {len(modified)}")
            print(f"Files Removed: {len(removed)}")
            
            if added or modified:
                print("\nChanges detected:")
                for f in set(added + modified):
                    print(f"  - {f}")
            
            # Save a simplified processed file to maintain flow if needed
            data = {
                'repository': repo_name,
                'files': {
                    'added': list(set(added)),
                    'modified': list(set(modified)),
                    'removed': list(set(removed))
                }
            }
            with open('webhook_processed.json', 'w') as f:
                json.dump(data, f, indent=2)
                
            print(f"\n{'='*60}")
            print("✅ Event logged successfully!")
            print(f"{'='*60}\n")
            
        except Exception as e:
            print(f"Error in processing: {e}")
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass


def main():
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebhookHandler)
    
    print(f"\n{'='*60}")
    print(f"🚀 GitHub Webhook Server Started!")
    print(f"{'='*60}")
    print(f"Listening on: http://localhost:{port}")
    print(f"Webhook URL: http://localhost:{port}/webhook")
    print(f"\nWaiting for GitHub push events...")
    print(f"{'='*60}\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")


if __name__ == '__main__':
    main()