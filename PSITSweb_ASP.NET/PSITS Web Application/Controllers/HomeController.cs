using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using PSITS_Web_Application.Models;
using PSITS_Web_Application.ViewModels;
using PSITSWeb_ASP.NET.data.Models.Data;
using System.Diagnostics;
using System.Threading.Tasks;

namespace PSITS_Web_Application.Controllers
{

    [AllowAnonymous]
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
        private readonly IDataRepository dataRepository;

        public HomeController(ILogger<HomeController> logger, IDataRepository dataRepository)
        {
            _logger = logger;
            this.dataRepository = dataRepository;
        }

        public IActionResult Index()
        {
            
            return View(new HomeViewModel(dataRepository));
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
