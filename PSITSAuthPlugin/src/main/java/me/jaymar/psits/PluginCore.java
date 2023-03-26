package me.jaymar.psits;

import me.jaymar.psits.Data.DataHandler;
import me.jaymar.psits.Data.PlayerInventory;
import me.jaymar.psits.Data.SQLConnector;
import org.bukkit.Bukkit;
import org.bukkit.configuration.serialization.ConfigurationSerialization;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.LinkedList;
import java.util.List;

public final class PluginCore extends JavaPlugin {

    private static PlayerInventoryConfig inventoryConfig;
    public static List<PlayerInventory> playerInventories = new LinkedList<>();
    @Override
    public void onEnable() {
        // Plugin startup logic
        PluginCore.inventoryConfig = new PlayerInventoryConfig(this);

        // register the classes
        ConfigurationSerialization.registerClass(PlayerInventory.class);
        // load the data
        playerInventories = (List<PlayerInventory>) inventoryConfig.getConfig().getList("PlayerData");
        if(playerInventories == null)
            playerInventories = new LinkedList<>();
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
        inventoryConfig.getConfig().set("PlayerData", playerInventories);
        inventoryConfig.saveConfig();
    }

}
