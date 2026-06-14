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
SESSION_ONLY_TOKEN_PLAN = DOCS_PLANS / "2026-06-10-session-only-oauth-tokens.md"
PROVIDER_ERROR_LOG_PLAN = DOCS_PLANS / "2026-06-10-provider-error-log-redaction.md"
OAUTH_RESPONSE_FIELD_PLAN = DOCS_PLANS / "2026-06-12-oauth-response-field-parsing.md"
OAUTH_WHITESPACE_PLAN = DOCS_PLANS / "2026-06-13-oauth-whitespace-input-guards.md"
OAUTH_FIELD_UNIQUENESS_PLAN = DOCS_PLANS / "2026-06-13-oauth-response-field-uniqueness.md"
STALE_OAUTH_CALLBACK_PLAN = DOCS_PLANS / "2026-06-13-stale-oauth-callback-guards.md"
MAKE_ROOT_PROTECTION_PLAN = DOCS_PLANS / "2026-06-14-make-root-override-protection.md"
LEGACY_UNITY_SETUP_PLAN = DOCS_PLANS / "2026-06-14-legacy-unity-setup-notes.md"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "check.yml"


def fail(message):
    print(f"check_unity_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def workflow_step_block(workflow, action):
    lines = workflow.splitlines()
    prefix = f"- uses: {action}"

    for index, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line == prefix or stripped_line.startswith(f"{prefix} #"):
            indentation = len(line) - len(line.lstrip())
            block = [line]
            for following_line in lines[index + 1 :]:
                following_indentation = len(following_line) - len(following_line.lstrip())
                if following_line.strip() and following_indentation <= indentation:
                    break
                block.append(following_line)
            return "\n".join(block)

    raise AssertionError(f"CI workflow must define the {action} step")


def check_required_project_files():
    gitignore = read_text(".gitignore")
    require("__pycache__/" in gitignore, "Python bytecode cache directories must be ignored")
    require("*.py[cod]" in gitignore, "Python bytecode files must be ignored")

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


def check_legacy_unity_setup_notes():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    readme = read_text("README.md")

    require(
        not (ROOT / "UnityTwitter/ProjectSettings/ProjectVersion.txt").exists(),
        "an exact Unity version must not be claimed without reviewing a newly added ProjectVersion.txt",
    )
    require("public string CONSUMER_KEY;" in demo, "Demo must expose the local consumer key field")
    require("public string CONSUMER_SECRET;" in demo, "Demo must expose the local consumer secret field")
    require("WWW" in api, "historical setup notes must remain grounded in the legacy WWW transport")
    for phrase in [
        "`ProjectVersion.txt`",
        "Legacy Unity And API Boundary",
        "entered locally",
        "Access tokens remain session-only",
        "PIN-based OAuth",
        "explicit user-triggered status posting",
        "legacy `WWW` transport",
        "retired or unverified",
        "docs/plans/2026-06-14-legacy-unity-setup-notes.md",
    ]:
        require(phrase in readme, f"README.md must document {phrase}")
    require(
        "Keep legacy Unity setup, local credential, PIN OAuth" in read_text("VISION.md"),
        "VISION.md must preserve the legacy setup boundary",
    )
    require(
        "unpinned legacy Unity editor boundary" in read_text("CHANGES.md"),
        "CHANGES.md must record the legacy setup boundary",
    )


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


def check_session_only_oauth_tokens():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require("PlayerPrefs.GetString" not in demo, "demo must not load OAuth values from PlayerPrefs")
    require("PlayerPrefs.SetString" not in demo, "demo must not persist OAuth values in PlayerPrefs")
    require("ClearLegacyStoredCredentials();" in demo, "demo must clear legacy stored OAuth values on startup")
    require("PlayerPrefs.Save();" in demo, "demo must flush legacy OAuth value deletion")
    for key in [
        "PLAYER_PREFS_TWITTER_USER_ID",
        "PLAYER_PREFS_TWITTER_USER_SCREEN_NAME",
        "PLAYER_PREFS_TWITTER_USER_TOKEN",
        "PLAYER_PREFS_TWITTER_USER_TOKEN_SECRET",
    ]:
        require(f"PlayerPrefs.DeleteKey({key});" in demo, f"demo must delete legacy {key} storage")
    require("m_AccessTokenResponse = response;" in demo, "successful OAuth tokens must remain available in memory")


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


def check_api_provider_error_log_redaction():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    for dynamic_log in (
        'Debug.Log(string.Format("GetRequestToken - failed. error : {0}", web.error))',
        'Debug.Log(string.Format("GetAccessToken - failed. error : {0}", web.error))',
        'Debug.Log(string.Format("PostTweet - failed. {0}", web.error))',
        'Debug.Log(string.Format("PostTweet - failed. {0}", error))',
    ):
        require(dynamic_log not in api, "API failures must not log provider-controlled error details")

    for redacted_log in (
        "GetRequestToken - request failed.",
        "GetAccessToken - request failed.",
        "PostTweet - request failed.",
        "PostTweet - response reported an error.",
    ):
        require(redacted_log in api, f"API failure log is missing redacted message: {redacted_log}")


def check_oauth_response_field_parsing():
    api = read_text("UnityTwitter/Assets/Twitter.cs")

    for field in ["oauth_token", "oauth_token_secret", "user_id", "screen_name"]:
        require(
            f'Regex.Match(web.text, @"{field}=([^&]+)")' not in api,
            f"OAuth response field {field} must not use unanchored direct regex extraction",
        )
    for assignment in [
        'Token = FormValue(web.text, "oauth_token")',
        'TokenSecret = FormValue(web.text, "oauth_token_secret")',
        'UserId = FormValue(web.text, "user_id")',
        'ScreenName = FormValue(web.text, "screen_name")',
    ]:
        require(assignment in api, f"OAuth response parsing must include {assignment}")
    require(
        'MatchCollection matches = Regex.Matches(' in api,
        "OAuth response parser must collect all exact-key matches",
    )
    require(
        '@"(?:^|&)" + Regex.Escape(key) + @"=([^&]*)"' in api,
        "OAuth response parser must match exact form field names",
    )
    require("if (matches.Count != 1)" in api, "OAuth response fields must occur exactly once")
    require(
        'Uri.UnescapeDataString(matches[0].Groups[1].Value.Replace("+", " "))' in api,
        "OAuth response parser must decode form values",
    )
    require("catch (UriFormatException)" in api, "malformed OAuth response escaping must fail closed")

    duplicate_fixtures = {
        "oauth_token": "oauth_token=first&other=value&oauth_token=second",
        "oauth_token_secret": "oauth_token_secret=first&other=value&oauth_token_secret=second",
        "user_id": "user_id=first&other=value&user_id=second",
        "screen_name": "screen_name=first&other=value&screen_name=second",
    }
    require(
        set(duplicate_fixtures) == {"oauth_token", "oauth_token_secret", "user_id", "screen_name"},
        "duplicate OAuth response fixtures must cover every consumed field",
    )
    for field, fixture in duplicate_fixtures.items():
        matches = re.findall(r"(?:^|&)" + re.escape(field) + r"=([^&]*)", fixture)
        require(len(matches) == 2, f"duplicate fixture for {field} must remain ambiguous")


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
        "OAuthValueIsMissing(requestToken)" in api,
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
        "response == null" in api and "OAuthValueIsMissing(response.Token)" in api,
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
        "OAuthValueIsMissing(requestToken)" in preamble,
        "GetAccessToken must guard missing request-token values before signing",
    )
    require(
        "OAuthValueIsMissing(pin)" in preamble,
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
        r"(?P<preamble>.*?)if \(OAuthValueIsMissing\(requestToken\)",
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


def check_oauth_whitespace_input_guards():
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    helper = (
        "private static bool OAuthValueIsMissing(string value)",
        "string.IsNullOrEmpty(value) || value.Trim().Length == 0",
    )
    for contract in helper:
        require(contract in api, f"OAuth whitespace guard is missing: {contract}")

    guarded_values = (
        "OAuthValueIsMissing(consumerKey)",
        "OAuthValueIsMissing(consumerSecret)",
        "OAuthValueIsMissing(requestToken)",
        "OAuthValueIsMissing(pin)",
        "OAuthValueIsMissing(response.Token)",
        "OAuthValueIsMissing(response.TokenSecret)",
        "OAuthValueIsMissing(response.UserId)",
        "OAuthValueIsMissing(response.ScreenName)",
    )
    for contract in guarded_values:
        require(contract in api, f"OAuth input must reject whitespace-only values: {contract}")

    empty_only_guards = (
        "string.IsNullOrEmpty(consumerKey)",
        "string.IsNullOrEmpty(consumerSecret)",
        "string.IsNullOrEmpty(requestToken)",
        "string.IsNullOrEmpty(pin)",
        "string.IsNullOrEmpty(response.Token)",
        "string.IsNullOrEmpty(response.TokenSecret)",
        "string.IsNullOrEmpty(response.UserId)",
        "string.IsNullOrEmpty(response.ScreenName)",
    )
    for contract in empty_only_guards:
        require(contract not in api, f"OAuth input must not use an empty-only guard: {contract}")

    require(
        api.index("if (OAuthValueIsMissing(requestToken))")
        < api.index("Application.OpenURL(string.Format(AuthorizationURL"),
        "request-token whitespace guard must precede browser authorization",
    )
    require(
        api.index("if (OAuthValueIsMissing(requestToken) || OAuthValueIsMissing(pin))")
        < api.index("WWW web = WWWAccessToken"),
        "request-token and PIN whitespace guards must precede access-token exchange",
    )


def check_stale_oauth_callback_guards():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    contracts = (
        "private int m_RequestTokenGeneration;",
        "private int m_AccessTokenGeneration;",
        "int requestTokenGeneration = ++m_RequestTokenGeneration;",
        "OnRequestTokenCallback(requestTokenGeneration, success, response)",
        "int accessTokenGeneration = ++m_AccessTokenGeneration;",
        "OnAccessTokenCallback(accessTokenGeneration, success, response)",
        "if (requestTokenGeneration != m_RequestTokenGeneration)",
        "if (accessTokenGeneration != m_AccessTokenGeneration)",
        "string requestToken = m_RequestTokenResponse.Token;",
        "if (success && response != null)",
    )
    for contract in contracts:
        require(contract in demo, f"stale OAuth callback contract is missing: {contract}")

    require(
        demo.count("m_RequestTokenResponse = null;") >= 3,
        "request-token state must clear on replacement, consumption, and failure",
    )
    require(
        demo.count("m_AccessTokenResponse = new AccessTokenResponse();") >= 4,
        "access-token state must clear on startup, replacement, exchange, and failure",
    )
    replacement_start = demo.index("if (GUI.Button(rect, text))")
    request_launch = demo.index("API.GetRequestToken", replacement_start)
    require(
        replacement_start
        < demo.index("m_RequestTokenResponse = null;", replacement_start)
        < demo.index("m_AccessTokenResponse = new AccessTokenResponse();", replacement_start)
        < demo.index("m_AccessTokenGeneration++;", replacement_start)
        < demo.index("int requestTokenGeneration = ++m_RequestTokenGeneration;", replacement_start)
        < request_launch,
        "replacement auth state must clear and invalidate before request-token launch",
    )
    token_copy = demo.index("string requestToken = m_RequestTokenResponse.Token;")
    access_launch = demo.index("API.GetAccessToken", token_copy)
    require(
        token_copy
        < demo.index("m_RequestTokenResponse = null;", token_copy)
        < demo.index("m_RequestTokenGeneration++;", token_copy)
        < demo.index("m_AccessTokenResponse = new AccessTokenResponse();", token_copy)
        < demo.index("int accessTokenGeneration = ++m_AccessTokenGeneration;", token_copy)
        < access_launch,
        "request tokens must be copied, consumed, and generation-bound before exchange",
    )
    require(
        demo.index("if (requestTokenGeneration != m_RequestTokenGeneration)")
        < demo.index("m_RequestTokenResponse = response;"),
        "request-token callbacks must reject stale generations before state assignment",
    )
    require(
        demo.index("if (accessTokenGeneration != m_AccessTokenGeneration)")
        < demo.index("m_AccessTokenResponse = response;"),
        "access-token callbacks must reject stale generations before state assignment",
    )

    documentation = {
        "README.md": "OAuth callback generations",
        "SECURITY.md": "superseded OAuth callbacks",
        "VISION.md": "Ignore superseded OAuth callbacks",
        "CHANGES.md": "Ignored superseded OAuth callbacks",
    }
    for relative_path, phrase in documentation.items():
        require(phrase in read_text(relative_path), f"{relative_path} must document stale OAuth callback guards")


def check_ci_workflow():
    workflow = read_text(".github/workflows/check.yml")
    checkout_action = "actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10"
    for fragment in [
        "permissions:\n  contents: read",
        "timeout-minutes: 10",
        "runs-on: ubuntu-24.04",
        "concurrency:",
        "cancel-in-progress: true",
        'python-version: ["3.10", "3.12", "3.14"]',
        checkout_action,
        "actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405",
        "persist-credentials: false",
        "workflow_dispatch:",
        "make check",
    ]:
        require(fragment in workflow, f"CI workflow must include {fragment}")
    require("@v" not in workflow, "CI actions must use immutable commits")
    require("ubuntu-latest" not in workflow, "CI workflow must not use a floating Ubuntu runner")
    require("# v6.0.3" in workflow, "checkout pin annotation must identify the exact release")
    require("# v6.2.0" in workflow, "setup-python pin annotation must identify the exact release")
    require(workflow.count("actions/checkout@") == 1, "CI workflow must define exactly one checkout action")
    require(workflow.count("actions/setup-python@") == 1, "CI workflow must define exactly one setup-python action")
    require(workflow.count("persist-credentials:") == 1, "checkout credential persistence must be configured once")
    require("persist-credentials: true" not in workflow, "checkout credentials must not persist")
    checkout_step = workflow_step_block(workflow, checkout_action)
    require(
        "\n        with:\n          persist-credentials: false" in checkout_step,
        "checkout step must disable credential persistence in its with block",
    )

    makefile = read_text("Makefile")
    makefile_lines = set(makefile.splitlines())
    require(
        "override ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))" in makefile_lines,
        "Makefile must protect commands rooted at the repository",
    )
    require("PYTHON ?= python3" in makefile_lines, "Makefile must preserve the Python command override")
    require('"$(ROOT)/scripts/check_unity_contracts.py"' in makefile, "Makefile must use the rooted checker path")
    require('"$(ROOT)/UnityTwitter"' in makefile, "Makefile must use the rooted Unity project path")

    documentation_contracts = {
        "README.md": "GitHub Actions runs the same `make check` static baseline",
        "SECURITY.md": "GitHub Actions runs the static `make check` baseline",
        "VISION.md": "Keep the static `make check` baseline running in GitHub Actions",
        "CHANGES.md": "Added a pinned, read-only GitHub Actions matrix",
        "docs/plans/2026-06-10-ci-baseline.md": "Added read-only GitHub Actions checks",
    }
    for relative_path, fragment in documentation_contracts.items():
        require(fragment in read_text(relative_path), f"{relative_path} must document the GitHub Actions baseline")


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")
    require(CONSUMER_CREDENTIAL_PLAN in plans, f"{CONSUMER_CREDENTIAL_PLAN.relative_to(ROOT)} must be present")
    require(TWEET_TEXT_LOG_PLAN in plans, f"{TWEET_TEXT_LOG_PLAN.relative_to(ROOT)} must be present")
    require(ACCOUNT_IDENTIFIER_LOG_PLAN in plans, f"{ACCOUNT_IDENTIFIER_LOG_PLAN.relative_to(ROOT)} must be present")
    require(CI_PLAN in plans, f"{CI_PLAN.relative_to(ROOT)} must be present")
    require(SESSION_ONLY_TOKEN_PLAN in plans, f"{SESSION_ONLY_TOKEN_PLAN.relative_to(ROOT)} must be present")
    require(PROVIDER_ERROR_LOG_PLAN in plans, f"{PROVIDER_ERROR_LOG_PLAN.relative_to(ROOT)} must be present")
    require(
        OAUTH_RESPONSE_FIELD_PLAN in plans,
        f"{OAUTH_RESPONSE_FIELD_PLAN.relative_to(ROOT)} must be present",
    )
    require(OAUTH_WHITESPACE_PLAN in plans, f"{OAUTH_WHITESPACE_PLAN.relative_to(ROOT)} must be present")
    require(
        OAUTH_FIELD_UNIQUENESS_PLAN in plans,
        f"{OAUTH_FIELD_UNIQUENESS_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        STALE_OAUTH_CALLBACK_PLAN in plans,
        f"{STALE_OAUTH_CALLBACK_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        MAKE_ROOT_PROTECTION_PLAN in plans,
        f"{MAKE_ROOT_PROTECTION_PLAN.relative_to(ROOT)} must be present",
    )
    require(
        LEGACY_UNITY_SETUP_PLAN in plans,
        f"{LEGACY_UNITY_SETUP_PLAN.relative_to(ROOT)} must be present",
    )

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = [
        check_required_project_files,
        check_runtime_urls_are_https,
        check_legacy_unity_setup_notes,
        check_bug_note_status,
        check_demo_token_logging,
        check_demo_account_identifier_logging,
        check_session_only_oauth_tokens,
        check_api_oauth_response_log_redaction,
        check_api_provider_error_log_redaction,
        check_oauth_response_field_parsing,
        check_oauth_nonce_entropy,
        check_authorization_url_token_safety,
        check_demo_access_flow_guards,
        check_access_token_exchange_guards,
        check_api_consumer_credential_guards,
        check_oauth_whitespace_input_guards,
        check_stale_oauth_callback_guards,
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
