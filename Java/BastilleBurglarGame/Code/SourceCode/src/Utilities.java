import java.util.Random;

public class Utilities
{
	/*
	This is a collection of useful but unrelated functions.
	*/

	public static int randomNumber(int low, int high)
	{
	    //Generates a random number between two integers.
			Random r = new Random();
	    //r.setSeed(x); //!!!!!!!! SEED !!!!!!
			int result = r.nextInt(high-low) + low;
			return result;
	}
}