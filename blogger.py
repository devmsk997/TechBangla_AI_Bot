import json
import os
import html as html_lib
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/blogger"
]


try:
    from config import BLOG_ID
except (ImportError, AttributeError):
    BLOG_ID = os.environ.get("BLOG_ID", "")


def _read_json(path):
    file_path = Path(path)

    if not file_path.exists():
        return {}

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def _get_credentials():
    """
    Load OAuth credentials from token.json.

    IMPORTANT:
    GitHub Actions is headless, so this function NEVER
    tries to open a browser or run an interactive OAuth flow.
    """

    token_data = _read_json(TOKEN_FILE)

    if not token_data:
        raise RuntimeError(
            "token.json was not created. "
            "Check the TOKEN_JSON GitHub secret."
        )

    client_data = _read_json(CREDENTIALS_FILE)

    oauth_config = (
        client_data.get("installed")
        or client_data.get("web")
        or {}
    )

    token = token_data.get("token")

    refresh_token = token_data.get(
        "refresh_token"
    )

    client_id = (
        token_data.get("client_id")
        or oauth_config.get("client_id")
    )

    client_secret = (
        token_data.get("client_secret")
        or oauth_config.get("client_secret")
    )

    token_uri = (
        token_data.get("token_uri")
        or oauth_config.get("token_uri")
        or "https://oauth2.googleapis.com/token"
    )

    scopes = (
        token_data.get("scopes")
        or SCOPES
    )

    if isinstance(scopes, str):
        scopes = [scopes]

    if not client_id:
        raise RuntimeError(
            "Google OAuth client_id is missing."
        )

    if not client_secret:
        raise RuntimeError(
            "Google OAuth client_secret is missing."
        )

    if not token and not refresh_token:
        raise RuntimeError(
            "TOKEN_JSON does not contain a usable "
            "access token or refresh token."
        )

    creds = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri=token_uri,
        client_id=client_id,
        client_secret=client_secret,
        scopes=scopes,
    )

    # GitHub Actions must never open a browser.
    # Refresh the OAuth access token directly.
    if refresh_token:
        try:
            creds.refresh(Request())

            # Update only the temporary runtime token.json.
            Path(TOKEN_FILE).write_text(
                creds.to_json(),
                encoding="utf-8"
            )

            print(
                "Google OAuth token refreshed successfully."
            )

        except Exception as exc:
            raise RuntimeError(
                "Google OAuth token refresh failed: "
                f"{exc}"
            ) from exc

    if not creds.token:
        raise RuntimeError(
            "Google OAuth access token is unavailable."
        )

    return creds


def _get_blogger_service():
    creds = _get_credentials()

    return build(
        "blogger",
        "v3",
        credentials=creds,
        cache_discovery=False,
    )


def _get_blog_id(service):
    """
    Use BLOG_ID from runtime config when available.
    Otherwise automatically discover the Blogger blog.
    """

    configured_blog_id = str(
        BLOG_ID or ""
    ).strip()

    if configured_blog_id:
        return configured_blog_id

    response = (
        service
        .blogs()
        .listByUser(
            userId="self"
        )
        .execute()
    )

    blogs = response.get(
        "items",
        []
    )

    if not blogs:
        raise RuntimeError(
            "No Blogger blog was found for "
            "the authorized Google account."
        )

    # Prefer a TechBangla blog if available.
    for blog in blogs:
        name = str(
            blog.get("name", "")
        ).lower()

        url = str(
            blog.get("url", "")
        ).lower()

        if (
            "techbangla" in name
            or "techbangla" in url
        ):
            return str(blog["id"])

    # If only one blog exists, use it.
    if len(blogs) == 1:
        return str(
            blogs[0]["id"]
        )

    names = ", ".join(
        str(
            blog.get(
                "name",
                "(unnamed)"
            )
        )
        for blog in blogs
    )

    raise RuntimeError(
        "Multiple Blogger blogs were found, "
        "but TechBangla could not be identified: "
        + names
    )


def create_post(
    title,
    content,
    labels=None,
    search_description="",
    image_url=None,
):
    """
    Publish one post to Blogger without interactive OAuth.
    """

    print(
        "Connecting to Blogger API..."
    )

    service = _get_blogger_service()

    blog_id = _get_blog_id(
        service
    )

    print(
        f"Blogger Blog ID ready: {blog_id}"
    )

    final_content = (
        content or ""
    )

    # Add featured image to top of Blogger article.
    if image_url:
        safe_image_url = html_lib.escape(
            str(image_url),
            quote=True
        )

        safe_title = html_lib.escape(
            str(title),
            quote=True
        )

        image_html = f"""
        <div class="separator"
             style="clear: both; text-align: center;">
          <img
            src="{safe_image_url}"
            alt="{safe_title}"
            style="max-width:100%;height:auto;"
          />
        </div>
        """

        final_content = (
            image_html
            + "\n"
            + final_content
        )

    clean_labels = []

    for label in labels or []:
        label = str(
            label
        ).strip()

        if label:
            clean_labels.append(
                label
            )

    post_body = {
        "kind": "blogger#post",
        "title": str(title),
        "content": final_content,
    }

    if clean_labels:
        post_body[
            "labels"
        ] = clean_labels

    print(
        "Publishing article to Blogger..."
    )

    result = (
        service
        .posts()
        .insert(
            blogId=blog_id,
            body=post_body,
            isDraft=False,
        )
        .execute()
    )

    post_url = result.get(
        "url",
        ""
    )

    post_id = result.get(
        "id",
        ""
    )

    print(
        "Blogger post published successfully."
    )

    print(
        "Post ID:",
        post_id
    )

    print(
        "Post URL:",
        post_url
    )

    return result
