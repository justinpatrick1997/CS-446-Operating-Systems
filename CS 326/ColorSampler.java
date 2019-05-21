/**
*Author: Justin Patrick
*Project: Color Sampler
*Class: CS 326
**/

import java.io.*;
import javax.swing.*;
import javax.swing.event.*;
import java.awt.*;
import java.awt.event.*;

public class ColorSampler extends JFrame
  {
    private static int numColors = 11;
    protected Color selectedColor;
    protected boolean colorAltered = false;
    protected static String title;
    protected JList<String> colorList;
    protected Shape rectangle;
    protected FileIO file;

    protected JButton redMinus;
    protected JButton redPlus;
    protected JButton greenMinus;
    protected JButton greenPlus;
    protected JButton blueMinus;
    protected JButton bluePlus;

    protected JLabel redLabel;
    protected JLabel greenLabel;
    protected JLabel blueLabel;
    protected JTextField tfRed;
    protected JTextField tfGreen;
    protected JTextField tfBlue;

    protected JButton saveBut;
    protected JButton resetBut;

	  protected static String[] colorArray;
	  protected static int[] redArray;
	  protected static int[] greenArray;
	  protected static int[] blueArray;
	  protected String currentColorName;
	  protected int rLocation;
	  protected int gLocation;
	  protected int currentIndex;
	  protected int bLocation;

public static void main( String argv [])
	{
		title = "Color Sampler";
	 	new ColorSampler(title);
	}

public ColorSampler(String title)
	{
		//intializing variables
		super(title);
		setBounds(150,150,310,300);
		addWindowListener( new WindowDestroyer());
		getContentPane().setLayout(null);
    file = new FileIO();
    colorArray = new String[20];
    redArray = new int[20];
    greenArray = new int[20];
    blueArray = new int[20];

    //initializing features
    redLabel = new JLabel("Red: ");
    greenLabel = new JLabel("Green: ");
    blueLabel = new JLabel("Blue: ");
    redMinus = new JButton("-");
    redPlus = new JButton("+");
    greenMinus = new JButton("-");
    greenPlus = new JButton("+");
    blueMinus = new JButton("-");
    bluePlus = new JButton("+");
    saveBut = new JButton("Save");
    resetBut = new JButton("Reset");
		currentColorName = new String("");
    tfRed = new JTextField(String.valueOf(rLocation));
    tfGreen = new JTextField(String.valueOf(gLocation));
    tfBlue = new JTextField(String.valueOf(bLocation));

    colorList = new JList<>();

    redMinus.addActionListener(new ActionHandler());
		redPlus.addActionListener(new ActionHandler());
		greenMinus.addActionListener(new ActionHandler());
		greenPlus.addActionListener(new ActionHandler());
		blueMinus.addActionListener(new ActionHandler());
		bluePlus.addActionListener(new ActionHandler());
    saveBut.addActionListener(new ActionHandler());
		resetBut.addActionListener(new ActionHandler());

		colorList.addListSelectionListener(new ListSelectionHandler());

    try
      {
        file.readInData(colorArray, redArray, greenArray, blueArray);
      }
    catch(IOException e)
      {
        System.out.println("\nerror - file will not read");
      }

    //deafult variables
    colorList.setListData(colorArray);
		rLocation = 0;
    gLocation = 0;
    bLocation = 0;
    currentIndex = 0;
		currentColorName  = "Red";

		//window set
		rectangle = new Shape();
	 	getContentPane().setLayout(null);
	 	getContentPane().add(rectangle);
	 	rectangle.setBounds(10,10,200,120);

 		getContentPane().add(redLabel);
 		redLabel.setBounds(10,135, 50, 30);
 		getContentPane().add(greenLabel);
 		greenLabel.setBounds(10,160, 60, 30);
 		getContentPane().add(blueLabel);
 		blueLabel.setBounds(10,185, 50, 30);

 		getContentPane().add(tfRed);
 		tfRed.setBounds(65, 140, 30, 20);
 		getContentPane().add(tfGreen);
 		tfGreen.setBounds(65, 165, 30, 20);
 		getContentPane().add(tfBlue);
 		tfBlue.setBounds(65, 190, 30, 20);

 		getContentPane().add(redMinus);
 		redMinus.setBounds(105, 140, 50, 20);
 		getContentPane().add(redPlus);
 		redPlus.setBounds(160, 140, 50, 20);

 		getContentPane().add(greenMinus);
 		greenMinus.setBounds(105, 165, 50, 20);
 		getContentPane().add(greenPlus);
 		greenPlus.setBounds(160, 165, 50, 20);

 		getContentPane().add(blueMinus);
 		blueMinus.setBounds(105, 190, 50, 20);
 		getContentPane().add(bluePlus);
 		bluePlus.setBounds(160, 190, 50, 20);

	 	getContentPane().add(saveBut);
	 	saveBut.setBounds(20, 230, 80, 20);

	 	getContentPane().add(resetBut);
	 	resetBut.setBounds(110, 230, 80, 20);

	 	getContentPane().add(colorList);
	 	colorList.setBounds(220, 10, 80, 220);
	 	colorList.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);

		colorList.setSelectedIndex(0);
    setVisible(true);
	}

class ActionHandler implements ActionListener
	 {
		   public void actionPerformed(ActionEvent e)
		     {
			     //initalize variables
			     int index = 0;

			     if( e.getSource() == redMinus )
			        {
				        if( rLocation > 0 )
				           {
					           //change color
					           rLocation = rLocation - 5;
					           rectangle.setColor( rLocation, gLocation, bLocation);
					           tfRed.setText(String.valueOf(rLocation));
					           setTitle("Color Sampler*");
				           }
			        }

			else if( e.getSource() == greenMinus )
			   {
				    if( gLocation > 0 )
				        {
					        //change color
					        gLocation = gLocation - 5;
					        rectangle.setColor( rLocation, gLocation, bLocation);
				          tfGreen.setText(String.valueOf(gLocation));
					        setTitle("Color Sampler*");
				        }
			    }
			else if( e.getSource() == blueMinus )
			   {
				    if( bLocation > 0 )
				        {
					        //change color
					        bLocation = bLocation - 5;
					        rectangle.setColor( rLocation, gLocation, bLocation );
					        tfBlue.setText(String.valueOf(bLocation));
					        setTitle("Color Sampler*");
				        }
			    }
			else if( e.getSource() == redPlus )
			   {
				       if( rLocation < 255 )
				           {
					           //change color
					           rLocation = rLocation + 5;
					           rectangle.setColor( rLocation, gLocation, bLocation);
					           tfRed.setText(String.valueOf(rLocation));
					           setTitle("Color Sampler*");
				           }
			   }
			else if( e.getSource() == greenPlus )
			  {
				   if( gLocation < 255 )
				    {
					   //change color
					   gLocation = gLocation + 5;
					   rectangle.setColor( rLocation, gLocation, bLocation);
					   tfGreen.setText(String.valueOf(gLocation));
					   setTitle("Color Sampler*");
				    }
			  }
			else if( e.getSource() == bluePlus )
			 {
				if( bLocation < 255 )
				   {
					   //change color
					   bLocation = bLocation + 5;
					   rectangle.setColor( rLocation, gLocation, bLocation);
					   tfBlue.setText(String.valueOf(bLocation));
					   setTitle("Color Sampler*");
				   }
			  }

			else if( e.getSource() == saveBut )
			  {
				  // save color
				  index = colorList.getSelectedIndex();
				  redArray[index] = rLocation;
				  greenArray[index] = gLocation;
				  blueArray[index] = bLocation;
				  setTitle("Color Sampler");
			  }

			else if(e.getSource() == resetBut)
			  {
				  // reset color
			  	index = colorList.getSelectedIndex();
				  rLocation = redArray[index];
				  gLocation = greenArray[index];
			  	bLocation = blueArray[index];
			  	tfRed.setText(String.valueOf(rLocation));
			  	tfGreen.setText(String.valueOf(gLocation));
				  tfBlue.setText(String.valueOf(bLocation));
				  rectangle.setColor( rLocation, gLocation, bLocation);
				  setTitle("Color Sampler");
			  }
		  }
	}

	class Shape extends JComponent
	  {
		  //initalizing variables
		  ColorSampler gui;
		  Color c;

		  public void draw( ColorSampler x )
		    {
			     // initializing members
			     gui = x;
			     c = new Color(255,255,255);
		    }

		  public void paint(Graphics g)
		    {
			    Dimension d = getSize();
			    g.setColor(c);
		  	  g.fillRect(1, 1, d.width-2, d.height-2);
		  	  g.setColor(c);
			    g.drawRect(1, 1, d.width-2, d.height-2);
	  	  }

		  public void setColor(int r, int g, int b )
		    {
		  	  c = new Color(r,g,b);
		  	  repaint();
		    }
	  }

//handling list selection
class ListSelectionHandler implements ListSelectionListener
	{
		public void valueChanged(ListSelectionEvent e)
		{
			//initalize variables
			int index = 0;
			index = colorList.getSelectedIndex();

			//Make sure index is within bounds of array
			if( index > -1 || index < 11 )
			{
				// paint new color
				rLocation = redArray[index];
				gLocation = greenArray[index];
				bLocation = blueArray[index];
				currentColorName = colorArray[index];
				tfRed.setText(String.valueOf(rLocation));
				tfGreen.setText(String.valueOf(gLocation));
				tfBlue.setText(String.valueOf(bLocation));
				rectangle.setColor( rLocation, gLocation, bLocation);
				setTitle("Color Sampler");
			}
		}
	}

	//read write functionality
	class FileIO
	{
		//read from file
		public void readInData(String[] name, int[] red, int[] green, int[] blue) throws IOException
		{
			//initalizing variables
			int index = 0;
		  	FileInputStream stream = new FileInputStream("colors.txt");
    	    InputStreamReader reader = new InputStreamReader(stream);
    	    StreamTokenizer tokens = new StreamTokenizer(reader);

    	    while(tokens.nextToken() != tokens.TT_EOF)
    	    {
    	    	//Read in values from file
    	        name[index] = (String) tokens.sval;
    	      	tokens.nextToken();
    	       	red[index] = (int) tokens.nval;
    	       	tokens.nextToken();
    	       	green[index] = (int) tokens.nval;
    	       	tokens.nextToken();
    	       	blue[index] = (int) tokens.nval;

    	       	index++;
    	    }
    	   	stream.close();
		}

		//store data to out file
		public void storeData(String[] name, int[] red, int[] green, int[] blue) throws IOException
		{
			//initializing variables
			int index = 0;
			FileOutputStream outStream = new FileOutputStream("outputFile.txt");
			PrintWriter writer = new PrintWriter(outStream);

			while(index < 11)
			  {
				  writer.println(name[index] + '\t' + red[index] + '\t' + green[index] + '\t' + blue[index]);
				  index++;
			  }
			writer.flush();
			outStream.close();
		 }
	}

class WindowDestroyer extends WindowAdapter
	 {
		 public void windowClosing(WindowEvent e)
 		 {
			 try
			  {
				  file.storeData(colorArray, redArray, greenArray, blueArray);
			  }
			 catch(IOException event)
		  	{
				  System.out.println("\nError: Please Try Again");
			  }
			 System.exit(0);
 		   }
	   }
}
