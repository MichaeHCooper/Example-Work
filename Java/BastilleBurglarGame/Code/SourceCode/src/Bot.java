public class Bot
{
	/*
	This is a bot object, it has several variables.
	Name  - this is the bot's name.
	Score - this is the current score that the bot has, equivalent to the number of
	        coins picked up.
	Owner - this is the current owner of the bot, for example player 1.
	x, y  - the location of the bot in the map, this is used as two copies of each bot
			are loaded up, one for the map and one for the botlist.  This is so that
			each bot can be quickly referenced.
	*/
	public int name;
	public int score = 0;
	public int owner;
	public int x;
	public int y;
	
	public Bot(int name, int owner, int x, int y)
	{
		this.name  = name;
		this.owner = owner;
		this.x     = x;
		this.y     = y;
	}
}