using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PSITS_Web_Application.Models.Auth
{
    public class LoginModel
    {
        public string Username { get; set; }
        public string Password { get; set; }
        public bool RememberLogin { get; set; }
        public string ReturnUrl { get; set; }
    }
}
