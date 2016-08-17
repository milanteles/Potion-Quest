/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Client_Joueur;

import java.awt.BorderLayout;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.ItemEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;

/**
 *
 * @author Milan
 */
public class Principal extends JFrame {

    private MapJoueur mapJoueur;
    private Connexion pageConnexion;
    private Options pageOptions;
    private Lobby pageLobby; 
    private String adresseServeur;
    private int portServeur;
    private String partie;
    private TimerTask task;
    private Timer timer;
    private ComPorts comports;
    
    private String comport;
    
    private int controleur;
    
    /**
     * Creates new form Principal
     */
    public Principal() {
        initComponents();
        
        initJFrame();
    }
    
    private void initJFrame() {
        this.setLayout(new BorderLayout());
        
        partie = null;
        
        pageLobby = new Lobby();
        
        timer = new Timer();
        
        task = new TimerTask() {
            @Override
            public void run() 
            {
                try {
                    mapJoueur.refresh();
                    if (mapJoueur.checkControleurNatif()) {
                        menuNatif.setSelected(true);
                    }
                    else {
                        menuNatif.setSelected(false);
                    }
                } catch (IOException ex) {
                    Logger.getLogger(Principal.class.getName()).log(Level.SEVERE, null, ex);
                }
            }	
        };
        
        menuArduino.addItemListener((ItemEvent event) -> {
            int state1 = event.getStateChange();
            if (state1 == ItemEvent.SELECTED) {
                comports.initialize();
                comports.setVisible(true);
                if (menuNatif.isSelected()) {
                    controleur = 2;
                }
                else {
                    controleur = 1;
                }
            } else {
                if (menuNatif.isSelected()) {
                   controleur = 0; 
                }
                else {
                    controleur = -1;
                }
                comports.setVisible(false);
            }
            if (mapJoueur != null) {
                if (controleur != -1) {
                    try {
                        mapJoueur = new MapJoueur(adresseServeur, portServeur, pageConnexion.getCredentials(), partie, controleur, comport);
                    } catch (IOException ex) {
                        System.err.println(ex.getMessage());
                    }
                }
                else {
                    mapJoueur.closeControleur();
                } 
            }
        });
        
        menuNatif.addItemListener((ItemEvent event) -> {
            int state1 = event.getStateChange();
            if (state1 == ItemEvent.SELECTED) {
                if (menuArduino.isSelected()) {
                    controleur = 2;
                }
                else {
                    controleur = 0;
                }
            } else {
                controleur = -1;
            }
            if (mapJoueur != null) {
                if (controleur != -1) {
                    try {
                        mapJoueur = new MapJoueur(adresseServeur, portServeur, pageConnexion.getCredentials(), partie, controleur, comport);
                    } catch (IOException ex) {
                        System.err.println(ex.getMessage());
                    }
                }
                else {
                    mapJoueur.closeControleur();
                } 
            }
        });
        
        // Initialisation du panel Connexion
        pageConnexion = new Connexion();
        this.setContentPane(pageConnexion);
        pageConnexion.addComponentListener(new ComponentAdapter() {
            @Override
            public void componentHidden(ComponentEvent e) {
                menuItemOptions.setEnabled(false);
                pageLobby = new Lobby(adresseServeur, portServeur, pageConnexion.getCredentials());
                pageLobby.addComponentListener(new ComponentAdapter() {
                    @Override
                    public void componentHidden(ComponentEvent e) {
                        try {
                            if (menuNatif.isSelected()) {
                                controleur = 0;
                            }
                            else if (menuArduino.isSelected()) {
                                controleur = 1;
                            }
                            else if (menuArduino.isSelected() && menuNatif.isSelected()) {
                                controleur = 2;
                            }
                            else {
                                controleur = -1;
                            }

                            partie = pageLobby.getPartie();
                            mapJoueur = new MapJoueur(adresseServeur, portServeur, pageConnexion.getCredentials(), partie, controleur, comport);
                            setContentPane(mapJoueur);
                            timer.scheduleAtFixedRate(task, 0, 2000);
                        } catch (IOException ex) {
                            System.err.println(ex.getMessage());
                        } 
                    }
                });
                setContentPane(pageLobby);
            }
        });
      
        pageOptions = new Options(this, true);
        pageOptions.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosed(WindowEvent e) {
                adresseServeur = pageOptions.getAdresseServeur();
                portServeur = pageOptions.getPortServeur();
                pageConnexion.setOptions(adresseServeur, portServeur);
            }
        });
        pageOptions.setVisible(false);
        
        comports = new ComPorts(this, true);
        comports.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosed(WindowEvent e) {
                comport = comports.getPort();
                menuArduino.setSelected(false);
                //menuNatif.setSelected(true);
            }
        });
        comports.setVisible(false);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        menuBar = new javax.swing.JMenuBar();
        menuConfiguration = new javax.swing.JMenu();
        menuItemOptions = new javax.swing.JMenuItem();
        menuItemQuitter = new javax.swing.JMenuItem();
        menuControleur = new javax.swing.JMenu();
        menuNatif = new javax.swing.JCheckBoxMenuItem();
        menuArduino = new javax.swing.JCheckBoxMenuItem();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setTitle("Potion Quest");

        menuConfiguration.setText("Configuration");

        menuItemOptions.setText("Options");
        menuItemOptions.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                menuItemOptionsActionPerformed(evt);
            }
        });
        menuConfiguration.add(menuItemOptions);

        menuItemQuitter.setText("Quitter");
        menuItemQuitter.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                menuItemQuitterActionPerformed(evt);
            }
        });
        menuConfiguration.add(menuItemQuitter);

        menuBar.add(menuConfiguration);

        menuControleur.setText("Contrôleur");

        menuNatif.setText("Natif");
        menuControleur.add(menuNatif);

        menuArduino.setText("Arduino");
        menuControleur.add(menuArduino);

        menuBar.add(menuControleur);

        setJMenuBar(menuBar);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 400, Short.MAX_VALUE)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 279, Short.MAX_VALUE)
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void menuItemOptionsActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_menuItemOptionsActionPerformed
        pageOptions.setVisible(true);
    }//GEN-LAST:event_menuItemOptionsActionPerformed

    private void menuItemQuitterActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_menuItemQuitterActionPerformed
        timer.cancel();
        this.dispose();
    }//GEN-LAST:event_menuItemQuitterActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Principal IHM = new Principal();
        IHM.setVisible(true);
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JCheckBoxMenuItem menuArduino;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JMenu menuConfiguration;
    private javax.swing.JMenu menuControleur;
    private javax.swing.JMenuItem menuItemOptions;
    private javax.swing.JMenuItem menuItemQuitter;
    private javax.swing.JCheckBoxMenuItem menuNatif;
    // End of variables declaration//GEN-END:variables
}
