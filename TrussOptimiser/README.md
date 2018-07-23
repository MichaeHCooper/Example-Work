We were tasked as part of one of our university modules to design the most effecient
possible truss to be laser cut out MDF as part of an in class competition.  Obviously
this is a very difficult question to answer, everyone else just spent lots of time
googling and checking lots of trusses by hand, I used a slightly different method.

I realised that this is a problem well suited to using a genetic algorithm so I built
a two part program, the first is a statically determinate solver, the second a genetic
optimiser.  Ultimately I went throuh several revisions to get the required speed to
effeciently search through enough trusses, several modifications were made to the solver
specifically using linear algebra instead of performing rotations as you would do by hand,
and performing the taylor expansion by hand of an equation to get faster solutions.

Ultimately the truss I cut out that was designed by the software beat everyone else by a
very wide margin and is currently displayed in my lecturers office!

The picture is the truss that was designed by my program (The wierd arch one) and the
other one is typical of what most people designed, for those not fammiliar with truss design.
