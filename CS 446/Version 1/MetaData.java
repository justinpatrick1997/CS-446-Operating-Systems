import java.util.*;
import java.io.*;
public class MetaData
{
		// Main Constructor

		// constructor
		public MetaData(char codeInput, String descriptorInput, int cyclesInput, String dataInput)
		{
			this.code = codeInput;
			this.descriptor = descriptorInput;
			this.cycles = cyclesInput;
			this.data = dataInput;
		}


		// only setter since I calculate processing time after construction
		public final void setProcessingTime(int processingTimeInput)
		{
			this.processingTime = processingTimeInput;
		}


		// getters
		public final char getCode()
		{
			return this.code;
		}
		public final String getDescriptor()
		{
			return this.descriptor;
		}
		public final int getCycles()
		{
			return this.cycles;
		}
		public final String getData()
		{
			return this.data;
		}
		public final int getProcessingTime()
		{
			return this.processingTime;
		}
		private char code;
		private String descriptor;
		private int cycles;
		private String data;

		private int processingTime;
}
