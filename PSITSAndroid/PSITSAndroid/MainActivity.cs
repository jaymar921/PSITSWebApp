using Android.App;
using Android.OS;
using Android.Runtime;
using Android.Webkit;
using AndroidX.AppCompat.App;

namespace PSITSAndroid
{
    [Activity(Label = "@string/app_name", Theme = "@style/Theme.AppCompat.Light.NoActionBar", MainLauncher = true)]
    public class MainActivity : AppCompatActivity
    {
        WebView webView;
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);
            Xamarin.Essentials.Platform.Init(this, savedInstanceState);
            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.activity_main);
            webView = FindViewById<WebView>(Resource.Id.webview);
            //webView.Settings.JavaScriptEnabled = true;
            //webView.LoadUrl("https://203.177.71.218:5001");

            webView.SetWebViewClient(new InvalidWebViewClient());
            webView.LoadUrl("https://203.177.71.218:5001");
            // Not required for Invalid certificate, but required for my site.
            WebSettings ws = webView.Settings;
            ws.JavaScriptEnabled = true;
            ws.AllowFileAccess = true;
        }
        public override void OnRequestPermissionsResult(int requestCode, string[] permissions, [GeneratedEnum] Android.Content.PM.Permission[] grantResults)
        {
            Xamarin.Essentials.Platform.OnRequestPermissionsResult(requestCode, permissions, grantResults);

            base.OnRequestPermissionsResult(requestCode, permissions, grantResults);
        }
        public class InvalidWebViewClient : WebViewClient
        {
            public override void OnReceivedSslError(WebView view, SslErrorHandler handler, Android.Net.Http.SslError error)
            {
                handler.Proceed();
            }
        }
    }
}