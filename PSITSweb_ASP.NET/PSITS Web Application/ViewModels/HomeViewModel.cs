using PSITSWeb_ASP.NET.data.Models.Data;
using PSITSWeb_ASP.NET.data.Models.Objects;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PSITS_Web_Application.ViewModels
{
    public class HomeViewModel
    {
        private readonly IDataRepository dataRepository;

        public HomeViewModel(IDataRepository dataRepository)
        {
            this.dataRepository = dataRepository;
        }

        public async Task<IEnumerable<Announcement>> GetAnnouncementsAsync() => await dataRepository.GetAllAnnouncementsAsync();
    }
}
