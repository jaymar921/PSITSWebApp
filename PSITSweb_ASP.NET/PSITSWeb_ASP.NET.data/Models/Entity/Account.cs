namespace PSITSWeb_ASP.NET.data.Models.Entity
{
    public class Account
    {
        public int Id { get; set; }
        public string RFID { get; set; }
        public string Firstname { get; set; }
        public string LastName { get; set; }
        public string Course { get; set; }
        public int Year { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
        public string Role { get; set; }
    }
}
