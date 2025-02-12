public class testOriginal {

    public int add(int a, int b) {
        return a + b;
    }

    int addCheck(int a, int b) {
        if (a > 0 && b > 0) {
            return a + b + a;
        } else {
            return a + b;
        }
    }

    protected static void print(String a) {
        System.out.println(a);
    }

    void printTwice(String a) {
        System.out.println(a);
        System.out.println(a);
    }

    public static void main(String[] args) {
        int one = 1;
        int two = 2;

        String apple = "apple";

        testOriginal a = new testOriginal();

        int result = a.add(one, two);

        if (result == 1) {
            System.out.println("one");
        } else if (result == 2) {
            System.out.println("two");
        } else {
            System.out.println("other");
        }

        switch (result) {
            case 1:
                System.out.println("one");
                break;
            case 2:
                System.out.println("two");
                break;
            case 3:
                System.out.println("three");
                break;
            default:
                System.out.println("other");

                int count = 0;

                do {
                    System.out.println(count);
                    count++;
                } while (count < 10);

                for (int i = 0; i < apple.length(); i++) {
                    System.out.println(apple.charAt(i));

                    int count2 = 0;
                    while (count2 < 9) {
                        System.out.println(apple);
                        count2++;
                    }

                    // Big nested test
                    if (result == 3) {
                        if (apple == "apple") {
                            if (true) {
                                System.out.println("all true");
                            }
                        } else if (apple == "banana") {
                            System.out.println("Not true");
                        }
                    } else {
                        System.out.println("other");
                    }
                }
        }
    }
}
