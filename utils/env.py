import logging
import os
import utils.paths as paths

class NginxEnv:
    def __init__(self, stream_hostname: str, key_server_hostname: str,
                 cert_pem_path: str = '/etc/nginx/ssl/server.crt',
                    cert_key_path: str = '/etc/nginx/ssl/server.key'):
        self.stream_host_name = stream_hostname
        self.key_server_hostname = key_server_hostname
        self.cert_pem_path = cert_pem_path
        self.cert_key_path = cert_key_path

    def __str__(self) -> str:
        return f"NGINX_STREAM_HOSTNAME={self.stream_host_name}\n" \
               f"NGINX_KEYSERVER_HOSTNAME={self.key_server_hostname}\n" \
                f"NGINX_CERT_PEM_PATH={self.cert_pem_path}\n" \
                f"NGINX_CERT_KEY_PATH={self.cert_key_path}\n"

class SrsOriginEnv:
    def __init__(self, http_auth_password: str, CANDIDATE: str):
        self.http_auth_password = http_auth_password
        self.CANDIDATE = CANDIDATE 

    def __str__(self) -> str:
        return f"SRS_HTTP_API_AUTH_PASSWORD={self.http_auth_password}\n" \
                f"CANDIDATE={self.CANDIDATE}\n" \
                f"SRS_VHOST_HTTP_HOOKS_ON_PUBLISH=http://control-api:3005/hook/streams\n" \
                f"SRS_VHOST_HTTP_HOOKS_ON_UNPUBLISH=http://control-api:3005/hook/streams\n" \
                f"SRS_VHOST_HTTP_HOOKS_ON_PLAY=http://control-api:3005/hook/sessions\n" \
                f"SRS_VHOST_HTTP_HOOKS_ON_STOP=http://control-api:3005/hook/sessions\n" \
                f"SRS_VHOST_HTTP_HOOKS_ON_DVR=http://control-api:3005/hook/dvr/s3\n"
        
    
class KeyServerEnv:
    def __init__(self, 
                 srs_endpoint: str,
                    srs_http_auth_password: str,
                    srs_hook_key: str,
                    feed_hmac_key: str,
                    stream_host_name: str,
                    DATABASE_URL: str,
                    GOOGLE_CLIENT_ID: str,

    ):
        self.srs_endpoint = srs_endpoint
        self.srs_http_auth_password = srs_http_auth_password
        self.srs_hook_key = srs_hook_key
        self.feed_hmac_key = feed_hmac_key
        self.stream_host_name = stream_host_name
        self.DATABASE_URL = DATABASE_URL
        self.GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID

    def __str__(self) -> str:
        return ''.join([
            f"SRS_API_ENDPOINT={self.srs_endpoint}\n",
            f"SRS_API_TOKEN={self.srs_http_auth_password}\n",
            f"SRS_HOOK_KEY={self.srs_hook_key}\n",
            f"FEED_HMAC_KEY={self.feed_hmac_key}\n",
            f"STREAM_HOST={self.stream_host_name}\n",
            f"DATABASE_URL={self.DATABASE_URL}\n",
            f"GOOGLE_CLIENT_ID={self.GOOGLE_CLIENT_ID}\n"
        ])

class CertbotCloudflareEnv:
    def __init__(self, cloudflare_api_key: str):
        self.cloudflare_api_key = cloudflare_api_key

    def __str__(self) -> str:
        return f"dns_cloudflare_api_token={self.cloudflare_api_key}\n"
    
def test_env_files():
    logging.info('Testing env files...')
    if not os.path.exists(paths.CERTS_PATH):
        logging.warning(f'Cert path does not exist: {paths.CERTS_PATH}, creating...')
        os.makedirs(paths.CERTS_PATH)
    if os.path.exists(paths.NGINX_ENV_PATH):
        logging.warning(f'Nginx env file already exists: {paths.NGINX_ENV_PATH}, deleting...')
        os.remove(paths.NGINX_ENV_PATH)
    if os.path.exists(paths.SRS_ORIGIN_ENV_PATH):
        logging.warning(f'SRS Origin env file already exists: {paths.SRS_ORIGIN_ENV_PATH}, deleting...')
        os.remove(paths.SRS_ORIGIN_ENV_PATH)
    if os.path.exists(paths.KEY_SERVER_ENV_PATH):
        logging.warning(f'Key Server env file already exists: {paths.KEY_SERVER_ENV_PATH}, deleting...')
        os.remove(paths.KEY_SERVER_ENV_PATH)
    logging.info('Testing env files complete.')
