import java.util.*;
import java.io.*;
public class Time {
    public static long get_time() {
        String cmd = "python3 python/timing.py";
        try {
            Process p = Runtime.getRuntime().exec(cmd);
            BufferedReader inp = new BufferedReader(new InputStreamReader(p.getInputStream()));
            return Long.parseLong(inp.readLine());
            
        }catch(IOException e){
            e.printStackTrace();
        }
        return -1L;
    }
}
