import java.io.*;
public class Util {
    public static int[] get_LUT(boolean x) {
        int[] LUT = new int[0x1000000];
        for(int i = 0; i<0x1000000; i++) {
            LUT[i] = i;
        }
        if(!x) return LUT;
        try {
            BufferedReader br = new BufferedReader(new FileReader(new File("LUT/table.data")));
            for(int i = 0; i<0x1000000; i++) {
                String line = br.readLine();
                LUT[i] = Integer.parseInt(line);
            }
        }catch(Exception e) {}
        return LUT;
    }
    public static void ensure_LUT() {
        File lut_file = new File("LUT/table.data");
        if(!lut_file.exists()){
            File lut_dir = new File("LUT");
            if(!lut_dir.exists()) lut_dir.mkdirs();
            
            String cmd = "python3 python/gen_table.py";
            try {
                Process p = Runtime.getRuntime().exec(cmd);
                BufferedReader inp = new BufferedReader(new InputStreamReader(p.getInputStream()));
                String line = inp.readLine();
                while(line != null) {
                    System.out.println(line);
                    line = inp.readLine();
                }
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }
}
