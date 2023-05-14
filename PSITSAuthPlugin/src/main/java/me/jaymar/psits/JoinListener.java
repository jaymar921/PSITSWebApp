package me.jaymar.psits;

import me.jaymar.psits.Data.APIConnector;
import me.jaymar.psits.Data.Account;
import me.jaymar.psits.Data.DataHandler;
import me.jaymar.psits.Data.PlayerInventory;
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
import org.bukkit.inventory.ItemStack;
import org.bukkit.potion.PotionEffect;
import org.bukkit.potion.PotionEffectType;
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
    private boolean hasSql = false;

    public JoinListener(boolean hasSql){
        if(Bukkit.getServer().getPluginManager().getPlugin("CustomEnchantments3") != null)
            hasCE3 = true;
        this.hasSql = hasSql;
    }
    @EventHandler
    private void OnJoin(PlayerJoinEvent event){
        event.setJoinMessage("");
        UUIDS.add(event.getPlayer().getUniqueId().toString());
        event.getPlayer().sendMessage(ChatColor.GREEN+"=+=+=+=+=+=+=+=+=+=+=+=+=+=+");
        event.getPlayer().sendMessage(ChatColor.AQUA+"Welcome to PSITS MC Server!");
        event.getPlayer().sendMessage(ChatColor.YELLOW+"Please Enter your ID number: ");

        new BukkitRunnable(){
            private final Location location = event.getPlayer().getLocation().clone();
            private final String uuid = event.getPlayer().getUniqueId().toString();
            @Override
            public void run() {
                if(UUIDS.contains(uuid)){
                    event.getPlayer().addPotionEffect(new PotionEffect(PotionEffectType.INVISIBILITY, 999, 2, false, false));
                    event.getPlayer().teleport(location);
                    event.getPlayer().sendTitle(ChatColor.RED+"PSITS Login",ChatColor.BLUE+"Enter your ID number and Password", 0, 20, 5);
                }else {
                    cancel();
                }
            }
        }.runTaskTimer(PluginCore.getPlugin(PluginCore.class), 5, 5);
    }

    @EventHandler
    private void OnPlayerLeft(PlayerQuitEvent event){
        PlayerInventory inventory = PlayerInventory.create(LOGGED_DATA.get(event.getPlayer().getUniqueId().toString()), event.getPlayer().getInventory().getContents(), event.getPlayer().getLocation());
        boolean found = false;
        for(PlayerInventory playerInventory : PluginCore.playerInventories){
            if(playerInventory == null) continue;
            if(playerInventory.uuid.equals(inventory.uuid)){
                found = true;
                playerInventory.inventoryData = inventory.inventoryData;
                playerInventory.locationData = inventory.locationData;
                break;
            }
        }

        if(!found)
            PluginCore.playerInventories.add(inventory);

        UUIDS.remove(event.getPlayer().getUniqueId().toString());
        LOGGED_DATA.remove(event.getPlayer().getUniqueId().toString());
        if(event.getPlayer().getCustomName() != null)
            event.setQuitMessage(ChatColor.YELLOW+"Goodbye "+ChatColor.AQUA+event.getPlayer().getCustomName()+ChatColor.YELLOW+"!");
        // clear the inventory
        event.getPlayer().getInventory().setContents(new ItemStack[event.getPlayer().getInventory().getContents().length]);
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

                if(hasSql){
                    for(Account account : DataHandler.AccountList){
                        if(retrieveAccount(id, password, account, event, uuid, player))
                            return;
                    }
                }else{
                    Account account = APIConnector.getAccount(id);
                    if(account != null)
                        if(retrieveAccount(id, password, account, event, uuid, player))
                            return;
                }

                event.getPlayer().sendMessage(ChatColor.RED+"ID number not found! Enter your ID Again");
                event.getPlayer().sendMessage(ChatColor.RED+"Make sure that you are using your "+ChatColor.AQUA+"ID Number"+ChatColor.RED+" registered at the "+ChatColor.AQUA+"PSITS UC Main Website");
                LOGGED_DATA.remove(uuid);

            }else {
                LOGGED_DATA.put(uuid,message);
                event.getPlayer().sendMessage(ChatColor.YELLOW+"Please Enter your Password: ");
            }
        }
    }


    public boolean retrieveAccount(String id, String password, Account account, AsyncPlayerChatEvent event, String uuid, Player player){
        if(String.valueOf(account.getID()).equals(id.trim())){
            if(StringUtility.hashString(password).equals(account.getPassword())){
                // welcome
                UUIDS.remove(uuid);
                Bukkit.getServer().getOnlinePlayers().forEach( players -> {
                    players.sendMessage(ChatColor.YELLOW+"Welcome "+ChatColor.AQUA+account.getName()+ChatColor.YELLOW+"!");
                });
                PluginCore.getPlugin(PluginCore.class).getLogger().info(account.getName()+" joined the server");
                // rename the player
                event.getPlayer().setDisplayName(account.getName());
                event.getPlayer().setCustomName(account.getName());
                event.getPlayer().setPlayerListName(account.getName());
                event.getPlayer().setCustomNameVisible(true);
                event.getPlayer().sendMessage(ChatColor.GREEN + "Feel free to walk around, gather resources and build something!");


                for(PlayerInventory playerInventory : PluginCore.playerInventories){
                    if(playerInventory == null)
                        return true;
                    if(playerInventory.uuid.equals(LOGGED_DATA.get(uuid))){
                        new BukkitRunnable(){
                            final Location location_data = playerInventory.locationData;
                            @Override
                            public void run() {
                                player.teleport(location_data);
                            }
                        }.runTaskLater(PluginCore.getPlugin(PluginCore.class),10);
                        player.getInventory().setContents(playerInventory.inventoryData);
                        return true;
                    }
                }

                new BukkitRunnable(){
                    @Override
                    public void run() {
                        event.getPlayer().removePotionEffect(PotionEffectType.INVISIBILITY);
                    }
                }.runTaskLater(PluginCore.getPlugin(PluginCore.class),10);

            }else {
                event.getPlayer().sendMessage(ChatColor.RED+"Invalid Password! Try again...");
                if(Math.random() <= 0.5){
                    event.getPlayer().sendMessage(ChatColor.RED+"If you forgot your password, reset your password at "+ChatColor.AQUA+"PSITS UC Main Website"+ChatColor.RED+". It will take 5 minutes to take effect.");
                }
            }
            return true;
        }
        return false;
    }
}
