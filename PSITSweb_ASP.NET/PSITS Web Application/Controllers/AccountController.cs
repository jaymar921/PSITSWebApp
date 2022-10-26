using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Routing;
using PSITS_Web_Application.Models.Auth;
using PSITSWeb_ASP.NET.data.Models.Data;
using PSITSWeb_ASP.NET.data.Models.Entity;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace PSITS_Web_Application.Controllers
{
    [AllowAnonymous]
    public class AccountController: Controller
    {
        private readonly IDataRepository dataRepository;
        private readonly LinkGenerator linkGenerator;

        public AccountController(IDataRepository dataRepository, LinkGenerator linkGenerator)
        {
            this.dataRepository = dataRepository;
            this.linkGenerator = linkGenerator;
        }

        [AllowAnonymous]
        public IActionResult Login(string returnUrl = "/")
        {
            return View(new LoginModel { ReturnUrl = returnUrl });
        }

        [HttpPost]
        [AllowAnonymous]
        public async Task<IActionResult> Login(LoginModel model)
        {
            var user = dataRepository.GetAccountByUserAndPass(model.Username, model.Password);
            if (user == null)
            {
                if (dataRepository.GetAccountById(int.Parse(model.Username)) != null)
                    TempData["AccountInformation"] = "Invalid Password";
                else TempData["AccountInformation"] = "Account not found :/";
                return View();
            }
                


            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.LastName),
                new Claim(ClaimTypes.Role, user.Role),
                new Claim("RFID", user.RFID)
            };

            var identity = new ClaimsIdentity(claims,
                CookieAuthenticationDefaults.AuthenticationScheme);
            var principal = new ClaimsPrincipal(identity);

            await HttpContext.SignInAsync(
                CookieAuthenticationDefaults.AuthenticationScheme,
                principal,
                new AuthenticationProperties { IsPersistent = model.RememberLogin });

            return LocalRedirect(model.ReturnUrl);
        }

        public async Task<IActionResult> Logout()
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return Redirect("/");
        }

        [AllowAnonymous]
        public ActionResult Register()
        {
            return View();
        }

        [HttpPost]
        [AllowAnonymous]
        public ActionResult Register(Account account)
        {
            
            var oldAcc = dataRepository.GetAccountById(account.Id);
            if(oldAcc != null)
            {
                TempData["AccountInformation"] = "Account already exists!";
                return View();
            }

            if (!dataRepository.RegisterAccount(account))
            {
                TempData["AccountInformation"] = "Registration Failure";
                return View();
            }
            TempData["AccountInformation"] = "Account Created";

            return RedirectToAction("Login", "Account");
        }
    }
}
