-------------------------
-------- PART A --------- 
-------------------------

type Var = String

data Term =
    Variable Var
  | Lambda   Var  Term
  | Apply    Term Term
  deriving Eq
-- I've included the extra term Eq to allow for terms to be equated to each other.

instance Show Term where
  show = pretty
-- Uncommented to automatically print show.

example :: Term
example = Lambda "a" (Lambda "x" (Apply (Apply (Lambda "y" (Variable "a")) (Variable "x")) (Variable "b")))

pretty :: Term -> String
pretty = f 0
    where
      f i (Variable x) = x
      f i (Lambda x m) = if i /= 0 then "(" ++ s ++ ")" else s where s = (showString "\\" []) ++ x ++ ". " ++ f 0 m 
      f i (Apply  n m) = if i == 2 then "(" ++ s ++ ")" else s where s = f 1 n ++ " " ++ f 2 m


------------------------- Assignment 1

numeral :: Int -> Term
numeral n = Lambda "f" (Lambda "x" (recursiveNumeral n))
-- This creates a churh numeral from an int.

recursiveNumeral :: Int -> Term
recursiveNumeral 0 = Variable "x"
recursiveNumeral n = Apply (Variable "f") (recursiveNumeral (n-1))
-- This function does the recursive applying for numeral.

-------------------------

merge :: Ord a => [a] -> [a] -> [a]
merge xs [] = xs
merge [] ys = ys
merge (x:xs) (y:ys)
    | x == y    = x : merge xs ys
    | x <= y    = x : merge xs (y:ys)
    | otherwise = y : merge (x:xs) ys


------------------------- Assignment 2

stringAppend :: (Char,Int) -> String
stringAppend (letter,number) 
    | number == 0 = [letter]
    | otherwise = [letter] ++ show(number)
-- This is to append an int to the end of a char.

charPlusNum :: [Char] -> [Int] -> [String]
charPlusNum letters numbers = map stringAppend (zip letters numbers)
-- This is to append the ints and chars in two lists to make a list of strings.

genVariables :: Int -> [String]
genVariables n = (charPlusNum ['a','b'..'z'] (replicate 26 n)) ++ genVariables (n+1)
-- Generates an infinite list of form an,bn..zn,an+1,bn+1..zn+1..an+m,bn+m..zn+m .

variables :: [Var]
variables = genVariables 0
-- Generates variables.

filterVariables :: [Var] -> [Var] -> [Var]
filterVariables list removingElems = filter (`notElem` removingElems) list
-- Removes elements from list given a list of elements to remove

fresh :: [Var] -> Var
fresh removingelements = (filterVariables variables removingelements) !! 0
-- Creates a new variable that is not in the given list.

usedList :: Term -> [Var]
usedList = f 0
    where
      f i (Variable x) = [x]
      f i (Lambda x m) = if i /= 0 then s else s where s = [x] ++ f 0 m 
      f i (Apply  n m) = if i == 2 then s else s where s = f 1 n ++ f 2 m
-- Reuses the code from pretty to create a list of the variables.  !!! Maybe rewrite to be more consistent.

unique :: [Var] -> [Var]
unique [] = []
unique (x:xs) =  merge [x] (unique (filter (/=x) xs))
-- Adds the elments  from a list into an orderded list whilst excluding duplicates.

used :: Term -> [Var]
used term = unique (reverse(usedList term))
-- Takes a term and creates an ordered list of the veriables.

------------------------- Assignment 3

rename :: Var -> Var -> Term -> Term
rename x y (Variable z)
    | x == z = Variable y
    | otherwise = Variable z
rename x y (Lambda z n)
    | x == z = Lambda y (rename x y n)
    | otherwise = Lambda z (rename x y n)
rename x y (Apply n m) = Apply (rename x y n) (rename x y m)
-- Replaces one variable with another.

substitute :: Var -> Term -> Term -> Term
substitute x n (Variable y)
    | x == y = n
    | otherwise = Variable y
substitute x n (Lambda y m)
    | x == y = (Lambda y m)
    | otherwise = let z = fresh ((used n)++(used m)++[x]) in Lambda z (substitute x n (rename y z m))
substitute x n (Apply m1 m2) = Apply (substitute x n m1) (substitute x n m2)
-- Implements capture-avoiding substitution.

------------------------- Assignment 4

betaAll :: Term -> [Term]
-- Allows both routes either making the substitution or not
betaAll (Apply (Lambda x n) m) = [substitute x m n] ++ (map ((flip Apply) m) (map (Lambda x) (betaAll n))) ++ (map (Apply (Lambda x n)) (betaAll m))
betaAll (Variable x) = [(Variable x)]
betaAll (Lambda x n) = map (Lambda x) (betaAll n)
-- Allows both routes either N1M->N2M or MN1 -> MN2
betaAll (Apply n m) =  (map ((flip Apply) m) (betaAll n)) ++ (map (Apply n) (betaAll m))
-- This creates all possible beta reductions, note that this may not be unique and has the initial.
-- This always puts the leftmost at the start of the list.

uniqueTerms :: [Term] -> [Term]
uniqueTerms [] = []
uniqueTerms (x:xs) =  [x] ++ (uniqueTerms (filter (/=x) xs))
-- This allows for non unique terms to be removed from a a list of terms.

beta :: Term -> [Term]
beta term = filter (/=term) (uniqueTerms (betaAll term))
-- This wraps up betaAll to remove unique terms, and the input terms from the output list of betaAll.

normalize :: Term -> IO ()
normalize term =
    let termList = beta term
        in do { print (pretty term)
              ; if termList == []
                    then print ""
                    else normalize (head termList)
              }
-- This one prints out the normalizing sequence in normal order.

------------------------- 

a_betaAll :: Term -> [Term]
-- Allows both routes either making the substitution or not
a_betaAll (Apply (Lambda x n) m) = [substitute x m n] ++ (map (Apply (Lambda x n)) (a_betaAll m)) ++ (map ((flip Apply) m) (map (Lambda x) (a_betaAll n)))
a_betaAll (Variable x) = [(Variable x)]
a_betaAll (Lambda x n) = map (Lambda x) (a_betaAll n)
-- Allows both routes either N1M->N2M or MN1 -> MN2
a_betaAll (Apply n m) = (map (Apply n) (a_betaAll m)) ++ (map ((flip Apply) m) (a_betaAll n))
-- This creates all possible beta reductions, note that this may not be unique and has the initial.
-- The order always puts the leftmost one as the last element in the list.

a_beta :: Term -> [Term]
a_beta term = reverse (filter (/=term) (uniqueTerms (a_betaAll term)))
-- By reversing the list direction applicative order reduction happens as betaAll puts the innermost in last.

a_normalize :: Term -> IO ()
a_normalize term =
    let termList = a_beta term
        in do { print (pretty term)
              ; if termList == []
                    then print ""
                    else a_normalize (head termList)
              }
-- Identical to normalize but works on the reversed list from a_beta

-------------------------

example1 :: Term
example1 = Apply (numeral 3) (numeral 3)
-- Requires many more steps in normal order than applicative order

example2 :: Term
example2 = Apply (numeral 0) (Apply (numeral 0) (numeral 0))
-- Requires one less step for normal order over applicative order

-------------------------
-------- PART B --------- 
-------------------------


------------------------- Assignment 5 (PAM)

type PState = (Term , [Term])
-- This is the tuple of the current term and a stack of terms, called the state.

prettyPState :: PState -> IO ()
prettyPState (term, termList) = print ((pretty term), (map pretty termList))
-- This allows pretty to be applied to a state, making it output as shown in the pdf.

prettyPStateTerm :: PState -> IO ()
prettyPStateTerm (term, termList) = print (pretty term)
-- This only prints the term of a PState.

-------------------------

state1 = (Lambda "x" (Lambda "y" (Variable "x")) , [Variable "Yes", Variable "No"])

term1 = Apply (Apply (Lambda "x" (Lambda "y" (Variable "x"))) (Variable "Yes")) (Variable "No")

term2 = Apply (Apply (Lambda "b" (Apply example (Variable "Yes"))) (Lambda "z" (Variable "z"))) (Variable "No")

-------------------------

p_start :: Term -> PState
p_start term = (term, []) :: PState
-- This makes a turn initial.

p_step :: PState -> PState
p_step ((Lambda x n), s) = ((substitute x (head s) n), (tail s)) :: PState
p_step ((Apply n m), s) = (n, [m] ++ s) :: PState
-- This performs one transition step.

p_final :: PState -> Bool
p_final ((Lambda x n), s) = if s == [] then True else False
p_final ((Variable x), s) = True
p_final (n, s) = False
-- This checks to see if a state is final.

p_runInitial :: PState -> IO ()
p_runInitial pState =
    let pStateNext = p_step pState
        in do { (prettyPState pState)
              ; if (p_final pState)
                    then print (pretty (p_readback pState))
                    else p_runInitial pStateNext
              }
-- This performs a run on an initial state.

p_run :: Term -> IO ()
p_run term = p_runInitial (p_start term)
-- This wraps up p_runInitial to take a term not a state.

p_readback :: PState -> Term
p_readback (term, []) = term
p_readback (term, termList) = Apply (p_readback ((term, (tail termList)) :: PState)) (head termList)
-- MAYBE REVISE TO SORT OUT ORDER

------------------------- Assignment 6 (KAM)

newtype Env = MakeEnv [(Var, Term, Env)]
-- Recursive definition of the environment E, which is  stack of triples (x, N, E)
-- Note that the first term is always simply a variable.
-- Note that MakeEnv is the constructor

newtype State = MakeState (Term, Env, [(Term, Env)])
-- This defines a state for the KAM, the the first term is N, second is E, third is S.

-------------------------

state2Env = MakeEnv [("y" , (Lambda "z" (Variable "z")) , MakeEnv [])]
state2Term = (Apply (Lambda "x" (Variable "x")) (Variable "y"))
state2 = MakeState ( state2Term , state2Env , [] ) :: State

state3Env = MakeEnv [("x" , (Lambda "x" (Apply (Variable "x") (Variable "x"))) , MakeEnv [])]
state3Term = (Apply (Variable "x") (Variable "x"))
state3 = MakeState ( state3Term , state3Env , [] ) :: State

state4Env = MakeEnv []
state4Term = (Lambda "y" (Variable "x"))
state4Env0 = MakeEnv [("b" , (Variable "c") , MakeEnv [])]
state4Env1 = MakeEnv [("z" , (Lambda "a" (Variable "b")) , state4Env0)]
state4 = MakeState (state4Term, state4Env, [((Variable "z"), state4Env1)])

-------------------------

lengthEnv :: Env -> Int
lengthEnv (MakeEnv []) = 0
lengthEnv (MakeEnv ((var, term, env):xs)) = 1 + lengthEnv ((MakeEnv xs))
-- Calculates the number of items in an env list.

dispEnv :: Env -> Env -> String
dispEnv (MakeEnv []) envCheck
    | (lengthEnv envCheck) == 0 = "[]"
    | otherwise = "]"
dispEnv (MakeEnv ((var, term, env):xs)) envCheck
    | (length xs) == (lengthEnv envCheck)-1 = "[(" ++ var ++ "," ++ (pretty term) ++ "," ++ (dispEnv env env) ++ ")" ++ (dispEnv (MakeEnv xs) envCheck)
    | (length xs) == 0 = ",(" ++ var ++ "," ++ (pretty term) ++ "," ++ (dispEnv env env) ++ ")" ++ (dispEnv (MakeEnv xs) envCheck)
    | otherwise = ",(" ++ var ++ "," ++ (pretty term) ++ "," ++ (dispEnv env env) ++ ")," ++ (dispEnv (MakeEnv xs) envCheck)
-- This takes an environment and converts it into a string to be printed

dispClosure :: [(Term, Env)] -> Int -> String
dispClosure [] lengthList
    | lengthList == 0 = "[]"
    | otherwise = "]"
dispClosure ((term, env):xs) lengthList
    | lengthList == (length xs)+1 = "[(" ++ (pretty term) ++ (dispEnv env env) ++ ")" ++ (dispClosure xs lengthList)
    | otherwise = ",(" ++ (pretty term) ++ (dispEnv env env) ++ ")" ++ (dispClosure xs lengthList)
-- This takes a closure and converts it into a string to be printed.

dispState :: State -> String
dispState (MakeState (term, env, closure)) = "(" ++ (pretty term) ++ "," ++ (dispEnv env env) ++ "," ++ (dispClosure closure (length closure)) ++ ")"
-- This takes a state and converts it into a string to be printed.

dispStateTerm :: State -> String
dispStateTerm (MakeState (term, env, closure)) = pretty term
-- This takes a state and returns a string of the term.

instance Show State where show state = show (dispState state)
-- This override the default show for env.

instance Show Env where show env = show (dispEnv env env)
-- This override the default show for env.

-- I would like to apologise for my absolute hack of the show functions, it is by far the ugliest haskell code I've ever written... May you forgive me.

-------------------------

start :: Term -> State
start term = MakeState (term, (MakeEnv []), [])
-- Turns a term into a start state.

deEnv :: Env -> [(Var, Term, Env)]
deEnv (MakeEnv []) = []
deEnv (MakeEnv ((var, term, env):xs)) = (var, term, env) : (deEnv (MakeEnv xs))
-- Takes a env type and de-types it into a list of triples.

addEnv :: (Var, Term, Env) -> Env -> Env
addEnv (var, term, env0) env1 = MakeEnv ( (var, term, env0) : (deEnv env1) )
-- Adds a new term to a env list.

step :: State -> State
step (MakeState ( (Variable x) , (MakeEnv ((y, n, f):xs)) , s ) )
    | x == y = MakeState ( n , f , s )
    | otherwise = MakeState ( (Variable x) , (MakeEnv xs) , s )
step (MakeState ( (Lambda x n) , e , ((m, f):xs) ) ) = MakeState ( n , (addEnv (x,m,f) e) , xs )
step (MakeState ( (Apply n m) , e , s) ) = MakeState ( n , e , (( m , e ):s))
-- Perfroms a transition step for a KAM

final :: State -> Bool
final (MakeState ( (Lambda x n) , e , [] ) ) = True
final (MakeState ( (Variable x) , (MakeEnv []) , s ) ) = True
final s = False
-- Checks to see ff a state is final or not.

runInitial :: State -> IO ()
runInitial state =
    let stateNext = step state
        in do { (print state)
              ; if (final state)
                    then print (pretty (readback state))
                    else runInitial stateNext
              }
-- This performs a run on an initial state.

run :: Term -> IO ()
run term = runInitial (start term)
-- Runs a sequence of applications.

termFromClosure :: (Term, Env) -> Term
termFromClosure ( (Variable x) , (MakeEnv []) ) = (Variable x)
termFromClosure ( (Variable x) , (MakeEnv ((y, n, e):xs)) )
    | x == y = termFromClosure (n , e)
    | otherwise = termFromClosure ((Variable x), (MakeEnv xs))
termFromClosure ( (Lambda x n) , e ) = Lambda x (termFromClosure (n , (addEnv (x , (Variable x) , (MakeEnv [])) e)))
termFromClosure ((Apply n m) , e) = Apply (termFromClosure  (n , e)) (termFromClosure (m , e))
-- Recursively creates a term given a closure.

applyStack :: [(Term, Env)] -> Term
applyStack [] = Variable "" -- SuperSketch but okay because of guard in read back.
applyStack [(term, env)] = termFromClosure (term , env)
applyStack ((term, env):xs) = Apply (termFromClosure (term , env)) (applyStack xs)
-- Applies a stack together.

readback :: State -> Term
readback (MakeState (n , env , stack)) 
    | length stack == 0 = (termFromClosure (n, env))
    | otherwise = Apply (termFromClosure (n, env)) (applyStack stack)
-- Applies the entirety of a state with each other.