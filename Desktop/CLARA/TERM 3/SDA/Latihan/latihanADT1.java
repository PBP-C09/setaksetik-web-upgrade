import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.Scanner;
import java.util.Set;

public class latihanADT1 {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        System.out.print("Input: ");
        String input = in.nextLine();

        ArrayList<Character> hurufSet = new ArrayList<>();
        ArrayList<Character> buang = new ArrayList<>();
        for (int i = 0; i < input.length(); i++){
            Character now = input.charAt(i);
            if (!hurufSet.contains(now) && !buang.contains(now)){
                hurufSet.add(now);
            } else{
                buang.add(now);
                hurufSet.remove(now);
            }
        }
        System.out.println("Output: " + hurufSet.get(0));
    }
}
