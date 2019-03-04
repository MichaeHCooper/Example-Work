import javax.swing.*;

import java.awt.Color;
import java.awt.Component;
import java.awt.GridLayout;
import java.awt.event.*;
import java.io.IOException;

//#################################################################################90chars
 
class Main
{
	public static JFrame frame = new JFrame();
	// Instantiates the frame.
	public static int size = 11;
	// The map size including borders.
	public static JLabel[][] guiMap = new JLabel[size][size];
	// Creates an array of the labels representing each tile.
	public static int topLeftX = 300;
	public static int topLeftY = 15;
	// Specifies the top left corner of the map
	public static int numCoins;
	// Specifies the number of coins in the map.

	public static ImageIcon emptyTile   = new ImageIcon("Assets/emptyTile.png"  );
	public static ImageIcon coinTile    = new ImageIcon("Assets/coinTile.png"   );
	public static ImageIcon wallTile    = new ImageIcon("Assets/wallTile.png"   );
	public static ImageIcon player1Tile = new ImageIcon("Assets/player1Tile.png");
	public static ImageIcon player2Tile = new ImageIcon("Assets/player2Tile.png");
	public static ImageIcon title = new ImageIcon("Assets/title.png");
	// Boots up image icons of the tiles.
	
	public static int numBots;
	// This is the number of bots per team.
	// Even bots are team 1.
	// Odd bots are team 2.
	public static int turns = 0;
	// Number of turns the game has done.
	public static int modTurns;
	// The number of turns each play can have between being able to modify ones code.
	public static MainMap mainMap;
	// Creates the actual game map
	
	
	public static JLabel score1 = new JLabel("Score Player 1: 0");
	public static JLabel score2 = new JLabel("Score Player 2: 0");
	// Create the score labels for the game.

	public static JLabel turnLabel = new JLabel("Turn 0");
	// the turn label, which shows the current turn number.
	
	public static Color  white = new Color(255, 255, 255);
	public static Color  grey  = new Color(200, 200, 200);
	// Initialises some colours to use for the games GUI.
	
	public static JTextArea[] inputs;
	// The array of text areas.
	public static JScrollPane[] scrolls;
	// The array of scrolling areas.
	public static JPanel[] tabs;
	// The array of each of the tabs.
	public static JTextField[] lineLocs;
	// The array of the lineLoc fields.
	public static BotProgram[] botPrograms;
	
	public static int curBot = 0;
	// Keeps track of the current bot in the game.
	

	public static void main(String[] args)
	{
		JTextField numBotInput = new JTextField("2",15);
		JTextField numCoinsInput = new JTextField("10",15);
		JTextField numTurnsInput = new JTextField("5",15);
		// Initialising the text entry fields for the title panel.
		JFrame startFrame = new JFrame();
		// Creates the title panel.
		
		ActionListener startGame = new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				startGame(Integer.valueOf(numBotInput.getText()),
						  Integer.valueOf(numCoinsInput.getText()),
						  Integer.valueOf(numTurnsInput.getText()));
				// This initialises a new game as a frame, also inputs the vales into the
				// text box as arguments. This is to boot the game up with a custom number
				// of bots, coins and turns between modding.
			}
		};
		// Action listener waiting to see if start game is clicked, if clicked runs the
		// start game function.
		
		JButton start = new JButton("Start");
		start.setBounds(120,300,80,25);
		start.addActionListener(startGame);
		// Actually creates the start game button
		
		JLabel numBotLabel = new JLabel("Number of Bots Per Team:");
		JLabel numCoinsLabel = new JLabel("Number of Coins:");
		JLabel numTurnsLabelA = new JLabel("Number of Turns Between");
		JLabel numTurnsLabelB = new JLabel("Code Modification:");
		// Creates the labels for the buttons and text areas.
		
		JLabel titleLabel = new JLabel();
		titleLabel.setIcon(title);
		// Adds the title for the title panel.
		
		numBotInput.setBounds(195,150,80,25);
		numCoinsInput.setBounds(195,200,80,25);
		numTurnsInput.setBounds(195,250,80,25);
		numBotLabel.setBounds(40,150,160,25);
		numCoinsLabel.setBounds(40,200,160,25);
		numTurnsLabelA.setBounds(40,240,160,25);
		numTurnsLabelB.setBounds(40,260,160,25);
		titleLabel.setBounds(10,10,300,113);
		// Sets the boundaries of the various components.
		
		startFrame.add(start);
		startFrame.add(numBotInput);
		startFrame.add(numCoinsInput);
		startFrame.add(numTurnsInput);
		startFrame.add(numBotLabel);
		startFrame.add(numCoinsLabel);
		startFrame.add(numTurnsLabelA);
		startFrame.add(numTurnsLabelB);
		startFrame.add(titleLabel);
		// Adds the components to the frame.
		
		startFrame.setSize(335,400);//400 width and 500 height
		startFrame.setLayout(null);//using no layout managers
		startFrame.setVisible(true);//making the frame visible
	}
	
	public static void startGame(int Bots, int Coins, int Turns)
	{
		/*
		The start game function initialises a new game as a separate panel.  Furthermore
		this is responsible for the overarching running of each game.
		*/
		numCoins = Coins;
		int numBotsIn = Bots;
		int modTurnsIn = Turns;
		// sets the number of coins, bots and turns between code modification.
		
		numBots = numBotsIn*2;
		// Number of bots to load the map up with, this is double what is input as it is
		// the total.
		modTurns = modTurnsIn*(numBots/2);
		// Number of turns between code modification, this is multiplied by the number of
		// bots as numTurns is the actual number of turns as opposed to what is displayed
		// on the screen, which only increases after all bots have moved.
		mainMap = new MainMap(size-2, numBots);
		// The new main map.
		inputs = new JTextArea[numBots];
		// Array holding all of the text panels. This allows later access.
		scrolls = new JScrollPane[numBots];
		// Array holding all of the scroll panels. This allows later access.
		tabs = new JPanel[numBots];
		// Array holding all of the panels, which are the tabs.
		lineLocs = new JTextField[numBots];
		// Array holding the textFields. This allows later access.
		botPrograms = new BotProgram[numBots];
		// Array of all the BotPrograms for each loaded bot.
		
		mainMap.addBots();
		mainMap.addCoins(numCoins);
		// Instantiates map variables.

		ActionListener nextEvent = new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				singleTurn();
			}
		};
		// Creates the action listener for to run the game.
		
		ActionListener nextMultiEvent = new ActionListener()
		{
			@Override
			public void actionPerformed(ActionEvent e)
			{
				multipleTurn();
			}
		};
		// Creates the action listener to run the game for 20 auto turns.

		JButton next = new JButton("Next");
		next.setBounds(170+topLeftX,600,80,25);
		next.addActionListener(nextEvent);
		frame.add(next);
		JButton skip = new JButton("Skip");
		skip.setBounds(250+topLeftX,600,80,25);
		skip.addActionListener(nextMultiEvent);
		frame.add(skip);
		// Creates the button to run the game.
		
		score1.setBounds(50+topLeftX,600,200,25);
		score2.setBounds(350+topLeftX,600,200,25);
		frame.add(score1);
		frame.add(score2);
		// Adds the score labels to the frame.
		
		turnLabel.setBounds(250+topLeftX,630,200,25);
		frame.add(turnLabel);
		// Adds the turn counter.
		
		JTabbedPane team1 = new JTabbedPane();
		JTabbedPane team2 = new JTabbedPane();
		team1.setBounds(15,15,270,600);
		team2.setBounds(865,15,270,600);
		// Creates the tabbed panes for the game.
		
		for (int i=0; i<numBots; i++)
		{
			makeTextArea(i);
			if (i%2 == 0)
			{
				// If bot number is even then adds to team1 pane
				team1.add("Bot "+Integer.toString((i/2)+1), tabs[i]);
			}
			else
			{
				// If bot number is odd then adds to team2 pane
				team2.add("Bot "+Integer.toString((i+1)/2), tabs[i]);
			}
		}
		// This loop creates each pane for the tabbed panes.

		frame.add(team1);
		frame.add(team2);
		// Adds the tabbed panes.
		
		addMap();
		updateMap();
		// Updates the map once to add images.
		
		frame.setSize(1165,700);//400 width and 500 height
		frame.setLayout(null);//using no layout managers
		frame.setVisible(true);//making the frame visible
	}
	
	public static void addMap()
	{
		/*
		This method is to add all of the labels to the map on which the map tile icons
		will be painted.
		*/
		for (int i=0; i<size; i++)
		{
			for (int j=0; j<size; j++)
			{
				int x = i*50+topLeftX;
				int y = j*50+topLeftY;
				int w = 50;
				int h = 50;
				guiMap[i][j] = new JLabel();
				guiMap[i][j].setBounds(x,y,w,h);
				frame.add(guiMap[i][j]);
			}
		}
	}

	public static void updateMap()
	{
		/*
		This method simply prints the current map to the GUI, it is analogous to
		MainMap.printMap();. The function update all of the label icons representing the
		map tile.
		*/
		for (int i=mainMap.size-1; i>=0; i--)
		{
			// Print out the map into the canvas.
			for (int j=0; j<mainMap.size; j++)
			{
				
				if (mainMap.map.get(j).get(i).obstacles.size() > 0)
				{
					guiMap[j][mainMap.size-1-i].setIcon(wallTile);
					guiMap[j][mainMap.size-1-i].setToolTipText("");
				}
				// Draws the walls.
				else if (mainMap.map.get(j).get(i).collectables.size() > 0)
				{
					guiMap[j][mainMap.size-1-i].setIcon(coinTile);
					guiMap[j][mainMap.size-1-i].setToolTipText("");
				}
				// Draws the coins.
				else if (mainMap.map.get(j).get(i).bots.size() > 0)
				{
					if (mainMap.map.get(j).get(i).bots.get(0).name%2 != 0)
					{
						guiMap[j][mainMap.size-1-i].setIcon(player1Tile);
						String text = "bot ";
						text += Integer.toString(
								(mainMap.map.get(j).get(i).bots.get(0).name/2)+1);
						text += ", Player 1";
						guiMap[j][mainMap.size-1-i].setToolTipText(text);
					}
					// Draws player 1.
					if (mainMap.map.get(j).get(i).bots.get(0).name%2 == 0)
					{
						guiMap[j][mainMap.size-1-i].setIcon(player2Tile);
						String text = "bot ";
						text += Integer.toString(
								(mainMap.map.get(j).get(i).bots.get(0).name+1)/2);
						text += ", Player 2";
						guiMap[j][mainMap.size-1-i].setToolTipText(text);
					}
					// Draws player 2.
				}
				else
				{
					guiMap[j][mainMap.size-1-i].setIcon(emptyTile);
					guiMap[j][mainMap.size-1-i].setToolTipText("");
				}
				// Draws empty tiles.
			}
		}
	}
	
	public static void nextTurn()
	{
		/*
		This function performs the backend game update performing each move for a bot
		and updating the MainMap.
		*/
        mainMap.moveBot(botPrograms[curBot].Next(mainMap), curBot+1);
        curBot++;
        turns++;
        if (curBot%numBots == 0)
        {
        	curBot = 0;
        }
	}
	
	public static void singleTurn()
	{
		/*
		Wraps up all of the code required to run a single turn of the game, including
		reading all of the code for each bot, updating the MainMap, then finally updating
		all of the graphics on the screen.
		*/
		for (int i=0; i<numBots; i++)
		{
			if ( ((turns+1)%(2*modTurns)) == 0)
			{
				inputs[i].setEditable(true);
				inputs[i].setBackground(white);
				lineLocs[i].setEditable(true);
				lineLocs[i].setBackground(white);
				// Editable if multiple of modTurns.
			}
			else
			{
				inputs[i].setEditable(false);
				inputs[i].setBackground(grey);
				lineLocs[i].setEditable(false);
				lineLocs[i].setBackground(grey);
				// Not editable if not multiple of modTurns.
			}
			botPrograms[i].ReadString(inputs[i].getText());
			botPrograms[i].LineLoc = Integer.valueOf(lineLocs[i].getText());
			// Reads the program and sets the lineLoc.
		}
		
		nextTurn();
		// Performs the next turn.
		updateMap();
		// Updates the map.

		turnLabel.setText("Turn "+Integer.toString(turns/numBots));
		// reads the current turn and prints to screen.
		int scoreCount1 = 0;
		int scoreCount2 = 0;
		
		for (int i=0; i<numBots; i++)
		{
			lineLocs[i].setText(Integer.toString(botPrograms[i].LineLoc));
			// Reads the current line location.
			if (i%2 == 0)
			{
				scoreCount1 += mainMap.botList.botList.get(i).score;
			}
			else
			{
				scoreCount2 += mainMap.botList.botList.get(i).score;
			}
		}
		
		score1.setText("Score Player 1: "+Integer.toString(scoreCount1));
		score2.setText("Score Player 2: "+Integer.toString(scoreCount2));
		// Reads the current scores and prints them to screen.
	}
	
	public static void multipleTurn()
	{
		/*
		Runs until the next modification point is reached.
		*/
		singleTurn();
		while ( (turns%(2*modTurns)) != 0 )
		{
			singleTurn();
		}
	}
	
	public static void makeTextArea(int i)
	{
		/*
		This function creates the individual pane for the tabbed panes, this consists of
		a scrolling text area, and the line location text area and label.  Furthermore
		it also initialises the bot program, this is because it is a convinient place to
		do so.
		*/
		tabs[i] = new JPanel();
		// Tab
		inputs[i] = new JTextArea(32,22);
		inputs[i].setText("end program");
		// Input
		scrolls[i] = new JScrollPane(inputs[i]);
		// Scroll
		lineLocs[i] = new JTextField("0",15);
		// LineLoc
		scrolls[i].setVerticalScrollBarPolicy
		(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
		// Sets the Input scroll bar to visible.
		JLabel labelA = new JLabel("Line Location:");
		tabs[i].add(scrolls[i]);
		tabs[i].add(labelA);
		tabs[i].add(lineLocs[i]);
		frame.add(tabs[i]);
		
		botPrograms[i] = new BotProgram(i+1);
		// initialises the bot programs.
	}
}