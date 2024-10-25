import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.StringTokenizer;

public class TemplateLab4 {
    private static InputReader in;
    private static PrintWriter out;
    public static int n, m;
    public static long p[][];


    public static void main(String[] args) {
		InputStream inputStream = System.in;
		in = new InputReader(inputStream);
		OutputStream outputStream = System.out;
		out = new PrintWriter(outputStream);

		n = in.nextInteger();
		m = in.nextInteger();
		
		for (int i = 1; i <= m; i++) {
			for (int j = 1; j <= n; j++) {
				p[i][j] = in.nextInteger();
			}
		}

		solve();
		long ans = 0;
		
		out.println(ans);
		out.close();
    }

    public static void solve() {
		// TODO
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