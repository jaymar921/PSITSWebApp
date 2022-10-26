using System;

namespace PSITSWeb_ASP.NET.data.Models.Objects
{
    public class Announcement
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public DateTime PublishedDate { get; set; }
        public string Content { get; set; }
    }
}
