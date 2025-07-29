import os
import dropbox
import logging

from dropbox.oauth import DropboxOAuth2FlowNoRedirect

# Initializes the logger
logger = logging.getLogger(__name__)


class Dropbox:
    def __init__(self):
        self.APP_KEY = os.getenv("APP_KEY")
        self.APP_SECRET = os.getenv("APP_SECRET")
        self.REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
        self.DROPBOX_OAUTH = None

    def refresh_access_token(self):

        # Initializes the oauth flow
        oauth_flow: DropboxOAuth2FlowNoRedirect = DropboxOAuth2FlowNoRedirect(
            consumer_key=self.APP_KEY,
            consumer_secret=self.APP_SECRET,
            token_access_type='offline'
        )

        # gets the refreshed access token
        result = oauth_flow.refresh_access_token(self.REFRESH_TOKEN)

        new_token = {
            "access_token": result.access_token,
            "expires_at": result.expires_at.isoformat()
        }

        return new_token

    def get_dropbox_client(self):

        if not self.DROPBOX_OAUTH:
            self.DROPBOX_OAUTH = self.refresh_access_token()

        try:
            # Try using current token
            dbx = dropbox.Dropbox(
                oauth2_access_token=self.DROPBOX_OAUTH['access_token']
            )
            dbx.users_get_current_account()  # check if token is still valid
        except dropbox.exceptions.AuthError:
            logger.info(
                "Access token expired at: "
                f"{self.DROPBOX_OAUTH['expires_at']}. Refreshing..."
            )
            access_token = self.refresh_access_token()
            dbx = dropbox.Dropbox(oauth2_access_token=access_token)

        return dbx
