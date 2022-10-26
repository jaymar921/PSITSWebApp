using System.ComponentModel.DataAnnotations;

namespace PSITSWeb_ASP.NET.data.Models.Entity
{
    public class Account
    {
        [Required]
        public int Id { get; set; }
        public string RFID { get; set; }
        public string Firstname { get; set; }
        public string LastName { get; set; }
        public string Course { get; set; }
        public int Year { get; set; }
        [Required]
        [RegularExpression(@"^([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)$")]
        public string Email { get; set; }
        [Required]
        [StringLength(32, MinimumLength = 8)]
        public string Password { get; set; }
        public string Role { get; set; }
    }
}
