import java.util.ArrayList;

public class MainMap
{
	/*
	This is the Map object, an ArrayList of ArrayLists of MapTiles
	*/
	public ArrayList< ArrayList<MapTile> > map = new ArrayList< ArrayList<MapTile> >();
	public BotList botList = new BotList();
	public int size = 0;
	public int numBots;
	
	public MainMap(int width, int numBots)
	{
		this.numBots = numBots;
		
		// Instantiates a square map of the given size and puts walls around it.
		size = width+2;
		
		for (int i=0; i<size; i++)
		{
			map.add(new ArrayList<MapTile>()); // instantiates each row.
			for (int j=0; j<size; j++)
			{
				map.get(i).add(new MapTile()); // instantiates each column in each row.
			}
		}
		// Instantiates an empty map.
		
		for (int i=0; i<size; i++)
		{
			map.get(0).get(i).obstacles.add(new Obstacle());
			// Adds walls to the first row.
		}
		for (int i=1; i<size-1; i++)
		{
			map.get(i).get(0).obstacles.add(new Obstacle());
			map.get(i).get(size-1).obstacles.add(new Obstacle());
			// Adds walls to the first and last elements of intermediate rows
		}
		for (int i=0; i<size; i++)
		{
			map.get(size-1).get(i).obstacles.add(new Obstacle());
			// Adds walls to the last row.
		}
		// Adds borders to the map.
	}
	
	public void addBots()
	{
		// Function to add two bots to the map and botlist, one in the bottom left, and
		// one in the top right.
		int j =0;
		for (int i=0; i<numBots; i++)
		{
			if (i%2 == 0)
			{
				map.get(1).get(1+j).bots.add(new Bot(i+1, 1, 1, 1+j));
				botList.botList.add(new Bot(i+1, 1, 1, 1+j));
			}
			else
			{
				map.get(size-2).get(size-2-j).bots.add(new Bot(i+1, 2, size-2, size-2-j));
				botList.botList.add(new Bot(i+1, 2, size-2, size-2-j));
				j++;
			}
		}
	}

	public void addCoins(int number)
	{
		// Adds a specified amount of coins to the map in random locations
		
		for (int i=0; i<number; i++)
		{
			int x = Utilities.randomNumber(1,size-1);
			int y = Utilities.randomNumber(1,size-1);
			if ((map.get(x).get(y).collectables.size() < 1)&&
			    (map.get(x).get(y).bots.size() < 1))
			{
				map.get(x).get(y).collectables.add(new Collectable());
			}
			else
			{
				i--;
			}
		}	
	}
	
	public void moveBot(String Command, int Name)
	{
		// This function moves the named bot in a certain direction.
		// It firstly searches for the named bot in the botList, then uses this to call
		// up the location of the bot in the map. It then checks if the move can actually
		// be made, if it can, the function then updates both the location on the map and
		// the location of the bot in the BotList.

		int curX = -1;
		int curY = -1;
		int botNumber = -1; // The current bot's location in the botList.
		int moveX = 0;
		int moveY = 0;
		Boolean validMove = false; // States if the move is valid or not.

		if (Command.equals("up"))
		{
			moveY = 1;
		}
		if (Command.equals("down"))
		{
			moveY = -1;
		}
		if (Command.equals("right"))
		{
			moveX = 1;
		}
		if (Command.equals("left"))
		{
			moveX = -1;
		}
		// This section sets the move vector for the bot from the given command.
		
		botNumber = botListLoc(Name);
		curX = botList.botList.get(botNumber).x;
		curY = botList.botList.get(botNumber).y;
		// This is the first step.  It retrieves the current location of the named bot.
		
		if ((map.get(curX+moveX).get(curY+moveY).obstacles.size() < 1)&&
			(map.get(curX+moveX).get(curY+moveY).bots.size() < 1))
		{
			validMove = true;
		}
		// This section checks that the bot is not attempting to move into an occupied
		// tile.
		
		if (validMove == true)
		{
			botList.botList.get(botNumber).x = curX+moveX;
			botList.botList.get(botNumber).y = curY+moveY;
			// Sets the x and y values for the bot in the bot list.
			map.get(curX).get(curY).bots.get(0).x = curX+moveX;
			map.get(curX).get(curY).bots.get(0).y = curY+moveY;
			// Sets the x and y values for the bot in the map.
			map.get(curX+moveX).get(curY+moveY).bots.add(
					map.get(curX).get(curY).bots.get(0));
			// Sets the bot of the new tile as the old bot.
			map.get(curX).get(curY).bots.remove(0);
			// Removes the bot from the old tile.
			if (map.get(curX+moveX).get(curY+moveY).collectables.size() > 0)
			{
				int score = map.get(curX+moveX).get(curY+moveY).
						collectables.get(0).score;
				// Gets the score assigned to the coin.
				botList.botList.get(botNumber).score += score;
				// Updates the score for the botList bot.
				map.get(curX+moveX).get(curY+moveY).bots.get(0).score += score;
				// Updates the score for the map bot.
				map.get(curX+moveX).get(curY+moveY).collectables.remove(0);
				// Removes the collectable.
			}
		}
		// This section then moves the bot and u[dates the score if it moves onto a coin.
		
		if ((validMove == false)&&(!Command.equals("end")))
		{
			System.out.println("invalid Move!");
		}
		// Prints out invalid move if the bot cannot take the move when it tries to.
	}
	
	public int botListLoc(int Name)
	{
		// finds the botList location given the name of the bot.
		int botNumber = -1;
		for (int i=0; i<botList.botList.size(); i++)
		{
			if (botList.botList.get(i).name == Name)
			{
				botNumber = i;
			}
		}
		return botNumber;
	}
	
	public void printMap()
	{
		/*
		Function to print the map to the command line.  This is useful for maintaining
		the code.
		*/
		String mapAll = "";
		for (int i=size-1; i>=0; i--)
		{
			// Print out every row.
			String mapRow = "";
			for (int j=0; j<size; j++)
			{
				if (map.get(j).get(i).obstacles.size() > 0)
				{
					mapRow += " #";
				}
				else if (map.get(j).get(i).collectables.size() > 0)
				{
					mapRow += " $";
				}
				else if (map.get(j).get(i).bots.size() > 0)
				{
					mapRow += " " + Integer.toString(
							map.get(j).get(i).bots.get(0).name);
				}
				else
				{
					mapRow += "  ";
				}
			}
			mapAll += mapRow+"\n";
		}
		System.out.println(mapAll);
	}
}




