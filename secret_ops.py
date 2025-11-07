# secret_ops.py

import logging

def get_user_data(user_id, password):
    # CRITICAL FLAW: Logs the unencrypted password!
    logging.info(f"Attempted login for {user_id} with password: {password}")
    return "User data..."