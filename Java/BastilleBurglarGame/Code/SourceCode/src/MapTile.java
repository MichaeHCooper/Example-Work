import java.util.*;

public class MapTile
{
	/*
	This is a MapTile object, it is the collection of three different ArrayLists.
	Bots  		 - ArrayList of the Bots.
	Collectables - ArrayList of the Collectables.
	Obstacles    - ArrayList of the Obstacles.
	By having arrayLists we can either have arbitrary length lists, and epmty lists.  The
	empty lists are useful as these represent an empty tile.  This leads to complete
	flexibility in functionality.
	*/
	public ArrayList<Bot>         bots         = new ArrayList<Bot>()        ;
	public ArrayList<Collectable> collectables = new ArrayList<Collectable>();
	public ArrayList<Obstacle>    obstacles    = new ArrayList<Obstacle>()   ;
}