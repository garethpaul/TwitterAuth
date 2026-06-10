#!/usr/bin/env python3
"""Static verification for the legacy Unity TwitterAuth sample."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-twitterauth-baseline.md"
CONSUMER_CREDENTIAL_PLAN = DOCS_PLANS / "2026-06-09-consumer-credential-guards.md"
TWEET_TEXT_LOG_PLAN = DOCS_PLANS / "2026-06-09-tweet-text-log-redaction.md"
ACCOUNT_IDENTIFIER_LOG_PLAN = DOCS_PLANS / "2026-06-09-account-identifier-log-redaction.md"
CI_PLAN = DOCS_PLANS / "2026-06-10-ci-baseline.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"


def fail(message):
    print(f"check_unity_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_required_project_files():
    for relative_path in [
        "UnityTwitter/Assets/Demo.cs",
        "UnityTwitter/Assets/Twitter.cs",
        "UnityTwitter/Assets/Demo.unity",
        "UnityTwitter/ProjectSettings/ProjectSettings.asset",
        ".github/workflows/check.yml",
        "docs/readme-overview.svg",
        "docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md",
    ]:
        require((ROOT / relative_path).exists(), f"{relative_path} must stay checked in")

    ET.parse(ROOT / "docs/readme-overview.svg")


def check_runtime_urls_are_https():
    for path in (ROOT / "UnityTwitter/Assets").glob("*.cs"):
        source = path.read_text(encoding="utf-8")
        require(
            not re.search(r'Application\.OpenURL\("http://', source),
            f"{path.relative_to(ROOT)} must not open plain HTTP URLs at runtime",
        )
        require(
            not re.search(r'new WWW\("http://', source),
            f"{path.relative_to(ROOT)} must not call plain HTTP URLs at runtime",
        )

    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require("https://dev.twitter.com/apps/new" in demo, "registration URL must use HTTPS")


def check_bug_note_status():
    bug = read_text("docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md")
    require("Status: Fixed" in bug, "plain HTTP bug note must record the fix status")
    require("https://dev.twitter.com/apps/new" in bug, "bug note must point to the HTTPS endpoint")


def check_demo_token_logging():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require('"\\n    Token : " +' not in demo, "demo must not log access or request tokens")
    require('"\\n    TokenSecret : " +' not in demo, "demo must not log token secrets")
    require("Token : <redacted>" in demo, "demo logs must redact token values")
    require("TokenSecret : <redacted>" in demo, "demo logs must redact token secret values")


def check_demo_account_identifier_logging():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require('"\\n    UserId : " +' not in demo, "demo must not log Twitter user IDs")
    require('"\\n    ScreenName : " +' not in demo, "demo must not log Twitter screen names")
    require("UserId : <redacted>" in demo, "demo logs must redact Twitter user IDs")
    require("ScreenName : <redacted>" in demo, "demo logs must redact Twitter screen names")


def check_api_oauth_response_log_redaction():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    require(
        'Debug.Log(string.Format("GetRequestToken - failed. response : {0}", web.text))' not in api,
        "request-token failures must not log raw OAuth response bodies",
    )
    require(
        'Debug.Log(string.Format("GetAccessToken - failed. response : {0}", web.text))' not in api,
        "access-token failures must not log raw OAuth response bodies",
    )
    require(
        "GetRequestToken - failed. response missing token fields." in api,
        "request-token parse failures must use a redacted missing-field message",
    )
    require(
        "GetAccessToken - failed. response missing token fields." in api,
        "access-token parse failures must use a redacted missing-field message",
    )


def check_oauth_nonce_entropy():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    require(
        "new System.Random()" not in api,
        "OAuth nonce generation must not use predictable System.Random",
    )
    require(
        "RNGCryptoServiceProvider" in api,
        "OAuth nonce generation must use cryptographic randomness",
    )
    require(
        "byte[] nonceBytes" in api,
        "OAuth nonce generation must draw random nonce bytes before formatting",
    )
    require(
        'BitConverter.ToString(nonceBytes).Replace("-", string.Empty)' in api,
        "OAuth nonce generation must format random bytes without separators",
    )


def check_authorization_url_token_safety():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    require(
        "string.IsNullOrEmpty(requestToken)" in api,
        "OpenAuthorizationPage must guard missing request-token values",
    )
    require(
        "OpenAuthorizationPage - request token is missing." in api,
        "OpenAuthorizationPage guard must log missing request-token state",
    )
    require(
        "string.Format(AuthorizationURL, UrlEncode(requestToken))" in api,
        "OpenAuthorizationPage must URL-encode request tokens",
    )
    require(
        "string.Format(AuthorizationURL, requestToken)" not in api,
        "OpenAuthorizationPage must not interpolate raw request-token values",
    )


def check_demo_access_flow_guards():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    require(
        "m_RequestTokenResponse != null" in demo,
        "PIN submission must guard missing request-token state",
    )
    require(
        "Request token is missing" in demo,
        "PIN submission guard must explain missing request-token state",
    )
    require(
        "m_AccessTokenResponse != null" in demo,
        "tweet submission must guard missing access-token state",
    )
    require(
        "Access token is missing" in demo,
        "tweet submission guard must explain missing access-token state",
    )
    require(
        "response == null" in api and "string.IsNullOrEmpty(response.Token)" in api,
        "PostTweet must guard missing access-token response before OAuth signing",
    )
    require(
        "PostTweet - access token is missing." in api,
        "PostTweet guard must log missing access-token state without secrets",
    )
    require(
        "yield break;" in api,
        "PostTweet guard must stop before building signed requests",
    )
    require(
        "PostTweet - text[{0}] is empty or too long." not in api,
        "PostTweet validation failures must not log tweet text",
    )
    require(
        "PostTweet - text is empty or too long." in api,
        "PostTweet validation failures must use a redacted text validation message",
    )


def check_access_token_exchange_guards():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    match = re.search(
        r"public static IEnumerator GetAccessToken\([^)]*\)\s*\{"
        r"(?P<preamble>.*?)WWW web = WWWAccessToken",
        api,
        re.DOTALL,
    )
    require(
        match,
        "GetAccessToken must validate inputs before building a signed request",
    )

    preamble = match.group("preamble")
    require(
        "string.IsNullOrEmpty(requestToken)" in preamble,
        "GetAccessToken must guard missing request-token values before signing",
    )
    require(
        "string.IsNullOrEmpty(pin)" in preamble,
        "GetAccessToken must guard missing PIN values before signing",
    )
    require(
        "GetAccessToken - request token or PIN is missing." in preamble,
        "GetAccessToken guard must log missing request-token or PIN state",
    )
    require(
        "callback(false, null);" in preamble and "yield break;" in preamble,
        "GetAccessToken guard must fail the callback and stop before building "
        "signed requests",
    )


def check_api_consumer_credential_guards():
    api = read_text("UnityTwitter/Assets/Twitter.cs")

    require(
        "private static bool ConsumerCredentialsAreMissing" in api,
        "API helpers must centralize missing consumer credential checks",
    )

    request_token_match = re.search(
        r"public static IEnumerator GetRequestToken\([^)]*\)\s*\{"
        r"(?P<preamble>.*?)WWW web = WWWRequestToken",
        api,
        re.DOTALL,
    )
    require(request_token_match, "GetRequestToken must guard before building a signed request")
    request_token_preamble = request_token_match.group("preamble")
    require(
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)" in request_token_preamble,
        "GetRequestToken must guard missing consumer credentials before signing",
    )
    require(
        "GetRequestToken - consumer credentials are missing." in request_token_preamble,
        "GetRequestToken guard must use a redacted credential-missing message",
    )
    require(
        "callback(false, null);" in request_token_preamble and "yield break;" in request_token_preamble,
        "GetRequestToken guard must fail the callback and stop before signing",
    )

    access_token_match = re.search(
        r"public static IEnumerator GetAccessToken\([^)]*\)\s*\{"
        r"(?P<preamble>.*?)if \(string\.IsNullOrEmpty\(requestToken\)",
        api,
        re.DOTALL,
    )
    require(access_token_match, "GetAccessToken must guard credentials before request-token checks")
    access_token_preamble = access_token_match.group("preamble")
    require(
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)" in access_token_preamble,
        "GetAccessToken must guard missing consumer credentials before signing",
    )
    require(
        "GetAccessToken - consumer credentials are missing." in access_token_preamble,
        "GetAccessToken guard must use a redacted credential-missing message",
    )
    require(
        "callback(false, null);" in access_token_preamble and "yield break;" in access_token_preamble,
        "GetAccessToken credential guard must fail the callback and stop before signing",
    )

    post_tweet_match = re.search(
        r"public static IEnumerator PostTweet\([^)]*\)\s*\{"
        r"(?P<preamble>.*?)if \(response == null",
        api,
        re.DOTALL,
    )
    require(post_tweet_match, "PostTweet must guard credentials before access-token checks")
    post_tweet_preamble = post_tweet_match.group("preamble")
    require(
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)" in post_tweet_preamble,
        "PostTweet must guard missing consumer credentials before signing",
    )
    require(
        "PostTweet - consumer credentials are missing." in post_tweet_preamble,
        "PostTweet guard must use a redacted credential-missing message",
    )
    require(
        "callback(false);" in post_tweet_preamble and "yield break;" in post_tweet_preamble,
        "PostTweet credential guard must fail the callback and stop before signing",
    )


def check_ci_workflow():
    workflow = read_text(".github/workflows/check.yml")
    for fragment in [
        "permissions:\n  contents: read",
        "timeout-minutes: 10",
        'python-version: ["3.10", "3.12", "3.14"]',
        "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10",
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "workflow_dispatch:",
        "make check",
    ]:
        require(fragment in workflow, f"CI workflow must include {fragment}")
    require("@v" not in workflow, "CI actions must use immutable commits")

    readme = read_text("README.md")
    require("GitHub Actions" in readme, "README must document the GitHub Actions check")


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")
    require(CONSUMER_CREDENTIAL_PLAN in plans, f"{CONSUMER_CREDENTIAL_PLAN.relative_to(ROOT)} must be present")
    require(TWEET_TEXT_LOG_PLAN in plans, f"{TWEET_TEXT_LOG_PLAN.relative_to(ROOT)} must be present")
    require(ACCOUNT_IDENTIFIER_LOG_PLAN in plans, f"{ACCOUNT_IDENTIFIER_LOG_PLAN.relative_to(ROOT)} must be present")
    require(CI_PLAN in plans, f"{CI_PLAN.relative_to(ROOT)} must be present")

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = [
        check_required_project_files,
        check_runtime_urls_are_https,
        check_bug_note_status,
        check_demo_token_logging,
        check_demo_account_identifier_logging,
        check_api_oauth_response_log_redaction,
        check_oauth_nonce_entropy,
        check_authorization_url_token_safety,
        check_demo_access_flow_guards,
        check_access_token_exchange_guards,
        check_api_consumer_credential_guards,
        check_ci_workflow,
        check_docs_plans,
    ]
    try:
        for check in checks:
            check()
    except (AssertionError, ET.ParseError) as exc:
        return fail(str(exc))

    print(f"Unity TwitterAuth contracts passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
