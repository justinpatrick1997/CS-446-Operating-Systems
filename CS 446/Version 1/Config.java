import java.util.*;
import java.io.*;
public class Config
{

		// Nothing since readConfigFile fills the object
		public Config()
		{
		}

		// Reads entire file into a string, then splits string into tokens and parsed one by one
		public final void readConfigFile(String configPath)
		{
			// File stream
      FileInputStream configFile = null;
			configFile.open(configPath);

			// Throw error if unable to open file
			if (configFile == null)
			{
				System.err.println("Unable to open file."); //std::cerr << "Unable to open file\n";
				System.exit(1);
			}

			// This vector holds each individual "token"
			ArrayList tokens = new ArrayList();
			String s;

			// Read a string of text up until whitespace and pushes to vector
      int c;
			while ((c = configFile.read()) != -1)
			{
				tokens.add(c);
			}

			// Iterates through vector checking for values
      Iterator itr = tokens.iterator();
			//for (Object it = tokens.begin(); it != tokens.end(); it++)
      while(itr.hasNext())
			{
        Object element = itr.next();
        int elemented = tokens.indexOf(itr);
				if (element.equals("Log:"))
				{
					this.logTo = (elemented + 3);
				}
				else if (element.equals("File"))
				{
					s = tokens.get(elemented + 2);
          boolean isPresent = s.indexOf(".mdf") != -1 ? true : false;
					if (isPresent)
					{
						this.filePath = s;
					}
				}
				else if ((it.next()).equals("Version/Phase:"))
				{
					this.version = Float.parseFloat(((it.next()) + 1));
				}
				else if ((it.next()).equals("Log"))
				{
					String temp = ((it.next()) + 3);
					if (temp.indexOf(".lgf") != -1)
					{
						this.logFilePath = temp;
					}
				}
				else if (en.equals("Monitor"))
				{
					this.monitorDisplayTime = Integer.parseInt(en+4);
				}
				else if (en.equals("Processor"))
				{
					this.processorCycleTime = Integer.parseInt(en+4);
				}
				else if (en.equals("Scanner"))
				{
					this.scannerCycleTime = Integer.parseInt(en+4);
				}
				else if (en.equals("Hard"))
				{
					this.harddriveCycleTime = Integer.parseInt(en+5);
				}
				else if (en.equals("Keyboard"))
				{
					this.keyboardCycleTime = Integer.parseInt(en+4);
				}
				else if (en.equals("Memory"))
				{
					this.memoryCycleTime = Integer.parseInt(en+4);
				}
				else if (en.equals("Projector"))
				{
					this.projectorCycleTime = Integer.parseInt(en+4);
				}
			}
			configFile.close();

			if (!this.validate())
			{
			  System.err.println("Missing data."); //	std::cerr << "Missing Data!\n" << std::endl;
				System.exit(1);
			}
		}

		// Validates the current config file to see if the parameters are valid
		// such as a cycletime should be greater than zero
		public final boolean validate()
		{
			boolean monitor = monitorDisplayTime > 0;
			boolean processor = this.processorCycleTime > 0;
			boolean scanner = this.scannerCycleTime > 0;
			boolean harddrive = this.harddriveCycleTime > 0;
			boolean keyboard = this.keyboardCycleTime > 0;
			boolean memory = this.memoryCycleTime > 0;
			boolean projector = this.projectorCycleTime > 0;

			boolean ver = this.version > 0;

			return monitor && processor && scanner && harddrive && keyboard && memory && projector && ver;
		}

		// getters
		public final String getFilePath()
		{
			return this.filePath;
		}
		public final int getMDT()
		{
			return this.monitorDisplayTime;
		}
		public final int getPCT()
		{
			return this.processorCycleTime;
		}
		public final int getSCT()
		{
			return this.scannerCycleTime;
		}
		public final int getHCT()
		{
			return this.harddriveCycleTime;
		}
		public final int getKCT()
		{
			return this.keyboardCycleTime;
		}
		public final int getMemCT()
		{
			return this.memoryCycleTime;
		}
		public final int getProCT()
		{
			return this.projectorCycleTime;
		}
		public final String getLogTo()
		{
			return this.logTo;
		}
		public final String getLogFilePath()
		{
			return this.logFilePath;
		}
		private float version;
		private String filePath;
		private int monitorDisplayTime;
		private int processorCycleTime;
		private int scannerCycleTime;
		private int harddriveCycleTime;
		private int keyboardCycleTime;
		private int memoryCycleTime;
		private int projectorCycleTime;

		private String logTo;
		private String logFilePath;

}
