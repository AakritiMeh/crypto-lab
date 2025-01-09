// hillciper and playcipher

// hill cipher
// c=pk mod26
// p=c(k ^-1)mod26
// k=[[9,4],[5,7]]
// p=MEET
// p=[[M,E],[E,T]] === [[12,4],[4,19]]
// c=(p*k) mod26
// p*k is a matrix multiplication
// here c=[[24,24],[1,19]]
// so c=[[Y,Y],[B,T]]

// k^-1= (adjoint(k) /det(k) ) mod26
// here det k= 43 mod 26
// det k=17

// adj k=[[7,-4],[-5,9]]
// k^-1=((1/17)*[[7,-4],[-5,9]])mod26
// 17^-1  * [[7,-4],[-5,9]] mod26
// so 17^-1 mod26 = apply extended eucledian algorithm

// extended eucledian method
//   Q A1 A2 A3 B1 B2 B3
//   - 1 0 26 0 1 1
//   1 0 1 17 1 -1 9
//   1 1 -1 9 -1 2 8
//   1 -1 2 8 2 -3 1

// since B3 is 1 so stop
// 17 ^-1 mod26 =23

// if u get any -ve value then add 26 to it
// 23 *[[7,-4],[-5,9]] mod26 = [[5,-14],[-11,25]]= [[5,12],[15,25]]
//
//  p= [[24,24],[1,19]] *[[5,12],[15,25]] mod26
