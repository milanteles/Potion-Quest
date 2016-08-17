/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Communication;

import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;
import gnu.io.SerialPortEvent;
import gnu.io.SerialPortEventListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.Observable;

/**
 *
 * @author Milan
 */
public class Serial_Gallileo extends Observable implements SerialPortEventListener {
    private SerialPort serialPort;
    
    private String reception;
    
    private String status;

    /**
    * A BufferedReader which will be fed by a InputStreamReader 
    * converting the bytes into characters 
    * making the displayed results codepage independent
    */
    private BufferedReader input;
    /** The output stream to the port */
    private OutputStream output;
    /** Milliseconds to block while waiting for port open */
    private static final int TIME_OUT = 2000;
    /** Default bits per second for COM port. */
    private static final int DATA_RATE = 9600;

    public void initialize(String port) throws Exception {
        
        CommPortIdentifier portId = CommPortIdentifier.getPortIdentifier(port);

        if (portId == null) {
            System.out.println("Could not find COM port.");
            status = "ERROR";
            return;
        }
        
        reception = null;
        
        // open serial port, and use class name for the appName.
        serialPort = (SerialPort) portId.open(this.getClass().getName(), TIME_OUT);

        // set port parameters
        serialPort.setSerialPortParams(DATA_RATE,
                        SerialPort.DATABITS_8,
                        SerialPort.STOPBITS_1,
                        SerialPort.PARITY_NONE);

        // open the streams
        input = new BufferedReader(new InputStreamReader(serialPort.getInputStream()));
        output = serialPort.getOutputStream();

        serialPort.disableReceiveTimeout();
        serialPort.enableReceiveThreshold(1);

        serialPort.addEventListener(this);
        serialPort.notifyOnDataAvailable(true); 
        
        status = "OK";
    }

    /**
     * This should be called when you stop using the port.
     * This will prevent port locking on platforms like Linux.
     */
    public synchronized void close() {
        if (serialPort != null) {
            serialPort.close();
        }
    }
    
    public String getReception() {
        return reception;
    }
    
    public void setReception(String reception) {
        this.reception = reception;
        setChanged();
        notifyObservers(reception);
    }

    @Override
    public void serialEvent(SerialPortEvent spe) {
        if (spe.getEventType() == SerialPortEvent.DATA_AVAILABLE) {
            try {
                String inputLine = input.readLine();
                setReception(inputLine);
            }
            catch (Exception e) {
                System.err.println(e.toString());
            }
        }
    }
    
    public void write(String envoi) throws IOException {
        envoi += '\0';
        this.output.write(envoi.getBytes());
    }
    
    public String getStatus() {
        return status;
    }
}
