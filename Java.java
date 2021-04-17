// Create a Main class
public class Main {

  // Create a fullThrottle() method
  public void fullThrottle ( ) {
    System . out . println ( "The car is going as fast as it can! " ) ;
  }

  public void speed ( String maxSpeed ) {
    System . out . println ( "Max speed is: " + maxSpeed ) ;
  }


  public static void main ( String [ ] args ) {

    Main myCar = new Main ( ) ;

    myCar . fullThrottle ( ) ;

    myCar . speed ( "200" ) ;
  }
} ;
