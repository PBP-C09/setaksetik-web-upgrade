import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.Stack;
import java.util.StringTokenizer;

public class Lab3ON {
    private static InputReader in;
    private static PrintWriter out;

    public static void main(String[] args) {
        InputStream inputStream = System.in;
        in = new InputReader(inputStream);
        OutputStream outputStream = System.out;
        out = new PrintWriter(outputStream);

        // Read inputs
        int N = in.nextInteger();
        long[] heights = new long[N]; // Use 'long' to handle large heights

        for (int i = 0; i < N; i++) {
            heights[i] = in.nextLong(); // Reading heights up to 10^9
        }

        // Call the function to calculate the number of visible people
        int[] result = calculateVisiblePeople(N, heights);

        // Output the result
        for (int i = 0; i < N; i++) {
            out.print(result[i] + " ");
        }

        // Don't forget to close/flush the output
        out.close();
    }

    // Function to calculate the number of visible people to the right using a stack
    public static int[] calculateVisiblePeople(int N, long[] heights) {
        int[] result = new int[N]; // Array to store the result
        Stack<Integer> stack = new Stack<>(); // Stack to store indices

        // Process each person from right to left
        for (int i = N - 1; i >= 0; i--) {
            // Count how many people can be seen
            int visibleCount = 0;
            
            // Pop from the stack all people that are shorter than or equal to the current person
            while (!stack.isEmpty() && heights[stack.peek()] <= heights[i]) {
                stack.pop();
                visibleCount++;
            }
            
            // If there are still people in the stack, one more person can be seen (the taller one)
            if (!stack.isEmpty()) {
                visibleCount++;
            }
            
            result[i] = visibleCount;
            
            // Push the current person's index onto the stack
            stack.push(i);
        }

        return result;
    }

    // Helper class for fast input
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

        public long nextLong() {
            return Long.parseLong(next());
        }
    }
}