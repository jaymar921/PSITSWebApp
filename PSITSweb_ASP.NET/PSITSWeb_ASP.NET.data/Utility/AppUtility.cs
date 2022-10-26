using System.Security.Cryptography;
using System.Text;

namespace PSITSWeb_ASP.NET.data.Utility
{
    public class AppUtility
    {
    }

    public static class StringExtension
    {
        public static string HashMD5(this string str)
        {
            using (MD5 md5 = MD5.Create())
            {
                byte[] inputBytes = Encoding.ASCII.GetBytes(str);
                byte[] hashBytes = md5.ComputeHash(inputBytes);

                StringBuilder sb = new StringBuilder();

                for (int i = 0; i < hashBytes.Length; i++)
                {
                    sb.Append(hashBytes[i].ToString("X2"));
                }
                return sb.ToString();
            }
        }
    }
}
