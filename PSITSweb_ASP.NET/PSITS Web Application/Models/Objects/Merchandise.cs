namespace PSITS_Web_Application.Models.Objects
{
    public class Merchandise
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Information { get; set; }
        public decimal Price { get; set; }
        public decimal Discount { get; set; }
        public int Stock { get; set; }

        public bool IsAvailable() => Stock != 0;
    }
}
