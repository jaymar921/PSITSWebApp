using PSITS_Web_Application.Models.Entity;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PSITS_Web_Application.Models.Data
{
    public class DataRepository : IDataRepository
    {
        private readonly SQLConnector connector;

        public DataRepository(SQLConnector connector)
        {
            this.connector = connector;
        }
        public Account GetAccount(string search)
        {

            Account account = null;

            string query = $"SELECT * FROM accounts where " +
                $"firstname like '%{search}%' or " +
                $"lastname like '%{search}%'";

            using(var reader = connector.ExecuteQueryReturn(query))
            {
                if (reader.Read())
                {
                    account = new Account
                    {
                        Id = (int)reader[0],
                        RFID = (string)reader[1],
                        Firstname = (string)reader[2],
                        LastName = (string)reader[3],
                        Course = (string)reader[4],
                        Year = (int)reader[5],
                        Email = (string)reader[6],
                        Password = (string)reader[7],
                    };
                }
                if (account != null)
                    return account;
                return new Account();
            }

            
        }

        public Account GetAccount(string username, string password)
        {
            throw new NotImplementedException();
        }

        public IEnumerable<Account> GetAccounts()
        {
            throw new NotImplementedException();
        }
    }
}
