package me.jaymar.psits.Data;

import me.jaymar.psits.PluginCore;
import org.bukkit.Bukkit;
import org.bukkit.configuration.file.FileConfiguration;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class APIConnector {
    public static String stream(URL url){
        try(InputStream input = url.openStream()){
            InputStreamReader isr = new InputStreamReader(input);
            BufferedReader reader = new BufferedReader(isr);
            StringBuilder json = new StringBuilder();
            int c;
            while((c = reader.read()) != -1){
                json.append((char)c);
            }
            return json.toString();
        }catch (IOException error){
            return "";
        }
    }

    public static Account getAccount(String id){
        FileConfiguration config = PluginCore.getPlugin(PluginCore.class).getConfig();
        URL url = null;
        try {
            url = new URL(config.getString("protocol"),config.getString("hostname"),config.getInt("port"),"/PSITS/api_mcs/accounts/"+id);

        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        }
        String json = stream(url);
        json = json.replace('{', ' ').replace('}', ' ');

        Map<String, String> map = new HashMap<>();
        for(String data : json.split(",")){
            if(data.contains(":")){
                String[] newData = data.split(":");
                map.put(newData[0].replace('"', ' ').trim(),newData[1].replace('"', ' ').trim());
            }
        }
        try {
            return new Account(map.get("firstname")+" "+map.get("lastname"),Integer.parseInt(map.get("uid")),map.get("password"));
        }catch (Exception error){
            PluginCore.getPlugin(PluginCore.class).getLogger().info("INFO: User tried to input ID that does not exist -> "+id);
            return null;
        }
    }

}
