import utils.paths as paths
import utils.env as service_env
from utils.interface_ip import get_external_ip
import logging
import uuid 
import argparse 
import os
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv('DOMAIN')
KEY_SERVER_HOSTNAME = 'scc.' + DOMAIN 
STREAM_HOSTNAME = 'stream.' + DOMAIN

def main(args):
    # Test env files
    if not args.skip_env:
        service_env.test_env_files()
    else:
        logging.info('Skipping env file test.')

    # Generate Secrets
    srs_api_key = uuid.uuid4().hex.upper()[0:16]
    feed_hmac_key = uuid.uuid4().hex.upper()[0:16]
    srs_hook_key = 'hookpass'


    # Fetch Candidate IP
    logging.info('Fetching candidate IP...')
    candidate_ip = get_external_ip()
    logging.info(f'Candidate IP: {candidate_ip}')

    # Generate env files
    logging.info('Generating env files...')
    nginx_env = service_env.NginxEnv(stream_hostname=STREAM_HOSTNAME,
                                    key_server_hostname=KEY_SERVER_HOSTNAME,
                                    cert_pem_path='/etc/letsencrypt/live/{}/fullchain.pem'.format(DOMAIN),
                                    cert_key_path='/etc/letsencrypt/live/{}/privkey.pem'.format(DOMAIN))
    with open(paths.NGINX_ENV_PATH, 'w') as f:
        f.write(str(nginx_env))
    
    srs_origin_env = service_env.SrsOriginEnv(http_auth_password=srs_api_key, CANDIDATE=candidate_ip)
    with open(paths.SRS_ORIGIN_ENV_PATH, 'w') as f:
        f.write(str(srs_origin_env))

    key_server_env = service_env.KeyServerEnv(srs_endpoint=f'http://srs:1985',
                                              srs_http_auth_password=srs_api_key,
                                              srs_hook_key=srs_hook_key,
                                              stream_host_name=STREAM_HOSTNAME,
                                              feed_hmac_key=feed_hmac_key,
                                              DATABASE_URL='mongodb+srv://root:root@mongo/ssc',
                                              GOOGLE_CLIENT_ID='365941463067-uriifplv9h8jobq6e2dv7v07ello9g7h.apps.googleusercontent.com'
                                              )
    with open(paths.KEY_SERVER_ENV_PATH, 'w',) as f:
        f.write(str(key_server_env))

    certbot_cloudflare_env = service_env.CertbotCloudflareEnv(cloudflare_api_key='dummy')
    with open(paths.CERTBOT_CLOUDFLARE_ENV_PATH, 'w') as f:
        f.write(str(certbot_cloudflare_env))

    logging.info('Generating env files complete.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='[Production]Deploy Yakkai services.'
    )
    parser.add_argument('--skip-env', action='store_true', help='Skip env file generation.')
    args = parser.parse_args()
    main(args)