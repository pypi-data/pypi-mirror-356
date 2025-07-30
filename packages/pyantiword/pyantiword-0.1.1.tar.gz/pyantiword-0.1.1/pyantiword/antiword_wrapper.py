import os
import subprocess

ANTIWORD_PATH = os.path.join(os.path.dirname(__file__), "antiword")
ANTIWORD_SHARE = os.path.join(os.path.dirname(__file__), "antiword_share")

def extract_text_with_antiword(doc_path):
    env = os.environ.copy()
    env["ANTIWORDHOME"] = ANTIWORD_SHARE
    result = subprocess.run(
        [ANTIWORD_PATH, doc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        env=env
    )
    return result.stdout.decode('utf-8')
