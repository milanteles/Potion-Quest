/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Client_Joueur;

import Communication.Http_Requester;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Base64;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.DefaultListModel;
import javax.swing.JComponent;
import javax.swing.SwingUtilities;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 *
 * @author milan.teles
 */
public class Controleur extends javax.swing.JDialog implements Http_Requester {

    private final DefaultListModel model;
    private String adresse;
    private int port;
    private String credentials;
    private String partie;
    
    /**
     * Creates new form Controleur
     * @param parent
     * @param modal
     */
    public Controleur(java.awt.Frame parent, boolean modal, String adresse, int port, String credentials) {
        super(parent, modal);
        initComponents();
        
        model = new DefaultListModel();
        
        listPotions.setModel(model);
        
        this.adresse = adresse;
        this.port = port;
        this.credentials = credentials;
        
        this.setModalityType(ModalityType.MODELESS);
        this.setTitle("Contrôleur natif");
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        paneInventaire = new javax.swing.JLayeredPane();
        jScrollPane1 = new javax.swing.JScrollPane();
        listPotions = new javax.swing.JList<>();
        jLayeredPane1 = new javax.swing.JLayeredPane();
        buttonUtiliser = new javax.swing.JButton();
        buttonLeft = new javax.swing.JButton();
        buttonRight = new javax.swing.JButton();
        buttonUp = new javax.swing.JButton();
        buttonDown = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.DISPOSE_ON_CLOSE);

        paneInventaire.setLayout(new java.awt.FlowLayout());

        jScrollPane1.setPreferredSize(new java.awt.Dimension(200, 130));

        listPotions.setModel(new javax.swing.AbstractListModel<String>() {
            String[] strings = { "Item 1", "Item 2", "Item 3", "Item 4", "Item 5" };
            public int getSize() { return strings.length; }
            public String getElementAt(int i) { return strings[i]; }
        });
        jScrollPane1.setViewportView(listPotions);

        paneInventaire.add(jScrollPane1);

        getContentPane().add(paneInventaire, java.awt.BorderLayout.NORTH);

        jLayeredPane1.setLayout(new java.awt.BorderLayout());

        buttonUtiliser.setText("Utiliser");
        buttonUtiliser.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonUtiliserActionPerformed(evt);
            }
        });
        jLayeredPane1.add(buttonUtiliser, java.awt.BorderLayout.CENTER);

        buttonLeft.setText("◄");
        buttonLeft.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonLeftActionPerformed(evt);
            }
        });
        jLayeredPane1.add(buttonLeft, java.awt.BorderLayout.WEST);

        buttonRight.setText("►");
        buttonRight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonRightActionPerformed(evt);
            }
        });
        jLayeredPane1.add(buttonRight, java.awt.BorderLayout.EAST);

        buttonUp.setText("▲");
        buttonUp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonUpActionPerformed(evt);
            }
        });
        jLayeredPane1.add(buttonUp, java.awt.BorderLayout.NORTH);

        buttonDown.setText("▼");
        buttonDown.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                buttonDownActionPerformed(evt);
            }
        });
        jLayeredPane1.add(buttonDown, java.awt.BorderLayout.SOUTH);

        getContentPane().add(jLayeredPane1, java.awt.BorderLayout.CENTER);

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void buttonLeftActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonLeftActionPerformed
        String request = this.partie + "/moves";
        
        JSONObject data = new JSONObject();
        data.put("action", "move");
        data.put("value", "left");
        try {
            this.post(request, data);
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        }        
    }//GEN-LAST:event_buttonLeftActionPerformed

    private void buttonUpActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonUpActionPerformed
        String request = this.partie + "/moves";
        
        JSONObject data = new JSONObject();
        data.put("action", "move");
        data.put("value", "up");
        try {
            this.post(request, data);
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        }
    }//GEN-LAST:event_buttonUpActionPerformed

    private void buttonDownActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonDownActionPerformed
        String request = this.partie + "/moves";
        
        JSONObject data = new JSONObject();
        data.put("action", "move");
        data.put("value", "down");
        try {
            this.post(request, data);
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        }
    }//GEN-LAST:event_buttonDownActionPerformed

    private void buttonRightActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonRightActionPerformed
        String request = this.partie + "/moves";
        
        JSONObject data = new JSONObject();
        data.put("action", "move");
        data.put("value", "right");
        try {
            this.post(request, data);
        } catch (IOException ex) {
            System.err.println(ex.getMessage());
        }
    }//GEN-LAST:event_buttonRightActionPerformed

    private void buttonUtiliserActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_buttonUtiliserActionPerformed
        
    }//GEN-LAST:event_buttonUtiliserActionPerformed

    public void setInventaire(String inventaire) {
        model.addElement(inventaire);
    }
    
    public void clear() {
        model.clear();
    }
    
    public void setPartie(String partie) {
        this.partie = partie;
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton buttonDown;
    private javax.swing.JButton buttonLeft;
    private javax.swing.JButton buttonRight;
    private javax.swing.JButton buttonUp;
    private javax.swing.JButton buttonUtiliser;
    private javax.swing.JLayeredPane jLayeredPane1;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JList<String> listPotions;
    private javax.swing.JLayeredPane paneInventaire;
    // End of variables declaration//GEN-END:variables

    @Override
    public boolean authentification() {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

    @Override
    public JSONArray get(String request) throws IOException {
        throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
    }

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
            
            int responseCode = con.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_NO_CONTENT) {
                StringBuilder response;
                try ( //success
                        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()))) {
                    String inputLine;
                    response = new StringBuilder();
                    while ((inputLine = in.readLine()) != null) {
                        response.append(inputLine);
                    }
                }
                retour = true;
            } else {
                retour = false;
            }
        } catch (MalformedURLException ex) {
            System.err.println(ex.getMessage());
        }  
        return retour;
    }
    
    public static void repaintParent(JComponent component)
    {

      // Get the parent of the component.
      JComponent parentComponent = (JComponent)SwingUtilities.getAncestorOfClass(JComponent.class, component);

      // Could we find a parent?
      if (parentComponent != null) 
      {
        // Repaint the parent.
        parentComponent.revalidate();
        parentComponent.repaint();
      }
      else
      {
        // Repaint the component itself.
        component.revalidate();
        component.repaint();
      }

    }
}