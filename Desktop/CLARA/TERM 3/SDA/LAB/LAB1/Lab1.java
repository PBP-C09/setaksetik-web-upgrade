import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class Lab1 {
    private static InputReader in;
    private static PrintWriter out;

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        in = new InputReader(inputStream);
        OutputStream outputStream = System.out;
        out = new PrintWriter(outputStream);

        // Read inputs
        long N = in.nextInteger();
        long M = in.nextInteger();
        long K = in.nextInteger();
        long X = in.nextInteger();
        long Y = in.nextInteger();

        long A[] = new long[(int)K];
        long B[] = new long[(int)K];

        for (int i = 0; i < K; i++) {
            A[i] = in.nextInteger();
            B[i] = in.nextInteger();
        }

        long posisiOriginalSofita = ((X-1)*M) + Y ;
        // System.out.println("posisi ori:" +posisiOriginalSofita);


        long kursiKosong = 0;
        for (int j = 0; j<K; j++){
            if (A[j] < X){
                // System.out.println("ini baris sofita " + X);
                // System.out.println(A[j]);   
                kursiKosong += 1;
                // System.out.println("ini kursikosong semengtara "+ kursiKosong);
            } else if (A[j] == X){
                if (B[j] < Y){
                    // System.out.println("ini BJ nya" + B[j]);
                    kursiKosong += 1;
            }

                    // System.out.println("ini  kursi kosong di barisnya" + kursiKosong);
                
            }

        }
        // System.out.println("ini kursi kosong final" + kursiKosong);

        long ans = 0;
        if (K == 0){
            // System.out.println("nih");
            ans = posisiOriginalSofita;
        } else{
            ans = posisiOriginalSofita - kursiKosong;
        }

        System.out.println(ans);


        // TODO: Write your code here
        // ! Hint:  Note that to get the full score, you might need to edit other parts of the code as well

        // don't forget to close/flush the output
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
}