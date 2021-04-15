// Create a Main class
public class Main {

  // Create a fullThrottle() method
  public void fullThrottle ( ) {
    System . out . println ( "The car is going as fast as it can! " ) ;
  }

 
  // Inside main, call the methods on the myCar object
  public static void main ( String [ ] args ) {
    // Create a myCar object
    Main myCar = new Main ( ) ;
    // Call the fullThrottle() method
    myCar . fullThrottle ( ) ;
    // Call the speed() method
    myCar . speed ( "200" ) ;
  }
} ;

