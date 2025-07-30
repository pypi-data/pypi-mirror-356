import dropbox
import logging

from dropbox import DropboxOAuth2FlowNoRedirect

# Initialize and configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - "
                              "%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_refresh_token(
        APP_KEY: str,
        APP_SECRET: str
) -> str:

    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY, APP_SECRET, token_access_type="offline"
    )

    authorize_url = auth_flow.start()
    print(f"1. Visit this URL: {authorize_url}")
    auth_code = input("3. Enter the code here: ").strip()

    result = auth_flow.finish(auth_code)

    return result.refresh_token


def get_dropbox_client(
        APP_KEY: str,
        APP_SECRET: str,
        REFRESH_TOKEN: str
) -> dropbox.Dropbox:

    dbx: dropbox.Dropbox = dropbox.Dropbox(
        oauth2_refresh_token=REFRESH_TOKEN,
        app_key=APP_KEY,
        app_secret=APP_SECRET
    )

    try:
        dbx.users_get_current_account()
        logger.info("Dropbox call to application: {APP_KEY} was successful")
        return dbx

    except dropbox.exceptions.AuthError as e:
        logger.error(f"Authentication error: {e}")
