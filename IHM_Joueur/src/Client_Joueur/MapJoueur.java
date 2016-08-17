/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Client_Joueur;

import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Base64;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JLabel;
import javax.swing.JPanel;
import org.json.JSONArray;
import org.json.JSONObject;
import Communication.Http_Requester;
import Communication.Serial_Gallileo;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.Observable;
import java.util.Observer;
import javax.swing.JFrame;

/**
 *
 * @author Milan
 */
public class MapJoueur extends JPanel implements Http_Requester, Observer {

    // Largeur et hauteur de la carte
    private int width;
    private int height;
    
    // Adresse et port du serveur de jeu
    private final String adresse;
    private final int port;
    
    // Port com Arduino
    private String comPort;
    
    // Credentials HTTP
    private final String credentials;
    
    // Tableau JSON de la carte
    private JSONArray mapView;
    
    // Interface sérié gérant le contrôleur Arduino
    private final Serial_Gallileo serie;
    
    // Contrôleur natif
    private Controleur natif;
    
    // Variable servant de choix de contrôleur
    private int controleur;
    
    // Variable contenant la partie en cours
    private String partie;
    
    // Grille d'affichage de la carte
    private JLabel[][] grid;
    
    // HashMaps
    private final HashMap<String, String> types;
    private final HashMap<String, String> sousTypes_cases;
    private final HashMap<String, String> sousTypes_objets;
    private final HashMap<String, String> variations_cases;
    private final HashMap<String, String> variations_objets_piece;
    private final HashMap<String, String> variations_objets_potion;
    private final HashMap<String, String> variations_objets_coffre;
    private final HashMap<String, String> rotations;
    
    // Inventaire
    private HashMap<String, Integer> inventaire;
    
    // Constructeur qui sert surtout à initialiser les contrôleurs
    public MapJoueur(String adresse, int port, String credentials, String partie, int controleur, String comPort) throws IOException{
        initComponents();
        
        this.controleur = controleur;
        
        types = new HashMap<>();
        sousTypes_cases = new HashMap<>();
        sousTypes_objets = new HashMap<>();
        variations_cases = new HashMap<>();
        variations_objets_piece = new HashMap<>();
        variations_objets_potion = new HashMap<>();
        variations_objets_coffre = new HashMap<>();
        rotations = new HashMap<>();
        
        inventaire = new HashMap<>();
        
        this.adresse = adresse;
        this.port = port;
        this.credentials = credentials;
        this.comPort = comPort;
        
        switch (this.controleur) {
            case 0:
                this.serie = null;
                this.natif = new Controleur((JFrame)this.getParent(), true, this.adresse, this.port, this.credentials);
                this.natif.setVisible(true);
                break;
            case 1:
                this.serie = new Serial_Gallileo();
                try {
                    this.serie.initialize(this.comPort);
                    this.observe(serie);
                } catch (Exception ex) {
                    System.err.println(ex.getMessage());
                }   this.natif = null;
                break;
            case 2:
                this.serie = new Serial_Gallileo();
                try {
                    this.serie.initialize(this.comPort);
                    this.observe(serie);
                } catch (Exception ex) {
                    System.err.println(ex.getMessage());
                }   this.natif = new Controleur((JFrame)this.getParent(), true, this.adresse, this.port, this.credentials);
                this.natif.setVisible(true);
                break;
            default:
                this.serie = null;
                this.natif = null;
                break;
        }
        
        if (this.natif != null) {
            this.natif.setPartie(this.partie);
            this.natif.addWindowListener(new WindowAdapter() {
                @Override
                public void windowClosed(WindowEvent e) {
                    natif = null;
                }
            });
        }
        
        this.partie = partie;
  
        initHashMaps();
        
        refresh();
    }
    
    // Initialise le layout contenant la carte avec les images décodées depuis le tableau JSON
    private void initJPanel(int width, int height) {
        map.removeAll();
        map.setLayout(new GridLayout(width,height));
        grid=new JLabel[width][height];
        for(int y=0; y<height; y++){
            for(int x=0; x<width; x++){   
                try {
                    ImageIcon image;
                    image = decode(x, y, mapView);
                    grid[x][y]=new JLabel(image);
                    map.add(grid[x][y]);
                } catch (IOException ex) {
                    Logger.getLogger(MapJoueur.class.getName()).log(Level.SEVERE, null, ex);
                } 
            }
        }
        map.repaint();
        map.revalidate();
        this.setVisible(true);
    }
    
    // Initialisation des HashMaps servant pour le décodage de la carte
    private void initHashMaps() {
        types.put("00", "franchissable");
        types.put("01", "infranchissable");
        types.put("02", "objet");
        
        sousTypes_cases.put("00", "ground-default");
        sousTypes_cases.put("01", "chemin");
        sousTypes_cases.put("02", "route");
        sousTypes_cases.put("03", "ground-primary");
        sousTypes_cases.put("04", "ground-secondary");
        sousTypes_cases.put("05", "ground-fake");
        
        sousTypes_objets.put("00", "piece");
        sousTypes_objets.put("01", "potion");
        sousTypes_objets.put("02", "coffre");
        
        variations_cases.put("XX", "");
        variations_cases.put("00", "p");
        variations_cases.put("01", "l");
        variations_cases.put("02", "v");
        variations_cases.put("03", "t");
        variations_cases.put("04", "x");
        variations_cases.put("05", "i");
        
        variations_objets_piece.put("XX", "");
        
        variations_objets_potion.put("00", "");
        variations_objets_potion.put("01", "fake");
        
        variations_objets_coffre.put("00", "1");
        variations_objets_coffre.put("01", "2");
        variations_objets_coffre.put("02", "pieces");
        
        rotations.put("00", "");
        rotations.put("01", "rot090");
        rotations.put("02", "rot180");
        rotations.put("03", "rot270");
        
        inventaire.put("fov-increase", 0);
        inventaire.put("magnet", 0);
        inventaire.put("happy-hour", 0);
        inventaire.put("immunity", 0);
        inventaire.put("taxman", 0);
        inventaire.put("lottery-win", 0);
    }

    // Décode le tableau JSON contenant la carte afin de récupérer l'image correspondante à chaque case
    private ImageIcon decode(int Case, int ligne, JSONArray map) throws IOException {
        String chemin = ".\\Images\\";
        String fichier = "";
        
        JSONArray jarr = new JSONArray(mapView.getJSONArray(ligne).toString());
        
        JSONObject objectCase = jarr.getJSONObject(Case);

        if (objectCase.length() != 0) {
        
            // Type
            if (!objectCase.getBoolean("isObstacle")) {
                fichier += types.get("00");
            }
            else {
                fichier += types.get("01");   
            }

            String skin = objectCase.getString("skin");
            if (!"".equals(skin)) {
                // Sous-Type
                switch (skin.substring(0, 2)) {
                    case "00":
                        fichier += '-' + sousTypes_cases.get("00");
                        break;
                    case "01":
                        fichier += '-' + sousTypes_cases.get("01");
                        break;
                    case "02":
                        fichier += '-' + sousTypes_cases.get("02");
                        break;
                    case "03":
                        fichier += '-' + sousTypes_cases.get("03");
                        break;
                    case "04":
                        fichier += '-' + sousTypes_cases.get("04");
                        break;
                    case "05":
                        fichier += '-' + sousTypes_cases.get("05");
                        break;
                }
                // Variation
                switch (skin.substring(2, 4)) {
                    default:
                        fichier += variations_cases.get("XX");
                        break;
                    case "00":
                        fichier += '-' + variations_cases.get("00");
                        break;
                    case "01":
                        fichier += '-' + variations_cases.get("01");
                        break;
                    case "02":
                        fichier += '-' + variations_cases.get("02");
                        break;
                    case "03":
                        fichier += '-' + variations_cases.get("03");
                        break;
                    case "04":
                        fichier += '-' + variations_cases.get("04");
                        break;
                    case "05":
                        fichier += '-' + variations_cases.get("05");
                        break;
                }
                // Orientation
                switch (skin.substring(4, 6)) {
                    case "00":
                        fichier += rotations.get("00");
                        break;
                    case "01":
                        chemin += "rotated\\";
                        fichier += '-' + rotations.get("01");
                        break;
                    case "02":
                        chemin += "rotated\\";
                        fichier += '-' + rotations.get("02");
                        break;
                    case "03":
                        chemin += "rotated\\";
                        fichier += '-' + rotations.get("03");
                        break;
                }
            }

            if (!objectCase.isNull("contains")) {
                String chemin2 = ".\\Images\\";
                String fichier2;
                BufferedImage imgBG;
                BufferedImage imgFG;
                BufferedImage combinedImage;
                Graphics2D g;
                String kind = objectCase.getJSONObject("contains").getString("kind");
                //System.out.println(kind);
                if (!kind.isEmpty()) {
                    switch (kind) {
                        case "coin":
                            fichier2 = types.get("02") + '-' + sousTypes_objets.get("00");
                            // Orientation
                            switch (objectCase.getJSONObject("contains").getString("skin").substring(2, 4)) {
                                case "00":
                                    fichier2 += rotations.get("00");
                                    break;
                                case "01":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("01");
                                    break;
                                case "02":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("02");
                                    break;
                                case "03":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("03");
                                    break;
                            }
                            imgBG = ImageIO.read(new File(chemin + fichier + ".png"));
                            imgFG = ImageIO.read(new File(chemin2 + fichier2 + ".png"));
                            combinedImage = new BufferedImage(imgBG.getWidth(), imgBG.getHeight(), BufferedImage.TYPE_INT_ARGB );
                            g = combinedImage.createGraphics();
                            g.drawImage(imgBG,0,0,null);
                            g.drawImage(imgFG,0,0,null);
                            g.dispose();

                            return new ImageIcon(combinedImage);
                        case "potion":
                            fichier2 = types.get("02") + '-' + sousTypes_objets.get("01");
                            switch (objectCase.getJSONObject("contains").getString("skin").substring(0, 2)) {
                                case "00":
                                    fichier2 += variations_objets_potion.get("00");
                                    break;
                                case "01":
                                    fichier2 += '-' + variations_objets_potion.get("01");
                                    break;
                            }
                            // Orientation
                            switch (objectCase.getJSONObject("contains").getString("skin").substring(2, 4)) {
                                case "00":
                                    fichier2 += rotations.get("00");
                                    break;
                                case "01":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("01");
                                    break;
                                case "02":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("02");
                                    break;
                                case "03":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("03");
                                    break;
                            }
                            imgBG = ImageIO.read(new File(chemin + fichier + ".png"));
                            imgFG = ImageIO.read(new File(chemin2 + fichier2 + ".png"));
                            combinedImage = new BufferedImage(imgBG.getWidth(), imgBG.getHeight(), BufferedImage.TYPE_INT_ARGB );
                            g = combinedImage.createGraphics();
                            g.drawImage(imgBG,0,0,null);
                            g.drawImage(imgFG,0,0,null);
                            g.dispose();

                            return new ImageIcon(combinedImage);
                        case "chest":
                            fichier2 = types.get("02") + '-' + sousTypes_objets.get("02");
                            switch (objectCase.getJSONObject("contains").getString("skin").substring(0, 2)) {
                                case "00":
                                    fichier2 += variations_objets_coffre.get("00");
                                    break;
                                case "01":
                                    fichier2 += variations_objets_coffre.get("01");
                                    break;
                                case "02":
                                    fichier2 += '-' + variations_objets_coffre.get("02");
                                    break;
                            }
                            // Orientation
                            switch (objectCase.getJSONObject("contains").getString("skin").substring(2, 4)) {
                                case "00":
                                    fichier2 += rotations.get("00");
                                    break;
                                case "01":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("01");
                                    break;
                                case "02":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("02");
                                    break;
                                case "03":
                                    chemin2 += "rotated\\";
                                    fichier2 += '-' + rotations.get("03");
                                    break;
                            }

                            imgBG = ImageIO.read(new File(chemin + fichier + ".png"));
                            imgFG = ImageIO.read(new File(chemin2 + fichier2 + ".png"));
                            combinedImage = new BufferedImage(imgBG.getWidth(), imgBG.getHeight(), BufferedImage.TYPE_INT_ARGB );
                            g = combinedImage.createGraphics();
                            g.drawImage(imgBG,0,0,null);
                            g.drawImage(imgFG,0,0,null);
                            g.dispose();

                            return new ImageIcon(combinedImage);
                    }
                }
            }

            if (!objectCase.isNull("players")) {
                //System.out.println(objectCase.getJSONArray("players"));
            }
        }
        else {
            fichier = "infranchissable-ground-default";
        }

        fichier += ".png";
        
        chemin += fichier;
        
        //System.out.println(chemin);
        
        return new ImageIcon(chemin);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {
        java.awt.GridBagConstraints gridBagConstraints;

        map = new javax.swing.JPanel();
        panelResume = new javax.swing.JPanel();
        panelPieces = new javax.swing.JPanel();
        labelPieces = new javax.swing.JLabel();
        labelNbPieces = new javax.swing.JLabel();
        panelClassement = new javax.swing.JPanel();
        labelClassement = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        textAreaClassement = new javax.swing.JTextArea();

        setLayout(new java.awt.BorderLayout());

        javax.swing.GroupLayout mapLayout = new javax.swing.GroupLayout(map);
        map.setLayout(mapLayout);
        mapLayout.setHorizontalGroup(
            mapLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 0, Short.MAX_VALUE)
        );
        mapLayout.setVerticalGroup(
            mapLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 300, Short.MAX_VALUE)
        );

        add(map, java.awt.BorderLayout.CENTER);

        panelResume.setLayout(new java.awt.BorderLayout());

        labelPieces.setText("Pièces :");
        panelPieces.add(labelPieces);

        labelNbPieces.setText("0");
        panelPieces.add(labelNbPieces);

        panelResume.add(panelPieces, java.awt.BorderLayout.NORTH);

        panelClassement.setLayout(new java.awt.GridBagLayout());

        labelClassement.setText("Classement");
        panelClassement.add(labelClassement, new java.awt.GridBagConstraints());

        textAreaClassement.setEditable(false);
        textAreaClassement.setColumns(15);
        textAreaClassement.setRows(10);
        jScrollPane1.setViewportView(textAreaClassement);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridx = 0;
        gridBagConstraints.gridy = 1;
        panelClassement.add(jScrollPane1, gridBagConstraints);

        panelResume.add(panelClassement, java.awt.BorderLayout.CENTER);

        add(panelResume, java.awt.BorderLayout.EAST);
    }// </editor-fold>//GEN-END:initComponents

    // Authentification HTTP non utilisée
    @Override
    public boolean authentification() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    // Get HTTP qui renvoie un tableau JSON
    @Override
    public JSONArray get(String request) throws IOException {
        String USER_AGENT = "Mozilla/5.0";

        JSONArray retour;
        retour = new JSONArray();
        
        URL obj;
        try {
            if (port != -1) {
                obj = new URL("http://" + adresse + ':' + port + request);
            }
            else {
                obj = new URL("http://" + adresse + request);
            }
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            String encoded = Base64.getEncoder().encodeToString(credentials.getBytes());
            con.setRequestProperty("Authorization", "Basic "+encoded);
            con.setRequestMethod("GET");
            con.setRequestProperty("User-Agent", USER_AGENT);
            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {                 StringBuilder response;
                try ( // success
                        BufferedReader in = new BufferedReader(new InputStreamReader(
                                con.getInputStream()))) {
                    String inputLine;
                    response = new StringBuilder();
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                }

                //JSONObject temp = new JSONObject(response.toString());
                retour = new JSONArray(response.toString());
                //retour.put(temp);
            } else {
                retour = null;
            }
        } catch (MalformedURLException ex) {
            System.err.println(ex.getMessage());
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        }
        
        return retour;
    }

    // Post HTTP qui prend un objet JSON en paramètre
    @Override
    public boolean post(String request, JSONObject data) throws IOException {
        String urlServeur = "http://" + adresse + ':' + port + request;
        URL obj;
        String USER_AGENT = "Mozilla/5.0";
        boolean retour = false;
        
        try {
            obj = new URL(urlServeur);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            String encoded = Base64.getEncoder().encodeToString(credentials.getBytes());
            con.setRequestProperty("Authorization", "Basic "+encoded);
            con.setRequestMethod("POST");
            con.setRequestProperty("User-Agent", USER_AGENT);
            con.setRequestProperty("Content-Type", "application/json");

            con.setDoOutput(true);
            try (OutputStreamWriter out = new OutputStreamWriter(con.getOutputStream())) {
                out.write(data.toString());
                out.flush();
            }

            String msg = con.getResponseMessage();
            int responseCode = con.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_CREATED) {
                StringBuilder response;
                try ( //success
                        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()))) {
                    String inputLine;
                    response = new StringBuilder();
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                }

                partie = response.toString();
                retour = true;
            } else {
                retour = false;
            }
        } catch (MalformedURLException ex) {
            System.err.println(ex.getMessage());
        }  
        return retour;
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel labelClassement;
    private javax.swing.JLabel labelNbPieces;
    private javax.swing.JLabel labelPieces;
    private javax.swing.JPanel map;
    private javax.swing.JPanel panelClassement;
    private javax.swing.JPanel panelPieces;
    private javax.swing.JPanel panelResume;
    private javax.swing.JTextArea textAreaClassement;
    // End of variables declaration//GEN-END:variables
   
    // Rafraîchis tout le JPanel en mettant à jour avec les nouvelles données reçues
    public void refresh() throws IOException {      
        textAreaClassement.setText("");
        JSONArray temp = get(partie);
        JSONObject response = temp.getJSONObject(0);
        mapView = new JSONArray(response.getString("mapView"));
       
        labelNbPieces.setText(Integer.toString(response.getJSONObject("inventory").getInt("coins")));
        
        JSONArray potions = response.getJSONObject("inventory").getJSONArray("potions");
        String envoiPotions = "";
        for (int i = 0;i < potions.length(); i++) {
            if (this.natif != null) {
                this.natif.setInventaire(potions.getJSONObject(i).getString("kind"));
            }
            switch (potions.getJSONObject(i).getString("kind")) {
                case "fov-increase":
                    int nb = inventaire.get("fov-increase");
                    inventaire.put("fov-increase", nb + 1);
                    break;
                case "magnet":
                    int nb2 = inventaire.get("magnet");
                    inventaire.put("magnet", nb2 + 1);
                    break;
                case "happy-hour":
                    int nb3 = inventaire.get("happy-hour");
                    inventaire.put("fov-increase", nb3 + 1);
                    break;
                case "immunity":
                    int nb4 = inventaire.get("immunity");
                    inventaire.put("fov-increase", nb4 + 1);
                    break;
                case "taxman":
                    int nb5 = inventaire.get("taxman");
                    inventaire.put("fov-increase", nb5 + 1);
                    break;
                case "lottery-win":
                    int nb6 = inventaire.get("lottery-win");
                    inventaire.put("fov-increase", nb6 + 1);
                    break;
            }
            envoiPotions = "POTIONS";
            envoiPotions += ";fov-increase:" + inventaire.get("fov-increase");
            envoiPotions += ";magnet:" + inventaire.get("magnet");
            envoiPotions += ";happy-hour:" + inventaire.get("happy-hour");
            envoiPotions += ";immunity:" + inventaire.get("immunity");
            envoiPotions += ";taxman:" + inventaire.get("taxman");
            envoiPotions += ";lottery-win:" + inventaire.get("lottery-win");
        }
        
        for (Object element : response.getJSONArray("ranking")) {
            textAreaClassement.append(element.toString() + '\n');
        }     
        
        if (this.serie != null) {
            if("OK".equals(this.serie.getStatus())) {   
                if (response.getString("currentPlayer").equals(credentials.substring(0, credentials.indexOf(":")))) {
                    try {
                        this.serie.write("START");
                        this.serie.write(envoiPotions);
                    } catch (IOException ex) {
                        System.err.println(ex.getMessage());
                    }
                }
                else {
                    try {
                        this.serie.write("WAIT");
                    } catch (IOException ex) {
                        System.err.println(ex.getMessage());
                    }
                }
            }
        }
        
        if (this.natif != null) {
            this.natif.setPartie(this.partie);
        }
        

        width = response.getInt("width");
        height = response.getInt("height");
        
        initJPanel(width, height);
        
        this.repaint();
        this.revalidate();
        this.validate();

        System.out.println("Test");
    }
    
    // Observe la trame reçue par le contrôleur arduino
    public void observe(Observable o) {
        o.addObserver(this);
    }

    // Lance le traitement de la trame lorsque le contrôleur arduino envoie des données
    @Override
    public void update(Observable o, Object arg) {
        traitementTrame((String)arg);
    }
    
    // Traite la trame de déplacement ou d'action du contrôleur arduino et envoi la requête au serveur
    public void traitementTrame(String trame) {
        JSONObject action = new JSONObject();
        String[] split = trame.split(";");
        if (split[0].equals("DEPLACEMENT")) {
            action.put("action", "move");
            switch (split[1]) {
                case "1":
                    action.put("value", "up");
                    break;
                case "2":
                    action.put("value", "down");
                    break;
                case "3":
                    action.put("value", "left");
                    break;
                case "4":
                    action.put("value", "right");
                    break;
                default:
                    action.put("value", "none");
                    break;
            }
        }
        else if (split[0].equals("POTION")) {
            action.put("action", "potion");
            action.put("value", split[1]);
        }
        
        try {
            System.out.println(action.toString());
            System.out.println(partie);
            if (post((partie + "/moves"), action)) {
                System.out.println("OK");
            }
            else {
                System.out.println("NOT OK");
            }
        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
    }
    
    // Définis le contrôleur :
    // 0 -> Contrôleur natif
    // 1 -> Contrôleur arduino
    // 2 -> Les 2 contrôleurs
    public void setControleur(int controleur) {
        this.controleur = controleur;
    }
    
    // Ferme le contrôleur natif
    public void closeControleur() {
        if (this.natif != null) {
            this.natif.dispose();
        }   
    }
    
    // Contrôle si le contrôleur natif est actif ou non
    public boolean checkControleurNatif() {
        return this.natif != null;
    }
}
