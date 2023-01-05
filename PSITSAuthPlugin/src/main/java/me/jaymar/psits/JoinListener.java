package me.jaymar.psits;

import me.jaymar.psits.Data.Account;
import me.jaymar.psits.Data.DataHandler;
import me.jaymar.psits.Utils.StringUtility;
import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Location;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.scheduler.BukkitRunnable;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class JoinListener implements Listener {

    private List<String> UUIDS = new LinkedList<>();
    private Map<String, String> LOGGED_DATA = new HashMap<>();
    private final String CE3_CHAT_OVERRIDER = "§r";
    private boolean hasCE3 = false;

    public JoinListener(){
        if(Bukkit.getServer().getPluginManager().getPlugin("CustomEnchantments3") != null)
            hasCE3 = true;
    }
    @EventHandler
    private void OnJoin(PlayerJoinEvent event){
        event.setJoinMessage("");
        UUIDS.add(event.getPlayer().getUniqueId().toString());
        event.getPlayer().sendMessage(ChatColor.AQUA+"Welcome to PSITS MC Server!");
        event.getPlayer().sendMessage(ChatColor.YELLOW+"Please Enter your ID number: ");
        new BukkitRunnable(){
            private final Location location = event.getPlayer().getLocation().clone();
            private final String uuid = event.getPlayer().getUniqueId().toString();
            @Override
            public void run() {
                if(UUIDS.contains(uuid)){
                    event.getPlayer().teleport(location);
                    event.getPlayer().sendTitle(ChatColor.RED+"Account Login",ChatColor.BLUE+"Enter your ID number and Password", 0, 20, 5);
                }else {
                    cancel();
                }
            }
        }.runTaskTimer(PluginCore.getPlugin(PluginCore.class), 5, 5);
    }

    @EventHandler
    private void OnPlayerLeft(PlayerQuitEvent event){
        UUIDS.remove(event.getPlayer().getUniqueId().toString());
        LOGGED_DATA.remove(event.getPlayer().getUniqueId().toString());
    }

    @EventHandler
    private void OnChatEvent(AsyncPlayerChatEvent event){
        Player player = event.getPlayer();
        if(UUIDS.size() == 0)
            return;

        String uuid = player.getUniqueId().toString();
        if(UUIDS.contains(uuid)){
            event.setCancelled(true);

            String message = event.getMessage();

            if(hasCE3){
                try {
                    message = message.split(CE3_CHAT_OVERRIDER)[2];
                }catch (Exception ignore){}
            }

            if(LOGGED_DATA.containsKey(uuid)){
                String id = LOGGED_DATA.get(uuid);
                String password = message;

                for(Account account : DataHandler.AccountList){
                    if(String.valueOf(account.getID()).equals(id.trim())){
                        if(StringUtility.hashString(password).equals(account.getPassword())){
                            // welcome
                            UUIDS.remove(uuid);
                            Bukkit.getServer().getOnlinePlayers().forEach( players -> {
                                players.sendMessage(ChatColor.YELLOW+"Welcome "+ChatColor.AQUA+account.getName()+ChatColor.YELLOW+"!");
                            });
                            PluginCore.getPlugin(PluginCore.class).getLogger().info(account.getName()+" joined the server");
                            LOGGED_DATA.remove(uuid);
                            // rename the player
                            event.getPlayer().setDisplayName(account.getName());
                            event.getPlayer().setCustomName(account.getName());
                            event.getPlayer().sendMessage(ChatColor.GREEN + "Feel free to walk around, gather resources and build something!");
                        }else {
                            event.getPlayer().sendMessage(ChatColor.RED+"Invalid Password! Try again...");
                        }
                        return;
                    }
                }
                event.getPlayer().sendMessage(ChatColor.RED+"ID number not found! Enter your ID Again");
                LOGGED_DATA.remove(uuid);

            }else {
                LOGGED_DATA.put(uuid,message);
                event.getPlayer().sendMessage(ChatColor.YELLOW+"Please Enter your Password: ");
            }
        }
    }
}
