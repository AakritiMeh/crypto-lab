// substitution method - monoalphabetic (classical cipher)
// polyalphabetic cipher(types-vignere and vernam)
// playfail
// hill cipher
// one time pad

// transposition method
// rail fence
// row column transposition

// caeser cipher (aka shift cipher)
// k=shift value
// c=(p+k)mod26
// p=(c-k)mod26

// vignere
//  size of plain text !=size of key ; so key is repeated
// ci=(pi+ki)mod 26 (i=in subscript)
// pi=(ci-ki) mod26
// example:
// key= deceptive
// p=   wearediscovered
// kwy= deceptivedecept
// so key will be repeated and will become as: ^

//  vernam cipher
//  size of plain text =size of key  ; key is not repeated
// works on bits only
// ci=(pi Xor ki)mod 26 (i=in subscript)
// pi=(ci Xor ki) mod26
// example:
// P= HAI
// K= SAY
// C=((H XOR S) ...)
// H XOR S:  7 XOR 18 = 00111 XOR 10010 = 10101 = 21 = V
// I XOR Y: = Q
// A XOR A =0 = A
// decryption:
// K=SAY
// C=VAQ
// p= ((S xor V)...)
// S XOR V= 18 XOR 21 = 7 = H

// bitwise XOR is done
