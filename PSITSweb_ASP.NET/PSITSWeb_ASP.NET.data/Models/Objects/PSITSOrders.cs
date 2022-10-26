using PSITSWeb_ASP.NET.data.Models.Entity;
using System;

namespace PSITSWeb_ASP.NET.data.Models.Objects
{
    public class PSITSOrders
    {
        public int Id { get; set; }
        public Account Account { get; set; }
        public DateTime OrderDate { get; set; }
        public Merchandise Merchandise { get; set; }
        public string Status { get; set; }
        public int Quantity { get; set; }
        public string Details { get; set; }
        public string Reference { get; set; }
    }
}
