using PSITSWeb_ASP.NET.data.Models.Entity;
using PSITSWeb_ASP.NET.data.Models.Objects;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace PSITSWeb_ASP.NET.data.Models.Data
{
    public interface IDataRepository
    {
        IEnumerable<Account> GetAllAccounts();
        Account GetAccount(string search);
        Account GetAccountById(int id);
        Account GetAccountByUserAndPass(string user, string pass);
        Task<IEnumerable<Announcement>> GetAllAnnouncementsAsync();
        bool RegisterAccount(Account account);

    }
}
