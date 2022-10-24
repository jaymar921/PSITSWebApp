using Microsoft.Extensions.Configuration;
using MySql.Data.MySqlClient;
using System;

namespace PSITS_Web_Application.Models.Data
{
    public class SQLConnector
    {
        private readonly string connStr;

        public SQLConnector(IConfiguration configuration)
        {
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
            catch(Exception)
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
