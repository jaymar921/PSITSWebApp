package me.jaymar.psits.Data;

public class Account {

    private String Name;
    private int ID;
    private String Password;

    public Account(String name, int ID, String password){
        this.Name = name;
        this.ID  = ID;
        this.Password = password;
    }

    public int getID(){
        return ID;
    }

    public String getName(){
        return Name;
    }

    public String getPassword(){
        return Password;
    }
}
