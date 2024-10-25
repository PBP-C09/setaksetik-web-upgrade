import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class Lab2p {
    private static InputReader in;
    private static PrintWriter out;

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        in = new InputReader(inputStream);
        OutputStream outputStream = System.out;
        out = new PrintWriter(outputStream);
        // System.out.print("Teks: ");
        String kata = in.next();
        System.out.println(solve(kata));
        out.close(); 
    }

    // taken from https://codeforces.com/submissions/Petr
    // together with PrintWriter, these input-output (IO) is much faster than the
    // usual Scanner(System.in) and System.out
    // please use these classes to avoid your fast algorithm gets Time Limit
    // Exceeded caused by slow input-output (IO)
    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 32768);
            tokenizer = null;
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public int nextInteger() {
            return Integer.parseInt(next());
        }
    }


    public static long solve(String kata) {
        char[] charArray = kata.toCharArray();
        int hitungS = 0;
        int hitungSD = 0;
        int hitungSDA = 0;
        for (int i = 0; i < kata.length(); i++){
            char c = kata.charAt(i);
            char s = 's';
            char d = 'd';
            char a = 'a';
            if (c == s){
                hitungS += 1;
            }
            else if (c == d && kata.charAt(i-1)!= s){
                hitungSD += hitungS;
            } 
            else if (c == a){
                hitungSDA += hitungSD;
            }
        }
        
        // int hitungKataSebelahan = 0;
        // for (int j = 0; j < kata.length(); j++){
        //     String sebelahan1 = "sd";
        //     String sebelahan2 = "da";
        //     String duahuruf = kata.charAt(j) + kata.charAt(j+1);
        //     if (dua)
        // }

        return hitungSDA;
    }
}