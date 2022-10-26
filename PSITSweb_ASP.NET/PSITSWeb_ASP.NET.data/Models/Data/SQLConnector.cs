using Microsoft.Extensions.Configuration;
using MySql.Data.MySqlClient;
using System;
using System.Threading.Tasks;

namespace PSITSWeb_ASP.NET.data.Models.Data
{
    public class SQLConnector
    {
        private readonly string connStr;

        public SQLConnector(IConfiguration configuration)
        {
            bool debug;
            bool.TryParse(configuration["Environment:Development"], out debug);

            if (debug)
                connStr = configuration.GetConnectionString("PSITSwebDebugging");
            else
                connStr = configuration.GetConnectionString("PSITSweb");

        }
        public MySqlConnection GetConnection()
        {
            return new MySqlConnection(connStr);
        }

        public bool IsConnected()
        {
            try
            {
                using var conn = GetConnection();
                conn.Open();
                return true;
            }
            catch (Exception)
            {
                return false;
            }
        }

        // Must be disposed
        public MySqlDataReader ExecuteQueryReturn(string query)
        {
            var conn = GetConnection();
            conn.Open();
            return new MySqlCommand(query, conn).ExecuteReader();
        }

        public async Task<MySqlDataReader> ExecuteQueryReturnAsync(string query)
        {
            var conn = GetConnection();
            conn.Open();
            MySqlCommand sqlCommand = new MySqlCommand(query, conn);
            return (MySqlDataReader)await sqlCommand.ExecuteReaderAsync();
        }

        // Must be disposed
        public void ExecuteQuery(string query)
        {
            if (!IsConnected())
                return;
            var conn = GetConnection();
            conn.Open();
            new MySqlCommand(query, conn).ExecuteNonQuery();
        }

    }
}
