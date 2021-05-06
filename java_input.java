// Create a NumKit class
class NumKit {
  //Recursive number power method.

  public int power(int num, int base){
    if(base == 0)
    {
        return 1;
    }
    else
    {
        int x = this.power(num, base - 1);
        return num * x;
    }
  }
    public int product(int a, int b) {
        if (a > 1) {
          return a + this.product(a, b - 1);
        }
        if (b == 0) {
          return 0;
        }
        else{
            return 1;
        }
    }
    public Boolean isPrime(int n)
    {
        // Corner case
        if (n <= 1){
            return false;
        }
        // Check from 2 to n-1
        for (int i = 2; i < n; i++) {
            if (n % i == 0){
                return false;
            }
        }

        return true;
    }

  // Create a isEven method to check if number is even/odd
  public String isEven(int a){
        String temp;
        if(a % 2 == 0)
        {
            temp = "Even";
            return temp;
        }
        else {
            temp = "Odd";
            return temp;
        }
  }
};

class MathNode {
    int data;
    String description;
    MathNode next;
    public MathNode(int data, String desc)
    {
        this.data = data;
        this.description = desc;
    }

    public void setNext(MathNode next)
    {
        this.next = next;
    }

    public void printList()
    {
        MathNode x = this;
        if(this.next != null){
            x = this.next;
        }
        System.out.println("\nYour Math Nodes: \n");
        while (x.next != null)
        {
            int d = x.data;
            String s = x.description;
            System.out.println("   "+ d + " | " + s);
            x = x.next;
        }
    }

};

class Main {

  // Inside main, call the methods square and isEven
  public static void main(String[] args){
    //Create Objects and Vars
    NumKit n = new NumKit();

    //Create Linked List of math nodes
    MathNode head = new MathNode(0, "root");
    MathNode cursor = head;
    for(int i = 0; i < 50; i++) {
        MathNode o;
        int temp;
        String stri;
        boolean flag;
        switch (i%7) {
            case 5:
                temp = n.power(i, i%7);

                cursor.setNext(new MathNode(temp, "power"));
                cursor = cursor.next;
                break;
            case 6:
                stri = n.isEven(i);
                cursor.setNext(new MathNode(i, stri));
                cursor = cursor.next;
                break;
            case 3:
                flag = n.isPrime(i);
                if (flag) {
                    cursor.setNext(new MathNode(i, "prime number"));
                }
                else{
                    cursor.setNext(new MathNode(i, "non-prime number"));
                }
                cursor = cursor.next;
        }
    }

    head.printList();

  }
};






