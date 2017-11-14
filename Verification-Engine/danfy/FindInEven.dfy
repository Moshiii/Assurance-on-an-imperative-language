/* The method findInEven (a, x) either returns an index r of array a such that 
    (a) r is even
    (b) the value of cell r of a is x
   Otherwise, it returns -1. 
   The method assumes that the array a is non-null.

   Write pre- and post-conditions for the method.
   Annotate the loop with invariants such that the method verifies.
*/
method findInEven (a: array<int>, x:int) returns (r:int)
  requires a != null
  
  ensures 0<=r ==> r%2==0 &&  r< a.Length && a[r] == x 
  ensures r<0 ==> forall k :: 0 <= k < a.Length && k%2==0 ==> a[k] != x
{
  r := -1;
  var i := 0;
  while (i < a.Length)
    invariant 0 <= i<= a.Length+1 && i%2==0    
    invariant r<0 ==> forall k :: 0 <= k < i && k%2==0 ==> a[k] != x
    invariant 0<=r ==> r%2==0 &&  r< a.Length && a[r] == x
  {
    if (x == a[i]) { r := i;return; }
    i := i + 2;
  }
  return;
}
