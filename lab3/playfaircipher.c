// aka multicipher encryption technique
// Plaintext diagrams to ciphrtext diagram

// we take 5 X 5 matrix - no repetitopn of characters
//  example - Key = MONARCHY
//  key matrix
//  M O N A   R
//  C H Y B   B
//  E F G I/J K
//  L P Q S   T
//  V Y W X   Z

// two chars I/J in same cell (since we have to fill all eng characters into this)
// plaintext = BA | LL | OO| N
// we split the plaintext
// since LL are same
// so we put filler character X
// BA LX LO ON

// RULES OR STEPS

// plaintext to diagram

// if 2 characters in the plaintext fall in the same row
// then each characer then each will be replced by the letter
// to the right with the firt letter circulating example - AR will be => RM
// for Eg: MA =>OR

// if two characters fall on the same column them we have to take the letter below it
// for eg: ME => CL
// for eg : NW => YN

// Each Plaintext letter in a plain is replaced by the letter that lies in its own row and column occupied by other plaintext character
// eg: HS => BP
// eg: EA => IM or JM
