import java.util.*;

void calculateProcessingTime(Config, MetaDataCode&, int&, int&);
void readMetaDataFile(String, ArrayList<MetaDataCode>&);
void outputToLogFile(Config, ArrayList<MetaDataCode>);
void output(Config, ArrayList<MetaDataCode>, std::ostream&, int);

int main(int argc, char * argv[])
{
	String configFilePath = argv[1];
	Config cf = new Config();
	ArrayList<MetaDataCode> MetaDataVector = new ArrayList<MetaDataCode>();
	int systemStatus = 0;
	int applicationStatus = 0;

	cf.readConfigFile(configFilePath);

	readMetaDataFile(cf.getFilePath(), MetaDataVector);

	for (MetaDataCode mdc : MetaDataVector)
	{
		calculateProcessingTime(cf, mdc, systemStatus, applicationStatus);
	}

	outputToLogFile(cf, MetaDataVector);
	return 0;
}


// Takes the MetaDataCode vector and config file and outputs to log file
void outputToLogFile(Config cf, ArrayList<MetaDataCode> mdv)
{
	std::ofstream logFile = new std::ofstream();

	int loggedToOption = 0;
	// these flags are set depending on where the config specifies where to log to
	boolean monitorFlag = false;
	boolean logFileFlag = false;

	if (cf.getLogTo().equals("Both"))
	{
		monitorFlag = true;
		logFileFlag = true;
		loggedToOption = 0;
	}
	else if (cf.getLogTo().equals("monitor"))
	{
		monitorFlag = true;
		loggedToOption = 1;
	}
	else if (cf.getLogTo().equals("file"))
	{
		logFileFlag = true;
		loggedToOption = 2;
	}
	else
	{
		System.err.println("Can't log to " + cf.getLogTo()); //std::cerr << "Cannot log to " << cf.getLogTo() << "!\n";
		System.exit(1);
	}

	if (monitorFlag)
	{
		output(cf, mdv, std::cout, loggedToOption);
	}

	if (logFileFlag)
	{
		logFile.open(cf.getLogFilePath());
		output(cf, mdv, logFile, loggedToOption);
		logFile.close();
	}
}

// Takes an ostream obj (cout or ofstream) and outputs the text to the log file
void output(Config cf, ArrayList<MetaDataCode> mdv, std::ostream & out, int loggedToOption)
{
	out << "Configuration File Data" << std::endl;
	out << "Monitor = " << cf.getMDT() << " ms/cycle" << std::endl;
	out << "Processor = " << cf.getPCT() << " ms/cycle" << std::endl;
	out << "Scanner = " << cf.getSCT() << " ms/cycle" << std::endl;
	out << "Hard Drive = " << cf.getHCT() << " ms/cycle" << std::endl;
	out << "Keyboard = " << cf.getKCT() << " ms/cycle" << std::endl;
	out << "Memory = " << cf.getMemCT() << " ms/cycle" << std::endl;
	out << "Projector = " << cf.getProCT() << " ms/cycle" << std::endl;

	// loggedToOption is chosen in outputToLogFile
	// it provides where to log
	if (loggedToOption == 0)
	{
		out << "Logged to: monitor and " << cf.getLogFilePath() << std::endl;
	}
	else if (loggedToOption == 1)
	{
		out << "Logged to: " << cf.getLogTo() << std::endl;
	}
	else if (loggedToOption == 2)
	{
		out << "Logged to: " << cf.getLogFilePath() << std::endl;
	}

	out << std::endl;
	out << "Meta-Data Metrics" << std::endl;

//C++ TO JAVA CONVERTER TODO TASK: There is no equivalent to implicit typing in Java unless the Java 10 inferred typing option is selected:
	for (auto it = mdv.begin(); it != mdv.end(); it++)
	{
		MetaDataCode mdc = it;
		if (!(mdc.getCode() == 'S') && !(mdc.getCode() == 'A'))
		{
			out << mdc.getData() << " - " << mdc.getProcessingTime() << " ms" << std::endl;
		}
	}
}

// Gets the filepath from the config and then reads the MetaData file into the MetaDataVector
// by constructing an object of each MetaDataCode and inserts it into the vector
void readMetaDataFile(String filePath, ArrayList<MetaDataCode>& MetaDataVector)
{
	std::ifstream metaDataFile = new std::ifstream();
	metaDataFile.open(filePath);

	ArrayList<String> tokens = new ArrayList<String>();
	String s;
	String temp;

	char codeInput;
	String descriptorInput;
	int cyclesInput;
	boolean readOverFlag = false;

//C++ TO JAVA CONVERTER WARNING: The right shift operator was not replaced by Java's logical right shift operator since the left operand was not confirmed to be of an unsigned type, but you should review whether the logical right shift operator (>>>) is more appropriate:
	while (metaDataFile >> s != 0)
	{
		if (s.indexOf("hard") != -1)
		{
//C++ TO JAVA CONVERTER WARNING: The right shift operator was not replaced by Java's logical right shift operator since the left operand was not confirmed to be of an unsigned type, but you should review whether the logical right shift operator (>>>) is more appropriate:
			metaDataFile >> temp;
			s.append(" ");
			s.append(temp);
		}

		tokens.add(s);
	}

	metaDataFile.close();

	// iterates over vector
	for (String it : tokens)
	{
		if (it.equals("Start"))
		{
			std::advance(it, 4);
		}
		else if (it.equals("End"))
		{
			break;
		}
		else if (readOverFlag)
		{
			// Gets thrown if another process is read after the period '.'
			System.err.println("Can't find end.");
			System.exit(1);
		}

		s = it;

		codeInput = s.charAt(0);
		s = s.substring(0, 0) + s.substring(0 + 2);

		descriptorInput = s.substring(0, s.indexOf('}'));
		s = s.substring(0, 0) + s.substring(0 + s.indexOf('}') + 1);

		// Gets the cycle number
		temp = s.substring(0, s.indexOf(';'));

		// this finds out if the process ends in a period
		// which indicates it is the last process to be read.
		if (temp.indexOf('.') != -1)
		{
			readOverFlag = true;
			s = s.substring(0, s.indexOf('.')) + s.substring(s.indexOf('.') + 1);
		}

		cyclesInput = Integer.parseInt(temp);

		// need to delete semicolon
		s = it;
		s = s.substring(0, std::remove(s.iterator(), s.end(), ';')) + s.substring(std::remove(s.iterator(), s.end(), ';') + s.end());

		MetaDataCode mdcTemp = new MetaDataCode(codeInput, descriptorInput, cyclesInput, s);
    MetaDataVector.add(mdcTemp);
    }
  }
}
// Gets code and validates descriptor and calculates process time
// Throws error if system or application order does not make sense (finishing before starting application)
	public static void calculateProcessingTime(Config cf, MetaDataCode mdc, tangible.RefObject<Integer> systemStatus, tangible.RefObject<Integer> applicationStatus)
	{
		if (mdc.getCode() == 'S')
		{
			if (mdc.getDescriptor().equals("begin") && systemStatus.argValue == 0)
			{
				systemStatus.argValue = 1;
			}
			else if (mdc.getDescriptor().equals("finish") && systemStatus.argValue == 1 && applicationStatus.argValue == 0)
			{
				systemStatus.argValue = 2;
			}
			else
			{
				std::cerr << "Missing begin or finish operation for OS!\n";
				System.exit(1);
			}
		}
		else if (mdc.getCode() == 'A')
		{
			if (mdc.getDescriptor().equals("begin") && applicationStatus.argValue == 0)
			{
				applicationStatus.argValue = 1;
			}
			else if (mdc.getDescriptor().equals("finish") && applicationStatus.argValue == 1)
			{
				applicationStatus.argValue = 0;
			}
			else
			{
				std::cerr << "Missing begin or finish operation for OS!\n";
				System.exit(1);
			}
		}
		else if (mdc.getCode() == 'P' && mdc.getDescriptor().equals("run"))
		{
			mdc.setProcessingTime(mdc.getCycles() * cf.getPCT());
		}
		else if (mdc.getCode() == 'I')
		{
			if (mdc.getDescriptor().equals("hard drive"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getHCT());
			}
			else if (mdc.getDescriptor().equals("keyboard"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getKCT());
			}
			else if (mdc.getDescriptor().equals("scanner"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getSCT());
			}
			else
			{
				std::cerr << "Invalid descriptor!" << std::endl;
				System.exit(1);
			}
		}
		else if (mdc.getCode() == 'O')
		{
			if (mdc.getDescriptor().equals("hard drive"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getHCT());
			}
			else if (mdc.getDescriptor().equals("monitor"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getMDT());
			}
			else if (mdc.getDescriptor().equals("projector"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getProCT());
			}
			else
			{
				std::cerr << "Invalid descriptor!" << std::endl;
				System.exit(1);
			}
		}
		else if (mdc.getCode() == 'M')
		{
			if (mdc.getDescriptor().equals("block"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getMemCT());
			}
			else if (mdc.getDescriptor().equals("allocate"))
			{
				mdc.setProcessingTime(mdc.getCycles() * cf.getMemCT());
			}
			else
			{
				std::cerr << "Invalid descriptor!" << std::endl;
				System.exit(1);
			}
		}
	}

// Gets the filepath from the config and then reads the MetaData file into the MetaDataVector
// by constructing an object of each MetaDataCode and inserts it into the vector
	public static void readMetaDataFile(String filePath, ArrayList<MetaDataCode> MetaDataVector)
	{
		std::ifstream metaDataFile = new std::ifstream();
		metaDataFile.open(filePath);

		ArrayList<String> tokens = new ArrayList<String>();
		String s;
		String temp;

		char codeInput;
		String descriptorInput;
		int cyclesInput;
		boolean readOverFlag = false;

//C++ TO JAVA CONVERTER WARNING: The right shift operator was not replaced by Java's logical right shift operator since the left operand was not confirmed to be of an unsigned type, but you should review whether the logical right shift operator (>>>) is more appropriate:
		while (metaDataFile >> s != 0)
		{
			if (s.indexOf("hard") != -1)
			{
//C++ TO JAVA CONVERTER WARNING: The right shift operator was not replaced by Java's logical right shift operator since the left operand was not confirmed to be of an unsigned type, but you should review whether the logical right shift operator (>>>) is more appropriate:
				metaDataFile >> temp;
				s.append(" ");
				s.append(temp);
			}

			tokens.add(s);
		}

		metaDataFile.close();

		// iterates over vector
		for (String it : tokens)
		{
			if (it.equals("Start"))
			{
				std::advance(it, 4);
			}
			else if (it.equals("End"))
			{
				break;
			}
			else if (readOverFlag)
			{
				// Gets thrown if another process is read after the period '.'
				std::cerr << "Cannot find end!" << std::endl;
				System.exit(1);
			}

			s = it;

			codeInput = s.charAt(0);
			s = s.substring(0, 0) + s.substring(0 + 2);

			descriptorInput = s.substring(0, s.indexOf('}'));
			s = s.substring(0, 0) + s.substring(0 + s.indexOf('}') + 1);

			// Gets the cycle number
			temp = s.substring(0, s.indexOf(';'));

			// this finds out if the process ends in a period
			// which indicates it is the last process to be read.
			if (temp.indexOf('.') != -1)
			{
				readOverFlag = true;
				s = s.substring(0, s.indexOf('.')) + s.substring(s.indexOf('.') + 1);
			}

			cyclesInput = Integer.parseInt(temp);

			// need to delete semicolon
			s = it;
			s = s.substring(0, std::remove(s.iterator(), s.end(), ';')) + s.substring(std::remove(s.iterator(), s.end(), ';') + s.end());

			MetaDataCode mdcTemp = new MetaDataCode(codeInput, descriptorInput, cyclesInput, s);
			MetaDataVector.add(mdcTemp);
		}
	}
