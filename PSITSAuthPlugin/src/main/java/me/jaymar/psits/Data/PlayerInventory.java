package me.jaymar.psits.Data;

import org.bukkit.Location;
import org.bukkit.configuration.serialization.ConfigurationSerializable;
import org.bukkit.inventory.ItemStack;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PlayerInventory implements ConfigurationSerializable {

    public String uuid;
    public ItemStack[] inventoryData;
    public Location locationData;


    public static PlayerInventory create(String uuid, ItemStack[] itemStacks, Location location)
    {
        PlayerInventory i = new PlayerInventory();
        i.uuid = uuid;
        i.locationData = location;
        i.inventoryData = itemStacks;
        return i;
    }

    @Override
    public Map<String, Object> serialize() {
        Map<String, Object> data = new HashMap<>();
        data.put("UUID", uuid);
        data.put("InventoryData", inventoryData);
        data.put("LocationData", locationData);
        return data;
    }

    public static PlayerInventory deserialize(Map<String, Object> arg){
        List<ItemStack> items = (List<ItemStack>) arg.get("InventoryData");
        ItemStack[] itemStacks = new ItemStack[items.size()];
        int i = 0;
        for(ItemStack item: items){
            itemStacks[i++] = item;
        }
        return PlayerInventory.create((String) arg.get("UUID"),itemStacks, (Location) arg.get("LocationData"));
    }
}
