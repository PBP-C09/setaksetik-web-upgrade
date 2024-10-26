import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class Lab4p {
    private static InputReader in;
    private static PrintWriter out;
    public static int n, m;
    public static long[][] p;

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        in = new InputReader(inputStream);
        OutputStream outputStream = System.out;
        out = new PrintWriter(outputStream);

        n = in.nextInteger();
        m = in.nextInteger();
        p = new long[n+1][m+1];

        
        // n hari
        // m kota
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                p[i][j] = in.nextInteger();
            }
        }

        solve();
        out.close();
    }

    // n hari
    // m kota
    public static void solve() {
        long[][] dp = new long[n][m]; // buat max

        //hari pertama
        for (int j = 0; j < m; j++) {
            dp[0][j] = p[0][j];
        }

        for (int i = 1; i < n; i++) {
            for (int j = 0; j < m; j++) {
                
                dp[i][j] = dp[i-1][j] + p[i][j];

                if (j > 0) {
                    dp[i][j] = Math.max(dp[i][j], dp[i-1][j-1] + p[i][j]);
                }

                if (j < m - 1) {
                    dp[i][j] = Math.max(dp[i][j], dp[i-1][j+1] + p[i][j]);
                }
            }
        }

        long ans = 0;
        for (int j = 0; j < m; j++) {
            ans = Math.max(ans, dp[n-1][j]);
        }

        out.println(ans);
    }

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
