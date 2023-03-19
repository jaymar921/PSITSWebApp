package me.jaymar.psits.Data;

import me.jaymar.psits.PluginCore;
import org.bukkit.Bukkit;
import org.bukkit.entity.Player;

import java.sql.*;
import java.util.List;

public class SQLConnector {
    String url = "jdbc:mysql://127.0.0.1:3306/psitswebapp";
    String username = "root";
    String password = "root";

    public SQLConnector(){

    }

    public Connection Connect(){
        Connection connection;
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            connection = DriverManager.getConnection(url, username, password);
        } catch (SQLException e) {
            return null;
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        return connection;
    }

    public static boolean Connected(){
        return new SQLConnector().Connect() != null;
    }

    public static void LoadAccounts(List<Account> accountsList){
        try{
            // get the connection
            Connection connection = new SQLConnector().Connect();
            if(connection == null)
                throw new Exception("Failed to connect to database");
            String query = "select * from accounts";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(query);

            while(resultSet.next()) {
                Account account = new Account(resultSet.getString(3) + " " + resultSet.getString(4), resultSet.getInt(1), resultSet.getString(8));
                accountsList.add(account);
            }

            //PluginCore.getPlugin(PluginCore.class).getLogger().info("Loaded "+accountsList.size() + " Accounts");

        }catch (Exception error){
            PluginCore.getPlugin(PluginCore.class).getLogger().info(error.getMessage());
        }
    }

    public static void UpdateUserCount(){
        try{
            // get the connection
            Connection connection = new SQLConnector().Connect();
            if(connection == null)
                throw new Exception("Failed to connect to database");
            int onlinePlayers = Bukkit.getOnlinePlayers().size();
            String names = "";
            for(Player p : Bukkit.getOnlinePlayers()){
                names += p.getCustomName() + ",";
            }
            try{
                String query = "insert into `psits_mcs` values(?,?,?)";
                PreparedStatement statement = connection.prepareStatement(query);
                statement.setInt(1, 1);
                statement.setInt(2, onlinePlayers);
                statement.setString(3, names);
                statement.executeUpdate();
            }catch (Exception e){
                String query = "update `psits_mcs` set users="+onlinePlayers+", names='"+names+"' where id=1";
                Statement statement = connection.createStatement();
                statement.executeUpdate(query);
            }

        }catch (Exception error){
            PluginCore.getPlugin(PluginCore.class).getLogger().info(error.getMessage());
        }
    }
}
