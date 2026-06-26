using Twitter;
using UnityEngine;

public class Demo : MonoBehaviour
{
    // Legacy releases stored long-lived OAuth values in PlayerPrefs. Keep the
    // key names only so existing plaintext values can be removed on startup.
    private const string PLAYER_PREFS_TWITTER_USER_ID = "TwitterUserID";

    private const string PLAYER_PREFS_TWITTER_USER_SCREEN_NAME = "TwitterUserScreenName";
    private const string PLAYER_PREFS_TWITTER_USER_TOKEN = "TwitterUserToken";
    private const string PLAYER_PREFS_TWITTER_USER_TOKEN_SECRET = "TwitterUserTokenSecret";
    private const string PIN_PLACEHOLDER = "Please enter your PIN here.";
    public bool ALLOW_TWEET_POSTING;
    public string CONSUMER_KEY;
    public string CONSUMER_SECRET;
    public float PIN_ENTER_HEIGHT;
    public float PIN_ENTER_WIDTH;
    public float PIN_ENTER_X;
    public float PIN_ENTER_Y;
    public float PIN_INPUT_HEIGHT;
    public float PIN_INPUT_WIDTH;
    public float PIN_INPUT_X;
    public float PIN_INPUT_Y;
    public float POST_TWEET_HEIGHT;
    public float POST_TWEET_WIDTH;
    public float POST_TWEET_X;
    public float POST_TWEET_Y;
    public float TWEET_INPUT_HEIGHT;
    public float TWEET_INPUT_WIDTH;
    public float TWEET_INPUT_X;
    public float TWEET_INPUT_Y;
    public float USER_LOG_IN_HEIGHT;
    public float USER_LOG_IN_WIDTH;
    public float USER_LOG_IN_X;
    public float USER_LOG_IN_Y;

    private AccessTokenResponse m_AccessTokenResponse;
    private int m_AccessTokenGeneration;
    private int m_PostTweetGeneration;
    private bool m_PostTweetInFlight;

    private string m_PIN = PIN_PLACEHOLDER;
    private int m_RequestTokenGeneration;
    private RequestTokenResponse m_RequestTokenResponse;
    private string m_Tweet = "Please enter your tweet here.";

    // Use this for initialization
    private void Start()
    {
        ClearLegacyStoredCredentials();
        m_AccessTokenResponse = new AccessTokenResponse();
    }

    // Update is called once per frame
    private void Update()
    {
    }

    // GUI
    private void OnGUI()
    {
        // LogIn/Register Button
        var rect = new Rect(Screen.width * USER_LOG_IN_X,
            Screen.height * USER_LOG_IN_Y,
            Screen.width * USER_LOG_IN_WIDTH,
            Screen.height * USER_LOG_IN_HEIGHT);

        if (string.IsNullOrEmpty(CONSUMER_KEY) || string.IsNullOrEmpty(CONSUMER_SECRET))
        {
            string text =
                "You need to register your game or application first.\n Click this button, register and fill CONSUMER_KEY and CONSUMER_SECRET of Demo game object.";
            if (GUI.Button(rect, text))
            {
                Application.OpenURL("https://dev.twitter.com/apps/new");
            }
        }
        else
        {
            string text = string.Empty;

            if (!string.IsNullOrEmpty(m_AccessTokenResponse.ScreenName))
            {
                text = m_AccessTokenResponse.ScreenName + "\nClick to register with a different Twitter account";
            }
            else
            {
                text = "You need to register your game or application first.";
            }

            if (GUI.Button(rect, text))
            {
                m_RequestTokenResponse = null;
                m_AccessTokenResponse = new AccessTokenResponse();
                m_AccessTokenGeneration++;
                int requestTokenGeneration = ++m_RequestTokenGeneration;
                StartCoroutine(API.GetRequestToken(CONSUMER_KEY, CONSUMER_SECRET,
                    (success, response) => OnRequestTokenCallback(requestTokenGeneration, success, response)));
            }
        }

        // PIN Input
        rect.x = Screen.width * PIN_INPUT_X;
        rect.y = Screen.height * PIN_INPUT_Y;
        rect.width = Screen.width * PIN_INPUT_WIDTH;
        rect.height = Screen.height * PIN_INPUT_HEIGHT;

        m_PIN = GUI.TextField(rect, m_PIN);

        // PIN Enter Button
        rect.x = Screen.width * PIN_ENTER_X;
        rect.y = Screen.height * PIN_ENTER_Y;
        rect.width = Screen.width * PIN_ENTER_WIDTH;
        rect.height = Screen.height * PIN_ENTER_HEIGHT;

        if (GUI.Button(rect, "Enter PIN"))
        {
            if (m_RequestTokenResponse != null &&
                !string.IsNullOrEmpty(m_RequestTokenResponse.Token) &&
                PINIsReady(m_PIN))
            {
                string requestToken = m_RequestTokenResponse.Token;
                m_RequestTokenResponse = null;
                m_RequestTokenGeneration++;
                m_AccessTokenResponse = new AccessTokenResponse();
                int accessTokenGeneration = ++m_AccessTokenGeneration;
                StartCoroutine(API.GetAccessToken(CONSUMER_KEY, CONSUMER_SECRET, requestToken, m_PIN,
                    (success, response) => OnAccessTokenCallback(accessTokenGeneration, success, response)));
            }
            else
            {
                print("OnAccessTokenCallback - skipped. Request token or PIN is missing.");
            }
        }

        // Tweet Input
        rect.x = Screen.width * TWEET_INPUT_X;
        rect.y = Screen.height * TWEET_INPUT_Y;
        rect.width = Screen.width * TWEET_INPUT_WIDTH;
        rect.height = Screen.height * TWEET_INPUT_HEIGHT;

        if (!ALLOW_TWEET_POSTING)
        {
            GUI.Label(rect, "Authentication-only mode. Tweet posting is disabled.");
            return;
        }

        m_Tweet = GUI.TextField(rect, m_Tweet);

        // Post Tweet Button
        rect.x = Screen.width * POST_TWEET_X;
        rect.y = Screen.height * POST_TWEET_Y;
        rect.width = Screen.width * POST_TWEET_WIDTH;
        rect.height = Screen.height * POST_TWEET_HEIGHT;

        if (GUI.Button(rect, "Post Tweet"))
        {
            if (m_PostTweetInFlight)
            {
                print("OnPostTweet - skipped. A post is already in progress.");
            }
            else if (m_AccessTokenResponse != null &&
                !string.IsNullOrEmpty(m_AccessTokenResponse.Token) &&
                !string.IsNullOrEmpty(m_AccessTokenResponse.TokenSecret))
            {
                int postTweetGeneration = ++m_PostTweetGeneration;
                m_PostTweetInFlight = true;
                StartCoroutine(API.PostTweet(m_Tweet, CONSUMER_KEY, CONSUMER_SECRET, m_AccessTokenResponse,
                    success => OnPostTweet(postTweetGeneration, success)));
            }
            else
            {
                print("OnPostTweet - skipped. Access token is missing.");
            }
        }
    }

    private void ClearLegacyStoredCredentials()
    {
        PlayerPrefs.DeleteKey(PLAYER_PREFS_TWITTER_USER_ID);
        PlayerPrefs.DeleteKey(PLAYER_PREFS_TWITTER_USER_SCREEN_NAME);
        PlayerPrefs.DeleteKey(PLAYER_PREFS_TWITTER_USER_TOKEN);
        PlayerPrefs.DeleteKey(PLAYER_PREFS_TWITTER_USER_TOKEN_SECRET);
        PlayerPrefs.Save();
    }

    private static bool PINIsReady(string pin)
    {
        return !string.IsNullOrEmpty(pin) &&
               pin != PIN_PLACEHOLDER &&
               pin == pin.Trim();
    }

    private void OnDisable()
    {
        m_RequestTokenGeneration++;
        m_AccessTokenGeneration++;
        m_PostTweetGeneration++;
        m_PostTweetInFlight = false;
        m_RequestTokenResponse = null;
    }

    private void OnRequestTokenCallback(int requestTokenGeneration, bool success, RequestTokenResponse response)
    {
        if (requestTokenGeneration != m_RequestTokenGeneration)
        {
            return;
        }

        if (success && response != null)
        {
            string log = "OnRequestTokenCallback - succeeded";
            log += "\n    Token : <redacted>";
            log += "\n    TokenSecret : <redacted>";
            print(log);

            m_RequestTokenResponse = response;

            API.OpenAuthorizationPage(response.Token);
        }
        else
        {
            m_RequestTokenResponse = null;
            print("OnRequestTokenCallback - failed.");
        }
    }

    private void OnAccessTokenCallback(int accessTokenGeneration, bool success, AccessTokenResponse response)
    {
        if (accessTokenGeneration != m_AccessTokenGeneration)
        {
            return;
        }

        if (success && response != null)
        {
            string log = "OnAccessTokenCallback - succeeded";
            log += "\n    UserId : <redacted>";
            log += "\n    ScreenName : <redacted>";
            log += "\n    Token : <redacted>";
            log += "\n    TokenSecret : <redacted>";
            print(log);

            m_AccessTokenResponse = response;
        }
        else
        {
            m_AccessTokenResponse = new AccessTokenResponse();
            print("OnAccessTokenCallback - failed.");
        }
    }

    private void OnPostTweet(int postTweetGeneration, bool success)
    {
        if (postTweetGeneration != m_PostTweetGeneration)
        {
            return;
        }

        m_PostTweetInFlight = false;
        print("OnPostTweet - " + (success ? "succedded." : "failed."));
    }
}
