/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Http;

import java.io.IOException;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 *
 * @author Milan
 */
public interface Requester {
    public boolean authentification();
    
    public JSONArray get(String request) throws IOException;
    
    public boolean post(String request, JSONObject data) throws IOException;
}
