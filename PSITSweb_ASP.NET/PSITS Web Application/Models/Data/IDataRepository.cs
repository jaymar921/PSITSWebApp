using PSITS_Web_Application.Models.Entity;
using System.Collections.Generic;

namespace PSITS_Web_Application.Models.Data
{
    public interface IDataRepository
    {
        IEnumerable<Account> GetAccounts();
        Account GetAccount(string search);
        Account GetAccount(int id_number, string password);

    }
}
