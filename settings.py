
#
# (C) Koninklijke Philips Electronics N.V. 2019
#
# All rights are reserved. Reproduction or transmission in whole or in
# part, in any form or by any means, electronic, mechanical or
# otherwise, is prohibited without the prior written consent of the
# copyright owner.
#

import os
from vcap_services import load_from_vcap_services
import logging
from logging.handlers import TimedRotatingFileHandler

HTTP_PROXY = os.getenv("PROXY_HTTP", "CHANGEME")
HTTPS_PROXY = os.getenv("PROXY_HTTPS", "CHANGEME")
ProxyDict = {
              "http": "http://" + HTTP_PROXY,
              "https": "https://" + HTTP_PROXY,
            }
enable_proxy = os.getenv("ENABLE_PROXY", False)
PROXY_ENABLED = enable_proxy in ["true", True]

HSPD_IAM_API_DOMAIN = os.getenv("HSPD_IAM_API_DOMAIN", "CHANGEME")
HSDP_S3_CREDS_API_DOMAIN = os.getenv("HSDP_S3_CREDS_API_DOMAIN", "CHANGEME")

HSDP_APIS_DICT = {
    "IAM_AUTH_API": HSPD_IAM_API_DOMAIN + "/authorize/oauth2/token",
    "IAM_REVOKE_TOKEN_API": HSPD_IAM_API_DOMAIN + "/authorize/oauth2/revoke",
    "S3_CREDS_API": HSDP_S3_CREDS_API_DOMAIN + "/core/credentials/Access/"
}

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("postgres_user")
POSTGRES_PW = os.getenv("Welcome@123")
POSTGRES_DB = os.getenv("Dbname#123")

CF_CLIENT_ID_SECRET = os.getenv("CF_CLIENT_ID_SECRET", "CHANGEME")

debug_mode = os.getenv("DEBUG_MODE", False)
DEBUG = True if debug_mode in ["true", True] else False

CF_PORT = os.getenv("CF_PORT")

APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
APP_PORT = os.getenv("APP_PORT", "5000")

AWS_BUCKET_REGION = os.getenv("AWS_BUCKET_REGION", "CHANGEME")

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "CHANGEME")

WHITELISTED_DOMAINS = os.getenv("WHITELISTED_DOMAINS", "localhost,127.0.0.1:5000").split(",")
WHITELISTED_DOMAINS = [wd.strip("\n ") for wd in WHITELISTED_DOMAINS]

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
LOG_FILE = os.getenv("LOG_FILE")
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_RETENTATION_DAYS = os.getenv("LOG_RETENTATION_DAYS")

HSDP_RDS_SERVICE = os.getenv("HSDP_RDS_SERVICE")

SESSION_TIMEOUT = os.getenv("SESSION_TIMEOUT", "0")
URL_EXPIRY = os.getenv("URL_EXPIRY", "0")

SNS_TOPIC_ARN_BASE = os.getenv("SNS_TOPIC_ARN_BASE", "CHANGEME")
SNS_PROTOCOL = os.getenv("SNS_PROTOCOL", "CHANGEME")
SNS_UNSUBSCRIPTION_BASE_URL = os.getenv("SNS_UNSUBSCRIPTION_BASE_URL", "CHANGEME")
SNS_REGION = os.getenv("SNS_REGION", "CHANGEME")

S3_PRODUCT_KEY = os.getenv("S3_PRODUCT_KEY", "CHANGEME")

VAULT_CLIENT_TOKEN_URL = os.getenv("VAULT_CLIENT_TOKEN_URL",'CHANGEME')
VAULT_SERVICE_HOST = os.getenv("VAULT_SERVICE_HOST","CHANGEME")
VAULT_SERVICE_SECRET_PATH_URL = os.getenv("VAULT_SERVICE_SECRET_PATH_URL",'CHANGEME')
ERROR_GENERATING_VAULT_AUTH_TOKEN = 'The auth token could not be generated.'
ERROR_RETREIVING_ALLOWEDFILETYPES = "The allowed file types could not be retrieved."
ERROR_RETREIVING_SNSKEYS = "The sns keys could not be retrieved."
SERVER_ERROR = 'Server Error.'

def get_logger(logging_level=logging.DEBUG, log_format=LOG_FORMAT):
    if LOG_FILE_PATH and LOG_FILE:
        logger = logging.getLogger()
        logger.setLevel(logging_level)
        file_handler = TimedRotatingFileHandler(LOG_FILE_PATH + LOG_FILE, when='D', interval=int(LOG_RETENTATION_DAYS))
        logs_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(logs_formatter)
        logger.addHandler(file_handler)
        logger.propagate = False
        return logger
    else:
        logging.basicConfig(format=log_format, level=logging_level)
        return logging.getLogger()

def get_db_creds():
    db_credentials = load_from_vcap_services(HSDP_RDS_SERVICE)
    if db_credentials:
        db_name = db_credentials.get("db_name")
        hostname = db_credentials.get("hostname")
        username = db_credentials.get("username")
        password = db_credentials.get("password")
        return db_name, hostname, username, password
    else:
        return POSTGRES_DB, POSTGRES_URL, POSTGRES_USER, POSTGRES_PW
