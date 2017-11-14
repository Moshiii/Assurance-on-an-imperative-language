/**
   Write a method that finds the maximum value of a given array 'a'.
   Write pre- and post-condition for the method FindMax.
   
   Annonate your implementation with invariant and decreases annotations so that it verifies.
*/
method FindMax (a:array<int>)  returns (max : int)
  requires a != null 
  requires 0<a.Length
  ensures exists k:int :: 0 <= k < a.Length && max == a[k]
  ensures forall k:int :: 0 <= k < a.Length ==> a[k] <= max     
{
  max:=a[0];
  var i:int :=1;
  while(i < a.Length)
    invariant (i<=a.Length) && (forall k:int :: 0<=k<i ==> a[k]<=max) && (exists k:int :: 0<=k<i && max==a[k]) 
    decreases (a.Length-i); 
  {
    if(a[i] > max){max := a[i];}
    i := i + 1;
  }
  
} 
