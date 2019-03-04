import java.io.*;
import java.util.*;

class BotProgram
{
  public String[][] Code;
  // The 2D array holding the code
  public int LineLoc;
  // An integer that keeps track of the location of the interpreter.
  Map Variables = new HashMap();
  // A dictionary to store variables in.
  int FileLength = 0;
  // Read file must be run first or else file length is simply 0.
  int botName;

  public BotProgram(int n)
  {
    // Constructor, this attaches a specific named bot to the program.
    botName = n;
  }

  public void ReadFile(String FileName)
  {
    // This method reads a program file then returns it as a 2D array of
    // strings, where each word is held in a subarray representing a line
    // and each line is held in the main array.
    try
    {
      FileReader frCode = new FileReader(FileName);
      BufferedReader brCode = new BufferedReader(frCode);
      String CodeLineStr;
      while((CodeLineStr = brCode.readLine()) != null)
      {
        FileLength++;
      }
      brCode.close();
      frCode.close();
    }
    catch(IOException e2){}
    // This section of code opens the file and reads each line to determine
    // in advance the number of lines in the file so that the array for code
    // can be correctly instasiated.
    Code = new String[FileLength][];
    // Creates an array of the file length to store the code.

    int Count = 0;
    try
    {
      FileReader frCode = new FileReader(FileName);
      BufferedReader brCode = new BufferedReader(frCode);
      String CodeLineStr;
      while((CodeLineStr = brCode.readLine()) != null)
      {
        CodeLineStr = removeLeadingSpaces(CodeLineStr);
        Code[Count] = CodeLineStr.split("\\s+");
        // Splits the string of the line into individual words.
        Count++;
      }
      brCode.close();
      frCode.close();
    }
    catch(IOException e2){System.out.println("File not read");}
    // Works in a very simmilar manner to the previous loop, however instead
    // of counting the code splits each line into an array of the words, then
    // adds these lines to the Code array.
  }

  public void ReadString(String File)
  {
    // This method reads a program file then returns it as a 2D array of
    // strings, where each word is held in a subarray representing a line
    // and each line is held in the main array.
    String[] CodeLines = File.split("\n");
    
    Code = new String[CodeLines.length][];
    // Creates an array of the file length to store the code.

    for (int i=0; i<CodeLines.length; i++)
    {
    	String CodeLineStr = removeLeadingSpaces(CodeLines[i]);
    	Code[i] = CodeLineStr.split("\\s+");
    }
  }
  
  public void PrintCode()
  {
    // This method is used solely for diagnostics to ensure that the ReadCodeFile
    // function is loading the code into the array correctly.
    for (int i=0; i<Code.length; i++)
    {
      for (int j=0; j<Code[i].length; j++)
      {
        System.out.print(Code[i][j]+"|");
      }
      System.out.print("\n");
    }
  }

  public String Next(MainMap mainMap)
  {
    // The purpose of this is to perform the next move in the program.  This does
    // two things, firstly it moves the pointer (LineLoc) to the location of the
    // be executed  next move to, then it returns the string of that move.  There
    // are five possible outputs 'up', 'down', 'left', 'right' and 'end'.  The end
    // signifier is special as it allows the program to end.

    // To allow the = after the variable simply do an "If code[i][2] == '=' do foo"
    // Simmilarly do the same thing with the + signs
    // Furthermore for the conditionals do two case functions, first checks for the
    // while loop, the second then checks for the equality symbol.
    // Variables are to be held in a dictionary of variable length, such that one
    // can simply call up and modify a dictionary by name.

    // It is very important to note that in the code all command which only have
    // one word go first !!

    // The map is passeed to the function, this allows the program to read the
    // current state of the map.
  
    int running = 0;
    while (running == 0) // Runs the loop for ever.
    {
      if ("print".equals(Code[LineLoc][0]))
      {
        // This is used as a diagnostic, prints a specified word.
        System.out.println(Code[LineLoc][1]);
        LineLoc++;
      }

      else if ("printvar".equals(Code[LineLoc][0]))
      {
        // This is used as a diagnostic, the function prints a variable.
        System.out.println(Variables.get(Code[LineLoc][1]).toString());
        LineLoc++;
      }

      else if ("up".equals(Code[LineLoc][0]))
      {
        // Up statement, moves line on by one and returns up.
        LineLoc ++;
        return "up";
      }

      else if ("down".equals(Code[LineLoc][0]))
      {
        // Down statement, moves line on by one and returns down.
        LineLoc ++;
        return "down";
      }

      else if ("left".equals(Code[LineLoc][0]))
      {
        // Left statement, moves line on by one and returns left.
        LineLoc ++;
        return "left";
      }

      else if ("right".equals(Code[LineLoc][0]))
      {
        // Right statement, moves line on by one and returns Right.
        LineLoc ++;
        return "right";
      }

      else if ("idle".equals(Code[LineLoc][0]))
      {
        // nothing statement statement, bot moves nowhere.
        LineLoc ++;
        return "end";
      }

      else if ("".equals(Code[LineLoc][0]))
      {
        // Checks for empty lines, these are usefull for spacing out a program
        LineLoc ++;
      }

      else if ("#".equals(Code[LineLoc][0]))
      {
        // Allows for comments in code
        LineLoc ++;
      }

      else if ("end".equals(Code[LineLoc][0]) && "program".equals(Code[LineLoc][1]))
      {
        // Returns the unique end statement if the program terminator is discovered.
        return "end";
      }

      else if ("=".equals(Code[LineLoc][1]))
      {
        // Assigns a variable to the variable map.  This function is versitile
        // and can handle overwriting too.  Note this stores the variable as
        // a string.
        Variables.put(Code[LineLoc][0], Code[LineLoc][2]);
        LineLoc ++;
      }

      else if ("+".equals(Code[LineLoc][1]))
      {
        // This overwrites the current variable with the named variable plus
        // a given value.
        int x = Integer.parseInt( Variables.get(Code[LineLoc][0]).toString() );
        // toString is neseccary as the map stores the data as java.lang.String
        int y = Integer.parseInt(Code[LineLoc][2]);
        Variables.put(Code[LineLoc][0], Integer.toString(x+y));
        // Adds the ints then converts back to a string.
        LineLoc ++;
      }

      else if ("-".equals(Code[LineLoc][1]))
      {
        // This overwrites the current variable with the named variable minus
        // a given value.
        int x = Integer.parseInt( Variables.get(Code[LineLoc][0]).toString() );
        // toString is neseccary as the map stores the data as java.lang.String
        int y = Integer.parseInt(Code[LineLoc][2]);
        Variables.put(Code[LineLoc][0], Integer.toString(x-y));
        // Adds the ints then converts back to a string.
        LineLoc ++;
      }

      else if ("while".equals(Code[LineLoc][0]))
      {
        // If the while statement is true, the program proceeds. Else the program
        // skips to the end of the while loop.
        int condition = Integer.parseInt( Variables.get(Code[LineLoc][1]).toString() );
        int variable = Integer.parseInt( Variables.get(Code[LineLoc][3]).toString() );

        if ("<".equals(Code[LineLoc][2])&&(condition < variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for less than.
          LineLoc ++;
        }

        else if (">".equals(Code[LineLoc][2])&&(condition > variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for greater than.
          LineLoc ++;
        }

        else if ("=".equals(Code[LineLoc][2])&&(condition == variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for parity.
          LineLoc ++;
        }

        else
        {
          // If the conditions are not true then the program proceeds to the end of
          // the loop.
          int NumberWhiles = 1;
          int NumberEnds = 0;
          while (NumberWhiles != NumberEnds)
          {
            // This particular bit checks the parity of the whiles seen and the end
            // loops seen, if they are equal then the end of the loop has been reached.
            // This is to handle nested loops.
            LineLoc++;
            if ("while".equals(Code[LineLoc][0]))
            {
              NumberWhiles++;
            }
            if ("end".equals(Code[LineLoc][0]) && "loop".equals(Code[LineLoc][1]))
            {
              NumberEnds++;
            }
          }
          LineLoc++;
          // Moves the lineloc to the position beyond the ned of the loop.
        }
      }

      else if ("end".equals(Code[LineLoc][0]) && "loop".equals(Code[LineLoc][1]))
      {
        // Does basically the same thing as the skipping loop section, except in
        // reverse.
        int NumberWhiles = 0;
        int NumberEnds = 1;
        while (NumberWhiles != NumberEnds)
        {
            LineLoc--;
            if ("while".equals(Code[LineLoc][0]))
            {
              NumberWhiles++;
            }
            if ("end".equals(Code[LineLoc][0]) && "loop".equals(Code[LineLoc][1]))
            {
              NumberEnds++;
            }          
        }
      }

      else if ("if".equals(Code[LineLoc][0])&&"bot".equals(Code[LineLoc][1]))
      {
    	int botNumber = mainMap.botListLoc(botName);
        int X = mainMap.botList.botList.get(botNumber).x; // Bot's current x coord
        int Y = mainMap.botList.botList.get(botNumber).y; // Bot's current y coord
        int condX = -1;
        int condY = -1;
        // These are the coordinates of the specified tile to search.
        Boolean BotInTile = false;
        // This checks if a bot is in a tile.
          if ("TL".equals(Code[LineLoc][3]))
          {
            condX = X-1;
            condY = Y+1;
          }
          if ("TC".equals(Code[LineLoc][3]))
          {
            condX = X;
            condY = Y+1;
          }
          if ("TR".equals(Code[LineLoc][3]))
          {
            condX = X+1;
            condY = Y+1;
          }
          if ("CL".equals(Code[LineLoc][3]))
          {
            condX = X-1;
            condY = Y;
          }
          if ("CR".equals(Code[LineLoc][3]))
          {
            condX = X+1;
            condY = Y;
          }
          if ("BL".equals(Code[LineLoc][3]))
          {
            condX = X-1;
            condY = Y-1;
          }
          if ("BC".equals(Code[LineLoc][3]))
          {
            condX = X;
            condY = Y-1;
          }
          if ("BR".equals(Code[LineLoc][3]))
          {
            condX = X+1;
            condY = Y-1;
          }
        // The switch function specifies where to search based on the given command.
        if (mainMap.map.get(condX).get(condY).bots.size() > 0)
        {
          BotInTile = true;
        }

        if (BotInTile == true)
        {
          LineLoc++;
        }
        if (BotInTile == false)
        {
          // If the conditions are not true then the program proceeds to the end of
          // the ifs.
          int NumberWhiles = 1;
          int NumberEnds = 0;
          while (NumberWhiles != NumberEnds)
          {
            // This particualr bit cheks the parity of the whiles seen and the end
            // ifs seen, if they are equal then the end of the loop has been reached.
            // This is to handle nested loops.
            LineLoc++;
            if ("if".equals(Code[LineLoc][0]))
            {
              NumberWhiles++;
            }
            if ("end".equals(Code[LineLoc][0]) && "if".equals(Code[LineLoc][1]))
            {
              NumberEnds++;
            }
          }
          LineLoc++;
          // Moves the lineloc to the position beyond the end of the loop.
        }
      }

      else if ("if".equals(Code[LineLoc][0])&&
      (
      "<".equals(Code[LineLoc][2])||
      ">".equals(Code[LineLoc][2])||
      "=".equals(Code[LineLoc][2])
      ) )
      {
        // If the if statement is true, the program proceeds. Else the program
        // skips to the end of the if statement.  The if statement is identical to
        // the while statement, the only difference is that the end if statement
        // does not return the lineloc to the top of the loop.
        int condition = Integer.parseInt( Variables.get(Code[LineLoc][1]).toString() );
        int variable = Integer.parseInt( Variables.get(Code[LineLoc][3]).toString() );

        if ("<".equals(Code[LineLoc][2])&&(condition < variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for less than.
          LineLoc ++;
        }

        else if (">".equals(Code[LineLoc][2])&&(condition > variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for greater than.
          LineLoc ++;
        }

        else if ("=".equals(Code[LineLoc][2])&&(condition == variable))
        {
          // If the conditions are true then the program proceeds to the next step.
          // This section looks for parity.
          LineLoc ++;
        }

        else
        {
          // If the conditions are not true then the program proceeds to the end of
          // the ifs.
          int NumberWhiles = 1;
          int NumberEnds = 0;
          while (NumberWhiles != NumberEnds)
          {
            // This particualr bit cheks the parity of the whiles seen and the end
            // ifs seen, if they are equal then the end of the loop has been reached.
            // This is to handle nested loops.
            LineLoc++;
            if ("if".equals(Code[LineLoc][0]))
            {
              NumberWhiles++;
            }
            if ("end".equals(Code[LineLoc][0]) && "if".equals(Code[LineLoc][1]))
            {
              NumberEnds++;
            }
          }
          LineLoc++;
          // Moves the lineloc to the position beyond the ned of the loop.
        }
      }

      else if ("end".equals(Code[LineLoc][0]) && "if".equals(Code[LineLoc][1]))
      {
        LineLoc++;
      }

      else
      {
        System.out.println("Syntax not recognised at "+Integer.toString(LineLoc+1));
        return "error";
      }

    }
    return "null";
  }

  public String removeLeadingSpaces(String w)
    {
	  /*
	  This function removes all leading spaces from a string, thus allowing for indents in
	  the code.  Code kindly borrowed from:
	  "https://howtodoinjava.com/java/string/remove-leading-whitespaces/"
	  */
        if (w == null) {
            return null;
        }
         
        if(w.isEmpty()) {
            return "";
        }
         
        int arrayIndex = 0;
        while(true)
        {
            if (!Character.isWhitespace(w.charAt(arrayIndex++))) {
                break;
            }
        }
        return w.substring(arrayIndex-1);
    }

}