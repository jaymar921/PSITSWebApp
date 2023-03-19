package me.jaymar.psits;

import me.jaymar.psits.Data.DataHandler;
import me.jaymar.psits.Data.SQLConnector;
import org.bukkit.Bukkit;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;

public final class PluginCore extends JavaPlugin {

    @Override
    public void onEnable() {
        // Plugin startup logic
        if(SQLConnector.Connected()){
            new BukkitRunnable(){
                @Override
                public void run(){
                    DataHandler.AccountList.clear();
                    SQLConnector.LoadAccounts(DataHandler.AccountList);
                }
            }.runTaskTimer(this, 10, 20*60*5);
            new BukkitRunnable(){
                @Override
                public void run(){
                    SQLConnector.UpdateUserCount();
                }
            }.runTaskTimer(this, 10, 20*60);
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
