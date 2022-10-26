using PSITSWeb_ASP.NET.data.Models.Entity;
using System;
using System.Collections.Generic;
using System.Text;

namespace PSITSWeb_ASP.NET.data.Models.Data
{
    internal static class AUTHORITIES
    {
        public static bool AUTHORIZED(this Account account)
        {
            IDictionary<string, string> admins = new Dictionary<string, string>
            {
                {"ABEJAR", "19889781"},
                {"RIBO", "19895283"},
                {"COLONIA", "20220885"},
                {"BELMONTE", "19871367"},
                {"SIERRA", "19889898"},
                {"ABELLANA", "21471909"},
                {"DUCAL", "19880152"},
                {"ANIBAN", "21496369"},
                {"CEMPRON", "19841998"},
                {"COSTILLAS", "21540950"},
                {"LEYROS", "21435474"},
                {"PADOLINA", "21400973"},
                {"DE LOS REYES", "19903483"},
                {"FLORENTINO", "18725242"},
                {"CUICO", "19888957"},
                {"OPINA", "19884253"},
                {"TIEMPO", "19924414"},
                {"SIR DD", "613000"},
                {"RACUYA", "19845262"}
            };
            foreach (var item in admins)
                if (item.Value == account.Id.ToString())
                    return true;
            return false;
        }
    }
}
