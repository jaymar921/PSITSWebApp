using System;

namespace PSITS_Web_Application.Models.Objects
{
    public class Announcements
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public DateTime PublishedDate { get; set; }
        public string Content { get; set; }
    }
}
