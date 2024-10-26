import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;

public class LatihanADT2 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Meminta input untuk siswa dan menu dalam satu kali input
        System.out.print("Masukkan input (contoh: siswa = [1,1,0,0], menu = [0,1,0,1]): ");
        String input = scanner.nextLine();

        // Memisahkan input menjadi dua bagian, siswa dan menu
        String[] parts = input.split(", menu = ");
        String siswaInput = parts[0].replace("siswa = ", "").replaceAll("[\\[\\]]", "");
        String menuInput = parts[1].replaceAll("[\\[\\]]", "");

        // Konversi input menjadi array
        int[] siswa = convertInputToArray(siswaInput);
        int[] menu = convertInputToArray(menuInput);

        // Panggil metode untuk menghitung jumlah siswa yang tidak bisa makan
        int result = countStudentsWhoCannotEat(siswa, menu);

        // Cetak hasilnya
        System.out.println("Jumlah siswa yang tidak bisa makan: " + result);

        scanner.close();
    }

    // Metode untuk mengonversi input string ke array integer
    public static int[] convertInputToArray(String input) {
        String[] inputStrings = input.split(",");
        int[] array = new int[inputStrings.length];
        for (int i = 0; i < inputStrings.length; i++) {
            array[i] = Integer.parseInt(inputStrings[i].trim());
        }
        return array;
    }

    // Metode untuk menghitung jumlah siswa yang tidak bisa makan
    public static int countStudentsWhoCannotEat(int[] siswa, int[] menu) {
        // Buat Queue untuk siswa dan Stack untuk menu
        Queue<Integer> antrianSiswa = new LinkedList<>();
        Stack<Integer> tumpukanMenu = new Stack<>();

        // Isi Queue siswa
        for (int s : siswa) {
            antrianSiswa.offer(s);
        }

        // Isi Stack menu
        for (int i = menu.length - 1; i >= 0; i--) {
            tumpukanMenu.push(menu[i]);
        }

        int counter = 0; // Untuk menghitung jumlah iterasi yang gagal

        while (!antrianSiswa.isEmpty() && counter < antrianSiswa.size()) {
            if (antrianSiswa.peek() == tumpukanMenu.peek()) {
                // Jika preferensi siswa cocok dengan menu teratas
                antrianSiswa.poll(); // Siswa mengambil menu dan keluar dari antrian
                tumpukanMenu.pop();  // Menu diambil dari tumpukan
                counter = 0; // Reset counter
            } else {
                // Jika tidak cocok, siswa pindah ke belakang antrian
                int siswaDepan = antrianSiswa.poll();
                antrianSiswa.offer(siswaDepan);
                counter++;
            }
        }

        // Jumlah siswa yang tidak bisa makan adalah yang tersisa dalam antrian
        return antrianSiswa.size();
    }
}
  