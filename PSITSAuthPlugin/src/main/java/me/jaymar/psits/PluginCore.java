package me.jaymar.psits;

import me.jaymar.psits.Data.DataHandler;
import me.jaymar.psits.Data.SQLConnector;
import me.jaymar.psits.Utils.StringUtility;
import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;

public final class PluginCore extends JavaPlugin {

    @Override
    public void onEnable() {
        // Plugin startup logic
        if(SQLConnector.Connected()){
            SQLConnector.LoadAccounts(DataHandler.AccountList);
            Bukkit.getServer().getPluginManager().registerEvents(new JoinListener(), this);
        }else {
            getLogger().info("Failed to connect to database");
        }
    }

    @Override
    public void onDisable() {
        // Plugin shutdown logic
    }
}
