using System;
using System.IO;
using Kerberos.NET;
using Kerberos.NET.Entities;

namespace KrbConverter
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string base64Kirbi = @"PUT_YOUR_BASE64_HERE";
            string outputPath = @"C:\Users\pliu\ccache_pliu";

            try
            {
                Console.WriteLine("[*] Decode Base64...");
                byte[] kirbiBytes = Convert.FromBase64String(
                    base64Kirbi.Replace("\r", "").Replace("\n", "").Trim()
                );

                Console.WriteLine("[*] Parse KRB-CRED...");
                KrbCred cred = KrbCred.DecodeApplication(kirbiBytes);

                Console.WriteLine("[*] Convert credential...");
                KerberosCredential kerberosCred = new KerberosCredential(cred);

                Console.WriteLine("[*] Create ccache...");
                var cache = new Krb5CredentialCache();
                cache.Add(kerberosCred);

                File.WriteAllBytes(outputPath, cache.Serialize());

                Console.WriteLine("[+] Success: " + outputPath);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.ToString());
            }
        }
    }
}