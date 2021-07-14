import java.awt.*;
import java.awt.event.*;
import java.awt.geom.*;
import java.util.*;
import javax.swing.*;

/**
 * AnalogClock is a resizable Swing component that draws an analog clock.
 *
 * @author Knute Johnson
 */
public class AnalogClock extends JComponent implements ActionListener {
    /** Constant for two times pi */
    private final static double TWOPI = Math.PI * 2.0;

    /** Timer to update display */
    private final javax.swing.Timer timer = new javax.swing.Timer(100,this);

    /**
     * Starts the clock running
     */
    public void start() {
        timer.start();
    }

    /**
     * Stops the clock running
     */
    public void stop() {
        timer.stop();
    }
    
    /**
     * Calls repaint() to draw the clock
     */
    public void actionPerformed(ActionEvent ae) {
        repaint();
    }

    @Override public void paintComponent(Graphics graphics) {
        Graphics2D g = (Graphics2D)graphics;
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
         RenderingHints.VALUE_ANTIALIAS_ON);

        // draw the background
        g.setColor(Color.WHITE);
        g.fillRect(0,0,getWidth(),getHeight());
        
        Calendar calendar = Calendar.getInstance();
        int secs = calendar.get(Calendar.SECOND);
        int mins = calendar.get(Calendar.MINUTE);
        int hours = calendar.get(Calendar.HOUR);
        
        int size = Math.min(getWidth(),getHeight());
        int center = size/2;
        
        // save the original transform
        AffineTransform at = g.getTransform();
        
        // draw minute ticks
        g.setColor(Color.BLACK);
        for (int i=0; i<60; i++) {
            g.drawLine(center,center/25,center,center/50);
            g.rotate(TWOPI * (6.0 / 360.0),center,center);
        }
        g.setTransform(at);
        
        // draw hour dots
        g.setColor(Color.RED);
        for (int i=0; i<12; i++) {
            g.fillOval(center-center/40,center/100,center/20,center/20);
            g.rotate(TWOPI * (30.0 / 360.0),center,center);
        }
        g.setTransform(at);

        int[] x,y;

        // draw hour hand
        g.setColor(Color.BLUE);
        g.rotate(TWOPI * (((hours * 3600.0) + (mins * 60.0) + secs) / 43200.0),
         center,center);
        x = new int[] { center,center+center/16,center,center-center/16 };
        y = new int[] { center+center/10,center,center/3,center };
        g.fill(new Polygon(x,y,x.length));
        g.setTransform(at);
        
        // draw minute hand
        g.setColor(new Color(80,80,255));
        g.rotate(TWOPI * ((mins * 60.0 + secs) / 3600.0),center,center);
        x = new int[] { center,center+center/20,center,center-center/20 };
        y = new int[] { center+center/5,center,center/20,center };
        g.fill(new Polygon(x,y,x.length));
        g.setTransform(at);
        
        // draw second hand
        g.setColor(Color.BLACK);
        g.fillOval(center-center/50,center-center/50,center/25,center/25);
        g.rotate(TWOPI * (secs/ 60.0),center,center);
        x = new int[] { center,center-center/100,center,center+center/100 };
        y = new int[] { center+center/4,center,center/30,center };
        g.fill(new Polygon(x,y,x.length));
        g.drawLine(center,center+center/4,center,center/15);
        g.setTransform(at);
    }
    
    /**
     * Main application entry point.  Creates the containing frame, creates
     * and starts the clock.  On window closing, stops the clock.
     *
     * @param args command line arguments, unused
     */
    public static void main(String[] args) {
        EventQueue.invokeLater(new Runnable() {
            public void run() {
                AnalogClock clock = new AnalogClock();
                JFrame frame = new JFrame("Analog Clock");
                frame.setLayout(new GridBagLayout());
                frame.setUndecorated(true);
                frame.getContentPane().setBackground(Color.WHITE);
                frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                frame.addWindowListener(new WindowAdapter() {
                    public void windowClosing(WindowEvent we) {
                        clock.stop();
                    }
                });
                frame.addMouseListener(new MouseAdapter() {
                    public void mousePressed(MouseEvent me) {
                        clock.stop();
                        frame.dispose();
                    }
                });
                clock.setPreferredSize(new Dimension(1080,1080));
                frame.add(clock);
                frame.setSize(1920,1080);
                //frame.pack();
                frame.setVisible(true);
                clock.start();
            }
        });
    }
}
