using PSITSWeb_ASP.NET.data.Models.Entity;
using PSITSWeb_ASP.NET.data.Models.Objects;
using PSITSWeb_ASP.NET.data.Utility;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace PSITSWeb_ASP.NET.data.Models.Data
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
            return GetAccount(search, "");
        }

        public Account GetAccountByUserAndPass(string user, string pass)
        {
            Account account = null;

            int idnum;
            Console.WriteLine($"user: {user} - pass: {pass}");
            if (!int.TryParse(user, out idnum))
                return null;

            string query = $"SELECT * FROM accounts where " +
                    $"idno = {idnum} and "+
                    $"password = '{pass.HashMD5()}'";
            Console.WriteLine($"query = {query}");
            using (var reader = connector.ExecuteQueryReturn(query))
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
                    setRole(account);
                }
                if (account != null)
                    return account;
                return GetAccountByRFIDAndPass(idnum, pass);
            }
        }

        public Account GetAccountByRFIDAndPass(int user, string pass)
        {
            Account account = null;


            string query = $"SELECT * FROM accounts where " +
                    $"rfid = {user} and " +
                    $"password = '{pass.HashMD5()}'";
            Console.WriteLine($"query = {query}");
            using (var reader = connector.ExecuteQueryReturn(query))
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
                    setRole(account);
                }
                if (account != null)
                    return account;
                return null;
            }
        }
        private Account GetAccount(string search, string password)
        {

            Account account = null;

            string query = $"SELECT * FROM accounts where " +
                $"firstname like '%{search}%' or " +
                $"lastname like '%{search}%' or " +
                $"course like '%{search}%' or " +
                $"email like '%{search}%'";

            int searchInt;
            if (int.TryParse(search, out searchInt))
                query = query + $"or idno = {searchInt} or " +
                    $"rfid = {searchInt} or " +
                    $"year = {searchInt}";

            if (!string.IsNullOrWhiteSpace(password))
                query = $"SELECT * FROM accounts where " +
                    $"idno = {searchInt} or " +
                    $"rfid = {searchInt} and " +
                    $"password = '{password.HashMD5()}'";

            using (var reader = connector.ExecuteQueryReturn(query))
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
                    setRole(account);
                }
                if (account != null)
                    return account;
                return new Account { };
            }


        }

        public Account GetAccountById(int id)
        {

            Account account = null;

            string query = $"SELECT * FROM accounts where " +
                $"idno = {id}";

            using (var reader = connector.ExecuteQueryReturn(query))
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
                    setRole(account);
                }
                if (account != null)
                    return account;
                return null;
            }


        }

        public IEnumerable<Account> GetAllAccounts()
        {
            throw new NotImplementedException();
        }

        private void setRole(Account account)
        {
            if (account.AUTHORIZED())
                account.Role = "ADMIN";
            else account.Role = "USER";
        }

        public async Task<IEnumerable<Announcement>> GetAllAnnouncementsAsync()
        {
            string query = "SELECT * FROM announcements";
            using (var reader = await connector.ExecuteQueryReturnAsync(query))
            {
                List<Announcement> announcements = new List<Announcement>();
                while (reader.Read())
                {
                    announcements.Add(
                        new Announcement
                        {
                            Id = (int)reader[0],
                            Title = (string)reader[1],
                            PublishedDate = (DateTime)reader[2],
                            Content = (string)reader[3]
                        }
                    );
                }
                return announcements;
            }
        }

        public bool RegisterAccount(Account account)
        {
            string query = $"INSERT INTO accounts values ({account.Id}, '{account.RFID}','{account.Firstname}','{account.LastName}','{account.Course}',{account.Year},'{account.Email}','{account.Password.HashMD5()}')";

            try
            {
                connector.ExecuteQuery(query);
                return true;
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                return false;
            }
        }
    }
}
