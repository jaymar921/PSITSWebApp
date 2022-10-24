using System;

namespace PSITS_Web_Application.Models.Objects
{
    public class PSITSEvent
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public DateTime PublishedDate { get; set; }
        public string information { get; set; }
        public string ImgUrl { get; set; }
    }
}
