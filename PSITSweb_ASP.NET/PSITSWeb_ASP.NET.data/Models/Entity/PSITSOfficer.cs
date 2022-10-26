using PSITSWeb_ASP.NET.data.Models.Entity;

namespace PSITS_Web_Application.Models.Entity
{
    public class PSITSOfficer
    {
        public Account Account { get; set; }
        public string Position { get; set; }
        public string Birthday { get; set; }
        public string ImageUrl { get; set; }
    }
}
